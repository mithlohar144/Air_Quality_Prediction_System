"""Shared styles, navigation, and utilities for AirPulse."""

SHARED_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
    --ink:       #06080f;
    --ink2:      #0d1220;
    --ink3:      #141d30;
    --ink4:      #1c2840;
    --wire:      rgba(148,212,255,0.10);
    --wire2:     rgba(148,212,255,0.06);
    --sky:       #94d4ff;
    --mint:      #6ee7b7;
    --rose:      #fda4af;
    --amber:     #fcd34d;
    --violet:    #c4b5fd;
    --text:      #e8f0fe;
    --text2:     #8da4c0;
    --text3:     #4a6080;
    --mono:      'JetBrains Mono', monospace;
}

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stApp"] {
    background: var(--ink) !important;
    font-family: 'Outfit', sans-serif;
    color: var(--text);
    scroll-behavior: smooth;
}

[data-testid="stHeader"], footer, #MainMenu,
[data-testid="stToolbar"], [data-testid="stDecoration"] {
    display: none !important;
}

[data-testid="stAppViewContainer"] > .main { padding: 0 !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }
section[data-testid="stSidebar"] {
    background: var(--ink2) !important;
    border-right: 1px solid var(--wire) !important;
}
section[data-testid="stSidebar"] * { color: var(--text) !important; }
section[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background: var(--ink3) !important;
    border-color: var(--wire) !important;
}
section[data-testid="stSidebar"] label { color: var(--text2) !important; font-size:0.82rem !important; }

/* ── SIDEBAR HEADER ─── */
.ap-sidebar-title {
    font-family: 'Outfit', sans-serif;
    font-size: 0.7rem; font-weight: 700;
    letter-spacing: 0.12em; text-transform: uppercase;
    color: var(--sky); margin-bottom: 1.25rem;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid var(--wire);
}

/* ── NAV ─── */
.ap-nav {
    position: sticky; top: 0; z-index: 999;
    height: 58px;
    display: flex; align-items: center; justify-content: space-between;
    padding: 0 2.5rem;
    background: rgba(6,8,15,0.92);
    backdrop-filter: blur(20px) saturate(180%);
    border-bottom: 1px solid var(--wire);
}
.ap-logo {
    font-family: 'Outfit', sans-serif;
    font-size: 1.15rem; font-weight: 800;
    letter-spacing: -0.03em;
    display: flex; align-items: center; gap: 7px;
    text-decoration: none; color: inherit;
}
.ap-logo-mark {
    width: 28px; height: 28px; border-radius: 8px;
    background: linear-gradient(135deg, #94d4ff 0%, #6ee7b7 100%);
    display: flex; align-items: center; justify-content: center;
    font-size: 0.85rem;
}
.ap-logo-text { color: var(--text); }
.ap-logo-text em { font-style: normal; color: var(--sky); }
.ap-nav-center { display: flex; gap: 2px; }
.ap-nav-link {
    font-size: 0.82rem; font-weight: 500;
    color: var(--text3); text-decoration: none;
    padding: 0.35rem 0.85rem; border-radius: 7px;
    transition: all 0.18s; letter-spacing: 0.01em;
    white-space: nowrap;
}
.ap-nav-link:hover { color: var(--text); background: var(--ink3); }
.ap-nav-link.active { color: var(--sky); background: rgba(148,212,255,0.08); }
.ap-nav-pip {
    display: flex; align-items: center; gap: 6px;
    font-size: 0.72rem; font-weight: 600;
    color: var(--ink); background: var(--mint);
    padding: 0.22rem 0.7rem; border-radius: 20px;
    letter-spacing: 0.05em;
}
.ap-nav-pip::before {
    content: ''; width: 6px; height: 6px;
    border-radius: 50%; background: var(--ink);
    animation: live-blink 1.6s ease infinite;
}
@keyframes live-blink { 0%,100%{opacity:1} 50%{opacity:0.3} }

/* ── PAGE SHELL ─── */
.ap-page { min-height: 100vh; }

/* ── PAGE HERO ─── */
.ap-page-hero {
    padding: 2.5rem 2.5rem 2rem;
    border-bottom: 1px solid var(--wire);
    background: linear-gradient(180deg, var(--ink2) 0%, transparent 100%);
    position: relative; overflow: hidden;
}
.ap-page-hero::after {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, var(--sky), transparent);
    opacity: 0.4;
}
.ap-breadcrumb {
    font-family: var(--mono);
    font-size: 0.68rem; color: var(--text3);
    margin-bottom: 0.6rem;
    letter-spacing: 0.08em;
}
.ap-breadcrumb span { color: var(--sky); }
.ap-page-title {
    font-size: 1.6rem; font-weight: 800;
    letter-spacing: -0.025em; color: var(--text);
    margin-bottom: 0.3rem;
}
.ap-page-title em { font-style: normal; color: var(--sky); }
.ap-page-sub {
    font-size: 0.88rem; color: var(--text2);
    font-weight: 400; line-height: 1.6;
}

