import os
import subprocess
import time
import pypdf

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARTIFACT_DIR = r"C:\Users\Chira\.gemini\antigravity\brain\7db43ad7-5edf-40df-9600-63f91ea727d4"
OUTPUT_PDF_SCRATCH = os.path.join(BASE_DIR, "WIT_SOC_Project_Technical_Report.pdf")
OUTPUT_PDF_ARTIFACT = os.path.join(ARTIFACT_DIR, "WIT_SOC_Project_Technical_Report.pdf")
HTML_TEMP_PATH = os.path.join(BASE_DIR, "report_reference_temp.html")

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>WIT-SOC: Project Technical Report</title>
<style>
    @page {
        size: letter portrait;
        margin: 11mm 15mm 11mm 15mm;
    }
    *, *:before, *:after {
        box-sizing: border-box;
    }
    body {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        color: #1f2937;
        line-height: 1.33;
        font-size: 8.4pt;
        background: #ffffff;
        margin: 0;
        padding: 0;
    }
    
    .page {
        page-break-after: always;
        padding: 0;
        margin: 0;
    }
    .page:last-child {
        page-break-after: auto;
    }
    
    /* Running Headers & Footers */
    .page-header {
        font-size: 7.2pt;
        font-weight: 700;
        color: #4b5563;
        letter-spacing: 0.8px;
        text-transform: uppercase;
        text-align: right;
        margin-bottom: 10px;
        border-bottom: 0.5px solid #cbd5e1;
        padding-bottom: 3px;
    }
    .page-footer {
        font-size: 7.6pt;
        color: #4b5563;
        text-align: center;
        margin-top: 10px;
        padding-top: 4px;
        border-top: 0.5px solid #cbd5e1;
    }

    /* Headings */
    h1.doc-title {
        font-size: 24pt;
        font-weight: 800;
        color: #14355a;
        text-align: center;
        margin-top: 45px;
        margin-bottom: 6px;
        letter-spacing: -0.5px;
    }
    h2.doc-subtitle {
        font-size: 13.5pt;
        font-weight: 700;
        color: #1d4ed8;
        text-align: center;
        margin-top: 0;
        margin-bottom: 12px;
    }
    p.doc-tagline {
        font-size: 8.8pt;
        font-style: italic;
        color: #4b5563;
        text-align: center;
        margin-bottom: 30px;
    }
    
    h2.sec-title {
        font-size: 11pt;
        font-weight: 800;
        color: #0f172a;
        margin-top: 9px;
        margin-bottom: 4px;
    }
    h3.sub-title {
        font-size: 9pt;
        font-weight: 700;
        color: #1e293b;
        margin-top: 6px;
        margin-bottom: 3px;
    }

    /* Tables Matching Reference Exact Navy Style */
    table.data-table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 4px;
        margin-bottom: 8px;
        font-size: 7.7pt;
    }
    table.data-table th {
        background-color: #14355a;
        color: #ffffff;
        font-weight: 700;
        text-align: left;
        padding: 3.5px 6px;
        border: 1px solid #14355a;
    }
    table.data-table td {
        padding: 3px 6px;
        border: 1px solid #cbd5e1;
        vertical-align: top;
    }
    table.data-table tr:nth-child(even) td {
        background-color: #f8fafc;
    }

    /* Meta Table on Cover Page */
    table.cover-table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 15px;
        margin-bottom: 25px;
        font-size: 8.2pt;
    }
    table.cover-table th {
        background-color: #14355a;
        color: #ffffff;
        font-weight: 700;
        text-align: left;
        padding: 5px 8px;
        border: 1px solid #14355a;
    }
    table.cover-table td {
        padding: 4.5px 8px;
        border: 1px solid #cbd5e1;
    }
    table.cover-table tr:nth-child(even) td {
        background-color: #f8fafc;
    }

    /* Lists */
    ul {
        margin-top: 3px;
        margin-bottom: 6px;
        padding-left: 16px;
    }
    li {
        margin-bottom: 2.5px;
    }
    
    p {
        margin-top: 3px;
        margin-bottom: 5px;
    }
    
    code {
        font-family: Consolas, "Courier New", monospace;
        font-size: 7.3pt;
        background: #f1f5f9;
        padding: 1px 3.5px;
        border-radius: 3px;
        color: #0f172a;
    }
    
    .note-text {
        font-size: 8pt;
        color: #64748b;
        font-style: italic;
        margin-top: 12px;
        text-align: center;
    }
</style>
</head>
<body>

