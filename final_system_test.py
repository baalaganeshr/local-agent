#!/usr/bin/env python3
"""
Final System Test and Usage Guide
Complete AI Chat Integration Test
"""

import requests
import time
import json
import webbrowser
import os
from datetime import datetime

def test_ollama_service():
    """Test if Ollama service is running"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        return response.status_code == 200
    except:
        return False

def test_api_endpoints():
    """Test all API endpoints"""
    endpoints = {
        "Health": "http://localhost:8001/health",
        "Root": "http://localhost:8001/",
        "Generate": "http://localhost:8001/ai/generate"
    }
    
    results = {}
    
    for name, url in endpoints.items():
        try:
            if name == "Generate":
                # Test with a simple prompt
                payload = {"prompt": "Hello, how are you?"}
                response = requests.post(url, json=payload, timeout=15)
            else:
                response = requests.get(url, timeout=10)
            
            results[name] = {
                "status": response.status_code,
                "working": response.status_code == 200,
                "response": response.text[:100] if len(response.text) < 100 else response.text[:100] + "..."
            }
        except Exception as e:
            results[name] = {
                "status": "ERROR",
                "working": False,
                "response": str(e)
            }
    
    return results

def open_chat_interface():
    """Open the chat interface in default browser"""
    chat_path = r"G:\c\OneDrive\Desktop\localai\local-agent\local-ai-service\ai_chat.html"
    if os.path.exists(chat_path):
        webbrowser.open(f"file:///{chat_path}")
        return True
    return False

def main():
    print("=" * 60)
    print("🚀 FINAL AI CHAT SYSTEM TEST")
    print("=" * 60)
    
    # Test Ollama
    print("\n1. Testing Ollama Service...")
    ollama_ok = test_ollama_service()
    print(f"   Ollama Status: {'✅ RUNNING' if ollama_ok else '❌ NOT RUNNING'}")
    
    # Test API
    print("\n2. Testing API Endpoints...")
    api_results = test_api_endpoints()
    
    working_count = 0
    total_count = len(api_results)
    
    for endpoint, result in api_results.items():
        status = "✅ WORKING" if result["working"] else "❌ FAILED"
        print(f"   {endpoint}: {status}")
        if result["working"]:
            working_count += 1
        if not result["working"]:
            print(f"      Error: {result['response']}")
    
    # Overall Status
    print(f"\n3. System Status:")
    print(f"   API Endpoints: {working_count}/{total_count} working")
    print(f"   Ollama: {'Connected' if ollama_ok else 'Disconnected'}")
    
    # Open chat interface
    print(f"\n4. Opening Chat Interface...")
    chat_opened = open_chat_interface()
    if chat_opened:
        print("   ✅ Chat interface opened in browser")
    else:
        print("   ❌ Could not open chat interface")
    
    # Final verdict
    print("\n" + "=" * 60)
    if working_count >= 2 and ollama_ok:
        print("🎉 SYSTEM READY FOR USE!")
        print("📱 Your AI Chat is now available in the browser window")
        print("💬 Type any message to start chatting with the AI")
        
        print(f"\n📋 USAGE INSTRUCTIONS:")
        print(f"   1. Use the opened browser window to chat")
        print(f"   2. API is running on: http://localhost:8001")
        print(f"   3. AI Model: gpt-oss:20b (13GB)")
        print(f"   4. Type messages and get AI responses instantly")
        
        print(f"\n🔧 TECHNICAL INFO:")
        print(f"   - FastAPI Server: localhost:8001")
        print(f"   - Ollama Service: localhost:11434")
        print(f"   - Chat Interface: {r'G:\c\OneDrive\Desktop\localai\local-agent\local-ai-service\ai_chat.html'}")
        
    else:
        print("❌ SYSTEM NOT FULLY READY")
        print("   Check the errors above and restart services if needed")
    
    print("=" * 60)
    
    # Keep the API running
    print(f"\n⏰ Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("💡 The API server should still be running in the background")
    print("🔄 You can run this test again anytime to check system status")

if __name__ == "__main__":
    main()
