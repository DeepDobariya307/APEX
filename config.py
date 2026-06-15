"""
APEX — Central Configuration
All tunable parameters in one place.
Every agent imports from here — never hardcode values anywhere else.
"""

from dataclasses import dataclass


@dataclass
class Config:
    # ── Claude Models ─────────────────────────────────────────────────────────
    # Sonnet for heavy reasoning (ATS, critique, rewrite, cover letter)
    # Haiku for fast structured extraction (parser, interview, learning)
    CLAUDE_PRIMARY_MODEL: str = "claude-sonnet-4-5-20250929"
    CLAUDE_FAST_MODEL: str = "claude-haiku-4-5-20251001"
    MAX_TOKENS: int = 8192
    INTERVIEW_MAX_TOKENS: int = 37000

    # ── Document Processing ───────────────────────────────────────────────────
    MAX_RESUME_PAGES: int = 5
    MAX_JD_CHARS: int = 15_000

    # ── ATS Engine ────────────────────────────────────────────────────────────
    ATS_PASS_THRESHOLD: int = 75       # Score above which we skip rewrite loop
    MAX_REWRITE_ITERATIONS: int = 1    # Max Critique→Rewrite cycles

    # ── Interview Agent ───────────────────────────────────────────────────────
    HR_QUESTIONS_COUNT: int = 5
    TECHNICAL_QUESTIONS_COUNT: int = 7
    BEHAVIORAL_QUESTIONS_COUNT: int = 5


config = Config()