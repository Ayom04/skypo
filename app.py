import streamlit as st
import pandas as pd
import numpy as np
import time
from sklearn.ensemble import IsolationForest
import plotly.graph_objects as go

# 1. PAGE SETUP
st.set_page_config(page_title="Nigeria Smart Grid Brain", layout="wide")
st.title("⚡ Nigeria National Grid: Digital Control Center")

# Sidebar for "God Mode" (Hackathon controls)
st.sidebar.header("Simulation Controls")
inject_fault = st.sidebar.button("🚨 INJECT FAULT (Simulate Attack)")

# 2. GENERATE LIVE DATA (Simulating Nanosensors)
# Normal grid voltage is usually around 330kV +/- 5%


def get_sensor_data(fault_active=False):
    if fault_active:
        # Generate chaotic data (Voltage collapse or spike)
        voltage = np.random.normal(150, 50, 1)  # Drop to 150kV
    else:
        # Generate normal stable data
        voltage = np.random.normal(330, 5, 1)   # Stable 330kV
    return voltage[0]


# 3. THE "AI BRAIN" (Isolation Forest)
# We train it instantly on "normal" historical data
rng = np.random.RandomState(42)
X_train = 0.3 * rng.randn(100, 1) + 330  # Fake normal history
clf = IsolationForest(random_state=42, contamination=0.01)
clf.fit(X_train)

# 4. MAIN DASHBOARD LOOP
placeholder = st.empty()
data_history = []

# Loop to simulate real-time feed
for seconds in range(200):
    with placeholder.container():
        # A. Fetch Data
        # If user clicked "Inject Fault", we force a drop for a few seconds
        is_fault = inject_fault and (seconds > 5 and seconds < 15)
        new_voltage = get_sensor_data(fault_active=is_fault)

        # B. AI Prediction (-1 is Anomaly, 1 is Normal)
        prediction = clf.predict([[new_voltage]])[0]
        status = "✅ STABLE" if prediction == 1 else "⚠️ CRITICAL FAULT DETECTED"
        color = "green" if prediction == 1 else "red"

        # C. Visualization (The "War Room")
        kpi1, kpi2, kpi3 = st.columns(3)
        kpi1.metric(label="Grid Voltage (kV)",
                    value=f"{new_voltage:.2f}", delta=f"{new_voltage-330:.2f}")
        kpi2.metric(label="AI Status", value=status)

        # Rerouting Logic (The Solution)
        if prediction == -1:
            kpi3.error("⚡ REROUTING POWER TO LOOP B...")
        else:
            kpi3.success("System Optimized")

        # D. Live Graph
        data_history.append(new_voltage)
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            y=data_history[-50:], mode='lines', name='Voltage'))
        fig.update_layout(title="Real-Time Nanosensor Feed",
                          yaxis_range=[0, 400])
        st.plotly_chart(fig, use_container_width=True)

        time.sleep(0.5)
