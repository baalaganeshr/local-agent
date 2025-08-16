# AI AGENTS INTEGRATION - COMPLETE SETUP GUIDE FOR WINDOWS
# =========================================================

## 🎯 SYSTEM STATUS: FULLY INTEGRATED ✅

Your AI agents system is now completely integrated with a single chat interface (`ai_chat.html`). All services are running and communicating properly.

## 📋 WHAT'S RUNNING:

### Core Services:
- ✅ **Ollama**: Port 11434 (Local AI models)
- ✅ **Local AI API**: Port 8001 (Business API) 
- ✅ **Unified Agent API**: Port 8002 (All agents integrated)
- ✅ **Marketplace**: Port 8080 (Service marketplace)

### Available Models:
- 🤖 **llama3.2:1b** (1.3GB) - Fast and efficient
- 📍 **Storage**: G:\ollama_models (plenty of space)

## 🚀 WINDOWS COMMANDS TO USE:

### 1. START ALL SERVICES (Single Command):
```batch
# Navigate to project directory
cd "G:\c\OneDrive\Desktop\localai\local-agent"

# Run the startup script
start_ai_services.bat
```

### 2. STOP ALL SERVICES:
```batch
stop_ai_services.bat
```

### 3. OPEN CHAT INTERFACE:
```batch
start "local-ai-service\ai_chat.html"
```

### 4. CHECK SERVICE STATUS:
```batch
netstat -an | findstr "8001 8002 8080 11434"
```

### 5. TEST API DIRECTLY:
```powershell
# Test unified API
Invoke-RestMethod -Uri "http://localhost:8002/health" -Method GET

# Test chat functionality
$body = @{ message = "Hello AI!" } | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8002/agents/customer_request_json" -Method POST -ContentType "application/json" -Body $body
```

### 6. ADD MORE MODELS:
```batch
# Check available models
ollama list

# Pull a larger model (optional)
ollama pull llama3.2:3b

# Pull a code-specialized model
ollama pull codellama:7b-code
```

### 7. CHECK INTEGRATION STATUS:
```batch
cd "G:\c\OneDrive\Desktop\localai\local-agent"
.\venv\Scripts\python.exe integration_checker.py
```

## 🎯 HOW TO USE:

### Chat Interface Features:
1. **Open**: `ai_chat.html` in your browser
2. **Chat**: Type messages and get AI responses
3. **Files**: Use the "+" button to upload documents, images, code
4. **History**: All conversations saved automatically
5. **Export**: Download chat history as JSON

### Supported File Types:
- 📁 **Documents**: PDF, DOC, DOCX, TXT, MD
- 🖼️ **Images**: PNG, JPG, GIF, SVG  
- 💻 **Code**: PY, JS, TS, HTML, CSS, JSON
- 📊 **Data**: CSV, XLSX
- 🎤 **Presentations**: PPT, PPTX

## 🔧 SYSTEM ARCHITECTURE:

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   ai_chat.html  │────│  Unified API     │────│     Ollama      │
│   (Your UI)     │    │  (Port 8002)     │    │  (Port 11434)   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ├── Customer Request Agent
                              ├── Marketplace Engine  
                              └── File Processing
```

## 💡 TROUBLESHOOTING:

### If services won't start:
```batch
# Kill any stuck processes
taskkill /f /im python.exe
taskkill /f /im ollama.exe

# Check for port conflicts
netstat -an | findstr "8001 8002 8080"

# Restart services
start_ai_services.bat
```

### If chat interface won't connect:
1. Check if `http://localhost:8002/health` responds
2. Make sure all services are running
3. Try refreshing the browser

### If models are missing:
```batch
# Check model location
echo %OLLAMA_MODELS%

# Should show: G:\ollama_models

# List available models
ollama list
```

## 🎉 READY TO USE!

Your system is now fully integrated and ready for production use:

- **Single Interface**: All AI capabilities through `ai_chat.html`
- **Local Processing**: All data stays on your machine
- **File Support**: Upload and analyze any file type
- **Multi-Model**: Easy to add more models as needed
- **Professional UI**: Clean, modern chat interface

**Just run `start_ai_services.bat` and start chatting with your AI agents!**
