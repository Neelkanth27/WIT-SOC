import time
import socket
import requests
from gpiozero import LED

import sys

# --- GPIO Setup (BCM Pin Numbers) ---
green_led = LED(22)
yellow_led = LED(27)
red_led = LED(17)

GATEWAY_URL = None
UDP_PORT = 9999

def configure_soc_server():
    """Configures the backend IP via CLI arguments or interactive prompt."""
    global GATEWAY_URL
    server_ip = None
    if len(sys.argv) > 1 and not sys.argv[1].startswith("-"):
        server_ip = sys.argv[1].strip()
    elif "--server-ip" in sys.argv:
        idx = sys.argv.index("--server-ip")
        if idx + 1 < len(sys.argv):
            server_ip = sys.argv[idx + 1].strip()
            
    if not server_ip:
        print("[?] Enter Backend Server IP (or press Enter for 192.168.137.1):")
        try:
            server_ip = input("> ").strip()
        except Exception:
            server_ip = ""
            
    if not server_ip:
        server_ip = "192.168.137.1"
        
    GATEWAY_URL = f"http://{server_ip}:8000/api/v1/status"
    print(f"[+] Gateway target URL configured as: {GATEWAY_URL}")

def set_leds(green=False, yellow=False, red=False):
    """Controls physical GPIO pin states on the breadboard."""
    if green: green_led.on() 
    else: green_led.off()
    
    if yellow: yellow_led.on() 
    else: yellow_led.off()
    
    if red: red_led.on() 
    else: red_led.off()

def run_controller():
    """
    Polls the Edge SOC Gateway, actuates physical LEDs, 
    and sends targeted UDP kill packets to isolated attacker IPs.
    """
    print("=" * 65)
    print("  Raspberry Pi Out-of-Band Hardware Mitigation Controller")
    print("=" * 65)
    configure_soc_server()
    set_leds(green=True)
    isolated_nodes = set()

    while True:
        try:
            response = requests.get(GATEWAY_URL, timeout=2)
            if response.status_code == 200:
                data = response.json()
                signal = data.get("hardware_signal", "GREEN")
                target_ip = data.get("isolated_ip")

                if signal == "GREEN":
                    set_leds(green=True)
                    isolated_nodes.clear() # Reset tracked nodes on clear

                elif signal == "YELLOW":
                    set_leds(yellow=True)

                elif signal == "RED":
                    set_leds(red=True)
                    # Send UDP kill packet if the node hasn't been isolated yet
                    if target_ip and target_ip not in isolated_nodes:
                        print(f"[ALERT] Critical state! Sending isolation packet to {target_ip}:{UDP_PORT}")
                        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                        sock.sendto(b"EXECUTE_ISOLATION", (target_ip, UDP_PORT))
                        sock.close()
                        isolated_nodes.add(target_ip)
                        print(f"[+] Network isolation signal dispatched to {target_ip}")

        except Exception as e:
            print(f"[!] Gateway connection error: {e}")
            set_leds(yellow=True) # Visual indicator of connectivity loss

        time.sleep(0.5)

if __name__ == "__main__":
    run_controller()