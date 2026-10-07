"""
APEX — UI Styles · "Quiet".

Built for reading comfort, not decoration:
- One typeface: Atkinson Hyperlegible (designed by the Braille Institute for
  legibility). No display serif, no uppercase tracked labels.
- Soft off-white ground with near-black ink (~16:1). Secondary text ~8:1, never
  lighter. Emerald #064E3B is the single accent (~11:1 on the ground).
- Sidebar and main area share one polarity, so every widget reads the same.
- Streamlit's own widgets keep their own layout. This sheet only sets colour,
  font, radius and borders on them — every past breakage (blank labels, lost
  ticks, collapsed file names) came from restyling their internals.

NOTE: cached in sys.modules — edits need a full server restart, not a save.
"""

LIGHT = """
    --apex-bg: #F8F3E6;
    --apex-panel: #F0E8D4;
    --apex-surface: #FFFCF4;
    --apex-ink: #1B1F1C;
    --apex-ink2: #4D524C;
    --apex-line: #E2D9C3;
    --apex-line-strong: #B5AA90;
    --apex-accent: #064E3B;
    --apex-accent-hover: #0A6B52;
    --apex-accent-ink: #FFFCF4;
    --apex-accent-soft: #DDEBDF;
    --apex-warn: #9A3412;
    --apex-warn-soft: #F8E3D2;
    --apex-hard: #064E3B;
    --apex-head: #F0E8D4;
    --apex-knob-x: 0px;
"""

DARK = """
    --apex-bg: #0F1714;
    --apex-panel: #142019;
    --apex-surface: #18251F;
    --apex-ink: #F1EADB;
    --apex-ink2: #B8B2A3;
    --apex-line: #26342D;
    --apex-line-strong: #4A5A51;
    --apex-accent: #8ED2B4;
    --apex-accent-hover: #A8DEC6;
    --apex-accent-ink: #0D1A14;
    --apex-accent-soft: #1D3329;
    --apex-warn: #F2A27A;
    --apex-warn-soft: #3A2418;
    --apex-hard: #050A08;
    --apex-head: #1F2E27;
    --apex-knob-x: 28px;
"""

_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:ital,wght@0,400;0,700;1,400&family=DM+Serif+Display&display=swap');

:root {
__TOKENS__
    --apex-font: "Atkinson Hyperlegible", "Segoe UI", system-ui, sans-serif;
    /* names app.py still uses inline */
    --apex-text: var(--apex-ink);
    --apex-display: var(--apex-ink);
    --apex-dim: var(--apex-ink2);
    --apex-faint: var(--apex-ink2);
    --apex-accent-text: var(--apex-accent);
}

@keyframes apexPulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.35; } }
@keyframes apexGrow { from { transform: scaleX(0.03); } to { transform: scaleX(1); } }
@keyframes apexArc { from { stroke-dashoffset: 100; } to { stroke-dashoffset: var(--dash, 0); } }
@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after { animation-duration: 0.001ms !important; animation-iteration-count: 1 !important; transition-duration: 0.001ms !important; }
}

/* ══ ground + type ════════════════════════════════════════════════════════ */

html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background: var(--apex-bg) !important; color: var(--apex-ink) !important; font-family: var(--apex-font) !important;
}
.stApp .block-container, .stApp [data-testid="stMainBlockContainer"] {
    max-width: 1080px !important; padding: 24px 40px 56px !important;
}
.stApp p, .stApp li, .stApp label, .stApp input, .stApp textarea, .stApp button,
.stApp [data-testid="stMarkdownContainer"], .stApp [data-baseweb] {
    font-family: var(--apex-font) !important;
}
.stApp .stMarkdown p, .stApp .stMarkdown li { color: var(--apex-ink) !important; font-size: 16px; line-height: 1.6; }
.stApp [data-testid="stMarkdownContainer"] { margin-bottom: 0 !important; }
.stApp h1, .stApp h2, .stApp h3, .stApp h4 { font-family: var(--apex-font) !important; color: var(--apex-ink) !important; font-weight: 700 !important; letter-spacing: 0 !important; }
.stApp a { color: var(--apex-accent) !important; text-underline-offset: 3px; }
.stApp a:hover { color: var(--apex-accent-hover) !important; }
::selection { background: var(--apex-accent-soft); color: var(--apex-ink); }
.stApp hr { border: 0 !important; border-top: 1px solid var(--apex-line) !important; background: none !important; margin: 16px 0 !important; }
.stApp :focus-visible { outline: 2px solid var(--apex-accent) !important; outline-offset: 2px !important; box-shadow: none !important; }

/* icons are a ligature font — keep it wherever a glyph lives */
.stApp [data-testid="stIconMaterial"], .stApp [class*="material-symbols"] {
    font-family: "Material Symbols Rounded", "Material Symbols Outlined", sans-serif !important;
    font-weight: 400 !important; letter-spacing: normal !important; color: inherit;
}

/* ══ chrome Streamlit adds ════════════════════════════════════════════════ */

