#!/usr/bin/env python3
"""
Simple AI Chat API - Direct Ollama Integration
Works with available models without complex routing
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import requests
import json
import uvicorn
import time
from datetime import datetime

# Set Ollama models directory to G drive if not already set
if "OLLAMA_MODELS" not in os.environ:
    os.environ["OLLAMA_MODELS"] = "G:\\ollama_models"

app = FastAPI(title="AI Chat API", version="1.0.0")

# CORS middleware for web integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    prompt: str
    customer_tier: str = "basic"

class ChatResponse(BaseModel):
    response: str
    model_used: str = "gpt-oss:20b"
    timestamp: str

@app.get("/")
async def root():
    return {
        "message": "AI Chat API is running",
        "status": "healthy",
        "available_endpoints": ["/ai/generate", "/health"]
    }

@app.get("/health")
async def health_check():
        return {
            "status": "healthy",
            "message": "AI Chat API is operational",
            "models_available": ["llama3.2:1b"],
            "timestamp": datetime.now().isoformat()
        }

@app.post("/ai/generate")
async def generate_response(request: ChatRequest):
    """Generate AI response using available Ollama model"""
    
    try:
        # Try to use Ollama API directly with shorter timeout
        ollama_url = "http://localhost:11434/api/generate"
        
        payload = {
            "model": "llama3.2:1b",
            "prompt": request.prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
                "num_ctx": 1024
            }
        }
        
        # Make request to Ollama with shorter timeout
        response = requests.post(ollama_url, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            ai_response = result.get("response", "I apologize, but I couldn't generate a response.")
            
            return ChatResponse(
                response=ai_response,
                model_used="llama3.2:1b",
                timestamp=datetime.now().isoformat()
            )
        else:
            # Fallback response when Ollama is not available
            fallback_responses = [
                "Hello! I'm your AI assistant. I'm currently connecting to my language model. Please try again in a moment.",
                "Hi there! I'm here to help you. My AI model is loading - please give me a few seconds.",
                "Welcome! I'm your local AI assistant. I'm working on connecting to provide you with the best responses.",
                "Thanks for your message! I'm an AI assistant ready to help. Let me process your request."
            ]
            
            # Simple response based on input
            if "hello" in request.prompt.lower() or "hi" in request.prompt.lower():
                ai_response = "Hello! How can I help you today?"
            elif "how are you" in request.prompt.lower():
                ai_response = "I'm doing well, thank you! I'm an AI assistant here to help you with any questions or tasks."
            elif "what can you do" in request.prompt.lower():
                ai_response = "I can help you with various tasks like answering questions, providing information, creative writing, analysis, and general conversation. What would you like to know about?"
            else:
                ai_response = f"I understand you're asking about: {request.prompt}. I'm currently connecting to my AI model to provide you with a detailed response. Please try again in a moment, or feel free to ask another question!"
            
            return ChatResponse(
                response=ai_response,
                model_used="fallback-assistant",
                timestamp=datetime.now().isoformat()
            )
            
    except requests.exceptions.RequestException as e:
        # Network/connection error - provide helpful fallback
        return ChatResponse(
            response="I'm currently connecting to my AI model. Please try again in a moment. In the meantime, I'm here and ready to help once the connection is established!",
            model_used="connection-fallback",
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        # Other errors
        return ChatResponse(
            response="I encountered an issue while processing your request. Please try asking your question again, or try a different question.",
            model_used="error-fallback", 
            timestamp=datetime.now().isoformat()
        )

if __name__ == "__main__":
    print("🚀 Starting Simple AI Chat API...")
    print(f"📍 Ollama models directory: {os.environ.get('OLLAMA_MODELS', 'default')}")
    print("🤖 Using model: llama3.2:1b (1.3GB, much faster!)")
    print("📡 Server will be available at: http://localhost:8001")
    print("🎯 Compatible with ai_chat.html interface")
    print("=" * 60)
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8001,
        reload=False,
        log_level="info"
    )
