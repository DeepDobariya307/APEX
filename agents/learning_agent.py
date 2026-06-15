"""
APEX — Learning Agent
Maps skill gaps to a concrete prioritised learning roadmap.
"""

from __future__ import annotations
import logging
from agents.base_agent import BaseAgent
from config import config
from core.models import ATSResult, LearningResource, LearningRoadmap, ParsedJobDescription, ParsedResume

logger = logging.getLogger(__name__)

LEARNING_SYSTEM = """You are a technical career coach specialising in AI/ML skills development.

Create a prioritised learning roadmap to close the gap between the candidate's skills
and the target role requirements.

Return ONLY a JSON object — no preamble, no explanation, no markdown fences.

JSON schema:
{
  "skill_gaps": [],
  "quick_wins": [],
  "resources": [
    {
      "skill": "",
      "resource_name": "",
      "resource_type": "",
      "platform": "",
      "estimated_time": "",
      "priority": ""
      "search_query": ""
    }
  ],
  "project_ideas": [],
  "estimated_ready_in": ""
}

Rules:
- skill_gaps: specific skills the candidate lacks for this role
- quick_wins: skills demonstrable within 1 week via a small project
- resources: one recommended resource per missing skill
  - resource_type: course, certification, project, documentation, or tutorial
  - priority: high (required skill), medium (preferred), low (nice to have)
  - search_query: a concise search query (4-8 words) someone could paste into the
    platform's search bar to find this exact resource, e.g. "Excel for Finance
    Professionals CFI" or "AWS Bedrock Lambda tutorial Databricks"
- project_ideas: 3-4 specific project ideas buildable in 1-2 weeks for GitHub portfolio
- estimated_ready_in: honest estimate to close all HIGH priority gaps
- Prioritise free resources over paid where possible
"""


class LearningAgent(BaseAgent):

    def __init__(self):
        super().__init__(model=config.CLAUDE_FAST_MODEL)

    def generate_roadmap(
        self,
        resume: ParsedResume,
        jd: ParsedJobDescription,
        ats_result: ATSResult,
    ) -> LearningRoadmap:
        logger.info("Generating learning roadmap...")
        user_prompt = self._build_prompt(resume, jd, ats_result)
        raw = self._call(system=LEARNING_SYSTEM, user=user_prompt, temperature=0.2)
        data = self._parse_json(raw)
        roadmap = LearningRoadmap(
            skill_gaps=data.get("skill_gaps", []),
            quick_wins=data.get("quick_wins", []),
            resources=[LearningResource(**r) for r in data.get("resources", [])],
            project_ideas=[
              p if isinstance(p, str) else p.get("title", str(p))
              for p in data.get("project_ideas", [])
            ],
            estimated_ready_in=data.get("estimated_ready_in", ""),
        )
        logger.info(
            "Roadmap: %d gaps, %d resources, %d project ideas",
            len(roadmap.skill_gaps), len(roadmap.resources), len(roadmap.project_ideas),
        )
        return roadmap

    def _build_prompt(
        self,
        resume: ParsedResume,
        jd: ParsedJobDescription,
        ats_result: ATSResult,
    ) -> str:
        return f"""
CANDIDATE CURRENT SKILLS: {', '.join(resume.skills)}

TARGET ROLE: {jd.job_title} at {jd.company}
Required skills: {', '.join(jd.required_skills)}
Preferred skills: {', '.join(jd.preferred_skills)}
Technologies: {', '.join(jd.technologies)}

SKILL GAPS:
  Missing required: {', '.join(ats_result.missing_required_skills)}
  Missing preferred: {', '.join(ats_result.missing_preferred_skills)}

Current ATS score: {ats_result.ats_score}/100

Generate a concrete learning roadmap to close these gaps.
"""