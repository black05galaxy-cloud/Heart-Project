# Heart Collaborative - Install packages and run app on localhost
# Run in PowerShell: .\run.ps1   (or: powershell -ExecutionPolicy Bypass -File run.ps1)

Set-Location $PSScriptRoot

Write-Host ""
Write-Host "  Heart Collaborative - Installing packages and starting app" -ForegroundColor Cyan
Write-Host "  --------------------------------------------------------" -ForegroundColor Cyan
Write-Host ""

Write-Host "Step 1: Installing required packages..." -ForegroundColor Yellow
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: pip install failed. Make sure Python and pip are installed." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Step 2: Starting Streamlit app..." -ForegroundColor Yellow
Write-Host "  App will open at:  http://localhost:8501" -ForegroundColor Green
Write-Host "  Press Ctrl+C to stop the server." -ForegroundColor Gray
Write-Host ""

# Open browser after a short delay (in background)
Start-Job -ScriptBlock {
    Start-Sleep -Seconds 5
    Start-Process "http://localhost:8501"
} | Out-Null

streamlit run app.py
