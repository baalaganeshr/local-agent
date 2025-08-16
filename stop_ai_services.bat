@echo off
REM =================================================================
REM   STOP AI AGENTS SERVICES - WINDOWS
REM   Cleanly shutdown all AI services
REM =================================================================

echo.
echo 🛑 STOPPING AI AGENTS SERVICES
echo ===============================
echo.

echo 🔄 Stopping Python processes...
taskkill /f /im python.exe 2>nul
if %errorlevel% equ 0 (
    echo    ✅ Python processes stopped
) else (
    echo    ℹ️  No Python processes found
)

echo 🔄 Stopping Ollama service...
taskkill /f /im ollama.exe 2>nul
if %errorlevel% equ 0 (
    echo    ✅ Ollama service stopped
) else (
    echo    ℹ️  Ollama not running
)

echo.
echo 🔍 Checking if ports are freed...
timeout /t 2 >nul

netstat -an | findstr ":8001 :8002 :8080" >nul
if %errorlevel% neq 0 (
    echo    ✅ All ports are now free
) else (
    echo    ⚠️  Some ports may still be in use
)

echo.
echo ✅ All AI services have been stopped.
echo.
pause