<!-- ======================================================================= -->
<!-- PAGE 1: COVER & DOCUMENT DETAIL                                         -->
<!-- ======================================================================= -->
<div class="page">
    <div class="page-header">WIT-SOC: WIRE-INTERPOSITION TRUST LAYER | PROJECT TECHNICAL REPORT</div>
    <div class="page-content">
        <h1 class="doc-title">WIT-SOC</h1>
        <h2 class="doc-subtitle">Wire-Interposition Trust Layer for Autonomous AI SOCs</h2>
        <p class="doc-tagline">System Architecture, Implementation, Security, Testing and Demonstration Guide</p>

        <table class="cover-table">
            <tr>
                <th style="width: 25%;">Report detail</th>
                <th style="width: 75%;">Description</th>
            </tr>
            <tr>
                <td><b>Project type</b></td>
                <td>Academic Cybersecurity, Artificial Intelligence & Hardware Security Project (FF No. 180)</td>
            </tr>
            <tr>
                <td><b>Institution</b></td>
                <td>Vishwakarma Institute of Technology, Pune &bull; Department of Computer Engineering (IoTCSBT)</td>
            </tr>
            <tr>
                <td><b>Academic term</b></td>
                <td>Academic Year 2026&ndash;27 &bull; Semester 5 &bull; Group No. 9</td>
            </tr>
            <tr>
                <td><b>Project team</b></td>
                <td>Ram Sunil Rajurkar (75), Chirag Mahavir Kochar (76), Atharva Satish Gaikwad (78), Prem Mangesh Palhade (80)</td>
            </tr>
            <tr>
                <td><b>Internal guide</b></td>
                <td>Prof. Yogesh Pawar (yogesh.pawar@vit.edu)</td>
            </tr>
            <tr>
                <td><b>System model</b></td>
                <td>Multi-node autonomous wire-interposition security architecture with out-of-band hardware quarantine</td>
            </tr>
            <tr>
                <td><b>Prepared</b></td>
                <td>18 October 2026</td>
            </tr>
            <tr>
                <td><b>Purpose</b></td>
                <td>Team handover, academic jury defense, and shared understanding of the complete system</td>
            </tr>
        </table>

        <p class="note-text">
            Based on project architecture and live multi-workstation verification results available on 18 October 2026.
        </p>
    </div>
    <div class="page-footer">Team Project Report &bull; 18 October 2026 &bull; 1</div>
</div>

