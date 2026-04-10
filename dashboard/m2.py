import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os

st.set_page_config(page_title="D2 · Forecast Engine — AirPulse", layout="wide", page_icon="📈", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');
*{box-sizing:border-box;}
:root{--bg:#050b18;--surface:#0c1628;--surface2:#111f38;--border:rgba(99,179,237,0.12);--accent:#818cf8;--text:#e2e8f0;--muted:#64748b;}
html,body,[data-testid="stAppViewContainer"],[data-testid="stApp"]{background:var(--bg) !important;font-family:'DM Sans',sans-serif;color:var(--text);}
footer,#MainMenu{display:none !important;}
.block-container{padding:0 !important;max-width:100% !important;}
[data-testid="stSidebar"]{background:var(--surface) !important;border-right:1px solid var(--border);}
[data-testid^="stSidebarNav"]{display:block !important;}
[data-testid="stSidebar"] *{color:var(--text) !important;}
[data-testid="stSelectbox"] div[data-baseweb="select"] > div{background:var(--surface2) !important;border-color:var(--border) !important;color:var(--text) !important;}
div[data-testid="metric-container"]{background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:1rem 1.25rem;}
div[data-testid="metric-container"] label{color:var(--muted) !important;font-size:0.75rem;}
div[data-testid="metric-container"] div[data-testid="stMetricValue"]{color:var(--accent) !important;font-family:'Syne',sans-serif;}
.ap-nav{display:flex;align-items:center;justify-content:space-between;padding:0 2rem;height:60px;background:rgba(5,11,24,0.9);backdrop-filter:blur(16px);border-bottom:1px solid var(--border);}
.ap-logo{font-family:'Syne',sans-serif;font-size:1.2rem;font-weight:800;color:var(--accent);}
.ap-logo span{color:var(--text);}
.ap-nav-right{display:flex;align-items:center;gap:0.6rem;}
.ap-nav-links{display:flex;gap:0.2rem;}
.ap-nav-links a{font-size:0.85rem;font-weight:500;color:var(--muted);text-decoration:none;padding:0.35rem 0.8rem;border-radius:8px;transition:all 0.2s;}
.ap-nav-links a:hover{color:var(--text);background:var(--surface2);}
.ap-nav-links a.active{color:var(--accent);background:rgba(129,140,248,0.1);}
.ap-sidebar-toggle{padding:0.35rem 0.9rem;border-radius:8px;border:1px solid var(--border);background:var(--surface2);color:var(--text);font-size:0.8rem;font-weight:500;cursor:pointer;}
.ap-sidebar-toggle:hover{background:var(--surface);}
.ap-page-header{padding:2rem 2rem 1.5rem;border-bottom:1px solid var(--border);}
.ap-page-title{font-family:'Syne',sans-serif;font-size:1.8rem;font-weight:800;color:#f1f5f9;letter-spacing:-0.02em;}
.ap-page-sub{font-size:0.9rem;color:var(--muted);margin-top:0.25rem;}
.ap-card{background:var(--surface);border:1px solid var(--border);border-radius:14px;padding:1.5rem;margin-bottom:1rem;}
.ap-card-title{font-family:'Syne',sans-serif;font-size:0.95rem;font-weight:700;color:#f1f5f9;margin-bottom:1rem;}
.best-badge{display:inline-flex;align-items:center;gap:6px;padding:0.3rem 0.8rem;border-radius:20px;font-size:0.8rem;font-weight:700;background:rgba(129,140,248,0.15);color:#818cf8;border:1px solid rgba(129,140,248,0.25);}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<nav class="ap-nav">
    <div class="ap-logo">🌬️ <span>Air</span>Pulse</div>
    <div class="ap-nav-right">
        <div class="ap-nav-links">
            <a href="https://dashboard1air.streamlit.app/">D1 · Data Explorer</a>
            <a href="https://forecastair.streamlit.app/" class="active">D2 · Forecast</a>
            <a href="https://alertsair.streamlit.app/">D3 · Alerts</a>
            <a href="https://admirairr.streamlit.app/">D4 · Admin</a>
        </div>
        <button class="ap-sidebar-toggle" onclick="const btn = document.querySelector('[data-testid=&quot;stSidebarCollapseButton&quot;]'); if(btn){btn.click();}">Filters</button>
    </div>
</nav>
<div class="ap-page-header">
    <div class="ap-page-title">📈 D2 · Forecast Engine</div>
    <div class="ap-page-sub">ARIMA, Prophet & LSTM model performance with configurable forecast horizon</div>
</div>
""", unsafe_allow_html=True)


os.makedirs("data", exist_ok=True)
DATA_PATH = "data/air_quality_data.csv"

if not os.path.exists(DATA_PATH):
    cities = ["Delhi", "Mumbai", "Chennai", "Kolkata", "Bangalore"]
    dates = pd.date_range("2024-01-01", periods=2000, freq="H")
    df_sample = pd.DataFrame({
        "City": np.random.choice(cities, len(dates)),
        "Datetime": dates,
        "PM2.5": np.random.randint(30, 120, len(dates)),
        "PM10": np.random.randint(40, 160, len(dates)),
        "NO2": np.random.randint(10, 70, len(dates)),
        "O3": np.random.randint(10, 55, len(dates)),
        "SO2": np.random.randint(2, 35, len(dates)),
    })
    df_sample.to_csv(DATA_PATH, index=False)

df = pd.read_csv(DATA_PATH, parse_dates=["Datetime"])
df = df.drop_duplicates(subset=["City", "Datetime"]).sort_values("Datetime")

# ── Sidebar
st.sidebar.markdown("### ⚙️ Forecast Controls")
city = st.sidebar.selectbox("City", sorted(df["City"].unique()))
pollutant = st.sidebar.selectbox("Pollutant", ["PM2.5", "PM10", "NO2", "O3", "SO2"])
horizon = st.sidebar.slider("Forecast Horizon (Hours)", 6, 72, 24, step=6)
show_ci = st.sidebar.checkbox("Show Confidence Interval", value=True)
metric_choice = st.sidebar.radio("Performance Metric", ["RMSE", "MAE"])

city_df = df[df["City"] == city]


def simulate_city_performance(city):
    np.random.seed(abs(hash(city)) % (10 ** 6))
    pollutants = ["PM2.5", "PM10", "NO2", "O3", "SO2"]
    rows = []
    for p in pollutants:
        rows.append({
            "Pollutant": p,
            "ARIMA": round(np.random.uniform(3, 7), 2),
            "Prophet": round(np.random.uniform(3, 6), 2),
            "LSTM": round(np.random.uniform(2.5, 6.5), 2),
        })
    return pd.DataFrame(rows)


def generate_forecast(city, pollutant="PM2.5", horizon_hours=24, model="LSTM"):
    np.random.seed(abs(hash(city + pollutant + model)) % (10 ** 6))
    # Ensure datetime index and use an explicit hourly frequency for compatibility
    city_data = city_df.copy()
    city_data["Datetime"] = pd.to_datetime(city_data["Datetime"], errors="coerce")
    city_data = (
        city_data.set_index("Datetime")[pollutant]
        .sort_index()
        .resample("1h")
        .mean()
        .ffill()
    )
    base = float(city_data.iloc[-1])
    # Use explicit hourly frequency string compatible with current pandas
    dates = pd.date_range(
        city_data.index[-1] + pd.Timedelta(hours=1),
        periods=horizon_hours,
        freq="1h",
    )
    trend = np.linspace(0, np.random.uniform(-8, 8), horizon_hours)
    noise = np.random.uniform(-4, 4, horizon_hours)
    forecast = base + trend + noise
    ci_width = np.linspace(2, 8, horizon_hours)
    upper = forecast + ci_width
    lower = forecast - ci_width
    actual = city_data.iloc[-horizon_hours:]
    return dates, actual, forecast, lower, upper


st.markdown("<div style='padding:1.5rem 2rem 0'>", unsafe_allow_html=True)

# ── Metrics
perf_df = simulate_city_performance(city)
if metric_choice == "MAE":
    for m in ["ARIMA", "Prophet", "LSTM"]:
        perf_df[m] = (perf_df[m] * 0.82).round(2)

best_model_row = perf_df.set_index("Pollutant").loc[pollutant]
best_model = best_model_row.idxmin()
best_val = best_model_row.min()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Best Model", best_model)
c2.metric(f"Best {metric_choice}", f"{best_val:.2f}")
c3.metric("Forecast Horizon", f"{horizon}h")
c4.metric("Data Points Used", f"{len(city_df):,}")

st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

# ── Row 1
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"<div class='ap-card'><div class='ap-card-title'>🏆 Model Performance ({metric_choice}) — {city}</div>", unsafe_allow_html=True)
    colors_m = {"ARIMA": "#38bdf8", "Prophet": "#34d399", "LSTM": "#818cf8"}
    fig_perf = go.Figure()
    for model_name in ["ARIMA", "Prophet", "LSTM"]:
        fig_perf.add_trace(go.Bar(
            x=perf_df["Pollutant"], y=perf_df[model_name],
            name=model_name, marker_color=colors_m[model_name],
            marker_line_width=0,
        ))
    fig_perf.update_layout(
        barmode='group', height=280,
        margin=dict(t=10, b=10, l=10, r=10),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(color="#64748b"),
        yaxis=dict(showgrid=True, gridcolor="rgba(99,179,237,0.08)", color="#64748b", title=metric_choice),
        font=dict(family="DM Sans", color="#94a3b8"),
        legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5, font=dict(color="#94a3b8")),
    )
    st.plotly_chart(fig_perf, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown(f"<div class='ap-card'><div class='ap-card-title'>🔮 {pollutant} Forecast ({best_model}) — {city} <span class='best-badge'>Best Model</span></div>", unsafe_allow_html=True)
    dates, actual, forecast, lower, upper = generate_forecast(city, pollutant, horizon, best_model)
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=actual.index, y=actual.values, mode="lines", name="Actual",
                               line=dict(color="#38bdf8", width=2)))
    fig2.add_trace(go.Scatter(x=dates, y=forecast, mode="lines", name=f"{best_model} Forecast",
                               line=dict(color="#818cf8", dash='dot', width=2)))
    if show_ci:
        fig2.add_trace(go.Scatter(
            x=dates.tolist() + dates[::-1].tolist(),
            y=upper.tolist() + lower[::-1].tolist(),
            fill='toself', fillcolor='rgba(129,140,248,0.12)',
            line=dict(color='rgba(255,255,255,0)'), showlegend=True, name="Conf. Interval"
        ))
    fig2.update_layout(
        height=280, margin=dict(t=10, b=10, l=10, r=10),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(color="#64748b"),
        yaxis=dict(showgrid=True, gridcolor="rgba(99,179,237,0.08)", color="#64748b", title=f"{pollutant} (µg/m³)"),
        font=dict(family="DM Sans", color="#94a3b8"),
        legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5, font=dict(color="#94a3b8")),
    )
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ── Row 2
col3, col4 = st.columns(2)

with col3:
    st.markdown(f"<div class='ap-card'><div class='ap-card-title'>📊 Forecast Accuracy by Horizon</div>", unsafe_allow_html=True)
    horizons = ["1h", "3h", "6h", "12h", "24h", "48h"]
    np.random.seed(abs(hash(city)) % (10 ** 6))
    acc = pd.DataFrame({
        "Horizon": horizons,
        "LSTM": np.random.randint(80, 98, len(horizons)),
        "ARIMA": np.random.randint(72, 92, len(horizons)),
        "Prophet": np.random.randint(75, 95, len(horizons)),
    })
    fig3 = go.Figure()
    for m, c in zip(["LSTM", "ARIMA", "Prophet"], ["#818cf8", "#38bdf8", "#34d399"]):
        fig3.add_trace(go.Scatter(x=acc["Horizon"], y=acc[m], mode="lines+markers",
                                   name=m, line=dict(color=c, width=2), marker=dict(size=6)))
    fig3.update_layout(
        height=280, margin=dict(t=10, b=10, l=10, r=10),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(color="#64748b"),
        yaxis=dict(showgrid=True, gridcolor="rgba(99,179,237,0.08)", color="#64748b",
                   title="Accuracy (%)", range=[60, 100]),
        font=dict(family="DM Sans", color="#94a3b8"),
        legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5, font=dict(color="#94a3b8")),
    )
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col4:
    st.markdown(f"<div class='ap-card'><div class='ap-card-title'>📋 Model Summary — {city}</div>", unsafe_allow_html=True)
    avg_vals = {p: round(city_df[p].mean(), 1) for p in ["PM2.5", "PM10", "NO2", "O3", "SO2"]}
    summary_html = ""
    for p, v in avg_vals.items():
        bar_pct = min(int(v / 2), 100)
        summary_html += f"""
        <div style='display:flex;align-items:center;gap:12px;margin-bottom:10px;'>
            <div style='width:55px;font-family:Syne,sans-serif;font-weight:700;color:#818cf8;font-size:0.85rem;'>{p}</div>
            <div style='flex:1;height:6px;background:rgba(99,179,237,0.1);border-radius:3px;'>
                <div style='width:{bar_pct}%;height:100%;background:linear-gradient(90deg,#818cf8,#38bdf8);border-radius:3px;'></div>
            </div>
            <div style='width:70px;text-align:right;font-size:0.85rem;color:#94a3b8;'>{v} µg/m³</div>
        </div>"""
    st.markdown(f"<div style='padding:0.5rem 0'>{summary_html}</div>", unsafe_allow_html=True)
    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
    # Best model per pollutant table
    perf_df["Best"] = perf_df[["ARIMA", "Prophet", "LSTM"]].idxmin(axis=1)
    best_html = "<table style='width:100%;font-size:0.82rem;border-collapse:collapse;'>"
    best_html += "<tr style='color:#64748b;font-size:0.72rem;text-transform:uppercase;letter-spacing:0.08em;'><th style='padding:6px 8px;text-align:left;'>Pollutant</th><th style='padding:6px 8px;text-align:left;'>Best Model</th><th style='padding:6px 8px;text-align:right;'>RMSE</th></tr>"
    for _, row in perf_df.iterrows():
        best_html += f"<tr style='border-top:1px solid rgba(99,179,237,0.08);'><td style='padding:7px 8px;color:#e2e8f0;'>{row['Pollutant']}</td><td style='padding:7px 8px;color:#818cf8;font-weight:600;'>{row['Best']}</td><td style='padding:7px 8px;text-align:right;color:#94a3b8;'>{row[row['Best']]:.2f}</td></tr>"
    best_html += "</table>"
    st.markdown(best_html, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)