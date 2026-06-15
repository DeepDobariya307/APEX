"""
APEX — Critique Agent
Analyses resume weaknesses against the target JD in surgical detail.
First half of the Critique→Rewrite loop.
"""

from __future__ import annotations
import logging
from agents.base_agent import BaseAgent
from config import config
from core.models import ATSResult, CritiqueResult, ParsedJobDescription, ParsedResume

logger = logging.getLogger(__name__)

CRITIQUE_SYSTEM = """You are a brutally honest career coach and ATS expert.
Identify EXACTLY what is weak in this resume for this specific role.

Return ONLY a JSON object — no preamble, no explanation, no markdown fences.

JSON schema:
{
  "overall_assessment": "",
  "weak_bullets": [
    {"original": "", "issue": "", "suggestion": ""}
  ],
  "missing_keywords": [],
  "missing_achievements": [],
  "structural_issues": [],
  "priority_fixes": []
}

CRITICAL HONESTY CONSTRAINT:
Your "suggestion" field guides a rewrite. The rewrite must remain 100% factually true —
it cannot invent tools, domains, or outcomes the candidate never had.

GOOD suggestion (honest reframe — emphasizes a REAL transferable skill):
"Emphasize the data validation and large-scale processing aspects of this project,
since BI roles value data quality rigor — but do not claim this was a BI project."

BAD suggestion (demands fabrication):
"Reframe this NLP project as a fraud detection / anomaly detection system" — this
asks the candidate to claim domain experience they don't have. DO NOT suggest this.

If a project has genuinely NO transferable angle to the target role, say so plainly
in "structural_issues" (e.g. "This project has no relevant transferable skills for
this role and may be better minimized rather than rewritten") rather than inventing
a connection.

Rules:
- weak_bullets: identify the 3-6 WORST performing bullet points
  - original: copy the bullet EXACTLY as written
  - issue: what specifically is wrong (vague, no metric, missing keyword, etc.)
  - suggestion: an HONEST improvement direction — better phrasing, surfacing real
    metrics, or genuinely transferable framing. Never suggest claiming a different
    domain, tool, or outcome than what actually happened.
- missing_keywords: exact keywords from the JD genuinely absent from the resume
- priority_fixes: top 5 honest, actionable improvements ranked by ATS impact.
- Do not mark them with numbers — the frontend will add that. Just return a list of strings in priority order.
  If the fundamental issue is "this candidate's background doesn't match this role
  well", say that plainly as a priority fix rather than suggesting fabrication.
- overall_assessment: be honest about fit. If the match is weak, say so — and note
  that the candidate should focus on portfolio projects (see learning roadmap) rather
  than resume fabrication to close the gap.

Be surgical. Be specific. Be honest above all else.
"""

class CritiqueAgent(BaseAgent):

    def __init__(self):
        super().__init__(model=config.CLAUDE_PRIMARY_MODEL)

    def critique(
        self,
        resume: ParsedResume,
        jd: ParsedJobDescription,
        ats_result: ATSResult,
        iteration: int = 1,
    ) -> CritiqueResult:
        logger.info("Critique pass %d — current ATS score: %d", iteration, ats_result.ats_score)
        user_prompt = self._build_prompt(resume, jd, ats_result, iteration)
        result = self._call_structured(
            system=CRITIQUE_SYSTEM,
            user=user_prompt,
            schema=CritiqueResult,
        )
        logger.info(
            "Critique complete: %d weak bullets, %d missing keywords",
            len(result.weak_bullets),
            len(result.missing_keywords),
        )
        return result

    def _build_prompt(
        self,
        resume: ParsedResume,
        jd: ParsedJobDescription,
        ats_result: ATSResult,
        iteration: int,
    ) -> str:
        bullets_block = []
        for exp in resume.experience:
            for b in exp.bullets:
                bullets_block.append(f"• {b}")
        for proj in resume.projects:
            for b in proj.bullets:
                bullets_block.append(f"• {b}")

        iter_note = (
            "" if iteration == 1
            else f"\nThis is ITERATION {iteration}. Focus on what still remains weak after the previous rewrite."
        )

        return f"""
CURRENT ATS SCORE: {ats_result.ats_score}/100{iter_note}
MISSING REQUIRED SKILLS: {', '.join(ats_result.missing_required_skills)}
MISSING PREFERRED SKILLS: {', '.join(ats_result.missing_preferred_skills)}

TARGET ROLE: {jd.job_title} at {jd.company}
REQUIRED SKILLS: {', '.join(jd.required_skills)}
KEY TECHNOLOGIES: {', '.join(jd.technologies)}
JD KEYWORDS: {', '.join(jd.keywords)}

CANDIDATE SKILLS: {', '.join(resume.skills)}

CURRENT BULLET POINTS:
{chr(10).join(bullets_block)}

CANDIDATE SUMMARY: {resume.summary}

Critique this resume for this specific role.
"""