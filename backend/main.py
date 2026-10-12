from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import joblib
import pandas as pd
import os
from datetime import datetime
from database import init_db, log_event, get_recent_logs, get_audit_stats, clear_audit_logs

app = FastAPI(title="Edge SOC Gateway - Autonomous AI Wire-Interposition Trust Layer")

# Allow CORS for dashboard access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize SQLite SIEM Audit Database
init_db()

# Resolve model path across different running directories
def load_threat_model():
    candidate_paths = [
        os.path.join(os.path.dirname(__file__), "model.pkl"),
        os.path.join(os.path.dirname(__file__), "..", "ai_model", "saved_model.pkl"),
        os.path.join(os.path.dirname(__file__), "saved_model.pkl"),
        "backend/model.pkl",
        "ai_model/saved_model.pkl",
        "model.pkl"
    ]
    for path in candidate_paths:
        if os.path.exists(path):
            try:
                model = joblib.load(path)
                print(f"[+] SUCCESS: AI Threat Detection Model loaded from: {path}")
                return model
            except Exception as err:
                print(f"[!] Found model at {path} but failed to load: {err}")
    print("[!] WARNING: Model file not found. Running in heuristic-only mode.")
    return None

rf_model = load_threat_model()

# Global state manager representing the wire-interposition hardware trust layer
latest_status = {
    "hardware_signal": "GREEN",
    "action": "ALLOW",
    "threat_score": 0.0,
    "isolated_ip": None,
    "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}

@app.post("/api/v1/telemetry")
async def receive_telemetry(payload: dict, request: Request):
    """
    Ingests live network flow telemetry from workstations, extracts the dynamic client IP,
    evaluates through dual-layer (Fast-Path Heuristics + Deep ML Random Forest),
    updates hardware state, and logs to SIEM database.
    """
    global latest_status
    
    # Dynamically extract client IP of the workstation sending the telemetry
    client_ip = request.client.host if request.client else "127.0.0.1"
    print(f"[*] Telemetry received from: {client_ip}")

    # Standardize input features
    flow_duration = float(payload.get("flow_duration", 0.0))
    flow_bytes_sec = float(payload.get("flow_bytes_sec", 0.0))
    total_fwd_packets = int(payload.get("total_fwd_packets", 0))
    total_bwd_packets = int(payload.get("total_bwd_packets", 0))
    fwd_packet_length_mean = float(payload.get("fwd_packet_length_mean", 0.0))

    # --- LAYER 1: Fast-Path Heuristic Engine (< 10ms) ---
    is_volumetric_spike = (flow_bytes_sec > 1000000.0) or (total_fwd_packets > 1000)
    is_stealth_recon = (total_fwd_packets <= 2 and total_bwd_packets == 0 and flow_duration < 25.0)

    # --- LAYER 2: Machine Learning Random Forest Feature Analysis ---
    threat_score = 0.0
    threat_class = "BENIGN"
    engine_used = "FAST_PATH_HEURISTIC"

    try:
        if rf_model:
            engine_used = "ML_RANDOM_FOREST"
            feature_row = pd.DataFrame([{
                "flow_duration": flow_duration,
                "flow_bytes_sec": flow_bytes_sec,
                "total_fwd_packets": total_fwd_packets,
                "total_bwd_packets": total_bwd_packets,
                "fwd_packet_length_mean": fwd_packet_length_mean
            }])
            
            # Predict probabilities: [P(Benign: 0), P(Suspicious: 1), P(Malicious: 2)]
            probabilities = rf_model.predict_proba(feature_row)[0]
            classes = list(rf_model.classes_)
            
            p_benign = probabilities[classes.index(0)] if 0 in classes else 0.0
            p_suspicious = probabilities[classes.index(1)] if 1 in classes else 0.0
            p_malicious = probabilities[classes.index(2)] if 2 in classes else 0.0

            if p_malicious >= 0.5 or is_volumetric_spike:
                threat_class = "MALICIOUS"
                threat_score = round(max(p_malicious * 100.0, 95.0), 2)
            elif p_suspicious >= 0.5 or is_stealth_recon:
                threat_class = "SUSPICIOUS"
                threat_score = round(max(p_suspicious * 75.0, 60.0), 2)
            else:
                threat_class = "BENIGN"
                threat_score = round(p_malicious * 30.0 + p_suspicious * 15.0, 2)
        else:
            # Fallback heuristic scoring if model not loaded
            if is_volumetric_spike:
                threat_class = "MALICIOUS"
                threat_score = 98.0
            elif is_stealth_recon:
                threat_class = "SUSPICIOUS"
                threat_score = 65.0
            else:
                threat_class = "BENIGN"
                threat_score = 5.0

        threat_score = float(threat_score)

        # --- SPECULATIVE POLICY & DECISION ENGINE ---
        if threat_score >= 85.0:
            latest_status["hardware_signal"] = "RED"
            latest_status["action"] = "PERM_LOCK"
            latest_status["threat_score"] = threat_score
            latest_status["isolated_ip"] = client_ip
            
        elif threat_score >= 50.0 and latest_status["hardware_signal"] != "RED":
            latest_status["hardware_signal"] = "YELLOW"
            latest_status["action"] = "TEMP_ISOLATE"
            latest_status["threat_score"] = threat_score
            
        elif latest_status["hardware_signal"] != "RED":
            # Reversible speculative execution: return to Green if safe
            latest_status["hardware_signal"] = "GREEN"
            latest_status["action"] = "ALLOW"
            latest_status["threat_score"] = threat_score

        latest_status["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # --- LOG INTO SQLite SIEM AUDIT DATABASE ---
        log_event(
            client_ip=client_ip,
            payload=payload,
            threat_score=threat_score,
            threat_class=threat_class,
            action=latest_status["action"],
            hardware_signal=latest_status["hardware_signal"],
            detection_engine=engine_used
        )

        return {
            "status": "success",
            "processed_ip": client_ip,
            "threat_score": threat_score,
            "threat_score_percentage": threat_score,
            "threat_class": threat_class,
            "action": latest_status["action"],
            "hardware_signal": latest_status["hardware_signal"]
        }

    except Exception as e:
        print(f"[!] ERROR processing telemetry: {e}")
        return {"status": "error", "message": str(e)}

@app.get("/api/v1/status")
async def get_status():
    """
    Polled every 0.5s by the Raspberry Pi / Mock Hardware Controller
    to actuate physical LEDs and trigger UDP kill packets.
    """
    return latest_status

@app.get("/api/v1/logs")
async def get_logs(limit: int = 50):
    """
    Provides real-time event logs for the Streamlit SOC Dashboard.
    """
    return get_recent_logs(limit=limit)

@app.get("/api/v1/stats")
async def get_stats():
    """
    Provides aggregated analytics for the Streamlit SOC Dashboard.
    """
    stats = get_audit_stats()
    stats["current_signal"] = latest_status["hardware_signal"]
    stats["current_action"] = latest_status["action"]
    stats["current_threat_score"] = latest_status["threat_score"]
    stats["isolated_ip"] = latest_status["isolated_ip"]
    return stats

@app.post("/api/v1/reset")
async def reset_status():
    """
    Clears the network isolation state, unfreezes the lock, and returns to GREEN.
    """
    global latest_status
    latest_status = {
        "hardware_signal": "GREEN",
        "action": "ALLOW",
        "threat_score": 0.0,
        "isolated_ip": None,
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    print("[*] INFO: System state manually reset to GREEN.")
    return {"status": "reset_successful", "current_state": latest_status}

if __name__ == "__main__":
    import uvicorn
    # Bind to 0.0.0.0 so all laptops and the Pi can reach this gateway
    uvicorn.run(app, host="0.0.0.0", port=8000)