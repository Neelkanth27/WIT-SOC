import time
import socket
import requests
import sys

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------
BACKEND_URL = None
POLL_INTERVAL = 0.5  # 500 ms poll rate
UDP_PORT = 9999

# Visual terminal indicators for software simulation
SIGNAL_VISUALS = {
    "GREEN":  "🟢 [GREEN LED: ON ]  🟡 [YELLOW LED: OFF]  🔴 [RED LED: OFF]  (Traffic Normal)",
    "YELLOW": "⚪ [GREEN LED: OFF]  🟡 [YELLOW LED: ON ]  🔴 [RED LED: OFF]  (Speculative Alert)",
    "RED":    "⚪ [GREEN LED: OFF]  🟡 [YELLOW LED: OFF]  🔴 [RED LED: ON ]  (QUARANTINE ENFORCED)"
}

def configure_soc_server():
    """Configures the backend IP via command line arguments or user prompt."""
    global BACKEND_URL
    
    server_ip = None
    if len(sys.argv) > 1 and not sys.argv[1].startswith("-"):
        server_ip = sys.argv[1].strip()
    elif "--server-ip" in sys.argv:
        idx = sys.argv.index("--server-ip")
        if idx + 1 < len(sys.argv):
            server_ip = sys.argv[idx + 1].strip()
            
    if not server_ip:
        print("[?] Enter Backend Server IP (or press Enter for localhost 127.0.0.1):")
        server_ip = input("> ").strip()
        
    if not server_ip:
        server_ip = "127.0.0.1"
        
    BACKEND_URL = f"http://{server_ip}:8000/api/v1/status"
    print(f"[+] Server URL configured as: {BACKEND_URL}")

def update_mock_led_state(signal: str):
    """Simulates physical LED state changes on terminal screen."""
    signal = str(signal).upper().strip()
    visual = SIGNAL_VISUALS.get(signal, "⚪ [ALL LEDS OFF]")
    print(f"\r[STATUS: {signal:6s}] {visual}", end="", flush=True)

def main():
    print("=" * 75)
    print("  AUTONOMOUS AI EDGE SOC: Virtual Hardware Trust Layer (Mock Pi)")
    print("  Controls Virtual LEDs & Dispatches Out-of-Band UDP Kill Packets")
    print("=" * 75)

    configure_soc_server()

    print(f"[*] Starting hardware polling loop for: {BACKEND_URL}")
    print(f"[*] Polling interval: {POLL_INTERVAL}s. Listening for threats... Press Ctrl+C to stop.\n")

    isolated_nodes = set()

    try:
        while True:
            try:
                response = requests.get(BACKEND_URL, timeout=1.0)
                if response.status_code == 200:
                    data = response.json()
                    hardware_signal = data.get("hardware_signal", "GREEN")
                    target_ip = data.get("isolated_ip")

                    update_mock_led_state(hardware_signal)

                    if hardware_signal == "GREEN":
                        if isolated_nodes:
                            isolated_nodes.clear()

                    elif hardware_signal == "RED":
                        # Send out-of-band UDP kill packet to sever the infected workstation
                        if target_ip and target_ip not in isolated_nodes:
                            print(f"\n[🚨 CRITICAL THREAT] Out-of-band kill command triggered for {target_ip}!")
                            try:
                                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                                sock.sendto(b"EXECUTE_ISOLATION", (target_ip, UDP_PORT))
                                sock.close()
                                isolated_nodes.add(target_ip)
                                print(f"[⚡ ACTION] UDP 'EXECUTE_ISOLATION' kill packet dispatched to {target_ip}:{UDP_PORT}!")
                                print("[🛡️ DEFENSE] Network interface severed on target endpoint.\n")
                            except Exception as sock_err:
                                print(f"\n[!] Socket transmission failed: {sock_err}")
                else:
                    update_mock_led_state("UNKNOWN")

            except requests.exceptions.RequestException:
                print("\r[NETWORK ERROR] Waiting for FastAPI backend connection...", end="", flush=True)

            time.sleep(POLL_INTERVAL)

    except KeyboardInterrupt:
        print("\n\n[INFO] Virtual Hardware Controller stopped cleanly.")

if __name__ == "__main__":
    main()
