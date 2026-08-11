import os
import sys
import time
import json
import random
from datetime import datetime
from typing import Tuple, Dict, Any
import requests
from pydantic import BaseModel, Field

# Enable ANSI colors on Windows CMD/PowerShell if needed
if sys.platform == "win32":
    os.system("")

# =====================================================================
# ANSI COLORING & HACKER TOOL STYLING
# =====================================================================
CLR_RESET   = "\033[0m"
CLR_BOLD    = "\033[1m"
CLR_RED     = "\033[91m"
CLR_GREEN   = "\033[92m"
CLR_YELLOW  = "\033[93m"
CLR_CYAN    = "\033[96m"
CLR_MAGENTA = "\033[95m"
CLR_WHITE   = "\033[97m"
CLR_GRAY    = "\033[90m"

BG_RED      = "\033[41m\033[97m\033[1m"
BG_GREEN    = "\033[42m\033[30m\033[1m"
BG_YELLOW   = "\033[43m\033[30m\033[1m"
BG_CYAN     = "\033[46m\033[30m\033[1m"

# =====================================================================
# DATA SCHEMA (PYDANTIC MODEL)
# =====================================================================
class TelemetryPayload(BaseModel):
    flow_duration: float = Field(..., description="Duration of network flow in seconds")
    flow_bytes_sec: float = Field(..., description="Data transfer rate in bytes/sec")
    total_fwd_packets: int = Field(..., description="Total forward packets sent")
    total_bwd_packets: int = Field(..., description="Total backward packets received")
    fwd_packet_length_mean: float = Field(..., description="Mean length of forward packets")

# =====================================================================
# TRAFFIC GENERATION ENGINE
# =====================================================================
def generate_traffic() -> Tuple[str, TelemetryPayload]:
    """
    Randomly generates either 'Normal' benign traffic or one of three specific 
    attack signatures based on Edge SOC heuristic rules:
      1. Volumetric DDoS : total_bwd_packets = 0, total_fwd_packets > 1000
      2. Stealth Port Scan: flow_duration < 20.0, total_fwd_packets = 1, total_bwd_packets = 0
      3. Data Exfiltration: fwd_packet_length_mean > 5000.0
    """
    traffic_types = [
        "Normal",
        "Volumetric DDoS",
        "Stealth Port Scan",
        "Data Exfiltration"
    ]
    
    # 40% chance Normal, 20% Volumetric DDoS, 20% Stealth Port Scan, 20% Data Exfiltration
    selected_type = random.choices(traffic_types, weights=[40, 20, 20, 20], k=1)[0]

    if selected_type == "Volumetric DDoS":
        # Signature: total_bwd_packets = 0, total_fwd_packets > 1000
        payload = TelemetryPayload(
            flow_duration=round(random.uniform(1.0, 15.0), 2),
            flow_bytes_sec=round(random.uniform(500000.0, 10000000.0), 2),
            total_fwd_packets=random.randint(1001, 8000),
            total_bwd_packets=0,
            fwd_packet_length_mean=round(random.uniform(500.0, 1400.0), 2)
        )

    elif selected_type == "Stealth Port Scan":
        # Signature: flow_duration < 20.0, total_fwd_packets = 1, total_bwd_packets = 0
        payload = TelemetryPayload(
            flow_duration=round(random.uniform(0.1, 19.9), 2),
            flow_bytes_sec=round(random.uniform(1.0, 100.0), 2),
            total_fwd_packets=1,
            total_bwd_packets=0,
            fwd_packet_length_mean=round(random.uniform(40.0, 64.0), 2)
        )

    elif selected_type == "Data Exfiltration":
        # Signature: fwd_packet_length_mean > 5000.0
        payload = TelemetryPayload(
            flow_duration=round(random.uniform(30.0, 600.0), 2),
            flow_bytes_sec=round(random.uniform(100000.0, 2000000.0), 2),
            total_fwd_packets=random.randint(10, 100),
            total_bwd_packets=random.randint(5, 50),
            fwd_packet_length_mean=round(random.uniform(5001.0, 15000.0), 2)
        )

    else: # Normal
        payload = TelemetryPayload(
            flow_duration=round(random.uniform(20.0, 500.0), 2),
            flow_bytes_sec=round(random.uniform(10.0, 500.0), 2),
            total_fwd_packets=random.randint(2, 20),
            total_bwd_packets=random.randint(2, 20),
            fwd_packet_length_mean=round(random.uniform(40.0, 1200.0), 2)
        )

    return selected_type, payload

# =====================================================================
# TERMINAL UI RENDERER
# =====================================================================
def print_banner():
    banner = f"""
{CLR_CYAN}{CLR_BOLD}██╗  ██╗██████╗ ███████╗    ███████╗██████╗  ██████╗ 
██║  ██║██╔══██╗██╔════╝    ██╔════╝██╔══██╗██╔════╝ 
███████║██████╔╝█████╗      ███████╗██║  ██║██║      
██╔══██║██╔═══╝ ██╔══╝      ╚════██║██║  ██║██║      
██║  ██║██║     ███████╗    ███████║██████╔╝╚██████╗ 
╚═╝  ╚═╝╚═╝     ╚══════╝    ╚══════╝╚═════╝  ╚═════╝{CLR_RESET}
{CLR_MAGENTA}{CLR_BOLD}⚡ EDGE SOC NETWORK TELEMETRY & ATTACK VECTOR SIMULATOR v2.0 ⚡{CLR_RESET}
    """
    print(banner)