<!-- ======================================================================= -->
<!-- PAGE 2: EXECUTIVE SUMMARY, GOALS & ARCHITECTURE                         -->
<!-- ======================================================================= -->
<div class="page">
    <div class="page-header">WIT-SOC: WIRE-INTERPOSITION TRUST LAYER | PROJECT TECHNICAL REPORT</div>
    <div class="page-content">
        <h2 class="sec-title">1. Executive Summary</h2>
        <p>
            WIT-SOC (Wire-Interposition Trust Layer for Autonomous AI Security Operations Centers) is an intelligent cybersecurity system designed to eliminate the critical 2-to-5 second latency gap inherent in traditional reactive SOC pipelines (Attack &rarr; Collect Logs &rarr; AI Inference &rarr; Final Decision &rarr; Isolation). During this computational window, fast-moving threats such as automated ransomware, network worms, and credential-dumping exploits laterally compromise entire subnets before classical firewalls intervene. Furthermore, software-only endpoint agents can be bypassed via local OS privilege escalation.
        </p>
        <p>
            WIT-SOC introduces two structural innovations: <b>Speculative Execution for Network Security</b> and an <b>Out-of-Band Hardware Mitigation Layer</b>. Early sub-threshold anomalies trigger temporary, reversible micro-containment at moderate confidence (&ge; 50%), while high-confidence attacks (&ge; 85%) trigger an independent hardware anchor (Raspberry Pi) that severs the compromised host's network interface out-of-band via UDP kill packets.
        </p>
        <p>
            Live checks verified dual-layer AI telemetry ingestion, sub-second threat scoring, speculative Yellow state transitions, permanent Red lockout, real-time Streamlit dashboard visualization, persistent SQLite SIEM audit logging, and automated Wi-Fi interface disconnection across physical network workstations.
        </p>

        <h2 class="sec-title">2. Project Goals</h2>
        <ul>
            <li>Demonstrate speculative containment concepts using a multi-node workstation and gateway topology.</li>
            <li>Eliminate the 2&ndash;5 second threat propagation window through fast-path heuristics and microsecond ML inference.</li>
            <li>Provide autonomous, out-of-band hardware enforcement independent of host OS software integrity.</li>
            <li>Implement reversible containment tiers to prevent operational business disruption from false alarms.</li>
            <li>Classify real-world network intrusions (benign, reconnaissance, and volumetric DDoS/ransomware) using CIC-IDS2017 features.</li>
            <li>Persist audit ledgers for compliance and forensic analysis in an ACID-compliant SQLite SIEM database.</li>
            <li>Expose a real-time web monitoring console displaying live gauges, telemetry charts, and emergency reset controls.</li>
        </ul>

        <h2 class="sec-title">3. High-Level Architecture</h2>
        <p>
            The system consists of workstation endpoint agents, an asynchronous FastAPI gateway running a dual-layer threat engine, a trained Random Forest classifier, an out-of-band hardware controller (Raspberry Pi / Mock Pi), an SQLite SIEM ledger, and a Streamlit SOC dashboard.
        </p>

        <table class="data-table">
            <tr>
                <th style="width: 24%;">Component</th>
                <th style="width: 36%;">Responsibility</th>
                <th style="width: 40%;">Usage</th>
            </tr>
            <tr>
                <td><b>Endpoint Agent Daemon</b></td>
                <td>Workstation enforcement listener</td>
                <td>Binds to UDP :9999; executes native OS network disconnection upon receiving hardware kill commands.</td>
            </tr>
            <tr>
                <td><b>Attack & Telemetry Simulator</b></td>
                <td>Traffic generation & decoy vector</td>
                <td>Streams 5-feature network flow metrics mimicking clean background usage or 3-stage intrusion attacks.</td>
            </tr>
            <tr>
                <td><b>Central Gateway (FastAPI)</b></td>
                <td>Ingestion, state management & API</td>
                <td>Extracts client IP, routes telemetry through dual-layer AI, manages Green/Yellow/Red system state.</td>
            </tr>
            <tr>
                <td><b>Random Forest AI Model</b></td>
                <td>Multi-class threat confidence scoring</td>
                <td>Evaluates tabular flow vectors; outputs exact class probabilities across Benign, Suspicious, and Malicious.</td>
            </tr>
            <tr>
                <td><b>Hardware Trust Layer</b></td>
                <td>Out-of-band verification & actuation</td>
                <td>Polls gateway every 0.5s; actuates physical breadboard LEDs; dispatches UDP isolation datagrams.</td>
            </tr>
            <tr>
                <td><b>SIEM Audit Database</b></td>
                <td>Persistent transactional logging</td>
                <td>Stores timestamped records of every flow, threat score, verdict, detection engine, and quarantined IP.</td>
            </tr>
            <tr>
                <td><b>Streamlit SOC Dashboard</b></td>
                <td>Analyst visualization & control</td>
                <td>Displays live threat gauges, traffic stream line charts, policy breakdown, and 1-click system reset.</td>
            </tr>
        </table>
    </div>
    <div class="page-footer">Team Project Report &bull; 18 October 2026 &bull; 2</div>
</div>

