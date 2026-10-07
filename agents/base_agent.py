"""
APEX — Base Agent
Shared Claude client and JSON extraction utilities.
"""

from __future__ import annotations

import json
import logging
import os
import re
from typing import Any, Dict, Type, TypeVar

import anthropic
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

from config import config

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


class BaseAgent:

    def __init__(self, model: str | None = None, max_tokens: int | None = None):
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.model = model or config.CLAUDE_PRIMARY_MODEL
        self.max_tokens = max_tokens or config.MAX_TOKENS

    # Newer anthropic SDKs dropped `temperature` from messages.create(). Send it
    # when the installed SDK accepts it; otherwise retry once without it.
    _supports_temperature = True

    def _kwargs(self, system: str, user: str, temperature: float) -> dict:
        kw = dict(
            model=self.model,
            max_tokens=self.max_tokens,
            system=system,
            messages=[{"role": "user", "content": user}],
        )
        if BaseAgent._supports_temperature:
            kw["temperature"] = temperature
        return kw

    @staticmethod
    def _is_temperature_error(e: Exception) -> bool:
        return "temperature" in str(e)

    @staticmethod
    def _text(message) -> str:
        return "".join(getattr(b, "text", "") for b in message.content)

    def _call(self, system: str, user: str, temperature: float = 0.0) -> str:
        try:
            message = self.client.messages.create(**self._kwargs(system, user, temperature))
        except (TypeError, anthropic.BadRequestError) as e:
            if not (BaseAgent._supports_temperature and self._is_temperature_error(e)):
                raise
            logger.warning("SDK/model rejects temperature, retrying without it")
            BaseAgent._supports_temperature = False
            message = self.client.messages.create(**self._kwargs(system, user, temperature))
        return self._text(message)

    def _stream_once(self, system: str, user: str, temperature: float) -> str:
        full_text = ""
        with self.client.messages.stream(**self._kwargs(system, user, temperature)) as stream:
            for text in stream.text_stream:
                full_text += text
        return full_text

    def _call_streaming(self, system: str, user: str, temperature: float = 0.0) -> str:
        try:
            return self._stream_once(system, user, temperature)
        except (TypeError, anthropic.BadRequestError) as e:
            if not (BaseAgent._supports_temperature and self._is_temperature_error(e)):
                raise
            logger.warning("SDK/model rejects temperature, retrying without it")
            BaseAgent._supports_temperature = False
            return self._stream_once(system, user, temperature)

    @staticmethod
    def _parse_json(text: str) -> Dict[str, Any]:
        try:
            return json.loads(text.strip())
        except json.JSONDecodeError:
            pass

        fenced = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
        if fenced:
            try:
                return json.loads(fenced.group(1).strip())
            except json.JSONDecodeError:
                pass

        brace_match = re.search(r"\{[\s\S]*\}", text)
        if brace_match:
            try:
                return json.loads(brace_match.group())
            except json.JSONDecodeError:
                pass

        logger.error("Failed to parse JSON from model output: %s", text[:200])
        raise ValueError("Could not extract valid JSON from model response.")

    def _call_structured(self, system: str, user: str, schema: Type[T], temperature: float = 0.0) -> T:
        raw = self._call(system, user, temperature=temperature)
        data = self._parse_json(raw)
        return schema.model_validate(data)