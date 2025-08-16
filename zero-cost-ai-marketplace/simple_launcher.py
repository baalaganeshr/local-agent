#!/usr/bin/env python3
"""
Marketplace Service Launcher
Simple launcher for the zero-cost AI marketplace
"""

import sys
import os
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent / "backend"
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

# Add the root directory to Python path  
root_dir = Path(__file__).parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

try:
    from fastapi import FastAPI, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    from pydantic import BaseModel
    import uvicorn
    
    # Create a simple FastAPI app
    app = FastAPI(title="Zero-Cost AI Marketplace", version="1.0.0")
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    @app.get("/")
    async def root():
        return {
            "message": "Zero-Cost AI Marketplace API",
            "status": "running",
            "version": "1.0.0"
        }
    
    @app.get("/health")
    async def health_check():
        return {
            "status": "healthy",
            "service": "marketplace"
        }
    
    @app.get("/api/status")
    async def api_status():
        return {
            "api_status": "operational",
            "services": {
                "marketplace": "running",
                "agents": "available"
            }
        }
    
    if __name__ == "__main__":
        print("🚀 Starting Zero-Cost AI Marketplace...")
        print("📡 Server will be available at: http://localhost:8080")
        print("=" * 60)
        
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8080,
            reload=False,
            log_level="info"
        )

except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Installing missing dependencies...")
    
    import subprocess
    result = subprocess.run([sys.executable, "-m", "pip", "install", "fastapi", "uvicorn"], 
                          capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Dependencies installed. Please run again.")
    else:
        print(f"❌ Failed to install dependencies: {result.stderr}")
