#!/usr/bin/env python3
"""
🚀 ZERO-COST AI MARKETPLACE - INTEGRATED BACKEND STARTUP
========================================================

Starts the FastAPI backend with integrated chat interface serving.

Features:
- Chat interface served at http://localhost:8001/
- API endpoints at http://localhost:8001/api/
- Static file serving for frontend assets
- CORS configured for browser access

Usage:
    python start_backend.py
"""

import uvicorn
import sys
import os

def main():
    print("🚀 Starting Zero-Cost AI Marketplace with Integrated Chat Interface...")
    print("=" * 60)
    print("📡 Backend API: http://localhost:8001/api/")
    print("💬 Chat Interface: http://localhost:8001/")
    print("📊 Health Check: http://localhost:8001/api/health")
    print("📚 API Docs: http://localhost:8001/docs")
    print("=" * 60)
    print("")
    print("✅ Chat interface integrated and ready for use!")
    print("✅ CORS configured for frontend-backend communication")
    print("✅ Static file serving enabled")
    print("✅ Local AI models: gpt-oss:20b, llama3.2:3b")
    print("")
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    
    try:
        uvicorn.run(
            "backend.api.main:app",
            host="0.0.0.0",
            port=8001,
            reload=False,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()