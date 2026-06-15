"""
APEX — UI Styles
Dark amber theme. Distinct from RAGNAROK.
"""

APEX_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, .stApp {
    font-family: 'Inter', sans-serif !important;
    background-color: #0a0a0f !important;
}

.block-container {
    padding-top: 5rem !important;
    max-width: 960px !important;
}

[data-testid="stSidebar"] {
    background-color: #0f0f18 !important;
    border-right: 1px solid rgba(245, 158, 11, 0.2) !important;
}

.apex-title {
    font-size: 2.2rem;
    font-weight: 700;
    background: linear-gradient(135deg, #f59e0b, #d97706);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -0.02em;
    line-height: 1.1;
}

.apex-subtitle {
    font-size: 0.72rem;
    color: #6b7280;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
    font-family: 'JetBrains Mono', monospace;
}

.score-card {
    background: linear-gradient(135deg, #1a1410, #1f1a0f);
    border: 1px solid rgba(245, 158, 11, 0.3);
    border-radius: 16px;
    padding: 2rem;
    text-align: center;
}

.score-number {
    font-size: 4rem;
    font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
    line-height: 1;
}

.score-high   { color: #22c55e; }
.score-medium { color: #f59e0b; }
.score-low    { color: #ef4444; }

.agent-step {
    background: #111118;
    border: 1px solid rgba(245, 158, 11, 0.12);
    border-left: 3px solid #f59e0b;
    border-radius: 0 8px 8px 0;
    padding: 0.6rem 1rem;
    margin-bottom: 0.4rem;
    font-size: 0.82rem;
    color: #9ca3af;
    font-family: 'JetBrains Mono', monospace;
}

.agent-step.running {
    border-left-color: #3b82f6;
    color: #93c5fd;
    background: #0f1520;
}

.agent-step.done {
    border-left-color: #22c55e;
    color: #86efac;
    background: #0f1a12;
}

.section-card {
    background: #111118;
    border: 1px solid rgba(245, 158, 11, 0.15);
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}

.skill-pill {
    display: inline-block;
    padding: 0.2rem 0.65rem;
    border-radius: 20px;
    font-size: 0.75rem;
    font-family: 'JetBrains Mono', monospace;
    margin: 0.15rem;
}

.skill-matched {
    background: rgba(34, 197, 94, 0.15);
    border: 1px solid rgba(34, 197, 94, 0.4);
    color: #86efac;
}

.skill-missing {
    background: rgba(239, 68, 68, 0.12);
    border: 1px solid rgba(239, 68, 68, 0.35);
    color: #fca5a5;
}

.skill-preferred {
    background: rgba(245, 158, 11, 0.12);
    border: 1px solid rgba(245, 158, 11, 0.35);
    color: #fcd34d;
}

.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #d97706, #b45309) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
}

.stButton > button[kind="primary"]:hover {
    box-shadow: 0 4px 20px rgba(245, 158, 11, 0.35) !important;
    transform: translateY(-1px) !important;
}

[data-testid="stMetric"] {
    background: #111118 !important;
    border: 1px solid rgba(245, 158, 11, 0.2) !important;
    border-radius: 10px !important;
    padding: 1rem !important;
}

[data-testid="stExpander"] {
    background: #111118 !important;
    border: 1px solid rgba(245, 158, 11, 0.1) !important;
    border-radius: 8px !important;
}

.bullet-before {
    background: rgba(239, 68, 68, 0.08);
    border-left: 3px solid #ef4444;
    padding: 0.5rem 0.75rem;
    border-radius: 0 6px 6px 0;
    font-size: 0.82rem;
    color: #fca5a5;
    font-family: 'JetBrains Mono', monospace;
    margin-bottom: 0.25rem;
}

.bullet-after {
    background: rgba(34, 197, 94, 0.08);
    border-left: 3px solid #22c55e;
    padding: 0.5rem 0.75rem;
    border-radius: 0 6px 6px 0;
    font-size: 0.82rem;
    color: #86efac;
    font-family: 'JetBrains Mono', monospace;
    margin-bottom: 0.75rem;
}

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #0a0a0f; }
::-webkit-scrollbar-thumb {
    background: rgba(245, 158, 11, 0.35);
    border-radius: 2px;
}

hr { border-color: rgba(245, 158, 11, 0.12) !important; }
</style>
"""


def apply_styles():
    import streamlit as st
    st.markdown(APEX_CSS, unsafe_allow_html=True)