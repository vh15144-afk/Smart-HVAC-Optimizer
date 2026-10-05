import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta


# ============================================================
# PAGE SETTINGS
# ============================================================

st.set_page_config(
    page_title="Smart HVAC AI Optimiser",
    page_icon="❄️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# LOGIN / AUTHENTICATION
# ============================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:

    st.title("❄️ Smart HVAC AI Optimiser")
    st.subheader("AI Energy Optimisation Console")

    st.write("")
    st.write("")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        st.info("🔐 Please login to access the HVAC dashboard.")

        username = st.text_input(
            "Username",
            placeholder="Enter username"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter password"
        )

        if st.button(
            "🔓 Login",
            type="primary",
            use_container_width=True
        ):

            if username == st.secrets["login"]["username"] and password == st.secrets["login"]["password"]:

                st.session_state.logged_in = True
                st.rerun()

            else:

                st.error("❌ Incorrect username or password.")

        st.caption(
            "Prototype login: admin / hvac123"
        )

    st.stop()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("❄️ Smart HVAC")
    st.caption("AI Energy Optimisation Console")

    st.divider()

    st.subheader("🏢 Select Zone")

    selected_zone = st.selectbox(
        "Zone",
        [
            "Entire Building",
            "Zone 1 - Main Hall",
            "Zone 2 - Office Area",
            "Zone 3 - Meeting Area",
            "Zone 4 - Restaurant Area"
        ],
        label_visibility="collapsed"
    )

    st.subheader("🤖 Operating Mode")

    operating_mode = st.selectbox(
        "Mode",
        [
            "AI Optimisation",
            "Energy Saving",
            "Comfort Priority"
        ],
        label_visibility="collapsed"
    )

    st.subheader("🌡️ Comfort temperature")

    comfort_temperature = st.slider(
        "Target Temperature",
        min_value=22.0,
        max_value=26.0,
        value=24.0,
        step=0.5
    )

    st.subheader("⚡ Automatic HVAC control")

    automatic_control = st.toggle(
        "Automatic HVAC Control",
        value=True
    )

    st.subheader("🔄 Live refresh")

    live_refresh = st.toggle(
        "Live Refresh",
        value=False
    )

    st.divider()

    st.info(
        "Prototype mode uses simulated sensor data. "
        "Later, the same software layer can receive "
        "real hardware data."
    )

    st.caption("🕐 Last updated")

    st.write(
        datetime.now().strftime(
            "%d-%b-%Y %I:%M:%S %p"
        )
    )

    st.divider()

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        st.session_state.logged_in = False
        st.rerun()


# ============================================================
# SIMULATED SENSOR DATA
# ============================================================

np.random.seed(42)

end_time = datetime.now()

time_values = pd.date_range(
    end=end_time,
    periods=49,
    freq="30min"
)


temperature = (
    23.7
    + 0.35 * np.sin(
        np.linspace(0, 4 * np.pi, 49)
    )
    + np.random.normal(0, 0.12, 49)
)

humidity = (
    55
    + 3 * np.sin(
        np.linspace(0, 3 * np.pi, 49)
    )
    + np.random.normal(0, 0.7, 49)
)

occupancy = (
    60
    + 12 * np.sin(
        np.linspace(0, 4 * np.pi, 49)
    )
    + np.random.normal(0, 2.5, 49)
)

occupancy = np.clip(
    occupancy,
    20,
    90
)

baseline_power = (
    17.5
    + occupancy * 0.035
    + np.random.normal(0, 0.45, 49)
)

optimised_power = baseline_power * 0.87

actual_power = optimised_power * 1.08

baseline_energy = baseline_power * 0.5

optimised_energy = optimised_power * 0.5

energy_saved = (
    baseline_energy - optimised_energy
)


data = pd.DataFrame({
    "Time": time_values,
    "Temperature": temperature,
    "Humidity": humidity,
    "Occupancy": occupancy,
    "Baseline Power": baseline_power,
    "Actual Power": actual_power,
    "Optimised Power": optimised_power,
    "Baseline Energy": baseline_energy,
    "Optimised Energy": optimised_energy,
    "Energy Saved": energy_saved
})


# ============================================================
# CURRENT DASHBOARD VALUES
# ============================================================

current_temperature = 24.72
current_humidity = 60.44
current_occupancy = 73.05
current_power = 16.27

energy_saved_24h = 51.28
baseline_energy_24h = 400.17
optimised_energy_24h = 348.88

saving_efficiency = 12.85

recommended_temperature = 23.7


# ============================================================
# MAIN TITLE
# ============================================================

st.title("❄️ Smart HVAC Energy Optimiser")

st.subheader(
    "AI-powered comfort management • "
    "energy intelligence • "
    "automatic HVAC decisions"
)

st.divider()


# ============================================================
# TOP METRICS
# ============================================================

st.subheader("📊 Current HVAC Status")

m1, m2, m3, m4, m5, m6 = st.columns(6)


with m1:

    st.metric(
        "🌡️ Temperature",
        f"{current_temperature:.2f} °C",
        f"Target: {comfort_temperature:.1f} °C"
    )


with m2:

    st.metric(
        "💧 Humidity",
        f"{current_humidity:.2f} %",
        "Comfort: Good"
    )


with m3:

    st.metric(
        "👥 Occupancy",
        f"{current_occupancy:.2f} %",
        "Currently Detected"
    )


with m4:

    st.metric(
        "⚡ Power Usage",
        f"{current_power:.2f} kW",
        "Current Consumption"
    )


with m5:

    st.metric(
        "🍃 Energy Saved",
        f"{energy_saved_24h:.2f} kWh",
        "vs Baseline"
    )


with m6:

    st.metric(
        "📈 Saving Efficiency",
        f"{saving_efficiency:.2f} %",
        "Improvement"
    )


st.write("")


# ============================================================
# POWER CONSUMPTION GRAPH
# ============================================================

graph1, graph2 = st.columns(2)


with graph1:

    st.subheader(
        "📈 Power Consumption Trend (Last 24 Hours)"
    )

    fig_power = go.Figure()

    fig_power.add_trace(
        go.Scatter(
            x=data["Time"],
            y=data["Baseline Power"],
            mode="lines",
            name="Baseline Power",
            line=dict(
                color="#d62728",
                dash="dash",
                width=2
            )
        )
    )

    fig_power.add_trace(
        go.Scatter(
            x=data["Time"],
            y=data["Actual Power"],
            mode="lines",
            name="Actual Power",
            line=dict(
                color="#1976d2",
                width=2
            )
        )
    )

    fig_power.add_trace(
        go.Scatter(
            x=data["Time"],
            y=data["Optimised Power"],
            mode="lines",
            name="Optimised Power",
            line=dict(
                color="#2e8b57",
                width=2
            )
        )
    )

    fig_power.update_layout(
        height=400,
        xaxis_title="Time",
        yaxis_title="Power (kW)",
        hovermode="x unified",
        plot_bgcolor="white",
        paper_bgcolor="white",
        legend=dict(
            orientation="h"
        )
    )

    st.plotly_chart(
        fig_power,
        use_container_width=True
    )


# ============================================================
# ENVIRONMENT & OCCUPANCY GRAPH
# ============================================================

with graph2:

    st.subheader(
        "🌡️ Environment & Occupancy"
    )

    fig_environment = make_subplots(
        specs=[[{"secondary_y": True}]]
    )

    fig_environment.add_trace(
        go.Scatter(
            x=data["Time"],
            y=data["Temperature"],
            mode="lines+markers",
            name="Temperature (°C)",
            line=dict(
                color="#d62728",
                width=2
            )
        ),
        secondary_y=False
    )

    fig_environment.add_trace(
        go.Scatter(
            x=data["Time"],
            y=data["Humidity"],
            mode="lines+markers",
            name="Humidity (%)",
            line=dict(
                color="#1f77b4",
                width=2
            )
        ),
        secondary_y=False
    )

    fig_environment.add_trace(
        go.Scatter(
            x=data["Time"],
            y=data["Occupancy"],
            mode="lines+markers",
            name="Occupancy (%)",
            line=dict(
                color="#2e8b57",
                dash="dash",
                width=2
            )
        ),
        secondary_y=True
    )

    fig_environment.update_yaxes(
        title_text="Temperature / Humidity",
        secondary_y=False
    )

    fig_environment.update_yaxes(
        title_text="Occupancy (%)",
        secondary_y=True
    )

    fig_environment.update_layout(
        height=400,
        hovermode="x unified",
        plot_bgcolor="white",
        paper_bgcolor="white",
        legend=dict(
            orientation="h"
        )
    )

    st.plotly_chart(
        fig_environment,
        use_container_width=True
    )


st.divider()


# ============================================================
# HVAC CONTROL CENTRE
# ============================================================

st.subheader("⚙️ HVAC Control Centre")

control1, control2, control3 = st.columns(3)


with control1:

    if automatic_control:

        st.success(
            "🟢 Automatic Control: ACTIVE"
        )

    else:

        st.warning(
            "🟡 Automatic Control: OFF"
        )


with control2:

    st.info(
        f"🌡️ Target Temperature: "
        f"{comfort_temperature:.1f} °C"
    )


with control3:

    if live_refresh:

        st.success(
            "🔄 Live Monitoring: ACTIVE"
        )

    else:

        st.info(
            "⏸️ Live Monitoring: OFF"
        )


st.write("")


# ============================================================
# BOTTOM SECTIONS
# ============================================================

ai_column, summary_column, gauge_column = st.columns(3)


# ============================================================
# AI RECOMMENDATION
# ============================================================

with ai_column:

    st.subheader(
        "🤖 AI Recommendation"
    )

    st.success(
        f"Recommended Temperature: "
        f"{recommended_temperature:.1f} °C"
    )

    st.write(
        "**AI Suggestion:** "
        "Lower temperature slightly to save energy."
    )

    st.write(
        "**Action:** "
        "Adjust cooling set-point and maintain "
        "current fan speed."
    )

    st.write("**Status:**")

    st.success(
        "✅ System Optimised"
    )

    st.write(
        "HVAC is operating efficiently."
    )


# ============================================================
# ENERGY SUMMARY
# ============================================================

with summary_column:

    st.subheader(
        "🌐 Energy Summary (Last 24 Hours)"
    )

    st.write(
        f"**Baseline Energy:** "
        f"{baseline_energy_24h:.2f} kWh"
    )

    st.divider()

    st.write(
        f"**Optimised Energy:** "
        f"{optimised_energy_24h:.2f} kWh"
    )

    st.divider()

    st.write(
        f"**Energy Saved:** "
        f"{energy_saved_24h:.2f} kWh"
    )

    st.divider()

    st.write(
        f"**Saving Efficiency:** "
        f"{saving_efficiency:.2f} %"
    )


# ============================================================
# ENERGY SAVING GAUGE
# ============================================================

with gauge_column:

    st.subheader(
        "📊 Energy Saving Gauge"
    )

    gauge = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=saving_efficiency,
            number={
                "suffix": "%",
                "font": {
                    "size": 30
                }
            },
            title={
                "text": "Saving Efficiency"
            },
            gauge={
                "axis": {
                    "range": [0, 100]
                },
                "bar": {
                    "color": "#2e8b57"
                },
                "steps": [
                    {
                        "range": [0, 30],
                        "color": "#eeeeee"
                    },
                    {
                        "range": [30, 70],
                        "color": "#dddddd"
                    },
                    {
                        "range": [70, 100],
                        "color": "#cccccc"
                    }
                ]
            }
        )
    )

    gauge.update_layout(
        height=300,
        margin=dict(
            l=20,
            r=20,
            t=30,
            b=10
        ),
        paper_bgcolor="white"
    )

    st.plotly_chart(
        gauge,
        use_container_width=True
    )


# ============================================================
# PROJECT INFORMATION
# ============================================================

st.divider()

st.subheader("ℹ️ System Information")

info1, info2, info3 = st.columns(3)


with info1:

    st.info(
        f"**Selected Zone**\n\n"
        f"{selected_zone}"
    )


with info2:

    st.info(
        f"**Operating Mode**\n\n"
        f"{operating_mode}"
    )


with info3:

    st.info(
        "**System Status**\n\n"
        "🟢 AI Optimisation Active"
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "❄️ Smart HVAC Energy Optimiser | "
    "AI-Powered Comfort • Energy Intelligence • "
    "Automatic Decisions"
)
