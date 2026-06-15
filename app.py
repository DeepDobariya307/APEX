"""
APEX — Main Streamlit Application
"""

import email
import os
import logging
import urllib.parse

import streamlit as st
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)

from core.document_processor import DocumentProcessor
from graph.orchestrator import apex_graph
from graph.state import APEXState
from ui.styles import apply_styles
from agents.interview_agent import InterviewAgent

st.set_page_config(
    page_title="APEX — AI Career Agent",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)
apply_styles()

processor = DocumentProcessor()
interview_agent = InterviewAgent()

def init_session():
    defaults = {
        "pipeline_result": None,
        "pipeline_ran": False,
        "agent_log": [],
        "interview_kit": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_session()

if not os.getenv("ANTHROPIC_API_KEY"):
    st.error("ANTHROPIC_API_KEY is not set.")
    st.stop()


# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="apex-title">⚡ APEX</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="apex-subtitle">AI Career Agent · Claude Powered</div>',
        unsafe_allow_html=True,
    )
    st.divider()

    st.markdown("**📄 Resume**")
    resume_file = st.file_uploader(
        "Upload Resume",
        type=["pdf", "txt"],
        label_visibility="collapsed",
        key="resume_upload",
    )

    st.markdown("**📋 Job Description**")
    jd_source = st.radio(
        "JD input method",
        ["Paste text", "Upload PDF"],
        horizontal=True,
        label_visibility="collapsed",
    )

    jd_text_input = None
    jd_file = None
    if jd_source == "Paste text":
        jd_text_input = st.text_area(
            "Paste JD",
            placeholder="Paste the full job description here...",
            height=200,
            label_visibility="collapsed",
        )
    else:
        jd_file = st.file_uploader(
            "Upload JD PDF",
            type=["pdf", "txt"],
            label_visibility="collapsed",
            key="jd_upload",
        )

    st.divider()

    st.markdown("**⚙️ Options**")
    internship_type = st.selectbox(
        "Application type",
        [
            "mandatory internship (Pflichtpraktikum)",
            "voluntary internship (Praktikum)",
            "Werkstudent (working student)",
            "part-time position",
            "mini job (geringfügige Beschäftigung)",
            "full-time position",
        ],
    )
    has_work_permit = st.checkbox("Mention German work permit in cover letter", value=True)

    st.divider()

    run_button = st.button(
        "⚡ Analyse & Generate",
        type="primary",
        use_container_width=True,
        disabled=(resume_file is None),
    )

    if st.session_state.pipeline_ran:
        if st.button("🔄 Reset", use_container_width=True):
            st.session_state.pipeline_result = None
            st.session_state.pipeline_ran = False
            st.session_state.agent_log = []
            st.session_state.interview_kit = None
            st.rerun()


# ── Main area ──────────────────────────────────────────────────────────────────
st.markdown('<div class="apex-title">⚡ APEX</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="apex-subtitle">AI-Powered Executive Career Agent</div>',
    unsafe_allow_html=True,
)

# ── Empty state ────────────────────────────────────────────────────────────────
if not st.session_state.pipeline_ran and not run_button:
    col1, col2, col3, col4 = st.columns(4)
    card = (
        "background:#111118; border:1px solid rgba(245,158,11,0.2); border-radius:12px;"
        "padding:1.5rem 1rem; text-align:center; height:170px;"
        "display:flex; flex-direction:column; justify-content:center; gap:0.5rem;"
    )
    steps = [
        ("📤", "Upload", "Resume PDF + job description"),
        ("🔍", "Parse", "AI extracts structured profile"),
        ("🔄", "Optimise", "Critique→Rewrite loop boosts ATS score"),
        ("📦", "Generate", "Cover letter, interview kit, learning roadmap"),
    ]
    for col, (icon, title, desc) in zip([col1, col2, col3, col4], steps):
        with col:
            st.markdown(
                f"<div style='{card}'>"
                f"<div style='font-size:1.8rem'>{icon}</div>"
                f"<div style='color:#f59e0b; font-weight:600; font-size:0.9rem'>{title}</div>"
                f"<div style='color:#6b7280; font-size:0.78rem; line-height:1.4'>{desc}</div>"
                f"</div>",
                unsafe_allow_html=True,
            )
    st.stop()


