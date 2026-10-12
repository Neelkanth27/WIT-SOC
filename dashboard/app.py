import streamlit as st
import requests
import pandas as pd
import time
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="WIT-SOC | Autonomous AI SOC Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #00d2ff;
        margin-bottom: 0px;
    }
    .sub-title {
        font-size: 1.0rem;
        color: #8892b0;
        margin-bottom: 20px;
    }
    .metric-box {
        background-color: #111936;
        border: 1px solid #1e295d;
        border-radius: 8px;
        padding: 15px;
        text-align: center;
    }
    .status-green {
        background: linear-gradient(90deg, #0f5132 0%, #198754 100%);
        color: #d1e7dd;
        padding: 16px;
        border-radius: 8px;
        font-weight: bold;
        font-size: 1.2rem;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 0 15px rgba(25, 135, 84, 0.4);
    }
    .status-yellow {
        background: linear-gradient(90deg, #664d03 0%, #ffc107 100%);
        color: #000;
        padding: 16px;
        border-radius: 8px;
        font-weight: bold;
        font-size: 1.2rem;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 0 15px rgba(255, 193, 7, 0.4);
    }
    .status-red {
        background: linear-gradient(90deg, #842029 0%, #dc3545 100%);
        color: #fff;
        padding: 16px;
        border-radius: 8px;
        font-weight: bold;
        font-size: 1.2rem;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 0 20px rgba(220, 53, 69, 0.7);
        animation: pulse 1.5s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.01); }
        100% { transform: scale(1); }
    }
</style>
""", unsafe_allow_html=True)

# Sidebar Configuration
st.sidebar.image("https://img.icons8.com/fluency/96/shield.png", width=64)
st.sidebar.title("SOC Control Panel")
st.sidebar.markdown("**WIT-SOC:** Wire-Interposition Trust Layer")
st.sidebar.caption("Vishwakarma Institute of Technology | Group 9")

gateway_host = st.sidebar.text_input("Gateway Base URL", value="http://127.0.0.1:8000")
refresh_rate = st.sidebar.slider("Polling Frequency (seconds)", min_value=1, max_value=5, value=2)

st.sidebar.markdown("---")
st.sidebar.subheader("Enforcement Actions")

if st.sidebar.button("🔄 Emergency System Reset", use_container_width=True, type="primary"):
    try:
        res = requests.post(f"{gateway_host}/api/v1/reset", timeout=2)
        if res.status_code == 200:
            st.sidebar.success("Gateway reset to GREEN state!")
            time.sleep(0.5)
            st.rerun()
    except Exception as e:
        st.sidebar.error(f"Reset failed: {e}")

st.sidebar.info("""
**Architecture Layers:**
1. **Telemetry Agent:** Endpoints streaming flow metrics
2. **Gateway:** Dual-layer ML + Heuristic Engine
3. **Trust Anchor:** Raspberry Pi Out-of-Band Hardware
4. **Quarantine:** Automated UDP Wi-Fi severance
""")

# Main Content
st.markdown('<div class="main-title">🛡️ WIT-SOC: Autonomous AI Security Operations Center</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Real-Time Threat Telemetry, Speculative Hardware Policy & Zero-Trust Quarantine</div>', unsafe_allow_html=True)

@st.fragment(run_every=f"{refresh_rate}s")
def render_live_dashboard():
    # 1. Fetch current live status
    try:
        status_res = requests.get(f"{gateway_host}/api/v1/status", timeout=1.5)
        status_data = status_res.json() if status_res.status_code == 200 else {}
    except Exception:
        status_data = {}

    # 2. Fetch stats
    try:
        stats_res = requests.get(f"{gateway_host}/api/v1/stats", timeout=1.5)
        stats_data = stats_res.json() if stats_res.status_code == 200 else {}
    except Exception:
        stats_data = {}

    # 3. Fetch recent audit logs
    try:
        logs_res = requests.get(f"{gateway_host}/api/v1/logs?limit=25", timeout=1.5)
        logs_data = logs_res.json() if logs_res.status_code == 200 else []
    except Exception:
        logs_data = []

    if not status_data:
        st.warning(f"⚠️ Unable to connect to Gateway at `{gateway_host}`. Ensure `backend/main.py` is running.")
        return

    signal = status_data.get("hardware_signal", "GREEN")
    threat_score = float(status_data.get("threat_score", 0.0))
    action = status_data.get("action", "ALLOW")
    isolated_ip = status_data.get("isolated_ip")

    # Banner Status
    if signal == "RED":
        st.markdown(f"""
        <div class="status-red">
            🚨 CRITICAL THREAT ACTIVE | HARDWARE SIGNAL: RED | ACTION: PERM_LOCK<br>
            <span style="font-size: 0.95rem; font-weight: normal;">
                Attacker IP <b>{isolated_ip}</b> isolated out-of-band. Host Wi-Fi adapter severed.
            </span>
        </div>
        """, unsafe_allow_html=True)
    elif signal == "YELLOW":
        st.markdown(f"""
        <div class="status-yellow">
            🟡 SPECULATIVE SUSPICIOUS ANOMALY | HARDWARE SIGNAL: YELLOW | ACTION: TEMP_ISOLATE<br>
            <span style="font-size: 0.95rem; font-weight: normal;">
                Early threshold tripped ({threat_score}%). Monitoring for escalation or reversible clear.
            </span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="status-green">
            🟢 NETWORK INTEGRITY NORMAL | HARDWARE SIGNAL: GREEN | ACTION: ALLOW<br>
            <span style="font-size: 0.95rem; font-weight: normal;">
                All endpoints verified benign. Wire-interposition layer actively inspecting packets.
            </span>
        </div>
        """, unsafe_allow_html=True)

    # 4 Key Metrics
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Live Threat Confidence", f"{threat_score}%", delta=f"{action}", delta_color="inverse" if threat_score > 50 else "normal")
    with c2:
        st.metric("Hardware Signal", f"{signal} LED", delta="Out-of-band Pi" if signal == "RED" else "Nominal")
    with c3:
        st.metric("Enforcement State", f"{action}", delta="Zero-Trust Policy")
    with c4:
        st.metric("Quarantined Endpoint", f"{isolated_ip if isolated_ip else 'None'}", delta="Network Interface Severed" if isolated_ip else "All Connected")

    st.markdown("---")

    # Analytics & Distribution Row
    col_chart, col_traffic = st.columns([2, 1])

    with col_chart:
        st.subheader("📈 Real-Time Flow Telemetry Stream")
        if logs_data:
            df_logs = pd.DataFrame(logs_data)
            chart_df = df_logs[["id", "threat_score", "flow_bytes_sec"]].copy()
            chart_df.rename(columns={"threat_score": "Threat Score (%)", "flow_bytes_sec": "Flow Rate (Bytes/s)"}, inplace=True)
            chart_df = chart_df.sort_values("id")
            st.line_chart(chart_df.set_index("id")[["Threat Score (%)"]])
        else:
            st.info("Awaiting telemetry stream from endpoints...")

    with col_traffic:
        st.subheader("📊 Policy Verdict Breakdown")
        g_count = stats_data.get("green_count", 0)
        y_count = stats_data.get("yellow_count", 0)
        r_count = stats_data.get("red_count", 0)
        
        stat_df = pd.DataFrame({
            "Verdict": ["🟢 Benign (ALLOW)", "🟡 Speculative (TEMP)", "🔴 Malicious (LOCK)"],
            "Flow Packets": [g_count, y_count, r_count]
        })
        st.bar_chart(stat_df.set_index("Verdict"))

    st.markdown("---")

    # SIEM Audit Log Table
    st.subheader("📋 SIEM Audit Log (SQLite Hardware-Verified Ledger)")
    if logs_data:
        df_display = pd.DataFrame(logs_data)
        columns_to_show = [
            "id", "timestamp", "client_ip", "threat_score", 
            "threat_class", "action", "hardware_signal", "detection_engine"
        ]
        available_cols = [c for c in columns_to_show if c in df_display.columns]
        st.dataframe(
            df_display[available_cols], 
            use_container_width=True, 
            hide_index=True
        )
    else:
        st.caption("No logs recorded yet. Run `endpoint/telemetry_simulator.py` to stream live traffic.")

# Invoke live dashboard
render_live_dashboard()
