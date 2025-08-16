@echo off
echo Starting AI Chat System...
echo.

echo 1. Starting API Server...
cd /d "G:\c\OneDrive\Desktop\localai\local-agent\local-ai-service"
start /min cmd /c "python simple_chat_api.py"

echo 2. Waiting for server to start...
timeout /t 3 /nobreak > nul

echo 3. Opening Chat Interface...
start "" "G:\c\OneDrive\Desktop\localai\local-agent\local-ai-service\ai_chat.html"

echo.
echo ✅ AI Chat System Started!
echo 📱 Your chat interface is now open
echo 💬 Start typing to chat with AI
echo.
echo Press any key to exit this launcher...
pause > nul
