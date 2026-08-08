"""
APEX — UI Styles
Source Serif 4 throughout, on a green ground. Light runs mint paper with olive
ink and forest pills; dark inverts to an olive ground with mint ink and celadon
pills. Moss (light) / celadon (dark) is the single interactive ink.

Source Serif 4 replaces the earlier Cormorant/Lora pairing deliberately:
Cormorant is a hairline display face and is unreadable at interface sizes.
Source Serif 4 is a screen-text serif — sturdy stems, large x-height.

Two token blocks, one per ground. Each defines its OWN dimmed and accent-text
values; a single ramp step cannot serve both grounds at 4.5:1. Light accent is
#3f6522 rather than a lighter moss because anything lighter fails on the panel.

NOTE: cached in sys.modules — edits need a full server restart, not a save.
"""

LIGHT = """
    --apex-bg: #cfe7d8;                /* mint — the ground */
    --apex-panel: #e2f1e8;
    --apex-tint: rgba(63, 101, 34, 0.10);
    --apex-track: rgba(42, 69, 39, 0.18);
    --apex-divider: rgba(42, 69, 39, 0.16);

    --apex-text: #2a4527;              /* olive — 7.3:1 on mint */
    --apex-display: #1d3a26;           /* forest */
    --apex-dim: #3a5a36;               /* 5.9:1 */
    --apex-faint: #6f8f6a;             /* strokes and chrome only */
    --apex-em: #3f6522;

    --apex-accent: #3f6522;            /* moss — 5.2:1 on mint, 5.8:1 on panel */
    --apex-accent-text: #3f6522;
    --apex-accent-soft: rgba(63, 101, 34, 0.14);
    --apex-link: #3f6522;
    --apex-link-hover: #1d3a26;

    --apex-cta-bg: #1d3a26;            /* forest fill */
    --apex-cta-fg: #ddf0e4;            /* mint label — 10.5:1 on the fill */
    --apex-cta-bg-hover: #2a5334;
    --apex-shadow-sm: 0 1px 2px rgba(21, 48, 28, 0.16);
    --apex-shadow-lg: 0 12px 30px rgba(21, 48, 28, 0.20);
    --apex-glow-a: rgba(63, 101, 34, 0.10);
    --apex-glow-b: rgba(168, 206, 139, 0.16);
"""

DARK = """
    --apex-bg: #0d1710;                /* deep olive — reads almost black */
    --apex-panel: #142117;
    --apex-tint: rgba(168, 206, 139, 0.12);
    --apex-track: rgba(216, 239, 224, 0.18);
    --apex-divider: rgba(216, 239, 224, 0.16);

    --apex-text: #d8efe0;              /* mint — 7.5:1 on olive */
    --apex-display: #eaf7ef;
    --apex-dim: #aecfb9;               /* dimmed, never washed out */
    --apex-faint: #85a78f;
    --apex-em: #a8ce8b;

    --apex-accent: #a8ce8b;            /* celadon — 6.5:1 on olive */
    --apex-accent-text: #a8ce8b;
    --apex-accent-soft: rgba(168, 206, 139, 0.16);
    --apex-link: #a8ce8b;
    --apex-link-hover: #cfe6b8;

    --apex-cta-bg: #a8ce8b;            /* celadon fill */
    --apex-cta-fg: #163020;            /* forest label — 8.0:1 on the fill */
    --apex-cta-bg-hover: #bfdda4;
    --apex-shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.34);
    --apex-shadow-lg: 0 12px 30px rgba(0, 0, 0, 0.42);
    --apex-glow-a: rgba(168, 206, 139, 0.13);
    --apex-glow-b: rgba(111, 154, 46, 0.12);
"""

_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;0,8..60,700;1,8..60,400&display=swap');

:root {
__TOKENS__
    --apex-font: "Source Serif 4", Georgia, serif;

    --apex-space-1: 5px;  --apex-space-2: 10px; --apex-space-3: 15px;
    --apex-space-4: 20px; --apex-space-6: 30px; --apex-space-8: 40px;
    --apex-radius-sm: 4px; --apex-radius-md: 12px; --apex-radius-lg: 18px;
    --apex-radius-pill: 999px;
}

/* ══ motion ═══════════════════════════════════════════════════════════════ */

@keyframes apexRise { from { opacity: 0; transform: translateY(18px); } to { opacity: 1; transform: translateY(0); } }
@keyframes apexArc  { from { stroke-dashoffset: 100; } to { stroke-dashoffset: var(--dash, 0); } }
@keyframes apexDraw { from { transform: scaleX(0); } to { transform: scaleX(1); } }
@keyframes apexPulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.28; } }
@keyframes apexSheen { from { background-position: 200% 0; } to { background-position: -200% 0; } }
@keyframes apexGrow { from { transform: scaleX(0.04); } to { transform: scaleX(1); } }
@keyframes apexDrift {
    0%   { transform: translate3d(-3%, 2%, 0) scale(1.04); }
    50%  { transform: translate3d(4%, -2%, 0) scale(1.1); }
    100% { transform: translate3d(-3%, 2%, 0) scale(1.04); }
}
@keyframes apexFadeIn { from { opacity: 0; } to { opacity: 1; } }

@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: 0.001ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.001ms !important;
    }
}

/* ══ ground ═══════════════════════════════════════════════════════════════ */

html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background: var(--apex-bg) !important;
    color: var(--apex-text) !important;
    font-family: var(--apex-font) !important;
}
[data-testid="stAppViewContainer"] { animation: apexFadeIn 0.26s ease-out both; }

.block-container {
    max-width: 1240px !important;
    padding-top: var(--apex-space-4) !important;
    padding-bottom: var(--apex-space-8) !important;
}

