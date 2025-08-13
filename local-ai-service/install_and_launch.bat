@echo off
echo 🚀 ZERO-COST AI MARKETPLACE - WINDOWS INSTALLER
echo ================================================
echo.

echo 📦 Installing Python requirements...
pip install fastapi uvicorn requests pydantic asyncio

echo.
echo 🧠 Checking AI models...
ollama list

echo.
echo 🚀 Launching marketplace...
python launch_marketplace.py

echo.
echo ✅ Installation complete!
echo 🌐 Open http://localhost:8000 in your browser
pause