# ── Pipeline execution ─────────────────────────────────────────────────────────
if run_button and resume_file is not None:
    st.session_state.pipeline_ran = False
    st.session_state.pipeline_result = None
    st.session_state.agent_log = []

    try:
        st.info("📄 Processing documents...")

        resume_text = processor.process_resume(resume_file)

        jd_source_input = jd_text_input if jd_source == "Paste text" else jd_file
        if not jd_source_input:
            st.error("Please provide a job description.")
            st.stop()

        jd_text = processor.process_job_description(jd_source_input)
        st.success(f"✅ Documents processed — Resume: {len(resume_text)} chars")

        st.info("🤖 Running agents — this takes 1-2 minutes...")

        initial_state: APEXState = {
            "resume_text": resume_text,
            "jd_text": jd_text,
            "internship_type": internship_type,
            "has_work_permit": has_work_permit,
            "rewrite_iteration": 0,
            "completed_nodes": [],
        }

        # Run graph ONCE and collect all state updates
        full_state = {}
        full_state.update(initial_state)

        for step in apex_graph.stream(initial_state):
            node_name = list(step.keys())[0]
            node_state = step[node_name]
            full_state.update(node_state)
            status_msg = node_state.get("status", f"Running {node_name}...")
            st.info(f"⚙️ {status_msg}")

        if full_state.get("error"):
            st.warning(f"Minor issue: {full_state['error']}")

        st.session_state.pipeline_result = full_state
        st.session_state.pipeline_ran = True
        st.rerun()

    except Exception as e:
        import traceback
        st.error(f"Error: {e}")
        st.code(traceback.format_exc())

