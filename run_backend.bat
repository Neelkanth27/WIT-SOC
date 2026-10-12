@echo off
title WIT-SOC Central AI Gateway
echo ========================================================
echo   Starting WIT-SOC Central Gateway (FastAPI + AI Engine)
echo   Listening on 0.0.0.0:8000 (Available across LAN)
echo ========================================================
if exist .venv\Scripts\python.exe (
    .venv\Scripts\python.exe -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
) else (
    python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
)
pause
