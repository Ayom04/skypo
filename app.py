import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.graph_objects as go
from datetime import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="SKYPO Grid Command",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS FOR PROFESSIONAL UI (DARK MODE OPTIMIZED) ---
st.markdown("""
    <style>
    .metric-card {
        background-color: #0E1117;
        border: 1px solid #303030;
        padding: 20px;
        border-radius: 5px;
        text-align: center;
    }
    .stAlert {
        padding: 10px;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: SIMULATION CONTROLS ---
st.sidebar.title("Grid Simulation Control")
st.sidebar.markdown("---")

simulation_mode = st.sidebar.radio(
    "Scenario Injection",
    ("Normal Operation", "High Load / Peak Time", "Transformer Fault", "Partial Collapse")
)

st.sidebar.markdown("### Node Selector")
selected_node = st.sidebar.selectbox("Select TCN/DisCo Asset", ["Substation LKK-102 (Lekki)", "Feeder ALS-004 (Alausa)", "Transformer MSH-09 (Mushin)"])

st.sidebar.info("System Status: Monitoring Active")

# --- HELPER FUNCTIONS FOR PHYSICS SIMULATION ---
def generate_data(mode):
    # Base values
    voltage = 220.0  # V
    frequency = 50.0 # Hz
    current = 15.0   # Amps
    temp = 45.0      # Celsius
    vibration = 0.5  # mm/s
    pf = 0.95        # Power Factor

    noise = np.random.normal(0, 0.1)

    if mode == "Normal Operation":
        voltage += np.random.normal(0, 2)
        frequency += np.random.normal(0, 0.05)
        current += np.random.normal(0, 1)
        temp += np.random.normal(0, 0.5)
        
    elif mode == "High Load / Peak Time":
        current = 45.0 + np.random.normal(0, 2) # High current
        voltage = 205.0 + np.random.normal(0, 2) # Voltage sag
        frequency = 49.2 + np.random.normal(0, 0.1) # Frequency drop
        temp = 65.0 + np.random.normal(0, 1) # Heating up
        
    elif mode == "Transformer Fault":
        vibration = 8.5 + np.random.normal(0, 1) # HIGH VIBRATION
        temp = 85.0 + np.random.normal(0, 2) # Overheating
        frequency = 50.0 + np.random.normal(0, 0.05)
        
    elif mode == "Partial Collapse":
        voltage = 50.0 + np.random.normal(0, 10) # Brownout
        frequency = 46.0 + np.random.normal(0, 0.5) # Dangerous frequency
        current = 0.0
        
    return {
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "voltage": round(voltage, 2),
        "frequency": round(frequency, 2),
        "current": round(current, 2),
        "temp": round(temp, 1),
        "vibration": round(vibration, 2),
        "pf": round(pf, 2)
    }

# --- MAIN DASHBOARD ---
st.title(f"📡 Real-Time Telemetry: {selected_node}")
st.markdown("Automated Grid Monitoring & Fault Detection System")

# Create placeholders for live updates
kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
chart_col1, chart_col2 = st.columns(2)
alert_placeholder = st.empty()

# Initialize history in session state if not exists
if 'history' not in st.session_state:
    st.session_state['history'] = pd.DataFrame(columns=['timestamp', 'voltage', 'frequency', 'current', 'temp', 'vibration'])

# --- LIVE SIMULATION LOOP ---
# In a real app, this would use st.experimental_rerun() or a stream
placeholder_kpi1 = kpi_col1.empty()
placeholder_kpi2 = kpi_col2.empty()
placeholder_kpi3 = kpi_col3.empty()
placeholder_kpi4 = kpi_col4.empty()
placeholder_chart1 = chart_col1.empty()
placeholder_chart2 = chart_col2.empty()

for i in range(200): # Run for 200 iterations for demo purposes
    data = generate_data(simulation_mode)
    
    # Update History
    new_row = pd.DataFrame([data])
    st.session_state['history'] = pd.concat([st.session_state['history'], new_row], ignore_index=True).tail(50)
    df = st.session_state['history']

    # 1. KPI METRICS
    with placeholder_kpi1.container():
        st.metric(label="Grid Frequency", value=f"{data['frequency']} Hz", delta=round(data['frequency']-50.0, 2))
    
    with placeholder_kpi2.container():
        st.metric(label="Line Voltage", value=f"{data['voltage']} V", delta=round(data['voltage']-220.0, 1))
        
    with placeholder_kpi3.container():
        st.metric(label="Transformer Temp", value=f"{data['temp']} °C", delta=round(data['temp']-45.0, 1), delta_color="inverse")
        
    with placeholder_kpi4.container():
        st.metric(label="Vibration Analysis", value=f"{data['vibration']} mm/s", delta_color="inverse")

    # 2. LOGIC & ALERTS (The "Brain" of your system)
    with alert_placeholder.container():
        if data['frequency'] < 49.0:
            st.error(f"CRITICAL: Under-Frequency Detected ({data['frequency']} Hz). Risk of Cascade Failure. AI Rerouting Initiated.")
        elif data['vibration'] > 5.0:
            st.warning(f"MAINTENANCE ALERT: Abnormal Vibration Detected ({data['vibration']} mm/s). Mechanical failure imminent.")
        elif data['temp'] > 75.0:
            st.warning(f"WARNING: Transformer Overheating ({data['temp']} °C). Cooling systems activated.")
        else:
            st.success("System Normal. AI Optimization Active.")

    # 3. REAL-TIME CHARTS
    with placeholder_chart1.container():
        fig_volt = go.Figure()
        fig_volt.add_trace(go.Scatter(y=df['voltage'], x=df['timestamp'], mode='lines', name='Voltage', line=dict(color='#00CC96')))
        fig_volt.add_trace(go.Scatter(y=[220]*len(df), x=df['timestamp'], mode='lines', name='Nominal', line=dict(color='white', dash='dash')))
        fig_volt.update_layout(title="Voltage Stability", template="plotly_dark", height=300, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig_volt, use_container_width=True)

    with placeholder_chart2.container():
        fig_freq = go.Figure()
        fig_freq.add_trace(go.Scatter(y=df['frequency'], x=df['timestamp'], mode='lines', name='Frequency', line=dict(color='#EF553B')))
        fig_freq.add_hline(y=50.0, line_dash="dash", line_color="white")
        fig_freq.update_layout(title="Frequency Deviation", template="plotly_dark", height=300, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig_freq, use_container_width=True)

    time.sleep(1) # Refresh rate