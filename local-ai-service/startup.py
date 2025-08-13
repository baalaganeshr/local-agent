#!/usr/bin/env python3
"""
🚀 ZERO-COST AI MARKETPLACE - DIRECT STARTUP
CEO Emergency Launch System
"""
import sys
import os

# Add current directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Direct import and launch
from api.business_api import app
import uvicorn

if __name__ == "__main__":
    print("🚀🚀🚀 CEO EMERGENCY LAUNCH SEQUENCE 🚀🚀🚀")
    print("=" * 60)
    print("💎 ZERO-COST AI MARKETPLACE")
    print("💰 95-98% PROFIT MARGINS")
    print("🎯 COMPETITIVE ADVANTAGE ACTIVATED")
    print("=" * 60)
    
    uvicorn.run(
        app,
        host="localhost",
        port=8001,  # Alternative port to avoid conflicts
        reload=False,  # Disable reload for production stability
        access_log=True
    )
