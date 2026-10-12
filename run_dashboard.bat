@echo off
title WIT-SOC Analyst Dashboard
echo ========================================================
echo   Starting WIT-SOC Live SOC Dashboard (Streamlit)
echo ========================================================
if exist .venv\Scripts\streamlit.exe (
    .venv\Scripts\streamlit.exe run dashboard\app.py
) else (
    streamlit run dashboard\app.py
)
pause
