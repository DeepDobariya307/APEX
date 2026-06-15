"""
APEX — LangGraph Orchestrator
Compatible with LangGraph 1.x
Uses explicit state passing — no Command objects.
"""

from __future__ import annotations

import logging
from typing import Literal

from langgraph.graph import END, StateGraph

from agents.ats_agent import ATSAgent
from agents.cover_letter_agent import CoverLetterAgent
from agents.critique_agent import CritiqueAgent
from agents.learning_agent import LearningAgent
from agents.parser_agent import ParserAgent
from agents.rewrite_agent import RewriteAgent
from config import config
from graph.state import APEXState

logger = logging.getLogger(__name__)

# ── Instantiate agents once ───────────────────────────────────────────────────
_parser = ParserAgent()
_ats = ATSAgent()
_critique = CritiqueAgent()
_rewrite = RewriteAgent()
_cover_letter = CoverLetterAgent()
_learning = LearningAgent()


# ── Node functions ────────────────────────────────────────────────────────────

def node_parse(state: APEXState) -> dict:
    logger.info("[node_parse] Parsing documents...")
    try:
        parsed_resume = _parser.parse_resume(state["resume_text"])
        parsed_jd = _parser.parse_job_description(state["jd_text"])
        return {
            "parsed_resume": parsed_resume,
            "parsed_jd": parsed_jd,
            "status": f"✅ Documents parsed — {len(parsed_resume.skills)} skills found in resume",
            "completed_nodes": list(state.get("completed_nodes", [])) + ["parse"],
        }
    except Exception as e:
        logger.error("[node_parse] Error: %s", e)
        return {"error": f"Parse error: {e}"}


def node_ats_score(state: APEXState) -> dict:
    logger.info("[node_ats_score] Scoring resume...")
    try:
        parsed_resume = state["parsed_resume"]
        parsed_jd = state["parsed_jd"]

        ats_result = _ats.analyze(parsed_resume, parsed_jd)
        initial_score = state.get("initial_ats_score", ats_result.ats_score)
        iteration = state.get("rewrite_iteration", 0)

        logger.info(
            "ATS score: %d, iteration: %d, threshold: %d, max_iter: %d",
            ats_result.ats_score,
            iteration,
            config.ATS_PASS_THRESHOLD,
            config.MAX_REWRITE_ITERATIONS,
        )

        return {
            "ats_result": ats_result,
            "initial_ats_score": initial_score,
            "rewrite_iteration": iteration,
            "parsed_resume": parsed_resume,
            "parsed_jd": parsed_jd,
            "status": f"✅ ATS Score: {ats_result.ats_score}/100 — {len(ats_result.missing_required_skills)} missing required skills",
            "completed_nodes": list(state.get("completed_nodes", [])) + ["ats_score"],
        }
    except Exception as e:
        logger.error("[node_ats_score] Error: %s", e)
        return {"error": f"ATS error: {e}"}


def node_critique(state: APEXState) -> dict:
    logger.info("[node_critique] Running critique pass...")
    iteration = state.get("rewrite_iteration", 0) + 1
    try:
        parsed_resume = state["parsed_resume"]
        parsed_jd = state["parsed_jd"]

        critique = _critique.critique(
            parsed_resume,
            parsed_jd,
            state["ats_result"],
            iteration=iteration,
        )
        return {
            "critique_result": critique,
            "rewrite_iteration": iteration,
            "parsed_resume": parsed_resume,
            "parsed_jd": parsed_jd,
            "status": f"✅ Critique complete — {len(critique.weak_bullets)} weak bullets identified",
            "completed_nodes": list(state.get("completed_nodes", [])) + [f"critique_{iteration}"],
        }
    except Exception as e:
        logger.error("[node_critique] Error: %s", e)
        return {"error": f"Critique error: {e}"}


def node_rewrite(state: APEXState) -> dict:
    logger.info("[node_rewrite] Rewriting resume sections...")
    iteration = state.get("rewrite_iteration", 1)
    try:
        parsed_resume = state["parsed_resume"]
        parsed_jd = state["parsed_jd"]

        rewrite = _rewrite.rewrite(
            parsed_resume,
            parsed_jd,
            state["critique_result"],
            state["ats_result"],
        )
        updated_resume = _apply_rewrites(parsed_resume, rewrite)
        return {
            "rewrite_result": rewrite,
            "parsed_resume": updated_resume,
            "parsed_jd": parsed_jd,
            "status": f"✅ Rewrite complete — {len(rewrite.keywords_injected)} keywords injected",
            "completed_nodes": list(state.get("completed_nodes", [])) + [f"rewrite_{iteration}"],
        }
    except Exception as e:
        logger.error("[node_rewrite] Error: %s", e)
        return {"error": f"Rewrite error: {e}"}


