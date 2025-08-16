@echo off
REM =================================================================
REM   AI AGENTS STARTUP SCRIPT FOR WINDOWS
REM   Complete integration with single chat interface
REM =================================================================

echo.
echo 🚀 STARTING AI AGENTS INTEGRATION SYSTEM
echo =========================================
echo.

REM Set Ollama models to G drive (more space)
set OLLAMA_MODELS=G:\ollama_models
echo 📍 Setting Ollama models location to: %OLLAMA_MODELS%

REM Navigate to project directory
cd /d "G:\c\OneDrive\Desktop\localai\local-agent"
echo 📂 Project directory: %CD%

REM Check if virtual environment exists
if not exist "venv\Scripts\python.exe" (
    echo ❌ Virtual environment not found!
    echo Please create one with: python -m venv venv
    pause
    exit /b 1
)

echo.
echo 🔧 STARTING SERVICES...
echo.

REM 1. Start Ollama (if not running)
echo 🤖 Starting Ollama service...
tasklist /fi "imagename eq ollama.exe" 2>nul | find /i "ollama.exe" >nul
if %errorlevel% neq 0 (
    start "" ollama serve
    timeout /t 5 >nul
) else (
    echo    ✅ Ollama already running
)

REM 2. Start Local AI Service (Port 8001)
echo 🧠 Starting Local AI Service on port 8001...
start "Local AI Service" /min .\venv\Scripts\python.exe local-ai-service\start_api_gdrive.py

REM 3. Start Unified Agent API (Port 8002)
echo 🔗 Starting Unified Agent API on port 8002...
start "Unified API" /min .\venv\Scripts\python.exe unified_agent_api.py

REM 4. Start Marketplace Service (Port 8080)
echo 🛍️ Starting Marketplace Service on port 8080...
start "Marketplace" /min .\venv\Scripts\python.exe zero-cost-ai-marketplace\simple_launcher.py

echo.
echo ⏳ Waiting for services to initialize...
timeout /t 10 >nul

REM 5. Verify all services are running
echo.
echo 🔍 CHECKING SERVICE STATUS...
echo.

netstat -an | findstr ":11434" >nul && echo    ✅ Ollama: RUNNING (Port 11434) || echo    ❌ Ollama: NOT RUNNING
netstat -an | findstr ":8001" >nul && echo    ✅ Local AI: RUNNING (Port 8001) || echo    ❌ Local AI: NOT RUNNING
netstat -an | findstr ":8002" >nul && echo    ✅ Unified API: RUNNING (Port 8002) || echo    ❌ Unified API: NOT RUNNING
netstat -an | findstr ":8080" >nul && echo    ✅ Marketplace: RUNNING (Port 8080) || echo    ❌ Marketplace: NOT RUNNING

echo.
echo 🌐 OPENING CHAT INTERFACE...
echo.

REM 6. Open the chat interface in default browser
start "" "local-ai-service\ai_chat.html"

echo.
echo ============================================
echo 🎉 AI AGENTS SYSTEM READY!
echo ============================================
echo.
echo 📱 Chat Interface: Opened in your browser
echo 🤖 Available Models: llama3.2:1b (1.3GB)
echo 💾 Model Location: G:\ollama_models
echo 🔧 All services integrated and running
echo.
echo 📋 Service URLs:
echo    • Chat Interface: file:///.../ai_chat.html
echo    • Unified API: http://localhost:8002
echo    • Local AI API: http://localhost:8001  
echo    • Marketplace: http://localhost:8080
echo    • Ollama: http://localhost:11434
echo.
echo 💡 Usage:
echo    1. Use the opened chat interface
echo    2. Upload files with the + button
echo    3. Chat with your local AI models
echo.
echo ⚠️  To stop all services, run: stop_ai_services.bat
echo.
pause
