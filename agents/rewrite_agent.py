"""
APEX — Rewrite Agent
Rewrites weak resume bullets and summary using critique guidance.
Second half of the Critique→Rewrite loop.
"""

from __future__ import annotations
import logging
from agents.base_agent import BaseAgent
from config import config
from core.models import ATSResult, CritiqueResult, ParsedJobDescription, ParsedResume, RewriteResult

logger = logging.getLogger(__name__)

REWRITE_SYSTEM = """You are an expert resume editor. You improve PHRASING and ATS keyword
density. You NEVER change WHAT the candidate actually did.

Return ONLY a JSON object — no preamble, no markdown fences.

JSON schema:
{
  "rewritten_summary": "",
  "rewritten_bullets": [
    {"original": "", "rewritten": "", "keywords_added": [], "recommendation": ""}
  ],
  "keywords_injected": [],
  "new_ats_score_estimate": 0
}

JSON schema addition per bullet:
  "recommendation": ""  // "rewrite" (default) or "remove" if this bullet has
                        // no honest transferable angle for this role

Rules addition:
- If a bullet genuinely cannot be honestly reframed for this role (e.g. it's
  irrelevant and the critique suggests removing it), set "rewritten" to an empty
  string and "recommendation" to "remove". Do NOT fabricate a rewrite just to fill
  the field. If the bullet can be improved but should remain, set "recommendation" to "rewrite".
- keywords_injected: list the specific JD keywords you successfully injected into the rewrites. Only include a keyword here if it is now genuinely supported by the rewritten bullet. Do not list keywords that were attempted but could not be honestly supported.
- new_ats_score_estimate: based on the critique and your rewrite, give an honest estimate of the new ATS score. Do not inflate unrealistically — a fundamentally mismatched resume should not jump to 85+ just from phrasing changes.


THE CORE TEST FOR EVERY BULLET:
Could the candidate defend this sentence, word for word, in an interview without lying?
If NO — you have fabricated. Rewrite again until the answer is YES.

CONCRETE EXAMPLE OF WHAT NOT TO DO:
Original: "Built deep learning models (BERT, BiLSTM) for toxic comment classification on 525K comments, achieving 94-96% accuracy."
Target role: BI Analyst (Power BI, DAX, SQL)

WRONG (fabrication — DO NOT DO THIS):
"Developed Power BI dashboards analyzing 525K records, created 15 DAX measures..."
^ This is FALSE. The candidate never touched Power BI or DAX in this project. This is lying on a resume.

CORRECT (honest reframing):
"Processed and validated a 525K-record dataset for a machine learning classification system,
applying systematic data quality checks and achieving 94-96% model accuracy — demonstrating
strong analytical rigor and large-scale data handling applicable to BI reporting environments."
^ This stays 100% factually true. It just highlights the TRANSFERABLE angle (data handling,
accuracy, analytical rigor) using language a BI recruiter recognizes, WITHOUT claiming
Power BI/DAX/dashboards were involved.

RULES:
1. Never introduce a tool, platform, or technology name that does not appear anywhere
   in the candidate's original resume text.
2a. Never invent metrics, team sizes, stakeholder counts, or business outcomes.
2b. NEVER alter, upgrade, or omit language proficiency levels. If the candidate's
    resume states "German (A2)", you may NEVER write "fluent in German", "German
    proficiency", or any phrasing that implies a higher level than stated. If you
    mention German at all, you MUST preserve the exact level (e.g. "German (A2,
    actively improving)"). The same applies to ALL languages and ALL certifications/
    proficiency levels anywhere in the resume — these are factual claims with legal/
    professional consequences if misrepresented and must be reproduced exactly as
    given, never upgraded.
3. Never change the subject/domain of a project. An NLP project must remain described
   as an NLP/data project — you may emphasise its transferable qualities only.
4. If the candidate has GENUINELY relevant experience for a JD skill, you may use that
   skill's terminology. If they do NOT, do not force it in — leave it as a gap.
5. Action verbs, structure, and metric *presentation* (already-present numbers) can be
   improved freely.
6. keywords_injected: ONLY keywords that are truthfully supported by what the candidate
   actually did. If almost nothing matches the JD, this list will be SHORT — that is fine
   and expected. A short honest list is correct behaviour.
7. new_ats_score_estimate: realistic. A fundamentally mismatched resume should NOT jump
   to 85+ just from phrasing changes — cap your estimate accordingly.
8.  If a bullet genuinely cannot be honestly reframed for this role (e.g. it's
   irrelevant and should be removed per the critique), set "rewritten" to an
   empty string and "recommendation" to "remove". Do NOT fabricate a rewrite
   just to fill the field.

For the summary: describe the candidate's REAL background and REAL skills honestly,
optionally noting genuine transferable interest in the target domain
(e.g. "...with a strong data and analytical foundation, now developing interest in
business intelligence tooling").
"""

class RewriteAgent(BaseAgent):

    def __init__(self):
        super().__init__(model=config.CLAUDE_PRIMARY_MODEL)

    def rewrite(
        self,
        resume: ParsedResume,
        jd: ParsedJobDescription,
        critique: CritiqueResult,
        ats_result: ATSResult,
    ) -> RewriteResult:
        logger.info("Rewriting %d weak bullets + summary...", len(critique.weak_bullets))
        user_prompt = self._build_prompt(resume, jd, critique, ats_result)
        result = self._call_structured(
            system=REWRITE_SYSTEM,
            user=user_prompt,
            schema=RewriteResult,
            temperature=0.3,
        )
        logger.info(
            "Rewrite complete: %d bullets rewritten, %d keywords injected, estimated score: %d",
            len(result.rewritten_bullets),
            len(result.keywords_injected),
            result.new_ats_score_estimate,
        )
        return result

    def _build_prompt(
        self,
        resume: ParsedResume,
        jd: ParsedJobDescription,
        critique: CritiqueResult,
        ats_result: ATSResult,
    ) -> str:
        weak_bullets_block = "\n".join(
            f"  BULLET: {b.original}\n  ISSUE: {b.issue}\n  GUIDANCE: {b.suggestion}"
            for b in critique.weak_bullets
        )
        return f"""
TARGET ROLE: {jd.job_title} at {jd.company}
REQUIRED SKILLS TO INJECT: {', '.join(ats_result.missing_required_skills[:10])}
MISSING KEYWORDS: {', '.join(critique.missing_keywords[:15])}

CURRENT SUMMARY:
{resume.summary}

WEAK BULLETS TO REWRITE (with guidance):
{weak_bullets_block}

PRIORITY FIXES:
{chr(10).join(f'  {i+1}. {fix}' for i, fix in enumerate(critique.priority_fixes))}

Rewrite the summary and each weak bullet.
"""