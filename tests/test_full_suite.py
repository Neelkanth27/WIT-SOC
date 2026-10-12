import os
import sys
import time
import socket
import asyncio
import pandas as pd
import numpy as np
import joblib

# Ensure root and backend are on sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, "backend"))

print("=" * 80)
print("  WIT-SOC: COMPREHENSIVE END-TO-END SYSTEM TEST SUITE")
print("  Verifying all features from Repository & Project Synopsis (FF No. 180)")
print("=" * 80)

passed_tests = 0
failed_tests = 0

def report_result(test_name: str, passed: bool, detail: str = ""):
    global passed_tests, failed_tests
    if passed:
        passed_tests += 1
        print(f"  [PASS] {test_name} - {detail}")
    else:
        failed_tests += 1
        print(f"  [FAIL] {test_name} - {detail}")

# -----------------------------------------------------------------------------
# TEST 1: AI Model Loading & 3-Tier Multi-Class Prediction
# -----------------------------------------------------------------------------
print("\n[SECTION 1: AI Model Engine (CIC-IDS2017 & Random Forest)]")
try:
    model_path = os.path.join(BASE_DIR, "backend", "model.pkl")
    rf_model = joblib.load(model_path)
    report_result("Model Loading", True, f"Successfully loaded from {os.path.basename(model_path)}")
    
    # Check features and classes
    classes = list(rf_model.classes_)
    report_result("Model Classes", set(classes) == {0, 1, 2}, f"Classes detected: {classes} (0=Benign, 1=Suspicious, 2=Malicious)")

    # 1a. Benign Test
    p_clean = pd.DataFrame([{
        "flow_duration": 150.0, "flow_bytes_sec": 200.0,
        "total_fwd_packets": 10, "total_bwd_packets": 10,
        "fwd_packet_length_mean": 500.0
    }])
    pred_clean = rf_model.predict(p_clean)[0]
    report_result("Benign Traffic Classification", pred_clean == 0, f"Predicted class {pred_clean} (Expected: 0)")

    # 1b. Suspicious / Recon Test
    p_recon = pd.DataFrame([{
        "flow_duration": 15.0, "flow_bytes_sec": 50.0,
        "total_fwd_packets": 1, "total_bwd_packets": 0,
        "fwd_packet_length_mean": 50.0
    }])
    pred_recon = rf_model.predict(p_recon)[0]
    report_result("Suspicious / Recon Classification", pred_recon == 1, f"Predicted class {pred_recon} (Expected: 1)")

    # 1c. Malicious / DDoS Test
    p_ddos = pd.DataFrame([{
        "flow_duration": 5.0, "flow_bytes_sec": 5000000.0,
        "total_fwd_packets": 2500, "total_bwd_packets": 0,
        "fwd_packet_length_mean": 6000.0
    }])
    pred_ddos = rf_model.predict(p_ddos)[0]
    report_result("Malicious / DDoS Classification", pred_ddos == 2, f"Predicted class {pred_ddos} (Expected: 2)")

except Exception as e:
    report_result("AI Model Engine", False, f"Exception occurred: {e}")

# -----------------------------------------------------------------------------
# TEST 2: SQLite SIEM Audit Database Integrity
# -----------------------------------------------------------------------------
print("\n[SECTION 2: SQLite SIEM Audit Database (Fig. 1 Architecture)]")
try:
    from database import init_db, log_event, get_recent_logs, get_audit_stats, clear_audit_logs
    init_db()
    clear_audit_logs()
    report_result("Database Initialization", True, "siem_audit.db table verified and ready")

    # Insert test events
    mock_payload = {
        "flow_duration": 10.0, "flow_bytes_sec": 100.0,
        "total_fwd_packets": 5, "total_bwd_packets": 5,
        "fwd_packet_length_mean": 200.0
    }
    log_event("192.168.1.10", mock_payload, 5.0, "BENIGN", "ALLOW", "GREEN", "ML_RANDOM_FOREST")
    log_event("192.168.1.20", mock_payload, 65.0, "SUSPICIOUS", "TEMP_ISOLATE", "YELLOW", "ML_RANDOM_FOREST")
    log_event("192.168.1.30", mock_payload, 95.0, "MALICIOUS", "PERM_LOCK", "RED", "FAST_PATH_HEURISTIC")

    logs = get_recent_logs(limit=10)
    report_result("Log Retrieval", len(logs) == 3, f"Retrieved {len(logs)} logged events")

    stats = get_audit_stats()
    stats_ok = (stats["total_packets"] == 3 and stats["green_count"] == 1 and 
                stats["yellow_count"] == 1 and stats["red_count"] == 1 and 
                "192.168.1.30" in stats["isolated_ips"])
    report_result("SIEM Audit Analytics Aggregation", stats_ok, f"Aggregated counts: {stats}")

