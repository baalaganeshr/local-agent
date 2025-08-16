#!/usr/bin/env python3
"""
Quick Service Status Check
"""

import requests
import sys
from datetime import datetime

def check_service_status():
    """Check status of all services"""
    print(f"🔍 Service Status Check - {datetime.now().strftime('%H:%M:%S')}")
    print("-" * 50)
    
    services = {
        "Ollama": "http://localhost:11434/api/tags",
        "Local AI": "http://localhost:8001/health", 
        "Marketplace": "http://localhost:8080"
    }
    
    total_running = 0
    
    for service_name, url in services.items():
        try:
            response = requests.get(url, timeout=3)
            if response.status_code == 200:
                print(f"✅ {service_name}: Running (Status: {response.status_code})")
                total_running += 1
            else:
                print(f"⚠️  {service_name}: Responding but error (Status: {response.status_code})")
        except requests.RequestException:
            print(f"❌ {service_name}: Not responding")
        except Exception as e:
            print(f"❌ {service_name}: Error - {str(e)}")
    
    print("-" * 50)
    print(f"📊 Services Running: {total_running}/{len(services)}")
    
    if total_running == len(services):
        print("✅ All services are operational!")
        return True
    else:
        print("⚠️  Some services need attention")
        return False

if __name__ == "__main__":
    check_service_status()
