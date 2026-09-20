@echo off
title Google Photos Case Study App
echo ===================================================
echo Starting Google Photos Review Pulse & RAG Assistant
echo ===================================================
echo Backend: Python RAG Engine + Pure Vector Search
echo Frontend: Streamlit Material Design 3 Web App
echo URL: http://localhost:8501
echo ===================================================

if exist "C:\Python314\python.exe" (
    "C:\Python314\python.exe" -m streamlit run app.py --server.port 8501
) else (
    python -m streamlit run app.py --server.port 8501
)
pause