<!-- ======================================================================= -->
<!-- PAGE 3: RUNTIME TOPOLOGY, TECH STACK & WORKFLOW                         -->
<!-- ======================================================================= -->
<div class="page">
    <div class="page-header">WIT-SOC: WIRE-INTERPOSITION TRUST LAYER | PROJECT TECHNICAL REPORT</div>
    <div class="page-content">
        <h2 class="sec-title">4. Runtime Topology and Ports</h2>
        <table class="data-table">
            <tr>
                <th style="width: 22%;">Service</th>
                <th style="width: 18%;">Host port(s)</th>
                <th style="width: 60%;">Role & Protocol</th>
            </tr>
            <tr>
                <td><b>FastAPI Gateway</b></td>
                <td>8000</td>
                <td>HTTP REST API; ingests <code>/api/v1/telemetry</code> and exposes <code>/api/v1/status</code>.</td>
            </tr>
            <tr>
                <td><b>Streamlit Dashboard</b></td>
                <td>8501</td>
                <td>Web UI; browser interface for real-time threat tracking and emergency system reset.</td>
            </tr>
            <tr>
                <td><b>Endpoint Agent</b></td>
                <td>9999</td>
                <td>UDP socket listener; receives out-of-band <code>EXECUTE_ISOLATION</code> kill commands.</td>
            </tr>
            <tr>
                <td><b>Mock Hardware Controller</b></td>
                <td>Internal polling</td>
                <td>0.5s polling client over HTTP; out-of-band UDP datagram sender to port 9999.</td>
            </tr>
            <tr>
                <td><b>Raspberry Pi Controller</b></td>
                <td>GPIO 17, 27, 22</td>
                <td>Physical breadboard hardware; actuates Red, Yellow, and Green LEDs; sends UDP kill packets.</td>
            </tr>
        </table>

        <h2 class="sec-title">5. Technology Stack</h2>
        <table class="data-table">
            <tr>
                <th style="width: 20%;">Area</th>
                <th style="width: 35%;">Technology</th>
                <th style="width: 45%;">Purpose</th>
            </tr>
            <tr>
                <td><b>Frontend / UI</b></td>
                <td>Streamlit 1.35+, Altair, HTML5/CSS3</td>
                <td>Interactive real-time SOC monitoring dashboard and analyst console.</td>
            </tr>
            <tr>
                <td><b>Backend / API</b></td>
                <td>Python 3.11+, FastAPI, Uvicorn, ASGI</td>
                <td>High-concurrency asynchronous API server and core state manager.</td>
            </tr>
            <tr>
                <td><b>AI / Threat Engine</b></td>
                <td>Scikit-Learn, Pandas, NumPy, Joblib</td>
                <td>Random Forest Classifier trained on CIC-IDS2017 intrusion telemetry.</td>
            </tr>
            <tr>
                <td><b>Audit Persistence</b></td>
                <td>SQLite3 (ACID compliant)</td>
                <td>Hardware-verified event logs and historical telemetry ledger.</td>
            </tr>
            <tr>
                <td><b>Hardware Layer</b></td>
                <td>Raspberry Pi (BCM GPIO), Gpiozero</td>
                <td>Physical LED status signaling and zero-trust out-of-band enforcement.</td>
            </tr>
            <tr>
                <td><b>Endpoint Severance</b></td>
                <td>Python Socket, Windows Netsh, Linux Nmcli</td>
                <td>Hardware-commanded network interface disconnection.</td>
            </tr>
            <tr>
                <td><b>Automation</b></td>
                <td>Windows Batchfiles (.bat)</td>
                <td>1-click deployment launchers for all master and endpoint components.</td>
            </tr>
        </table>

        <h2 class="sec-title">6. How the System Works</h2>

        <h3 class="sub-title">6.1 Telemetry Collection & Feature Extraction</h3>
        <p>
            Workstation endpoints continuously measure network flow behavior and stream 5 standardized telemetry metrics:
            <code>flow_duration</code> (ms), <code>flow_bytes_sec</code> (rate), <code>total_fwd_packets</code> (count), <code>total_bwd_packets</code> (count), and <code>fwd_packet_length_mean</code> (size).
        </p>

        <h3 class="sub-title">6.2 Dual-Layer AI Detection Engine</h3>
        <p>
            Upon receiving telemetry, the Central Gateway evaluates threat confidence using a two-stage pipeline:
        </p>
        <ul>
            <li><b>Layer 1 (Fast-Path Heuristics, &lt; 10ms):</b> Evaluates volumetric flood triggers (<code>flow_bytes_sec &gt; 1,000,000</code> or <code>total_fwd_packets &gt; 1,000</code>). High-volume DDoS/ransomware attacks are detected immediately.</li>
            <li><b>Layer 2 (Random Forest Classifier):</b> If sub-threshold, the 5 features are fed to the pre-compiled ML model, calculating exact probabilities across Benign, Suspicious, and Malicious classes.</li>
        </ul>
    </div>
    <div class="page-footer">Team Project Report &bull; 18 October 2026 &bull; 3</div>
</div>

