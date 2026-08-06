import time
import requests
from gpiozero import LED

# -----------------------------------------------------------------------------
# Configuration & Hardware Pin Setup
# -----------------------------------------------------------------------------
# Backend API configuration (Update server IP address as needed)
BACKEND_URL = "http://192.168.1.100:8000/status"  # Replace with FastAPI server host IP
POLL_INTERVAL = 0.5  # Poll every 0.5 seconds

# BCM GPIO Pin Assignments
# - Green LED  --> GPIO 22 (Pin 15)
# - Yellow LED --> GPIO 27 (Pin 13)
# - Red LED    --> GPIO 17 (Pin 11)
led_green = LED(22)
led_yellow = LED(27)
led_red = LED(17)

# Mapping hardware signals to their respective GPIO LED objects
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
    
    # First, turn off all LEDs to maintain strict single-active state
    turn_off_all_leds()

    if signal in LED_MAP:
        LED_MAP[signal].on()
        print(f"[STATUS] Hardware Signal: {signal} -> {signal} LED active.")
    else:
        print(f"[WARNING] Unrecognized signal received: '{signal}'. All LEDs OFF.")


def main():
    print("=" * 60)
    print("Edge SOC Raspberry Pi Hardware Mitigation Controller")
    print(f"Polling backend endpoint: {BACKEND_URL}")
    print(f"Interval: {POLL_INTERVAL} seconds")
    print("Press Ctrl+C to stop.")
    print("=" * 60)

    # Initial safety reset of all LEDs
    turn_off_all_leds()

    try:
        while True:
            try:
                # Fetch status from FastAPI backend
                response = requests.get(BACKEND_URL, timeout=1.0)
                if response.status_code == 200:
                    data = response.json()
                    hardware_signal = data.get("hardware_signal", "UNKNOWN")
                    update_led_state(hardware_signal)
                else:
                    print(f"[ERROR] API returned HTTP status {response.status_code}")
                    turn_off_all_leds()

            except requests.exceptions.RequestException as e:
                print(f"[NETWORK ERROR] Failed to connect to FastAPI backend: {e}")
                turn_off_all_leds()

            # Wait before the next poll cycle
            time.sleep(POLL_INTERVAL)

    except KeyboardInterrupt:
        print("\n[INFO] Exiting hardware mitigation controller...")
    finally:
        # Guarantee clean GPIO shutdown on exit
        turn_off_all_leds()
        print("[INFO] All LEDs turned off. GPIO cleanup complete.")


if __name__ == "__main__":
    main()
