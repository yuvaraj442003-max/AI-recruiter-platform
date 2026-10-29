# run_backend.ps1 - Automated Startup for Redis & FastAPI Backend Server
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  AI RECRUITER - BACKEND SERVER STARTUP   " -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# 1. Check if PostgreSQL server port 5432 is open
$pgActive = Test-NetConnection -ComputerName "127.0.0.1" -Port 5432 -InformationLevel Quiet

if (-not $pgActive) {
    Write-Host "[+] PostgreSQL is not running on port 5432. Starting PostgreSQL server..." -ForegroundColor Yellow
    # Attempt service start first
    $svcResult = Start-Process -FilePath "net.exe" -ArgumentList "start postgresql-x64-17" -Wait -PassThru -WindowStyle Hidden -ErrorAction SilentlyContinue
    
    # If service start failed (e.g. non-admin shell), start via pg_ctl directly
    $pgActive = Test-NetConnection -ComputerName "127.0.0.1" -Port 5432 -InformationLevel Quiet
    if (-not $pgActive) {
        $pgDataPaths = @(
            "C:\Program Files\PostgreSQL\17\data",
            "C:\Program Files\PostgreSQL\16\data",
            "C:\Program Files\PostgreSQL\18\data"
        )
        foreach ($dp in $pgDataPaths) {
            $binPath = (Split-Path (Split-Path $dp -Parent) -Parent) + "\bin\pg_ctl.exe"
            if ((Test-Path $dp) -and (Test-Path $binPath)) {
                Start-Process -FilePath $binPath -ArgumentList "start -D `"$dp`" -w" -WindowStyle Hidden
                Start-Sleep -Seconds 2
                break
            }
        }
    }

    $pgActiveNow = Test-NetConnection -ComputerName "127.0.0.1" -Port 5432 -InformationLevel Quiet
    if ($pgActiveNow) {
        Write-Host "[+] PostgreSQL Primary Database started successfully on port 5432!" -ForegroundColor Green
    } else {
        Write-Host "[!] Error: PostgreSQL failed to start on port 5432. Please ensure PostgreSQL 17 is running." -ForegroundColor Red
        Exit 1
    }
} else {
    Write-Host "[+] PostgreSQL Primary Database is already running on port 5432." -ForegroundColor Green
}

# 2. Check if Redis server port 6379 is open
$redisActive = Test-NetConnection -ComputerName "127.0.0.1" -Port 6379 -InformationLevel Quiet

if (-not $redisActive) {
    Write-Host "[+] Live Redis is not running on port 6379. Launching redis-server..." -ForegroundColor Yellow
    Start-Process -FilePath "redis-server" -WindowStyle Hidden
    Start-Sleep -Seconds 1
    Write-Host "[+] Live Redis Server started successfully in background!" -ForegroundColor Green
} else {
    Write-Host "[+] Live Redis Server is already running on port 6379." -ForegroundColor Green
}

# 3. Launch Uvicorn FastAPI Server
Write-Host "[+] Launching Uvicorn FastAPI application..." -ForegroundColor Cyan
Write-Host "------------------------------------------" -ForegroundColor Gray

& ".\venv\Scripts\python.exe" -m uvicorn app.main:app --reload
