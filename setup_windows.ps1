# AI Agents Integration Lab - Windows Setup Script
# Complete dependency installation for Windows PowerShell

Write-Host "🚀 AI Agents Integration Lab - Environment Setup" -ForegroundColor Green
Write-Host "=" * 50 -ForegroundColor Green

$ErrorActionPreference = "Stop"

try {
    # Check if Python is installed
    Write-Host "`n🔍 Checking Python installation..." -ForegroundColor Cyan
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
    } else {
        Write-Host "❌ Python not found! Please install Python 3.8+ first." -ForegroundColor Red
        exit 1
    }

    # Create virtual environment if it doesn't exist
    if (!(Test-Path "venv")) {
        Write-Host "`n📦 Creating virtual environment..." -ForegroundColor Cyan
        python -m venv venv
        Write-Host "✅ Virtual environment created!" -ForegroundColor Green
    } else {
        Write-Host "`n✅ Virtual environment already exists!" -ForegroundColor Green
    }

    # Activate virtual environment
    Write-Host "`n🔄 Activating virtual environment..." -ForegroundColor Cyan
    & ".\venv\Scripts\Activate.ps1"
    Write-Host "✅ Virtual environment activated!" -ForegroundColor Green

    # Upgrade pip
    Write-Host "`n🔄 Upgrading pip..." -ForegroundColor Cyan
    .\venv\Scripts\python.exe -m pip install --upgrade pip
    Write-Host "✅ Pip upgraded successfully!" -ForegroundColor Green

    # Install main dependencies
    Write-Host "`n📦 Installing main dependencies..." -ForegroundColor Cyan
    .\venv\Scripts\pip.exe install -r requirements.txt
    Write-Host "✅ Main dependencies installed!" -ForegroundColor Green

    # Install local-ai-service dependencies
    if (Test-Path "local-ai-service\requirements.txt") {
        Write-Host "`n📦 Installing local-ai-service dependencies..." -ForegroundColor Cyan
        .\venv\Scripts\pip.exe install -r "local-ai-service\requirements.txt"
        Write-Host "✅ Local-ai-service dependencies installed!" -ForegroundColor Green
    }

    # Install zero-cost-marketplace dependencies
    if (Test-Path "zero-cost-ai-marketplace\requirements.txt") {
        Write-Host "`n📦 Installing zero-cost-marketplace dependencies..." -ForegroundColor Cyan
        .\venv\Scripts\pip.exe install -r "zero-cost-ai-marketplace\requirements.txt"
        Write-Host "✅ Zero-cost-marketplace dependencies installed!" -ForegroundColor Green
    }

    # Test critical imports
    Write-Host "`n🧪 Testing critical imports..." -ForegroundColor Cyan
    .\venv\Scripts\python.exe -c "import fastapi, uvicorn, requests, pandas, numpy, httpx, pytest, psutil, structlog; print('✅ All critical imports successful!')"

    Write-Host "`n🎉 Environment setup completed successfully!" -ForegroundColor Green
    Write-Host "`n📋 Next steps:" -ForegroundColor Yellow
    Write-Host "   1. Environment is already activated in this session" -ForegroundColor White
    Write-Host "   2. Run tests: .\venv\Scripts\python.exe -m pytest" -ForegroundColor White
    Write-Host "   3. Start services: .\venv\Scripts\python.exe local-ai-service\start_api.py" -ForegroundColor White
    Write-Host "   4. For future sessions, activate with: .\venv\Scripts\Activate.ps1" -ForegroundColor White

} catch {
    Write-Host "`n❌ Setup failed with error: $_" -ForegroundColor Red
    Write-Host "Please check the error message above and try again." -ForegroundColor Red
    exit 1
}
