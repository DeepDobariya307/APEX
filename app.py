"""
APEX — Main Streamlit Application

Render layer only. Session-state keys, the apex_graph.stream() loop and every
agent call behave exactly as before.
"""

import html
import logging
import os
import urllib.parse
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)

from config import config
from core.document_processor import DocumentProcessor
from graph.orchestrator import apex_graph
from graph.state import APEXState
from ui.styles import apply_styles, icon, gauge, graph_svg
from agents.interview_agent import InterviewAgent

st.set_page_config(
    page_title="APEX — AI Career Agent",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded",
)


def init_session():
    defaults = {
        "pipeline_result": None,
        "pipeline_ran": False,
        "agent_log": [],
        "interview_kit": None,
        "theme": "light",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


init_session()
apply_styles(st.session_state.theme)

processor = DocumentProcessor()
interview_agent = InterviewAgent()

if not os.getenv("ANTHROPIC_API_KEY"):
    st.error("ANTHROPIC_API_KEY is not set.")
    st.stop()


# ── Helpers ───────────────────────────────────────────────────────────────────

def esc(value) -> str:
    """Every model-generated string passes through here before touching HTML."""
    return html.escape("" if value is None else str(value), quote=True)


def md(html_str: str) -> None:
    st.markdown(html_str, unsafe_allow_html=True)


def tags(items, kind: str = "") -> str:
    cls = f"apex-tag {kind}".strip()
    return (
        '<div class="apex-tags">'
        + "".join(f'<span class="{cls}">{esc(i)}</span>' for i in items)
        + "</div>"
    )


NODE_ORDER = ["parse", "ats_score", "critique", "rewrite", "cover_letter", "learning"]


def _next_expected(last_node: str, state: dict):
    """Mirrors graph/orchestrator.py routing so the trace can show what's next."""
    if last_node == "parse":
        return "ats_score"
    if last_node == "ats_score":
        ats = state.get("ats_result")
        score = ats.ats_score if ats is not None else 0
        iteration = state.get("rewrite_iteration", 0)
        if score < config.ATS_PASS_THRESHOLD and iteration < config.MAX_REWRITE_ITERATIONS:
            return "critique"
        return "cover_letter"
    if last_node == "critique":
        return "rewrite"
    if last_node == "rewrite":
        return "ats_score"
    if last_node == "cover_letter":
        return "learning"
    return None


def render_trace(entries, running=None, finished=False) -> str:
    """The whole trace as one HTML string — painted into a single st.empty()."""
    done = {e["node"] for e in entries}

    seg = []
    for node in NODE_ORDER:
        if node == running and not finished:
            seg.append('<div class="now"><i></i></div>')
        elif node in done:
            seg.append('<div class="done"></div>')
        else:
            seg.append("<div></div>")

    lines = []
    for e in entries:
        lines.append(
            '<div class="apex-log-line">'
            f'{icon("check", 14, "var(--apex-accent)", 2.4)}'
            f'<span class="apex-log-node">{esc(e["node"])}</span>'
            f'<span>{esc(e["status"])}</span>'
            "</div>"
        )
    if running and not finished:
        lines.append(
            '<div class="apex-log-line now">'
            f'{icon("arrow-right", 14, "var(--apex-accent)")}'
            f'<span>{esc(running)}</span>'
            '<span class="apex-log-node">working…</span>'
            "</div>"
        )
        for node in NODE_ORDER[NODE_ORDER.index(running) + 1:]:
            lines.append(
                '<div class="apex-log-line queued">'
                "<span></span>"
                f"<span>{esc(node)}</span><span>Queued</span>"
                "</div>"
            )

    head = "Pipeline complete" if finished else "Working…"
    count = (
        f"{len(entries)} steps recorded" if finished
        else f"{len(done)} of {len(NODE_ORDER)} complete"
    )
    return (
        '<div class="apex-row">'
        f'<div class="apex-h-lg">{head}</div>'
        f'<div class="apex-kicker">{count}</div>'
        "</div>"
        f'<div class="apex-seg">{"".join(seg)}</div>'
        f'<div>{"".join(lines)}</div>'
    )


def strip_status(status: str) -> str:
    return status.replace("✅", "").strip()


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    md(
        '<div style="font-family:var(--apex-font);font-weight:700;font-size:34px;'
        'letter-spacing:-0.03em;color:var(--apex-display);line-height:1">APEX</div>'
        '<div class="apex-kicker" style="padding-top:7px">Six agents, one graph</div>'
    )
    st.divider()

    md('<div class="apex-kicker" style="margin-bottom:4.6px">Résumé</div>')
    resume_file = st.file_uploader(
        "Upload Resume", type=["pdf", "txt"], label_visibility="collapsed", key="resume_upload"
    )

    md('<div class="apex-kicker" style="margin:9.2px 0 4.6px">Job description</div>')
    jd_source = st.radio(
        "JD input method", ["Paste text", "Upload PDF"], horizontal=True, label_visibility="collapsed"
    )

    jd_text_input = None
    jd_file = None
    if jd_source == "Paste text":
        jd_text_input = st.text_area(
            "Paste JD",
            placeholder="Paste the full job description here…",
            height=180,
            label_visibility="collapsed",
        )
    else:
        jd_file = st.file_uploader(
            "Upload JD PDF", type=["pdf", "txt"], label_visibility="collapsed", key="jd_upload"
        )

    st.divider()
    md('<div class="apex-kicker" style="margin-bottom:4.6px">Application type</div>')
    internship_type = st.selectbox(
        "Application type",
        [
            "Mandatory Internship (Pflichtpraktikum)",
            "Voluntary Internship (Praktikum)",
            "Werkstudent (Working Student)",
            "Part-Time Position",
            "Mini Job (Geringfügige Beschäftigung)",
            "Full-Time Position",
        ],
        label_visibility="collapsed",
    )
    has_work_permit = st.checkbox("Mention German work permit in cover letter", value=True)

    st.divider()

    has_jd = bool(jd_text_input and jd_text_input.strip()) or jd_file is not None
    has_resume = resume_file is not None

    gate = []
    for met, label in ((has_resume, "Résumé attached"), (has_jd, "Job description added")):
        mark = (
            icon("check", 14, "var(--apex-accent)", 2.4) if met
            else icon("circle", 14, "var(--apex-faint)", 1.8)
        )
        gate.append(f'<div class="apex-gate-item {"met" if met else ""}">{mark}{esc(label)}</div>')
    md(f'<div class="apex-gate">{"".join(gate)}</div>')

    run_button = st.button(
        "Run the pipeline",
        type="primary",
        use_container_width=True,
        disabled=not (has_resume and has_jd),
    )
    md('<div class="apex-note" style="font-size:15px;padding-top:10px">About ninety seconds. Claude Sonnet and Haiku.</div>')

    if st.session_state.pipeline_ran:
        st.divider()
        if st.button("Reset", use_container_width=True):
            st.session_state.pipeline_result = None
            st.session_state.pipeline_ran = False
            st.session_state.agent_log = []
            st.session_state.interview_kit = None
            st.rerun()


# ── Top row: nav line + the theme switch ──────────────────────────────────────
nav_col, theme_col = st.columns([7, 1])
with nav_col:
    md(
        '<div style="display:flex;gap:20px;align-items:baseline;font-size:16px;padding-top:12px">'
        '<span style="font-weight:600">Pipeline</span>'
        f'<span style="color:var(--apex-dim)">LangGraph · six nodes · threshold {config.ATS_PASS_THRESHOLD}</span>'
        "</div>"
    )
with theme_col:
    going_dark = st.session_state.theme == "light"
    if st.button(
        "Dark" if going_dark else "Light",
        key="theme_toggle",
        use_container_width=True,
        help="Switch theme",
    ):
        st.session_state.theme = "dark" if going_dark else "light"
        st.rerun()


# ── Empty state ───────────────────────────────────────────────────────────────
if not st.session_state.pipeline_ran and not run_button:
    steps = [
        ("1", "Ingest", "Résumé and posting extracted to plain text with pdfplumber."),
        ("2", "Parse", "A strict profile: contact, skills, experience, projects."),
        ("3", "Optimise", f"Below {config.ATS_PASS_THRESHOLD} the graph loops: critique, rewrite, re-score."),
        ("4", "Produce", "Cover letter, interview kit, a roadmap for the gaps."),
    ]
    step_html = "".join(
        f'<div><div class="apex-step-num">{n}</div>'
        f'<div class="apex-step-title">{esc(t)}</div>'
        f'<div class="apex-step-body">{esc(d)}</div></div>'
        for n, t, d in steps
    )

    md(
        '<div class="apex-hero"><div class="apex-hero-field"></div>'
        '<div class="apex-hero-inner">'
        '<div class="apex-eyebrow"><span class="apex-dot"></span>Six agents · one graph · Claude</div>'
        '<div class="apex-display">Past the filter,<br><em>into the room.</em></div>'
        '<div class="apex-drawn-rule"></div>'
        '<div class="apex-lede">Six agents read your résumé the way an applicant tracking '
        "system does — then rewrite it the way a hiring manager reads. Scored, critiqued, "
        "and rewritten until it clears the threshold.</div>"
        "</div></div>"
        '<div class="apex-rule"></div>'
        f'<div class="apex-steps">{step_html}</div>'
        '<div class="apex-rule"></div>'
        '<div class="apex-kicker" style="padding-bottom:13.8px">The graph</div>'
        + graph_svg(config.ATS_PASS_THRESHOLD)
    )
    st.stop()


# ── Pipeline execution ────────────────────────────────────────────────────────
if run_button and resume_file is not None:
    st.session_state.pipeline_ran = False
    st.session_state.pipeline_result = None
    st.session_state.agent_log = []

    try:
        resume_text = processor.process_resume(resume_file)
        jd_source_input = jd_text_input if jd_source == "Paste text" else jd_file
        if not jd_source_input:
            st.error("Please provide a job description.")
            st.stop()
        jd_text = processor.process_job_description(jd_source_input)

        initial_state: APEXState = {
            "resume_text": resume_text,
            "jd_text": jd_text,
            "internship_type": internship_type,
            "has_work_permit": has_work_permit,
            "rewrite_iteration": 0,
            "completed_nodes": [],
        }

        full_state = {}
        full_state.update(initial_state)

        # One surface, repainted — not one alert box per node.
        trace_slot = st.empty()
        log = [{"node": "ingest", "status": f"Documents read — {len(resume_text)} characters"}]
        trace_slot.markdown(render_trace(log, running="parse"), unsafe_allow_html=True)

        for step in apex_graph.stream(initial_state):
            node_name = list(step.keys())[0]
            node_state = step[node_name]
            full_state.update(node_state)

            log.append({"node": node_name, "status": strip_status(node_state.get("status", f"{node_name} complete"))})
            # Persisted, so st.rerun() below does not destroy the run history.
            st.session_state.agent_log = list(log)

            trace_slot.markdown(
                render_trace(log, running=_next_expected(node_name, full_state)),
                unsafe_allow_html=True,
            )

        if full_state.get("error"):
            log.append({"node": "warning", "status": str(full_state["error"])})
            st.session_state.agent_log = list(log)

        st.session_state.pipeline_result = full_state
        st.session_state.pipeline_ran = True
        st.rerun()

    except Exception as e:
        import traceback
        st.error(f"Error: {e}")
        st.code(traceback.format_exc())


# ── Results ───────────────────────────────────────────────────────────────────
if st.session_state.pipeline_ran and st.session_state.pipeline_result:
    state = st.session_state.pipeline_result

    ats = state.get("ats_result")
    rewrite = state.get("rewrite_result")
    critique = state.get("critique_result")
    cover_letter = state.get("cover_letter")
    learning_roadmap = state.get("learning_roadmap")
    parsed_jd = state.get("parsed_jd")
    parsed_resume = state.get("parsed_resume")
    initial_score = state.get("initial_ats_score", ats.ats_score if ats else 0)
    iterations = state.get("rewrite_iteration", 0)

    role = getattr(parsed_jd, "job_title", "") or "This role"
    company = getattr(parsed_jd, "company", "")
    iter_label = "no rewrite" if iterations == 0 else ("one rewrite" if iterations == 1 else f"{iterations} rewrites")

    md(
        '<div class="apex-row">'
        f'<div class="apex-h-lg">{esc(role)}'
        + (f' <em>at {esc(company)}</em>' if company else "")
        + "</div>"
        f'<div class="apex-kicker">{esc(datetime.now().strftime("%d %B %Y"))} · {iter_label}</div>'
        "</div>"
    )

    if st.session_state.agent_log:
        with st.expander("Agent trace"):
            md(render_trace(st.session_state.agent_log, finished=True))

    tab_ats, tab_opt, tab_cover, tab_int, tab_learn = st.tabs(
        ["ATS score", "Optimisation", "Cover letter", "Interview prep", "Learning roadmap"]
    )

    # ── ATS ───────────────────────────────────────────────────────────────────
    with tab_ats:
        if ats:
            delta = ats.ats_score - initial_score
            foot = f"up {delta} after the rewrite" if delta > 0 else f"of {100}"
            cov = int(round(ats.keyword_coverage_pct))
            matched = len(ats.matched_skills)
            missing = len(ats.missing_required_skills)
            md(
                '<div class="apex-score">'
                + gauge(ats.ats_score, "ATS score", foot)
                + '<div class="apex-metrics">'
                '<div><div class="apex-metric-label">Keyword coverage</div>'
                f'<div class="apex-figure">{cov}<sup>%</sup></div>'
                f'<div class="apex-bar"><div style="width:{min(cov,100)}%"></div></div>'
                '<div class="apex-metric-foot">of the posting\'s keywords</div></div>'
                '<div><div class="apex-metric-label">Matched skills</div>'
                f'<div class="apex-figure">{matched}</div>'
                f'<div class="apex-bar"><div style="width:{min(matched * 4, 100)}%"></div></div>'
                '<div class="apex-metric-foot">found in the résumé</div></div>'
                '<div><div class="apex-metric-label">Missing required</div>'
                f'<div class="apex-figure apex-figure-quiet">{missing}</div>'
                f'<div class="apex-bar apex-bar-quiet"><div style="width:{min(missing * 12, 100)}%"></div></div>'
                '<div class="apex-metric-foot">skills still to close</div></div>'
                "</div></div>"
                '<div class="apex-rule"></div>'
            )

            if ats.strengths or ats.weaknesses:
                md(
                    '<div class="apex-two">'
                    '<div><div class="apex-h" style="padding-bottom:13.8px">Strengths</div>'
                    + "".join(f'<div class="apex-finding">{esc(s)}</div>' for s in ats.strengths)
                    + "</div>"
                    '<div><div class="apex-h" style="padding-bottom:13.8px">Weaknesses</div>'
                    + "".join(f'<div class="apex-finding apex-finding-quiet">{esc(w)}</div>' for w in ats.weaknesses)
                    + "</div></div><div class=\"apex-rule\"></div>"
                )

            blocks = []
            if ats.jd_matched_skills:
                blocks.append(
                    '<div><div class="apex-row" style="padding-bottom:13.8px">'
                    '<div class="apex-h">Relevant to this role</div>'
                    f'<div class="apex-kicker">{len(ats.jd_matched_skills)} matched</div></div>'
                    + tags(ats.jd_matched_skills) + "</div>"
                )
            if ats.missing_required_skills:
                blocks.append(
                    '<div><div class="apex-row" style="padding-bottom:13.8px">'
                    '<div class="apex-h">Required, not found</div>'
                    '<div class="apex-kicker">close these first</div></div>'
                    + tags(ats.missing_required_skills, "apex-tag-absent") + "</div>"
                )
            if ats.missing_preferred_skills:
                blocks.append(
                    '<div><div class="apex-h" style="padding-bottom:13.8px">Preferred, not found</div>'
                    + tags(ats.missing_preferred_skills, "apex-tag-neutral") + "</div>"
                )
            if parsed_resume and parsed_resume.skills_categorized:
                cats = "".join(
                    f'<div style="padding-top:13.8px"><div class="apex-metric-label" '
                    f'style="padding-bottom:6px">{esc(cat)}</div>{tags(sk)}</div>'
                    for cat, sk in parsed_resume.skills_categorized.items() if sk
                )
                if cats:
                    blocks.append(f'<div><div class="apex-h">Your résumé skills</div>{cats}</div>')
            if ats.suggested_renames:
                rows = "".join(
                    f"<tr><td>{esc(r.resume_term)}</td>"
                    f'<td class="gold">{esc(r.suggested_term)}</td>'
                    f'<td class="quiet">{esc(r.jd_term)}</td></tr>'
                    for r in ats.suggested_renames
                )
                blocks.append(
                    '<div><div class="apex-h" style="padding-bottom:9.2px">Suggested renames</div>'
                    '<table class="apex-table"><thead><tr><th>Your term</th><th>Rename to</th>'
                    f"<th>Matches</th></tr></thead><tbody>{rows}</tbody></table></div>"
                )
            if blocks:
                md('<div style="display:flex;flex-direction:column;gap:27.6px">' + "".join(blocks) + "</div>")
        else:
            md('<div class="apex-note">ATS result not available.</div>')

    # ── Optimisation ──────────────────────────────────────────────────────────
    with tab_opt:
        bits = [b for b in [
            iter_label if iterations else "",
            f"{initial_score} → {ats.ats_score}" if ats else "",
            f"{len(rewrite.keywords_injected)} keywords" if rewrite and rewrite.keywords_injected else "",
        ] if b]
        md(
            '<div class="apex-row">'
            '<div class="apex-h-lg">Critique &amp; rewrite</div>'
            f'<div class="apex-kicker">{esc(" · ".join(bits))}</div></div>'
        )

        if critique:
            if critique.overall_assessment:
                md(f'<div class="apex-quote">{esc(critique.overall_assessment)}</div>')
            if critique.priority_fixes:
                md(
                    '<div class="apex-h" style="padding-bottom:13.8px">Priority fixes</div>'
                    '<div class="apex-numlist">'
                    + "".join(
                        f'<div class="apex-numitem"><span>{i}</span><span>{esc(fx)}</span></div>'
                        for i, fx in enumerate(critique.priority_fixes, 1)
                    )
                    + "</div>"
                )
        else:
            md('<div class="apex-quote">The score already cleared the threshold, so no rewrite was needed.</div>')

        if rewrite:
            pairs = []
            for rb in rewrite.rewritten_bullets:
                if rb.rewritten:
                    right = (
                        '<div class="apex-diff-label after">After</div>'
                        f'<div class="apex-after">{esc(rb.rewritten)}</div>'
                    )
                else:
                    right = (
                        '<div class="apex-diff-label">De-emphasise</div>'
                        '<div class="apex-before">Limited relevance to this role. Drop it from this '
                        "application, but keep it on the master résumé.</div>"
                    )
                pairs.append(
                    '<div class="apex-diff-pair">'
                    '<div><div class="apex-diff-label">Before</div>'
                    f'<div class="apex-before">{esc(rb.original)}</div></div>'
                    f"<div>{right}</div></div>"
                )
            if pairs:
                md(
                    '<div class="apex-rule"></div>'
                    '<div class="apex-h" style="padding-bottom:9.2px">Bullet by bullet</div>'
                    + "".join(pairs)
                )
            if rewrite.rewritten_summary:
                md(
                    '<div class="apex-h" style="padding:27.6px 0 9.2px">Rewritten summary</div>'
                    f'<div class="apex-prose">{esc(rewrite.rewritten_summary)}</div>'
                )
            if rewrite.keywords_injected:
                md(
                    '<div class="apex-h" style="padding:27.6px 0 13.8px">Keywords injected</div>'
                    + tags(rewrite.keywords_injected)
                )

    # ── Cover letter ──────────────────────────────────────────────────────────
    with tab_cover:
        if cover_letter:
            contact = getattr(parsed_resume, "contact", None)
            name = getattr(contact, "name", "") if contact else ""
            location = getattr(contact, "location", "") if contact else ""
            email = getattr(contact, "email", "") if contact else ""
            phone = getattr(contact, "phone", "") if contact else ""
            contact_line = " · ".join([x for x in [email, phone] if x])

            md(
                '<div class="apex-row" style="padding-bottom:27.6px">'
                '<div class="apex-h-lg">Cover letter</div>'
                f'<div class="apex-kicker">{cover_letter.word_count} words'
                + (f" · {len(cover_letter.keywords_used)} keywords" if cover_letter.keywords_used else "")
                + "</div></div>"
            )

            # One HTML block: Streamlit renders separate calls as siblings, so the
            # letter body cannot be a child of the plate any other way.
            paragraphs = "".join(
                f"<p>{esc(p.strip())}</p>" for p in cover_letter.body.split("\n\n") if p.strip()
            )
            from_lines = "<br>".join(esc(x) for x in [name, location, contact_line] if x)
            md(
                '<div class="apex-plate">'
                f'<div class="muted" style="text-align:right;font-size:13.5px;line-height:1.8">{from_lines}</div>'
                f'<div class="muted" style="font-size:13.5px;padding:27.6px 0 18.4px">{esc(datetime.now().strftime("%d %B %Y"))}</div>'
                f'<div class="apex-plate-subject">{esc(cover_letter.subject_line)}</div>'
                f"{paragraphs}"
                f'<p style="font-style:italic">{esc(name)}</p>'
                "</div>"
            )

            if cover_letter.keywords_used:
                md(
                    '<div class="apex-rule"></div>'
                    '<div class="apex-h" style="padding-bottom:13.8px">Keywords used</div>'
                    + tags(cover_letter.keywords_used)
                )
            md('<div class="apex-rule"></div>')
            st.download_button(
                "Download .txt",
                data=f"{cover_letter.body}\n\n{name}",
                file_name="cover_letter.txt",
                mime="text/plain",
            )
        else:
            md('<div class="apex-note">Cover letter not available.</div>')

    # ── Interview prep ────────────────────────────────────────────────────────
    with tab_int:
        if st.session_state.interview_kit is None:
            md(
                '<div class="apex-h-lg">Interview prep</div>'
                '<div class="apex-note" style="padding:13.8px 0 27.6px">A tailored kit: HR, '
                "technical, behavioural and project questions drawn from this résumé and this "
                "role. It takes a minute or two and spends additional API credits.</div>"
            )
            if st.button("Prepare for interview", type="primary"):
                with st.spinner("Generating the interview kit…"):
                    try:
                        st.session_state.interview_kit = interview_agent.generate_kit(
                            parsed_resume, parsed_jd
                        )
                        st.rerun()
                    except Exception as e:
                        import traceback
                        st.error(f"Interview kit generation failed: {e}")
                        st.code(traceback.format_exc())
        else:
            kit = st.session_state.interview_kit
            for title, questions in [
                ("HR", kit.hr_questions),
                ("Technical", kit.technical_questions),
                ("Behavioural", kit.behavioral_questions),
                ("Project discussion", kit.project_questions),
            ]:
                if not questions:
                    continue
                md(
                    '<div class="apex-row" style="padding:9.2px 0">'
                    f'<div class="apex-h">{esc(title)}</div>'
                    f'<div class="apex-kicker">{len(questions)} questions</div></div>'
                )
                for i, q in enumerate(questions, 1):
                    with st.expander(f"{i}. {q.question}"):
                        md(
                            '<div style="border-left:2px solid var(--apex-accent);padding-left:13.8px">'
                            '<div class="apex-metric-label" style="color:var(--apex-accent-text);'
                            'padding-bottom:9.2px">Suggested answer</div>'
                            f'<div class="apex-prose">{esc(q.suggested_answer)}</div>'
                            + (
                                '<div class="apex-metric-label" style="padding:18.4px 0 9.2px">Tip</div>'
                                f'<div class="apex-prose">{esc(q.tips)}</div>' if q.tips else ""
                            )
                            + "</div>"
                        )
                md('<div class="apex-rule"></div>')
            if st.button("Regenerate interview kit"):
                st.session_state.interview_kit = None
                st.rerun()

    # ── Learning roadmap ──────────────────────────────────────────────────────
    with tab_learn:
        if learning_roadmap:
            md(
                '<div class="apex-h-lg">Learning roadmap</div>'
                + (
                    f'<div class="apex-note" style="padding-top:13.8px">Ready in '
                    f"{esc(learning_roadmap.estimated_ready_in)}.</div>"
                    if learning_roadmap.estimated_ready_in else ""
                )
            )

            if learning_roadmap.quick_wins:
                md(
                    '<div class="apex-h" style="padding:27.6px 0 4.6px">Quick wins</div>'
                    '<div class="apex-note" style="padding-bottom:13.8px">Under a week each</div>'
                    '<div class="apex-numlist">'
                    + "".join(
                        f'<div class="apex-numitem"><span>{i}</span><span>{esc(w)}</span></div>'
                        for i, w in enumerate(learning_roadmap.quick_wins, 1)
                    )
                    + "</div>"
                )

            if learning_roadmap.resources:
                rows = []
                for r in learning_roadmap.resources:
                    url = ""
                    if r.search_query:
                        q = urllib.parse.quote(r.search_query)
                        p = (r.platform or "").lower()
                        if "youtube" in p:
                            url = f"https://www.youtube.com/results?search_query={q}"
                        elif "coursera" in p:
                            url = f"https://www.coursera.org/search?query={q}"
                        elif "udemy" in p:
                            url = f"https://www.udemy.com/courses/search/?q={q}"
                        else:
                            url = f"https://www.google.com/search?q={q}"
                    link = f' · <a href="{esc(url)}" target="_blank" rel="noopener">find it</a>' if url else ""
                    detail = " · ".join([x for x in [esc(r.platform), esc(r.resource_type), esc(r.estimated_time)] if x])
                    cls = "apex-tag" if (r.priority or "").lower() == "high" else "apex-tag apex-tag-neutral"
                    rows.append(
                        f'<tr><td>{esc(r.skill)}</td>'
                        f'<td class="quiet" style="font-style:normal">{esc(r.resource_name)}<br>{detail}{link}</td>'
                        f'<td class="right"><span class="{cls}">{esc(r.priority)}</span></td></tr>'
                    )
                md(
                    '<div class="apex-rule"></div>'
                    '<table class="apex-table"><thead><tr><th>Skill</th><th>Resource</th>'
                    f'<th class="right">Priority</th></tr></thead><tbody>{"".join(rows)}</tbody></table>'
                )

            if learning_roadmap.project_ideas:
                md(
                    '<div class="apex-h" style="padding:36.8px 0 13.8px">Portfolio projects</div>'
                    '<div class="apex-numlist">'
                    + "".join(
                        f'<div class="apex-numitem"><span>{i}</span><span>{esc(idea)}</span></div>'
                        for i, idea in enumerate(learning_roadmap.project_ideas, 1)
                    )
                    + "</div>"
                )
        else:
            md('<div class="apex-note">Learning roadmap not available.</div>')
