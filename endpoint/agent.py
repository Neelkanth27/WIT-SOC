import requests
import time
import random
import socket
import os
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# =====================================================================
# 1. CONFIGURATION & GLOBAL STATE
# =====================================================================
MACHINE_ID = socket.gethostname()
UDP_PORT = 9999
BEACON_MESSAGE = b"WIT_SOC_SERVER_BEACON"

# The folder we will monitor for the fake PDF execution
# NEW (Guaranteed to always spawn inside the endpoint/ folder)
AGENT_DIR = os.path.dirname(os.path.abspath(__file__))
TRIGGER_FOLDER = os.path.join(AGENT_DIR, "Target_Desktop")
os.makedirs(TRIGGER_FOLDER, exist_ok=True)

# Global variables controlled by our background threads
ATTACK_MODE = False
SOC_URL = None

# =====================================================================
# 2. UDP AUTO-DISCOVERY (The "Ears")
# =====================================================================
def discover_soc_server():
    """Listens for the SOC Server's broadcast beacon on the local network."""
    global SOC_URL
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("", UDP_PORT))
    
    print("[*] Listening for SOC Server beacon on the network...")
    while SOC_URL is None:
        data, addr = sock.recvfrom(1024)
        if data == BEACON_MESSAGE:
            server_ip = addr[0]
            SOC_URL = f"http://{server_ip}:8000/api/v1/telemetry"
            print(f"[+] Server auto-discovered at {server_ip}!")
            break

# =====================================================================
# 3. WATCHDOG TROJAN TRIGGER (The "Eyes")
# =====================================================================
class TrojanMonitor(FileSystemEventHandler):
    def on_created(self, event):
        global ATTACK_MODE
        # If any file is dropped/executed in the target folder, trigger the attack
        if not event.is_directory:
            print(f"\n[!!!] CRITICAL: Unauthorized file execution detected: {os.path.basename(event.src_path)}")
            print("[!!!] Malware payload activated. Switching to DDoS Mode...\n")
            ATTACK_MODE = True

def start_folder_monitor():
    """Runs the watchdog observer in the background."""
    observer = Observer()
    observer.schedule(TrojanMonitor(), TRIGGER_FOLDER, recursive=False)
    observer.start()

# =====================================================================
# 4. TELEMETRY GENERATION ENGINE
# =====================================================================
def generate_normal_traffic():
    return {
        "flow_duration": random.uniform(10.0, 500.0),
        "flow_bytes_sec": random.uniform(5.0, 100.0),
        "total_fwd_packets": random.randint(1, 5),
        "total_bwd_packets": random.randint(1, 5),
        "fwd_packet_length_mean": random.uniform(10.0, 50.0)
    }

def generate_malicious_traffic():
    return {
        "flow_duration": random.uniform(3000000.0, 10000000.0),
        "flow_bytes_sec": random.uniform(10000000.0, 50000000.0),
        "total_fwd_packets": random.randint(2000, 8000),
        "total_bwd_packets": 0,
        "fwd_packet_length_mean": random.uniform(800.0, 1500.0)
    }

# =====================================================================
# 5. MAIN EXECUTION LOOP
# =====================================================================
def stream_telemetry():
    print("=" * 60)
    print(f"[*] WIT-SOC Endpoint Agent")
    print(f"[*] Machine ID: {MACHINE_ID}")
    print(f"[*] Monitoring Folder: {TRIGGER_FOLDER}")
    print("=" * 60 + "\n")

    # Start the folder monitor
    start_folder_monitor()

    # Block until we find the server
    discover_soc_server()
    print("[*] Beginning network telemetry stream...\n")

    try:
        while True:
            payload = generate_malicious_traffic() if ATTACK_MODE else generate_normal_traffic()
            
            status_msg = "[!] FIRING MALICIOUS PAYLOAD" if ATTACK_MODE else "[+] Streaming normal telemetry"
            print(f"{status_msg} -> {SOC_URL}")

            try:
                response = requests.post(SOC_URL, json=payload, timeout=2)
                if response.status_code == 200:
                    v = response.json()
                    print(f"    └─ SOC Verdict: {v['action']} | Signal: {v['hardware_signal']} | Score: {v['threat_score_percentage']}%\n")
                else:
                    print(f"    └─ [ERROR] Status: {response.status_code}\n")
            except requests.exceptions.RequestException:
                print("    └─ [NETWORK ERROR] Connection to SOC lost.\n")

            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\n[*] Agent stopped by user.")

if __name__ == "__main__":
    stream_telemetry()