#!/usr/bin/env python3
"""
Complete Integration Test - End-to-End AI Chat System
Tests the full integration from chat interface to AI models
"""

import requests
import json
import time
from datetime import datetime

def test_complete_integration():
    """Test the complete AI chat integration"""
    print("🚀 Testing Complete AI Chat Integration")
    print("=" * 60)
    
    # Test messages to send
    test_messages = [
        "Hello! How are you?",
        "What can you help me with?", 
        "Tell me about artificial intelligence",
        "What's the weather like?",
        "Can you write a short poem?"
    ]
    
    api_url = "http://localhost:8001/ai/generate"
    health_url = "http://localhost:8001/health"
    
    # First check API health
    print("🔍 Checking API Health...")
    try:
        health_response = requests.get(health_url, timeout=5)
        if health_response.status_code == 200:
            health_data = health_response.json()
            print(f"✅ API Status: {health_data['status']}")
            print(f"✅ Available Models: {health_data['models_available']}")
            print(f"✅ API Message: {health_data['message']}")
        else:
            print(f"❌ Health check failed with status: {health_response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False
    
    print("\n🤖 Testing AI Chat Responses...")
    success_count = 0
    total_tests = len(test_messages)
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n📝 Test {i}/{total_tests}: {message[:30]}...")
        
        try:
            # Prepare request
            payload = {
                "prompt": message,
                "customer_tier": "basic"
            }
            
            # Send request
            start_time = time.time()
            response = requests.post(api_url, json=payload, timeout=30)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                ai_response = data.get('response', 'No response')
                model_used = data.get('model_used', 'Unknown')
                
                print(f"✅ Response received ({response_time:.2f}s)")
                print(f"🤖 Model: {model_used}")
                print(f"💬 AI Response: {ai_response[:100]}...")
                
                success_count += 1
            else:
                print(f"❌ Request failed with status: {response.status_code}")
                print(f"   Error: {response.text}")
                
        except Exception as e:
            print(f"❌ Request error: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    print("🏁 INTEGRATION TEST SUMMARY")
    print("=" * 60)
    
    success_rate = (success_count / total_tests) * 100
    print(f"📊 Success Rate: {success_count}/{total_tests} ({success_rate:.1f}%)")
    
    if success_rate >= 80:
        print("✅ INTEGRATION TEST: PASSED")
        print("🎉 AI Chat system is fully operational!")
        
        print(f"\n🔗 System URLs:")
        print(f"   • Chat Interface: file:///G:/c/OneDrive/Desktop/localai/local-agent/local-ai-service/ai_chat.html")
        print(f"   • API Health: {health_url}")
        print(f"   • API Endpoint: {api_url}")
        
        return True
    else:
        print("❌ INTEGRATION TEST: FAILED")
        print("⚠️  Some components need attention")
        return False

if __name__ == "__main__":
    success = test_complete_integration()
    
    if success:
        print(f"\n🎯 READY TO USE!")
        print("You can now open the ai_chat.html file in your browser and start chatting!")
        print("The AI will respond using the integrated local models and services.")
    else:
        print(f"\n🔧 NEEDS WORK")
        print("Some integration issues need to be resolved.")
    
    exit(0 if success else 1)
