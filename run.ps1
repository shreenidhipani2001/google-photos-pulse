# Google Photos App PowerShell Launcher
Write-Host "===================================================" -ForegroundColor Cyan
Write-Host " Starting Google Photos Review Pulse & RAG Engine  " -ForegroundColor Cyan
Write-Host "===================================================" -ForegroundColor Cyan
Write-Host "Backend: Python RAG Engine + Pure Vector Search"
Write-Host "Frontend: Streamlit Material Design 3 Web App"
Write-Host "Access URL: http://localhost:8501" -ForegroundColor Green
Write-Host "==================================================="

$pythonPath = "C:\Python314\python.exe"
if (Test-Path $pythonPath) {
    & $pythonPath -m streamlit run app.py --server.port 8501
} else {
    python -m streamlit run app.py --server.port 8501
}
