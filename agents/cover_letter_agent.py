"""
APEX — Cover Letter Agent
Generates a tailored, ATS-friendly cover letter.
"""

from __future__ import annotations
import logging
from agents.base_agent import BaseAgent
from config import config
from core.models import CoverLetter, ParsedJobDescription, ParsedResume

logger = logging.getLogger(__name__)

COVER_LETTER_SYSTEM = """You are an expert cover letter writer specialising in tech roles in Europe.

Write a professional, tailored cover letter. Return ONLY a JSON object.

JSON schema:
{
  "subject_line": "",
  "body": "",
  "word_count": 0,
  "keywords_used": []
}

Rules:
1. Length: 350-380 words — fits exactly one page
2. Structure:
   - The body field starts DIRECTLY with "Dear [Hiring Team/Manager/specific name if known]," — do NOT repeat the subject line or job title heading inside the body.
   - Opening paragraph: explicitly state the application type and job title (e.g. "I am writing to apply for the [Werkstudent/Praktikum/etc.] position as [Job Title]"), then give a specific hook connecting candidate's background to this exact role
   - Middle 1: most relevant technical experience with concrete results
   - Middle 2: projects or achievements that directly address JD requirements
   - Closing: enthusiasm, call to action, mention availability
   - The main paragraphs should sound like how the candidate is willing to be useful to the employer — not just a generic "I am passionate about X and would be a great fit" statement. Focus on what they can bring to the company.
   - Even if the main JD keywords or skills, sound like how a candidate can easily adopt and learn them, do not say they already have them if they don't. Instead, focus on the transferable skills and relevant experience they do have, and express enthusiasm for learning the specific tools/skills mentioned in the JD.
   - The body MUST END with the closing line "Sincerely," or "Best regards," followed by a newline, and that's it — do NOT put the candidate's name after it. The name is added separately by the application, not by you.
3. Tone: professional but human — not robotic, not sycophantic
4. Naturally use 5-8 keywords from the JD
5. If candidate is a student: mention internship type
6. If candidate has work permit: mention it briefly in closing
7. Do NOT use hollow phrases like "I am passionate about" or "I would be a great fit"
8. Do NOT mention LinkedIn, GitHub, or IEEE links
9. subject_line: "Application for [Job Title] at [Company]"
10. keywords_used: list the JD keywords you wove into the letter
"""


class CoverLetterAgent(BaseAgent):

    def __init__(self):
        super().__init__(model=config.CLAUDE_PRIMARY_MODEL)

    def generate(
        self,
        resume: ParsedResume,
        jd: ParsedJobDescription,
        internship_type: str = "mandatory internship (Pflichtpraktikum)",
        has_work_permit: bool = True,
    ) -> CoverLetter:
        logger.info("Generating cover letter for: %s at %s", jd.job_title, jd.company)
        user_prompt = self._build_prompt(resume, jd, internship_type, has_work_permit)
        result = self._call_structured(
            system=COVER_LETTER_SYSTEM,
            user=user_prompt,
            schema=CoverLetter,
            temperature=0.4,
        )
        result.body = self._clean_body(result.body, resume.contact.name, result.subject_line)
        if result.word_count == 0:
            result.word_count = len(result.body.split())
        logger.info("Cover letter generated: %d words", result.word_count)
        return result

    @staticmethod
    def _clean_body(body: str, candidate_name: str, subject_line: str) -> str:
        """
        Safety net: strip any subject-line repetition and trailing name
        the model may have included despite instructions.
        """
        import re

        lines = [l for l in body.split("\n")]

        # Remove lines that are just a repeated "Application for..." subject
        lines = [
            l for l in lines
            if not (l.strip().lower().startswith("application for") and len(l.strip()) > 10)
        ]

        # Rejoin and strip trailing signature artifacts
        cleaned = "\n".join(lines).strip()

        # Remove "Sincerely,\nName" or "Sincerely, Name" or "Best regards,\nName" at the end
        name_escaped = re.escape(candidate_name)
        patterns = [
            rf"(Sincerely|Best regards|Kind regards),?\s*\n?\s*{name_escaped}\s*$",
            rf"(Sincerely|Best regards|Kind regards),?\s*{name_escaped}\s*$",
        ]
        for pattern in patterns:
            cleaned = re.sub(pattern, r"\1,", cleaned, flags=re.IGNORECASE).strip()

        return cleaned

    def _build_prompt(
        self,
        resume: ParsedResume,
        jd: ParsedJobDescription,
        internship_type: str,
        has_work_permit: bool,
    ) -> str:
        top_experience = resume.experience[0] if resume.experience else None
        exp_block = ""
        if top_experience:
            exp_block = (
                f"Most recent role: {top_experience.title} at {top_experience.company} "
                f"({top_experience.duration})\nKey bullets:\n"
                + "\n".join(f"  • {b}" for b in top_experience.bullets[:4])
            )

        top_project = resume.projects[0] if resume.projects else None
        proj_block = ""
        if top_project:
            proj_block = (
                f"Strongest project: {top_project.name}\n"
                + "\n".join(f"  • {b}" for b in top_project.bullets[:3])
            )

        permit_note = (
            "Candidate holds a valid German residence and work permit — mention briefly in closing."
            if has_work_permit else ""
        )

        return f"""
CANDIDATE:
Name: {resume.contact.name}
Location: {resume.contact.location}
Application type: {internship_type}
{permit_note}

PROFILE: {resume.summary}
Skills: {', '.join(resume.skills[:15])}

{exp_block}

{proj_block}

Education: {resume.education[0].degree if resume.education else ''} at {resume.education[0].institution if resume.education else ''}

TARGET ROLE: {jd.job_title} at {jd.company} ({jd.location})
Key requirements: {', '.join(jd.required_skills[:8])}
Technologies: {', '.join(jd.technologies[:10])}
Keywords to use: {', '.join(jd.keywords[:12])}

Write a compelling tailored cover letter.
"""