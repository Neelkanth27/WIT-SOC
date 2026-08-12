import os
import sys
import time
import json
import random
from datetime import datetime
from typing import Tuple, Dict, Any

# Enable ANSI colors on Windows CMD/PowerShell if needed
if sys.platform == "win32":
    os.system("")

# Try to import required dependencies
try:
    import requests
    from pydantic import BaseModel, Field
except ImportError:
    print("\033[91m[!] Missing dependencies. Run: pip install requests pydantic\033[0m")
    sys.exit(1)

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
def generate_traffic(seq: int, mode: str) -> Tuple[str, TelemetryPayload]:
    """
    Generates network traffic telemetry.
    
    If mode is 'clean' (default):
      - Generates normal background traffic.
      - Every 5th packet (seq % 5 == 0) simulates a 'Background Anomaly (False Flag)' signature:
        flow_duration=15.0, flow_bytes_sec=50.0, total_fwd_packets=1, total_bwd_packets=0, fwd_packet_length_mean=50.0
        
    If mode is 'attack' (triggered with --attack CLI flag):
      - Stage-based attack payload simulating a sequential breach:
        - seq == 1: Stage 1: Dropper Execution (Initial Foothold)
        - seq == 2: Stage 2: Reconnaissance (Stealth Port Scan)
        - seq >= 3: Stage 3: Data Exfiltration & Volumetric DDoS
    """
    if mode == "clean":
        if seq > 0 and seq % 5 == 0:
            return "Background Anomaly (False Flag)", TelemetryPayload(
                flow_duration=15.0,
                flow_bytes_sec=50.0,
                total_fwd_packets=1,
                total_bwd_packets=0,
                fwd_packet_length_mean=50.0
            )
        else:
            return "Normal Background Traffic", TelemetryPayload(
                flow_duration=round(random.uniform(20.0, 500.0), 2),
                flow_bytes_sec=round(random.uniform(10.0, 500.0), 2),
                total_fwd_packets=random.randint(2, 20),
                total_bwd_packets=random.randint(2, 20),
                fwd_packet_length_mean=round(random.uniform(40.0, 1200.0), 2)
            )
    else: # mode == "attack"
        if seq == 1:
            return "Stage 1: Dropper Execution (Initial Foothold)", TelemetryPayload(
                flow_duration=100.0,
                flow_bytes_sec=150.0,
                total_fwd_packets=10,
                total_bwd_packets=10,
                fwd_packet_length_mean=500.0
            )
        elif seq == 2:
            return "Stage 2: Reconnaissance (Stealth Port Scan)", TelemetryPayload(
                flow_duration=15.0,
                flow_bytes_sec=50.0,
                total_fwd_packets=1,
                total_bwd_packets=0,
                fwd_packet_length_mean=50.0
            )
        else:
            return "Stage 3: Data Exfiltration & Volumetric DDoS", TelemetryPayload(
                flow_duration=5.0,
                flow_bytes_sec=5000000.0,
                total_fwd_packets=2500,
                total_bwd_packets=0,
                fwd_packet_length_mean=6000.0
            )

# =====================================================================
# TERMINAL UI RENDERER
# =====================================================================
def print_banner(mode: str):
    banner = f"""
{CLR_CYAN}{CLR_BOLD}██╗  ██╗██████╗ ███████╗    ███████╗██████╗  ██████╗ 
██║  ██║██╔══██╗██╔════╝    ██╔════╝██╔══██╗██╔════╝ 
███████║██████╔╝█████╗      ███████╗██║  ██║██║      
██╔══██║██╔═══╝ ██╔══╝      ╚════██║██║  ██║██║      
██║  ██║██║     ███████╗    ███████║██████╔╝╚██████╗ 
╚═╝  ╚═╝╚═╝     ╚══════╝    ╚══════╝╚═════╝  ╚═════╝{CLR_RESET}
{CLR_MAGENTA}{CLR_BOLD}⚡ EDGE SOC NETWORK TELEMETRY & ATTACK VECTOR SIMULATOR v2.0 ⚡{CLR_RESET}
{CLR_YELLOW}{CLR_BOLD}Mode: {CLR_WHITE}{('BACKGROUND TELEMETRY' if mode == 'clean' else 'MALWARE EXECUTING / ATTACK SIMULATION')}{CLR_RESET}
    """
    print(banner)

