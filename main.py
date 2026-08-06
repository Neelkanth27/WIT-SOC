from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any

app = FastAPI(
    title="Edge SOC Hardware Mitigation API",
    description="Backend API providing system status and hardware signals for Edge SOC mitigation."
)

# Global status dictionary (in production, this would be updated by SOC detection engines)
latest_status: Dict[str, Any] = {
    "hardware_signal": "GREEN",
    "system_health": "NORMAL",
    "threat_level": 0
}


class StatusUpdate(BaseModel):
    hardware_signal: str


@app.get("/", summary="Root status endpoint")
def root():
    return {"message": "Edge SOC Backend is running."}


@app.get("/status", summary="Get latest hardware signal status")
def get_latest_status():
    """
    Returns the latest system status dictionary containing the 'hardware_signal'
    ('GREEN', 'YELLOW', or 'RED') polled by the Raspberry Pi hardware module.
    """
    return latest_status


@app.post("/status", summary="Update hardware signal status (For simulation/testing)")
def update_status(payload: StatusUpdate):
    """
    Simulate state changes (e.g., set hardware_signal to GREEN, YELLOW, or RED).
    """
    signal = payload.hardware_signal.upper()
    if signal not in ["GREEN", "YELLOW", "RED"]:
        raise HTTPException(status_code=400, detail="Invalid signal. Must be GREEN, YELLOW, or RED.")
    
    latest_status["hardware_signal"] = signal
    return {"message": f"Hardware signal updated to {signal}", "status": latest_status}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
