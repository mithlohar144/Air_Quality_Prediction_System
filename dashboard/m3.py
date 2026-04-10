import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import random
import os

st.set_page_config(page_title="D3 · Alert System — AirPulse", layout="wide", page_icon="🚨", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');
*{box-sizing:border-box;}
:root{--bg:#050b18;--surface:#0c1628;--surface2:#111f38;--border:rgba(99,179,237,0.12);--accent:#f87171;--text:#e2e8f0;--muted:#64748b;}
html,body,[data-testid="stAppViewContainer"],[data-testid="stApp"]{background:var(--bg) !important;font-family:'DM Sans',sans-serif;color:var(--text);}
[data-testid="stHeader"],footer,#MainMenu{display:none !important;}
.block-container{padding:0 !important;max-width:100% !important;}
[data-testid="stSidebar"]{background:var(--surface) !important;border-right:1px solid var(--border);}
[data-testid="stSidebar"] *{color:var(--text) !important;}
[data-testid="stSelectbox"] div[data-baseweb="select"] > div{background:var(--surface2) !important;border-color:var(--border) !important;color:var(--text) !important;}
div[data-testid="metric-container"]{background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:1rem 1.25rem;}
div[data-testid="metric-container"] label{color:var(--muted) !important;font-size:0.75rem;}
div[data-testid="metric-container"] div[data-testid="stMetricValue"]{color:var(--accent) !important;font-family:'Syne',sans-serif;}
.ap-nav{display:flex;align-items:center;justify-content:space-between;padding:0 2rem;height:60px;background:rgba(5,11,24,0.9);backdrop-filter:blur(16px);border-bottom:1px solid var(--border);}
.ap-logo{font-family:'Syne',sans-serif;font-size:1.2rem;font-weight:800;color:#f87171;}
.ap-logo span{color:var(--text);}
.ap-nav-right{display:flex;align-items:center;gap:0.6rem;}
.ap-nav-links{display:flex;gap:0.2rem;}
.ap-nav-links a{font-size:0.85rem;font-weight:500;color:var(--muted);text-decoration:none;padding:0.35rem 0.8rem;border-radius:8px;transition:all 0.2s;}
.ap-nav-links a:hover{color:var(--text);background:var(--surface2);}
.ap-nav-links a.active{color:#f87171;background:rgba(248,113,113,0.1);}
.ap-sidebar-toggle{padding:0.35rem 0.9rem;border-radius:8px;border:1px solid var(--border);background:var(--surface2);color:var(--text);font-size:0.8rem;font-weight:500;cursor:pointer;}
.ap-sidebar-toggle:hover{background:var(--surface);}
.ap-page-header{padding:2rem 2rem 1.5rem;border-bottom:1px solid var(--border);}
.ap-page-title{font-family:'Syne',sans-serif;font-size:1.8rem;font-weight:800;color:#f1f5f9;letter-spacing:-0.02em;}
.ap-page-sub{font-size:0.9rem;color:var(--muted);margin-top:0.25rem;}
.ap-card{background:var(--surface);border:1px solid var(--border);border-radius:14px;padding:1.5rem;margin-bottom:1rem;}
.ap-card-title{font-family:'Syne',sans-serif;font-size:0.95rem;font-weight:700;color:#f1f5f9;margin-bottom:1rem;}
.alert-card{border-radius:12px;padding:1rem 1.25rem;margin-bottom:0.75rem;display:flex;align-items:flex-start;gap:12px;}
.alert-icon{font-size:1.2rem;margin-top:1px;}
.alert-title{font-weight:700;font-size:0.95rem;margin-bottom:2px;}
.alert-desc{font-size:0.82rem;opacity:0.8;}
.aqi-band{display:inline-flex;align-items:center;gap:8px;padding:0.5rem 1.2rem;border-radius:25px;font-family:'Syne',sans-serif;font-weight:800;font-size:1.1rem;border:1px solid;}
.trend-row{display:flex;align-items:center;justify-content:space-between;padding:0.6rem 0;border-bottom:1px solid rgba(99,179,237,0.06);}
.trend-date{font-size:0.82rem;color:#64748b;}
.trend-aqi{font-family:'Syne',sans-serif;font-weight:700;font-size:0.95rem;}
.trend-cat{font-size:0.78rem;padding:0.2rem 0.6rem;border-radius:10px;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<nav class="ap-nav">
    <div class="ap-logo">🌬️ <span>Air</span>Pulse</div>
    <div class="ap-nav-right">
        <div class="ap-nav-links">
            <a href="https://dashboard1air.streamlit.app/">D1 · Data Explorer</a>
            <a href="https://forecastair.streamlit.app/">D2 · Forecast</a>
            <a href="https://alertsair.streamlit.app/" class="active">D3 · Alerts</a>
            <a href="https://admirairr.streamlit.app/">D4 · Admin</a>
        </div>
        <button class="ap-sidebar-toggle" onclick="const btn = document.querySelector('[data-testid=&quot;stSidebarCollapseButton&quot;]'); if(btn){btn.click();}">Filters</button>
    </div>
</nav>
<div class="ap-page-header">
    <div class="ap-page-title">🚨 D3 · Alert System</div>
    <div class="ap-page-sub">Real-time AQI gauge, 7-day trends, pollutant concentrations and health alerts</div>
</div>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    DATA_PATH = "data/air_quality_data.csv"
    if not os.path.exists(DATA_PATH):
        os.makedirs("data", exist_ok=True)
        cities = ["Delhi", "Mumbai", "Chennai", "Kolkata", "Bangalore"]
        dates = pd.date_range("2024-01-01", periods=2000, freq="H")
        df_s = pd.DataFrame({
            "City": np.random.choice(cities, len(dates)),
            "Datetime": dates,
            "PM2.5": np.random.randint(20, 160, len(dates)),
            "PM10": np.random.randint(30, 200, len(dates)),
            "NO2": np.random.randint(10, 80, len(dates)),
            "O3": np.random.randint(10, 60, len(dates)),
            "SO2": np.random.randint(2, 40, len(dates)),
        })
        df_s.to_csv(DATA_PATH, index=False)
    df = pd.read_csv(DATA_PATH)
    for col in ["Datetime", "Date"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    return df


df = load_data()

required_cols = {"City", "PM2.5", "PM10", "O3"}
if not required_cols.issubset(df.columns):
    st.error("❌ Required columns missing: City, PM2.5, PM10, O3")
    st.stop()

cities = sorted(df["City"].unique())
city = st.sidebar.selectbox("🏙️ City", cities)

st.sidebar.markdown("### 🎚️ AQI Range Filter")
aqi_min_s = 0
aqi_max_s = 400
aqi_range = st.sidebar.slider("AQI Range", min_value=0, max_value=400, value=(0, 400))

city_data = df[df["City"] == city].copy()
date_col = "Datetime" if "Datetime" in city_data.columns else ("Date" if "Date" in city_data.columns else None)
if date_col:
    city_data = city_data.sort_values(date_col)

latest_row = city_data.iloc[-1]
raw_aqi = int((latest_row["PM2.5"] * 0.5) + (latest_row["PM10"] * 0.3) + (latest_row["O3"] * 0.2))
avg_aqi = max(aqi_range[0], min(raw_aqi, aqi_range[1]))


def aqi_band(aqi):
    if aqi <= 50:   return "Good", "#4ade80", "rgba(74,222,128,0.1)", "rgba(74,222,128,0.25)"
    if aqi <= 100:  return "Moderate", "#facc15", "rgba(250,204,21,0.1)", "rgba(250,204,21,0.25)"
    if aqi <= 150:  return "Sensitive Groups", "#fb923c", "rgba(251,146,60,0.1)", "rgba(251,146,60,0.25)"
    if aqi <= 200:  return "Unhealthy", "#f87171", "rgba(248,113,113,0.1)", "rgba(248,113,113,0.25)"
    if aqi <= 300:  return "Very Unhealthy", "#a78bfa", "rgba(167,139,250,0.1)", "rgba(167,139,250,0.25)"
    return "Hazardous", "#ef4444", "rgba(239,68,68,0.15)", "rgba(239,68,68,0.3)"


cat, color, bg, border = aqi_band(avg_aqi)

st.markdown("<div style='padding:1.5rem 2rem 0'>", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Current AQI", avg_aqi)
c2.metric("Category", cat)
c3.metric("PM2.5", f"{latest_row['PM2.5']:.0f} µg/m³")
c4.metric("PM10", f"{latest_row['PM10']:.0f} µg/m³")

st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

col1, col2 = st.columns([1.2, 1])

with col1:
    st.markdown(f"<div class='ap-card'><div class='ap-card-title'>🎯 AQI Gauge — {city}</div>", unsafe_allow_html=True)

    labels = ["Good\n0–50", "Moderate\n51–100", "Sensitive\n101–150", "Unhealthy\n151–200", "Very Bad\n201–300", "Hazardous\n301+"]
    values = [50, 50, 50, 50, 100, 100]
    gauge_colors = ['#4ade80', '#facc15', '#fb923c', '#f87171', '#a78bfa', '#ef4444']

    fig_gauge = go.Figure()
    fig_gauge.add_trace(go.Pie(
        labels=labels, values=values, hole=0.65,
        marker=dict(colors=gauge_colors, line=dict(color='#050b18', width=3)),
        textinfo='none', sort=False, direction="clockwise",
        hovertemplate="<b>%{label}</b><extra></extra>"
    ))
    fig_gauge.add_annotation(
        x=0.5, y=0.48,
        text=f"<b style='font-size:42px'>{avg_aqi}</b>",
        font=dict(size=42, color=color, family="Syne"),
        showarrow=False
    )
    fig_gauge.add_annotation(
        x=0.5, y=0.35,
        text=f"<span style='font-size:13px'>{cat}</span>",
        font=dict(size=13, color="#94a3b8"),
        showarrow=False
    )
    fig_gauge.update_layout(
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5,
                    font=dict(color="#94a3b8", size=10)),
        margin=dict(l=20, r=20, t=20, b=20),
        height=340,
        paper_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig_gauge, use_container_width=True)
    st.markdown(f"""
    <div style='text-align:center;margin-top:0.5rem;'>
        <span class='aqi-band' style='background:{bg};color:{color};border-color:{border};'>
            ● {cat}
        </span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown(f"<div class='ap-card'><div class='ap-card-title'>📅 7-Day AQI Trend</div>", unsafe_allow_html=True)

    if date_col and date_col in city_data.columns:
        last_week = city_data.tail(7)
        dates_list = last_week[date_col].dt.strftime("%a %d %b").tolist()
        aqi_values = (last_week["PM2.5"] * 0.5 + last_week["PM10"] * 0.3 + last_week["O3"] * 0.2).astype(int).tolist()
    else:
        base = avg_aqi
        aqi_values = [max(0, min(400, base + random.randint(-15, 15))) for _ in range(7)]
        dates_list = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    for d, v in zip(dates_list, aqi_values):
        b_cat, b_color, b_bg, b_border = aqi_band(v)
        st.markdown(f"""
        <div class='trend-row'>
            <span class='trend-date'>{d}</span>
            <span class='trend-aqi' style='color:{b_color};'>{v}</span>
            <span class='trend-cat' style='background:{b_bg};color:{b_color};border:1px solid {b_border};'>{b_cat}</span>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Health tips based on AQI
    tips = {
        "Good": ("✅", "Air quality is excellent", "Enjoy outdoor activities freely."),
        "Moderate": ("⚠️", "Acceptable quality", "Unusually sensitive individuals should consider reducing prolonged exertion outdoors."),
        "Sensitive Groups": ("🟠", "Sensitive groups at risk", "Children, elderly and those with respiratory conditions should limit outdoor exertion."),
        "Unhealthy": ("🔴", "Unhealthy for everyone", "Everyone should reduce outdoor activity. Wear N95 masks when outdoors."),
        "Very Unhealthy": ("🟣", "Serious health risk", "Avoid outdoor activities. Use air purifiers indoors."),
        "Hazardous": ("☠️", "Emergency conditions", "Stay indoors. Seal windows. Seek medical attention if experiencing symptoms."),
    }
    icon, title, desc = tips.get(cat, ("ℹ️", "Check AQI", ""))
    tip_color = color
    st.markdown(f"""
    <div class='ap-card' style='border-color:{border};background:rgba(5,11,24,0.5);'>
        <div style='display:flex;gap:10px;align-items:flex-start;'>
            <span style='font-size:1.3rem;'>{icon}</span>
            <div>
                <div style='font-weight:700;color:{tip_color};font-size:0.9rem;margin-bottom:4px;'>{title}</div>
                <div style='font-size:0.82rem;color:#94a3b8;line-height:1.5;'>{desc}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Pollutant chart
st.markdown("<div class='ap-card'><div class='ap-card-title'>📊 Pollutant Concentrations Over Time</div>", unsafe_allow_html=True)

if date_col:
    x_axis = city_data[date_col].astype(str).tolist()
else:
    x_axis = list(range(len(city_data)))

fig = go.Figure()
poll_colors = {"PM2.5": "#38bdf8", "PM10": "#818cf8", "O3": "#34d399"}
for poll, c in poll_colors.items():
    if poll in city_data.columns:
        fig.add_trace(go.Scatter(
            x=x_axis, y=city_data[poll], mode='lines',
            name=poll, line=dict(width=1.5, color=c),
        ))

fig.add_hline(y=60, line_dash="dash", line_color="rgba(248,113,113,0.5)",
              annotation_text="WHO Limit", annotation_font_color="#f87171",
              annotation_font_size=11)
fig.update_layout(
    template="plotly_white", height=280,
    margin=dict(l=10, r=10, t=10, b=10),
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(color="#64748b", showgrid=False),
    yaxis=dict(showgrid=True, gridcolor="rgba(99,179,237,0.08)", color="#64748b", title="µg/m³"),
    font=dict(family="DM Sans", color="#94a3b8"),
    legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5, font=dict(color="#94a3b8")),
)
st.plotly_chart(fig, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# ── Alerts
st.markdown("<div class='ap-card'><div class='ap-card-title'>🚨 Active Alerts</div>", unsafe_allow_html=True)

alerts = []
if avg_aqi > 150:
    alerts.append(("🔴", "Unhealthy Air Quality", "PM2.5 levels exceed safe limits. Sensitive groups should stay indoors.", "#f87171", "rgba(248,113,113,0.1)", "rgba(248,113,113,0.2)"))
if avg_aqi > 200:
    alerts.append(("🟣", "Very Unhealthy Conditions", "AQI exceeds 200. Health alert for all population groups.", "#a78bfa", "rgba(167,139,250,0.1)", "rgba(167,139,250,0.2)"))
if "PM10" in latest_row and latest_row["PM10"] > 100:
    alerts.append(("🟠", "High PM10 Levels", f"Dust/smoke PM10 at {latest_row['PM10']:.0f} µg/m³ — above recommended threshold.", "#fb923c", "rgba(251,146,60,0.1)", "rgba(251,146,60,0.2)"))
if "O3" in latest_row and latest_row["O3"] > 80:
    alerts.append(("⚡", "Ozone Alert", f"Ground-level ozone at {latest_row['O3']:.0f} µg/m³. May trigger respiratory issues.", "#fbbf24", "rgba(251,191,36,0.1)", "rgba(251,191,36,0.2)"))

if not alerts:
    st.markdown("""
    <div style='display:flex;align-items:center;gap:10px;padding:1rem;background:rgba(74,222,128,0.06);border:1px solid rgba(74,222,128,0.2);border-radius:10px;'>
        <span style='font-size:1.2rem;'>✅</span>
        <span style='color:#4ade80;font-weight:600;'>No active alerts — air quality is within safe limits.</span>
    </div>
    """, unsafe_allow_html=True)
else:
    for icon, title, desc, c, bg, brd in alerts:
        st.markdown(f"""
        <div class='alert-card' style='background:{bg};border:1px solid {brd};'>
            <span class='alert-icon'>{icon}</span>
            <div>
                <div class='alert-title' style='color:{c};'>{title}</div>
                <div class='alert-desc' style='color:#94a3b8;'>{desc}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("</div></div>", unsafe_allow_html=True)