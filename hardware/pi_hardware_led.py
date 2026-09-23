import time
import socket
import requests
from gpiozero import LED

# --- GPIO Setup (BCM Pin Numbers) ---
green_led = LED(22)
yellow_led = LED(27)
red_led = LED(17)

# Gateway endpoint hosted on PC 1
GATEWAY_URL = "http://192.168.137.1:8000/api/v1/status"
UDP_PORT = 9999

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
    print("[*] Raspberry Pi Out-of-Band Hardware Controller Started...")
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