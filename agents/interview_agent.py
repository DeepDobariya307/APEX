"""
APEX — Interview Agent
Generates a complete interview preparation kit.
"""

from __future__ import annotations
import logging
from agents.base_agent import BaseAgent
from config import config
from core.models import InterviewKit, InterviewQuestion, ParsedJobDescription, ParsedResume

logger = logging.getLogger(__name__)

INTERVIEW_SYSTEM = """You are an experienced technical interviewer and career coach.

Generate an interview preparation kit. Return ONLY a JSON object.

JSON schema:
{
  "hr_questions": [
    {
      "question": "",
      "category": "hr",
      "suggested_answer": "",
      "tips": ""
    }
  ],
  "technical_questions": [{"question": "", "category": "technical", "suggested_answer": "", "tips": ""}],
  "behavioral_questions": [{"question": "", "category": "behavioral", "suggested_answer": "", "tips": ""}],
  "project_questions": [{"question": "", "category": "project", "suggested_answer": "", "tips": ""}]
}

Rules:
- hr_questions: 3 questions about motivation, background, goals
- technical_questions: 4 questions specific to the JD's required technologies
- behavioral_questions: 3 STAR-format questions using "Tell me about a time when..." framing
- project_questions: 3 questions about the candidate's specific projects
- suggested_answer: 2-3 sentence model answer tailored to THIS candidate's background
- tips: one specific tip for answering this question well
- Technical questions must be specific to the role's stack — not generic CS questions
"""

class InterviewAgent(BaseAgent):

    def __init__(self):
        super().__init__(model=config.CLAUDE_FAST_MODEL, max_tokens=config.INTERVIEW_MAX_TOKENS)

    def generate_kit(self, resume: ParsedResume, jd: ParsedJobDescription) -> InterviewKit:
        logger.info("Generating interview kit for: %s at %s", jd.job_title, jd.company)
        user_prompt = self._build_prompt(resume, jd)
        raw = self._call_streaming(system=INTERVIEW_SYSTEM, user=user_prompt, temperature=0.3)
        data = self._parse_json(raw)
        kit = InterviewKit(
            hr_questions=[InterviewQuestion(**q) for q in data.get("hr_questions", [])],
            technical_questions=[InterviewQuestion(**q) for q in data.get("technical_questions", [])],
            behavioral_questions=[InterviewQuestion(**q) for q in data.get("behavioral_questions", [])],
            project_questions=[InterviewQuestion(**q) for q in data.get("project_questions", [])],
        )
        logger.info(
            "Interview kit: %d HR, %d technical, %d behavioral, %d project",
            len(kit.hr_questions), len(kit.technical_questions),
            len(kit.behavioral_questions), len(kit.project_questions),
        )
        return kit

    def _build_prompt(self, resume: ParsedResume, jd: ParsedJobDescription) -> str:
        projects_block = "\n".join(
            f"  - {p.name}: {p.description} (Tech: {', '.join(p.technologies)})"
            for p in resume.projects
        )
        experience_block = "\n".join(
            f"  - {e.title} at {e.company} ({e.duration})"
            for e in resume.experience
        )
        return f"""
CANDIDATE:
Name: {resume.contact.name}
Summary: {resume.summary}
Skills: {', '.join(resume.skills)}

Experience:
{experience_block}

Projects:
{projects_block}

TARGET ROLE: {jd.job_title} at {jd.company}
Required skills: {', '.join(jd.required_skills)}
Technologies: {', '.join(jd.technologies)}
Key responsibilities: {', '.join(jd.responsibilities[:5])}

Generate a complete interview preparation kit.
"""