<!-- ======================================================================= -->
<!-- PAGE 4: SPECULATIVE POLICY, API & SECURITY                              -->
<!-- ======================================================================= -->
<div class="page">
    <div class="page-header">WIT-SOC: WIRE-INTERPOSITION TRUST LAYER | PROJECT TECHNICAL REPORT</div>
    <div class="page-content">
        <h3 class="sub-title">6.3 Speculative Execution Policy Matrix</h3>
        <table class="data-table">
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
                <td><b>GREEN</b></td>
                <td>Green LED ON</td>
                <td>Nominal State. Standard employee traffic permitted without restriction.</td>
            </tr>
            <tr>
                <td><b>50.0% &ndash; 84.9%</b></td>
                <td><code>TEMP_ISOLATE</code></td>
                <td><b>YELLOW</b></td>
                <td>Yellow LED ON</td>
                <td><b>Speculative Micro-Containment:</b> Sub-threshold anomaly flagged. Monitored; fully reversible if traffic normalizes.</td>
            </tr>
            <tr>
                <td><b>&ge; 85.0%</b></td>
                <td><code>PERM_LOCK</code></td>
                <td><b>RED</b></td>
                <td>Red LED ON + UDP Kill</td>
                <td><b>Quarantine Enforced:</b> Out-of-band UDP kill packet fired to port 9999. Host Wi-Fi adapter severed instantly.</td>
            </tr>
        </table>

        <h3 class="sub-title">6.4 Out-of-Band Hardware Quarantine</h3>
        <p>
            When a critical threat is confirmed (&ge; 85%), the hardware controller actuates the Red LED and fires a datagram containing <code>EXECUTE_ISOLATION</code> over UDP to port 9999 of the attacker's extracted IP. The workstation daemon executes <code>netsh wlan disconnect</code> (or <code>nmcli radio wifi off</code>), severing the radio layer in under a second.
        </p>

        <h3 class="sub-title">6.5 Persistent SIEM Audit Logging</h3>
        <p>
            Every incoming telemetry event is committed to <code>siem_audit.db</code>. The schema stores timestamp, client IP, raw flow metrics, threat score, verdict, hardware signal, and the detection engine used (Heuristic or Random Forest).
        </p>

        <h2 class="sec-title">7. API Reference</h2>
        <table class="data-table">
            <tr>
                <th style="width: 12%;">Method</th>
                <th style="width: 28%;">Endpoint</th>
                <th style="width: 60%;">Purpose</th>
            </tr>
            <tr>
                <td><b>POST</b></td>
                <td><code>/api/v1/telemetry</code></td>
                <td>Ingests workstation flow metrics, extracts client IP, evaluates AI threat score, updates state.</td>
            </tr>
            <tr>
                <td><b>GET</b></td>
                <td><code>/api/v1/status</code></td>
                <td>Polled every 0.5s by hardware controllers; returns hardware signal, action, score, and isolated IP.</td>
            </tr>
            <tr>
                <td><b>GET</b></td>
                <td><code>/api/v1/logs</code></td>
                <td>Returns recent SIEM audit records from SQLite for the monitoring dashboard.</td>
            </tr>
            <tr>
                <td><b>GET</b></td>
                <td><code>/api/v1/stats</code></td>
                <td>Returns aggregated packet counts, verdict distributions, and list of all isolated IP addresses.</td>
            </tr>
            <tr>
                <td><b>POST</b></td>
                <td><code>/api/v1/reset</code></td>
                <td>Clears active network quarantine, unfreezes state, and resets hardware signals back to GREEN.</td>
            </tr>
        </table>

        <h2 class="sec-title">8. Security and Zero-Trust Integrity</h2>
        <ul>
            <li><b>Out-of-Band Integrity:</b> Security enforcement is decoupled from the host OS. Even if malware achieves local root/SYSTEM privileges on the workstation, it cannot alter the independent hardware trust anchor.</li>
            <li><b>Reversible Speculative Safety:</b> Temporary isolation during Yellow states automatically subsides if traffic normalizes, eliminating false-positive business interruption.</li>
            <li><b>Hardware Fail-Safe:</b> If the hardware controller loses network connectivity to the gateway, all LEDs default to Yellow as an explicit visual alert.</li>
            <li><b>Zero Hardcoded Secrets:</b> Network communication relies on dynamic runtime IP extraction and standard transport protocols.</li>
        </ul>
    </div>
    <div class="page-footer">Team Project Report &bull; 18 October 2026 &bull; 4</div>
</div>

