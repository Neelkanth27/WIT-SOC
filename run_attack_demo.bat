@echo off
title WIT-SOC Attack Simulation Demo
echo ========================================================
echo   Launching Simulated Multi-Stage Cyber Attack Pipeline
echo ========================================================
if exist .venv\Scripts\python.exe (
    .venv\Scripts\python.exe endpoint\setup.py
) else (
    python endpoint\setup.py
)
pause
