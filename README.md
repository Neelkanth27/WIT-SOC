# WIT-SOC: Wire-Interposition Trust Layer for Autonomous AI Security Operations Centers

[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/FastAPI-0.110%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![Dashboard](https://img.shields.io/badge/Streamlit-1.35%2B-FF4B4B.svg)](https://streamlit.io/)
[![Hardware](https://img.shields.io/badge/Hardware-Raspberry%20Pi-C51A4A.svg)](https://www.raspberrypi.com/)
[![Academic Year](https://img.shields.io/badge/Academic%20Year-2026--27-orange.svg)]()

> **Department of Computer Engineering (IoT, Cyber Security & Blockchain Technology)**  
> **Vishwakarma Institute of Technology, Pune**  
> **Semester 5 | Capstone Group No. 9**

---

## 👥 Project Team & Mentorship
* **Ram Sunil Rajurkar** (Roll: 75 | GR: 1252050154)
* **Chirag Mahavir Kochar** (Roll: 76 | GR: 1252050155)
* **Atharva Satish Gaikwad** (Roll: 78 | GR: 1252050157)
* **Prem Mangesh Palhade** (Roll: 80 | GR: 1252050159)
* **Internal Guide:** Prof. Yogesh Pawar

---

## 📌 Executive Summary & Problem Statement
Modern AI Security Operations Centers (AI SOCs) analyze cyber threats using machine learning and LLMs. However, the conventional reactive sequence:
$$\text{Attack} \longrightarrow \text{Collect Logs} \longrightarrow \text{AI Inference} \longrightarrow \text{Final Decision} \longrightarrow \text{Isolation}$$
incurs **2 to 5 seconds of computational latency**. 

During this critical window, fast-spreading threats (lateral-moving ransomware, worms, and credential theft scripts) rapidly compromise other hosts on the subnet. Furthermore, software firewalls on compromised machines can be disabled via OS-level privilege escalation.

**WIT-SOC** solves this by introducing:
1. **Speculative Execution for Network Security:** Enforcing temporary, reversible containment early at moderate confidence levels ($\ge 50\%$) *before* waiting for the final decision.
2. **Out-of-Band Hardware Verification Layer (Raspberry Pi):** An independent hardware trust anchor outside the host operating system that physically verifies threats and dispatches an immediate network kill command.

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          LOCAL NETWORK (WI-FI / LAN)                        │
└───────▲──────────────────────────────────────▲──────────────────────────▲───┘
        │                                      │                          │
        │ 1. Telemetry Stream                  │ 4. UDP Kill Packet       │
        │    (Flow Metrics)                    │    (EXECUTE_ISOLATION)   │
        ▼                                      ▼                          │
┌──────────────────────────────┐     ┌────────────────────────────┐       │
│  CENTRAL GATEWAY & AI ENGINE │     │   OUT-OF-BAND TRUST LAYER  │       │
│  (FastAPI Backend :8000)     │     │   (Raspberry Pi / Mock Pi) │       │
│                              │     │                            │       │
│ ├─ Layer 1: Fast Heuristics  │────►│ ├─ 0.5s Gateway Polling    │       │
│ │   (<10ms Volumetric Check) │     │ ├─ GPIO Breadboard LEDs    │       │
│ ├─ Layer 2: Random Forest ML │     │ │   🟢 GREEN (Normal)      │       │
│ │   (CIC-IDS2017 Model)      │     │ │   🟡 YELLOW (Speculative)│       │
│ ├─ SQLite SIEM Audit Ledger  │     │ │   🔴 RED (Quarantine)    │       │
│ └─ Streamlit SOC UI (:8501)  │     │ └─ UDP Socket Dispatcher   │       │
└──────────────────────────────┘     └────────────────────────────┘       │
                                                                          │
                                       ┌──────────────────────────────────┴───┐
                                       │       WORKSTATION ENDPOINT           │
                                       │ ├─ Network Agent (Port 9999)         │
                                       │ │   (Drops Wi-Fi via OS Netsh/Nmcli) │
                                       │ └─ Multi-Stage Attack Simulator      │
                                       └──────────────────────────────────────┘
```

---

## 📂 Repository Structure

```
WIT-SOC/
├── ai_model/                     # Machine Learning Threat Engine
│   ├── dataset/                  # Synthetic & CIC-IDS2017 training datasets
│   ├── generate_dataset.py       # Multi-class telemetry generator
│   ├── train_model.py            # Random Forest training & validation script
│   └── saved_model.pkl           # Pre-compiled high-performance ML model
│
├── backend/                      # Central Edge SOC Gateway
│   ├── database.py               # SQLite SIEM Audit Logging module
│   ├── main.py                   # FastAPI REST API & dual-layer inference
│   └── model.pkl                 # Active production threat model
│
├── dashboard/                    # Interactive SOC Web UI
│   └── app.py                    # Streamlit real-time monitoring dashboard
│
├── endpoint/                     # Workstation Agent & Threat Simulation
│   ├── agent.py                  # Background daemon listening on UDP 9999
│   ├── telemetry_simulator.py    # Flow traffic streamer (clean & attack modes)
│   ├── setup.py                  # Decoy Trojan updater (triggers attack)
│   └── install_update.bat        # Windows decoy batch launcher
│
├── hardware/                     # Out-of-Band Hardware Layer
│   ├── pi_hardware_led.py        # Raspberry Pi GPIO production controller
│   └── mock_pi_controller.py     # Virtual hardware controller for PC demos
│
├── run_backend.bat               # 1-Click launcher for FastAPI Gateway
├── run_dashboard.bat             # 1-Click launcher for Streamlit Dashboard
├── run_mock_pi.bat               # 1-Click launcher for Virtual Hardware
├── run_endpoint_agent.bat        # 1-Click launcher for Endpoint Agent
├── run_attack_demo.bat           # 1-Click launcher for Simulated Attack
└── requirements.txt              # Project dependencies
```

---

## 🚦 Three-Tier Speculative Policy Matrix

| Threat Score | Action | Signal | Hardware Output | System Behavior |
|:---|:---|:---:|:---:|:---|
| **$< 50\%$** | `ALLOW` | 🟢 **GREEN** | Green LED Active | Traffic verified benign. Normal operations permitted. |
| **$50\% - 84\%$** | `TEMP_ISOLATE` | 🟡 **YELLOW** | Yellow LED Active | **Speculative Containment:** Early anomaly flagged (port scan / reconnaissance). Reversible if score subsides. |
| **$\ge 85\%$** | `PERM_LOCK` | 🔴 **RED** | Red LED Active + UDP Kill | **Permanent Quarantine:** Out-of-band UDP kill packet fired to port `9999`. Host drops Wi-Fi adapter instantly. |

---

## 💻 Multi-Laptop Testing Guide (Without Raspberry Pi)

To test the complete end-to-end system across 2 to 3 laptops connected to the same Wi-Fi / Hotspot:

### Laptop 1: SOC Master Server
1. Find your IPv4 address using `ipconfig` (e.g., `192.168.43.50`).
2. Start the Backend Gateway:
   ```cmd
   run_backend.bat
   ```
3. Start the Live Streamlit Dashboard:
   ```cmd
   run_dashboard.bat
   ```
   *(Opens at `http://localhost:8501`)*
4. Start the Virtual Hardware Controller:
   ```cmd
   run_mock_pi.bat
   ```

### Laptop 2: Target / Attacker Laptop
1. Start the Endpoint Severing Agent:
   ```cmd
   run_endpoint_agent.bat
   ```
2. Trigger the simulated cyber attack:
   ```cmd
   run_attack_demo.bat
   ```
   *Enter Laptop 1's IP address when prompted.*
3. **Observation:**
   * Laptop 1 dashboard updates in real time to `🟡 YELLOW` during Reconnaissance.
   * Upon Stage 3 (Volumetric DDoS), status triggers `🔴 RED`.
   * Laptop 1's virtual hardware fires the UDP kill packet.
   * **Laptop 2's Wi-Fi adapter is immediately severed!**

### Laptop 3 (Optional): Benign Workstation
Run clean background telemetry to verify non-interference:
```cmd
python endpoint/telemetry_simulator.py
```
*(Remains 🟢 GREEN, never disconnected).*

---

## 🔌 Raspberry Pi Physical Integration

When deploying on the physical Raspberry Pi with breadboard LEDs:

### Pinout Mapping

| Component | Color | Raspberry Pi Pin (BCM GPIO) | Physical Pin # | Resistor Value | Ground Connection |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Red LED** | Red | **GPIO 17** | Pin 11 | 220Ω – 330Ω | GND (Pin 6 / 9) |
| **Yellow LED** | Yellow | **GPIO 27** | Pin 13 | 220Ω – 330Ω | GND (Pin 6 / 9) |
| **Green LED** | Green | **GPIO 22** | Pin 15 | 220Ω – 330Ω | GND (Pin 6 / 9) |

### Execution on Pi
```bash
cd hardware
python pi_hardware_led.py
```
*(Polls `GATEWAY_URL` every 0.5s, actuates physical LEDs, and dispatches the UDP kill packet on RED).*

---

## 📜 License
This project is developed as part of the academic curriculum at Vishwakarma Institute of Technology, Pune. Licensed under the MIT License.