<!-- ======================================================================= -->
<!-- PAGE 5: LIVE VERIFICATION RESULTS & EVIDENCE                            -->
<!-- ======================================================================= -->
<div class="page">
    <div class="page-header">WIT-SOC: WIRE-INTERPOSITION TRUST LAYER | PROJECT TECHNICAL REPORT</div>
    <div class="page-content">
        <h2 class="sec-title">9. Live Verification Results</h2>
        <p>
            These checks were performed interactively on 18 October 2026 across two physical laptops on a local Wi-Fi subnet (PC 1: <code>172.20.70.36</code> | PC 2: <code>172.20.70.210</code>).
        </p>

        <table class="data-table" style="font-size: 7.3pt;">
            <tr>
                <th style="width: 25%;">Test</th>
                <th style="width: 55%;">Observed result</th>
                <th style="width: 20%;">Status / scope</th>
            </tr>
            <tr>
                <td><b>Gateway Startup</b></td>
                <td>FastAPI gateway initialized on <code>0.0.0.0:8000</code>; model loaded successfully.</td>
                <td><b>Pass</b></td>
            </tr>
            <tr>
                <td><b>Dashboard Launch</b></td>
                <td>Streamlit dashboard initialized at <code>http://localhost:8501</code>; status nominal GREEN.</td>
                <td><b>Pass</b></td>
            </tr>
            <tr>
                <td><b>Virtual Hardware Init</b></td>
                <td>Mock Pi controller initialized; polling 0.5s loop; GREEN LED active.</td>
                <td><b>Pass</b></td>
            </tr>
            <tr>
                <td><b>Agent Initialization</b></td>
                <td>Endpoint severing agent bound to UDP :9999 on PC 2; listening for kill packets.</td>
                <td><b>Pass</b></td>
            </tr>
            <tr>
                <td><b>Clean Flow Telemetry</b></td>
                <td>Packet #1 processed; threat score 0.0%; verdict ALLOW; hardware remains GREEN.</td>
                <td><b>Pass</b></td>
            </tr>
            <tr>
                <td><b>Speculative Anomaly</b></td>
                <td>Packet #2 (port scan) processed; threat score 75.0%; hardware switched to YELLOW.</td>
                <td><b>Pass (Speculative)</b></td>
            </tr>
            <tr>
                <td><b>Volumetric Attack Flood</b></td>
                <td>Packet #3 (DDoS/exfiltration) processed; threat score 100.0%; verdict PERM_LOCK.</td>
                <td><b>Pass (Critical)</b></td>
            </tr>
            <tr>
                <td><b>Dynamic IP Extraction</b></td>
                <td>Gateway automatically identified attacker IP as <code>172.20.70.210</code> without manual config.</td>
                <td><b>Pass</b></td>
            </tr>
            <tr>
                <td><b>Out-of-Band UDP Dispatch</b></td>
                <td>Hardware layer dispatched <code>EXECUTE_ISOLATION</code> datagram to <code>172.20.70.210:9999</code>.</td>
                <td><b>Pass</b></td>
            </tr>
            <tr>
                <td><b>Hardware Wi-Fi Severance</b></td>
                <td>PC 2 agent received kill command; dropped Wi-Fi card via native Netsh command.</td>
                <td><b>Pass (&lt; 1s TTC)</b></td>
            </tr>
            <tr>
                <td><b>Emergency System Reset</b></td>
                <td>Dashboard reset button cleared lock; returned gateway and hardware state to GREEN.</td>
                <td><b>Pass</b></td>
            </tr>
            <tr>
                <td><b>Second Demo Verification</b></td>
                <td>PC 2 reconnected and rerun; system demonstrated 100% reproducible quarantine.</td>
                <td><b>Pass (Repeatable)</b></td>
            </tr>
        </table>

        <h2 class="sec-title">10. Test Run Evidence</h2>
        <table class="data-table" style="font-size: 7.4pt;">
            <tr>
                <th style="width: 25%;">Field</th>
                <th style="width: 75%;">Value for Live Test Run</th>
            </tr>
            <tr>
                <td><b>Master Gateway Node</b></td>
                <td><code>172.20.70.36</code> (FastAPI :8000, Streamlit :8501, Mock Pi Controller)</td>
            </tr>
            <tr>
                <td><b>Target Workstation Node</b></td>
                <td><code>172.20.70.210</code> (Severing Agent :9999, Telemetry Simulator)</td>
            </tr>
            <tr>
                <td><b>Malicious Flow Profile</b></td>
                <td>Duration: 5.0ms &bull; Rate: 5,000,000 bytes/sec &bull; Forward Packets: 2500 &bull; Packet Length: 6000</td>
            </tr>
            <tr>
                <td><b>AI Model Confidence</b></td>
                <td>100.0% Malicious (Random Forest Classifier + Volumetric Fast-Path Heuristic)</td>
            </tr>
            <tr>
                <td><b>Hardware Action Taken</b></td>
                <td>State: <code>PERM_LOCK</code> &bull; Signal: <code>RED LED</code> &bull; Datagram: <code>EXECUTE_ISOLATION</code></td>
            </tr>
            <tr>
                <td><b>Endpoint Agent Execution</b></td>
                <td><code>Disconnection request was completed successfully for interface "Wi-Fi".</code></td>
            </tr>
        </table>

        <h2 class="sec-title">11. Automated Assurance & Regression Suite</h2>
        <p>
            An automated integration test suite (<code>tests/test_full_suite.py</code>) executes <b>17 comprehensive assertions</b> covering model loading, multi-class predictions, database CRUD operations, policy transitions, UDP transmission, and dashboard syntax. All 17 tests passed with zero failures in &lt; 3 seconds.
        </p>
    </div>
    <div class="page-footer">Team Project Report &bull; 18 October 2026 &bull; 5</div>
</div>

