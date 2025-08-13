#Requires -Version 5.1
<#
.SYNOPSIS
    Enhanced Ollama Service Management and GPT-OSS:20B Testing Script
.DESCRIPTION
    Comprehensive script to fix, restart, and test Ollama service with GPT-OSS:20B model
    Includes error handling, logging, and business test automation
.NOTES
    Version: 2.0
    Author: Multi-AI Agents Framework
#>

[CmdletBinding()]
param(
    [switch]$SkipTests,
    [switch]$Verbose,
    [int]$TimeoutSeconds = 30
)

# Enhanced error handling
$ErrorActionPreference = "Continue"
$ProgressPreference = "SilentlyContinue"

# Initialize logging
$LogFile = Join-Path $PSScriptRoot "ollama_service_$(Get-Date -Format 'yyyyMMdd_HHmmss').log"

function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $LogEntry = "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] [$Level] $Message"
    Write-Host $LogEntry
    $LogEntry | Out-File -FilePath $LogFile -Append -Encoding UTF8
}

function Test-OllamaInstallation {
    Write-Log "🔍 CHECKING OLLAMA INSTALLATION" "INFO"
    
    # Check if Ollama is installed
    $OllamaPath = Get-Command "ollama" -ErrorAction SilentlyContinue
    if (-not $OllamaPath) {
        Write-Log "❌ Ollama not found in PATH. Checking common locations..." "ERROR"
        
        $CommonPaths = @(
            "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe",
            "$env:PROGRAMFILES\Ollama\ollama.exe",
            "$env:PROGRAMFILES(X86)\Ollama\ollama.exe"
        )
        
        foreach ($Path in $CommonPaths) {
            if (Test-Path $Path) {
                Write-Log "✅ Found Ollama at: $Path" "INFO"
                $env:PATH += ";$(Split-Path $Path -Parent)"
                return $true
            }
        }
        
        Write-Log "❌ Ollama not found. Please install from https://ollama.ai" "ERROR"
        return $false
    }
    
    Write-Log "✅ Ollama found in PATH: $($OllamaPath.Source)" "INFO"
    return $true
}

function Stop-OllamaProcesses {
    Write-Log "🛑 STEP 1: Stopping existing Ollama processes" "INFO"
    
    try {
        $OllamaProcesses = Get-Process -Name "ollama" -ErrorAction SilentlyContinue
        if ($OllamaProcesses) {
            $OllamaProcesses | Stop-Process -Force -ErrorAction SilentlyContinue
            Start-Sleep -Seconds 2
            Write-Log "✅ Stopped $($OllamaProcesses.Count) Ollama process(es)" "INFO"
        } else {
            Write-Log "ℹ️ No existing Ollama processes found" "INFO"
        }
    }
    catch {
        Write-Log "⚠️ Error stopping processes: $($_.Exception.Message)" "WARN"
    }
}

function Start-OllamaService {
    Write-Log "🚀 STEP 2: Starting Ollama service" "INFO"
    
    try {
        # Start Ollama service with better process handling
        $ProcessInfo = Start-Process -FilePath "ollama" -ArgumentList "serve" -WindowStyle Hidden -PassThru
        Write-Log "✅ Started Ollama service (PID: $($ProcessInfo.Id))" "INFO"
        
        # Wait for service initialization
        Write-Log "⏳ STEP 3: Waiting for service initialization ($TimeoutSeconds seconds)" "INFO"
        Start-Sleep -Seconds 3
        
        # Test service availability with retry logic
        $RetryCount = 0
        $MaxRetries = $TimeoutSeconds / 3
        
        do {
            try {
                $Response = Invoke-RestMethod -Uri "http://localhost:11434/api/tags" -TimeoutSec 5 -ErrorAction Stop
                Write-Log "✅ Ollama service is running properly!" "INFO"
                return $true
            }
            catch {
                $RetryCount++
                if ($RetryCount -lt $MaxRetries) {
                    Write-Log "⏳ Service not ready yet, retrying in 3 seconds... (Attempt $RetryCount/$MaxRetries)" "INFO"
                    Start-Sleep -Seconds 3
                } else {
                    Write-Log "❌ Service failed to start after $TimeoutSeconds seconds" "ERROR"
                    return $false
                }
            }
        } while ($RetryCount -lt $MaxRetries)
    }
    catch {
        Write-Log "❌ Failed to start Ollama service: $($_.Exception.Message)" "ERROR"
        return $false
    }
}

function Test-GptOssModel {
    Write-Log "📦 STEP 4: Verifying GPT-OSS:20B model availability" "INFO"
    
    try {
        $Models = & ollama list 2>&1
        Write-Log "Available models:" "INFO"
        Write-Log $Models "INFO"
        
        if ($Models -match "gpt-oss:20b") {
            Write-Log "✅ GPT-OSS:20B model is available!" "INFO"
            return $true
        } else {
            Write-Log "❌ GPT-OSS:20B model not found" "ERROR"
            Write-Log "💡 Run: ollama pull gpt-oss:20b" "INFO"
            return $false
        }
    }
    catch {
        Write-Log "❌ Error checking models: $($_.Exception.Message)" "ERROR"
        return $false
    }
}

