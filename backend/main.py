from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np
import os
import sqlite3
from datetime import datetime

app = FastAPI(title="WIT-SOC AI Backend Engine")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

DB_FILE = "soc_audit.db"

def init_db():
    conn = sqlite3.connect(DB_FILE, timeout=10)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS telemetry_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, flow_duration REAL, flow_bytes_sec REAL, 
            threat_score REAL, action_taken TEXT, hardware_signal TEXT, detection_engine TEXT)''')
    conn.commit()
    conn.close()

init_db()

latest_status = {"hardware_signal": "GREEN", "action": "ALLOW", "threat_score": 0.0, "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
BASE_DIR = os.path.dirname(os.path.dirname(__file__)) if "__file__" in locals() else os.getcwd()
MODEL_PATH = os.path.join(BASE_DIR, "ai_model", "saved_model.pkl")

try:
    model = joblib.load(MODEL_PATH)
    print("[+] AI Model successfully loaded into Edge SOC memory.")
except Exception as e:
    print(f"[!] Warning: AI Model offline ({e}). Heuristic mode active.")
    model = None

class TelemetryPayload(BaseModel):
    flow_duration: float
    flow_bytes_sec: float
    total_fwd_packets: int
    total_bwd_packets: int
    fwd_packet_length_mean: float

@app.post("/api/v1/telemetry")
def analyze_telemetry(data: TelemetryPayload):
    global latest_status
    score_percent = 0.0
    action = "ALLOW"
    led_color = "GREEN"
    detection_engine = "AI Engine"

    if data.total_bwd_packets == 0 and data.total_fwd_packets > 1000:
        score_percent = 99.9
        action = "PERM_LOCK"
        led_color = "RED"
        detection_engine = "Heuristic: Volumetric DDoS"
    elif data.flow_duration < 20.0 and data.total_fwd_packets == 1 and data.total_bwd_packets == 0:
        score_percent = 70.0  
        action = "TEMP_ISOLATE"
        led_color = "YELLOW"
        detection_engine = "Heuristic: Stealth Port Scan"
    elif data.fwd_packet_length_mean > 5000.0:
        score_percent = 98.0
        action = "PERM_LOCK"
        led_color = "RED"
        detection_engine = "Heuristic: Data Exfiltration"
    elif model is not None:
        payload_dict = {"flow_duration": data.flow_duration, "flow_bytes_sec": data.flow_bytes_sec, 
                        "total_fwd_packets": data.total_fwd_packets, "total_bwd_packets": data.total_bwd_packets, "fwd_packet_length_mean": data.fwd_packet_length_mean}
        features_df = pd.DataFrame([list(model.feature_names_in_)], columns=list(model.feature_names_in_)) if hasattr(model, "feature_names_in_") else pd.DataFrame([payload_dict])
        features_df.iloc[0] = [data.flow_duration, data.flow_bytes_sec, data.total_fwd_packets, data.total_bwd_packets, data.fwd_packet_length_mean]
        
        probabilities = model.predict_proba(features_df)[0]
        classes = list(model.classes_)
        malicious_idx = next((idx for idx, cls in enumerate(classes) if str(cls).strip().lower() in ['2', '2.0', '1', '1.0', 'ddos', 'malicious', 'attack', 'portscan']), 1 if len(classes) > 1 else 0)
        score_percent = round(float(probabilities[malicious_idx]) * 100, 2)

        if score_percent >= 85.0:
            action, led_color = "PERM_LOCK", "RED"
        elif score_percent >= 65.0:
            action, led_color = "TEMP_ISOLATE", "YELLOW"

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if latest_status["action"] != "PERM_LOCK":
        latest_status = {"hardware_signal": led_color, "action": action, "threat_score": score_percent, "last_updated": current_time}

    try:
        conn = sqlite3.connect(DB_FILE, timeout=10)
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO telemetry_logs (timestamp, flow_duration, flow_bytes_sec, threat_score, action_taken, hardware_signal, detection_engine)
                          VALUES (?, ?, ?, ?, ?, ?, ?)''', (current_time, data.flow_duration, data.flow_bytes_sec, score_percent, action, led_color, detection_engine))
        conn.commit()
        conn.close()
    except Exception: pass
    return {"threat_score_percentage": score_percent, "action": action, "hardware_signal": led_color, "engine": detection_engine}

@app.get("/api/v1/logs")
def get_audit_logs(limit: int = 20):
    conn = sqlite3.connect(DB_FILE, timeout=10)
    conn.row_factory = sqlite3.Row  
    rows = [dict(row) for row in conn.cursor().execute('SELECT * FROM telemetry_logs ORDER BY id DESC LIMIT ?', (limit,)).fetchall()]
    conn.close()
    return {"logs": rows}

@app.get("/api/v1/status")
def get_hardware_status():
    return latest_status

@app.post("/api/v1/reset")
def reset_hardware_status():
    global latest_status
    latest_status = {"hardware_signal": "GREEN", "action": "ALLOW", "threat_score": 0.0, "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    return {"status": "SUCCESS"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)