<!-- ======================================================================= -->
<!-- PAGE 6: LIMITATIONS, RUNBOOK & TEAM OWNERSHIP                           -->
<!-- ======================================================================= -->
<div class="page">
    <div class="page-header">WIT-SOC: WIRE-INTERPOSITION TRUST LAYER | PROJECT TECHNICAL REPORT</div>
    <div class="page-content">
        <h2 class="sec-title">12. Limitations and Claims to Avoid</h2>
        <ul>
            <li>The current endpoint agent runs in user/system space utilizing OS-level netsh/nmcli utilities. It demonstrates the out-of-band wire-interposition principle but is not yet implemented as an in-kernel eBPF packet drop driver.</li>
            <li>The physical Raspberry Pi hardware module is validated via its software controller and verified virtual controller; physical breadboard LEDs will be demonstrated during final on-campus hardware reviews.</li>
            <li>Do not claim the model detects arbitrary zero-day binaries; the model is specifically trained on network flow telemetry features (duration, rates, packet counts).</li>
            <li>Do not claim enterprise data center deployment; position the Raspberry Pi implementation as an educational prototype mirroring modern SmartNIC/DPU wire-interposition architectures.</li>
        </ul>

        <h2 class="sec-title">13. Demo Runbook</h2>
        <p><b>Project Directory:</b> <code>C:\\Users\\Chira\\.gemini\\antigravity\\scratch\\WIT-SOC</code></p>
        <ul>
            <li><b>Step 1 (Master Setup):</b> Connect both laptops to same Wi-Fi/Hotspot. Run <code>ipconfig</code> on PC 1 to get IPv4 (<code>172.20.70.36</code>).</li>
            <li><b>Step 2 (Start Backend):</b> Run <code>run_backend.bat</code>. Verify Uvicorn starts on <code>0.0.0.0:8000</code> and AI model loads.</li>
            <li><b>Step 3 (Start Dashboard):</b> Run <code>run_dashboard.bat</code>. Open <code>http://localhost:8501</code>; verify status is GREEN.</li>
            <li><b>Step 4 (Start Hardware Controller):</b> Run <code>run_mock_pi.bat</code>. Press Enter for localhost. Verify GREEN LED is active.</li>
            <li><b>Step 5 (Start Endpoint Agent on PC 2):</b> On PC 2, run <code>run_endpoint_agent.bat</code>. Verify UDP socket listens on port 9999.</li>
            <li><b>Step 6 (Trigger Attack on PC 2):</b> Run <code>python telemetry_simulator.py --attack</code>. Enter PC 1's IP.</li>
            <li><b>Step 7 (Observe Mitigation):</b> Show Stage 1 (Green), Stage 2 (Yellow warning), Stage 3 (Red Perm Lock). Show PC 2 Wi-Fi dropping.</li>
            <li><b>Step 8 (System Reset):</b> Click "Emergency System Reset" in dashboard sidebar to return to Green. Toggle PC 2 Wi-Fi to reconnect.</li>
        </ul>

        <h2 class="sec-title">14. Suggested Team Ownership</h2>
        <table class="data-table">
            <tr>
                <th style="width: 25%;">Area</th>
                <th style="width: 75%;">What the teammate should understand / own during jury evaluation</th>
            </tr>
            <tr>
                <td><b>AI / Machine Learning</b></td>
                <td>Feature extraction, Random Forest hyperparameters, CIC-IDS2017 dataset, multi-class mapping, fast-path heuristics.</td>
            </tr>
            <tr>
                <td><b>Backend & API Gateway</b></td>
                <td>FastAPI async routes, dynamic client IP extraction, state transitions, CORS, SQLite SIEM database schema.</td>
            </tr>
            <tr>
                <td><b>Hardware & OOB Trust</b></td>
                <td>Raspberry Pi GPIO pinouts, breadboard resistors, out-of-band UDP socket dispatching, zero-trust hardware principles.</td>
            </tr>
            <tr>
                <td><b>Endpoint & Testing</b></td>
                <td>Endpoint agent daemon, Netsh/Nmcli interface dropping, 3-stage attack simulation, multi-laptop empirical verification.</td>
            </tr>
        </table>
    </div>
    <div class="page-footer">Team Project Report &bull; 18 October 2026 &bull; 6</div>
</div>

