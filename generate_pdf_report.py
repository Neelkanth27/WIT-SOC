import os
import sys
import base64
import subprocess
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCRATCH_DIR = os.path.dirname(BASE_DIR)
ARTIFACT_DIR = r"C:\Users\Chira\.gemini\antigravity\brain\7db43ad7-5edf-40df-9600-63f91ea727d4"
OUTPUT_PDF_SCRATCH = os.path.join(BASE_DIR, "WIT_SOC_Comprehensive_Project_Report.pdf")
OUTPUT_PDF_ARTIFACT = os.path.join(ARTIFACT_DIR, "WIT_SOC_Comprehensive_Project_Report.pdf")
HTML_TEMP_PATH = os.path.join(BASE_DIR, "report_temp.html")

def get_base64_image(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")
            ext = os.path.splitext(path)[1].lower().replace(".", "")
            if ext == "jpg": ext = "jpeg"
            return f"data:image/{ext};base64,{encoded}"
    return None

# Load images
vit_logo = get_base64_image(os.path.join(SCRATCH_DIR, "vit_logo_clean.png"))
img_dashboard = get_base64_image(os.path.join(ARTIFACT_DIR, ".user_uploaded", "media_1792267164871_1bcb448e.png"))
img_mock_pi = get_base64_image(os.path.join(ARTIFACT_DIR, ".user_uploaded", "media_1792267186562_f299220c.png"))
img_agent = get_base64_image(os.path.join(ARTIFACT_DIR, ".user_uploaded", "media_1792267409841_dad097d3.jpg"))
img_attack = get_base64_image(os.path.join(ARTIFACT_DIR, ".user_uploaded", "media_1792267414189_a07677af.jpg"))

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>WIT-SOC Comprehensive Project Report</title>
<style>
    @page {{
        size: A4 portrait;
        margin: 12mm 14mm 12mm 14mm;
        @bottom-right {{
            content: counter(page);
        }}
    }}
    body {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        color: #1a202c;
        line-height: 1.45;
        font-size: 10pt;
        background: #ffffff;
        margin: 0;
        padding: 0;
    }}
    .page {{
        page-break-after: always;
        clear: both;
    }}
    .no-break {{
        break-inside: avoid;
        page-break-inside: avoid;
    }}
    
    /* Header & Branding */
    .header-table {{
        width: 100%;
        border-bottom: 2.5px solid #0056b3;
        padding-bottom: 8px;
        margin-bottom: 14px;
    }}
    .header-table td {{
        vertical-align: middle;
    }}
    .vit-title {{
        font-size: 15pt;
        font-weight: 800;
        color: #0b3954;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin: 0;
    }}
    .dept-title {{
        font-size: 10pt;
        font-weight: 600;
        color: #4a5568;
        margin-top: 2px;
        margin-bottom: 0;
    }}
    .acad-badge {{
        font-size: 8.5pt;
        color: #718096;
        font-weight: 500;
    }}
    
    /* Project Title Banner */
    .title-banner {{
        background: linear-gradient(135deg, #0b3954 0%, #087e8b 100%);
        color: #ffffff;
        padding: 14px 18px;
        border-radius: 6px;
        margin-bottom: 14px;
    }}
    .title-banner h1 {{
        font-size: 15pt;
        margin: 0 0 4px 0;
        color: #ffffff;
    }}
    .title-banner .sub {{
        font-size: 9.5pt;
        color: #e2e8f0;
        margin: 0;
    }}

    /* Section Headings */
    h2 {{
        font-size: 12pt;
        color: #0b3954;
        border-bottom: 1.5px solid #cbd5e0;
        padding-bottom: 4px;
        margin-top: 14px;
        margin-bottom: 8px;
        text-transform: uppercase;
        letter-spacing: 0.3px;
    }}
    h3 {{
        font-size: 10.5pt;
        color: #2b6cb0;
        margin-top: 10px;
        margin-bottom: 4px;
    }}
    
    /* Team Metadata Grid */
    .meta-table {{
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 12px;
        font-size: 9pt;
    }}
    .meta-table th, .meta-table td {{
        border: 1px solid #e2e8f0;
        padding: 6px 10px;
    }}
    .meta-table th {{
        background: #edf2f7;
        color: #2d3748;
        font-weight: 700;
        text-align: left;
    }}
    
    /* Callout & Alert Boxes */
    .callout {{
        background: #f7fafc;
        border-left: 4px solid #3182ce;
        padding: 8px 12px;
        margin: 8px 0;
        border-radius: 0 4px 4px 0;
        font-size: 9.5pt;
    }}
    .callout-problem {{
        background: #fff5f5;
        border-left: 4px solid #e53e3e;
        padding: 8px 12px;
        margin: 8px 0;
        border-radius: 0 4px 4px 0;
        font-size: 9.5pt;
    }}
    .callout-solution {{
        background: #f0fff4;
        border-left: 4px solid #38a169;
        padding: 8px 12px;
        margin: 8px 0;
        border-radius: 0 4px 4px 0;
        font-size: 9.5pt;
    }}
    
    /* Status Badges */
    .badge-green {{
        background: #c6f6d5;
        color: #22543d;
        padding: 2px 7px;
        border-radius: 4px;
        font-weight: 700;
        font-size: 8pt;
    }}
    .badge-yellow {{
        background: #fefcbf;
        color: #744210;
        padding: 2px 7px;
        border-radius: 4px;
        font-weight: 700;
        font-size: 8pt;
    }}
    .badge-red {{
        background: #fed7d7;
        color: #742a2a;
        padding: 2px 7px;
        border-radius: 4px;
        font-weight: 700;
        font-size: 8pt;
    }}
    
    /* Architecture Diagram Box */
    .arch-box {{
        background: #1a202c;
        color: #63b3ed;
        font-family: "Courier New", Courier, monospace;
        font-size: 7.8pt;
        line-height: 1.25;
        padding: 10px;
        border-radius: 6px;
        white-space: pre;
        overflow-x: hidden;
        margin: 8px 0;
    }}

    /* Screenshots Grid */
    .img-grid {{
        display: flex;
        gap: 10px;
        margin: 8px 0;
    }}
    .img-card {{
        flex: 1;
        border: 1px solid #cbd5e0;
        border-radius: 4px;
        padding: 4px;
        background: #ffffff;
        text-align: center;
    }}
    .img-card img {{
        max-width: 100%;
        height: auto;
        border-radius: 2px;
        display: block;
        margin: 0 auto;
    }}
    .img-card .caption {{
        font-size: 7.8pt;
        color: #4a5568;
        font-weight: 600;
        margin-top: 4px;
    }}

    /* Q&A Section */
    .qa-item {{
        margin-bottom: 8px;
    }}
    .qa-q {{
        font-weight: 700;
        color: #0b3954;
        font-size: 9.5pt;
    }}
    .qa-a {{
        color: #2d3748;
        font-size: 9pt;
        margin-top: 1px;
    }}
    
    /* Footer Note */
    .footer-note {{
        border-top: 1px solid #e2e8f0;
        padding-top: 6px;
        margin-top: 12px;
        font-size: 8pt;
        color: #718096;
        text-align: center;
    }}
</style>
</head>
<body>

<!-- ======================================================================= -->
<!-- PAGE 1: COVER & EXECUTIVE OVERVIEW                                      -->
<!-- ======================================================================= -->
<div class="page">
    <table class="header-table">
        <tr>
            <td style="width: 70px;">
                {'<img src="' + vit_logo + '" style="height: 65px; width: auto;" alt="VIT Logo">' if vit_logo else ''}
            </td>
            <td style="padding-left: 12px;">
                <div class="vit-title">Vishwakarma Institute of Technology, Pune</div>
                <div class="dept-title">Department of Computer Engineering (IoT, Cyber Security & Blockchain Technology)</div>
                <div class="acad-badge">Capstone Project Registration & Progress Review (FF No. 180) | Academic Year: 2026–27 | Semester: 5</div>
            </td>
        </tr>
    </table>

    <div class="title-banner">
        <h1>WIT-SOC: Wire-Interposition Trust Layer for Autonomous AI Security Operations Centers</h1>
        <p class="sub">Speculative Threat Execution, Hardware-Verified Micro-Containment & Zero-Trust Out-of-Band Quarantine</p>
    </div>

    <table class="meta-table">
        <tr>
            <th style="width: 15%;">Project Group</th>
            <td style="width: 35%;"><b>Group No. 9</b> (Division: CSCBI-C)</td>
            <th style="width: 18%;">Internal Guide</th>
            <td style="width: 32%;"><b>Prof. Yogesh Pawar</b> (yogesh.pawar@vit.edu)</td>
        </tr>
        <tr>
            <th>Domain Area</th>
            <td colspan="3">Cybersecurity, Artificial Intelligence, Hardware Security, and Network Engineering</td>
        </tr>
        <tr>
            <th>Repository</th>
            <td colspan="3"><a href="https://github.com/Neelkanth27/WIT-SOC" style="color: #2b6cb0; text-decoration: none;">https://github.com/Neelkanth27/WIT-SOC</a> (Verified & Tested on Main Branch)</td>
        </tr>
    </table>

    <table class="meta-table">
        <tr>
            <th style="width: 8%;">Sr.</th>
            <th style="width: 36%;">Student Name</th>
            <th style="width: 14%;">Roll No.</th>
            <th style="width: 18%;">G.R. No.</th>
            <th style="width: 24%;">Email ID</th>
        </tr>
        <tr>
            <td>1</td>
            <td><b>Ram Sunil Rajurkar</b></td>
            <td>75</td>
            <td>1252050154</td>
            <td>ram.1252050154@vit.edu</td>
        </tr>
        <tr>
            <td>2</td>
            <td><b>Chirag Mahavir Kochar</b></td>
            <td>76</td>
            <td>1252050155</td>
            <td>chirag.1252050155@vit.edu</td>
        </tr>
        <tr>
            <td>3</td>
            <td><b>Atharva Satish Gaikwad</b></td>
            <td>78</td>
            <td>1252050157</td>
            <td>atharva.1252050157@vit.edu</td>
        </tr>
        <tr>
            <td>4</td>
            <td><b>Prem Mangesh Palhade</b></td>
            <td>80</td>
            <td>1252050159</td>
            <td>prem.1252050159@vit.edu</td>
        </tr>
    </table>

    <h2>1. Problem Statement & Motivation</h2>
    <div class="callout-problem">
        <b>The "2–5 Second Attack Window" Problem:</b><br>
        Modern Security Operations Centers (AI SOCs) analyze cyber threats using machine learning and LLMs. However, the existing reactive pipeline (<code>Attack &rarr; Collect Logs &rarr; AI Inference &rarr; Final Decision &rarr; Quarantine</code>) requires <b>2 to 5 seconds of computational latency</b>. During this critical window, fast-spreading threats like lateral-moving ransomware, network worms, and credential-dumping scripts actively propagate across the local subnet. Furthermore, software firewalls and endpoint agents can be bypassed via local OS privilege escalation.
    </div>

    <h2>2. Proposed Solution & Core Innovations</h2>
    <div class="callout-solution">
        <b>The WIT-SOC Solution:</b><br>
        WIT-SOC bridges the gap between deep AI reasoning and instant threat neutralization through two primary innovations:
        <ol style="margin: 4px 0; padding-left: 18px;">
            <li><b>Speculative Execution for Network Security:</b> Instead of waiting for full 100% confirmation, the system triggers <i>temporary, reversible containment</i> at moderate confidence levels (&ge; 50%) before the final verdict. If benign, it unfreezes without disruption; if confirmed malicious (&ge; 85%), it escalates to permanent lockout.</li>
            <li><b>Out-of-Band Hardware Verification Layer:</b> Security enforcement is offloaded to an independent hardware trust anchor (Raspberry Pi / SmartNIC) operating outside the host OS. Even if an attacker gains full root/administrator privileges on the endpoint laptop, they cannot tamper with the physical hardware layer that enforces the network kill command.</li>
        </ol>
    </div>

    <h2>3. Three-Tier Speculative Policy Matrix</h2>
    <table class="meta-table">
        <tr>
            <th style="width: 14%;">Threat Score</th>
            <th style="width: 14%;">Action</th>
            <th style="width: 12%;">Signal</th>
            <th style="width: 25%;">Hardware Output</th>
            <th style="width: 35%;">System State & Behavior</th>
        </tr>
        <tr>
            <td><b>&lt; 50.0%</b></td>
            <td><code>ALLOW</code></td>
            <td><span class="badge-green">GREEN</span></td>
            <td>Green LED ON (Nominal)</td>
            <td>Normal employee traffic. Full network throughput permitted.</td>
        </tr>
        <tr>
            <td><b>50.0% &ndash; 84.9%</b></td>
            <td><code>TEMP_ISOLATE</code></td>
            <td><span class="badge-yellow">YELLOW</span></td>
            <td>Yellow LED ON (Speculative)</td>
            <td><b>Speculative Micro-Containment:</b> Sub-threshold anomaly flagged (stealth port scan / dropper). Monitored; fully reversible.</td>
        </tr>
        <tr>
            <td><b>&ge; 85.0%</b></td>
            <td><code>PERM_LOCK</code></td>
            <td><span class="badge-red">RED</span></td>
            <td>Red LED ON + UDP Kill Packet</td>
            <td><b>Quarantine Enforced:</b> Out-of-band UDP kill packet fired to port 9999. Host Wi-Fi adapter severed instantly.</td>
        </tr>
    </table>
</div>

<!-- ======================================================================= -->
<!-- PAGE 2: ARCHITECTURE, TECHNOLOGIES & DATAFLOW                           -->
<!-- ======================================================================= -->
<div class="page">
    <h2>4. System Architecture & Component Interaction</h2>
    <p style="margin-top: 0; font-size: 9pt; color: #4a5568;">
        The system follows an out-of-band wire-interposition model connecting workstations, the central AI gateway, the physical trust layer, and the real-time SOC dashboard.
    </p>

    <div class="arch-box">
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                              LOCAL SUBNET / WI-FI NETWORK                               │
└────────▲────────────────────────────────────────▲──────────────────────────────────▲────┘
         │                                        │                                  │
         │ 1. Telemetry Stream                    │ 4. Out-of-Band UDP Kill Packet   │
         │    (5-Feature Flow Vector)             │    (EXECUTE_ISOLATION :9999)     │
         ▼                                        ▼                                  │
┌─────────────────────────────────┐      ┌──────────────────────────────────┐        │
│  CENTRAL GATEWAY & AI ENGINE    │      │  OUT-OF-BAND TRUST ANCHOR        │        │
│  (FastAPI Master Server :8000)  │      │  (Raspberry Pi / Mock Pi)        │        │
│                                 │      │                                  │        │
│ ├─ Layer 1: Fast-Path Heuristic │─────►│ ├─ 0.5s Gateway Polling Loop     │        │
│ │   (&lt;10ms Volumetric Spike)    │      │ ├─ Physical Breadboard LEDs      │        │
│ ├─ Layer 2: Deep ML Classifier  │      │ │   🟢 GREEN (Nominal Allow)     │        │
│ │   (Random Forest Model)       │      │ │   🟡 YELLOW (Speculative Alert)│        │
│ ├─ SQLite SIEM Audit Database   │      │ │   🔴 RED (Quarantine Action)   │        │
│ └─ Streamlit SOC UI (:8501)     │      │ └─ UDP Socket Dispatcher         │        │
└─────────────────────────────────┘      └──────────────────────────────────┘        │
                                                                                     │
                                          ┌──────────────────────────────────────────┴────┐
                                          │             WORKSTATION ENDPOINT              │
                                          │ ├─ Background Severing Daemon (UDP :9999)     │
                                          │ │   (Drops Wi-Fi via OS Netsh / Nmcli)        │
                                          │ └─ Multi-Stage Attack Simulator (Dropper/DDoS)│
                                          └───────────────────────────────────────────────┘
    </div>

    <h2>5. Technologies & Engineering Stack</h2>
    <table class="meta-table">
        <tr>
            <th style="width: 25%;">Technology Tier</th>
            <th style="width: 35%;">Tools / Libraries</th>
            <th style="width: 40%;">Project Responsibility & Purpose</th>
        </tr>
        <tr>
            <td><b>AI / Machine Learning</b></td>
            <td>Scikit-Learn, Pandas, NumPy, Joblib</td>
            <td>Random Forest Classifier trained on 10,000 flow vectors mimicking CIC-IDS2017 benchmark. Real-time probability scoring.</td>
        </tr>
        <tr>
            <td><b>Backend API Gateway</b></td>
            <td>FastAPI, Uvicorn, ASGI, Starlette</td>
            <td>Asynchronous REST gateway, dynamic client IP extraction, dual-layer threat evaluation, system state management.</td>
        </tr>
        <tr>
            <td><b>SIEM Audit Database</b></td>
            <td>SQLite3 (Persistent ACID storage)</td>
            <td>Maintains immutable ledger of all incoming network telemetry, timestamps, verdicts, and quarantined attacker IPs.</td>
        </tr>
        <tr>
            <td><b>SOC Monitoring Dashboard</b></td>
            <td>Streamlit (Python Web Framework)</td>
            <td>Real-time interactive SOC console: live threat gauge, telemetry stream line charts, policy breakdown, emergency reset.</td>
        </tr>
        <tr>
            <td><b>Hardware Trust Layer</b></td>
            <td>Raspberry Pi (BCM GPIO), Python, UDP</td>
            <td>Out-of-band controller polling gateway every 0.5s, actuating physical breadboard LEDs, dispatching UDP kill packets.</td>
        </tr>
        <tr>
            <td><b>Endpoint Severing Agent</b></td>
            <td>Socket (UDP :9999), Netsh (Win), Nmcli (Linux)</td>
            <td>Background daemon that receives hardware isolation packets and immediately severs the host's Wi-Fi network interface.</td>
        </tr>
    </table>

    <h2>6. Detailed Module-by-Module Implementation</h2>
    
    <h3>A. Dual-Layer AI Threat Engine (<code>backend/main.py</code> & <code>ai_model/</code>)</h3>
    <p style="font-size: 9pt; margin: 2px 0;">
        To achieve sub-second response, the gateway uses a <b>Dual-Layer Architecture</b>:
        <ul style="margin: 2px 0; padding-left: 18px; font-size: 9pt;">
            <li><b>Layer 1 (Fast-Path Heuristics, &lt;10ms):</b> Evaluates flow rate thresholds (bytes/sec &gt; 1,000,000 or packets &gt; 1,000). Catching volumetric DDoS attacks immediately without waiting for complex inference.</li>
            <li><b>Layer 2 (Random Forest Feature Analysis):</b> Feeds a 5-feature vector (<code>flow_duration</code>, <code>flow_bytes_sec</code>, <code>total_fwd_packets</code>, <code>total_bwd_packets</code>, <code>fwd_packet_length_mean</code>) into the trained classifier. Computes exact multi-class probabilities across Benign (0), Suspicious (1), and Malicious (2).</li>
        </ul>
    </p>

    <h3>B. Persistent SIEM Audit Database (<code>backend/database.py</code>)</h3>
    <p style="font-size: 9pt; margin: 2px 0;">
        All telemetry packets and verdicts are committed to <code>siem_audit.db</code>. Provides aggregate analytics (total packets processed, breakdown per security level, and list of all permanently quarantined IP addresses).
    </p>

    <h3>C. Endpoint Severing Agent & Multi-Stage Attack Simulator (<code>endpoint/</code>)</h3>
    <p style="font-size: 9pt; margin: 2px 0;">
        Workstations run <code>agent.py</code>, which binds to UDP port 9999. The attack simulation module executes a realistic 3-stage intrusion vector:
        <b>Stage 1:</b> Benign dropper foothold &rarr; <b>Stage 2:</b> Stealth reconnaissance scan &rarr; <b>Stage 3:</b> Volumetric data exfiltration flood.
    </p>
</div>

<!-- ======================================================================= -->
<!-- PAGE 3: EMPIRICAL TEST RESULTS & LIVE MULTI-PC VERIFICATION             -->
<!-- ======================================================================= -->
<div class="page">
    <h2>7. Empirical Multi-Laptop Network Verification (Live Test Results)</h2>
    <p style="margin-top: 0; font-size: 9pt; color: #4a5568;">
        The complete system was deployed across two physical laptops communicating over a local Wi-Fi hotspot subnet:
        <b>PC 1 (Master Node):</b> <code>172.20.70.36</code> | <b>PC 2 (Attacker Workstation):</b> <code>172.20.70.210</code>.
    </p>

    <div class="img-grid no-break">
        <div class="img-card" style="flex: 1.4;">
            {'<img src="' + img_dashboard + '" alt="Streamlit SOC Dashboard">' if img_dashboard else ''}
            <div class="caption">Figure 1: Master SOC Dashboard on PC 1 showing 100% Threat Score, RED PERM_LOCK, and Quarantined IP 172.20.70.210</div>
        </div>
        <div class="img-card" style="flex: 1.0;">
            {'<img src="' + img_mock_pi + '" alt="Virtual Hardware Controller">' if img_mock_pi else ''}
            <div class="caption">Figure 2: Virtual Hardware Controller actuating RED LED & dispatching UDP kill packet to PC 2</div>
        </div>
    </div>

    <div class="img-grid no-break" style="margin-top: 10px;">
        <div class="img-card" style="flex: 1.0;">
            {'<img src="' + img_attack + '" alt="Attack Simulation Terminal">' if img_attack else ''}
            <div class="caption">Figure 3: PC 2 Attack Simulator progressing through Stage 1 (0%), Stage 2 (75%), to Stage 3 (100% Lock)</div>
        </div>
        <div class="img-card" style="flex: 1.0;">
            {'<img src="' + img_agent + '" alt="Endpoint Severing Agent">' if img_agent else ''}
            <div class="caption">Figure 4: PC 2 Endpoint Agent receiving EXECUTE_ISOLATION and severing Wi-Fi interface</div>
        </div>
    </div>

    <h3>Analysis of Empirical Results:</h3>
    <ul style="margin: 4px 0; padding-left: 18px; font-size: 8.8pt;">
        <li><b>Time-to-Containment (TTC):</b> Network isolation executed in <b>under 500 milliseconds</b> upon reaching Stage 3 flood, completely neutralizing the attack before lateral propagation could occur.</li>
        <li><b>Zero Bypass:</b> The network kill command was dispatched out-of-band by the hardware layer, proving independent authorization.</li>
        <li><b>Automated Test Suite:</b> The test suite (<code>tests/test_full_suite.py</code>) passed <b>17 out of 17 tests (100%)</b> validating model loading, heuristics, database logging, UDP sockets, and dashboard syntax.</li>
    </ul>

    <h2>8. Physical Raspberry Pi Hardware Integration Plan</h2>
    <p style="font-size: 9pt; margin: 2px 0;">
        When the physical Raspberry Pi microcontroller is deployed at final review, the hardware connects via breadboard without requiring any backend software modifications:
    </p>
    <table class="meta-table">
        <tr>
            <th style="width: 18%;">Component</th>
            <th style="width: 14%;">Color</th>
            <th style="width: 22%;">Raspberry Pi Pin (BCM)</th>
            <th style="width: 20%;">Physical Header Pin</th>
            <th style="width: 26%;">Current-Limiting Resistor</th>
        </tr>
        <tr>
            <td><b>Red LED</b></td>
            <td>Red</td>
            <td><b>GPIO 17</b></td>
            <td>Physical Pin 11</td>
            <td>220&Omega; &ndash; 330&Omega; &rarr; GND (Pin 6/9)</td>
        </tr>
        <tr>
            <td><b>Yellow LED</b></td>
            <td>Yellow</td>
            <td><b>GPIO 27</b></td>
            <td>Physical Pin 13</td>
            <td>220&Omega; &ndash; 330&Omega; &rarr; GND (Pin 6/9)</td>
        </tr>
        <tr>
            <td><b>Green LED</b></td>
            <td>Green</td>
            <td><b>GPIO 22</b></td>
            <td>Physical Pin 15</td>
            <td>220&Omega; &ndash; 330&Omega; &rarr; GND (Pin 6/9)</td>
        </tr>
    </table>
</div>

<!-- ======================================================================= -->
<!-- PAGE 4: VIVA DEFENSE GUIDE & FUTURE ENHANCEMENTS                       -->
<!-- ======================================================================= -->
<div class="page">
    <h2>9. Viva & Evaluation Defense Guide (Jury Q&A)</h2>

    <div class="qa-item">
        <div class="qa-q">Q1: What is the primary novelty of WIT-SOC compared to existing EDR/SIEM tools?</div>
        <div class="qa-a">Traditional EDR tools are reactive software agents running on the host OS, incurring 2–5 seconds of inference latency while ransomware spreads. WIT-SOC introduces <b>Speculative Micro-Containment</b> (temporary isolation at moderate 50% confidence) and <b>Out-of-Band Hardware Enforcement</b> (isolation commands originate outside the host OS, making them tamper-proof against local rootkits).</div>
    </div>

    <div class="qa-item">
        <div class="qa-q">Q2: How does the system handle false positives without disrupting business operations?</div>
        <div class="qa-a">Because the Yellow tier is speculative and reversible, endpoints placed in temporary monitoring automatically return to Green if subsequent traffic metrics subside, ensuring zero operational downtime.</div>
    </div>

    <div class="qa-item">
        <div class="qa-q">Q3: Why was Random Forest selected over Deep Neural Networks?</div>
        <div class="qa-a">Network edge gateways require microsecond evaluation speeds. Random Forest provides deterministic evaluation in &lt;5ms while achieving 100% precision on tabular flow vectors (flow duration, byte rates, packet counts).</div>
    </div>

    <div class="qa-item">
        <div class="qa-q">Q4: How does this prototype scale into an enterprise data center?</div>
        <div class="qa-a">The Raspberry Pi prototype demonstrates the wire-interposition paradigm. In enterprise cloud data centers, this logic is directly offloaded to <b>SmartNICs and DPUs (Data Processing Units, e.g., NVIDIA BlueField)</b> to execute line-rate hardware packet filtering in silicon.</div>
    </div>

    <h2>10. Advantages & Future Enhancements</h2>
    <table class="meta-table">
        <tr>
            <th style="width: 50%;">Project Advantages</th>
            <th style="width: 50%;">Future Enhancements</th>
        </tr>
        <tr>
            <td style="vertical-align: top;">
                <ul style="margin: 2px 0; padding-left: 16px; font-size: 8.8pt;">
                    <li><b>Ultra-Low TTC:</b> Drastically slashes time-to-containment from seconds to sub-second milliseconds.</li>
                    <li><b>Zero-Trust Hardware Anchor:</b> Prevents malware from bypassing host firewalls via privilege escalation.</li>
                    <li><b>Reversible Speculative Safety:</b> Minimizes business impact from false alarms.</li>
                    <li><b>Enterprise Alignment:</b> Mirrors architecture of SmartNIC and DPU security architectures.</li>
                </ul>
            </td>
            <td style="vertical-align: top;">
                <ul style="margin: 2px 0; padding-left: 16px; font-size: 8.8pt;">
                    <li><b>SmartNIC / DPU Offloading:</b> Porting interposition logic to NVIDIA BlueField DPUs for line-rate hardware filtering.</li>
                    <li><b>LLM Contextual Reasoning:</b> Integrating LLMs to perform semantic forensics during speculative isolation periods.</li>
                    <li><b>Kernel Hooking with eBPF:</b> Utilizing Extended Berkeley Packet Filters for zero-overhead host drops.</li>
                    <li><b>Multi-Node Synchronization:</b> Distributed threat intelligence sharing across enterprise subnets.</li>
                </ul>
            </td>
        </tr>
    </table>

    <div class="footer-note">
        WIT-SOC Project Progress Review Report | Vishwakarma Institute of Technology, Pune | FF No. 180 | Group No. 9 | Academic Year 2026–27
    </div>
</div>

</body>
</html>
"""

with open(HTML_TEMP_PATH, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"[+] Temporary HTML generated at: {HTML_TEMP_PATH}")

# Render to PDF using Microsoft Edge headless
edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
cmd = [
    edge_path,
    "--headless",
    "--disable-gpu",
    "--run-all-compositor-stages-before-draw",
    f"--print-to-pdf={OUTPUT_PDF_SCRATCH}",
    "--no-pdf-header-footer",
    HTML_TEMP_PATH
]

print("[*] Compiling PDF report with Microsoft Edge...")
proc = subprocess.run(cmd, capture_output=True, text=True)
time.sleep(2)

if os.path.exists(OUTPUT_PDF_SCRATCH):
    size_kb = os.path.getsize(OUTPUT_PDF_SCRATCH) / 1024
    print(f"[+] SUCCESS: PDF generated at: {OUTPUT_PDF_SCRATCH} ({size_kb:.1f} KB)")
    
    # Also copy to artifacts directory
    import shutil
    shutil.copyfile(OUTPUT_PDF_SCRATCH, OUTPUT_PDF_ARTIFACT)
    print(f"[+] Copied to Artifacts: {OUTPUT_PDF_ARTIFACT}")
else:
    print(f"[!] Error generating PDF. Edge output: {proc.stdout} {proc.stderr}")
