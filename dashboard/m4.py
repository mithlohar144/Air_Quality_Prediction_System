import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time
import os

st.set_page_config(page_title="D4 · Admin Dashboard — AirPulse", layout="wide", page_icon="🧠")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');
*{box-sizing:border-box;}
:root{--bg:#050b18;--surface:#0c1628;--surface2:#111f38;--border:rgba(99,179,237,0.12);--accent:#34d399;--text:#e2e8f0;--muted:#64748b;}
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
.ap-logo{font-family:'Syne',sans-serif;font-size:1.2rem;font-weight:800;color:#34d399;}
.ap-logo span{color:var(--text);}
.ap-nav-right{display:flex;align-items:center;gap:0.6rem;}
.ap-nav-links{display:flex;gap:0.2rem;}
.ap-nav-links a{font-size:0.85rem;font-weight:500;color:var(--muted);text-decoration:none;padding:0.35rem 0.8rem;border-radius:8px;transition:all 0.2s;}
.ap-nav-links a:hover{color:var(--text);background:var(--surface2);}
.ap-nav-links a.active{color:#34d399;background:rgba(52,211,153,0.1);}
.ap-sidebar-toggle{padding:0.35rem 0.9rem;border-radius:8px;border:1px solid var(--border);background:var(--surface2);color:var(--text);font-size:0.8rem;font-weight:500;cursor:pointer;}
.ap-sidebar-toggle:hover{background:var(--surface);}
.ap-page-header{padding:2rem 2rem 1.5rem;border-bottom:1px solid var(--border);}
.ap-page-title{font-family:'Syne',sans-serif;font-size:1.8rem;font-weight:800;color:#f1f5f9;letter-spacing:-0.02em;}
.ap-page-sub{font-size:0.9rem;color:var(--muted);margin-top:0.25rem;}
.ap-card{background:var(--surface);border:1px solid var(--border);border-radius:14px;padding:1.5rem;margin-bottom:1rem;}
.ap-card-title{font-family:'Syne',sans-serif;font-size:0.95rem;font-weight:700;color:#f1f5f9;margin-bottom:1rem;}
.mode-tab{display:inline-flex;background:var(--surface2);border-radius:10px;padding:4px;gap:4px;margin-bottom:1.5rem;}
.mode-btn{padding:0.4rem 1.2rem;border-radius:8px;font-size:0.85rem;font-weight:600;cursor:pointer;transition:all 0.2s;border:none;}
.mode-btn.active{background:var(--accent);color:#050b18;}
.mode-btn.inactive{background:transparent;color:var(--muted);}
.model-result-row{display:flex;align-items:center;justify-content:space-between;padding:0.75rem 1rem;border-radius:10px;margin-bottom:0.5rem;border:1px solid;}
.upload-zone{border:2px dashed var(--border);border-radius:14px;padding:2.5rem;text-align:center;background:var(--surface2);}
.upload-zone-title{font-family:'Syne',sans-serif;font-size:1rem;font-weight:700;color:#f1f5f9;margin-bottom:0.5rem;}
.upload-zone-sub{font-size:0.85rem;color:var(--muted);}
/* Override streamlit file uploader */
[data-testid="stFileUploaderDropzone"]{background:var(--surface2) !important;border-color:var(--border) !important;}
[data-testid="stFileUploaderDropzoneInstructions"]{color:var(--muted) !important;}
/* Toggle */
[data-testid="stToggle"] span{color:var(--text) !important;}
/* DataFrame */
[data-testid="stDataFrame"]{border-radius:10px;overflow:hidden;}
/* Button */
.stButton button{background:linear-gradient(135deg,#34d399,#38bdf8);color:#050b18;font-weight:700;border:none;border-radius:10px;padding:0.6rem 1.5rem;font-family:'DM Sans',sans-serif;}
.stButton button:hover{opacity:0.9;transform:translateY(-1px);}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<nav class="ap-nav">
    <div class="ap-logo">🌬️ <span>Air</span>Pulse</div>
    <div class="ap-nav-right">
        <div class="ap-nav-links">
            <a href="https://dashboard1air.streamlit.app/">D1 · Data Explorer</a>
            <a href="https://forecastair.streamlit.app/">D2 · Forecast</a>
            <a href="https://alertsair.streamlit.app/">D3 · Alerts</a>
            <a href="https://admirairr.streamlit.app/" class="active">D4 · Admin</a>
        </div>
        <button class="ap-sidebar-toggle" onclick="const btn = document.querySelector('[data-testid=&quot;stSidebarCollapseButton&quot;]'); if(btn){btn.click();}">Filters</button>
    </div>
</nav>
<div class="ap-page-header">
    <div class="ap-page-title">🧠 D4 · Admin Dashboard</div>
    <div class="ap-page-sub">Upload datasets, retrain ML models and compare performance metrics</div>
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

df_base = pd.read_csv(DATA_PATH, parse_dates=["Datetime"])

st.sidebar.markdown("### ⚙️ Controls")
city = st.sidebar.selectbox("City", sorted(df_base["City"].unique()))
pollutant = st.sidebar.selectbox("Pollutant", ["PM2.5", "PM10", "NO2", "O3", "SO2"])
forecast_horizon = st.sidebar.selectbox("Forecast Horizon", ["24 Hours", "48 Hours", "7 Days"])
admin_mode = st.sidebar.toggle("🧠 Admin Mode (Upload & Retrain)")

city_df = df_base[df_base["City"] == city]

st.markdown("<div style='padding:1.5rem 2rem 0'>", unsafe_allow_html=True)

# ── Overview (non-admin) mode
if not admin_mode:
    np.random.seed(abs(hash(city + pollutant)) % (10 ** 6))
    aqi_value = int(city_df["PM2.5"].mean() * 0.5 + city_df["PM10"].mean() * 0.3 + city_df["O3"].mean() * 0.2)
    if aqi_value <= 50:   aqi_status, aqi_color = "Good", "#4ade80"
    elif aqi_value <= 100: aqi_status, aqi_color = "Moderate", "#facc15"
    else:                  aqi_status, aqi_color = "Poor", "#f87171"

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("City", city)
    c2.metric("Avg AQI", aqi_value)
    c3.metric("Status", aqi_status)
    c4.metric("Pollutant Focus", pollutant)

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='ap-card'><div class='ap-card-title'>🎯 Current AQI Gauge</div>", unsafe_allow_html=True)
        fig_g = go.Figure(go.Indicator(
            mode="gauge+number",
            value=aqi_value,
            title={'text': f"AQI — {city}", 'font': {'color': '#94a3b8', 'size': 14, 'family': 'DM Sans'}},
            number={'font': {'color': aqi_color, 'size': 48, 'family': 'Syne'}},
            gauge={
                "axis": {"range": [0, 300], "tickcolor": "#64748b", "tickfont": {"color": "#64748b"}},
                "bar": {"color": aqi_color, "thickness": 0.25},
                "bgcolor": "rgba(0,0,0,0)",
                "borderwidth": 0,
                "steps": [
                    {"range": [0, 50], "color": "rgba(74,222,128,0.15)"},
                    {"range": [50, 100], "color": "rgba(250,204,21,0.15)"},
                    {"range": [100, 150], "color": "rgba(251,146,60,0.15)"},
                    {"range": [150, 200], "color": "rgba(248,113,113,0.15)"},
                    {"range": [200, 300], "color": "rgba(167,139,250,0.15)"},
                ],
                "threshold": {"line": {"color": aqi_color, "width": 3}, "value": aqi_value},
            },
        ))
        fig_g.update_layout(
            height=260, margin=dict(t=30, b=10, l=20, r=20),
            paper_bgcolor="rgba(0,0,0,0)", font=dict(family="DM Sans"),
        )
        st.plotly_chart(fig_g, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown(f"<div class='ap-card'><div class='ap-card-title'>📈 {pollutant} Trend — {city}</div>", unsafe_allow_html=True)
        sample = city_df.sort_values("Datetime").tail(48)
        fig_t = go.Figure()
        fig_t.add_trace(go.Scatter(
            x=sample["Datetime"], y=sample[pollutant],
            mode="lines", fill="tozeroy",
            line=dict(color="#34d399", width=1.5),
            fillcolor="rgba(52,211,153,0.06)",
        ))
        fig_t.update_layout(
            height=260, margin=dict(t=10, b=10, l=10, r=10),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(color="#64748b", showgrid=False),
            yaxis=dict(showgrid=True, gridcolor="rgba(99,179,237,0.08)", color="#64748b", title=f"{pollutant} (µg/m³)"),
            font=dict(family="DM Sans", color="#94a3b8"),
        )
        st.plotly_chart(fig_t, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div style='background:rgba(52,211,153,0.06);border:1px solid rgba(52,211,153,0.2);border-radius:12px;padding:1rem 1.5rem;display:flex;align-items:center;gap:12px;'>
        <span style='font-size:1.3rem;'>🧠</span>
        <div>
            <div style='font-weight:700;color:#34d399;margin-bottom:3px;'>Enable Admin Mode</div>
            <div style='font-size:0.85rem;color:#64748b;'>Toggle <strong>Admin Mode</strong> in the sidebar to upload a dataset and retrain ML models.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── ADMIN MODE
else:
    st.markdown("<div class='ap-card'><div class='ap-card-title'>📂 Upload Training Dataset</div>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Upload a CSV file with air quality data",
        type=["csv"],
        help="Required columns: numeric target + feature columns. Optional: Date/Datetime column."
    )
    st.markdown("</div>", unsafe_allow_html=True)

    if uploaded_file is not None:
        try:
            try:
                df_upload = pd.read_csv(uploaded_file, encoding='utf-8')
            except UnicodeDecodeError:
                df_upload = pd.read_csv(uploaded_file, encoding='latin1')
        except Exception as e:
            st.error(f"Error reading file: {e}")
            st.stop()

            st.markdown("<div class='ap-card'><div class='ap-card-title'>👁️ Dataset Preview</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='color:#64748b;font-size:0.85rem;margin-bottom:0.75rem;'>{len(df_upload):,} rows × {len(df_upload.columns)} columns</div>", unsafe_allow_html=True)
            st.dataframe(df_upload.head(8), use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

            # ── Column selection
            col1, col2 = st.columns(2)
            with col1:
                target_col = st.selectbox("🎯 Target Column", options=df_upload.columns)
            with col2:
                feature_options = [c for c in df_upload.columns if c != target_col]
                features = st.multiselect("🧩 Feature Columns", options=feature_options,
                                           default=feature_options[:min(5, len(feature_options))])

            # ── Model selection
            st.markdown("<div class='ap-card'><div class='ap-card-title'>🤖 Select Models to Train</div>", unsafe_allow_html=True)
            mc1, mc2, mc3, mc4, mc5 = st.columns(5)
            run_rf = mc1.checkbox("Random Forest", value=True)
            run_xgb = mc2.checkbox("XGBoost", value=True)
            run_arima = mc3.checkbox("ARIMA", value=False, help="Slow on large datasets")
            run_prophet = mc4.checkbox("Prophet", value=False, help="Requires date column")
            run_lstm = mc5.checkbox("LSTM", value=False, help="Requires TensorFlow")
            st.markdown("</div>", unsafe_allow_html=True)

            if st.button("🚀 Retrain Models", use_container_width=True):
                if not features:
                    st.error("Please select at least one feature column.")
                elif target_col not in df_upload.columns:
                    st.error("Please select a valid target column.")
                else:
                    with st.spinner("⚙️ Training models..."):
                        # ── Preprocessing (no sklearn dependency issues)
                        data = df_upload.copy().dropna()
                        
                        # Encode categoricals
                        for col in data.columns:
                            if data[col].dtype == 'object':
                                try:
                                    data[col] = pd.to_datetime(data[col])
                                    data[col] = data[col].astype(np.int64) // 10**9
                                except Exception:
                                    codes = data[col].astype('category').cat.codes
                                    data[col] = codes

                        # Drop remaining non-numeric
                        numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
                        valid_features = [f for f in features if f in numeric_cols]
                        
                        if not valid_features:
                            st.error("No numeric feature columns found after encoding.")
                            st.stop()

                        X = data[valid_features].values.astype(float)
                        y = data[target_col].values.astype(float)

                        # Min-max scale manually
                        X_min, X_max = X.min(axis=0), X.max(axis=0)
                        X_range = np.where(X_max - X_min == 0, 1, X_max - X_min)
                        X_scaled = (X - X_min) / X_range

                        y_min, y_max = y.min(), y.max()
                        y_range = y_max - y_min if y_max != y_min else 1
                        y_scaled = (y - y_min) / y_range

                        split = int(0.8 * len(X_scaled))
                        X_train, X_test = X_scaled[:split], X_scaled[split:]
                        y_train, y_test = y_scaled[:split], y_scaled[split:]
                        
                        results = []
                        predictions = {}
                        progress = st.progress(0)

                        # ── Random Forest
                        if run_rf:
                            try:
                                from sklearn.ensemble import RandomForestRegressor
                                from sklearn.metrics import mean_squared_error
                                rf = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
                                rf.fit(X_train, y_train)
                                y_pred = rf.predict(X_test)
                                rmse = np.sqrt(mean_squared_error(y_test, y_pred))
                                mae = np.mean(np.abs(y_test - y_pred))
                                results.append({"Model": "Random Forest", "RMSE": round(rmse, 4), "MAE": round(mae, 4)})
                                predictions["Random Forest"] = {"actual": y_test[:50], "pred": y_pred[:50]}
                            except ImportError:
                                st.warning("sklearn not available for Random Forest.")
                            progress.progress(20)

                        # ── XGBoost
                        if run_xgb:
                            try:
                                from xgboost import XGBRegressor
                                from sklearn.metrics import mean_squared_error
                                xgb = XGBRegressor(n_estimators=100, random_state=42, verbosity=0)
                                xgb.fit(X_train, y_train)
                                y_pred = xgb.predict(X_test)
                                rmse = np.sqrt(mean_squared_error(y_test, y_pred))
                                mae = np.mean(np.abs(y_test - y_pred))
                                results.append({"Model": "XGBoost", "RMSE": round(rmse, 4), "MAE": round(mae, 4)})
                                predictions["XGBoost"] = {"actual": y_test[:50], "pred": y_pred[:50]}
                            except ImportError:
                                st.warning("XGBoost not installed. Run: pip install xgboost")
                            progress.progress(40)

                        # ── ARIMA (lightweight simulation if statsmodels unavailable)
                        if run_arima:
                            try:
                                from statsmodels.tsa.arima.model import ARIMA
                                y_series = pd.Series(y[:200])  # limit for speed
                                model_a = ARIMA(y_series, order=(2, 1, 2))
                                fit_a = model_a.fit()
                                y_pred_a = fit_a.fittedvalues
                                y_actual_a = y_series[1:]
                                y_pred_a = y_pred_a[1:]
                                rmse = float(np.sqrt(np.mean((y_actual_a.values - y_pred_a.values) ** 2)))
                                rmse_scaled = rmse / y_range
                                mae_scaled = float(np.mean(np.abs(y_actual_a.values - y_pred_a.values))) / y_range
                                results.append({"Model": "ARIMA", "RMSE": round(rmse_scaled, 4), "MAE": round(mae_scaled, 4)})
                                predictions["ARIMA"] = {"actual": y_actual_a.values[:50] / y_range,
                                                         "pred": y_pred_a.values[:50] / y_range}
                            except ImportError:
                                st.warning("statsmodels not installed.")
                            except Exception as e:
                                st.warning(f"ARIMA failed: {e}")
                            progress.progress(60)

                        # ── Prophet
                        if run_prophet:
                            try:
                                from prophet import Prophet
                                date_col_p = None
                                for c in df_upload.columns:
                                    try:
                                        pd.to_datetime(df_upload[c])
                                        date_col_p = c
                                        break
                                    except Exception:
                                        continue
                                if date_col_p:
                                    df_prophet = pd.DataFrame({'ds': pd.to_datetime(df_upload[date_col_p]), 'y': y})
                                else:
                                    df_prophet = pd.DataFrame({'ds': pd.date_range('2023-01-01', periods=len(y), freq='D'), 'y': y})
                                df_prophet = df_prophet.dropna()
                                m_p = Prophet(daily_seasonality=True, yearly_seasonality=False)
                                m_p.fit(df_prophet)
                                future = m_p.make_future_dataframe(periods=30)
                                fc = m_p.predict(future)
                                y_pred_p = fc['yhat'][:len(y)].values
                                rmse = float(np.sqrt(np.mean((y - y_pred_p) ** 2))) / y_range
                                mae = float(np.mean(np.abs(y - y_pred_p))) / y_range
                                results.append({"Model": "Prophet", "RMSE": round(rmse, 4), "MAE": round(mae, 4)})
                                predictions["Prophet"] = {"actual": (y[:50] - y_min) / y_range,
                                                           "pred": (y_pred_p[:50] - y_min) / y_range}
                            except ImportError:
                                st.warning("Prophet not installed.")
                            except Exception as e:
                                st.warning(f"Prophet failed: {e}")
                            progress.progress(80)

                        # ── LSTM
                        if run_lstm:
                            try:
                                from tensorflow.keras.models import Sequential
                                from tensorflow.keras.layers import LSTM as KerasLSTM, Dense
                                X_lstm = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
                                X_test_lstm = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))
                                model_lstm = Sequential([
                                    KerasLSTM(32, input_shape=(X_train.shape[1], 1)),
                                    Dense(1)
                                ])
                                model_lstm.compile(optimizer='adam', loss='mse')
                                model_lstm.fit(X_lstm, y_train, epochs=5, batch_size=32, verbose=0)
                                y_pred_l = model_lstm.predict(X_test_lstm, verbose=0).flatten()
                                rmse = float(np.sqrt(np.mean((y_test - y_pred_l) ** 2)))
                                mae = float(np.mean(np.abs(y_test - y_pred_l)))
                                results.append({"Model": "LSTM", "RMSE": round(rmse, 4), "MAE": round(mae, 4)})
                                predictions["LSTM"] = {"actual": y_test[:50], "pred": y_pred_l[:50]}
                            except ImportError:
                                st.warning("TensorFlow not installed.")
                            except Exception as e:
                                st.warning(f"LSTM failed: {e}")
                            progress.progress(100)

                        progress.empty()

                        if not results:
                            st.error("No models were trained successfully. Please select at least one model and ensure required packages are installed.")
                        else:
                            result_df = pd.DataFrame(results).sort_values("RMSE")
                            best_model = result_df.iloc[0]["Model"]
                            best_rmse = result_df.iloc[0]["RMSE"]

                            # ── Success banner
                            st.markdown(f"""
                            <div style='background:rgba(52,211,153,0.1);border:1px solid rgba(52,211,153,0.25);border-radius:12px;padding:1rem 1.5rem;margin-bottom:1rem;'>
                                <div style='font-family:Syne,sans-serif;font-size:1.1rem;font-weight:800;color:#34d399;margin-bottom:4px;'>
                                    🏆 Best Model: {best_model}
                                </div>
                                <div style='color:#64748b;font-size:0.875rem;'>RMSE = {best_rmse:.4f} (scaled) — lowest error across all trained models</div>
                            </div>
                            """, unsafe_allow_html=True)

                            col1, col2 = st.columns(2)

                            with col1:
                                st.markdown("<div class='ap-card'><div class='ap-card-title'>📊 Model RMSE Comparison</div>", unsafe_allow_html=True)
                                colors_bar = {"Random Forest": "#34d399", "XGBoost": "#38bdf8",
                                              "ARIMA": "#818cf8", "Prophet": "#fbbf24", "LSTM": "#f87171"}
                                fig_bar = go.Figure(go.Bar(
                                    x=result_df["Model"],
                                    y=result_df["RMSE"],
                                    marker_color=[colors_bar.get(m, "#38bdf8") for m in result_df["Model"]],
                                    marker_line_width=0,
                                    text=result_df["RMSE"].apply(lambda x: f"{x:.4f}"),
                                    textposition="outside",
                                    textfont=dict(color="#94a3b8", size=11),
                                ))
                                fig_bar.update_layout(
                                    height=260, margin=dict(t=30, b=10, l=10, r=10),
                                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                    xaxis=dict(color="#64748b"),
                                    yaxis=dict(showgrid=True, gridcolor="rgba(99,179,237,0.08)",
                                               color="#64748b", title="RMSE (lower = better)"),
                                    font=dict(family="DM Sans", color="#94a3b8"),
                                )
                                st.plotly_chart(fig_bar, use_container_width=True)
                                st.markdown("</div>", unsafe_allow_html=True)

                            with col2:
                                st.markdown("<div class='ap-card'><div class='ap-card-title'>📋 Performance Table</div>", unsafe_allow_html=True)
                                table_html = "<table style='width:100%;font-size:0.85rem;border-collapse:collapse;'>"
                                table_html += "<tr style='color:#64748b;font-size:0.72rem;text-transform:uppercase;letter-spacing:0.08em;'><th style='padding:8px;text-align:left;'>Model</th><th style='padding:8px;text-align:right;'>RMSE</th><th style='padding:8px;text-align:right;'>MAE</th></tr>"
                                for i, row in result_df.iterrows():
                                    is_best = row["Model"] == best_model
                                    bg = "rgba(52,211,153,0.06)" if is_best else ""
                                    badge = " <span style='font-size:0.7rem;background:rgba(52,211,153,0.15);color:#34d399;padding:1px 6px;border-radius:8px;'>best</span>" if is_best else ""
                                    table_html += f"<tr style='border-top:1px solid rgba(99,179,237,0.08);background:{bg};'>"
                                    table_html += f"<td style='padding:8px;color:#f1f5f9;font-weight:600;'>{row['Model']}{badge}</td>"
                                    table_html += f"<td style='padding:8px;text-align:right;color:#34d399;font-family:Syne,sans-serif;'>{row['RMSE']:.4f}</td>"
                                    table_html += f"<td style='padding:8px;text-align:right;color:#94a3b8;'>{row['MAE']:.4f}</td></tr>"
                                table_html += "</table>"
                                st.markdown(table_html, unsafe_allow_html=True)
                                st.markdown("</div>", unsafe_allow_html=True)

                            # ── Predicted vs Actual chart
                            if best_model in predictions:
                                st.markdown(f"<div class='ap-card'><div class='ap-card-title'>🔍 Predicted vs Actual — {best_model}</div>", unsafe_allow_html=True)
                                p_data = predictions[best_model]
                                fig_pa = go.Figure()
                                fig_pa.add_trace(go.Scatter(
                                    y=list(p_data["actual"]), mode='lines', name='Actual',
                                    line=dict(color="#38bdf8", width=2)
                                ))
                                fig_pa.add_trace(go.Scatter(
                                    y=list(p_data["pred"]), mode='lines', name='Predicted',
                                    line=dict(color="#34d399", dash='dot', width=2)
                                ))
                                fig_pa.update_layout(
                                    height=280, margin=dict(t=10, b=10, l=10, r=10),
                                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                    xaxis=dict(color="#64748b", title="Sample index"),
                                    yaxis=dict(showgrid=True, gridcolor="rgba(99,179,237,0.08)",
                                               color="#64748b", title="Scaled Value"),
                                    font=dict(family="DM Sans", color="#94a3b8"),
                                    legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5, font=dict(color="#94a3b8")),
                                )
                                st.plotly_chart(fig_pa, use_container_width=True)
                                st.markdown("</div>", unsafe_allow_html=True)

                            st.success("✅ Model retraining complete!")

    else:
        st.markdown("""
        <div class='ap-card'>
            <div class='ap-card-title'>📤 Dataset Requirements</div>
            <div style='font-size:0.875rem;color:#64748b;line-height:1.8;'>
                <div>✅ <strong style='color:#f1f5f9;'>Format:</strong> CSV file (.csv)</div>
                <div>✅ <strong style='color:#f1f5f9;'>Target column:</strong> Numeric (e.g., PM2.5, AQI)</div>
                <div>✅ <strong style='color:#f1f5f9;'>Feature columns:</strong> Numeric or categorical (auto-encoded)</div>
                <div>✅ <strong style='color:#f1f5f9;'>Date column:</strong> Optional — needed for Prophet & ARIMA</div>
                <div style='margin-top:0.75rem;'>📌 <em>The sample dataset at <code>data/air_quality_data.csv</code> can be used for testing.</em></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)