def prompt_server_ip(mode: str) -> str:
    """Prompts user for Backend Server IP or loads from file cache."""
    ip_file = "target_ip.txt"
    if mode == "attack" and os.path.exists(ip_file):
        with open(ip_file, "r") as f:
            server_ip = f.read().strip()
        print(f"{CLR_GREEN}[+] Loaded cached target IP: {CLR_BOLD}{server_ip}{CLR_RESET}")
    else:
        print(f"{CLR_YELLOW}[?] Enter Backend Server IP address (default: 127.0.0.1): {CLR_RESET}", end="")
        user_input = input().strip()
        server_ip = user_input if user_input else "127.0.0.1"
        try:
            with open(ip_file, "w") as f:
                f.write(server_ip)
        except Exception:
            pass # Ignore write failures if read-only filesystem

    target_url = f"http://{server_ip}:8000/api/v1/telemetry"
    print(f"{CLR_GREEN}[+] Target URL set to: {CLR_BOLD}{target_url}{CLR_RESET}\n")
    return target_url

def render_transmission_log(seq: int, mode: str, traffic_type: str, payload: TelemetryPayload, target_url: str):
    timestamp = datetime.now().strftime("%H:%M:%S")
    payload_dict = payload.model_dump()
    json_str = json.dumps(payload_dict, indent=2)

    # Style header based on traffic type/mode
    if "Normal" in traffic_type:
        type_badge = f"{BG_GREEN} NORMAL TELEMETRY {CLR_RESET}"
    elif "Anomaly" in traffic_type:
        type_badge = f"{BG_YELLOW} FALSE FLAG / ANOMALY {CLR_RESET}"
    else:
        type_badge = f"{BG_RED} ATTACK DETECTED: {traffic_type.upper()} {CLR_RESET}"

    print(f"{CLR_GRAY}─" * 70 + CLR_RESET)
    print(f"{CLR_CYAN}[{timestamp}]{CLR_RESET} {CLR_BOLD}PACKET #{seq:04d}{CLR_RESET} | Mode: {mode.upper()} | Type: {type_badge}")
    print(f"{CLR_GRAY}📤 Transmitting payload to {target_url}...{CLR_RESET}")
    print(f"{CLR_WHITE}{json_str}{CLR_RESET}")

    # Send Request
    try:
        start_t = time.time()
        response = requests.post(target_url, json=payload_dict, timeout=3.0)
        latency = round((time.time() - start_t) * 1000, 2)

        if response.status_code == 200:
            res_data = response.json()
            verdict = res_data.get("action", "ALLOW")
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

            if verdict == "PERM_LOCK":
                print(f"\n{BG_RED} 🚨 CRITICAL THREAT DETECTED: PERM_LOCK ISSUED 🚨 {CLR_RESET}")
                print(f"{CLR_RED}[!] Threat Score: {score}% | Hardware Signal: RED\n[!] WORKSTATION NETWORK INTERFACE ISOLATED BY EDGE SOC.\n[*] Execution halted. Threat neutralized.{CLR_RESET}\n")
                print(f"{CLR_YELLOW}[*] Simulated network sever. Device will remain in isolated sleep state. Press Ctrl+C to exit.{CLR_RESET}")
                while True:
                    time.sleep(3600)

        else:
            print(f"\n{CLR_RED}📥 BACKEND RESPONSE [{response.status_code} ERROR]:{CLR_RESET}")
            print(f"   └─ Response body: {response.text}\n")

    except requests.exceptions.RequestException as err:
        print(f"\n{CLR_RED}📥 BACKEND TRANSMISSION FAILURE:{CLR_RESET}")
        print(f"   └─ Connection error: {err}")
        print(f"   └─ {CLR_YELLOW}Ensure backend is running at {target_url}{CLR_RESET}\n")

# =====================================================================
# MAIN EXECUTION LOOP
# =====================================================================
def main():
    mode = "attack" if "--attack" in sys.argv else "clean"
    print_banner(mode)
    target_url = prompt_server_ip(mode)

    print(f"{CLR_CYAN}[*] Starting infinite telemetry transmission loop (Interval: 2.0s)...{CLR_RESET}")
    print(f"{CLR_GRAY}[*] Press Ctrl+C to abort telemetry stream.{CLR_RESET}\n")

    seq = 1
    try:
        while True:
            traffic_type, payload = generate_traffic(seq, mode)
            render_transmission_log(seq, mode, traffic_type, payload, target_url)
            seq += 1
            time.sleep(2.0)
    except KeyboardInterrupt:
        print(f"\n\n{CLR_YELLOW}[!] Telemetry transmission halted by user operator.{CLR_RESET}")
        print(f"{CLR_GREEN}[+] Session closed cleanly.{CLR_RESET}")
        sys.exit(0)

if __name__ == "__main__":
    main()
