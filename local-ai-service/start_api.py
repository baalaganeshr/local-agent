#!/usr/bin/env python3
"""
🚀 MINIMAL API LAUNCHER
Direct FastAPI startup without module path issues
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.business_api import app
import uvicorn

if __name__ == "__main__":
    print("🚀 Starting Zero-Cost AI Marketplace API...")
    print("📡 Server will be available at: http://localhost:8001")
    print("🎯 Chat Interface: Open ai_chat.html in your browser")
    print("=" * 60)
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8001,
        reload=False,
        log_level="info"
    )