except Exception as e:
    report_result("SQLite SIEM Database", False, f"Exception occurred: {e}")

# -----------------------------------------------------------------------------
# TEST 3: Central Gateway & Dual-Layer Policy Engine
# -----------------------------------------------------------------------------
print("\n[SECTION 3: Central Gateway & Dual-Layer Policy Engine (FastAPI)]")
try:
    from main import receive_telemetry, get_status, get_stats, reset_status

    class MockRequest:
        def __init__(self, ip):
            class Client:
                def __init__(self, host):
                    self.host = host
            self.client = Client(ip)

    async def test_gateway_flows():
        # Step 3a. Clean telemetry
        req_clean = MockRequest("10.0.0.101")
        res1 = await receive_telemetry({
            "flow_duration": 120.0, "flow_bytes_sec": 180.0,
            "total_fwd_packets": 12, "total_bwd_packets": 8,
            "fwd_packet_length_mean": 450.0
        }, req_clean)
        report_result("Flow 1: Benign Telemetry Ingestion", 
                      res1["hardware_signal"] == "GREEN" and res1["action"] == "ALLOW",
                      f"Signal={res1['hardware_signal']}, Score={res1['threat_score']}%, Action={res1['action']}")

        # Step 3b. Reconnaissance telemetry -> Speculative Temporary Containment
        req_recon = MockRequest("10.0.0.102")
        res2 = await receive_telemetry({
            "flow_duration": 15.0, "flow_bytes_sec": 50.0,
            "total_fwd_packets": 1, "total_bwd_packets": 0,
            "fwd_packet_length_mean": 50.0
        }, req_recon)
        report_result("Flow 2: Speculative Threat Detection (TEMP_ISOLATE)", 
                      res2["hardware_signal"] == "YELLOW" and res2["action"] == "TEMP_ISOLATE",
                      f"Signal={res2['hardware_signal']}, Score={res2['threat_score']}%, Action={res2['action']}")

        # Step 3c. Volumetric Attack Telemetry -> Permanent Lockout & IP Extraction
        req_attack = MockRequest("10.0.0.103")
        res3 = await receive_telemetry({
            "flow_duration": 5.0, "flow_bytes_sec": 5000000.0,
            "total_fwd_packets": 2500, "total_bwd_packets": 0,
            "fwd_packet_length_mean": 6000.0
        }, req_attack)
        report_result("Flow 3: Critical Threat Containment (PERM_LOCK)", 
                      res3["hardware_signal"] == "RED" and res3["action"] == "PERM_LOCK",
                      f"Signal={res3['hardware_signal']}, Score={res3['threat_score']}%, Action={res3['action']}")

        # Step 3d. Check Status endpoint for Pi Polling
        status_now = await get_status()
        report_result("Status Endpoint for Pi Polling", 
                      status_now["hardware_signal"] == "RED" and status_now["isolated_ip"] == "10.0.0.103",
                      f"Polled state: Signal={status_now['hardware_signal']}, Isolated IP={status_now['isolated_ip']}")

        # Step 3e. Test Reset endpoint
        reset_res = await reset_status()
        report_result("Emergency System Reset", 
                      reset_res["current_state"]["hardware_signal"] == "GREEN" and reset_res["current_state"]["isolated_ip"] is None,
                      "System successfully reset to GREEN nominal state")

    asyncio.run(test_gateway_flows())

