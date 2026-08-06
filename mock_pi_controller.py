import time
import requests

# Backend API configuration (Local server)
BACKEND_URL = "http://127.0.0.1:8000/status"
POLL_INTERVAL = 0.5  # 500 ms poll rate

# Visual indicators for terminal output
SIGNAL_VISUALS = {
    "GREEN":  "🟢 [GREEN LED: ON ]  🟡 [YELLOW LED: OFF]  🔴 [RED LED: OFF]",
    "YELLOW": "⚪ [GREEN LED: OFF]  🟡 [YELLOW LED: ON ]  🔴 [RED LED: OFF]",
    "RED":    "⚪ [GREEN LED: OFF]  🟡 [YELLOW LED: OFF]  🔴 [RED LED: ON ]"
}


def update_mock_led_state(signal: str):
    """Simulates physical LED state changes on terminal screen."""
    signal = str(signal).upper().strip()
    
    visual = SIGNAL_VISUALS.get(signal)
    if visual:
        print(f"\r[STATUS: {signal:6s}] {visual}", end="", flush=True)
    else:
        print(f"\r[STATUS: UNKNOWN] ⚪ [GREEN LED: OFF]  🟡 [YELLOW LED: OFF]  🔴 [RED LED: OFF]", end="", flush=True)


def main():
    print("=" * 70)
    print("      SOFTWARE SIMULATION: Raspberry Pi Hardware LED Controller")
    print("      (Simulating gpiozero hardware polling without physical Pi)")
    print(f"      Polling Backend: {BACKEND_URL} every {POLL_INTERVAL}s")
    print("=" * 70)
    print("Press Ctrl+C to stop simulation.\n")

    try:
        while True:
            try:
                response = requests.get(BACKEND_URL, timeout=1.0)
                if response.status_code == 200:
                    data = response.json()
                    hardware_signal = data.get("hardware_signal", "UNKNOWN")
                    update_mock_led_state(hardware_signal)
                else:
                    update_mock_led_state("UNKNOWN")
            except requests.exceptions.RequestException:
                print("\r[NETWORK ERROR] Waiting for FastAPI backend to start...", end="", flush=True)

            time.sleep(POLL_INTERVAL)

    except KeyboardInterrupt:
        print("\n\n[INFO] Simulation stopped cleanly.")


if __name__ == "__main__":
    main()
