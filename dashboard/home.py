import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _shared import SHARED_CSS, nav

st.set_page_config(
    page_title="AirPulse — Real-Time AQI Intelligence",
    page_icon="🌬️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown(SHARED_CSS, unsafe_allow_html=True)
st.markdown("""
<style>
/* ── HOME-SPECIFIC ─── */
section[data-testid="stSidebar"] { display: none !important; }

.ap-hero {
    position: relative;
    padding: 6rem 2.5rem 5rem;
    overflow: hidden;
    background: var(--ink);
}
.ap-hero-orbs {
    position: absolute; inset: 0; z-index: 0; pointer-events: none;
}
.ap-hero-orbs::before {
    content: '';
    position: absolute; top: -80px; left: 50%; transform: translateX(-50%);
    width: 700px; height: 500px; border-radius: 50%;
    background: radial-gradient(ellipse, rgba(148,212,255,0.07) 0%, transparent 65%);
}
.ap-hero-orbs::after {
    content: '';
    position: absolute; bottom: -100px; right: 5%;
    width: 400px; height: 400px; border-radius: 50%;
    background: radial-gradient(ellipse, rgba(110,231,183,0.05) 0%, transparent 65%);
}
.ap-hero-grid {
    position: absolute; inset: 0; z-index: 0; pointer-events: none;
    background-image:
        linear-gradient(rgba(148,212,255,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(148,212,255,0.03) 1px, transparent 1px);
    background-size: 48px 48px;
    mask-image: radial-gradient(ellipse 80% 80% at 50% 0%, black, transparent);
}
.ap-hero-inner {
    position: relative; z-index: 1;
    max-width: 740px;
}
.ap-tag {
    display: inline-flex; align-items: center; gap: 8px;
    font-size: 0.72rem; font-weight: 700; letter-spacing: 0.1em;
    text-transform: uppercase; color: var(--sky);
    background: rgba(148,212,255,0.07);
    border: 1px solid rgba(148,212,255,0.18);
    padding: 0.32rem 0.85rem; border-radius: 20px;
    margin-bottom: 1.75rem;
}
.ap-tag::before {
    content: ''; width: 5px; height: 5px; border-radius: 50%;
    background: var(--sky);
    animation: live-blink 1.6s ease infinite;
}
.ap-hero h1 {
    font-size: clamp(2.6rem, 5vw, 4.2rem);
    font-weight: 900; line-height: 1.0;
    letter-spacing: -0.04em; color: #f0f6ff;
    margin-bottom: 1.5rem;
}
.ap-hero h1 .hl {
    background: linear-gradient(120deg, var(--sky) 0%, var(--mint) 60%, var(--sky) 100%);
    background-size: 200% auto;
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: shimmer 4s linear infinite;
}
@keyframes shimmer { to { background-position: 200% center; } }
.ap-hero p {
    font-size: 1.1rem; font-weight: 300; line-height: 1.8;
    color: var(--text2); max-width: 540px; margin-bottom: 2.5rem;
}
.ap-cta-row { display: flex; gap: 0.85rem; flex-wrap: wrap; }
.ap-cta-primary {
    display: inline-flex; align-items: center; gap: 8px;
    padding: 0.7rem 1.6rem; border-radius: 9px;
    font-size: 0.88rem; font-weight: 700; text-decoration: none;
    background: linear-gradient(135deg, var(--sky), var(--mint));
    color: var(--ink);
    box-shadow: 0 0 28px rgba(148,212,255,0.25);
    transition: all 0.22s; letter-spacing: 0.01em;
}
.ap-cta-primary:hover {
    box-shadow: 0 0 42px rgba(148,212,255,0.4);
    transform: translateY(-2px);
}
.ap-cta-ghost {
    display: inline-flex; align-items: center; gap: 8px;
    padding: 0.7rem 1.6rem; border-radius: 9px;
    font-size: 0.88rem; font-weight: 600; text-decoration: none;
    background: transparent; color: var(--text);
    border: 1px solid var(--wire);
    transition: all 0.22s;
}
.ap-cta-ghost:hover { background: var(--ink3); border-color: rgba(148,212,255,0.25); }

/* ── STAT BAND ─── */
.ap-stat-band {
    display: grid; grid-template-columns: repeat(4,1fr);
    border-top: 1px solid var(--wire);
    border-bottom: 1px solid var(--wire);
}
.ap-stat-cell {
    padding: 1.6rem 2.5rem;
    border-right: 1px solid var(--wire);
    background: var(--ink);
}
.ap-stat-cell:last-child { border-right: none; }
.ap-stat-num {
    font-size: 2.2rem; font-weight: 900;
    letter-spacing: -0.04em; color: var(--sky);
    font-family: 'Outfit', sans-serif;
    line-height: 1;
    margin-bottom: 4px;
}
.ap-stat-lbl {
    font-size: 0.75rem; font-weight: 500;
    color: var(--text3); letter-spacing: 0.04em;
    text-transform: uppercase;
}

/* ── SECTION ─── */
.ap-section { padding: 4.5rem 2.5rem; }
.ap-section-eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem; font-weight: 600;
    letter-spacing: 0.12em; text-transform: uppercase;
    color: var(--sky); margin-bottom: 0.7rem;
}
.ap-section-heading {
    font-size: clamp(1.7rem,3vw,2.5rem); font-weight: 800;
    letter-spacing: -0.03em; color: #f0f6ff; margin-bottom: 0.8rem;
    line-height: 1.15;
}
.ap-section-lead {
    font-size: 0.95rem; color: var(--text2); line-height: 1.75;
    max-width: 500px;
}

/* ── DASHBOARD GRID ─── */
.ap-dash-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px,1fr));
    gap: 1.25rem; margin-top: 2.5rem;
}
.ap-dash-tile {
    position: relative; overflow: hidden;
    background: var(--ink2);
    border: 1px solid var(--wire);
    border-radius: 14px; padding: 1.75rem;
    text-decoration: none;
    display: flex; flex-direction: column; gap: 0.9rem;
    transition: all 0.28s cubic-bezier(.22,1,.36,1);
}
.ap-dash-tile::before {
    content: ''; position: absolute;
    inset: 0; border-radius: 14px;
    background: linear-gradient(135deg, var(--tile-glow, rgba(148,212,255,0.04)) 0%, transparent 55%);
    transition: opacity 0.28s;
}
.ap-dash-tile:hover {
    border-color: var(--tile-color, var(--sky));
    box-shadow: 0 0 0 1px var(--tile-color, var(--sky)),
                0 12px 40px var(--tile-shadow, rgba(148,212,255,0.1));
    transform: translateY(-3px);
}
.ap-dash-tile:hover::before { opacity: 2; }
.ap-tile-badge {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem; font-weight: 600; letter-spacing: 0.1em;
    color: var(--tile-color, var(--sky));
    background: var(--tile-bg, rgba(148,212,255,0.08));
    border: 1px solid var(--tile-border, rgba(148,212,255,0.2));
    padding: 0.2rem 0.6rem; border-radius: 5px;
    display: inline-block; width: fit-content;
}
.ap-tile-icon {
    font-size: 1.6rem; line-height: 1;
}
.ap-tile-title {
    font-size: 1rem; font-weight: 700;
    color: #f0f6ff; letter-spacing: -0.01em;
}
.ap-tile-desc {
    font-size: 0.82rem; color: var(--text2); line-height: 1.6;
    flex: 1;
}
.ap-tile-cta {
    font-size: 0.78rem; font-weight: 600;
    color: var(--tile-color, var(--sky));
    display: flex; align-items: center; gap: 4px;
    margin-top: 0.25rem;
    transition: gap 0.2s;
}
.ap-dash-tile:hover .ap-tile-cta { gap: 8px; }

/* ── AQI REFERENCE TABLE ─── */
.ap-ref-wrap {
    margin-top: 2.5rem;
    border: 1px solid var(--wire);
    border-radius: 14px; overflow: hidden;
}
.ap-ref-table { width: 100%; border-collapse: collapse; }
.ap-ref-table thead { background: var(--ink3); }
.ap-ref-table th {
    padding: 0.8rem 1.25rem; text-align: left;
    font-size: 0.68rem; font-weight: 700;
    letter-spacing: 0.1em; text-transform: uppercase;
    color: var(--text3);
}
.ap-ref-table td {
    padding: 0.85rem 1.25rem;
    border-top: 1px solid var(--wire2);
    font-size: 0.86rem; color: #c8d8ec;
}
.ap-ref-table tbody tr { background: var(--ink2); transition: background 0.18s; }
.ap-ref-table tbody tr:hover { background: var(--ink3); }
.ap-aqi-range {
    font-family: 'JetBrains Mono', monospace;
    font-weight: 600; font-size: 0.88rem; color: #f0f6ff;
}
.ap-cat-pill {
    display: inline-flex; align-items: center; gap: 6px;
    padding: 0.25rem 0.75rem; border-radius: 20px;
    font-size: 0.76rem; font-weight: 700;
}

/* ── POLLUTANT GRID ─── */
.ap-poll-grid {
    display: grid; grid-template-columns: repeat(auto-fit, minmax(155px,1fr));
    gap: 1rem; margin-top: 2.5rem;
}
.ap-poll-tile {
    background: var(--ink2); border: 1px solid var(--wire);
    border-radius: 12px; padding: 1.4rem;
    text-align: center; transition: all 0.22s;
    position: relative; overflow: hidden;
}
.ap-poll-tile::before {
    content: attr(data-sym);
    position: absolute; bottom: -12px; right: -8px;
    font-size: 3.5rem; font-weight: 900; opacity: 0.04;
    color: var(--sky); font-family: 'JetBrains Mono', monospace;
    pointer-events: none;
}
.ap-poll-tile:hover {
    border-color: rgba(148,212,255,0.25);
    background: var(--ink3);
    transform: translateY(-3px);
}
.ap-poll-sym {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.35rem; font-weight: 700; color: var(--sky);
    margin-bottom: 0.45rem;
}
.ap-poll-name { font-size: 0.78rem; color: var(--text2); margin-bottom: 0.4rem; font-weight: 500; }
.ap-poll-info { font-size: 0.72rem; color: var(--text3); line-height: 1.55; }

/* ── STEPS ─── */
.ap-steps-list { margin-top: 2.5rem; display: flex; flex-direction: column; gap: 2px; }
.ap-step-row {
    display: flex; gap: 1.25rem; align-items: flex-start;
    background: var(--ink2); border: 1px solid var(--wire);
    padding: 1.4rem 1.6rem; transition: all 0.2s;
}
.ap-step-row:first-child { border-radius: 12px 12px 0 0; }
.ap-step-row:last-child  { border-radius: 0 0 12px 12px; }
.ap-step-row:hover { background: var(--ink3); border-color: rgba(148,212,255,0.2); z-index: 1; }
.ap-step-n {
    min-width: 36px; height: 36px; border-radius: 8px;
    background: rgba(148,212,255,0.08); border: 1px solid rgba(148,212,255,0.18);
    display: flex; align-items: center; justify-content: center;
    font-family: 'JetBrains Mono', monospace; font-weight: 700;
    color: var(--sky); font-size: 0.82rem;
}
.ap-step-t { font-weight: 600; color: #f0f6ff; margin-bottom: 3px; font-size: 0.9rem; }
.ap-step-d { font-size: 0.82rem; color: var(--text2); line-height: 1.6; }

/* ── ABOUT ─── */
.ap-about-card {
    background: var(--ink2); border: 1px solid var(--wire);
    border-radius: 16px; padding: 3rem;
    position: relative; overflow: hidden;
}
.ap-about-card::after {
    content: ''; position: absolute;
    top: -80px; right: -80px; width: 260px; height: 260px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(148,212,255,0.05) 0%, transparent 70%);
    pointer-events: none;
}
.ap-about-card h2 {
    font-size: 1.5rem; font-weight: 800; letter-spacing: -0.025em;
    color: #f0f6ff; margin-bottom: 0.9rem;
}
.ap-about-card p {
    font-size: 0.93rem; color: var(--text2); line-height: 1.85;
    max-width: 640px;
}

/* ── FOOTER ─── */
.ap-footer {
    display: flex; justify-content: space-between; align-items: center;
    padding: 1.5rem 2.5rem;
    border-top: 1px solid var(--wire);
    font-size: 0.76rem; color: var(--text3);
}
.ap-footer strong { color: var(--text2); }
.ap-footer-links { display: flex; gap: 1rem; }
.ap-footer-links a {
    color: var(--text3); text-decoration: none;
    transition: color 0.18s;
}
.ap-footer-links a:hover { color: var(--sky); }

/* ── SEP LINE ─── */
.ap-sep {
    height: 1px; background: var(--wire);
    margin: 0 2.5rem;
}
</style>
""", unsafe_allow_html=True)

# ── NAV
st.markdown(nav("home"), unsafe_allow_html=True)

# ── HERO
st.markdown("""
<section class="ap-hero">
    <div class="ap-hero-orbs"></div>
    <div class="ap-hero-grid"></div>
    <div class="ap-hero-inner">
        <div class="ap-tag rise">Real-Time Air Quality Intelligence</div>
        <h1 class="rise rise-1">
            Know your air.<br>
            <span class="hl">Protect your world.</span>
        </h1>
        <p class="rise rise-2">
            AirPulse tracks, forecasts, and alerts you on air quality across cities.
            Six pollutants. Four dashboards. One clear picture of what you breathe.
        </p>
        <div class="ap-cta-row rise rise-3">
            <a href="/Alert_System" class="ap-cta-primary">🚨 Live Alerts</a>
            <a href="/Data_Explorer" class="ap-cta-ghost">📊 Explore Data →</a>
            <a href="/Forecast_Engine" class="ap-cta-ghost">📈 Forecast →</a>
        </div>
    </div>
</section>
""", unsafe_allow_html=True)

# ── STAT BAND
st.markdown("""
<div class="ap-stat-band">
    <div class="ap-stat-cell">
        <div class="ap-stat-num">5+</div>
        <div class="ap-stat-lbl">Cities Monitored</div>
    </div>
    <div class="ap-stat-cell">
        <div class="ap-stat-num">6</div>
        <div class="ap-stat-lbl">Pollutants Tracked</div>
    </div>
    <div class="ap-stat-cell">
        <div class="ap-stat-num">72h</div>
        <div class="ap-stat-lbl">Forecast Horizon</div>
    </div>
    <div class="ap-stat-cell">
        <div class="ap-stat-num">5</div>
        <div class="ap-stat-lbl">ML Models</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── DASHBOARDS
st.markdown("""
<section class="ap-section">
    <div class="ap-section-eyebrow">// platform</div>
    <div class="ap-section-heading">Four dashboards.<br>One system.</div>
    <p class="ap-section-lead">Each module is purpose-built — from raw data to ML forecasts to live alerts and model retraining.</p>

    <div class="ap-dash-grid">

        <a href="/Data_Explorer" class="ap-dash-tile"
            style="--tile-color:#94d4ff;--tile-bg:rgba(148,212,255,0.07);--tile-border:rgba(148,212,255,0.18);--tile-glow:rgba(148,212,255,0.06);--tile-shadow:rgba(148,212,255,0.12);">
            <div class="ap-tile-badge">D1 · DATA</div>
            <div class="ap-tile-icon">📊</div>
            <div class="ap-tile-title">Data Explorer</div>
            <div class="ap-tile-desc">Time series, correlation heatmaps, distributions and multi-city statistical comparisons.</div>
            <div class="ap-tile-cta">Open → </div>
        </a>

        <a href="/Forecast_Engine" class="ap-dash-tile"
            style="--tile-color:#c4b5fd;--tile-bg:rgba(196,181,253,0.07);--tile-border:rgba(196,181,253,0.18);--tile-glow:rgba(196,181,253,0.06);--tile-shadow:rgba(196,181,253,0.12);">
            <div class="ap-tile-badge">D2 · FORECAST</div>
            <div class="ap-tile-icon">📈</div>
            <div class="ap-tile-title">Forecast Engine</div>
            <div class="ap-tile-desc">ARIMA, Prophet & LSTM forecasts with confidence intervals up to 72 hours ahead.</div>
            <div class="ap-tile-cta">Open → </div>
        </a>

        <a href="/Alert_System" class="ap-dash-tile"
            style="--tile-color:#fda4af;--tile-bg:rgba(253,164,175,0.07);--tile-border:rgba(253,164,175,0.18);--tile-glow:rgba(253,164,175,0.06);--tile-shadow:rgba(253,164,175,0.12);">
            <div class="ap-tile-badge">D3 · ALERTS</div>
            <div class="ap-tile-icon">🚨</div>
            <div class="ap-tile-title">Alert System</div>
            <div class="ap-tile-desc">AQI gauge, 7-day trend table, pollutant concentration chart and health alert cards.</div>
            <div class="ap-tile-cta">Open → </div>
        </a>

        <a href="/Admin_Dashboard" class="ap-dash-tile"
            style="--tile-color:#6ee7b7;--tile-bg:rgba(110,231,183,0.07);--tile-border:rgba(110,231,183,0.18);--tile-glow:rgba(110,231,183,0.06);--tile-shadow:rgba(110,231,183,0.12);">
            <div class="ap-tile-badge">D4 · ADMIN</div>
            <div class="ap-tile-icon">🧠</div>
            <div class="ap-tile-title">Admin Panel</div>
            <div class="ap-tile-desc">Upload datasets, retrain XGBoost / RF / Prophet / ARIMA / LSTM and compare RMSE.</div>
            <div class="ap-tile-cta">Open → </div>
        </a>

    </div>
</section>
""", unsafe_allow_html=True)

st.markdown('<div class="ap-sep"></div>', unsafe_allow_html=True)

# ── AQI REFERENCE
st.markdown("""
<section class="ap-section">
    <div class="ap-section-eyebrow">// reference</div>
    <div class="ap-section-heading">AQI scale & health guide</div>
    <p class="ap-section-lead">Six bands with color-coded health implications and recommended protective actions.</p>

    <div class="ap-ref-wrap">
        <table class="ap-ref-table">
            <thead>
                <tr>
                    <th>AQI Range</th>
                    <th>Category</th>
                    <th>Health Implication</th>
                    <th>Recommended Action</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><span class="ap-aqi-range">0 – 50</span></td>
                    <td><span class="ap-cat-pill" style="background:rgba(74,222,128,0.1);color:#4ade80;border:1px solid rgba(74,222,128,0.22);">● Good</span></td>
                    <td>Satisfactory, minimal health risk</td>
                    <td>Normal outdoor activity</td>
                </tr>
                <tr>
                    <td><span class="ap-aqi-range">51 – 100</span></td>
                    <td><span class="ap-cat-pill" style="background:rgba(252,211,77,0.1);color:#fcd34d;border:1px solid rgba(252,211,77,0.22);">● Moderate</span></td>
                    <td>Acceptable; sensitive individuals may be affected</td>
                    <td>Limit prolonged exertion if unusually sensitive</td>
                </tr>
                <tr>
                    <td><span class="ap-aqi-range">101 – 150</span></td>
                    <td><span class="ap-cat-pill" style="background:rgba(251,146,60,0.1);color:#fb923c;border:1px solid rgba(251,146,60,0.22);">● Sensitive Groups</span></td>
                    <td>Children, elderly, asthma sufferers at risk</td>
                    <td>Reduce outdoor exposure for sensitive groups</td>
                </tr>
                <tr>
                    <td><span class="ap-aqi-range">151 – 200</span></td>
                    <td><span class="ap-cat-pill" style="background:rgba(253,164,175,0.1);color:#fda4af;border:1px solid rgba(253,164,175,0.22);">● Unhealthy</span></td>
                    <td>Everyone may experience health effects</td>
                    <td>Limit outdoor activity; wear N95 masks</td>
                </tr>
                <tr>
                    <td><span class="ap-aqi-range">201 – 300</span></td>
                    <td><span class="ap-cat-pill" style="background:rgba(196,181,253,0.1);color:#c4b5fd;border:1px solid rgba(196,181,253,0.22);">● Very Unhealthy</span></td>
                    <td>Health alert — serious effects for everyone</td>
                    <td>Avoid outdoor activity; use air purifiers</td>
                </tr>
                <tr>
                    <td><span class="ap-aqi-range">301+</span></td>
                    <td><span class="ap-cat-pill" style="background:rgba(239,68,68,0.1);color:#ef4444;border:1px solid rgba(239,68,68,0.25);">● Hazardous</span></td>
                    <td>Emergency conditions; everyone at risk</td>
                    <td>Stay indoors, seal windows, seek medical help</td>
                </tr>
            </tbody>
        </table>
    </div>
</section>
""", unsafe_allow_html=True)

st.markdown('<div class="ap-sep"></div>', unsafe_allow_html=True)

# ── POLLUTANTS
st.markdown("""
<section class="ap-section">
    <div class="ap-section-eyebrow">// monitored pollutants</div>
    <div class="ap-section-heading">What we track</div>
    <p class="ap-section-lead">Six key pollutants continuously measured across all monitored cities.</p>

    <div class="ap-poll-grid">
        <div class="ap-poll-tile" data-sym="PM">
            <div class="ap-poll-sym">PM2.5</div>
            <div class="ap-poll-name">Fine Particles</div>
            <div class="ap-poll-info">Sub-2.5µm; penetrates deep lung tissue causing systemic harm</div>
        </div>
        <div class="ap-poll-tile" data-sym="PM">
            <div class="ap-poll-sym">PM10</div>
            <div class="ap-poll-name">Coarse Particles</div>
            <div class="ap-poll-info">Up to 10µm; irritates respiratory tract, aggravates asthma</div>
        </div>
        <div class="ap-poll-tile" data-sym="N">
            <div class="ap-poll-sym">NO₂</div>
            <div class="ap-poll-name">Nitrogen Dioxide</div>
            <div class="ap-poll-info">Mainly from vehicles; inflames airways and reduces lung function</div>
        </div>
        <div class="ap-poll-tile" data-sym="S">
            <div class="ap-poll-sym">SO₂</div>
            <div class="ap-poll-name">Sulfur Dioxide</div>
            <div class="ap-poll-info">Industrial emissions; causes eye and throat irritation</div>
        </div>
        <div class="ap-poll-tile" data-sym="C">
            <div class="ap-poll-sym">CO</div>
            <div class="ap-poll-name">Carbon Monoxide</div>
            <div class="ap-poll-info">Odorless gas; reduces oxygen delivery to organs</div>
        </div>
        <div class="ap-poll-tile" data-sym="O">
            <div class="ap-poll-sym">O₃</div>
            <div class="ap-poll-name">Ground Ozone</div>
            <div class="ap-poll-info">Formed in sunlight; triggers asthma and lung inflammation</div>
        </div>
    </div>
</section>
""", unsafe_allow_html=True)

st.markdown('<div class="ap-sep"></div>', unsafe_allow_html=True)

# ── HOW IT WORKS
st.markdown("""
<section class="ap-section">
    <div class="ap-section-eyebrow">// methodology</div>
    <div class="ap-section-heading">How AQI is calculated</div>
    <div class="ap-steps-list">
        <div class="ap-step-row">
            <div class="ap-step-n">01</div>
            <div>
                <div class="ap-step-t">Monitor Pollutants</div>
                <div class="ap-step-d">Stations continuously measure concentrations of PM2.5, PM10, NO₂, SO₂, CO, and O₃.</div>
            </div>
        </div>
        <div class="ap-step-row">
            <div class="ap-step-n">02</div>
            <div>
                <div class="ap-step-t">Convert to Sub-Index</div>
                <div class="ap-step-d">Each pollutant concentration maps to a sub-index via standardized regulatory formulas.</div>
            </div>
        </div>
        <div class="ap-step-row">
            <div class="ap-step-n">03</div>
            <div>
                <div class="ap-step-t">Take the Maximum</div>
                <div class="ap-step-d">The highest sub-index becomes the overall AQI — representing the worst present hazard.</div>
            </div>
        </div>
        <div class="ap-step-row">
            <div class="ap-step-n">04</div>
            <div>
                <div class="ap-step-t">Categorize & Alert</div>
                <div class="ap-step-d">AQI maps to a color band and health category, triggering advisories when thresholds are crossed.</div>
            </div>
        </div>
    </div>
</section>
""", unsafe_allow_html=True)

st.markdown('<div class="ap-sep"></div>', unsafe_allow_html=True)

# ── ABOUT
st.markdown("""
<section class="ap-section">
    <div class="ap-about-card">
        <div class="ap-section-eyebrow">// about</div>
        <h2>Built by Sumit</h2>
        <p>
            A frontend developer driven by data, design, and environmental sustainability.
            AirPulse bridges the gap between sensor data and real-world decisions —
            clean interfaces, accurate forecasts, and timely alerts so anyone can act
            on the quality of the air they breathe.
        </p>
    </div>
</section>
""", unsafe_allow_html=True)

# ── FOOTER
st.markdown("""
<footer class="ap-footer">
    <div>© 2025 <strong>AirPulse</strong> · Built by Sumit</div>
    <div class="ap-footer-links">
        <a href="/Data_Explorer">Data Explorer</a>
        <a href="/Forecast_Engine">Forecast</a>
        <a href="/Alert_System">Alerts</a>
        <a href="/Admin_Dashboard">Admin</a>
    </div>
    <div>5 cities · 6 pollutants · Updated hourly</div>
</footer>
""", unsafe_allow_html=True)