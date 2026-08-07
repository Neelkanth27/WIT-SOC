# Edge SOC Hardware Mitigation Layer - LED Status Module

This module connects a Raspberry Pi hardware mitigation layer to the Edge SOC backend. It securely connects to the backend IP address and polls the `/api/v1/status` endpoint every 0.5 seconds to light up the corresponding physical LED (**GREEN**, **YELLOW**, or **RED**).

---

## 1. Dependencies & Run Instructions

### Dependencies
- `requests`
- `gpiozero`

Install dependencies on the Raspberry Pi:
```bash
pip install requests gpiozero
```

### Running the Controller
Ensure your Raspberry Pi is connected to the same network as the Edge SOC server (hotspot or Ethernet).

Run the production hardware script:
```bash
python pi_hardware_led.py
```

*(Optional: For testing on a PC without physical Pi hardware, run `python mock_pi_controller.py`)*

---

## 2. Breadboard & GPIO Wiring Setup

### Pinout Mapping Table

| Component | Color | Raspberry Pi Pin (BCM GPIO) | Physical Pin # | Resistor Value | Ground Connection |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Red LED** | Red | **GPIO 17** | Pin 11 | 220Ω – 330Ω | GND (Pin 6 or Pin 9) |
| **Yellow LED** | Yellow | **GPIO 27** | Pin 13 | 220Ω – 330Ω | GND (Pin 6 or Pin 9) |
| **Green LED** | Green | **GPIO 22** | Pin 15 | 220Ω – 330Ω | GND (Pin 6 or Pin 9) |

### Step-by-Step Wiring Guide

1. **Common Ground (GND)**:
   - Connect a jumper wire from **Physical Pin 6 (GND)** or **Physical Pin 9 (GND)** on the Raspberry Pi header to the **Negative (-) power rail** on your breadboard.

2. **Green LED Connection**:
   - Place the Green LED on the breadboard.
   - Connect the **Anode** (longer leg (+)) to **GPIO 22 (Physical Pin 15)** via a jumper wire.
   - Connect the **Cathode** (shorter leg (-)) to a **220Ω resistor**, and connect the other side of the resistor to the **GND rail**.

3. **Yellow LED Connection**:
   - Place the Yellow LED on the breadboard.
   - Connect the **Anode** (longer leg (+)) to **GPIO 27 (Physical Pin 13)** via a jumper wire.
   - Connect the **Cathode** (shorter leg (-)) to a **220Ω resistor**, and connect the other side of the resistor to the **GND rail**.

4. **Red LED Connection**:
   - Place the Red LED on the breadboard.
   - Connect the **Anode** (longer leg (+)) to **GPIO 17 (Physical Pin 11)** via a jumper wire.
   - Connect the **Cathode** (shorter leg (-)) to a **220Ω resistor**, and connect the other side of the resistor to the **GND rail**.