header[data-testid="stHeader"] { background: transparent !important; height: auto !important; }
[data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stStatusWidget"],
#MainMenu, footer { display: none !important; }

/* ══ type — one serif does everything ═════════════════════════════════════ */

h1, h2, h3, h4, h5, h6, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {
    font-family: var(--apex-font) !important;
    font-weight: 600 !important;
    color: var(--apex-display) !important;
    line-height: 1.14 !important;
    letter-spacing: -0.015em !important;
}
h1 { font-size: 42px !important; }
h2 { font-size: 32px !important; }
h3 { font-size: 25px !important; }
h4 { font-size: 21px !important; }

.stMarkdown, .stMarkdown p, .stMarkdown li, [data-testid="stMarkdownContainer"],
[data-testid="stText"], .stTextInput label, .stTextArea label {
    font-family: var(--apex-font) !important;
    color: var(--apex-text) !important;
    font-size: 17px;
    line-height: 1.6;
}
[data-testid="stCaptionContainer"], .stCaption, small { color: var(--apex-dim) !important; }

a, .stMarkdown a { color: var(--apex-link) !important; text-underline-offset: 3px; }
a:hover, .stMarkdown a:hover { color: var(--apex-link-hover) !important; }

hr { border: 0 !important; height: 1px !important; background: var(--apex-divider) !important; margin: var(--apex-space-4) 0 !important; }
::selection { background: var(--apex-accent-soft); }

:focus { outline: none; }
:focus-visible, button:focus-visible, [data-baseweb="tab"]:focus-visible,
[data-testid="stFileUploaderDropzone"]:focus-visible, summary:focus-visible,
input:focus-visible, textarea:focus-visible {
    outline: 2px solid var(--apex-accent) !important;
    outline-offset: 2px !important;
    box-shadow: none !important;
}

/* ══ sidebar ══════════════════════════════════════════════════════════════ */

[data-testid="stSidebar"], [data-testid="stSidebarContent"] {
    background: var(--apex-panel) !important;
    border-right: 1px solid var(--apex-divider) !important;
}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
[data-testid="stSidebar"] label, [data-testid="stSidebar"] span {
    font-size: 15px; color: var(--apex-text) !important;
}

/* The rail is a fixed width, so its contents must be measured against it:
   every descendant borders its box and nothing is allowed to exceed the rail.
   Without this the controls keep their natural width and clip at the edge. */
[data-testid="stSidebar"] * { box-sizing: border-box !important; }
[data-testid="stSidebar"] [data-testid="stSidebarUserContent"],
[data-testid="stSidebar"] [data-testid="stVerticalBlock"],
[data-testid="stSidebar"] [data-testid="stElementContainer"],
[data-testid="stSidebar"] [data-testid="stHorizontalBlock"],
[data-testid="stSidebar"] [data-baseweb="select"],
[data-testid="stSidebar"] [data-testid="stFileUploader"],
[data-testid="stSidebar"] .stTextArea, [data-testid="stSidebar"] .stButton,
[data-testid="stSidebar"] .stButton > button {
    max-width: 100% !important; min-width: 0 !important;
}
[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] {
    padding: 22px 20px 30px !important;
}
[data-testid="stSidebar"] .apex-kicker { font-size: 12px !important; letter-spacing: 0.14em; }
[data-testid="stSidebar"] .stButton > button,
[data-testid="stSidebar"] [data-testid^="stBaseButton"] {
    font-size: 15px !important; padding: 10px 20px !important;
}
[data-testid="stSidebar"] .stButton > button * ,
[data-testid="stSidebar"] [data-testid^="stBaseButton"] * { font-size: 15px !important; }
/* the uploader is the widest thing in the rail — let it wrap instead of clip */
[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] {
    flex-direction: column !important;
    align-items: flex-start !important;
    gap: 10px !important;
    padding: 16px !important;
}
[data-testid="stSidebar"] [data-testid="stFileUploaderDropzoneInstructions"] {
    font-size: 13px !important; line-height: 1.5 !important;
}
[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] small,
[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] span {
    font-size: 13px !important; white-space: normal !important;
}
[data-testid="stSidebar"] [data-baseweb="select"] > div {
    font-size: 15px !important; white-space: normal !important;
}
[data-testid="stSidebar"] [data-baseweb="select"] div[title] {
    white-space: nowrap !important; overflow: hidden !important;
    text-overflow: ellipsis !important; font-size: 15px !important;
}
[data-testid="stSidebar"] .stTextArea textarea { font-size: 15px !important; }
[data-testid="stSidebar"] [data-testid="stCheckbox"] label {
    align-items: flex-start !important;
}
[data-testid="stSidebar"] [data-testid="stCheckbox"] label > div:last-child,
[data-testid="stSidebar"] [data-testid="stCheckbox"] label span {
    white-space: normal !important; line-height: 1.5 !important;
}
[data-testid="stSidebar"] .apex-gate-item, [data-testid="stSidebar"] .apex-note {
    font-size: 14px !important; white-space: normal !important;
}
@media (min-width: 1100px) {
    [data-testid="stSidebar"], [data-testid="stSidebar"] > div:first-child {
        width: 340px !important; min-width: 340px !important; max-width: 340px !important;
    }
}

/* ══ buttons ══════════════════════════════════════════════════════════════
   Streamlit renames its button testids between versions, so every rule here
   matches on THREE selectors at once (class, kind attr, stBaseButton-* testid).
   Relying on kind="secondary" alone is what previously left the theme toggle
   unstyled and painted a black pill with a black label.                      */

.stButton > button,
[data-testid="stDownloadButton"] button,
[data-testid^="stBaseButton"] {
    font-family: var(--apex-font) !important;
    font-weight: 600 !important;
    font-size: 17px !important;
    line-height: 1.2 !important;
    border-radius: var(--apex-radius-lg) !important;
    padding: 11px 26px !important;
    box-shadow: none !important;
    white-space: nowrap !important;
    transition: background 0.16s ease, color 0.16s ease, border-color 0.16s ease;
}

/* the label is its own markdown container — it must inherit, never take
   --apex-text, or it paints dark ink on a dark fill */
.stButton > button *, [data-testid="stDownloadButton"] button *,
[data-testid^="stBaseButton"] * {
    color: inherit !important;
    font-family: var(--apex-font) !important;
    font-weight: 600 !important;
    font-size: 17px !important;
}

/* solid ink — the primary action */
.stButton > button[kind="primary"],
[data-testid="stBaseButton-primary"],
[data-testid="stDownloadButton"] button {
    background: var(--apex-cta-bg) !important;
    color: var(--apex-cta-fg) !important;
    border: 1px solid var(--apex-cta-bg) !important;
}
.stButton > button[kind="primary"]:hover,
[data-testid="stBaseButton-primary"]:hover,
[data-testid="stDownloadButton"] button:hover {
    background: var(--apex-cta-bg-hover) !important;
    border-color: var(--apex-cta-bg-hover) !important;
    color: var(--apex-cta-fg) !important;
}

/* outlined — everything else, including the theme toggle */
.stButton > button[kind="secondary"],
[data-testid="stBaseButton-secondary"],
[data-testid="stBaseButton-tertiary"] {
    background: transparent !important;
    color: var(--apex-accent-text) !important;
    border: 1px solid var(--apex-accent) !important;
}
.stButton > button[kind="secondary"]:hover,
[data-testid="stBaseButton-secondary"]:hover,
[data-testid="stBaseButton-tertiary"]:hover {
    background: var(--apex-accent-soft) !important;
    color: var(--apex-accent-text) !important;
}

/* Disabled: drop the fill, keep the label legible. The border goes on the
   BUTTON only — putting it on `*` too drew a second box inside the first. */
.stButton > button:disabled, [data-testid^="stBaseButton"]:disabled {
    background: transparent !important;
    border: 1px dashed var(--apex-faint) !important;
    color: var(--apex-dim) !important;
    opacity: 1 !important;
    cursor: not-allowed !important;
}
.stButton > button:disabled * , [data-testid^="stBaseButton"]:disabled * {
    color: var(--apex-dim) !important;
    border: 0 !important;
    background: transparent !important;
}

/* ══ inputs ═══════════════════════════════════════════════════════════════ */

.stTextArea textarea, .stTextInput input {
    background: var(--apex-bg) !important;
    color: var(--apex-text) !important;
    font-family: var(--apex-font) !important;
    font-size: 16px !important;
    border: 1px solid var(--apex-divider) !important;
    border-radius: var(--apex-radius-md) !important;
    caret-color: var(--apex-accent) !important;
}
.stTextArea textarea::placeholder { color: var(--apex-dim) !important; opacity: 1; }
.stTextArea textarea:focus, .stTextInput input:focus { border-color: var(--apex-accent) !important; box-shadow: none !important; }

[data-baseweb="select"] > div {
    background: var(--apex-bg) !important;
    border: 1px solid var(--apex-divider) !important;
    border-radius: var(--apex-radius-md) !important;
    font-family: var(--apex-font) !important;
    font-size: 16px !important;
    color: var(--apex-text) !important;
    min-height: 42px !important;
}
[data-baseweb="select"] div, [data-baseweb="select"] span { color: var(--apex-text) !important; }
[data-baseweb="select"] svg { fill: var(--apex-accent-text) !important; color: var(--apex-accent-text) !important; }
[data-baseweb="popover"] [data-baseweb="menu"], [data-baseweb="popover"] ul {
    background: var(--apex-panel) !important;
    border: 1px solid var(--apex-divider) !important;
    font-family: var(--apex-font) !important;
}
[data-baseweb="popover"] li { font-size: 16px !important; color: var(--apex-text) !important; }
[data-baseweb="popover"] li:hover, [data-baseweb="popover"] li[aria-selected="true"] {
    background: var(--apex-accent-soft) !important; color: var(--apex-accent-text) !important;
}

/* radio → segmented control */
[data-testid="stRadio"] [role="radiogroup"] {
    display: inline-flex !important; gap: 0 !important;
    border: 1px solid var(--apex-divider);
    border-radius: var(--apex-radius-md); overflow: hidden;
}
[data-testid="stRadio"] [role="radiogroup"] label {
    margin: 0 !important; padding: 8px 16px !important;
    font-family: var(--apex-font) !important; font-size: 16px !important;
    color: var(--apex-text) !important; background: transparent !important;
}
[data-testid="stRadio"] [role="radiogroup"] label * { color: var(--apex-text) !important; }
[data-testid="stRadio"] [role="radiogroup"] label:not(:first-child) { border-left: 1px solid var(--apex-divider); }
[data-testid="stRadio"] [role="radiogroup"] label:hover { background: var(--apex-accent-soft) !important; }
[data-testid="stRadio"] [role="radiogroup"] label:has(input:checked) {
    background: var(--apex-accent-soft) !important;
    box-shadow: inset 0 -2px 0 var(--apex-accent);
}
[data-testid="stRadio"] [role="radiogroup"] label:has(input:checked) * { color: var(--apex-accent-text) !important; }
[data-testid="stRadio"] [role="radiogroup"] label > div:first-child { display: none !important; }

/* checkbox — fill the box, and force the tick glyph to the contrasting ink.
   Do NOT blanket-reset span backgrounds here; that erased the fill before. */
[data-testid="stCheckbox"] label {
    font-family: var(--apex-font) !important;
    font-size: 16px !important;
    color: var(--apex-text) !important;
    align-items: center !important;
}
[data-testid="stCheckbox"] label > span:first-child,
[data-testid="stCheckbox"] [data-baseweb="checkbox"] > span:first-child {
    background: var(--apex-bg) !important;
    border: 1.5px solid var(--apex-faint) !important;
    border-radius: var(--apex-radius-md) !important;
}
[data-testid="stCheckbox"] label:has(input:checked) > span:first-child,
[data-testid="stCheckbox"] [data-baseweb="checkbox"] > span[data-checked="true"] {
    background: var(--apex-cta-bg) !important;
    border-color: var(--apex-cta-bg) !important;
}
[data-testid="stCheckbox"] label:has(input:checked) > span:first-child svg,
[data-testid="stCheckbox"] span[data-checked="true"] svg {
    fill: var(--apex-cta-fg) !important;
    stroke: var(--apex-cta-fg) !important;
    color: var(--apex-cta-fg) !important;
    opacity: 1 !important;
}
[data-testid="stCheckbox"] label > div { color: var(--apex-text) !important; }

/* file uploader */
[data-testid="stFileUploaderDropzone"] {
    background: var(--apex-bg) !important;
    border: 1px dashed var(--apex-faint) !important;
    border-radius: var(--apex-radius-md) !important;
    padding: var(--apex-space-4) !important;
}
[data-testid="stFileUploaderDropzone"]:hover { border-color: var(--apex-accent) !important; }
[data-testid="stFileUploaderDropzone"] svg { fill: var(--apex-accent-text) !important; }
[data-testid="stFileUploaderDropzoneInstructions"] span,
[data-testid="stFileUploaderDropzoneInstructions"] div,
[data-testid="stFileUploaderDropzoneInstructions"] small {
    font-family: var(--apex-font) !important; color: var(--apex-text) !important; font-size: 15px !important;
}
[data-testid="stFileUploaderFile"], [data-testid="stFileUploaderFile"] * {
    font-family: var(--apex-font) !important; color: var(--apex-text) !important; font-size: 15px !important;
}

/* ══ tabs ═════════════════════════════════════════════════════════════════ */

[data-baseweb="tab-list"] {
    gap: var(--apex-space-8) !important; background: transparent !important;
    border-bottom: 1px solid var(--apex-divider) !important; padding: 0 !important;
}
[data-baseweb="tab"] {
    background: transparent !important;
    padding: 0 0 var(--apex-space-3) 0 !important;
    font-family: var(--apex-font) !important;
    font-weight: 600 !important; font-size: 21px !important;
    color: var(--apex-dim) !important;
    border-bottom: 2px solid transparent !important;
    margin-bottom: -1px !important;
}
[data-baseweb="tab"] * { color: inherit !important; font-size: 21px !important; }
[data-baseweb="tab"]:hover { color: var(--apex-text) !important; }
[data-baseweb="tab"][aria-selected="true"] {
    color: var(--apex-accent-text) !important; border-bottom-color: var(--apex-accent) !important;
}
[data-baseweb="tab-highlight"], [data-baseweb="tab-border"] { display: none !important; }
[data-baseweb="tab-panel"] { padding-top: var(--apex-space-6) !important; }

/* ══ alerts, expander, spinner ════════════════════════════════════════════ */

[data-testid="stAlert"], [data-testid="stAlertContainer"], [data-testid="stNotification"] {
    background: transparent !important; border: 0 !important;
    border-left: 2px solid var(--apex-accent) !important; border-radius: 0 !important;
    padding: var(--apex-space-1) 0 var(--apex-space-1) var(--apex-space-3) !important;
    box-shadow: none !important;
}
[data-testid="stAlert"] p, [data-testid="stAlertContainer"] p,
[data-testid="stAlert"] div, [data-testid="stAlertContainer"] div {
    font-family: var(--apex-font) !important; font-size: 17px !important; color: var(--apex-text) !important;
}
[data-testid="stAlert"] svg, [data-testid="stAlertContainer"] svg { display: none !important; }

[data-testid="stExpander"] {
    background: transparent !important; border: 0 !important;
    border-bottom: 1px solid var(--apex-divider) !important; border-radius: 0 !important;
}
[data-testid="stExpander"] summary {
    background: transparent !important; padding: var(--apex-space-3) 0 !important;
    font-family: var(--apex-font) !important; font-size: 17px !important; color: var(--apex-text) !important;
}
[data-testid="stExpander"] summary * { color: var(--apex-text) !important; font-size: 17px !important; }
[data-testid="stExpander"] summary:hover, [data-testid="stExpander"] summary:hover * { color: var(--apex-accent-text) !important; }
[data-testid="stExpander"] summary svg { fill: var(--apex-accent-text) !important; }
[data-testid="stExpanderDetails"] { padding: 0 0 var(--apex-space-4) 0 !important; }

[data-testid="stSpinner"] i, .stSpinner > div { border-top-color: var(--apex-accent) !important; border-right-color: transparent !important; }
[data-testid="stSpinner"] p { color: var(--apex-text) !important; font-family: var(--apex-font) !important; }
.stCode, pre, code {
    background: var(--apex-panel) !important; color: var(--apex-text) !important;
    border: 1px solid var(--apex-divider) !important; border-radius: var(--apex-radius-md) !important; font-size: 14px !important;
}
::-webkit-scrollbar { width: 9px; height: 9px; }
::-webkit-scrollbar-track { background: var(--apex-bg); }
::-webkit-scrollbar-thumb { background: var(--apex-track); border-radius: var(--apex-radius-sm); }
::-webkit-scrollbar-thumb:hover { background: var(--apex-accent); }

/* ══════════════════════════════════════════════════════════════════════════
   APEX components
   ══════════════════════════════════════════════════════════════════════════ */

/* The hero light field is masked to nothing at its edges — an unmasked
   gradient inside overflow:hidden printed a hard-edged rectangle. */
.apex-hero { position: relative; overflow: hidden; padding: 56px 0 40px; }
.apex-hero-field {
    position: absolute; inset: -20%; pointer-events: none;
    animation: apexDrift 30s ease-in-out infinite;
    background:
        radial-gradient(40% 46% at 24% 18%, var(--apex-glow-a) 0%, transparent 70%),
        radial-gradient(44% 50% at 78% 30%, var(--apex-glow-b) 0%, transparent 72%);
    -webkit-mask-image: radial-gradient(ellipse 62% 58% at 50% 46%, #000 0%, transparent 78%);
    mask-image: radial-gradient(ellipse 62% 58% at 50% 46%, #000 0%, transparent 78%);
}
.apex-hero-inner { position: relative; display: flex; flex-direction: column; align-items: center; text-align: center; }
.apex-eyebrow {
    animation: apexRise 0.7s ease-out both;
    display: flex; align-items: center; gap: 10px;
    font-size: 15px; letter-spacing: 0.1em; text-transform: uppercase;
    color: var(--apex-accent-text); padding-bottom: var(--apex-space-4);
}
.apex-dot { width: 7px; height: 7px; border-radius: 50%; background: var(--apex-accent); animation: apexPulse 2.4s ease-in-out infinite; }
.apex-display {
    animation: apexRise 0.7s ease-out both;
    font-family: var(--apex-font); font-weight: 700;
    font-size: clamp(40px, 5.6vw, 82px); line-height: 1.04; letter-spacing: -0.028em;
    color: var(--apex-display); max-width: 22ch; margin: 0;
}
.apex-display em { font-style: italic; font-weight: 400; color: var(--apex-em); }
.apex-drawn-rule {
    width: 120px; height: 2px; background: var(--apex-accent);
    transform-origin: center; animation: apexDraw 1s cubic-bezier(0.16,0.84,0.28,1) 0.5s both;
    margin-top: var(--apex-space-4);
}
.apex-lede {
    animation: apexRise 0.7s ease-out 0.18s both;
    font-size: 20px; line-height: 1.6; color: var(--apex-text);
    max-width: 58ch; padding-top: var(--apex-space-4);
}

.apex-kicker { font-size: 14px; letter-spacing: 0.09em; text-transform: uppercase; color: var(--apex-dim); }
.apex-h { font-family: var(--apex-font); font-weight: 600; font-size: 23px; color: var(--apex-display); margin: 0; }
.apex-h-lg {
    font-family: var(--apex-font); font-weight: 700;
    font-size: clamp(28px, 3.2vw, 42px); letter-spacing: -0.022em; line-height: 1.1;
    color: var(--apex-display); margin: 0;
}
.apex-h-lg em { font-style: italic; font-weight: 400; color: var(--apex-dim); font-size: 0.72em; }
.apex-note { font-size: 17px; line-height: 1.6; color: var(--apex-dim); max-width: 68ch; }
.apex-prose { font-size: 18px; line-height: 1.62; color: var(--apex-text); max-width: 68ch; }
.apex-rule { height: 1px; background: var(--apex-divider); margin: var(--apex-space-6) 0 var(--apex-space-4); }
.apex-row { display: flex; justify-content: space-between; align-items: baseline; gap: var(--apex-space-4); flex-wrap: wrap; }

/* — the gauge — */
.apex-score { display: grid; grid-template-columns: 236px 1fr; gap: var(--apex-space-8); align-items: center; }
@media (max-width: 900px) { .apex-score { grid-template-columns: 1fr; justify-items: center; } }
.apex-gauge { position: relative; width: 236px; height: 236px; }
.apex-gauge svg { display: block; }
.apex-gauge-mid { position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 2px; }
.apex-gauge-num {
    animation: apexRise 0.8s ease-out 0.45s both;
    font-family: var(--apex-font); font-weight: 700; font-size: 84px; line-height: 1;
    color: var(--apex-accent-text); font-variant-numeric: lining-nums tabular-nums;
    letter-spacing: -0.03em;
}
.apex-gauge-lbl { animation: apexRise 0.8s ease-out 0.65s both; font-size: 14px; letter-spacing: 0.09em; text-transform: uppercase; color: var(--apex-dim); }
/* never centre with transform here — apexRise animates transform and wins */
.apex-gauge-foot {
    position: absolute; left: 0; right: 0; bottom: 8px; text-align: center;
    animation: apexRise 0.8s ease-out 1s both;
    font-size: 16px; color: var(--apex-accent-text); white-space: nowrap;
}

.apex-metrics { display: grid; grid-template-columns: repeat(3, 1fr); gap: var(--apex-space-6); }
@media (max-width: 700px) { .apex-metrics { grid-template-columns: 1fr; gap: var(--apex-space-4); } }
.apex-metric-label { font-size: 14px; letter-spacing: 0.09em; text-transform: uppercase; color: var(--apex-dim); }
.apex-figure {
    font-family: var(--apex-font); font-weight: 700;
    font-size: clamp(48px, 4.6vw, 68px); line-height: 1; letter-spacing: -0.03em;
    font-variant-numeric: lining-nums tabular-nums;
    color: var(--apex-display); padding: var(--apex-space-2) 0;
}
.apex-figure sup { font-size: 0.4em; font-weight: 400; color: var(--apex-dim); vertical-align: baseline; }
.apex-figure-quiet { color: var(--apex-dim); }
.apex-bar { height: 3px; background: var(--apex-track); border-radius: var(--apex-radius-sm); overflow: hidden; }
.apex-bar > div { height: 100%; background: var(--apex-accent); transform-origin: left; animation: apexGrow 1.3s cubic-bezier(0.16,0.84,0.28,1) 0.55s both; }
.apex-bar-quiet > div { background: var(--apex-faint); }
.apex-metric-foot { font-size: 16px; color: var(--apex-dim); padding-top: var(--apex-space-2); }

/* — the trace — */
.apex-seg { display: flex; gap: 6px; padding: var(--apex-space-4) 0; }
.apex-seg > div { flex: 1; height: 4px; border-radius: var(--apex-radius-sm); background: var(--apex-track); overflow: hidden; }
.apex-seg > div.done { background: var(--apex-accent); }
.apex-seg > div.now > i { display: block; height: 100%; background: var(--apex-accent-text); transform-origin: left; animation: apexGrow 1.7s ease-in-out infinite alternate; }
.apex-log-line {
    display: grid; grid-template-columns: 26px 150px 1fr; gap: var(--apex-space-2);
    align-items: baseline; padding: 10px 0; font-size: 17px; color: var(--apex-text);
}
@media (max-width: 620px) { .apex-log-line { grid-template-columns: 26px 1fr; } .apex-log-line .apex-log-node { display: none; } }
.apex-log-node { color: var(--apex-dim); }
.apex-log-line.queued { color: var(--apex-faint); }
.apex-log-line.now {
    padding: 13px var(--apex-space-3); border-radius: var(--apex-radius-md);
    background: linear-gradient(100deg, var(--apex-tint) 30%, var(--apex-accent-soft) 60%, var(--apex-tint) 70%);
    background-size: 220% 100%; animation: apexSheen 2.6s linear infinite;
}

/* — findings, tags, tables — */
.apex-two { display: grid; grid-template-columns: 1fr 1fr; gap: var(--apex-space-8); }
@media (max-width: 800px) { .apex-two { grid-template-columns: 1fr; gap: var(--apex-space-4); } }
.apex-finding { font-size: 18px; line-height: 1.62; color: var(--apex-text); padding-left: 16px; border-left: 2px solid var(--apex-accent); margin-bottom: var(--apex-space-3); }
.apex-finding-quiet { border-left-color: var(--apex-faint); }

.apex-tags { display: flex; flex-wrap: wrap; gap: 7px; }
.apex-tag {
    display: inline-flex; align-items: center; font-size: 16px; padding: 4px 11px;
    border-radius: var(--apex-radius-md); background: var(--apex-tint); color: var(--apex-accent-text);
}
.apex-tag-absent { background: transparent; border: 1px dashed var(--apex-faint); color: var(--apex-text); }
.apex-tag-neutral { background: transparent; border: 1px solid var(--apex-divider); color: var(--apex-dim); }

.apex-table { width: 100%; border-collapse: collapse; font-size: 17px; }
.apex-table th {
    text-align: left; font-family: var(--apex-font); font-weight: 400;
    font-size: 14px; letter-spacing: 0.09em; text-transform: uppercase; color: var(--apex-dim);
    padding: 0 var(--apex-space-3) var(--apex-space-2) 0; border-bottom: 1px solid var(--apex-divider);
}
.apex-table td { padding: var(--apex-space-3) var(--apex-space-3) var(--apex-space-3) 0; border-bottom: 1px solid var(--apex-divider); color: var(--apex-text); vertical-align: top; line-height: 1.55; }
.apex-table td.quiet { color: var(--apex-dim); }
.apex-table td.gold { color: var(--apex-accent-text); }
.apex-table td.right, .apex-table th.right { text-align: right; padding-right: 0; }
@media (max-width: 640px) {
    .apex-table, .apex-table tbody, .apex-table tr, .apex-table td { display: block; width: 100%; }
    .apex-table thead { display: none; }
    .apex-table tr { border-bottom: 1px solid var(--apex-divider); padding: var(--apex-space-2) 0; }
    .apex-table td { border-bottom: 0; padding: 2px 0; text-align: left !important; }
}

/* — the diff — */
.apex-diff-pair { display: grid; grid-template-columns: 1fr 1fr; gap: var(--apex-space-8); padding: var(--apex-space-4) 0; border-top: 1px solid var(--apex-divider); }
@media (max-width: 800px) { .apex-diff-pair { grid-template-columns: 1fr; gap: var(--apex-space-3); } }
.apex-diff-label { font-size: 14px; letter-spacing: 0.09em; text-transform: uppercase; color: var(--apex-dim); padding-bottom: var(--apex-space-1); }
.apex-diff-label.after { color: var(--apex-accent-text); }
.apex-before { font-size: 18px; line-height: 1.62; color: var(--apex-dim); }
.apex-after { font-size: 18px; line-height: 1.62; color: var(--apex-text); }
.apex-after .kw { color: var(--apex-accent-text); border-bottom: 2px solid var(--apex-accent); }
.apex-quote { font-size: 22px; line-height: 1.5; color: var(--apex-text); max-width: 60ch; padding: var(--apex-space-4) 0 var(--apex-space-6); font-style: italic; }

/* — the letter: a document, not a screen. Paper in BOTH themes, so its ink is
     pinned locally rather than inherited. — */
.apex-plate {
    max-width: 780px; margin: 0 auto; background: #f8f4f4;
    padding: 60px 68px; border: 8px solid var(--apex-panel); box-shadow: var(--apex-shadow-lg);
}
@media (max-width: 640px) { .apex-plate { padding: 30px 24px; } }
.apex-plate, .apex-plate * { color: #201e1d !important; }
.apex-plate .muted, .apex-plate .muted * { color: #4a4746 !important; }
.apex-plate-subject {
    font-family: var(--apex-font); font-weight: 700; font-size: 26px; line-height: 1.2;
    letter-spacing: -0.02em;
    padding-bottom: var(--apex-space-3); border-bottom: 1px solid rgba(32,30,29,0.16); margin-bottom: var(--apex-space-4);
}
.apex-plate p { margin: 0 0 var(--apex-space-3); font-size: 18px; line-height: 1.7; }
.apex-plate p:last-child { margin-bottom: 0; }

/* — run gate, steps, graph — */
.apex-gate { display: flex; flex-direction: column; gap: 7px; font-size: 16px; margin-bottom: var(--apex-space-3); }
.apex-gate-item { display: flex; align-items: center; gap: 9px; color: var(--apex-dim); }
.apex-gate-item.met { color: var(--apex-accent-text); }

.apex-steps { display: grid; grid-template-columns: repeat(4, 1fr); gap: var(--apex-space-6); }
@media (max-width: 1000px) { .apex-steps { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 600px) { .apex-steps { grid-template-columns: 1fr; gap: var(--apex-space-4); } }
.apex-step-num { font-family: var(--apex-font); font-weight: 700; font-size: 30px; line-height: 1; color: var(--apex-accent-text); font-variant-numeric: lining-nums; }
.apex-step-title { font-family: var(--apex-font); font-weight: 600; font-size: 21px; color: var(--apex-display); padding-top: 10px; }
.apex-step-body { font-size: 17px; color: var(--apex-dim); line-height: 1.55; padding-top: 6px; }

.apex-graph { display: flex; flex-direction: column; gap: var(--apex-space-2); font-size: 17px; color: var(--apex-text); }
.apex-graph-line { display: flex; align-items: center; gap: var(--apex-space-2); flex-wrap: wrap; }
.apex-graph-line.indent { padding-left: var(--apex-space-6); }
.apex-node { border: 1px solid var(--apex-divider); border-radius: var(--apex-radius-md); padding: 5px 12px; }
.apex-node.loop { border-color: var(--apex-accent); color: var(--apex-accent-text); }
.apex-graph em { color: var(--apex-dim); font-style: italic; }

.apex-numlist { display: flex; flex-direction: column; gap: var(--apex-space-3); }
.apex-numitem { display: grid; grid-template-columns: 30px 1fr; font-size: 18px; color: var(--apex-text); line-height: 1.6; }
.apex-numitem span:first-child { font-weight: 700; color: var(--apex-accent-text); font-variant-numeric: lining-nums; }

/* ══════════════════════════════════════════════════════════════════════════
   Green system — pill geometry, icon-font repair, sidebar re-open control
   ══════════════════════════════════════════════════════════════════════════ */

/* Streamlit draws its glyphs with a Material Symbols LIGATURE font: the markup
   literally contains the word "upload" and the font turns it into an icon.
   The blanket font-family override above swapped in the serif, so the ligature
   never formed and the word printed next to the label — that is the whole
   "uploadUpload" bug. Restore the icon font wherever a glyph lives. */
[data-testid="stIconMaterial"], [class*="material-symbols"],
.stButton > button [data-testid="stIconMaterial"],
[data-testid="stFileUploaderDropzone"] [data-testid="stIconMaterial"] {
    font-family: "Material Symbols Rounded", "Material Symbols Outlined", sans-serif !important;
    font-weight: 400 !important;
    font-size: 20px !important;
    letter-spacing: normal !important;
    line-height: 1 !important;
}

/* ── pill geometry ─────────────────────────────────────────────────────────*/
.stButton > button, [data-testid="stDownloadButton"] button, [data-testid^="stBaseButton"] {
    border-radius: var(--apex-radius-pill) !important;
    padding: 13px 30px !important;
}
[data-baseweb="select"] > div {
    border-radius: var(--apex-radius-pill) !important;
    padding-left: 10px !important;
    min-height: 46px !important;
}
[data-baseweb="popover"] [data-baseweb="menu"], [data-baseweb="popover"] ul {
    border-radius: var(--apex-radius-md) !important; overflow: hidden !important;
}
[data-testid="stRadio"] [role="radiogroup"] {
    border-radius: var(--apex-radius-pill) !important;
    padding: 4px !important; gap: 4px !important;
    background: var(--apex-panel) !important;
}
[data-testid="stRadio"] [role="radiogroup"] label {
    border-radius: var(--apex-radius-pill) !important;
    padding: 8px 18px !important;
}
[data-testid="stRadio"] [role="radiogroup"] label:not(:first-child) { border-left: 0 !important; }
[data-testid="stRadio"] [role="radiogroup"] label:has(input:checked) {
    background: var(--apex-cta-bg) !important; box-shadow: none !important;
}
[data-testid="stRadio"] [role="radiogroup"] label:has(input:checked) * {
    color: var(--apex-cta-fg) !important;
}
.stTextArea textarea, .stTextInput input {
    border-radius: var(--apex-radius-md) !important;
    padding: 12px 14px !important;
    line-height: 1.6 !important;
}
[data-testid="stFileUploaderDropzone"] {
    border-radius: var(--apex-radius-lg) !important;
    border-width: 1.5px !important;
}
[data-testid="stCheckbox"] label > span:first-child,
[data-testid="stCheckbox"] [data-baseweb="checkbox"] > span:first-child {
    border-radius: 7px !important;
}
.apex-node { border-radius: var(--apex-radius-pill); padding: 7px 18px; }
.apex-tag { border-radius: var(--apex-radius-pill); padding: 6px 14px; }
.apex-bar, .apex-seg > div, .apex-bar > div { border-radius: var(--apex-radius-pill); }
.apex-plate { border-radius: var(--apex-radius-lg); }

/* The letter stays paper in both themes — its ink moves into the green family
   rather than reverting to near-black. */
.apex-plate { background: #f4faf6; }
.apex-plate, .apex-plate * { color: #1d3a26 !important; }
.apex-plate .muted, .apex-plate .muted * { color: #3a5a36 !important; }
.apex-plate-subject { border-bottom-color: rgba(29, 58, 38, 0.18); }

/* ── the graph, drawn ──────────────────────────────────────────────────────*/
.apex-graph-card {
    background: var(--apex-panel);
    border-radius: var(--apex-radius-lg);
    padding: 26px 28px 20px;
    display: flex; flex-direction: column; gap: 18px;
}
.apex-graph-svg {
    width: 100%; height: auto; display: block;
    font-family: var(--apex-font); overflow: visible;
}
.apex-graph-key {
    display: flex; gap: 28px; flex-wrap: wrap; align-items: center;
    border-top: 1px solid var(--apex-divider); padding-top: 16px;
    font-size: 16px; color: var(--apex-dim);
}
.apex-graph-key > div { display: flex; align-items: center; gap: 10px; }

/* ── the sidebar is structural, not dismissable ────────────────────────────
   It holds every input the app has. Streamlit collapses it by translating it
   off-canvas and the re-open control lives in a header we flatten to nothing,
   so once it was gone it never came back. It is now pinned open and the
   collapse affordance is removed rather than restyled. */
[data-testid="stSidebar"] {
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    transform: none !important;
    margin-left: 0 !important;
    left: 0 !important;
}
[data-testid="stSidebar"][aria-expanded="false"] { transform: none !important; }
[data-testid="stSidebarContent"] { display: flex !important; visibility: visible !important; }
[data-testid="stSidebarCollapseButton"], [data-testid="stSidebarCollapsedControl"] {
    display: none !important;
}
@media (min-width: 1100px) {
    [data-testid="stSidebar"], [data-testid="stSidebar"] > div:first-child,
    [data-testid="stSidebar"] [data-testid="stSidebarContent"] {
        width: 340px !important; min-width: 340px !important; max-width: 340px !important;
    }
}

/* ── the invisible header must not intercept clicks ────────────────────────
   Streamlit's toolbar header is position:fixed, ~3.75rem tall, and spans the
   full width. This stylesheet makes it transparent, but a transparent element
   still takes pointer events — which is why the theme switch, sitting under
   its lower edge, only responded on its bottom half. Pass clicks through the
   bar itself and re-arm only its real controls. */
[data-testid="stHeader"], [data-testid="stToolbar"] ~ div, header[data-testid="stHeader"] {
    pointer-events: none !important;
    background: transparent !important;
    height: 0 !important;
    min-height: 0 !important;
}
[data-testid="stHeader"] button, [data-testid="stHeader"] a,
[data-testid="stToolbar"], [data-testid="stToolbar"] * { pointer-events: auto !important; }
[data-testid="stAppViewContainer"] > .main .block-container,
[data-testid="stAppViewBlockContainer"] { padding-top: 34px !important; }

/* tooltips are chrome, and chrome follows the theme */
[data-testid="stTooltipContent"], [role="tooltip"], [data-baseweb="tooltip"] > div {
    background: var(--apex-cta-bg) !important;
    color: var(--apex-cta-fg) !important;
    border-radius: var(--apex-radius-md) !important;
    font-family: var(--apex-font) !important;
    font-size: 14px !important;
    padding: 8px 14px !important;
    box-shadow: var(--apex-shadow-sm) !important;
}
[data-testid="stTooltipContent"] *, [role="tooltip"] *, [data-baseweb="tooltip"] > div * {
    color: var(--apex-cta-fg) !important;
    font-family: var(--apex-font) !important;
    font-size: 14px !important;
}
/* the tooltip's hover target wraps the button — it must not shrink its hit area */
[data-testid="stTooltipHoverTarget"] { width: 100% !important; display: block !important; }
[data-testid="stTooltipHoverTarget"] > div { width: 100% !important; }
</style>
"""


def apex_css(theme: str = "light") -> str:
    return _CSS.replace("__TOKENS__", DARK if theme == "dark" else LIGHT)


def apply_styles(theme: str = "light") -> None:
    import streamlit as st
    st.markdown(apex_css(theme), unsafe_allow_html=True)


# ── Phosphor-style icons, inlined ─────────────────────────────────────────────

_PATHS = {
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "arrow-right": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
    "circle": '<circle cx="12" cy="12" r="9"/>',
    "download": '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="m7 10 5 5 5-5"/><path d="M12 15V3"/>',
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M6.3 17.7l-1.4 1.4M19.1 4.9l-1.4 1.4"/>',
    "moon": '<path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/>',
}


def icon(name: str, size: int = 15, stroke: str = "currentColor", width: float = 2.0) -> str:
    return (
        f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
        f'stroke="{stroke}" stroke-width="{width}" stroke-linecap="round" '
        f'stroke-linejoin="round" aria-hidden="true">{_PATHS.get(name, "")}</svg>'
    )


def gauge(score: int, label: str = "ATS score", foot: str = "") -> str:
    """The score as an accent arc that draws itself. The end value rides on an
    inline --dash property, so the score drives the animation."""
    score = max(0, min(100, int(score)))
    arc = "M43.43 156.57 A 80 80 0 1 1 156.57 156.57"
    return (
        '<div class="apex-gauge">'
        '<svg width="236" height="236" viewBox="0 0 200 200">'
        f'<path d="{arc}" fill="none" stroke="var(--apex-track)" stroke-width="6" stroke-linecap="round"></path>'
        f'<path d="{arc}" pathLength="100" fill="none" stroke="var(--apex-accent)" stroke-width="6" '
        f'stroke-linecap="round" stroke-dasharray="100 100" '
        f'style="--dash:{100 - score}; stroke-dashoffset:{100 - score}; '
        f'animation:apexArc 1.6s cubic-bezier(0.16,0.84,0.28,1) 0.15s both;"></path>'
        "</svg>"
        '<div class="apex-gauge-mid">'
        f'<div class="apex-gauge-num">{score}</div>'
        f'<div class="apex-gauge-lbl">{label}</div>'
        "</div>"
        + (f'<div class="apex-gauge-foot">{foot}</div>' if foot else "")
        + "</div>"
    )


def graph_svg(threshold: int = 75) -> str:
    """The LangGraph route as a drawn diagram rather than three lines of text.

    Solid edges are the path that clears the threshold; dashed edges fall short
    and loop back into ats_score. Coordinates are fixed against the 844x252
    viewBox, so the whole thing scales with the column and never reflows.

    Emitted as ONE unindented line on purpose: Streamlit runs its markdown
    parser over this string first, and any line indented four spaces or more
    becomes a fenced code block — which is what printed the raw SVG source.
    """
    alt = (
        f"parse to ats_score. At or above {threshold}: cover_letter then "
        "learning. Below: critique, rewrite, and back to ats_score."
    )
    return (
        '<div class="apex-graph-card">'
        '<svg viewBox="0 0 844 252" class="apex-graph-svg" role="img" '
        f'aria-label="{alt}">'
        '<defs>'
        '<marker id="apexArrow" viewBox="0 0 10 10" refX="9" refY="5" '
        'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        '<path d="M0,0 L10,5 L0,10 z" fill="var(--apex-accent)"></path>'
        '</marker>'
        '</defs>'
        '<g stroke="var(--apex-accent)" stroke-width="2" fill="none" marker-end="url(#apexArrow)">'
        '<path d="M104,119 H144"></path>'
        '<path d="M282,119 H324"></path>'
        '<path d="M510,119 V45 H550"></path>'
        '<path d="M706,45 H724"></path>'
        '</g>'
        '<path d="M480,119 H510" stroke="var(--apex-accent)" stroke-width="2" fill="none"></path>'
        '<g stroke="var(--apex-accent)" stroke-width="2" fill="none" stroke-dasharray="6 5" '
        'marker-end="url(#apexArrow)">'
        '<path d="M510,119 V193 H550"></path>'
        '<path d="M672,193 H694"></path>'
        '<path d="M758,216 V238 H216 V148"></path>'
        '</g>'
        '<g fill="var(--apex-panel)" stroke="var(--apex-faint)" stroke-width="1.5">'
        '<rect x="0" y="96" width="104" height="46" rx="23"></rect>'
        '<rect x="150" y="96" width="132" height="46" rx="23"></rect>'
        '<rect x="556" y="22" width="150" height="46" rx="23"></rect>'
        '<rect x="730" y="22" width="110" height="46" rx="23"></rect>'
        '<rect x="556" y="170" width="116" height="46" rx="23"></rect>'
        '<rect x="700" y="170" width="116" height="46" rx="23"></rect>'
        '</g>'
        '<rect x="330" y="96" width="150" height="46" rx="23" fill="none" '
        'stroke="var(--apex-accent)" stroke-width="2" stroke-dasharray="7 5"></rect>'
        '<g fill="var(--apex-text)" font-size="17" text-anchor="middle" dominant-baseline="central">'
        '<text x="52" y="120">parse</text>'
        '<text x="216" y="120">ats_score</text>'
        '<text x="631" y="46">cover_letter</text>'
        '<text x="785" y="46">learning</text>'
        '<text x="614" y="194">critique</text>'
        '<text x="758" y="194">rewrite</text>'
        '</g>'
        '<text x="405" y="120" fill="var(--apex-accent)" font-size="17" font-weight="600" '
        'text-anchor="middle" dominant-baseline="central">score &#8805; '
        f'{threshold}?</text>'
        '<g fill="var(--apex-accent)" font-size="16" font-style="italic">'
        '<text x="521" y="82">yes</text>'
        '<text x="521" y="163">no</text>'
        '</g>'
        '<text x="487" y="230" fill="var(--apex-dim)" font-size="16" font-style="italic" '
        'text-anchor="middle">re-score, and loop until it clears</text>'
        '</svg>'
        '<div class="apex-graph-key">'
        '<div><svg width="30" height="8" aria-hidden="true">'
        '<line x1="0" y1="4" x2="30" y2="4" stroke="var(--apex-accent)" stroke-width="2"></line>'
        '</svg>Clears the threshold</div>'
        '<div><svg width="30" height="8" aria-hidden="true">'
        '<line x1="0" y1="4" x2="30" y2="4" stroke="var(--apex-accent)" stroke-width="2" '
        'stroke-dasharray="6 5"></line>'
        '</svg>Falls short &#8212; critique, rewrite, re-score</div>'
        '</div>'
        '</div>'
    )
