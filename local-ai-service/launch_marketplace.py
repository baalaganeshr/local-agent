#!/usr/bin/env python3
"""
🚀 ZERO-COST AI MARKETPLACE LAUNCHER
===================================

CEO's One-Click Launch System for Market Domination!

This script launches the complete AI marketplace with:
✅ Smart model routing
✅ Business API service  
✅ Real-time analytics
✅ 95% profit margins
"""

import asyncio
import subprocess
import sys
import os
import time
import requests
from pathlib import Path

def print_ceo_banner():
    """Print the CEO's victory banner"""
    banner = """
🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀
🚀                                                                🚀
🚀        ZERO-COST AI MARKETPLACE LAUNCHER                      🚀  
🚀        =================================                       🚀
🚀                                                                🚀
🚀    💎 COMPETITIVE ADVANTAGES:                                 🚀
🚀       • ZERO AI API costs (100% local)                       🚀
🚀       • Smart dual-model routing                             🚀
🚀       • 95-98% profit margins                               🚀
🚀       • Enterprise-grade quality                            🚀
🚀                                                                🚀
🚀    🎯 BUSINESS MODEL:                                         🚀  
🚀       • Basic: $0.05/request → 98% margin                   🚀
🚀       • Premium: $0.15/request → 95% margin                 🚀
🚀       • Enterprise: $0.30/request → 95% margin              🚀
🚀                                                                🚀
🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀
"""
    print(banner)

def check_ollama_service():
    """Check if Ollama service is running"""
    print("🔍 Checking Ollama service...")
    
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json()
            model_names = [model['name'] for model in models.get('models', [])]
            print(f"✅ Ollama is running with models: {model_names}")
            return True, model_names
        else:
            print(f"❌ Ollama API returned status {response.status_code}")
            return False, []
    except requests.exceptions.RequestException as e:
        print(f"❌ Ollama service not available: {e}")
        return False, []

def verify_models():
    """Verify required models are available"""
    print("🔍 Verifying AI models...")
    
    ollama_running, models = check_ollama_service()
    
    if not ollama_running:
        print("❌ ERROR: Ollama service is not running!")
        print("💡 SOLUTION: Run 'ollama serve' in another terminal")
        return False
    
    required_models = ["llama3.2:3b", "gpt-oss:20b"]
    available_models = [model for model in required_models if any(req in model for req in models)]
    
    print(f"📦 Required models: {required_models}")
    print(f"✅ Available models: {available_models}")
    
    if len(available_models) >= 1:
        print("✅ At least one model available - marketplace can operate")
        return True
    else:
        print("❌ No required models found!")
        print("💡 SOLUTION: Run 'ollama pull llama3.2:3b' and 'ollama pull gpt-oss:20b'")
        return False

def install_requirements():
    """Install required Python packages"""
    print("📦 Installing requirements...")
    
    requirements_file = Path(__file__).parent / "requirements.txt"
    
    if requirements_file.exists():
        try:
            subprocess.run([
                sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
            ], check=True, capture_output=True, text=True)
            print("✅ Requirements installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install requirements: {e}")
            print("💡 Try running: pip install fastapi uvicorn requests")
            return False
    else:
        print("⚠️ requirements.txt not found, continuing anyway...")
        return True

