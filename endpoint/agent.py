import socket
import os
import sys

# UDP Listener configuration for receiving isolation commands
UDP_PORT = 9999
BUFFER_SIZE = 1024

def start_agent():
    """
    Background daemon running on workstation endpoints.
    Listens for UDP kill packets from the Raspberry Pi and severs network adapter.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", UDP_PORT))
    print(f"[*] Endpoint Severing Agent active on UDP port {UDP_PORT}...")

    while True:
        try:
            data, addr = sock.recvfrom(BUFFER_SIZE)
            message = data.decode("utf-8").strip()
            print(f"[!] Hardware command received from {addr[0]}: {message}")

            if message == "EXECUTE_ISOLATION":
                print("[ALERT] Threat signal verified! Executing network disconnect...")
                
                # Execute native OS command to drop active Wi-Fi interface
                if sys.platform.startswith("win"):
                    os.system("netsh wlan disconnect")
                else:
                    os.system("nmcli radio wifi off")
                    
                print("[+] Interface disconnected successfully.")
        except Exception as e:
            print(f"[ERROR] Socket error encountered: {e}")

if __name__ == "__main__":
    start_agent()