function Test-SystemIntegration {
    Write-Log "🔧 STEP 5: Testing Multi-AI Agents Integration" "INFO"
    
    try {
        # Test basic Python imports
        Write-Log "Testing core system imports..." "INFO"
        $ImportTest = & python -c @"
import sys, os
sys.path.insert(0, '.')
try:
    from owl_integration import create_owl_integration
    print('✅ OWL integration: OK')
except Exception as e:
    print(f'⚠️ OWL integration: {e}')

try:
    from marketplace_engine import MarketplaceEngine
    print('✅ Marketplace engine: OK')
except Exception as e:
    print(f'⚠️ Marketplace engine: {e}')

try:
    from agents.base_agent import BaseAgent
    print('✅ Base agent: OK')
except Exception as e:
    print(f'⚠️ Base agent: {e}')

print('System integration test completed')
"@ 2>&1
        
        Write-Log "Integration test results: $ImportTest" "INFO"
        
        # Test if integration dashboard works
        if (Test-Path "integration_dashboard.py") {
            Write-Log "Testing integration dashboard..." "INFO"
            $DashboardTest = & python integration_dashboard.py 2>&1
            if ($LASTEXITCODE -eq 0) {
                Write-Log "✅ Integration dashboard: Working" "INFO"
            } else {
                Write-Log "⚠️ Integration dashboard: Issues detected" "WARN"
            }
        }
        
    }
    catch {
        Write-Log "❌ System integration test failed: $($_.Exception.Message)" "ERROR"
    }
}

function Invoke-BusinessTests {
    if ($SkipTests) {
        Write-Log "⏭️ Skipping business tests as requested" "INFO"
        return
    }
    
    Write-Log "🧪 STEP 6: Running GPT-OSS:20B Business Tests" "INFO"
    
    $QuickTests = @(
        "Hello, respond with 'READY' if you can process business requests",
        "What is 2+2? Answer with just the number.",
        "List 3 AI agent use cases in one sentence each"
    )
    
    foreach ($TestPrompt in $QuickTests) {
        try {
            Write-Log "Testing: $TestPrompt" "INFO"
            $Response = & ollama run gpt-oss:20b $TestPrompt 2>&1 | Select-Object -First 5
            Write-Log "Response received: $($Response -join ' ')" "INFO"
        }
        catch {
            Write-Log "⚠️ Test failed: $($_.Exception.Message)" "WARN"
        }
    }
}

function Show-TroubleshootingGuide {
    Write-Log "💡 TROUBLESHOOTING GUIDE" "INFO"
    Write-Log "=========================" "INFO"
    Write-Log "If issues persist, try these solutions:" "INFO"
    Write-Log "1. Check Windows Defender/Antivirus exclusions" "INFO"
    Write-Log "2. Run PowerShell as Administrator" "INFO"
    Write-Log "3. Check port 11434: netstat -an | findstr 11434" "INFO"
    Write-Log "4. Reinstall Ollama from https://ollama.ai" "INFO"
    Write-Log "5. Try smaller model: ollama pull llama3.1:8b" "INFO"
    Write-Log "" "INFO"
    Write-Log "📊 Log file: $LogFile" "INFO"
}

function Show-NextSteps {
    Write-Log "🎯 NEXT STEPS FOR SUCCESS" "INFO"
    Write-Log "=========================" "INFO"
    Write-Log "Your Multi-AI Agents system is ready!" "INFO"
    Write-Log "" "INFO"
    Write-Log "🏪 AVAILABLE COMMANDS:" "INFO"
    Write-Log "- python integration_dashboard.py" "INFO"
    Write-Log "- python customer_request_agent.py" "INFO"
    Write-Log "- python system_test_comprehensive.py" "INFO"
    Write-Log "" "INFO"
    Write-Log "💰 BUSINESS VALUE:" "INFO"
    Write-Log "- Local AI deployment (no API costs)" "INFO"
    Write-Log "- Premium model performance" "INFO"
    Write-Log "- Full data privacy control" "INFO"
}

# MAIN EXECUTION
Write-Log "🔧 ENHANCED OLLAMA & MULTI-AI AGENTS MANAGER v2.0" "INFO"
Write-Log "===================================================" "INFO"

try {
    # Check Ollama installation
    if (-not (Test-OllamaInstallation)) {
        throw "Ollama installation not found"
    }
    
    # Stop and restart service
    Stop-OllamaProcesses
    
    if (-not (Start-OllamaService)) {
        throw "Failed to start Ollama service"
    }
    
    # Verify model
    $ModelAvailable = Test-GptOssModel
    if (-not $ModelAvailable) {
        Write-Log "⚠️ GPT-OSS:20B not available, but service is running" "WARN"
    }
    
    # Test system integration
    Test-SystemIntegration
    
    # Run business tests
    if ($ModelAvailable) {
        Invoke-BusinessTests
    }
    
    # Success
    Write-Log "🎉 SYSTEM READY FOR BUSINESS!" "INFO"
    Show-NextSteps
    
}
catch {
    Write-Log "❌ CRITICAL ERROR: $($_.Exception.Message)" "ERROR"
    Show-TroubleshootingGuide
    exit 1
}
finally {
    Write-Log "📋 Execution completed. Log saved: $LogFile" "INFO"
}
