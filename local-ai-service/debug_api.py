#!/usr/bin/env python3
"""
Debug API Starter - with detailed error logging
"""

import os
import sys

# Set environment variable for G drive models
os.environ["OLLAMA_MODELS"] = "G:\\ollama_models"

# Add current directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def main():
    try:
        print("🔍 Debug API Starter")
        print("📍 Setting OLLAMA_MODELS to G:\\ollama_models")
        print("📂 Current directory:", current_dir)
        print("🐍 Python path:", sys.path[:3])
        print("")
        
        # Import FastAPI and other modules
        from fastapi import FastAPI, HTTPException
        from fastapi.middleware.cors import CORSMiddleware
        from pydantic import BaseModel
        import requests
        import uvicorn
        from datetime import datetime
        
        print("✅ Imported FastAPI modules successfully")
        
        # Create the app
        app = FastAPI(title="AI Chat API - Debug Version", version="1.0.0")
        
        # CORS
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        print("✅ Created FastAPI app with CORS")
        
        # Models
        class ChatRequest(BaseModel):
            prompt: str
            customer_tier: str = "basic"

        class ChatResponse(BaseModel):
            response: str
            model_used: str
            timestamp: str
        
        print("✅ Defined Pydantic models")
        
        @app.get("/")
        async def root():
            return {
                "message": "AI Chat API is running",
                "status": "healthy",
                "timestamp": datetime.now().isoformat()
            }
        
        @app.get("/health")
        async def health():
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
                print(f"🎯 Received request: {request.prompt[:50]}...")
                
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
                
                print(f"📡 Sending to Ollama: {ollama_url}")
                
                # Make request to Ollama with shorter timeout
                response = requests.post(ollama_url, json=payload, timeout=30)
                
                print(f"📡 Ollama response status: {response.status_code}")
                
                if response.status_code == 200:
                    result = response.json()
                    ai_response = result.get("response", "I apologize, but I couldn't generate a response.")
                    
                    print(f"✅ Got AI response: {ai_response[:50]}...")
                    
                    return ChatResponse(
                        response=ai_response,
                        model_used="llama3.2:1b",
                        timestamp=datetime.now().isoformat()
                    )
                else:
                    print(f"❌ Ollama error: {response.status_code}")
                    raise HTTPException(status_code=500, detail=f"Ollama API error: {response.status_code}")
                    
            except requests.exceptions.Timeout:
                print("⏰ Timeout error")
                return ChatResponse(
                    response="The AI is taking longer than expected. Please try a shorter message.",
                    model_used="timeout-fallback",
                    timestamp=datetime.now().isoformat()
                )
                
            except requests.exceptions.RequestException as e:
                print(f"🔌 Connection error: {e}")
                return ChatResponse(
                    response="I'm currently connecting to my AI model. Please try again in a moment.",
                    model_used="connection-fallback",
                    timestamp=datetime.now().isoformat()
                )
                
            except Exception as e:
                print(f"💥 Unexpected error: {e}")
                return ChatResponse(
                    response="I encountered an issue while processing your request. Please try again.",
                    model_used="error-fallback", 
                    timestamp=datetime.now().isoformat()
                )
        
        print("✅ Defined all endpoints")
        print("")
        print("🚀 Starting server on http://localhost:8001")
        print("=" * 60)
        
        # Start the server
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8001,
            reload=False,
            log_level="info"
        )
        
    except Exception as e:
        print(f"💥 CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
