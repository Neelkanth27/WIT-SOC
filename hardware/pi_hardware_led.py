import time
import requests
from gpiozero import LED

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------
BACKEND_URL = None
POLL_INTERVAL = 0.5  # Poll every 0.5 seconds

def configure_soc_server():
    """Prompts the user for the backend IP during demo setup."""
    global BACKEND_URL
    print("[?] Enter the Backend Server IP (e.g., 10.45.2.100):")
    server_ip = input("> ").strip()
    
    if not server_ip:
        print("[!] No IP entered. Defaulting to 127.0.0.1 for local testing.")
        server_ip = "127.0.0.1"
        
    BACKEND_URL = f"http://{server_ip}:8000/api/v1/status"
    print(f"[+] Server URL configured as: {BACKEND_URL}")

# -----------------------------------------------------------------------------
# BCM GPIO Pin Assignments & LED Hardware Mapping
# -----------------------------------------------------------------------------
# - Green LED  --> GPIO 22 (Physical Pin 15)
# - Yellow LED --> GPIO 27 (Physical Pin 13)
# - Red LED    --> GPIO 17 (Physical Pin 11)
led_green = LED(22)
led_yellow = LED(27)
led_red = LED(17)

LED_MAP = {
    "GREEN": led_green,
    "YELLOW": led_yellow,
    "RED": led_red
}

def turn_off_all_leds():
    """Ensures all LEDs are completely powered off."""
    led_green.off()
    led_yellow.off()
    led_red.off()

def update_led_state(signal: str):
    """
    Sets the active LED color while turning off all others.
    If signal is invalid or unknown, turns off all LEDs.
    """
    signal = str(signal).upper().strip()
    
    # Turn off all LEDs first to guarantee a single active state
    turn_off_all_leds()

    if signal in LED_MAP:
        LED_MAP[signal].on()
        print(f"[STATUS] Hardware Signal: {signal} -> {signal} LED active.")
    else:
        print(f"[WARNING] Unrecognized signal received: '{signal}'. All LEDs OFF.")

def main():
    print("=" * 60)
    print("Edge SOC Raspberry Pi Hardware Mitigation Controller")
    print("=" * 60)

    # Initial safety reset of all LEDs
    turn_off_all_leds()

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
                    update_led_state(hardware_signal)
                else:
                    print(f"[ERROR] API returned HTTP status {response.status_code}")
                    turn_off_all_leds()

            except requests.exceptions.RequestException as e:
                print(f"[NETWORK ERROR] Connection to backend lost: {e}")
                turn_off_all_leds()

            time.sleep(POLL_INTERVAL)

    except KeyboardInterrupt:
        print("\n[INFO] Exiting hardware mitigation controller...")
    finally:
        turn_off_all_leds()
        print("[INFO] All LEDs turned off. GPIO cleanup complete.")

if __name__ == "__main__":
    main()
