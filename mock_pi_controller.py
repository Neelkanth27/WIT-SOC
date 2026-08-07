import time
import requests

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------
BACKEND_URL = None
POLL_INTERVAL = 0.5  # 500 ms poll rate

# Visual terminal indicators for software simulation
SIGNAL_VISUALS = {
    "GREEN":  "🟢 [GREEN LED: ON ]  🟡 [YELLOW LED: OFF]  🔴 [RED LED: OFF]",
    "YELLOW": "⚪ [GREEN LED: OFF]  🟡 [YELLOW LED: ON ]  🔴 [RED LED: OFF]",
    "RED":    "⚪ [GREEN LED: OFF]  🟡 [YELLOW LED: OFF]  🔴 [RED LED: ON ]"
}


def configure_soc_server():
    """Prompts the user for the backend IP during demo setup."""
    global BACKEND_URL
    print("[?] Enter the Backend Server IP (e.g., 10.45.2.100) or press Enter for localhost:")
    server_ip = input("> ").strip()
    if not server_ip:
        server_ip = "127.0.0.1"
    BACKEND_URL = f"http://{server_ip}:8000/api/v1/status"
    print(f"[+] Server URL configured as: {BACKEND_URL}")


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
    print("=" * 70)

    # Step 1: Manually configure the SOC Backend Server IP
    configure_soc_server()

    print(f"[*] Starting polling loop for: {BACKEND_URL}")
    print(f"[*] Poll Interval: {POLL_INTERVAL} seconds. Press Ctrl+C to exit.\n")

    # Step 2: Main polling loop
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
                print("\r[NETWORK ERROR] Waiting for FastAPI backend connection...", end="", flush=True)

            time.sleep(POLL_INTERVAL)

    except KeyboardInterrupt:
        print("\n\n[INFO] Simulation stopped cleanly.")


if __name__ == "__main__":
    main()
