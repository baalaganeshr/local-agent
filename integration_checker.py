#!/usr/bin/env python3
"""
Comprehensive Integration Checker
Checks all integrations, connections, and system health
"""

import subprocess
import sys
import requests
import json
import psutil
import os
from datetime import datetime
from typing import Dict, List, Any, Tuple
from pathlib import Path

class IntegrationChecker:
    """Comprehensive system integration checker"""
    
    def __init__(self):
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "checks": {},
            "overall_status": "unknown",
            "issues": [],
            "recommendations": []
        }
        
    def check_python_environment(self) -> Dict[str, Any]:
        """Check Python environment and packages"""
        print("🐍 Checking Python Environment...")
        
        try:
            python_version = sys.version
            pip_packages = self._get_installed_packages()
            
            required_packages = [
                "fastapi", "uvicorn", "requests", "pandas", 
                "numpy", "httpx", "pytest", "psutil", "structlog"
            ]
            
            missing_packages = []
            for pkg in required_packages:
                if pkg not in pip_packages:
                    missing_packages.append(pkg)
            
            result = {
                "status": "healthy" if not missing_packages else "issues",
                "python_version": python_version.split()[0],
                "total_packages": len(pip_packages),
                "missing_packages": missing_packages,
                "required_packages_installed": len(required_packages) - len(missing_packages)
            }
            
            if missing_packages:
                self.results["issues"].append(f"Missing packages: {', '.join(missing_packages)}")
                self.results["recommendations"].append("Install missing packages with: pip install " + " ".join(missing_packages))
            
            print(f"   ✅ Python {result['python_version']} with {result['total_packages']} packages")
            if missing_packages:
                print(f"   ❌ Missing: {', '.join(missing_packages)}")
            
            return result
            
        except Exception as e:
            print(f"   ❌ Error checking Python environment: {e}")
            return {"status": "error", "error": str(e)}
    
    def check_services(self) -> Dict[str, Any]:
        """Check if required services are running"""
        print("🌐 Checking Services...")
        
        services = {
            "ollama": "http://localhost:11434/api/tags",
            "local_ai": "http://localhost:8001/health", 
            "frontend": "http://localhost:8080",
            "marketplace": "http://localhost:8001/marketplace/health"
        }
        
        service_status = {}
        
        for service_name, url in services.items():
            try:
                response = requests.get(url, timeout=5)
                service_status[service_name] = {
                    "status": "running",
                    "response_code": response.status_code,
                    "url": url
                }
                print(f"   ✅ {service_name}: Running")
                
            except requests.RequestException:
                service_status[service_name] = {
                    "status": "not_running",
                    "url": url
                }
                print(f"   ❌ {service_name}: Not running")
                self.results["issues"].append(f"{service_name} service is not running")
        
        # Check system processes for Ollama
        ollama_processes = [p for p in psutil.process_iter() if 'ollama' in p.name().lower()]
        if ollama_processes and service_status.get("ollama", {}).get("status") == "not_running":
            print("   ⚠️  Ollama process found but service not responding")
            
        return {
            "services": service_status,
            "total_services": len(services),
            "running_services": sum(1 for s in service_status.values() if s["status"] == "running")
        }
    
    def check_agent_modules(self) -> Dict[str, Any]:
        """Check agent module imports and functionality"""
        print("🤖 Checking Agent Modules...")
        
        modules_to_check = [
            ("agents.base_agent", "BaseAgent"),
            ("owl_integration", "MockOWLIntegration"),
            ("agent_discovery_engine", "AgentDiscoveryEngine"),
            ("customer_request_agent", "CustomerRequestAgent"),
            ("marketplace_engine", "MarketplaceEngine")
        ]
        
        module_status = {}
        
        for module_name, class_name in modules_to_check:
            try:
                # Add current directory to path for imports
                current_dir = Path(__file__).parent
                if str(current_dir) not in sys.path:
                    sys.path.insert(0, str(current_dir))
                
                __import__(module_name)
                module_status[module_name] = {
                    "status": "importable",
                    "class": class_name
                }
                print(f"   ✅ {module_name}: Importable")
                
            except ImportError as e:
                module_status[module_name] = {
                    "status": "import_error",
                    "error": str(e)
                }
                print(f"   ❌ {module_name}: Import error - {e}")
                self.results["issues"].append(f"Module {module_name} has import issues")
        
        return {
            "modules": module_status,
            "total_modules": len(modules_to_check),
            "working_modules": sum(1 for s in module_status.values() if s["status"] == "importable")
        }
    
    def check_file_structure(self) -> Dict[str, Any]:
        """Check critical file structure"""
        print("📁 Checking File Structure...")
        
        critical_files = [
            "requirements.txt",
            "agents/__init__.py",
            "agents/base_agent.py",
            "local-ai-service/requirements.txt",
            "zero-cost-ai-marketplace/requirements.txt",
            "integration_lab.toml"
        ]
        
        file_status = {}
        
        for file_path in critical_files:
            full_path = Path(file_path)
            if full_path.exists():
                file_status[file_path] = {
                    "status": "exists",
                    "size": full_path.stat().st_size if full_path.is_file() else "directory"
                }
                print(f"   ✅ {file_path}: Exists")
            else:
                file_status[file_path] = {"status": "missing"}
                print(f"   ❌ {file_path}: Missing")
                self.results["issues"].append(f"Critical file missing: {file_path}")
        
        return {
            "files": file_status,
            "total_files": len(critical_files),
            "existing_files": sum(1 for s in file_status.values() if s["status"] == "exists")
        }
    
    def check_system_resources(self) -> Dict[str, Any]:
        """Check system resources"""
        print("💻 Checking System Resources...")
        
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('.')
            
            result = {
                "cpu_usage": cpu_percent,
                "memory_usage": {
                    "total": memory.total // (1024**3),  # GB
                    "available": memory.available // (1024**3),  # GB
                    "percent": memory.percent
                },
                "disk_usage": {
                    "total": disk.total // (1024**3),  # GB
                    "free": disk.free // (1024**3),  # GB
                    "percent": (disk.used / disk.total) * 100
                }
            }
            
            print(f"   ✅ CPU: {cpu_percent:.1f}%")
            print(f"   ✅ Memory: {memory.percent:.1f}% used ({memory.available // (1024**3)}GB available)")
            print(f"   ✅ Disk: {result['disk_usage']['percent']:.1f}% used ({result['disk_usage']['free']}GB free)")
            
            # Add warnings for high resource usage
            if cpu_percent > 80:
                self.results["issues"].append("High CPU usage detected")
            if memory.percent > 85:
                self.results["issues"].append("High memory usage detected")
            if result['disk_usage']['percent'] > 90:
                self.results["issues"].append("Low disk space")
                
            return result
            
        except Exception as e:
            print(f"   ❌ Error checking system resources: {e}")
            return {"status": "error", "error": str(e)}
    
    def _get_installed_packages(self) -> List[str]:
        """Get list of installed Python packages"""
        try:
            result = subprocess.run([sys.executable, "-m", "pip", "list"], 
                                  capture_output=True, text=True, check=True)
            lines = result.stdout.strip().split('\n')[2:]  # Skip header lines
            return [line.split()[0].lower() for line in lines if line.strip()]
        except:
            return []
    
    def run_all_checks(self) -> Dict[str, Any]:
        """Run all integration checks"""
        print("🚀 Starting Comprehensive Integration Check")
        print("=" * 60)
        
        # Run all checks
        self.results["checks"]["python_environment"] = self.check_python_environment()
        self.results["checks"]["services"] = self.check_services()
        self.results["checks"]["agent_modules"] = self.check_agent_modules()
        self.results["checks"]["file_structure"] = self.check_file_structure()
        self.results["checks"]["system_resources"] = self.check_system_resources()
        
        # Determine overall status
        total_issues = len(self.results["issues"])
        if total_issues == 0:
            self.results["overall_status"] = "healthy"
        elif total_issues <= 3:
            self.results["overall_status"] = "minor_issues"
        else:
            self.results["overall_status"] = "needs_attention"
        
        # Generate recommendations
        if not self.results["recommendations"]:
            if self.results["overall_status"] == "healthy":
                self.results["recommendations"].append("System is healthy - consider running regular checks")
            else:
                self.results["recommendations"].append("Address the issues listed above for optimal performance")
        
        return self.results
    
    def print_summary(self):
        """Print a summary of all checks"""
        print("\n" + "=" * 60)
        print("🏁 INTEGRATION CHECK SUMMARY")
        print("=" * 60)
        
        status_emoji = {
            "healthy": "✅",
            "minor_issues": "⚠️ ",
            "needs_attention": "❌"
        }
        
        print(f"{status_emoji.get(self.results['overall_status'], '❓')} Overall Status: {self.results['overall_status'].replace('_', ' ').title()}")
        print(f"📊 Total Issues Found: {len(self.results['issues'])}")
        
        if self.results["issues"]:
            print("\n🚨 Issues Found:")
            for i, issue in enumerate(self.results["issues"], 1):
                print(f"   {i}. {issue}")
        
        if self.results["recommendations"]:
            print("\n💡 Recommendations:")
            for i, rec in enumerate(self.results["recommendations"], 1):
                print(f"   {i}. {rec}")
        
        print(f"\n📅 Check completed at: {self.results['timestamp']}")

def main():
    """Main function to run integration checks"""
    checker = IntegrationChecker()
    results = checker.run_all_checks()
    checker.print_summary()
    
    # Save results to file
    results_file = Path("integration_check_results.json")
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📁 Detailed results saved to: {results_file.absolute()}")
    
    return 0 if results["overall_status"] == "healthy" else 1

if __name__ == "__main__":
    sys.exit(main())