/* ── CARDS ─── */
.ap-card {
    background: var(--ink2);
    border: 1px solid var(--wire);
    border-radius: 12px; padding: 1.4rem;
    margin-bottom: 1rem; position: relative;
    overflow: hidden;
}
.ap-card-header {
    display: flex; align-items: center; justify-content: space-between;
    margin-bottom: 1rem;
}
.ap-card-title {
    font-size: 0.78rem; font-weight: 700;
    letter-spacing: 0.07em; text-transform: uppercase;
    color: var(--text2);
}
.ap-card-accent {
    font-family: var(--mono); font-size: 0.68rem;
    color: var(--sky); background: rgba(148,212,255,0.08);
    padding: 0.18rem 0.55rem; border-radius: 5px;
    border: 1px solid rgba(148,212,255,0.15);
}

/* ── METRICS ─── */
div[data-testid="metric-container"] {
    background: var(--ink2) !important;
    border: 1px solid var(--wire) !important;
    border-radius: 12px !important;
    padding: 1rem 1.2rem !important;
}
div[data-testid="metric-container"] [data-testid="stMetricLabel"] {
    font-size: 0.72rem !important; font-weight: 700 !important;
    letter-spacing: 0.07em !important; text-transform: uppercase !important;
    color: var(--text3) !important;
}
div[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-family: 'Outfit', sans-serif !important;
    font-size: 1.6rem !important; font-weight: 800 !important;
    color: var(--sky) !important; letter-spacing: -0.03em !important;
}
div[data-testid="metric-container"] [data-testid="stMetricDelta"] {
    font-size: 0.75rem !important;
}

/* ── CONTENT PADDING ─── */
.ap-content { padding: 1.75rem 2.5rem; }

/* ── PLOTLY CHART DARK ─── */
.stPlotlyChart { border-radius: 10px; overflow: hidden; }

/* ── TABLES ─── */
[data-testid="stDataFrame"] {
    border: 1px solid var(--wire) !important;
    border-radius: 10px !important; overflow: hidden !important;
}

/* ── SELECTBOX / INPUTS ─── */
[data-baseweb="select"] > div {
    background: var(--ink3) !important;
    border-color: var(--wire) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
}
[data-baseweb="input"] input {
    background: var(--ink3) !important;
    border-color: var(--wire) !important;
    color: var(--text) !important;
}

/* ── BUTTONS ─── */
.stButton button {
    background: linear-gradient(135deg, var(--sky), var(--mint)) !important;
    color: var(--ink) !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 700 !important; border: none !important;
    border-radius: 9px !important;
    padding: 0.5rem 1.4rem !important;
    letter-spacing: 0.01em !important;
    transition: opacity 0.2s, transform 0.2s !important;
}
.stButton button:hover {
    opacity: 0.9 !important; transform: translateY(-1px) !important;
}

/* ── TOGGLE ─── */
[data-testid="stToggle"] {
    padding: 0.6rem 0.8rem;
    background: var(--ink3);
    border-radius: 9px;
    border: 1px solid var(--wire);
}

/* ── RADIO ─── */
[data-testid="stRadio"] label { color: var(--text2) !important; font-size: 0.85rem !important; }

/* ── SLIDER ─── */
[data-testid="stSlider"] [data-baseweb="slider"] { padding: 0 !important; }

/* ── FILE UPLOADER ─── */
[data-testid="stFileUploaderDropzone"] {
    background: var(--ink3) !important;
    border: 2px dashed var(--wire) !important;
    border-radius: 12px !important;
}

/* ── CHECKBOX ─── */
[data-testid="stCheckbox"] label { color: var(--text2) !important; font-size: 0.85rem !important; }

/* ── PROGRESS ─── */
[data-testid="stProgress"] > div > div > div {
    background: linear-gradient(90deg, var(--sky), var(--mint)) !important;
    border-radius: 4px !important;
}

/* ── ALERTS ─── */
[data-testid="stAlert"] {
    border-radius: 10px !important;
    border: 1px solid var(--wire) !important;
}

/* ── SPINNER ─── */
[data-testid="stSpinner"] { color: var(--sky) !important; }

/* ── DIVIDER ─── */
hr { border-color: var(--wire) !important; }

