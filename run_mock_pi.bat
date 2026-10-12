@echo off
title WIT-SOC Virtual Hardware Controller
echo ========================================================
echo   Starting Virtual Hardware Layer (Mock Pi Controller)
echo   Controls Virtual LEDs & Dispatches Out-of-Band UDP Kill
echo ========================================================
if exist .venv\Scripts\python.exe (
    .venv\Scripts\python.exe hardware\mock_pi_controller.py
) else (
    python hardware\mock_pi_controller.py
)
pause
