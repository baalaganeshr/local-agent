#!/usr/bin/env python3
"""
Unified Agent API - Single Entry Point for All AI Agents
Integrates all agents into a single API server for the chat interface
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import asyncio
import json
import time
from datetime import datetime
import uvicorn
import sys
import os
import requests
import aiofiles

# Set environment variables
os.environ["OLLAMA_MODELS"] = "G:\\ollama_models"

# Add project paths
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.join(current_dir, 'agents'))

app = FastAPI(
    title="🤖 Unified Agent API",
    description="Single API for all AI agents with local model integration",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatMessage(BaseModel):
    message: str
    meta: Optional[Dict[str, Any]] = None

class AgentResponse(BaseModel):
    response: str
    agent: str
    model: str
    timestamp: str

# Global configuration
OLLAMA_BASE_URL = "http://localhost:11434"
DEFAULT_MODEL = "llama3.2:1b"

def get_available_models():
    """Get list of available Ollama models"""
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            return [model["name"] for model in models]
    except:
        pass
    return [DEFAULT_MODEL]

def call_ollama(prompt: str, model: str = DEFAULT_MODEL) -> str:
    """Call Ollama API directly"""
    try:
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
                "max_tokens": 2000
            }
        }
        
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return result.get("response", "No response generated")
        else:
            return f"Error: {response.status_code} - {response.text}"
            
    except Exception as e:
        return f"Error connecting to Ollama: {str(e)}"

def call_ollama_stream(prompt: str, model: str = DEFAULT_MODEL):
    """Stream response from Ollama"""
    try:
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": True,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
                "max_tokens": 2000
            }
        }
        
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json=payload,
            stream=True,
            timeout=30
        )
        
        if response.status_code == 200:
            for line in response.iter_lines():
                if line:
                    try:
                        data = json.loads(line)
                        if 'response' in data:
                            yield data['response']
                    except:
                        continue
        else:
            yield f"Error: {response.status_code} - {response.text}"
            
    except Exception as e:
        yield f"Error connecting to Ollama: {str(e)}"

# Customer Request Agent Integration
class CustomerRequestProcessor:
    """Process customer requests with intelligent routing"""
    
    def __init__(self):
        self.agent_name = "Customer Request Agent"
        self.models = get_available_models()
    
    def process_request(self, message: str, files: List[str] = None) -> str:
        """Process customer request with context"""
        
        # Enhanced prompt with agent context
        context_prompt = f"""You are an expert AI assistant representing a professional AI services company. 
        
Your capabilities:
- Technical consulting and solution architecture
- Code review and development assistance  
- Business analysis and requirements gathering
- Integration planning and system design
- Multi-model AI deployment strategies

Customer Request: {message}

Provide a comprehensive, professional response that demonstrates expertise while being helpful and actionable. 
If files were attached, acknowledge them and explain how you would process them.

Response:"""

        if files:
            context_prompt += f"\n\nAttached Files: {', '.join(files)}"
            context_prompt += "\nNote: File processing capabilities available for analysis."

        return call_ollama(context_prompt, self.models[0] if self.models else DEFAULT_MODEL)

    def stream_response(self, message: str, files: List[str] = None):
        """Stream the response"""
        context_prompt = f"""You are an expert AI assistant representing a professional AI services company. 

Customer Request: {message}

Provide a comprehensive, professional response:"""

        if files:
            context_prompt += f"\n\nAttached Files: {', '.join(files)}"

        return call_ollama_stream(context_prompt, self.models[0] if self.models else DEFAULT_MODEL)

# Initialize processors
customer_processor = CustomerRequestProcessor()

@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "service": "Unified Agent API",
        "status": "running",
        "models": get_available_models(),
        "agents": ["customer_request", "marketplace", "owl_integration"],
        "endpoints": [
            "/agents/customer_request",
            "/agents/marketplace", 
            "/agents/status",
            "/health"
        ]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    models = get_available_models()
    
    # Test Ollama connection
    ollama_status = "healthy"
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=3)
        if response.status_code != 200:
            ollama_status = "error"
    except:
        ollama_status = "disconnected"
    
    return {
        "status": "healthy" if ollama_status == "healthy" else "degraded",
        "ollama": ollama_status,
        "models": models,
        "model_path": os.environ.get("OLLAMA_MODELS", "default"),
        "timestamp": datetime.now().isoformat()
    }

@app.post("/agents/customer_request")
async def customer_request_endpoint(
    message: str = Form(...),
    files: List[UploadFile] = File(default=[])
):
    """Handle customer requests with file support"""
    
    # Process uploaded files
    file_names = []
    if files and files[0].filename:  # Check if files were actually uploaded
        for file in files:
            if file.filename:
                file_names.append(file.filename)
                # Save file for processing (optional)
                # content = await file.read()
                # You could save and process files here
    
    # Process the request
    try:
        response_text = customer_processor.process_request(message, file_names)
        
        return {
            "response": response_text,
            "agent": "customer_request",
            "model": customer_processor.models[0] if customer_processor.models else DEFAULT_MODEL,
            "files_processed": len(file_names),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")

@app.post("/agents/customer_request_json")
async def customer_request_json(request: ChatMessage):
    """Handle JSON customer requests"""
    
    try:
        response_text = customer_processor.process_request(request.message)
        
        return {
            "response": response_text,
            "agent": "customer_request", 
            "model": customer_processor.models[0] if customer_processor.models else DEFAULT_MODEL,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")

@app.get("/agents/status")
async def agent_status():
    """Get status of all agents"""
    return {
        "customer_request": {
            "status": "active",
            "model": customer_processor.models[0] if customer_processor.models else DEFAULT_MODEL,
            "capabilities": ["text_processing", "file_analysis", "consultation"]
        },
        "marketplace": {
            "status": "active", 
            "features": ["service_discovery", "pricing", "integration"]
        },
        "system": {
            "ollama_models": get_available_models(),
            "model_path": os.environ.get("OLLAMA_MODELS"),
            "api_version": "2.0.0"
        }
    }

# Additional endpoints for other agents can be added here

if __name__ == "__main__":
    print("🚀 Starting Unified Agent API...")
    print(f"📍 Ollama models: {os.environ.get('OLLAMA_MODELS', 'default location')}")
    print(f"🤖 Available models: {get_available_models()}")
    print("📡 API will be available at: http://localhost:8002")
    print("🎯 Chat Interface: ai_chat.html")
    print("=" * 60)
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8002,
        reload=False,
        log_level="info"
    )