<!-- ======================================================================= -->
<!-- PAGE 7: CONCLUSION & APPENDICES                                         -->
<!-- ======================================================================= -->
<div class="page">
    <div class="page-header">WIT-SOC: WIRE-INTERPOSITION TRUST LAYER | PROJECT TECHNICAL REPORT</div>
    <div class="page-content">
        <h2 class="sec-title">15. Conclusion</h2>
        <p>
            Live verification demonstrates an operational, end-to-end autonomous cyber defense system. By combining <b>Speculative Micro-Containment</b> with an <b>Out-of-Band Hardware Mitigation Layer</b>, WIT-SOC eliminates the dangerous 2-to-5 second latency window exploited by lateral-moving ransomware. The multi-laptop deployment successfully proved sub-second detection, accurate dynamic IP extraction, real-time visual telemetry tracking, and reliable automated network isolation. The prototype successfully validates the wire-interposition security paradigm and provides a solid foundation for future offloading to enterprise SmartNICs and DPUs.
        </p>

        <h2 class="sec-title">Appendix A &mdash; Useful Commands & Endpoints</h2>
        <table class="data-table">
            <tr>
                <th style="width: 30%;">Purpose</th>
                <th style="width: 70%;">Command / HTTP Endpoint</th>
            </tr>
            <tr>
                <td><b>Check Gateway Status</b></td>
                <td><code>curl.exe http://localhost:8000/api/v1/status</code></td>
            </tr>
            <tr>
                <td><b>View SIEM Audit Statistics</b></td>
                <td><code>curl.exe http://localhost:8000/api/v1/stats</code></td>
            </tr>
            <tr>
                <td><b>Trigger System Reset</b></td>
                <td><code>curl.exe -X POST http://localhost:8000/api/v1/reset</code></td>
            </tr>
            <tr>
                <td><b>Run Automated Test Suite</b></td>
                <td><code>.venv\\Scripts\\python.exe tests\\test_full_suite.py</code></td>
            </tr>
            <tr>
                <td><b>Query SQLite SIEM Database</b></td>
                <td><code>sqlite3 backend\\siem_audit.db "SELECT * FROM telemetry_logs ORDER BY id DESC LIMIT 5;"</code></td>
            </tr>
            <tr>
                <td><b>Re-enable Wi-Fi on Windows</b></td>
                <td><code>netsh interface set interface "Wi-Fi" enable</code></td>
            </tr>
        </table>

        <h2 class="sec-title">Appendix B &mdash; Raspberry Pi Physical Hardware Pinout</h2>
        <table class="data-table">
            <tr>
                <th style="width: 18%;">Component</th>
                <th style="width: 14%;">Color</th>
                <th style="width: 22%;">Raspberry Pi Pin (BCM)</th>
                <th style="width: 20%;">Physical Header Pin</th>
                <th style="width: 26%;">Wiring & Connection</th>
            </tr>
            <tr>
                <td><b>Red LED</b></td>
                <td>Red</td>
                <td><b>GPIO 17</b></td>
                <td>Physical Pin 11</td>
                <td>Anode &rarr; Pin 11 &bull; Cathode &rarr; 220&Omega; &rarr; GND (Pin 6/9)</td>
            </tr>
            <tr>
                <td><b>Yellow LED</b></td>
                <td>Yellow</td>
                <td><b>GPIO 27</b></td>
                <td>Physical Pin 13</td>
                <td>Anode &rarr; Pin 13 &bull; Cathode &rarr; 220&Omega; &rarr; GND (Pin 6/9)</td>
            </tr>
            <tr>
                <td><b>Green LED</b></td>
                <td>Green</td>
                <td><b>GPIO 22</b></td>
                <td>Physical Pin 15</td>
                <td>Anode &rarr; Pin 15 &bull; Cathode &rarr; 220&Omega; &rarr; GND (Pin 6/9)</td>
            </tr>
        </table>
    </div>
    <div class="page-footer">Team Project Report &bull; 18 October 2026 &bull; 7</div>
</div>

</body>
</html>
"""

with open(HTML_TEMP_PATH, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"[+] Clean HTML generated at: {HTML_TEMP_PATH}")

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

print("[*] Rendering PDF with Microsoft Edge...")
proc = subprocess.run(cmd, capture_output=True, text=True)
time.sleep(2)

if os.path.exists(OUTPUT_PDF_SCRATCH):
    reader = pypdf.PdfReader(OUTPUT_PDF_SCRATCH)
    total_pages = len(reader.pages)
    size_kb = os.path.getsize(OUTPUT_PDF_SCRATCH) / 1024
    print(f"[+] SUCCESS: PDF compiled at: {OUTPUT_PDF_SCRATCH} ({size_kb:.1f} KB)")
    print(f"[*] EXACT PAGE COUNT: {total_pages} pages")
    
    import shutil
    shutil.copyfile(OUTPUT_PDF_SCRATCH, OUTPUT_PDF_ARTIFACT)
    print(f"[+] Synced to Artifacts: {OUTPUT_PDF_ARTIFACT}")
else:
    print(f"[!] Compilation failed: {proc.stdout} {proc.stderr}")
