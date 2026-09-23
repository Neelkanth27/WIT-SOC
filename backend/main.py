from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import joblib
import pandas as pd
from datetime import datetime

app = FastAPI(title="Edge SOC Gateway")

# Allow CORS for dashboard access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load your Random Forest Model (ensure the path matches your .pkl file location)
try:
    rf_model = joblib.load("model.pkl") 
    print("SUCCESS: Machine Learning Model loaded.")
except Exception as e:
    print(f"WARNING: Model not found. Running in heuristic-only mode. Error: {e}")
    rf_model = None

# --- NEW: Added 'isolated_ip' to the global state ---
latest_status = {
    "hardware_signal": "GREEN",
    "action": "ALLOW",
    "threat_score": 0.0,
    "isolated_ip": None 
}

@app.post("/api/v1/telemetry")
async def receive_telemetry(payload: dict, request: Request):
    """
    Receives telemetry from endpoint laptops, extracts their dynamic IP,
    runs the ML model, and updates the hardware controller state.
    """
    global latest_status
    
    # --- NEW: Dynamically extract the IP address of the laptop sending the data ---
    client_ip = request.client.host
    print(f"INFO: Telemetry received from {client_ip}")

    # Process payload into dataframe for model prediction (adjust features as per your model)
    try:
        # Example feature extraction based on your prior setup
        features = pd.DataFrame([payload])
        
        if rf_model:
            # Get probability of malicious class (assuming class 1 is malicious)
            prediction_proba = rf_model.predict_proba(features)[0]
            threat_score = round(prediction_proba[1] * 100, 2)
        else:
            # Fallback heuristic if model isn't loaded (e.g., volumetric check)
            threat_score = 95.0 if payload.get("total_fwd_packets", 0) > 1000 else 0.0

        # --- NEW: State Logic with IP Extraction ---
        if threat_score >= 85.0:
            latest_status["hardware_signal"] = "RED"
            latest_status["action"] = "PERM_LOCK"
            latest_status["threat_score"] = threat_score
            latest_status["isolated_ip"] = client_ip  # Save the attacker's IP for the Pi!
            
        elif threat_score >= 50.0 and latest_status["hardware_signal"] != "RED":
            latest_status["hardware_signal"] = "YELLOW"
            latest_status["action"] = "TEMP_ISOLATE"
            latest_status["threat_score"] = threat_score
            # We don't isolate on Yellow, just warn
            
        elif latest_status["hardware_signal"] == "GREEN":
            # Only update green stats if we aren't currently locked down
            latest_status["threat_score"] = threat_score

        return {"status": "success", "processed_ip": client_ip, "threat_score": threat_score}

    except Exception as e:
        print(f"ERROR processing telemetry: {e}")
        return {"status": "error", "message": str(e)}

@app.get("/api/v1/status")
async def get_status():
    """
    The Raspberry Pi polls this endpoint every 0.5 seconds to know what LEDs to light
    up and who to shoot the kill packet to.
    """
    return latest_status

@app.post("/api/v1/reset")
async def reset_status():
    """
    Clears the network lock and resets the system to GREEN.
    """
    global latest_status
    latest_status = {
        "hardware_signal": "GREEN",
        "action": "ALLOW",
        "threat_score": 0.0,
        "isolated_ip": None  # --- NEW: Clear the isolated IP ---
    }
    print("INFO: System state manually reset to GREEN.")
    return {"status": "reset_successful", "current_state": latest_status}

if __name__ == "__main__":
    import uvicorn
    # Bind to 0.0.0.0 so all laptops and the Pi can reach this server
    uvicorn.run(app, host="0.0.0.0", port=8000)