[data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stStatusWidget"], #MainMenu, footer { display: none !important; }
[data-testid="stHeader"] { background: transparent !important; height: 0 !important; min-height: 0 !important; pointer-events: none !important; }
[data-testid="stHeader"] * { pointer-events: auto; }
[data-testid="stSidebarHeader"], [data-testid="stLogoSpacer"],
[data-testid="stSidebarCollapseButton"], [data-testid="stSidebarCollapsedControl"] { display: none !important; }

/* ══ sidebar ══════════════════════════════════════════════════════════════ */

[data-testid="stSidebar"], [data-testid="stSidebarContent"] { background: var(--apex-panel) !important; border-right: 1px solid var(--apex-line) !important; }
[data-testid="stSidebar"] { transform: none !important; visibility: visible !important; }
@media (min-width: 1000px) {
    [data-testid="stSidebar"], [data-testid="stSidebar"] > div:first-child { width: 320px !important; min-width: 320px !important; max-width: 320px !important; }
}
.stApp [data-testid="stSidebarUserContent"] { padding: 22px 20px 24px !important; }
.stApp [data-testid="stSidebar"] [data-testid="stVerticalBlock"] { gap: 8px !important; }
.stApp [data-testid="stSidebar"] .stMarkdown p, .stApp [data-testid="stSidebar"] label { font-size: 14.5px !important; color: var(--apex-ink) !important; }

.apex-brand { font-size: 22px; font-weight: 700; color: var(--apex-ink); line-height: 1.2; }
.apex-brand-sub { font-size: 13.5px; color: var(--apex-ink2); padding-top: 2px; }
.apex-label { font-size: 13.5px; font-weight: 700; color: var(--apex-ink); padding-top: 14px; }
.apex-label.first { padding-top: 18px; }

.apex-gate { display: flex; flex-direction: column; gap: 4px; padding: 8px 0 4px; }
.apex-gate-item { display: flex; align-items: center; gap: 8px; font-size: 13.5px; color: var(--apex-ink2); }
.apex-gate-item.met { color: var(--apex-ink); }
.apex-note { font-size: 15px; line-height: 1.6; color: var(--apex-ink2); max-width: 66ch; }
[data-testid="stSidebar"] .apex-note { font-size: 13px; line-height: 1.5; }

/* ══ buttons ══════════════════════════════════════════════════════════════ */

.stApp .stButton > button, .stApp [data-testid="stDownloadButton"] button, .stApp [data-testid^="stBaseButton"] {
    font-family: var(--apex-font) !important; font-size: 14.5px !important; font-weight: 700 !important;
    border-radius: 8px !important; padding: 8px 16px !important; min-height: 38px !important; box-shadow: none !important;
    transition: background 0.12s ease, border-color 0.12s ease;
}
.stApp .stButton > button p, .stApp [data-testid="stDownloadButton"] button p, .stApp [data-testid^="stBaseButton"] p {
    font-size: 14.5px !important; font-weight: 700 !important; color: inherit !important; margin: 0 !important;
}
.stApp .stButton > button[kind="primary"], .stApp [data-testid="stBaseButton-primary"], .stApp [data-testid="stDownloadButton"] button {
    background: var(--apex-accent) !important; color: var(--apex-accent-ink) !important; border: 1px solid var(--apex-accent) !important;
}
.stApp .stButton > button[kind="primary"]:hover, .stApp [data-testid="stBaseButton-primary"]:hover, .stApp [data-testid="stDownloadButton"] button:hover {
    background: var(--apex-accent-hover) !important; border-color: var(--apex-accent-hover) !important; color: var(--apex-accent-ink) !important;
}
.stApp .stButton > button[kind="secondary"], .stApp [data-testid="stBaseButton-secondary"] {
    background: var(--apex-surface) !important; color: var(--apex-ink) !important; border: 1px solid var(--apex-line-strong) !important;
}
.stApp .stButton > button[kind="secondary"]:hover, .stApp [data-testid="stBaseButton-secondary"]:hover {
    border-color: var(--apex-accent) !important; color: var(--apex-ink) !important; background: var(--apex-surface) !important;
}
.stApp .stButton > button:active, .stApp [data-testid^="stBaseButton"]:active { transform: translateY(1px); }
.stApp .stButton > button:disabled, .stApp [data-testid^="stBaseButton"]:disabled {
    background: transparent !important; color: var(--apex-ink2) !important; border: 1px dashed var(--apex-line-strong) !important;
    opacity: 1 !important; cursor: not-allowed !important; transform: none !important;
}
.stApp .stButton > button:disabled p, .stApp [data-testid^="stBaseButton"]:disabled p { color: var(--apex-ink2) !important; }
.stApp .st-key-run_pipeline button { min-height: 44px !important; font-size: 15.5px !important; }
.stApp .st-key-run_pipeline button p { font-size: 15.5px !important; }
.stApp .st-key-jd_mode_paste button, .stApp .st-key-jd_mode_pdf button { min-height: 34px !important; padding: 5px 8px !important; }
.stApp .st-key-jd_mode_paste button p, .stApp .st-key-jd_mode_pdf button p { font-size: 13.5px !important; }

/* ══ inputs — colour and border only ══════════════════════════════════════ */

.stApp .stTextArea [data-baseweb="textarea"], .stApp .stTextInput [data-baseweb="input"] {
    background: var(--apex-surface) !important; border: 1px solid var(--apex-line-strong) !important; border-radius: 8px !important;
}
.stApp .stTextArea [data-baseweb="textarea"]:focus-within, .stApp .stTextInput [data-baseweb="input"]:focus-within { border-color: var(--apex-accent) !important; }
.stApp .stTextArea [data-baseweb="base-input"], .stApp .stTextInput [data-baseweb="base-input"] { background: transparent !important; }
.stApp .stTextArea textarea, .stApp .stTextInput input {
    background: transparent !important; color: var(--apex-ink) !important; border: 0 !important;
    font-size: 14.5px !important; line-height: 1.55 !important; caret-color: var(--apex-accent) !important;
}
.stApp .stTextArea textarea::placeholder { color: var(--apex-ink2) !important; opacity: 1 !important; }

.stApp [data-baseweb="select"] > div {
    background: var(--apex-surface) !important; border: 1px solid var(--apex-line-strong) !important; border-radius: 8px !important;
    color: var(--apex-ink) !important; font-size: 14.5px !important;
}
.stApp [data-baseweb="select"] * { color: var(--apex-ink) !important; }
.stApp [data-baseweb="select"] svg { fill: var(--apex-ink2) !important; }
[data-baseweb="popover"] ul, [data-baseweb="popover"] [data-baseweb="menu"] {
    background: var(--apex-surface) !important; border: 1px solid var(--apex-line-strong) !important; border-radius: 8px !important;
}
[data-baseweb="popover"] li { color: var(--apex-ink) !important; font-family: var(--apex-font) !important; font-size: 14.5px !important; }
[data-baseweb="popover"] li:hover, [data-baseweb="popover"] li[aria-selected="true"] { background: var(--apex-accent-soft) !important; }

.stApp [data-testid="stCheckbox"] label p { font-size: 14.5px !important; line-height: 1.45 !important; color: var(--apex-ink) !important; }

.stApp [data-testid="stFileUploaderDropzone"] {
    background: var(--apex-surface) !important; border: 1px dashed var(--apex-line-strong) !important; border-radius: 10px !important;
}
.stApp [data-testid="stFileUploaderDropzone"]:hover { border-color: var(--apex-accent) !important; }
.stApp [data-testid="stFileUploader"] span, .stApp [data-testid="stFileUploader"] small, .stApp [data-testid="stFileUploader"] div {
    color: var(--apex-ink);
}
.stApp [data-testid="stFileUploader"] small { color: var(--apex-ink2) !important; font-size: 12.5px !important; }
.stApp [data-testid="stFileUploader"] svg { fill: var(--apex-ink2); color: var(--apex-ink2); }
.stApp [data-testid="stFileUploaderFile"] { background: transparent !important; color: var(--apex-ink) !important; }
.stApp [data-testid="stFileUploaderFileName"] { color: var(--apex-ink) !important; font-size: 14px !important; }
.stApp [data-testid="stFileUploaderDeleteBtn"] button { background: transparent !important; border: 0 !important; color: var(--apex-ink2) !important; min-height: 0 !important; padding: 4px !important; }

/* tooltips */
[data-testid="stTooltipContent"], [role="tooltip"] { background: var(--apex-ink) !important; color: var(--apex-bg) !important; border-radius: 6px !important; font-family: var(--apex-font) !important; font-size: 13px !important; }
[data-testid="stTooltipContent"] * { color: var(--apex-bg) !important; }

/* ══ theme switch: 60x32 track, knob slides on --apex-knob-x ══════════════ */

.stApp .st-key-theme_toggle button[kind],
.stApp [data-testid="stElementContainer"]:has(#apex-theme-marker) + [data-testid="stElementContainer"] button[kind] {
    position: relative !important; display: block !important;
    width: 60px !important; min-width: 60px !important; max-width: 60px !important;
    height: 32px !important; min-height: 32px !important; padding: 0 !important; margin-left: auto !important;
    border-radius: 999px !important; border: 1px solid var(--apex-line-strong) !important; background: var(--apex-surface) !important;
}
.stApp .st-key-theme_toggle button[kind]:hover,
.stApp [data-testid="stElementContainer"]:has(#apex-theme-marker) + [data-testid="stElementContainer"] button[kind]:hover { border-color: var(--apex-accent) !important; }
.stApp .st-key-theme_toggle button[kind] [data-testid="stMarkdownContainer"],
.stApp [data-testid="stElementContainer"]:has(#apex-theme-marker) + [data-testid="stElementContainer"] button[kind] [data-testid="stMarkdownContainer"] {
    position: absolute !important; top: 4px !important; left: 4px !important; width: 22px !important; height: 22px !important;
    border-radius: 50% !important; background: var(--apex-ink) !important;
    display: flex !important; align-items: center !important; justify-content: center !important;
    transform: translateX(var(--apex-knob-x)) !important; transition: transform 200ms ease !important; pointer-events: none !important;
}
.stApp .st-key-theme_toggle button[kind] p, .stApp .st-key-theme_toggle button[kind] *,
.stApp [data-testid="stElementContainer"]:has(#apex-theme-marker) + [data-testid="stElementContainer"] button[kind] p {
    margin: 0 !important; line-height: 1 !important; font-size: 12px !important; color: var(--apex-bg) !important;
    font-family: "Segoe UI Symbol", "Apple Symbols", sans-serif !important;
}
#apex-theme-marker { display: block; height: 0; }

/* ══ tabs, expanders, alerts ══════════════════════════════════════════════ */

.stApp [data-baseweb="tab-list"] { gap: 28px !important; background: transparent !important; border-bottom: 1px solid var(--apex-line) !important; }
.stApp [data-baseweb="tab"] { background: transparent !important; padding: 10px 0 !important; height: auto !important; border-bottom: 2px solid transparent !important; margin-bottom: -1px !important; }
.stApp [data-baseweb="tab"] p { font-size: 15px !important; font-weight: 700 !important; color: var(--apex-ink2) !important; }
.stApp [data-baseweb="tab"]:hover p { color: var(--apex-ink) !important; }
.stApp [data-baseweb="tab"][aria-selected="true"] { border-bottom-color: var(--apex-accent) !important; }
.stApp [data-baseweb="tab"][aria-selected="true"] p { color: var(--apex-ink) !important; }
.stApp [data-baseweb="tab-highlight"], .stApp [data-baseweb="tab-border"] { display: none !important; }
.stApp [data-baseweb="tab-panel"] { padding-top: 24px !important; }

.stApp [data-testid="stExpander"] details { background: var(--apex-surface) !important; border: 1px solid var(--apex-line) !important; border-radius: 10px !important; }
.stApp [data-testid="stExpander"] summary { padding: 11px 14px !important; }
.stApp [data-testid="stExpander"] summary p { font-size: 15px !important; font-weight: 700 !important; color: var(--apex-ink) !important; }
.stApp [data-testid="stExpander"] summary:hover p { color: var(--apex-accent) !important; }
.stApp [data-testid="stExpander"] summary svg { fill: var(--apex-ink2) !important; color: var(--apex-ink2) !important; }

.stApp [data-testid="stAlert"] { background: var(--apex-surface) !important; border: 1px solid var(--apex-line-strong) !important; border-radius: 10px !important; }
.stApp [data-testid="stAlert"] p { color: var(--apex-ink) !important; font-size: 15px !important; }
.stApp [data-testid="stSpinner"] p { color: var(--apex-ink) !important; }
.stApp pre, .stApp code { background: var(--apex-surface) !important; color: var(--apex-ink) !important; border-radius: 8px !important; font-size: 13px !important; }

/* ══════════════════════════════════════════════════════════════════════════
   APEX content
   ══════════════════════════════════════════════════════════════════════════ */

.apex-navline { font-size: 13.5px; color: var(--apex-ink2); padding-top: 8px; }
.apex-kicker { font-size: 13.5px; color: var(--apex-ink2); }
.apex-h { font-size: 17px; font-weight: 700; color: var(--apex-ink); margin: 0; line-height: 1.3; }
.apex-h-lg { font-size: 26px; font-weight: 700; color: var(--apex-ink); margin: 0; line-height: 1.2; }
.apex-h-lg em { font-style: normal; font-weight: 400; color: var(--apex-ink2); }
.apex-prose { font-size: 16px; line-height: 1.65; color: var(--apex-ink); max-width: 70ch; }
.apex-rule { height: 0; border-top: 1px solid var(--apex-line); margin: 24px 0; }
.apex-row { display: flex; justify-content: space-between; align-items: baseline; gap: 16px; flex-wrap: wrap; }
.apex-section { display: flex; flex-direction: column; gap: 10px; }

/* — idle — */
.apex-intro { display: flex; flex-direction: column; gap: 28px; padding-top: 28px; }
.apex-title { font-size: 34px; font-weight: 700; line-height: 1.15; color: var(--apex-ink); max-width: 24ch; margin: 0; }
.apex-lede { font-size: 17px; line-height: 1.6; color: var(--apex-ink2); max-width: 62ch; margin-top: 10px; }
.apex-steps { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 24px; }
@media (max-width: 900px) { .apex-steps { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
.apex-step { border-top: 2px solid var(--apex-line); padding-top: 12px; display: flex; flex-direction: column; gap: 4px; }
.apex-step.loop { border-top-color: var(--apex-accent); }
.apex-step-num { font-size: 13px; font-weight: 700; color: var(--apex-accent); }
.apex-step-title { font-size: 16px; font-weight: 700; color: var(--apex-ink); }
.apex-step-body { font-size: 14.5px; line-height: 1.5; color: var(--apex-ink2); }
.apex-route { background: var(--apex-surface); border: 1px solid var(--apex-line); border-radius: 10px; padding: 14px 18px; font-size: 14.5px; line-height: 1.6; color: var(--apex-ink2); }
.apex-route b { color: var(--apex-ink); }
.apex-route code { background: transparent !important; border: 0 !important; padding: 0 !important; font-size: 13.5px !important; color: var(--apex-ink) !important; }

/* — trace — */
.apex-seg { display: grid; grid-template-columns: repeat(6, 1fr); gap: 4px; margin: 16px 0 8px; }
.apex-seg > div { height: 6px; border-radius: 3px; background: var(--apex-line); }
.apex-seg > div.done { background: var(--apex-accent); }
.apex-seg > div.now { background: var(--apex-accent); animation: apexPulse 1.2s ease-in-out infinite; }
.apex-seg > div.now > i { display: none; }
.apex-log-line { display: grid; grid-template-columns: 22px 130px minmax(0, 1fr); gap: 10px; align-items: center; padding: 10px 0; border-bottom: 1px solid var(--apex-line); font-size: 15px; color: var(--apex-ink); }
.apex-log-node { font-size: 14px; color: var(--apex-ink2); }
.apex-log-line.now { font-weight: 700; }
.apex-log-line.now .apex-log-node { color: var(--apex-accent); }
.apex-log-line.queued, .apex-log-line.queued .apex-log-node { color: var(--apex-ink2); }
@media (max-width: 620px) { .apex-log-line { grid-template-columns: 22px 1fr; } .apex-log-line .apex-log-node { display: none; } }

/* — score — */
.apex-score { display: grid; grid-template-columns: 150px minmax(0, 1fr); gap: 36px; align-items: center; }
@media (max-width: 800px) { .apex-score { grid-template-columns: 1fr; } }
.apex-gauge { position: relative; width: 140px; height: 140px; }
.apex-gauge svg { display: block; }
.apex-gauge-mid { position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; }
.apex-gauge-num { font-size: 40px; font-weight: 700; line-height: 1; color: var(--apex-ink); font-variant-numeric: tabular-nums; }
.apex-gauge-lbl { font-size: 12.5px; color: var(--apex-ink2); padding-top: 4px; }
.apex-gauge-foot { font-size: 13.5px; color: var(--apex-accent); padding-top: 8px; font-weight: 700; }
.apex-metrics { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 28px; }
@media (max-width: 700px) { .apex-metrics { grid-template-columns: 1fr; gap: 16px; } }
.apex-metrics > div { display: flex; flex-direction: column; gap: 6px; }
.apex-metric-label { font-size: 13.5px; color: var(--apex-ink2); }
.apex-figure { font-size: 30px; font-weight: 700; line-height: 1; color: var(--apex-ink); font-variant-numeric: tabular-nums; }
.apex-figure sup { font-size: 0.6em; vertical-align: baseline; font-weight: 400; color: var(--apex-ink2); }
.apex-figure-quiet { color: var(--apex-warn); }
.apex-bar { height: 4px; border-radius: 2px; background: var(--apex-line); overflow: hidden; }
.apex-bar > div { height: 100%; background: var(--apex-accent); transform-origin: left; animation: apexGrow 0.9s ease-out 0.2s both; }
.apex-bar-quiet > div { background: var(--apex-warn); }
.apex-metric-foot { font-size: 13px; color: var(--apex-ink2); }

/* — findings, tags, skills — */
.apex-two { display: grid; grid-template-columns: 1fr 1fr; gap: 32px; }
@media (max-width: 800px) { .apex-two { grid-template-columns: 1fr; gap: 20px; } }
.apex-finding { position: relative; padding-left: 18px; font-size: 15px; line-height: 1.55; color: var(--apex-ink); margin-bottom: 8px; }
.apex-finding::before { content: ""; position: absolute; left: 2px; top: 0.6em; width: 6px; height: 6px; border-radius: 50%; background: var(--apex-accent); }
.apex-finding-quiet::before { background: var(--apex-warn); }

.apex-tags { display: flex; flex-wrap: wrap; gap: 6px; }
.apex-tag { display: inline-flex; align-items: center; font-size: 13.5px; line-height: 1.3; padding: 3px 9px; border-radius: 6px; background: var(--apex-accent-soft); color: var(--apex-accent); }
.apex-tag-absent { background: var(--apex-warn-soft); color: var(--apex-warn); }
.apex-tag-neutral { background: transparent; color: var(--apex-ink2); box-shadow: inset 0 0 0 1px var(--apex-line-strong); }

.apex-skillset { display: grid; grid-template-columns: 200px minmax(0, 1fr); gap: 6px 20px; font-size: 14.5px; line-height: 1.55; }
@media (max-width: 700px) { .apex-skillset { grid-template-columns: 1fr; } }
.apex-skillset dt { color: var(--apex-ink2); margin: 0; }
.apex-skillset dd { color: var(--apex-ink); margin: 0 0 6px; }

/* — tables — */
.apex-table { width: 100%; border-collapse: collapse; font-size: 14.5px; }
.apex-table th { text-align: left; font-size: 13px; font-weight: 700; color: var(--apex-ink2); padding: 0 12px 8px 0; border-bottom: 1px solid var(--apex-line-strong); }
.apex-table td { padding: 10px 12px 10px 0; border-bottom: 1px solid var(--apex-line); color: var(--apex-ink); vertical-align: top; line-height: 1.5; }
.apex-table td.quiet { color: var(--apex-ink2); }
.apex-table td.gold { color: var(--apex-accent); font-weight: 700; }
.apex-table td.right, .apex-table th.right { text-align: right; padding-right: 0; }
@media (max-width: 640px) {
    .apex-table, .apex-table tbody, .apex-table tr, .apex-table td { display: block; width: 100%; }
    .apex-table thead { display: none; }
    .apex-table tr { border-bottom: 1px solid var(--apex-line); padding: 8px 0; }
    .apex-table td { border-bottom: 0; padding: 2px 0; text-align: left !important; }
}

/* — critique & rewrite — */
.apex-quote { font-size: 17px; line-height: 1.6; font-style: italic; color: var(--apex-ink); max-width: 70ch; border-left: 3px solid var(--apex-accent); padding-left: 14px; margin: 16px 0 24px; }
.apex-numlist { display: flex; flex-direction: column; gap: 8px; }
.apex-numitem { display: grid; grid-template-columns: 24px minmax(0, 1fr); font-size: 15px; line-height: 1.55; color: var(--apex-ink); }
.apex-numitem span:first-child { font-weight: 700; color: var(--apex-accent); }
.apex-diff-pair { display: grid; grid-template-columns: 1fr 1fr; gap: 28px; padding: 14px 0; border-top: 1px solid var(--apex-line); }
@media (max-width: 800px) { .apex-diff-pair { grid-template-columns: 1fr; gap: 8px; } }
.apex-diff-label { font-size: 13px; font-weight: 700; color: var(--apex-ink2); padding-bottom: 4px; }
.apex-diff-label.after { color: var(--apex-accent); }
.apex-before { font-size: 15px; line-height: 1.55; color: var(--apex-ink2); }
.apex-after { font-size: 15px; line-height: 1.55; color: var(--apex-ink); }

/* — the letter — */
.apex-plate { max-width: 720px; background: var(--apex-surface); border: 1px solid var(--apex-line); border-radius: 10px; padding: 40px 48px; }
@media (max-width: 640px) { .apex-plate { padding: 24px 20px; } }
.stApp .apex-plate, .stApp .apex-plate p { color: var(--apex-ink) !important; }
.stApp .apex-plate .muted { color: var(--apex-ink2) !important; }
.apex-plate-subject { font-size: 19px; font-weight: 700; line-height: 1.3; padding-bottom: 14px; }
.stApp .apex-plate p { margin: 0 0 12px; font-size: 16px; line-height: 1.7; }
.stApp .apex-plate p:last-child { margin-bottom: 0; }

/* ══════════════════════════════════════════════════════════════════════════
   Retro heat — serif headings, double rules, small hard offset shadows.
   Decoration only; every text colour above is unchanged.
   ══════════════════════════════════════════════════════════════════════════ */

:root { --apex-serif: "DM Serif Display", Georgia, serif; }
.apex-brand { font-family: var(--apex-serif); font-weight: 400; font-size: 30px; line-height: 1; }
.apex-brand-sub { padding-top: 6px; padding-bottom: 10px; border-bottom: 3px double var(--apex-line-strong); }
.apex-title, .apex-h-lg, .apex-gauge-num, .apex-figure { font-family: var(--apex-serif); font-weight: 400; }
.apex-title { font-size: 40px; line-height: 1.1; }
.apex-h-lg { font-size: 30px; }
.apex-h-lg em { font-style: italic; font-family: var(--apex-serif); }
.apex-gauge-num { font-size: 44px; }
.apex-figure { font-size: 34px; }
.apex-step { border-top: 4px double var(--apex-line-strong); padding-top: 14px; }
.apex-step.loop { border-top-color: var(--apex-accent); }
.apex-tag { border-radius: 999px; padding: 3px 11px; }

/* primary actions: ink outline with a hard 3px offset; pressing collapses it */
.stApp .stButton > button[kind="primary"], .stApp [data-testid="stBaseButton-primary"], .stApp [data-testid="stDownloadButton"] button {
    border: 2px solid var(--apex-hard) !important; box-shadow: 3px 3px 0 var(--apex-hard) !important;
}
.stApp .stButton > button[kind="primary"]:active, .stApp [data-testid="stBaseButton-primary"]:active, .stApp [data-testid="stDownloadButton"] button:active {
    transform: translate(2px, 2px) !important; box-shadow: 1px 1px 0 var(--apex-hard) !important;
}
.stApp .stButton > button:disabled, .stApp [data-testid^="stBaseButton"]:disabled { box-shadow: none !important; }
.stApp .st-key-jd_mode_paste button, .stApp .st-key-jd_mode_pdf button { box-shadow: none !important; }
.stApp .st-key-jd_mode_paste button:active, .stApp .st-key-jd_mode_pdf button:active { transform: none !important; }

/* cards: route, letter, expanders, tables */
.apex-route, .apex-plate { border: 1.5px solid var(--apex-line-strong); box-shadow: 4px 4px 0 var(--apex-line); }
.stApp [data-testid="stExpander"] details { border: 1.5px solid var(--apex-line-strong) !important; }
.apex-quote { border-left: 4px double var(--apex-accent); padding-left: 16px; }
.apex-plate-subject { font-family: var(--apex-serif); font-weight: 400; font-size: 22px; border-bottom: 3px double var(--apex-line); margin-bottom: 16px; }

/* — tables: one boxed card. Streamlit's own markdown-table rules (cell borders,
     light row fills that vanished in dark mode) are reset first. — */
.stApp .apex-table, .stApp .apex-table th, .stApp .apex-table td, .stApp .apex-table tr {
    border: 0 !important; background: transparent !important;
}
.stApp .apex-table {
    display: table !important; width: 100% !important; margin: 12px 0 4px !important;
    border-collapse: separate !important; border-spacing: 0 !important;
    border: 1.5px solid var(--apex-line-strong) !important; border-radius: 10px !important; overflow: hidden;
    background: var(--apex-surface) !important; box-shadow: 4px 4px 0 var(--apex-line);
}
.stApp .apex-table th {
    background: var(--apex-head) !important; color: var(--apex-ink) !important;
    font-size: 13px !important; font-weight: 700 !important; text-align: left;
    padding: 11px 16px !important; border-bottom: 1.5px solid var(--apex-line-strong) !important;
}
.stApp .apex-table td {
    color: var(--apex-ink) !important; padding: 12px 16px !important; line-height: 1.55 !important;
    border-bottom: 1px solid var(--apex-line) !important; vertical-align: top;
}
.stApp .apex-table tbody tr:last-child td { border-bottom: 0 !important; }
.stApp .apex-table td.quiet { color: var(--apex-ink2) !important; }
.stApp .apex-table td.gold { color: var(--apex-accent) !important; font-weight: 700; }
.stApp .apex-table td.right, .stApp .apex-table th.right { text-align: right; }
@media (max-width: 640px) {
    .stApp .apex-table, .stApp .apex-table tbody, .stApp .apex-table tr, .stApp .apex-table td { display: block !important; }
    .stApp .apex-table td { padding: 4px 14px !important; border-bottom: 0 !important; }
    .stApp .apex-table tr { border-bottom: 1px solid var(--apex-line) !important; padding: 8px 0; }
}

/* — uploaded file: Streamlit paints the chip from the LIGHT config theme, so in
     dark mode it was a pale card with pale text. Strip every inner fill, then
     draw one outlined row in the current theme. — */
.stApp [data-testid="stFileUploader"] section div, .stApp [data-testid="stFileUploader"] li,
.stApp [data-testid="stFileUploader"] ul { background: transparent !important; background-color: transparent !important; }
.stApp [data-testid="stFileUploaderFile"] {
    border: 1.5px solid var(--apex-line-strong) !important; border-radius: 8px !important; background: var(--apex-surface) !important;
}
.stApp [data-testid="stFileUploader"] [data-testid="stFileUploaderFile"] *,
.stApp [data-testid="stFileUploader"] section * { color: var(--apex-ink) !important; }
.stApp [data-testid="stFileUploader"] small { color: var(--apex-ink2) !important; }
.stApp [data-testid="stFileUploader"] svg { fill: var(--apex-ink2) !important; color: var(--apex-ink2) !important; }
.stApp [data-testid="stFileUploader"] button[kind] { background: var(--apex-surface) !important; color: var(--apex-ink) !important; border: 1px solid var(--apex-line-strong) !important; box-shadow: none !important; }
.stApp [data-testid="stFileUploaderDeleteBtn"] button { border: 0 !important; background: transparent !important; }

/* ── dark-mode fixes: Streamlit paints textarea / select / menus from the LIGHT
     config theme, so every inner layer is repainted from the current tokens ── */
.stApp .stTextArea [data-baseweb="textarea"], .stApp .stTextArea [data-baseweb="textarea"] > div,
.stApp .stTextArea [data-baseweb="base-input"], .stApp .stTextArea textarea,
.stApp .stTextInput [data-baseweb="input"], .stApp .stTextInput [data-baseweb="input"] > div, .stApp .stTextInput input {
    background: var(--apex-surface) !important; background-color: var(--apex-surface) !important;
    color: var(--apex-ink) !important; -webkit-text-fill-color: var(--apex-ink) !important;
}
.stApp .stTextArea textarea::placeholder, .stApp .stTextInput input::placeholder {
    color: var(--apex-ink2) !important; -webkit-text-fill-color: var(--apex-ink2) !important;
}
.stApp [data-baseweb="select"] > div, .stApp [data-baseweb="select"] > div > div { background: var(--apex-surface) !important; background-color: var(--apex-surface) !important; }
.stApp [data-baseweb="select"] div, .stApp [data-baseweb="select"] input { color: var(--apex-ink) !important; -webkit-text-fill-color: var(--apex-ink) !important; }
[data-baseweb="popover"], [data-baseweb="popover"] > div, [data-baseweb="popover"] ul, [data-baseweb="popover"] li {
    background: var(--apex-surface) !important; background-color: var(--apex-surface) !important;
}
[data-baseweb="popover"] li, [data-baseweb="popover"] li * { color: var(--apex-ink) !important; }
[data-baseweb="popover"] li:hover, [data-baseweb="popover"] li[aria-selected="true"] { background: var(--apex-accent-soft) !important; }

/* long option names (German in brackets): wrap instead of clipping */
[data-baseweb="popover"] li, [data-baseweb="popover"] li * { white-space: normal !important; overflow: visible !important; text-overflow: clip !important; line-height: 1.4 !important; }
[data-baseweb="popover"] li { height: auto !important; min-height: 40px; padding-top: 8px !important; padding-bottom: 8px !important; }
.stApp [data-baseweb="select"] > div { height: auto !important; min-height: 42px; }
.stApp [data-baseweb="select"] [title], .stApp [data-baseweb="select"] > div > div:first-child,
.stApp [data-baseweb="select"] > div > div:first-child * {
    white-space: normal !important; overflow: visible !important; text-overflow: clip !important; line-height: 1.35 !important;
}

/* expander header: Streamlit fills it from the LIGHT config theme — repaint from tokens */
.stApp [data-testid="stExpander"] details, .stApp [data-testid="stExpander"] details > div,
.stApp [data-testid="stExpander"] summary, .stApp [data-testid="stExpander"] summary:hover,
.stApp [data-testid="stExpander"] details[open] > summary, .stApp [data-testid="stExpanderDetails"] {
    background: var(--apex-surface) !important; background-color: var(--apex-surface) !important;
}
.stApp [data-testid="stExpander"] summary, .stApp [data-testid="stExpander"] summary * { color: var(--apex-ink) !important; }
.stApp [data-testid="stExpander"] summary:hover p { color: var(--apex-accent) !important; }
.stApp [data-testid="stExpander"] summary svg { fill: var(--apex-ink2) !important; color: var(--apex-ink2) !important; }

/* section headings that sit above tables/lists get breathing room */
.apex-section { gap: 12px; }
.stApp .apex-h { padding-bottom: 2px; }
</style>
"""


def apex_css(theme: str = "light") -> str:
    return _CSS.replace("__TOKENS__", DARK if theme == "dark" else LIGHT)


def apply_styles(theme: str = "light") -> None:
    import streamlit as st
    st.markdown(apex_css(theme), unsafe_allow_html=True)


_PATHS = {
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "arrow-right": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
    "circle": '<circle cx="12" cy="12" r="9"/>',
    "download": '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="m7 10 5 5 5-5"/><path d="M12 15V3"/>',
}


def icon(name: str, size: int = 15, stroke: str = "currentColor", width: float = 2.0) -> str:
    return (
        f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
        f'stroke="{stroke}" stroke-width="{width}" stroke-linecap="round" '
        f'stroke-linejoin="round" aria-hidden="true">{_PATHS.get(name, "")}</svg>'
    )


def gauge(score: int, label: str = "ATS score", foot: str = "") -> str:
    """A thin accent ring with the number inside; foot line sits underneath."""
    score = max(0, min(100, int(score)))
    return (
        "<div>"
        '<div class="apex-gauge">'
        '<svg width="140" height="140" viewBox="0 0 140 140">'
        '<circle cx="70" cy="70" r="60" fill="none" stroke="var(--apex-line)" stroke-width="8"></circle>'
        '<circle cx="70" cy="70" r="60" pathLength="100" fill="none" stroke="var(--apex-accent)" stroke-width="8" '
        'stroke-linecap="round" stroke-dasharray="100 100" transform="rotate(-90 70 70)" '
        f'style="--dash:{100 - score}; stroke-dashoffset:{100 - score}; animation:apexArc 1.1s ease-out both;"></circle>'
        "</svg>"
        '<div class="apex-gauge-mid">'
        f'<div class="apex-gauge-num">{score}</div>'
        f'<div class="apex-gauge-lbl">{label}</div>'
        "</div></div>"
        + (f'<div class="apex-gauge-foot">{foot}</div>' if foot else "")
        + "</div>"
    )