def node_cover_letter(state: APEXState) -> dict:
    logger.info("[node_cover_letter] Writing cover letter...")
    try:
        parsed_resume = state["parsed_resume"]
        parsed_jd = state["parsed_jd"]

        cl = _cover_letter.generate(
            parsed_resume,
            parsed_jd,
            internship_type=state.get("internship_type", "mandatory internship (Pflichtpraktikum)"),
            has_work_permit=state.get("has_work_permit", True),
        )
        return {
            "cover_letter": cl,
            "parsed_resume": parsed_resume,
            "parsed_jd": parsed_jd,
            "status": f"✅ Cover letter written — {cl.word_count} words",
            "completed_nodes": list(state.get("completed_nodes", [])) + ["cover_letter"],
        }
    except Exception as e:
        logger.error("[node_cover_letter] Error: %s", e)
        return {"error": f"Cover letter error: {e}"}

def node_learning(state: APEXState) -> dict:
    logger.info("[node_learning] Building learning roadmap...")
    try:
        parsed_resume = state["parsed_resume"]
        parsed_jd = state["parsed_jd"]
        ats_result = state["ats_result"]

        roadmap = _learning.generate_roadmap(parsed_resume, parsed_jd, ats_result)
        return {
            "learning_roadmap": roadmap,
            "status": f"✅ Learning roadmap complete — {len(roadmap.resources)} resources",
            "completed_nodes": list(state.get("completed_nodes", [])) + ["learning"],
        }
    except Exception as e:
        logger.error("[node_learning] Error: %s", e)
        return {"error": f"Learning error: {e}"}


# ── Routing ───────────────────────────────────────────────────────────────────

def route_after_ats(state: APEXState) -> Literal["critique", "cover_letter"]:
    ats_result = state.get("ats_result")
    current_score = ats_result.ats_score if ats_result is not None else 0
    iteration = state.get("rewrite_iteration", 0)

    logger.info(
        "ROUTING — score: %d, iteration: %d, threshold: %d, max: %d",
        current_score,
        iteration,
        config.ATS_PASS_THRESHOLD,
        config.MAX_REWRITE_ITERATIONS,
    )

    if current_score < config.ATS_PASS_THRESHOLD and iteration < config.MAX_REWRITE_ITERATIONS:
        logger.info("ROUTING → critique")
        return "critique"
    else:
        logger.info("ROUTING → cover_letter")
        return "cover_letter"


# ── Rewrite application helper ────────────────────────────────────────────────

def _apply_rewrites(resume, rewrite_result) -> object:
    rewrite_map = {
        rb.original: rb.rewritten
        for rb in rewrite_result.rewritten_bullets
    }
    for exp in resume.experience:
        exp.bullets = [rewrite_map.get(b, b) for b in exp.bullets]
    for proj in resume.projects:
        proj.bullets = [rewrite_map.get(b, b) for b in proj.bullets]
    if rewrite_result.rewritten_summary:
        resume.summary = rewrite_result.rewritten_summary
    return resume


# ── Graph construction ────────────────────────────────────────────────────────

def build_graph() -> StateGraph:
    graph = StateGraph(APEXState)

    graph.add_node("parse", node_parse)
    graph.add_node("ats_score", node_ats_score)
    graph.add_node("critique", node_critique)
    graph.add_node("rewrite", node_rewrite)
    graph.add_node("cover_letter", node_cover_letter)
    graph.add_node("learning", node_learning)

    graph.set_entry_point("parse")

    graph.add_edge("parse", "ats_score")
    graph.add_edge("critique", "rewrite")
    graph.add_edge("rewrite", "ats_score")

    graph.add_conditional_edges(
        "ats_score",
        route_after_ats,
        {
            "critique": "critique",
            "cover_letter": "cover_letter",
        },
    )

    graph.add_edge("cover_letter", "learning")
    graph.add_edge("learning", END)

    return graph.compile()


apex_graph = build_graph()