/* ── SCROLLBAR ─── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--ink2); }
::-webkit-scrollbar-thumb { background: var(--wire); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(148,212,255,0.2); }

/* ── ANIMATION KEYFRAMES ─── */
@keyframes rise {
    from { opacity:0; transform: translateY(16px); }
    to   { opacity:1; transform: translateY(0); }
}
.rise { animation: rise 0.5s ease both; }
.rise-1 { animation-delay: 0.05s; }
.rise-2 { animation-delay: 0.1s; }
.rise-3 { animation-delay: 0.15s; }
.rise-4 { animation-delay: 0.2s; }
</style>
"""

def nav(active: str) -> str:
    """Render the shared navigation bar. active = 'home'|'data'|'forecast'|'alerts'|'admin'"""
    pages = [
        ("home",     "/",                 "Home"),
        ("data",     "/Data_Explorer",    "D1 · Data"),
        ("forecast", "/Forecast_Engine",  "D2 · Forecast"),
        ("alerts",   "/Alert_System",     "D3 · Alerts"),
        ("admin",    "/Admin_Dashboard",  "D4 · Admin"),
    ]
    links = ""
    for key, href, label in pages:
        cls = "ap-nav-link active" if key == active else "ap-nav-link"
        links += f'<a href="{href}" class="{cls}">{label}</a>'

    return f"""
<nav class="ap-nav">
    <a href="/" class="ap-logo">
        <div class="ap-logo-mark">🌬</div>
        <span class="ap-logo-text">Air<em>Pulse</em></span>
    </a>
    <div class="ap-nav-center">{links}</div>
    <div class="ap-nav-pip">LIVE</div>
</nav>
"""

def page_hero(breadcrumb: str, title: str, subtitle: str) -> str:
    return f"""
<div class="ap-page-hero rise">
    <div class="ap-breadcrumb">AirPulse / <span>{breadcrumb}</span></div>
    <div class="ap-page-title">{title}</div>
    <div class="ap-page-sub">{subtitle}</div>
</div>
"""

CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Outfit", color="#8da4c0", size=11),
    margin=dict(l=10, r=10, t=14, b=10),
    xaxis=dict(
        showgrid=True, gridcolor="rgba(148,212,255,0.06)",
        zeroline=False, color="#4a6080",
        tickfont=dict(size=10),
    ),
    yaxis=dict(
        showgrid=True, gridcolor="rgba(148,212,255,0.06)",
        zeroline=False, color="#4a6080",
        tickfont=dict(size=10),
    ),
    legend=dict(
        orientation="h", yanchor="bottom", y=-0.22,
        xanchor="center", x=0.5,
        font=dict(size=10, color="#8da4c0"),
        bgcolor="rgba(0,0,0,0)",
    ),
    hoverlabel=dict(
        bgcolor="#141d30", bordercolor="rgba(148,212,255,0.2)",
        font=dict(family="Outfit", size=12, color="#e8f0fe"),
    ),
)

PALETTE = {
    "sky":    "#94d4ff",
    "mint":   "#6ee7b7",
    "rose":   "#fda4af",
    "amber":  "#fcd34d",
    "violet": "#c4b5fd",
    "coral":  "#fb923c",
}

POLL_COLORS = {
    "PM2.5": "#94d4ff",
    "PM10":  "#c4b5fd",
    "NO2":   "#6ee7b7",
    "O3":    "#fcd34d",
    "SO2":   "#fda4af",
}

AQI_BANDS = [
    (50,  "Good",             "#4ade80", "rgba(74,222,128,0.1)",  "rgba(74,222,128,0.22)"),
    (100, "Moderate",         "#fcd34d", "rgba(252,211,77,0.1)",  "rgba(252,211,77,0.22)"),
    (150, "Sensitive Groups", "#fb923c", "rgba(251,146,60,0.1)",  "rgba(251,146,60,0.22)"),
    (200, "Unhealthy",        "#fda4af", "rgba(253,164,175,0.1)", "rgba(253,164,175,0.22)"),
    (300, "Very Unhealthy",   "#c4b5fd", "rgba(196,181,253,0.1)", "rgba(196,181,253,0.22)"),
    (500, "Hazardous",        "#ef4444", "rgba(239,68,68,0.12)",  "rgba(239,68,68,0.28)"),
]

def get_aqi_band(aqi: int):
    for threshold, label, color, bg, border in AQI_BANDS:
        if aqi <= threshold:
            return label, color, bg, border
    return "Hazardous", "#ef4444", "rgba(239,68,68,0.12)", "rgba(239,68,68,0.28)"