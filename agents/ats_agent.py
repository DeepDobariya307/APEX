"""
APEX — ATS Agent
Scores a parsed resume against a parsed job description.
Two-pass: deterministic skill matching + Claude Sonnet semantic scoring.
"""

from __future__ import annotations
import logging
import re
from typing import List, Set, Tuple
from agents.base_agent import BaseAgent
from config import config
from core.models import ATSResult, ParsedJobDescription, ParsedResume, SkillMatch, SuggestedRename

logger = logging.getLogger(__name__)

ATS_SYSTEM = """You are a senior technical recruiter and ATS expert.

Analyse the candidate's resume against the job description and return a JSON ATS analysis.

Return ONLY a JSON object — no preamble, no explanation, no markdown fences.

JSON schema:
{
  "ats_score": 0,
  "keyword_coverage_pct": 0.0,
  "strengths": [],
  "weaknesses": [],
  "missing_required_skills": [],
  "missing_preferred_skills": [],
  "jd_matched_skills": [],
  "suggested_renames": [
    {"resume_term": "", "suggested_term": "", "jd_term": ""}
  ]
}

Scoring rubric:
- 90-100: Exceptional match
- 75-89:  Good match, worth interviewing
- 60-74:  Moderate match, some gaps
- 40-59:  Weak match, significant gaps
- 0-39:   Poor match, major gaps

Do NOT include generic soft-skill traits (structured thinking, presentation creation,
report writing, methodological competence, self-initiative, analytical thinking,
team-oriented, solution-oriented, etc.) in missing_required_skills or
missing_preferred_skills — these are not resume keyword gaps. If genuinely relevant,
mention briefly in weaknesses only.

IMPORTANT: Before marking any skill as "missing", carefully check the FULL resume text
including the Languages, Certifications, Skills, Experience, and Projects sections —
information is often present but not in the exact wording of the JD. For example,
"German (B1)" in a Languages section satisfies a "good German skills" requirement.
"Soft Skills: ... Cross-Functional Collaboration ..." satisfies "teamwork" or
"interdisciplinary collaboration" requirements. Match on MEANING, not exact phrasing.

SELF-CONSISTENCY CHECK (mandatory before finalizing your response):
After drafting "strengths" and "missing_required_skills"/"missing_preferred_skills",
re-read both lists. If something is listed as a STRENGTH (e.g. "German B1 meets the
requirement"), it must NOT also appear in missing_required_skills or
missing_preferred_skills. Remove any such contradictions before responding.
A skill is either present (and possibly noted as a strength/limitation in weaknesses
if the LEVEL is insufficient) OR missing entirely — never both.

JD_MATCHED_SKILLS:
List every skill/competency from the candidate's resume that is relevant to this JD —
broader than just required_skills/preferred_skills. Match on MEANING, not exact wording.
Include technical skills, tools, domains, and relevant soft skills/competencies that
genuinely appear in the resume and connect to something in the JD (responsibilities,
qualifications, or keywords). Each entry should be phrased using the candidate's OWN
resume terminology (not the JD's wording) — this list represents "what the candidate
already has that's relevant here."

SUGGESTED_RENAMES:
Identify cases where the candidate's resume uses different WORDING for a concept the
JD also expresses, where renaming would improve ATS keyword matching WITHOUT changing
meaning. Example: resume says "fast learner", JD says "quick learning ability" — these
mean the same thing, suggest renaming "fast learner" to "quick learning ability".
Only suggest renames where the meaning is genuinely equivalent. Each entry needs:
  - resume_term: the exact phrase as it appears in the resume
  - suggested_term: the ATS-friendly rewording
  - jd_term: the JD phrase that motivated this suggestion
If no good renames exist, return an empty list — do not force suggestions.

HARD FILTER for missing_required_skills / missing_preferred_skills:
Before adding ANY item to these lists, ask: "Is this a specific tool, technology,
platform, certification, language proficiency, or domain (e.g. Databricks, Azure
DevOps, reinsurance, German B2)?" If the answer is NO — if it is instead a generic
work-style description (proactive, independent working, collaboration, problem-solving,
documentation habits, structured thinking, communication style) — DO NOT include it
in either missing list. At most mention it in weaknesses if truly unaddressed.

Be precise and honest. Do not inflate scores.
"""