def launch_api_service():
    """Launch the FastAPI business service"""
    print("🚀 Launching AI Marketplace API...")
    
    api_file = Path(__file__).parent / "api" / "business_api.py"
    
    if not api_file.exists():
        print(f"❌ API file not found: {api_file}")
        return None
    
    try:
        # Launch FastAPI with uvicorn
        cmd = [
            sys.executable, "-m", "uvicorn",
            "api.business_api:app",
            "--host", "0.0.0.0",
            "--port", "8000",
            "--reload"
        ]
        
        print(f"Running command: {' '.join(cmd)}")
        
        process = subprocess.Popen(
            cmd,
            cwd=Path(__file__).parent,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        return process
    
    except Exception as e:
        print(f"❌ Failed to launch API: {e}")
        return None

def wait_for_api_startup():
    """Wait for API to be ready"""
    print("⏳ Waiting for API to start...")
    
    for attempt in range(30):
        try:
            response = requests.get("http://localhost:8000/health", timeout=2)
            if response.status_code == 200:
                print("✅ API is ready!")
                return True
        except:
            pass
        
        time.sleep(1)
        print(f"   Attempt {attempt + 1}/30...")
    
    print("❌ API failed to start within 30 seconds")
    return False

def run_quick_test():
    """Run a quick test of the marketplace"""
    print("🧪 Running quick marketplace test...")
    
    try:
        # Test basic endpoint
        response = requests.get("http://localhost:8000/", timeout=10)
        if response.status_code == 200:
            print("✅ Basic endpoint working")
        
        # Test AI generation
        ai_request = {
            "prompt": "Hello, test the marketplace!",
            "customer_tier": "basic"
        }
        
        response = requests.post(
            "http://localhost:8000/ai/generate", 
            json=ai_request, 
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ AI generation working:")
            print(f"   Model: {result['model_used']}")
            print(f"   Time: {result['response_time']}s")
            print(f"   Efficiency: {result['cost_efficiency']}")
            print(f"   Response: {result['response'][:100]}...")
            return True
        else:
            print(f"❌ AI generation failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def show_success_message():
    """Show the CEO's success message"""
    success_banner = """
🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉
🎉                                                                🎉
🎉        🚀 MARKETPLACE LAUNCHED SUCCESSFULLY! 🚀               🎉
🎉        =======================================                🎉
🎉                                                                🎉
🎉    💎 YOUR ZERO-COST AI MARKETPLACE IS LIVE!                 🎉
🎉                                                                🎉
🎉    🌐 API URL: http://localhost:8000                          🎉
🎉    📚 Documentation: http://localhost:8000/docs               🎉
🎉    📊 Business Analytics: http://localhost:8000/business/analytics 🎉
🎉    ❤️ Health Check: http://localhost:8000/health              🎉
🎉                                                                🎉
🎉    🎯 NEXT STEPS:                                             🎉
🎉       1. Open http://localhost:8000/docs in your browser     🎉
🎉       2. Test the /ai/generate endpoint                       🎉
🎉       3. Check /business/analytics for profit metrics        🎉
🎉       4. Scale up and DOMINATE THE MARKET! 💪                🎉
🎉                                                                🎉
🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉
"""
    print(success_banner)

def main():
    """Main launcher function"""
    
    print_ceo_banner()
    
    print("🏁 STARTING MARKETPLACE LAUNCH SEQUENCE...")
    print("=" * 60)
    
    # Step 1: Verify models
    if not verify_models():
        print("\n❌ LAUNCH ABORTED: Models not ready")
        print("Please ensure Ollama is running and models are installed")
        return False
    
    # Step 2: Install requirements  
    if not install_requirements():
        print("\n⚠️ WARNING: Requirements installation failed")
        print("Continuing anyway - some features may not work")
    
    # Step 3: Launch API service
    api_process = launch_api_service()
    if not api_process:
        print("\n❌ LAUNCH ABORTED: Could not start API service")
        return False
    
    try:
        # Step 4: Wait for startup
        if not wait_for_api_startup():
            print("\n❌ LAUNCH ABORTED: API failed to start")
            return False
        
        # Step 5: Run tests
        if run_quick_test():
            show_success_message()
        else:
            print("\n⚠️ WARNING: Some tests failed, but marketplace is running")
            print("🌐 API URL: http://localhost:8000")
            print("📚 Documentation: http://localhost:8000/docs")
        
        # Step 6: Keep running
        print("\n🔄 Marketplace is running... Press Ctrl+C to stop")
        
        try:
            api_process.wait()
        except KeyboardInterrupt:
            print("\n\n🛑 Shutting down marketplace...")
            api_process.terminate()
            api_process.wait()
            print("✅ Marketplace stopped successfully")
            
    except Exception as e:
        print(f"\n❌ Error during operation: {e}")
        if api_process:
            api_process.terminate()
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎯 MISSION ACCOMPLISHED! Zero-cost AI marketplace launched successfully!")
    else:
        print("\n❌ LAUNCH FAILED! Check the errors above and try again.")
    
    sys.exit(0 if success else 1)
