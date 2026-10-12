@echo off
title WIT-SOC Endpoint Severing Agent
echo ========================================================
echo   Starting Endpoint Severing Daemon (Listening Port 9999)
echo   Awaiting Hardware Out-of-Band Network Kill Signal
echo ========================================================
if exist .venv\Scripts\python.exe (
    .venv\Scripts\python.exe endpoint\agent.py
) else (
    python endpoint\agent.py
)
pause
