import requests
import time

BACKEND_URL = "http://127.0.0.1:8000/status"

def set_signal(signal_name: str):
    try:
        res = requests.post(BACKEND_URL, json={"hardware_signal": signal_name})
        if res.status_code == 200:
            print(f"✓ Backend signal updated to: {signal_name}")
        else:
            print(f"✗ Failed to update signal: {res.text}")
    except Exception as e:
        print(f"✗ Error connecting to backend: {e}")

def main():
    print("=" * 50)
    print("       Edge SOC Interactive Signal Trigger")
    print("=" * 50)
    print("Controls:")
    print("  [1] Send GREEN signal")
    print("  [2] Send YELLOW signal")
    print("  [3] Send RED signal")
    print("  [q] Quit")
    print("=" * 50)

    while True:
        choice = input("\nSelect Signal [1/2/3/q]: ").strip().lower()
        if choice == '1':
            set_signal("GREEN")
        elif choice == '2':
            set_signal("YELLOW")
        elif choice == '3':
            set_signal("RED")
        elif choice == 'q':
            print("Exiting trigger control.")
            break
        else:
            print("Invalid input! Please press 1, 2, 3, or q.")

if __name__ == "__main__":
    main()
