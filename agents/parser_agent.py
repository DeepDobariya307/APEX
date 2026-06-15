"""
APEX — Parser Agent
Extracts structured Pydantic models from raw resume and job description text.
Uses Claude Haiku for fast, cheap structured extraction.
"""

from __future__ import annotations
import logging
from agents.base_agent import BaseAgent
from config import config
from core.models import ParsedJobDescription, ParsedResume

logger = logging.getLogger(__name__)

RESUME_PARSE_SYSTEM = """You are an expert resume parser. Extract structured information from the resume text.

Return ONLY a JSON object — no preamble, no explanation, no markdown fences.

JSON schema:
{
  "contact": {
    "name": "",
    "email": "",
    "phone": "",
    "location": "",
    "linkedin": "",
    "github": ""
  },
  "summary": "",
  "skills": [],
  "experience": [
    {
      "title": "",
      "company": "",
      "duration": "",
      "bullets": []
    }
  ],
  "education": [
    {
      "degree": "",
      "institution": "",
      "year": "",
      "gpa": ""
    }
  ],
  "projects": [
    {
      "name": "",
      "description": "",
      "technologies": [],
      "bullets": []
    }
  ],
  "certifications": [],
  "languages": []

CRITICAL: The "languages" field MUST capture every language and proficiency level
mentioned anywhere in the resume, in the exact format given (e.g. "English (C1)",
"German (B1)", "Hindi (Native)"). This is often in a dedicated "LANGUAGES" section
near the bottom of the resume — do not skip it.
}

Rules:
- Extract ALL bullet points verbatim
- Skills should be a flat list of individual technologies/tools
- If a field is not present, leave it as empty string or empty list
- Do not invent or infer information not present in the text
"""

JD_PARSE_SYSTEM = """You are an expert job description analyst. Extract structured information from the job description.

Return ONLY a JSON object — no preamble, no explanation, no markdown fences.

JSON schema:
{
  "job_title": "",
  "company": "",
  "location": "",
  "required_skills": [],
  "preferred_skills": [],
  "responsibilities": [],
  "qualifications": [],
  "experience_years": "",
  "technologies": [],
  "keywords": [],
  "soft_traits": []
}

Rules:
- required_skills: skills explicitly marked as required, must have, or essential
- preferred_skills: skills marked as nice to have, preferred, or bonus
- technologies: ALL specific tools, frameworks, languages, platforms mentioned anywhere
- keywords: important ATS keywords including soft skills and domain terms
- If required vs preferred is ambiguous, put in required_skills
- Extract every single technology mentioned
- required_skills/preferred_skills: ONLY technical skills, tools, domains, certifications,
  languages (e.g. "German B1"), or specific experience types. NEVER include generic
  work-style traits.
- soft_traits: generic personal/work-style traits (e.g. "structured thinking",
  "self-initiative", "analytical thinking", "presentation skills", "report writing",
  "methodological competence", "team-oriented", "solution-oriented"). These go HERE,
  never in required_skills or preferred_skills.
- Translate non-English job descriptions into English when extracting.

- Do NOT split a single compound requirement into multiple overlapping entries.
  E.g. "AWS (Bedrock, Lambda, API Gateway)" should be ONE entry in required_skills
  (or at most list each AWS service once, not also the umbrella "AWS" phrase again).
  Avoid near-duplicate phrasings of the same requirement.

"""


class ParserAgent(BaseAgent):

    def __init__(self):
        super().__init__(model=config.CLAUDE_FAST_MODEL)

    def parse_resume(self, raw_text: str) -> ParsedResume:
        logger.info("Parsing resume (%d chars)...", len(raw_text))
        result = self._call_structured(
            system=RESUME_PARSE_SYSTEM,
            user=f"Parse this resume:\n\n{raw_text}",
            schema=ParsedResume,
        )
        result.raw_text = raw_text
        logger.info(
            "Resume parsed: %d skills, %d experiences, %d projects",
            len(result.skills),
            len(result.experience),
            len(result.projects),
        )
        return result

    def parse_job_description(self, raw_text: str) -> ParsedJobDescription:
        logger.info("Parsing job description (%d chars)...", len(raw_text))
        result = self._call_structured(
            system=JD_PARSE_SYSTEM,
            user=f"Parse this job description:\n\n{raw_text}",
            schema=ParsedJobDescription,
        )
        result.raw_text = raw_text
        logger.info(
            "JD parsed: '%s' at '%s' — %d required skills",
            result.job_title,
            result.company,
            len(result.required_skills),
        )
        return result
    