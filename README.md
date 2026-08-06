# Edge SOC Hardware Mitigation Layer - LED Status Module

This module connects a Raspberry Pi hardware mitigation layer to the Edge SOC FastAPI backend. It polls the backend status endpoint every 0.5 seconds and lights up the corresponding LED (**GREEN**, **YELLOW**, or **RED**) based on the `"hardware_signal"` field.

---

## 1. FastAPI GET Route (`main.py`)

Add this endpoint to your FastAPI backend `main.py`:

```python
from fastapi import FastAPI
from typing import Dict, Any

app = FastAPI()

latest_status: Dict[str, Any] = {
    "hardware_signal": "GREEN",
    "system_health": "NORMAL"
}

@app.get("/status")
def get_latest_status():
    """Returns the latest status dictionary containing the hardware_signal."""
    return latest_status
```

---

## 2. Raspberry Pi Controller Script (`pi_hardware_led.py`)

Dependencies: `requests`, `gpiozero`

Install dependencies on Raspberry Pi:
```bash
pip install requests gpiozero
```

Running the script:
```bash
python pi_hardware_led.py
```

---

## 3. Breadboard & GPIO Wiring Setup

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

---

## 4. Git Branching & Submission Workflow

Follow these git commands to submit your feature branch without pushing directly to `main`:

```bash
# 1. Create and switch to your feature branch
git checkout -b hardware-led

# 2. Stage your changes
git add .

# 3. Commit your work with conventional commit message
git commit -m "feat: added hardware led mitigation module"

# 4. Push your branch to GitHub
git push origin hardware-led
```

After pushing, navigate to your GitHub repository and create a Pull Request (PR) from `hardware-led` into `main` for review by the Team Lead.