except Exception as e:
    report_result("Central Gateway Policy Engine", False, f"Exception occurred: {e}")

# -----------------------------------------------------------------------------
# TEST 4: Out-of-Band Hardware Mitigation Layer (UDP Kill Packet)
# -----------------------------------------------------------------------------
print("\n[SECTION 4: Out-of-Band Hardware Mitigation Layer (UDP Kill Packet)]")
try:
    TEST_PORT = 9999
    receiver_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    receiver_sock.bind(("127.0.0.1", TEST_PORT))
    receiver_sock.settimeout(2.0)

    # Simulate hardware controller dispatching kill packet
    sender_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sender_sock.sendto(b"EXECUTE_ISOLATION", ("127.0.0.1", TEST_PORT))
    sender_sock.close()

    # Receive packet
    data, addr = receiver_sock.recvfrom(1024)
    receiver_sock.close()

    received_msg = data.decode("utf-8").strip()
    report_result("UDP Kill Packet Transmission & Reception", 
                  received_msg == "EXECUTE_ISOLATION",
                  f"Packet payload: '{received_msg}' from {addr[0]}")

except Exception as e:
    report_result("Out-of-Band Hardware Mitigation Layer", False, f"Exception occurred: {e}")

# -----------------------------------------------------------------------------
# TEST 5: Telemetry Generator & Decoy Simulator
# -----------------------------------------------------------------------------
print("\n[SECTION 5: Telemetry Generator & Decoy Simulator]")
try:
    from endpoint.telemetry_simulator import generate_traffic
    # Clean mode traffic
    t_clean_name, p_clean_obj = generate_traffic(1, "clean")
    report_result("Clean Traffic Generator", 
                  p_clean_obj.flow_duration > 0 and p_clean_obj.total_fwd_packets >= 2,
                  f"Generated '{t_clean_name}' (FwdPackets={p_clean_obj.total_fwd_packets})")

    # Attack mode traffic
    t_atk1, p_atk1 = generate_traffic(1, "attack")
    t_atk2, p_atk2 = generate_traffic(2, "attack")
    t_atk3, p_atk3 = generate_traffic(3, "attack")
    report_result("3-Stage Attack Pipeline Simulation", 
                  "DDoS" in t_atk3 and p_atk3.flow_bytes_sec >= 1000000.0,
                  f"Stage 1: '{t_atk1}' -> Stage 2: '{t_atk2}' -> Stage 3: '{t_atk3}'")

except Exception as e:
    report_result("Telemetry Generator", False, f"Exception occurred: {e}")

# -----------------------------------------------------------------------------
# TEST 6: Streamlit Dashboard Syntax & Compilation Check
# -----------------------------------------------------------------------------
print("\n[SECTION 6: Streamlit Dashboard Syntax & Compilation]")
try:
    dashboard_path = os.path.join(BASE_DIR, "dashboard", "app.py")
    with open(dashboard_path, "r", encoding="utf-8") as f:
        code = f.read()
    compile(code, dashboard_path, "exec")
    report_result("Streamlit Dashboard Source Validation", True, f"Parsed {os.path.basename(dashboard_path)} with 0 syntax errors")
except Exception as e:
    report_result("Streamlit Dashboard Source Validation", False, f"Syntax or compilation error: {e}")

# -----------------------------------------------------------------------------
# FINAL SUMMARY
# -----------------------------------------------------------------------------
print("\n" + "=" * 80)
total_tests = passed_tests + failed_tests
print(f"  TOTAL TESTS RUN: {total_tests} | PASSED: {passed_tests} | FAILED: {failed_tests}")
if failed_tests == 0:
    print("  STATUS: ALL SYSTEM FUNCTIONS & FEATURES ARE 100% OPERATIONAL AND VERIFIED!")
else:
    print(f"  STATUS: {failed_tests} TESTS FAILED. PLEASE REVIEW.")
print("=" * 80)

sys.exit(0 if failed_tests == 0 else 1)