def prompt_server_ip() -> str:
    """Prompts user for Backend Server IP without UDP auto-discovery."""
    print(f"{CLR_YELLOW}[?] Enter Backend Server IP address (default: 127.0.0.1): {CLR_RESET}", end="")
    user_input = input().strip()
    
    if not user_input:
        server_ip = "127.0.0.1"
    else:
        server_ip = user_input

    target_url = f"http://{server_ip}:8000/api/v1/telemetry"
    print(f"\n{CLR_GREEN}[+] Target URL set to: {CLR_BOLD}{target_url}{CLR_RESET}\n")
    return target_url

def render_transmission_log(seq: int, traffic_type: str, payload: TelemetryPayload, target_url: str):
    timestamp = datetime.now().strftime("%H:%M:%S")
    payload_dict = payload.model_dump()
    json_str = json.dumps(payload_dict, indent=2)

    # Style header based on traffic type
    if traffic_type == "Normal":
        type_badge = f"{BG_GREEN} NORMAL TELEMETRY {CLR_RESET}"
    else:
        type_badge = f"{BG_RED} ATTACK DETECTED: {traffic_type.upper()} {CLR_RESET}"

    print(f"{CLR_GRAY}─" * 70 + CLR_RESET)
    print(f"{CLR_CYAN}[{timestamp}]{CLR_RESET} {CLR_BOLD}PACKET #{seq:04d}{CLR_RESET} | Type: {type_badge}")
    print(f"{CLR_GRAY}📤 Transmitting payload to {target_url}...{CLR_RESET}")
    print(f"{CLR_WHITE}{json_str}{CLR_RESET}")

    # Send Request
    try:
        start_t = time.time()
        response = requests.post(target_url, json=payload_dict, timeout=3.0)
        latency = round((time.time() - start_t) * 1000, 2)

        if response.status_code == 200:
            res_data = response.json()
            verdict = res_data.get("action", "UNKNOWN")
            score = res_data.get("threat_score_percentage", 0.0)
            signal = res_data.get("hardware_signal", "GREEN")
            engine = res_data.get("engine", "AI Model / Heuristics")

            # Colorize Verdict Action
            if verdict == "PERM_LOCK":
                v_str = f"{BG_RED} PERM_LOCK (ISOLATE) {CLR_RESET}"
            elif verdict == "TEMP_ISOLATE":
                v_str = f"{BG_YELLOW} TEMP_ISOLATE {CLR_RESET}"
            else:
                v_str = f"{BG_GREEN} ALLOW {CLR_RESET}"

            # Hardware LED Signal Emoji
            led_emoji = "🔴 RED" if signal == "RED" else ("🟡 YELLOW" if signal == "YELLOW" else "🟢 GREEN")

            print(f"\n{CLR_GREEN}📥 BACKEND RESPONSE [200 OK] ({latency}ms):{CLR_RESET}")
            print(f"   ├─ {CLR_BOLD}Verdict Action{CLR_RESET}   : {v_str}")
            print(f"   ├─ {CLR_BOLD}Threat Score  {CLR_RESET}   : {CLR_MAGENTA}{score}%{CLR_RESET}")
            print(f"   ├─ {CLR_BOLD}Hardware Signal{CLR_RESET}  : {led_emoji}")
            print(f"   └─ {CLR_BOLD}Detection Engine{CLR_RESET} : {CLR_CYAN}{engine}{CLR_RESET}\n")

        else:
            print(f"\n{CLR_RED}📥 BACKEND RESPONSE [{response.status_code} ERROR]:{CLR_RESET}")
            print(f"   └─ Response body: {response.text}\n")

    except requests.exceptions.RequestException as err:
        print(f"\n{CLR_RED}📥 BACKEND TRANSMISSION FAILURE:{CLR_RESET}")
        print(f"   └─ Connection error: {err}")
        print(f"   └─ {CLR_YELLOW}Ensure backend is running at http://<server_ip>:8000{CLR_RESET}\n")

# =====================================================================
# MAIN EXECUTION LOOP
# =====================================================================
def main():
    print_banner()
    target_url = prompt_server_ip()

    print(f"{CLR_CYAN}[*] Starting infinite telemetry transmission loop (Interval: 2.0s)...{CLR_RESET}")
    print(f"{CLR_GRAY}[*] Press Ctrl+C to abort telemetry stream.{CLR_RESET}\n")

    seq = 1
    try:
        while True:
            traffic_type, payload = generate_traffic()
            render_transmission_log(seq, traffic_type, payload, target_url)
            seq += 1
            time.sleep(2.0)
    except KeyboardInterrupt:
        print(f"\n\n{CLR_YELLOW}[!] Telemetry transmission halted by user operator.{CLR_RESET}")
        print(f"{CLR_GREEN}[+] Session closed cleanly.{CLR_RESET}")
        sys.exit(0)

if __name__ == "__main__":
    main()
