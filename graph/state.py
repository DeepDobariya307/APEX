"""
APEX — LangGraph State
Compatible with LangGraph 1.x
"""

from __future__ import annotations
from typing import List, Optional, Any
from typing_extensions import TypedDict, Annotated
import operator


class APEXState(TypedDict, total=False):
    # ── Raw inputs ─────────────────────────────────────────────────────────
    resume_text: str
    jd_text: str
    internship_type: str
    has_work_permit: bool

    # ── Parsed structures ──────────────────────────────────────────────────
    parsed_resume: Any
    parsed_jd: Any

    # ── ATS analysis ───────────────────────────────────────────────────────
    ats_result: Any
    initial_ats_score: int

    # ── Critique → Rewrite loop ────────────────────────────────────────────
    critique_result: Any
    rewrite_result: Any
    rewrite_iteration: int

    # ── Output agents ──────────────────────────────────────────────────────
    cover_letter: Any
    interview_kit: Any
    learning_roadmap: Any

    # ── Pipeline metadata ──────────────────────────────────────────────────
    status: str
    error: Optional[str]
    completed_nodes: Annotated[List[str], operator.add]