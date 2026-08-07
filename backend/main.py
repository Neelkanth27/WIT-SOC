from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np
import os
import sqlite3
import socket
import threading
import time
from datetime import datetime

# =====================================================================
# 1. INITIALIZE FASTAPI & CORS (Allows Frontend Dashboard access)
# =====================================================================
app = FastAPI(
    title="WIT-SOC AI Backend Engine",
    description="Microsecond Hybrid Threat Analysis & Edge Isolation API",
    version="2.0.0"
)

# Enable CORS so Teammate 2's frontend can fetch data without browser blocks
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================================================
# 2. DATABASE INITIALIZATION (SQLite SIEM Audit Trail)
# =====================================================================
DB_FILE = "soc_audit.db"

def init_db():
    conn = sqlite3.connect(DB_FILE, timeout=10)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS telemetry_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            flow_duration REAL,
            flow_bytes_sec REAL,
            threat_score REAL,
            action_taken TEXT,
            hardware_signal TEXT,
            detection_engine TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Global state to keep track of the latest status for instant hardware polling
latest_status = {
    "hardware_signal": "GREEN",
    "action": "ALLOW",
    "threat_score": 0.0,
    "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}

# Alias for hardware status route consistency
global_hardware_state = latest_status

# =====================================================================
# 3. DYNAMIC UDP AUTO-DISCOVERY BEACON (Zero-Config Network Discovery)
# =====================================================================
UDP_PORT = 9999
BEACON_MESSAGE = b"WIT_SOC_SERVER_BEACON"

def udp_beacon_thread():
    """Silently broadcasts a UDP beacon so agents auto-discover this server IP."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.settimeout(0.2)
    
    print(f"[*] UDP Auto-Discovery Beacon started on port {UDP_PORT}...")
    while True:
        try:
            sock.sendto(BEACON_MESSAGE, ('<broadcast>', UDP_PORT))
        except Exception as e:
            pass
        time.sleep(2)  # Broadcast every 2 seconds

# Start the UDP beacon in a background thread
beacon_thread = threading.Thread(target=udp_beacon_thread, daemon=True)
beacon_thread.start()

# =====================================================================
# 4. LOAD AI MODEL ENGINE
# =====================================================================
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "ai_model", "saved_model.pkl")

try:
    model = joblib.load(MODEL_PATH)
    print("[+] AI Model successfully loaded into Edge SOC memory.")
    if hasattr(model, "feature_names_in_"):
        print(f"[*] Model Feature Order: {list(model.feature_names_in_)}")
except Exception as e:
    print(f"[!] Warning: AI Model offline ({e}). Heuristic mode active.")
    model = None

# =====================================================================
# 5. DATA SCHEMAS
# =====================================================================
class TelemetryPayload(BaseModel):
    flow_duration: float
    flow_bytes_sec: float
    total_fwd_packets: int
    total_bwd_packets: int
    fwd_packet_length_mean: float

# =====================================================================
# 6. CORE TELEMETRY INGESTION & HYBRID ENGINE
# =====================================================================
@app.post("/api/v1/telemetry")
def analyze_telemetry(data: TelemetryPayload):
    global latest_status
    score_percent = 0.0
    action = "ALLOW"
    led_color = "GREEN"
    detection_engine = "AI Engine"

    # --- LAYER 1: HEURISTIC ENGINE (Fast-Path Signatures) ---
    
    # Signature 1: Volumetric DDoS (Massive forward flood, no backward response)
    if data.total_bwd_packets == 0 and data.total_fwd_packets > 1000:
        score_percent = 99.9
        action = "PERM_LOCK"
        led_color = "RED"
        detection_engine = "Heuristic: Volumetric DDoS"
        print(f"[!] HYBRID TRIGGER: Volumetric DDoS Intercepted!")

    # Signature 2: Stealth Port Scan (Single packet, ultra-fast connection attempt)
    elif data.flow_duration < 20.0 and data.total_fwd_packets == 1 and data.total_bwd_packets == 0:
        score_percent = 95.0
        action = "PERM_LOCK"
        led_color = "RED"
        detection_engine = "Heuristic: Stealth Port Scan"
        print(f"[!] HYBRID TRIGGER: Stealth Port Scan Intercepted!")

    # Signature 3: Data Exfiltration (Massive abnormal outbound packet size)
    elif data.fwd_packet_length_mean > 5000.0:
        score_percent = 98.0
        action = "PERM_LOCK"
        led_color = "RED"
        detection_engine = "Heuristic: Data Exfiltration"
        print(f"[!] HYBRID TRIGGER: Data Exfiltration Intercepted!")

    # --- LAYER 2: RANDOM FOREST AI ENGINE (Complex Threat Analysis) ---
    elif model is not None:
        payload_dict = {
            "flow_duration": data.flow_duration,
            "flow_bytes_sec": data.flow_bytes_sec,
            "total_fwd_packets": data.total_fwd_packets,
            "total_bwd_packets": data.total_bwd_packets,
            "fwd_packet_length_mean": data.fwd_packet_length_mean
        }

        if hasattr(model, "feature_names_in_"):
            cols = list(model.feature_names_in_)
            val_map = [
                data.flow_duration,
                data.flow_bytes_sec,
                data.total_fwd_packets,
                data.total_bwd_packets,
                data.fwd_packet_length_mean
            ]
            features_df = pd.DataFrame([val_map], columns=cols)
        else:
            features_df = pd.DataFrame([payload_dict])

        probabilities = model.predict_proba(features_df)[0]
        classes = list(model.classes_)

        malicious_idx = None
        for idx, cls in enumerate(classes):
            cls_str = str(cls).strip().lower()
            if cls_str in ['2', '2.0', '1', '1.0', 'ddos', 'malicious', 'attack', 'portscan']:
                malicious_idx = idx
                break

        if malicious_idx is None:
            malicious_idx = 1 if len(classes) > 1 else 0

        malicious_score = probabilities[malicious_idx]
        score_percent = round(float(malicious_score) * 100, 2)

        if score_percent >= 85.0:
            action = "PERM_LOCK"
            led_color = "RED"
        elif score_percent >= 65.0:
            action = "TEMP_ISOLATE"
            led_color = "YELLOW"

    # Update in-memory state for Raspberry Pi / Dashboard status headers
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    latest_status = {
        "hardware_signal": led_color,
        "action": action,
        "threat_score": score_percent,
        "last_updated": current_time
    }

    # --- LOG TO SIEM AUDIT DATABASE ---
    try:
        conn = sqlite3.connect(DB_FILE, timeout=10)
        cursor = conn.cursor()
        
        # Schema migration check
        cursor.execute("PRAGMA table_info(telemetry_logs)")
        columns = [column[1] for column in cursor.fetchall()]
        if 'detection_engine' not in columns:
            cursor.execute("ALTER TABLE telemetry_logs ADD COLUMN detection_engine TEXT")

        cursor.execute('''
            INSERT INTO telemetry_logs (timestamp, flow_duration, flow_bytes_sec, threat_score, action_taken, hardware_signal, detection_engine)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (current_time, data.flow_duration, data.flow_bytes_sec, score_percent, action, led_color, detection_engine))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[!] Database logging failed: {e}")

    return {
        "threat_score_percentage": score_percent,
        "action": action,
        "hardware_signal": led_color,
        "engine": detection_engine
    }

# =====================================================================
# 7. TEAMMATES API ENDPOINTS (Frontend Dashboard & Raspberry Pi)
# =====================================================================
@app.get("/api/v1/logs")
def get_audit_logs(limit: int = 20):
    """API for Teammate 2 (Dashboard): Fetches recent SIEM logs for UI tables/charts."""
    try:
        conn = sqlite3.connect(DB_FILE, timeout=10)
        conn.row_factory = sqlite3.Row  # Returns rows as key-value dicts
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, timestamp, flow_duration, flow_bytes_sec, threat_score, action_taken, hardware_signal, detection_engine 
            FROM telemetry_logs 
            ORDER BY id DESC 
            LIMIT ?
        ''', (limit,))
        rows = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return {"logs": rows}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/status")
def get_hardware_status():
    """API for Teammate 3 (Raspberry Pi) & Dashboard Header: Returns live signal state."""
    return latest_status


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)