class ATSAgent(BaseAgent):

    def __init__(self):
        super().__init__(model=config.CLAUDE_PRIMARY_MODEL)

    def analyze(self, resume: ParsedResume, jd: ParsedJobDescription) -> ATSResult:
        logger.info("Running ATS analysis for: %s", jd.job_title)

        skill_matches, matched_skills, missing_required, missing_preferred = (
            self._match_skills(resume, jd)
        )

        llm_result = self._llm_analyze(resume, jd)

        strengths_text = " ".join(llm_result.get("strengths", [])).lower()

        def _contradicts_strength(skill: str) -> bool:
            words = [w for w in re.findall(r"[a-zA-Z]+", skill.lower()) if len(w) > 3]
            if not words:
                return False
            return any(w in strengths_text for w in words)

        raw_missing_required = list(
            set(llm_result.get("missing_required_skills", [])) | set(missing_required)
        )
        raw_missing_preferred = list(
            set(llm_result.get("missing_preferred_skills", [])) | set(missing_preferred)
        )

        all_missing_required = [s for s in raw_missing_required if not _contradicts_strength(s)]
        all_missing_preferred = [s for s in raw_missing_preferred if not _contradicts_strength(s)]

        keyword_coverage = max(
            self._keyword_coverage(resume, jd),
            float(llm_result.get("keyword_coverage_pct", 0)),
        )

        return ATSResult(
            ats_score=int(llm_result.get("ats_score", 0)),
            matched_skills=matched_skills,
            missing_required_skills=all_missing_required,
            missing_preferred_skills=all_missing_preferred,
            keyword_coverage_pct=round(keyword_coverage, 1),
            strengths=llm_result.get("strengths", []),
            weaknesses=llm_result.get("weaknesses", []),
            skill_matches=skill_matches,
            jd_matched_skills=llm_result.get("jd_matched_skills", []),
            suggested_renames=[
                SuggestedRename(**r) for r in llm_result.get("suggested_renames", [])
            ],
        )

    def _match_skills(
        self,
        resume: ParsedResume,
        jd: ParsedJobDescription,
    ) -> Tuple[List[SkillMatch], List[str], List[str], List[str]]:

        all_resume_text = " ".join([
            " ".join(resume.skills),
            resume.summary,
            " ".join(bullet for exp in resume.experience for bullet in exp.bullets),
            " ".join(
                " ".join(p.technologies) + " " + " ".join(p.bullets)
                for p in resume.projects
            ),
            resume.raw_text,
        ]).lower()

        all_resume_text = re.sub(r"[^\w\s\+\#]", " ", all_resume_text)

        skill_matches: List[SkillMatch] = []
        matched_skills: List[str] = []
        missing_required: List[str] = []
        missing_preferred: List[str] = []

        def _found(skill: str) -> bool:
            normalised = skill.lower().strip()
            if normalised in all_resume_text:
                return True
            tokens = normalised.split()
            return all(t in all_resume_text for t in tokens)

        for skill in jd.required_skills:
            found = _found(skill)
            skill_matches.append(
                SkillMatch(skill=skill, found_in_resume=found, importance="required")
            )
            if found:
                matched_skills.append(skill)
            else:
                missing_required.append(skill)

        for skill in jd.preferred_skills:
            found = _found(skill)
            skill_matches.append(
                SkillMatch(skill=skill, found_in_resume=found, importance="preferred")
            )
            if found and skill not in matched_skills:
                matched_skills.append(skill)
            elif not found:
                missing_preferred.append(skill)

        return skill_matches, matched_skills, missing_required, missing_preferred

    def _keyword_coverage(self, resume: ParsedResume, jd: ParsedJobDescription) -> float:
        if not jd.keywords:
            return 0.0
        resume_lower = resume.raw_text.lower()
        found = sum(1 for kw in jd.keywords if kw.lower() in resume_lower)
        return (found / len(jd.keywords)) * 100

    def _llm_analyze(self, resume: ParsedResume, jd: ParsedJobDescription) -> dict:
        resume_summary = self._format_resume_for_llm(resume)
        jd_summary = self._format_jd_for_llm(jd)
        logger.info("Resume languages field: %s", resume.languages)
        user_prompt = f"RESUME:\n{resume_summary}\n\nJOB DESCRIPTION:\n{jd_summary}\n\nAnalyse this resume against this job description."
        raw = self._call(system=ATS_SYSTEM, user=user_prompt, temperature=0.0)
        return self._parse_json(raw)

    @staticmethod
    def _format_resume_for_llm(resume: ParsedResume) -> str:
        lines = [
            f"Name: {resume.contact.name}",
            f"Location: {resume.contact.location}",
            f"Summary: {resume.summary}",
            f"Skills: {', '.join(resume.skills)}",
            f"Languages: {', '.join(resume.languages)}",
            f"Certifications: {', '.join(resume.certifications)}",
            "",
            "Experience:",
        ]
        for exp in resume.experience:
            lines.append(f"  {exp.title} at {exp.company} ({exp.duration})")
            for b in exp.bullets:
                lines.append(f"    • {b}")
        lines.append("\nEducation:")
        for edu in resume.education:
            lines.append(f"  {edu.degree} — {edu.institution} ({edu.year})")
        lines.append("\nProjects:")
        for proj in resume.projects:
            lines.append(f"  {proj.name}: {', '.join(proj.technologies)}")
            for b in proj.bullets:
                lines.append(f"    • {b}")
        return "\n".join(lines)

    @staticmethod
    def _format_jd_for_llm(jd: ParsedJobDescription) -> str:
        lines = [
            f"Role: {jd.job_title} at {jd.company} ({jd.location})",
            f"Experience required: {jd.experience_years}",
            f"Required Skills: {', '.join(jd.required_skills)}",
            f"Preferred Skills: {', '.join(jd.preferred_skills)}",
            f"Technologies: {', '.join(jd.technologies)}",
            f"Keywords: {', '.join(jd.keywords)}",
            "\nResponsibilities:",
        ]
        for r in jd.responsibilities[:8]:
            lines.append(f"  • {r}")
        return "\n".join(lines)