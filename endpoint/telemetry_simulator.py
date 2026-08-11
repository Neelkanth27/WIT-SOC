import os, sys, time, random
if sys.platform == "win32": os.system("")

CLR_RESET, CLR_BOLD, CLR_RED, CLR_GREEN, CLR_YELLOW, CLR_CYAN, CLR_GRAY = "\033[0m", "\033[1m", "\033[91m", "\033[92m", "\033[93m", "\033[96m", "\033[90m"
BG_RED, BG_GREEN, BG_YELLOW = "\033[41m\033[97m\033[1m", "\033[42m\033[30m\033[1m", "\033[43m\033[30m\033[1m"

try:
    import requests
    from pydantic import BaseModel
except ImportError:
    print("[!] Missing dependencies. Run: pip install requests pydantic"); sys.exit(1)

class TelemetryPayload(BaseModel):
    flow_duration: float; flow_bytes_sec: float; total_fwd_packets: int; total_bwd_packets: int; fwd_packet_length_mean: float

def generate_traffic(seq: int, mode: str):
    if mode == "clean":
        if seq > 0 and seq % 5 == 0:
            return "Background Anomaly (False Flag)", TelemetryPayload(flow_duration=15.0, flow_bytes_sec=50.0, total_fwd_packets=1, total_bwd_packets=0, fwd_packet_length_mean=50.0)
        return "Normal Background Traffic", TelemetryPayload(flow_duration=round(random.uniform(20.0, 500.0), 2), flow_bytes_sec=round(random.uniform(10.0, 500.0), 2), total_fwd_packets=random.randint(2, 20), total_bwd_packets=random.randint(2, 20), fwd_packet_length_mean=round(random.uniform(40.0, 1200.0), 2))
    else:
        if seq == 1: return "Stage 1: Dropper Execution (Initial Foothold)", TelemetryPayload(flow_duration=100.0, flow_bytes_sec=150.0, total_fwd_packets=10, total_bwd_packets=10, fwd_packet_length_mean=500.0)
        elif seq == 2: return "Stage 2: Reconnaissance (Stealth Port Scan)", TelemetryPayload(flow_duration=15.0, flow_bytes_sec=50.0, total_fwd_packets=1, total_bwd_packets=0, fwd_packet_length_mean=50.0)
        else: return "Stage 3: Data Exfiltration & Volumetric DDoS", TelemetryPayload(flow_duration=5.0, flow_bytes_sec=5000000.0, total_fwd_packets=2500, total_bwd_packets=0, fwd_packet_length_mean=6000.0)

def prompt_server_ip(mode: str) -> str:
    ip_file = "target_ip.txt"
    if mode == "attack" and os.path.exists(ip_file):
        with open(ip_file, "r") as f: server_ip = f.read().strip()
    else:
        print(f"{CLR_YELLOW}[?] Enter Backend Server IP address: {CLR_RESET}", end="")
        server_ip = input().strip() or "127.0.0.1"
        with open(ip_file, "w") as f: f.write(server_ip)
    target_url = f"http://{server_ip}:8000/api/v1/telemetry"
    return target_url

def main():
    mode = "attack" if "--attack" in sys.argv else "clean"
    print(f"{CLR_CYAN}{CLR_BOLD}⚡ EDGE SOC ENDPOINT AGENT - [{'BACKGROUND TELEMETRY' if mode == 'clean' else 'MALWARE EXECUTING'}] ⚡{CLR_RESET}\n")
    target_url = prompt_server_ip(mode)
    seq = 1

    try:
        while True:
            t_type, payload = generate_traffic(seq, mode)
            print(CLR_GRAY + ("─" * 70) + CLR_RESET)
            print(f"{CLR_CYAN}PACKET #{seq:04d}{CLR_RESET} | Mode: {mode.upper()} | Type: {t_type}")
            try:
                res = requests.post(target_url, json=payload.model_dump() if hasattr(payload, "model_dump") else payload.dict(), timeout=3.0)
                if res.status_code == 200:
                    data = res.json()
                    verdict, score = data.get("action", "ALLOW"), data.get("threat_score_percentage", 0.0)
                    if verdict == "PERM_LOCK":
                        print(f"\n{BG_RED} 🚨 CRITICAL THREAT DETECTED: PERM_LOCK ISSUED 🚨 {CLR_RESET}")
                        print(f"{CLR_RED}[!] Threat Score: {score}% | Hardware Signal: RED\n[!] WORKSTATION NETWORK INTERFACE ISOLATED BY EDGE SOC.\n[*] Execution halted. Threat neutralized.{CLR_RESET}\n")
                        while True: time.sleep(3600)
                    elif verdict == "TEMP_ISOLATE":
                        print(f"  ├─ Verdict: {BG_YELLOW} TEMP_ISOLATE (WARNING) {CLR_RESET}\n  └─ Threat Score: {score}% | Signal: 🟡 YELLOW (Monitoring...)")
                    else:
                        print(f"  ├─ Verdict: {BG_GREEN} ALLOW {CLR_RESET}\n  └─ Threat Score: {score}% | Signal: 🟢 GREEN")
            except Exception as err: print(f"{CLR_RED}[!] Transmission failure: {err}{CLR_RESET}")
            seq += 1
            time.sleep(2.0)
    except KeyboardInterrupt: sys.exit(0)

if __name__ == "__main__": main()