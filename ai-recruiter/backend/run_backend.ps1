# run_backend.ps1 - Automated Startup for Redis & FastAPI Backend Server
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  AI RECRUITER - BACKEND SERVER STARTUP   " -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# 1. Check if Redis server port 6379 is open
$redisActive = Test-NetConnection -ComputerName "127.0.0.1" -Port 6379 -InformationLevel Quiet

if (-not $redisActive) {
    Write-Host "[+] Live Redis is not running on port 6379. Launching redis-server..." -ForegroundColor Yellow
    Start-Process -FilePath "redis-server" -WindowStyle Hidden
    Start-Sleep -Seconds 1
    Write-Host "[+] Live Redis Server started successfully in background!" -ForegroundColor Green
} else {
    Write-Host "[+] Live Redis Server is already running on port 6379." -ForegroundColor Green
}

# 2. Launch Uvicorn FastAPI Server
Write-Host "[+] Launching Uvicorn FastAPI application..." -ForegroundColor Cyan
Write-Host "------------------------------------------" -ForegroundColor Gray

& ".\venv\Scripts\python.exe" -m uvicorn app.main:app --reload
