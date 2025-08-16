#!/usr/bin/env python3
"""
Startup script for AI Chat API with proper environment setup
"""

import os
import sys

# Set Ollama models directory to G drive
os.environ["OLLAMA_MODELS"] = "G:\\ollama_models"

# Add the current directory to Python path
sys.path.append(os.path.dirname(__file__))

# Import and run the main app
if __name__ == "__main__":
    from simple_chat_api import app
    import uvicorn
    
    print("🚀 Starting AI Chat API with G: drive models...")
    print("📍 Ollama models directory: G:\\ollama_models")
    print("🤖 Using model: llama3.2:1b (1.3GB, much faster!)")
    print("📡 Server will be available at: http://localhost:8001")
    print("=" * 60)
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8001,
        reload=False,
        log_level="info"
    )
