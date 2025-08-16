#!/usr/bin/env python3
"""
Service Startup Manager
Starts all required services for the AI Agents Integration Lab
"""

import subprocess
import time
import sys
import requests
import os
from pathlib import Path
from typing import Dict, List, Tuple

class ServiceManager:
    """Manages startup and monitoring of all required services"""
    
    def __init__(self):
        self.services = {}
        self.project_root = Path(__file__).parent
        self.python_exe = self.project_root / "venv" / "Scripts" / "python.exe"
    
    def check_ollama_installed(self) -> bool:
        """Check if Ollama is installed"""
        try:
            result = subprocess.run(["ollama", "--version"], 
                                  capture_output=True, text=True, timeout=5)
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    def start_ollama(self) -> bool:
        """Start Ollama service"""
        print("🚀 Starting Ollama service...")
        
        if not self.check_ollama_installed():
            print("❌ Ollama is not installed!")
            print("   Please install Ollama from: https://ollama.ai")
            return False
        
        try:
            # Kill any existing Ollama processes
            subprocess.run(["taskkill", "/f", "/im", "ollama.exe"], 
                         capture_output=True, timeout=10)
            time.sleep(2)
        except:
            pass
        
        try:
            # Start Ollama service in background
            process = subprocess.Popen(["ollama", "serve"], 
                                     stdout=subprocess.DEVNULL,
                                     stderr=subprocess.DEVNULL)
            
            # Wait for service to start
            for i in range(20):  # Wait up to 20 seconds
                try:
                    response = requests.get("http://localhost:11434/api/tags", timeout=2)
                    if response.status_code == 200:
                        print("✅ Ollama service started successfully")
                        self.services["ollama"] = process
                        return True
                except:
                    time.sleep(1)
            
            print("❌ Ollama service failed to start properly")
            return False
            
        except Exception as e:
            print(f"❌ Failed to start Ollama: {e}")
            return False
    
    def start_local_ai_service(self) -> bool:
        """Start the local AI service"""
        print("🚀 Starting Local AI service...")
        
        service_dir = self.project_root / "local-ai-service"
        startup_script = service_dir / "start_api.py"
        
        if not startup_script.exists():
            print(f"❌ Startup script not found: {startup_script}")
            return False
        
        try:
            # Start the service
            process = subprocess.Popen([str(self.python_exe), str(startup_script)],
                                     cwd=str(service_dir),
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)
            
            # Wait for service to start
            for i in range(15):  # Wait up to 15 seconds
                try:
                    response = requests.get("http://localhost:8001/health", timeout=2)
                    if response.status_code == 200:
                        print("✅ Local AI service started successfully")
                        self.services["local_ai"] = process
                        return True
                except:
                    time.sleep(1)
                    
                # Check if process is still alive
                if process.poll() is not None:
                    stdout, stderr = process.communicate()
                    print(f"❌ Local AI service process died")
                    if stderr:
                        print(f"   Error: {stderr.decode()}")
                    return False
            
            print("❌ Local AI service failed to respond")
            return False
            
        except Exception as e:
            print(f"❌ Failed to start Local AI service: {e}")
            return False
    
    def start_marketplace_service(self) -> bool:
        """Start the marketplace service"""
        print("🚀 Starting Marketplace service...")
        
        marketplace_dir = self.project_root / "zero-cost-ai-marketplace"
        
        # Check for different possible startup files
        startup_files = [
            marketplace_dir / "backend" / "api" / "main.py",
            marketplace_dir / "main.py",
            marketplace_dir / "app.py"
        ]
        
        startup_script = None
        for file in startup_files:
            if file.exists():
                startup_script = file
                break
        
        if not startup_script:
            print("❌ No marketplace startup script found")
            return False
        
        try:
            # Start with uvicorn
            process = subprocess.Popen([
                str(self.python_exe), "-m", "uvicorn",
                f"{startup_script.stem}:app",
                "--host", "0.0.0.0",
                "--port", "8080"
            ], cwd=str(startup_script.parent),
               stdout=subprocess.PIPE,
               stderr=subprocess.PIPE)
            
            # Wait for service to start
            for i in range(15):
                try:
                    response = requests.get("http://localhost:8080", timeout=2)
                    if response.status_code == 200:
                        print("✅ Marketplace service started successfully")
                        self.services["marketplace"] = process
                        return True
                except:
                    time.sleep(1)
                
                # Check if process is still alive
                if process.poll() is not None:
                    stdout, stderr = process.communicate()
                    print(f"❌ Marketplace service process died")
                    if stderr:
                        print(f"   Error: {stderr.decode()}")
                    return False
            
            print("❌ Marketplace service failed to respond")
            return False
            
        except Exception as e:
            print(f"❌ Failed to start Marketplace service: {e}")
            return False
    
    def check_models(self) -> bool:
        """Check and pull required models"""
        print("🤖 Checking AI models...")
        
        required_models = ["llama3.2:3b"]
        
        try:
            # Get list of installed models
            response = requests.get("http://localhost:11434/api/tags", timeout=10)
            if response.status_code != 200:
                print("❌ Cannot connect to Ollama service")
                return False
            
            installed_models = [model["name"] for model in response.json().get("models", [])]
            
            for model in required_models:
                if model not in installed_models:
                    print(f"📥 Pulling model: {model}")
                    result = subprocess.run(["ollama", "pull", model], 
                                          capture_output=True, text=True, timeout=300)
                    if result.returncode == 0:
                        print(f"✅ Model {model} pulled successfully")
                    else:
                        print(f"❌ Failed to pull model {model}")
                        return False
                else:
                    print(f"✅ Model {model} already installed")
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to check models: {e}")
            return False
    
    def start_all_services(self) -> bool:
        """Start all required services"""
        print("🚀 AI Agents Integration Lab - Service Startup")
        print("=" * 60)
        
        success_count = 0
        
        # Start Ollama first (required by other services)
        if self.start_ollama():
            success_count += 1
            
            # Pull required models
            if self.check_models():
                print("✅ All required models are available")
        
        # Start Local AI service
        if self.start_local_ai_service():
            success_count += 1
        
        # Start Marketplace service
        if self.start_marketplace_service():
            success_count += 1
        
        print("\n" + "=" * 60)
        print(f"🏁 Service Startup Complete: {success_count}/3 services started")
        
        if success_count == 3:
            print("✅ All services started successfully!")
            print("\n📋 Service URLs:")
            print("   🤖 Ollama API: http://localhost:11434")
            print("   🔧 Local AI Service: http://localhost:8001")
            print("   🌐 Marketplace: http://localhost:8080")
            return True
        else:
            print("⚠️  Some services failed to start")
            return False
    
    def stop_all_services(self):
        """Stop all running services"""
        print("🛑 Stopping all services...")
        
        for service_name, process in self.services.items():
            try:
                print(f"   Stopping {service_name}...")
                process.terminate()
                process.wait(timeout=5)
                print(f"   ✅ {service_name} stopped")
            except:
                try:
                    process.kill()
                    print(f"   ✅ {service_name} killed")
                except:
                    print(f"   ⚠️  Could not stop {service_name}")
        
        # Also try to kill Ollama specifically
        try:
            subprocess.run(["taskkill", "/f", "/im", "ollama.exe"], 
                         capture_output=True, timeout=5)
        except:
            pass

def main():
    """Main function"""
    manager = ServiceManager()
    
    try:
        success = manager.start_all_services()
        
        if success:
            print("\n🎉 Press Ctrl+C to stop all services")
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n🛑 Shutdown requested...")
                manager.stop_all_services()
                print("✅ All services stopped")
        else:
            print("\n❌ Service startup failed")
            return 1
            
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        manager.stop_all_services()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
