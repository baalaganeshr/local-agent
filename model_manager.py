#!/usr/bin/env python3
"""
Model Management Helper
Add and manage additional models for the unified API
"""

import os
import subprocess
import requests
import json

def check_ollama_models():
    """Check what models are currently available in Ollama"""
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        if result.returncode == 0:
            print("📋 Currently available Ollama models:")
            print(result.stdout)
            return result.stdout
        else:
            print("❌ Error checking Ollama models")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def pull_model(model_name):
    """Pull a new model using Ollama"""
    try:
        print(f"📥 Pulling model: {model_name}")
        result = subprocess.run(['ollama', 'pull', model_name], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Successfully pulled {model_name}")
            return True
        else:
            print(f"❌ Failed to pull {model_name}: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error pulling model: {e}")
        return False

def suggest_models():
    """Suggest additional models that work well"""
    suggestions = [
        {
            "name": "llama3.2:3b",
            "description": "Larger Llama 3.2 model (3B parameters) - Better quality, slower",
            "size": "~2GB"
        },
        {
            "name": "phi3:mini",
            "description": "Microsoft Phi-3 Mini - Fast and efficient",
            "size": "~2.3GB"
        },
        {
            "name": "gemma2:2b",
            "description": "Google Gemma 2B - Good balance of speed and quality",
            "size": "~1.6GB"
        },
        {
            "name": "codellama:7b-code",
            "description": "Code-specific Llama model - Great for programming",
            "size": "~3.8GB"
        }
    ]
    
    print("\n🤖 Suggested models to add:")
    print("=" * 50)
    for i, model in enumerate(suggestions, 1):
        print(f"{i}. {model['name']}")
        print(f"   📝 {model['description']}")
        print(f"   💾 Size: {model['size']}")
        print()

def test_api():
    """Test the unified API"""
    try:
        response = requests.get("http://localhost:8002/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Unified API is healthy!")
            print(f"📍 Models available: {data.get('models', [])}")
            print(f"🗂️ Model path: {data.get('model_path', 'Not set')}")
            return True
        else:
            print("❌ API responded with error")
            return False
    except Exception as e:
        print(f"❌ API not accessible: {e}")
        return False

def main():
    print("🚀 AI Model Management Helper")
    print("=" * 40)
    
    # Check current models
    check_ollama_models()
    
    # Test API
    test_api()
    
    # Suggest additional models
    suggest_models()
    
    print("💡 To add a model, run: ollama pull <model_name>")
    print("📖 For more models, visit: https://ollama.ai/library")
    
    # Check if we want to pull a model
    while True:
        choice = input("\n🤖 Would you like to pull a suggested model? (1-4, or 'n' to skip): ")
        if choice.lower() == 'n':
            break
        elif choice in ['1', '2', '3', '4']:
            models = ["llama3.2:3b", "phi3:mini", "gemma2:2b", "codellama:7b-code"]
            selected_model = models[int(choice) - 1]
            
            confirm = input(f"📥 Pull {selected_model}? This may take several minutes. (y/n): ")
            if confirm.lower() == 'y':
                pull_model(selected_model)
                check_ollama_models()
            break
        else:
            print("❌ Invalid choice. Please enter 1-4 or 'n'.")

if __name__ == "__main__":
    main()
