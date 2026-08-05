from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
import os
import sqlite3
from datetime import datetime

# 1. Initialize the FastAPI Application
app = FastAPI(
    title="WIT-SOC AI Backend Engine",
    description="Microsecond Threat Scoring & Speculative Hardware Isolation API",
    version="1.0.0"
)

# 2. Database Initialization (SQLite)
# This creates a local database file to log all AI decisions (SIEM Simulation)
DB_FILE = "soc_audit.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS telemetry_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            flow_duration REAL,
            flow_bytes_sec REAL,
            threat_score REAL,
            action_taken TEXT,
            hardware_signal TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Run the database initialization when the server starts
init_db()

# 3. Dynamically Locate and Load the AI Model
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "ai_model", "saved_model.pkl")

try:
    model = joblib.load(MODEL_PATH)
    print("[+] AI Model successfully loaded into Edge SOC memory.")
except Exception as e:
    print(f"[!] Critical Error: Could not load model from {MODEL_PATH}. Details: {e}")
    model = None

# 4. Data Validation Schema (Pydantic Bouncer)
class TelemetryPayload(BaseModel):
    flow_duration: float
    flow_bytes_sec: float
    total_fwd_packets: int
    total_bwd_packets: int
    fwd_packet_length_mean: float

# 5. Core Telemetry Analysis & Speculative Policy Endpoint
@app.post("/api/v1/telemetry")
def analyze_telemetry(data: TelemetryPayload):
    if model is None:
        raise HTTPException(status_code=500, detail="AI Model Engine is offline.")

    # Convert incoming telemetry into a 2D NumPy array for the AI
    features = np.array([[
        data.flow_duration,
        data.flow_bytes_sec,
        data.total_fwd_packets,
        data.total_bwd_packets,
        data.fwd_packet_length_mean
    ]])

    # Calculate class probabilities and isolate Malicious probability (Class 2)
    probabilities = model.predict_proba(features)[0]
    classes = list(model.classes_)
    malicious_score = probabilities[classes.index(2)] if 2 in classes else 0.0
    score_percent = round(float(malicious_score) * 100, 2)

    # --- SPECULATIVE HARDWARE THRESHOLD LOGIC (PATENT ENGINE) ---
    if score_percent >= 85.0:
        action = "PERM_LOCK"
        led_color = "RED"
    elif score_percent >= 65.0:
        action = "TEMP_ISOLATE"
        led_color = "YELLOW"
    else:
        action = "ALLOW"
        led_color = "GREEN"

    # --- LOG DECISION TO SIEM DATABASE ---
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('''
            INSERT INTO telemetry_logs (timestamp, flow_duration, flow_bytes_sec, threat_score, action_taken, hardware_signal)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (current_time, data.flow_duration, data.flow_bytes_sec, score_percent, action, led_color))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[!] Database logging failed: {e}")

    # Return the verdict back to the requester
    return {
        "threat_score_percentage": score_percent,
        "action": action,
        "hardware_signal": led_color
    }