# ── Results dashboard ──────────────────────────────────────────────────────────
if st.session_state.pipeline_ran and st.session_state.pipeline_result:
    state = st.session_state.pipeline_result

    ats = state.get("ats_result")
    rewrite = state.get("rewrite_result")
    critique = state.get("critique_result")
    cover_letter = state.get("cover_letter")
    learning_roadmap = state.get("learning_roadmap")
    initial_score = state.get("initial_ats_score", ats.ats_score if ats else 0)

    tab_ats, tab_optimise, tab_cover, tab_interview, tab_learning = st.tabs([
        "📊 ATS Score",
        "✏️ Optimisation",
        "📝 Cover Letter",
        "🎤 Interview Prep",
        "📚 Learning Roadmap",
    ])

    # ── ATS Score ──────────────────────────────────────────────────────────────
    with tab_ats:
        if ats:
            # ── 4 metrics horizontally ─────────────────────────────────────
            m1, m2, m3, m4 = st.columns(4)

            score_class = (
                "score-high" if ats.ats_score >= 75
                else "score-medium" if ats.ats_score >= 50
                else "score-low"
            )
            delta = ats.ats_score - initial_score
            delta_html = (
                f"<div style='color:#22c55e; font-size:0.82rem; margin-top:0.3rem'>▲ +{delta} after optimisation</div>"
                if delta > 0 else ""
            )

            with m1:
                st.markdown(
                    f"<div class='score-card'>"
                    f"<div style='color:#9ca3af; font-size:0.7rem; text-transform:uppercase; letter-spacing:0.1em; margin-bottom:0.4rem'>ATS Score</div>"
                    f"<div class='score-number {score_class}'>{ats.ats_score}</div>"
                    f"<div style='color:#6b7280; font-size:0.75rem'>/100</div>"
                    f"{delta_html}"
                    f"</div>",
                    unsafe_allow_html=True,
                )

            with m2:
                st.markdown(
                    f"<div class='score-card'>"
                    f"<div style='color:#9ca3af; font-size:0.7rem; text-transform:uppercase; letter-spacing:0.1em; margin-bottom:0.4rem'>Keyword Coverage</div>"
                    f"<div class='score-number score-medium'>{ats.keyword_coverage_pct:.0f}%</div>"
                    f"<div style='color:#6b7280; font-size:0.75rem'>of JD keywords</div>"
                    f"</div>",
                    unsafe_allow_html=True,
                )

            with m3:
                st.markdown(
                    f"<div class='score-card'>"
                    f"<div style='color:#9ca3af; font-size:0.7rem; text-transform:uppercase; letter-spacing:0.1em; margin-bottom:0.4rem'>Matched Skills</div>"
                    f"<div class='score-number score-high'>{len(ats.matched_skills)}</div>"
                    f"<div style='color:#6b7280; font-size:0.75rem'>skills found</div>"
                    f"</div>",
                    unsafe_allow_html=True,
                )

            with m4:
                st.markdown(
                    f"<div class='score-card'>"
                    f"<div style='color:#9ca3af; font-size:0.7rem; text-transform:uppercase; letter-spacing:0.1em; margin-bottom:0.4rem'>Missing Required</div>"
                    f"<div class='score-number score-low'>{len(ats.missing_required_skills)}</div>"
                    f"<div style='color:#6b7280; font-size:0.75rem'>skills gap</div>"
                    f"</div>",
                    unsafe_allow_html=True,
                )

            st.markdown("<br>", unsafe_allow_html=True)

            # ── Strengths and weaknesses side by side ──────────────────────
            col_str, col_weak = st.columns(2)

            with col_str:
                if ats.strengths:
                    st.markdown("#### ✅ Strengths")
                    for s in ats.strengths:
                        st.markdown(f"- {s}")

            with col_weak:
                if ats.weaknesses:
                    st.markdown("#### ⚠️ Weaknesses")
                    for w in ats.weaknesses:
                        st.markdown(f"- {w}")

            st.divider()

            # ── Skill pills ────────────────────────────────────────────────
            # ── Skill Analysis (5 categories) ────────────────────────────────
            st.markdown("#### 🔑 Skill Analysis")

            parsed_resume = state.get("parsed_resume")

            # 1. Resume skills (categorized)
            if parsed_resume and parsed_resume.skills_categorized:
                st.markdown(
    "<div style='font-size:1.05rem; font-weight:700; color:#fcd34d; margin-top:0.5rem; margin-bottom:0.3rem;'>"
    "1. Your Resume Skills</div>",
    unsafe_allow_html=True,
)
                for category, skill_list in parsed_resume.skills_categorized.items():
                    if skill_list:
                        st.markdown(f"*{category}*")
                        pills = "".join(
                            f'<span class="skill-pill skill-matched">{s}</span>'
                            for s in skill_list
                        )
                        st.markdown(pills, unsafe_allow_html=True)

            st.markdown("")

            # 2. Skills matching this JD
            if ats.jd_matched_skills:
                st.markdown(
    "<div style='font-size:1.05rem; font-weight:700; color:#fcd34d; margin-top:0.5rem; margin-bottom:0.3rem;'>"
    "2. Your Skills Relevant to This Role</div>",
    unsafe_allow_html=True,
)
                pills = "".join(
                    f'<span class="skill-pill skill-matched">{s}</span>'
                    for s in ats.jd_matched_skills
                )
                st.markdown(pills, unsafe_allow_html=True)

            st.markdown("")

            # 3. Suggested renames
            if ats.suggested_renames:
                st.markdown(
    "<div style='font-size:1.05rem; font-weight:700; color:#fcd34d; margin-top:0.5rem; margin-bottom:0.3rem;'>"
    "3. Suggested Keyword Renames</div>",
    unsafe_allow_html=True,
)
                for r in ats.suggested_renames:
                    st.markdown(
                        f"- Consider changing **\"{r.resume_term}\"** → "
                        f"**\"{r.suggested_term}\"** (matches JD term: *{r.jd_term}*)"
                    )

            st.markdown("")

            # 4. Missing required skills
            if ats.missing_required_skills:
                st.markdown(
    "<div style='font-size:1.05rem; font-weight:700; color:#fcd34d; margin-top:0.5rem; margin-bottom:0.3rem;'>"
    "4. Must-Have Skills Not Found in Your Resume</div>",
    unsafe_allow_html=True,
)
                pills = "".join(
                    f'<span class="skill-pill skill-missing">{s}</span>'
                    for s in ats.missing_required_skills
                )
                st.markdown(pills, unsafe_allow_html=True)

            st.markdown("")

            # 5. Missing preferred skills
            if ats.missing_preferred_skills:
                st.markdown(
    "<div style='font-size:1.05rem; font-weight:700; color:#fcd34d; margin-top:0.5rem; margin-bottom:0.3rem;'>"
    "5. Preferred Skills Not Found in Your Resume</div>",
    unsafe_allow_html=True,
)
                pills = "".join(
                    f'<span class="skill-pill skill-preferred">{s}</span>'
                    for s in ats.missing_preferred_skills
                )
                st.markdown(pills, unsafe_allow_html=True)
        else:
            st.warning("ATS result not available.")

    # ── Optimisation ───────────────────────────────────────────────────────────
    with tab_optimise:
        iterations = state.get("rewrite_iteration", 0)

        if critique:
            st.markdown("#### 🔍 Critique Analysis")
            if critique.overall_assessment:
                st.info(critique.overall_assessment)
            if critique.priority_fixes:
                st.markdown("**Priority Fixes**")
                for i, fix in enumerate(critique.priority_fixes, 1):
                    st.markdown(f"{i}. {fix}")
        else:
            st.info("ATS score was above threshold — no rewrite needed.")

        if rewrite:
            st.markdown("#### ✏️ Rewritten Bullets")
            for rb in rewrite.rewritten_bullets:
                if rb.rewritten:
                    st.markdown(
                        f'<div class="bullet-before">❌ {rb.original}</div>'
                        f'<div class="bullet-after">✅ {rb.rewritten}</div>',
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        f'<div class="bullet-before">❌ {rb.original}</div>'
                        f'<div class="bullet-after" style="border-left-color:#f59e0b; color:#fcd34d;">'
                        f'⚠️ Recommend removing this bullet — no honest reframing fits this role.</div>',
                        unsafe_allow_html=True,
                    )
                    
            if rewrite.rewritten_summary:
                st.markdown("#### 📝 Rewritten Summary")
                st.success(rewrite.rewritten_summary)
            if rewrite.keywords_injected:
                st.markdown("**Keywords injected:**")
                pills = "".join(
                    f'<span class="skill-pill skill-matched">{kw}</span>'
                    for kw in rewrite.keywords_injected
                )
                st.markdown(pills, unsafe_allow_html=True)

    # ── Cover Letter ───────────────────────────────────────────────────────────
    with tab_cover:
        if cover_letter:
            st.markdown(f"**Word count:** {cover_letter.word_count}")
            st.divider()

            from datetime import datetime
            today = datetime.now().strftime("%d %B %Y")

            parsed_resume = state.get("parsed_resume")
            candidate_name = parsed_resume.contact.name if parsed_resume else ""
            candidate_location = parsed_resume.contact.location if parsed_resume else ""
            candidate_email = parsed_resume.contact.email if parsed_resume else ""
            candidate_phone = parsed_resume.contact.phone if parsed_resume else ""

            contact_line = " | ".join(filter(None, [candidate_email, candidate_phone]))

            header_html = (
                "<div style='text-align:right; line-height:1.6; margin-bottom:1.5rem;'>"
                f"<div>{candidate_name}</div>"
                f"<div>{candidate_location}</div>"
                f"<div>{contact_line}</div>"
                "</div>"
                f"<div style='margin-bottom:1.5rem;'>{today}</div>"
                "<div style='text-align:center; font-weight:600; text-decoration:underline; margin-bottom:1.5rem;'>"
                f"Subject: {cover_letter.subject_line}</div>"
            )
            st.markdown(header_html, unsafe_allow_html=True)

            st.markdown(cover_letter.body)
            st.markdown(candidate_name)

            if cover_letter.keywords_used:
                st.divider()
                st.markdown("**JD keywords used:**")
                pills = "".join(
                    f'<span class="skill-pill skill-matched">{kw}</span>'
                    for kw in cover_letter.keywords_used
                )
                st.markdown(pills, unsafe_allow_html=True)

            st.divider()
            full_letter_text = f"{cover_letter.body}\n\n{candidate_name}"
            st.download_button(
                "📥 Download .txt",
                data=full_letter_text,
                file_name="cover_letter.txt",
                mime="text/plain",
            )
        else:
            st.warning("Cover letter not available.")

    # ── Interview Prep ─────────────────────────────────────────────────────────
    with tab_interview:
        if st.session_state.interview_kit is None:
            st.markdown(
                "Generate a tailored interview preparation kit — HR, technical, "
                "behavioral, and project-specific questions based on this resume and role."
            )
            st.caption("This takes about 1-2 minutes and uses additional API credits — "
                       "only generate this if you're confident about this application.")

            if st.button("🎤 Prepare for Interview", type="primary"):
                with st.spinner("Generating interview kit..."):
                    try:
                        parsed_resume = state.get("parsed_resume")
                        parsed_jd = state.get("parsed_jd")
                        kit = interview_agent.generate_kit(parsed_resume, parsed_jd)
                        st.session_state.interview_kit = kit
                        st.rerun()
                    except Exception as e:
                        import traceback
                        st.error(f"Interview kit generation failed: {e}")
                        st.code(traceback.format_exc())
        else:
            kit = st.session_state.interview_kit
            sections = [
                ("👤 HR Questions", kit.hr_questions),
                ("💻 Technical Questions", kit.technical_questions),
                ("🌟 Behavioral Questions", kit.behavioral_questions),
                ("🚀 Project Discussion", kit.project_questions),
            ]
            for section_title, questions in sections:
                if questions:
                    st.markdown(f"#### {section_title}")
                    for i, q in enumerate(questions, 1):
                        with st.expander(f"Q{i}: {q.question}"):
                            st.markdown(f"**💡 Suggested Answer:**\n{q.suggested_answer}")
                            if q.tips:
                                st.markdown(f"**🎯 Tip:** {q.tips}")
                    st.divider()

            if st.button("🔄 Regenerate Interview Kit"):
                st.session_state.interview_kit = None
                st.rerun()

    # ── Learning Roadmap ───────────────────────────────────────────────────────
    with tab_learning:
        if learning_roadmap:
            if learning_roadmap.estimated_ready_in:
                st.info(f"⏱️ Estimated time to close all high-priority gaps: **{learning_roadmap.estimated_ready_in}**")

            if learning_roadmap.quick_wins:
                st.markdown("#### ⚡ Quick Wins (< 1 week each)")
                for qw in learning_roadmap.quick_wins:
                    st.markdown(f"- {qw}")

            if learning_roadmap.resources:
                st.markdown("#### 📚 Learning Resources")
                for r in learning_roadmap.resources:
                    priority_color = (
                        "#ef4444" if r.priority == "high"
                        else "#f59e0b" if r.priority == "medium"
                        else "#6b7280"
                    )
                    search_url = ""
                    if r.search_query:
                        query_encoded = urllib.parse.quote(r.search_query)
                        platform_lower = r.platform.lower()
                        if "youtube" in platform_lower:
                            search_url = f"https://www.youtube.com/results?search_query={query_encoded}"
                        elif "coursera" in platform_lower:
                            search_url = f"https://www.coursera.org/search?query={query_encoded}"
                        elif "udemy" in platform_lower:
                            search_url = f"https://www.udemy.com/courses/search/?q={query_encoded}"
                        else:
                            search_url = f"https://www.google.com/search?q={query_encoded}"

                    link_html = (
                        f" · <a href='{search_url}' target='_blank' style='color:#fcd34d;'>Find it →</a>"
                        if search_url else ""
                    )

                    st.markdown(
                        f"<div class='section-card'>"
                        f"<div style='display:flex; justify-content:space-between; align-items:center;'>"
                        f"<span style='font-weight:600; color:#e2e0f0'>{r.skill}</span>"
                        f"<span style='color:{priority_color}; font-size:0.72rem; text-transform:uppercase'>{r.priority} priority</span>"
                        f"</div>"
                        f"<div style='color:#9ca3af; font-size:0.85rem; margin-top:0.4rem'>"
                        f"<strong>{r.resource_name}</strong> — {r.platform} · {r.resource_type} · {r.estimated_time}{link_html}"
                        f"</div>"
                        f"</div>",
                        unsafe_allow_html=True,
                    )
            if learning_roadmap.project_ideas:
                st.markdown("#### 💡 Portfolio Project Ideas")
                for i, idea in enumerate(learning_roadmap.project_ideas, 1):
                    st.markdown(f"**{i}.** {idea}")
        else:
            st.warning("Learning roadmap not available.")