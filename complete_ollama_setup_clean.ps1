# COMPLETE OLLAMA + GPT-OSS SETUP GUIDE
# Execute these steps to get everything working

Write-Host "COMPLETE OLLAMA SETUP FOR AI AGENT MARKETPLACE" -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Green
Write-Host ""

Write-Host "CURRENT STATUS CHECK" -ForegroundColor Cyan
Write-Host "====================" -ForegroundColor Cyan
Write-Host ""

# Check if Ollama is installed
$ollamaPath = Get-Command ollama -ErrorAction SilentlyContinue
if ($ollamaPath) {
    Write-Host "Ollama is installed at: $($ollamaPath.Source)" -ForegroundColor Green
} else {
    Write-Host "Ollama is NOT installed" -ForegroundColor Red
    Write-Host ""
    Write-Host "INSTALL OLLAMA:" -ForegroundColor Yellow
    Write-Host "1. Go to https://ollama.ai"
    Write-Host "2. Download Ollama for Windows"
    Write-Host "3. Run the installer"
    Write-Host "4. Restart PowerShell after installation"
    Write-Host ""
    Write-Host "STOP HERE and install Ollama first!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "CHECKING OLLAMA SERVICE" -ForegroundColor Cyan
Write-Host "=======================" -ForegroundColor Cyan

# Check if Ollama service is running
try {
    Invoke-WebRequest -Uri "http://localhost:11434/api/tags" -TimeoutSec 5 -ErrorAction Stop | Out-Null
    Write-Host "Ollama service is running!" -ForegroundColor Green
} catch {
    Write-Host "Ollama service is not running" -ForegroundColor Red
    Write-Host "Starting Ollama service..." -ForegroundColor Yellow
    
    # Kill any existing processes
    Get-Process -Name "ollama" -ErrorAction SilentlyContinue | Stop-Process -Force
    
    # Start Ollama service
    Start-Process -FilePath "ollama" -ArgumentList "serve" -WindowStyle Hidden
    
    Write-Host "Waiting 20 seconds for service to start..." -ForegroundColor Yellow
    Start-Sleep -Seconds 20
    
    # Check again
    try {
        Invoke-WebRequest -Uri "http://localhost:11434/api/tags" -TimeoutSec 5 -ErrorAction Stop | Out-Null
        Write-Host "Ollama service started successfully!" -ForegroundColor Green
    } catch {
        Write-Host "Failed to start Ollama service" -ForegroundColor Red
        Write-Host "Try restarting your computer and running this script again" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "CHECKING GPT-OSS:20B MODEL" -ForegroundColor Cyan
Write-Host "===========================" -ForegroundColor Cyan

# List available models
try {
    $models = & ollama list 2>$null
    Write-Host "Available models:"
    Write-Host $models
} catch {
    Write-Host "Error listing models: $_" -ForegroundColor Red
    $models = ""
}

if ($models -match "gpt-oss:20b") {
    Write-Host "GPT-OSS:20B model is available!" -ForegroundColor Green
} else {
    Write-Host "GPT-OSS:20B model not found" -ForegroundColor Red
    Write-Host ""
    Write-Host "DOWNLOADING GPT-OSS:20B MODEL" -ForegroundColor Yellow
    Write-Host "=============================" -ForegroundColor Yellow
    Write-Host "This is a large download (~12GB). Ensure you have:"
    Write-Host "   • Good internet connection"
    Write-Host "   • At least 15GB free disk space"
    Write-Host "   • 30+ minutes for download"
    Write-Host ""
    
    $confirm = Read-Host "Do you want to download GPT-OSS:20B now? (y/N)"
    if ($confirm -eq "y" -or $confirm -eq "Y") {
        Write-Host "Starting download..." -ForegroundColor Green
        try {
            & ollama pull gpt-oss:20b
            Write-Host "Download complete!" -ForegroundColor Green
        } catch {
            Write-Host "Download failed: $_" -ForegroundColor Red
            Write-Host "Check your internet connection and try again" -ForegroundColor Yellow
            exit 1
        }
    } else {
        Write-Host "Cannot proceed without the model" -ForegroundColor Red
        Write-Host "Run 'ollama pull gpt-oss:20b' when ready to download" -ForegroundColor Yellow
        exit 1
    }
}

Write-Host ""
Write-Host "QUICK FUNCTIONALITY TEST" -ForegroundColor Cyan
Write-Host "========================" -ForegroundColor Cyan

Write-Host "Testing with simple prompt..." -ForegroundColor Yellow
try {
    $testResult = & ollama run gpt-oss:20b "Say hello and confirm you're working properly." 2>$null
    if ($testResult) {
        Write-Host "GPT-OSS:20B is responding!" -ForegroundColor Green
        Write-Host "Response preview:"
        Write-Host ($testResult | Select-Object -First 3) -ForegroundColor Gray
    } else {
        Write-Host "GPT-OSS:20B is not responding properly" -ForegroundColor Red
    }
} catch {
    Write-Host "Error testing GPT-OSS:20B: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "READY FOR BUSINESS TESTS!" -ForegroundColor Green
Write-Host "=========================" -ForegroundColor Green
Write-Host "Now you can run our AI Agent Marketplace tests:"
Write-Host ""
Write-Host "TEST 1: AI Agent Creation" -ForegroundColor Yellow
Write-Host 'ollama run gpt-oss:20b "Create a Python class for a WhatsApp Business Agent that can send automated follow-up messages to customers. Include proper error handling and rate limiting."'
Write-Host ""
Write-Host "TEST 2: Business Strategy Analysis" -ForegroundColor Yellow
Write-Host 'ollama run gpt-oss:20b "Analyze the AI agent marketplace opportunity. What are the top 5 most profitable agent types for small businesses in 2025?"'
Write-Host ""
Write-Host "TEST 3: Code Integration" -ForegroundColor Yellow
Write-Host 'ollama run gpt-oss:20b "Write a FastAPI endpoint that integrates with our Ollama GPT-OSS model to power AI agents in our marketplace. Include proper error handling and response streaming."'
Write-Host ""
Write-Host "TEST 4: Sales Copy Generation" -ForegroundColor Yellow
Write-Host 'ollama run gpt-oss:20b "Write a compelling landing page headline and 3 bullet points for an AI Agent Marketplace that helps businesses automate WhatsApp, social media, and sales processes."'
Write-Host ""
Write-Host "TEST 5: Technical Architecture" -ForegroundColor Yellow
Write-Host 'ollama run gpt-oss:20b "Design the architecture for integrating local Ollama models into our existing OWL-based AI agent system. Consider scalability, performance, and reliability."'
Write-Host ""
Write-Host "COPY AND PASTE EACH COMMAND ABOVE TO TEST!" -ForegroundColor Cyan
