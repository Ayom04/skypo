Here’s a **cleaned-up, clearer, professional** README for your project — short, direct, and free of unnecessary explanations:

---

# **Skypo – Nigeria National Grid Digital Control Center**

A lightweight interactive dashboard that simulates live data from the Nigerian electricity grid and uses a simple AI model to detect anomalies.

---

## **Features**

- Real-time simulated grid voltage data
- AI-powered anomaly detection (Isolation Forest)
- Live dashboard with metrics and charts
- One-click **fault injection** to simulate grid instability or attacks

---

## **Quick Start**

### **1. Create and activate a virtual environment (macOS / zsh)**

```bash
python3 -m venv venv
source venv/bin/activate
```

### **2. Install dependencies**

```bash
pip install -r requirements.txt
```

### **3. Run the dashboard**

```bash
streamlit run app.py
```

Streamlit usually opens automatically at **[http://localhost:8501](http://localhost:8501)**.

---

## **What You’ll See**

- Dashboard title: **Nigeria National Grid: Digital Control Center**
- Sidebar with: **🚨 Inject Fault (Simulate Attack)**
- Live metrics (voltage, AI status, system message)
- Real-time voltage graph
- Temporary voltage drop when a fault is injected

---

## **How It Works (Short)**

- The app generates continuous fake sensor data.
- A simple machine-learning model checks for abnormal patterns.
- When anomalies appear, the dashboard displays a warning and simulated automated response.

---

## **Tech Stack**

- **Streamlit** (UI/Dashboard)
- **Scikit-learn** (Anomaly detection)
- **Plotly** (Live charts)
- **Pandas / NumPy** (Data processing)
- Python **3.8+**

---

## **Troubleshooting**

If Streamlit or any package is missing:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---
