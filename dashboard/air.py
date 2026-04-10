import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="D1 · Data Explorer — AirPulse", layout="wide", page_icon="📊")

# ── Shared dark-theme CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');
*{box-sizing:border-box;}
:root{
    --bg:#050b18;--surface:#0c1628;--surface2:#111f38;
    --border:rgba(99,179,237,0.12);--accent:#38bdf8;--accent2:#818cf8;
    --text:#e2e8f0;--muted:#64748b;
}
html,body,[data-testid="stAppViewContainer"],[data-testid="stApp"]{
    background:var(--bg) !important;
    font-family:'DM Sans',sans-serif; color:var(--text);
}
[data-testid="stHeader"],footer,#MainMenu{display:none !important;}
.block-container{padding:0 !important; max-width:100% !important;}
[data-testid="stSidebar"]{background:var(--surface) !important; border-right:1px solid var(--border);}
[data-testid="stSidebar"] *{color:var(--text) !important;}
.stSelectbox>div>div, .stRadio>div, .stSlider{color:var(--text);}
[data-testid="stSelectbox"] div[data-baseweb="select"] > div,
[data-testid="stTextInput"] input{
    background:var(--surface2) !important; border-color:var(--border) !important; color:var(--text) !important;
}
div[data-testid="metric-container"]{
    background:var(--surface); border:1px solid var(--border);
    border-radius:12px; padding:1rem 1.25rem;
}
div[data-testid="metric-container"] label{color:var(--muted) !important; font-size:0.75rem;}
div[data-testid="metric-container"] div[data-testid="stMetricValue"]{color:var(--accent) !important; font-family:'Syne',sans-serif;}
.ap-nav{
    display:flex; align-items:center; justify-content:space-between;
    padding:0 2rem; height:60px;
    background:rgba(5,11,24,0.9); backdrop-filter:blur(16px);
    border-bottom:1px solid var(--border);
}
.ap-logo{font-family:'Syne',sans-serif;font-size:1.2rem;font-weight:800;color:var(--accent);}
.ap-logo span{color:var(--text);}
.ap-nav-right{display:flex;align-items:center;gap:0.6rem;}
.ap-nav-links{display:flex;gap:0.2rem;}
.ap-nav-links a{font-size:0.85rem;font-weight:500;color:var(--muted);text-decoration:none;padding:0.35rem 0.8rem;border-radius:8px;transition:all 0.2s;}
.ap-nav-links a:hover{color:var(--text);background:var(--surface2);}
.ap-nav-links a.active{color:var(--accent);background:rgba(56,189,248,0.08);}
.ap-sidebar-toggle{padding:0.35rem 0.9rem;border-radius:8px;border:1px solid var(--border);background:var(--surface2);color:var(--text);font-size:0.8rem;font-weight:500;cursor:pointer;}
.ap-sidebar-toggle:hover{background:var(--surface);}
.ap-page-header{padding:2rem 2rem 1.5rem;border-bottom:1px solid var(--border);}
.ap-page-title{font-family:'Syne',sans-serif;font-size:1.8rem;font-weight:800;color:#f1f5f9;letter-spacing:-0.02em;}
.ap-page-sub{font-size:0.9rem;color:var(--muted);margin-top:0.25rem;}
.ap-card{background:var(--surface);border:1px solid var(--border);border-radius:14px;padding:1.5rem;margin-bottom:1rem;}
.ap-card-title{font-family:'Syne',sans-serif;font-size:0.95rem;font-weight:700;color:#f1f5f9;margin-bottom:1rem;letter-spacing:0.01em;}
.stPlotlyChart{border-radius:10px;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<nav class="ap-nav">
    <div class="ap-logo">🌬️ <span>Air</span>Pulse</div>
    <div class="ap-nav-right">
        <div class="ap-nav-links">
            <a href="https://dashboard1air.streamlit.app/" class="active">D1 · Data Explorer</a>
            <a href="https://forecastair.streamlit.app/">D2 · Forecast</a>
            <a href="https://alertsair.streamlit.app/">D3 · Alerts</a>
            <a href="https://admirairr.streamlit.app/">D4 · Admin</a>
        </div>
        <button class="ap-sidebar-toggle" onclick="const btn = document.querySelector('[data-testid=&quot;stSidebarCollapseButton&quot;]'); if(btn){btn.click();}">Filters</button>
    </div>
</nav>
<div class="ap-page-header">
    <div class="ap-page-title">📊 D1 · Data Explorer</div>
    <div class="ap-page-sub">Time series, correlations, distributions & statistics across cities and pollutants</div>
</div>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    DATA_PATH = "data/air_quality_data.csv"
    if not os.path.exists(DATA_PATH):
        os.makedirs("data", exist_ok=True)
        cities = ["Delhi", "Mumbai", "Chennai", "Kolkata", "Bangalore"]
        dates = pd.date_range("2024-01-01", periods=2000, freq="H")
        df_sample = pd.DataFrame({
            "City": np.random.choice(cities, len(dates)),
            "Datetime": dates,
            "PM2.5": np.random.randint(20, 160, len(dates)),
            "PM10": np.random.randint(30, 200, len(dates)),
            "NO2": np.random.randint(10, 80, len(dates)),
            "O3": np.random.randint(10, 60, len(dates)),
            "SO2": np.random.randint(2, 40, len(dates)),
        })
        df_sample.to_csv(DATA_PATH, index=False)
    df = pd.read_csv(DATA_PATH)
    df['Datetime'] = pd.to_datetime(df['Datetime'])
    df = df[df['Datetime'] > (df['Datetime'].max() - pd.DateOffset(years=1))]
    return df


df = load_data()
POLL_COLS = ["PM2.5", "PM10", "NO2", "O3", "SO2"]

# ── Sidebar
st.sidebar.markdown("### ⚙️ Controls")
city = st.sidebar.selectbox("City", sorted(df["City"].unique()))
pollutant = st.sidebar.radio("Pollutant", POLL_COLS)
time_range = st.sidebar.selectbox("Time Range", ["Last 7 Days", "Last 30 Days", "Last 90 Days", "All Data"])

city_data = df[df["City"] == city].sort_values("Datetime")

# Apply time filter
cutoff_map = {"Last 7 Days": 7, "Last 30 Days": 30, "Last 90 Days": 90}
if time_range in cutoff_map:
    cutoff = city_data["Datetime"].max() - pd.Timedelta(days=cutoff_map[time_range])
    city_data = city_data[city_data["Datetime"] >= cutoff]

st.markdown("<div style='padding:1.5rem 2rem 0'>", unsafe_allow_html=True)

# ── Metrics row
c1, c2, c3, c4, c5, c6 = st.columns(6)
stats = city_data[pollutant].describe()
c1.metric("Mean", f"{stats['mean']:.1f}")
c2.metric("Median", f"{city_data[pollutant].median():.1f}")
c3.metric("Max", f"{stats['max']:.1f}")
c4.metric("Min", f"{stats['min']:.1f}")
c5.metric("Std Dev", f"{stats['std']:.1f}")
c6.metric("Data Points", f"{len(city_data):,}")

st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

# ── Row 1
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"<div class='ap-card'><div class='ap-card-title'>📈 {pollutant} Time Series — {city}</div>", unsafe_allow_html=True)
    fig = px.line(city_data, x="Datetime", y=pollutant, color_discrete_sequence=["#38bdf8"])
    fig.update_traces(line=dict(width=1.5))
    fig.update_layout(
        height=280, margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=True, gridcolor="rgba(99,179,237,0.08)", color="#64748b"),
        yaxis=dict(showgrid=True, gridcolor="rgba(99,179,237,0.08)", color="#64748b"),
        font=dict(family="DM Sans", color="#94a3b8"),
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='ap-card'><div class='ap-card-title'>🔗 Pollutant Correlation Heatmap</div>", unsafe_allow_html=True)
    corr = df[POLL_COLS].corr()
    fig2, ax = plt.subplots(figsize=(5, 3.2))
    fig2.patch.set_facecolor('#0c1628')
    ax.set_facecolor('#0c1628')
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="Blues",
                ax=ax, linewidths=0.5, linecolor='#111f38',
                annot_kws={"size": 9, "color": "white"},
                cbar_kws={"shrink": 0.8})
    ax.tick_params(colors='#94a3b8', labelsize=9)
    plt.tight_layout()
    st.pyplot(fig2)
    plt.close()
    st.markdown("</div>", unsafe_allow_html=True)

# ── Row 2
col3, col4 = st.columns(2)

with col3:
    st.markdown(f"<div class='ap-card'><div class='ap-card-title'>📉 {pollutant} Distribution</div>", unsafe_allow_html=True)
    fig3 = px.histogram(city_data, x=pollutant, nbins=25, color_discrete_sequence=["#818cf8"])
    fig3.update_layout(
        height=280, margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=True, gridcolor="rgba(99,179,237,0.08)", color="#64748b"),
        yaxis=dict(showgrid=True, gridcolor="rgba(99,179,237,0.08)", color="#64748b"),
        font=dict(family="DM Sans", color="#94a3b8"),
        bargap=0.05,
    )
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col4:
    st.markdown(f"<div class='ap-card'><div class='ap-card-title'>📦 All Pollutants Box Plot — {city}</div>", unsafe_allow_html=True)
    fig4 = go.Figure()
    colors = ["#38bdf8", "#818cf8", "#34d399", "#fbbf24", "#f87171"]
    for i, p in enumerate(POLL_COLS):
        fig4.add_trace(go.Box(
            y=city_data[p], name=p,
            marker_color=colors[i],
            line_color=colors[i],
            boxmean=True,
        ))
    fig4.update_layout(
        height=280, margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(color="#64748b"),
        yaxis=dict(showgrid=True, gridcolor="rgba(99,179,237,0.08)", color="#64748b"),
        font=dict(family="DM Sans", color="#94a3b8"),
        showlegend=False,
    )
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ── Multi-city comparison
st.markdown("<div class='ap-card'><div class='ap-card-title'>🏙️ City Comparison — Average Pollutant Levels</div>", unsafe_allow_html=True)
city_avg = df.groupby("City")[POLL_COLS].mean().reset_index()
fig5 = go.Figure()
colors2 = ["#38bdf8", "#818cf8", "#34d399", "#fbbf24", "#f87171"]
for i, p in enumerate(POLL_COLS):
    fig5.add_trace(go.Bar(x=city_avg["City"], y=city_avg[p], name=p, marker_color=colors2[i]))
fig5.update_layout(
    barmode="group", height=300,
    margin=dict(l=10, r=10, t=10, b=10),
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(color="#64748b"),
    yaxis=dict(showgrid=True, gridcolor="rgba(99,179,237,0.08)", color="#64748b", title="µg/m³"),
    font=dict(family="DM Sans", color="#94a3b8"),
    legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5,
                font=dict(color="#94a3b8")),
)
st.plotly_chart(fig5, use_container_width=True)
st.markdown("</div></div>", unsafe_allow_html=True)