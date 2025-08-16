#!/usr/bin/env python3
"""
Final Integration Status Report
Comprehensive report on all integrations and their connectivity
"""

import json
import requests
import subprocess
import sys
from datetime import datetime
from pathlib import Path

class FinalIntegrationReport:
    """Generate final comprehensive integration report"""
    
    def __init__(self):
        self.report = {
            "timestamp": datetime.now().isoformat(),
            "overall_status": "unknown",
            "integrations": {},
            "summary": {},
            "recommendations": []
        }
    
    def check_service_integrations(self):
        """Check all service integrations"""
        print("🌐 Checking Service Integrations...")
        
        services = {
            "ollama": {
                "url": "http://localhost:11434/api/tags",
                "description": "Ollama AI Model Service",
                "critical": True
            },
            "local_ai": {
                "url": "http://localhost:8001/health", 
                "description": "Local AI Service API",
                "critical": True
            },
            "marketplace": {
                "url": "http://localhost:8080/health",
                "description": "Zero-Cost AI Marketplace",
                "critical": False
            },
            "marketplace_api": {
                "url": "http://localhost:8080/api/status",
                "description": "Marketplace API Endpoints",
                "critical": False
            }
        }
        
        for service_name, config in services.items():
            try:
                response = requests.get(config["url"], timeout=5)
                if response.status_code == 200:
                    self.report["integrations"][service_name] = {
                        "status": "connected",
                        "url": config["url"],
                        "description": config["description"],
                        "response_time": response.elapsed.total_seconds(),
                        "critical": config["critical"]
                    }
                    print(f"   ✅ {config['description']}: Connected")
                else:
                    self.report["integrations"][service_name] = {
                        "status": "error",
                        "url": config["url"],
                        "description": config["description"],
                        "error": f"HTTP {response.status_code}",
                        "critical": config["critical"]
                    }
                    print(f"   ⚠️  {config['description']}: Error {response.status_code}")
                    
            except requests.RequestException as e:
                self.report["integrations"][service_name] = {
                    "status": "disconnected",
                    "url": config["url"],
                    "description": config["description"],
                    "error": str(e),
                    "critical": config["critical"]
                }
                print(f"   ❌ {config['description']}: Disconnected")
    
    def check_agent_integrations(self):
        """Check agent module integrations"""
        print("\n🤖 Checking Agent Module Integrations...")
        
        agents = {
            "base_agent": {
                "module": "agents.base_agent",
                "class": "BaseAgent",
                "description": "Base Agent Framework"
            },
            "customer_request": {
                "module": "customer_request_agent", 
                "class": "CustomerRequestAgent",
                "description": "Customer Request Handler Agent"
            },
            "owl_integration": {
                "module": "owl_integration",
                "class": "MockOWLIntegration", 
                "description": "OWL Framework Integration"
            },
            "discovery_engine": {
                "module": "agent_discovery_engine",
                "class": "AgentDiscoveryEngine",
                "description": "Agent Discovery System"
            },
            "marketplace_engine": {
                "module": "marketplace_engine",
                "class": "MarketplaceEngine",
                "description": "Marketplace Engine"
            }
        }
        
        for agent_name, config in agents.items():
            try:
                # Try to import the module
                module = __import__(config["module"])
                if hasattr(module, config["class"]):
                    self.report["integrations"][f"agent_{agent_name}"] = {
                        "status": "available",
                        "module": config["module"],
                        "class": config["class"],
                        "description": config["description"]
                    }
                    print(f"   ✅ {config['description']}: Available")
                else:
                    self.report["integrations"][f"agent_{agent_name}"] = {
                        "status": "class_missing",
                        "module": config["module"],
                        "class": config["class"],
                        "description": config["description"],
                        "error": f"Class {config['class']} not found"
                    }
                    print(f"   ⚠️  {config['description']}: Class missing")
                    
            except ImportError as e:
                self.report["integrations"][f"agent_{agent_name}"] = {
                    "status": "import_error",
                    "module": config["module"],
                    "class": config["class"], 
                    "description": config["description"],
                    "error": str(e)
                }
                print(f"   ❌ {config['description']}: Import error")
    
    def check_file_integrations(self):
        """Check critical file integrations"""
        print("\n📁 Checking File System Integrations...")
        
        critical_files = {
            "main_requirements": {
                "path": "requirements.txt",
                "description": "Main Project Dependencies"
            },
            "integration_config": {
                "path": "integration_lab.toml",
                "description": "Integration Lab Configuration"
            },
            "agent_init": {
                "path": "agents/__init__.py",
                "description": "Agent Module Initialization"
            },
            "base_agent": {
                "path": "agents/base_agent.py", 
                "description": "Base Agent Implementation"
            },
            "local_ai_requirements": {
                "path": "local-ai-service/requirements.txt",
                "description": "Local AI Service Dependencies"
            },
            "marketplace_requirements": {
                "path": "zero-cost-ai-marketplace/requirements.txt",
                "description": "Marketplace Dependencies"
            }
        }
        
        for file_name, config in critical_files.items():
            file_path = Path(config["path"])
            if file_path.exists():
                self.report["integrations"][f"file_{file_name}"] = {
                    "status": "available",
                    "path": str(file_path),
                    "description": config["description"],
                    "size": file_path.stat().st_size if file_path.is_file() else "directory"
                }
                print(f"   ✅ {config['description']}: Available")
            else:
                self.report["integrations"][f"file_{file_name}"] = {
                    "status": "missing",
                    "path": str(file_path),
                    "description": config["description"],
                    "error": "File not found"
                }
                print(f"   ❌ {config['description']}: Missing")
    
    def generate_summary(self):
        """Generate integration summary"""
        total_integrations = len(self.report["integrations"])
        connected = sum(1 for i in self.report["integrations"].values() if i["status"] in ["connected", "available"])
        errors = sum(1 for i in self.report["integrations"].values() if i["status"] in ["error", "class_missing"])
        disconnected = sum(1 for i in self.report["integrations"].values() if i["status"] in ["disconnected", "import_error", "missing"])
        
        # Check critical services
        critical_issues = []
        for name, integration in self.report["integrations"].items():
            if integration.get("critical", False) and integration["status"] != "connected":
                critical_issues.append(name)
        
        self.report["summary"] = {
            "total_integrations": total_integrations,
            "connected_integrations": connected,
            "error_integrations": errors,
            "disconnected_integrations": disconnected,
            "success_rate": (connected / total_integrations * 100) if total_integrations > 0 else 0,
            "critical_issues": critical_issues
        }
        
        # Determine overall status
        if len(critical_issues) == 0 and connected >= total_integrations * 0.8:
            self.report["overall_status"] = "healthy"
        elif len(critical_issues) <= 1 and connected >= total_integrations * 0.6:
            self.report["overall_status"] = "minor_issues"
        else:
            self.report["overall_status"] = "needs_attention"
        
        # Generate recommendations
        if len(critical_issues) > 0:
            self.report["recommendations"].append(f"Fix critical services: {', '.join(critical_issues)}")
        
        if self.report["summary"]["success_rate"] < 80:
            self.report["recommendations"].append("Improve integration success rate by addressing disconnected services")
        
        if not self.report["recommendations"]:
            self.report["recommendations"].append("System integrations are healthy - consider regular monitoring")
    
    def print_report(self):
        """Print comprehensive integration report"""
        print("\n" + "=" * 80)
        print("🏁 COMPREHENSIVE INTEGRATION STATUS REPORT")
        print("=" * 80)
        
        status_emoji = {
            "healthy": "✅",
            "minor_issues": "⚠️ ",
            "needs_attention": "❌"
        }
        
        summary = self.report["summary"]
        print(f"{status_emoji.get(self.report['overall_status'], '❓')} Overall Status: {self.report['overall_status'].replace('_', ' ').title()}")
        print(f"📊 Integration Success Rate: {summary['success_rate']:.1f}%")
        print(f"🔗 Connected Integrations: {summary['connected_integrations']}/{summary['total_integrations']}")
        
        if summary['critical_issues']:
            print(f"\n🚨 Critical Issues ({len(summary['critical_issues'])}):")
            for issue in summary['critical_issues']:
                integration = self.report["integrations"][issue]
                print(f"   • {integration['description']}: {integration['status']}")
        
        print(f"\n📋 Integration Breakdown:")
        print(f"   ✅ Connected: {summary['connected_integrations']}")
        print(f"   ⚠️  Errors: {summary['error_integrations']}")
        print(f"   ❌ Disconnected: {summary['disconnected_integrations']}")
        
        if self.report["recommendations"]:
            print(f"\n💡 Recommendations:")
            for i, rec in enumerate(self.report["recommendations"], 1):
                print(f"   {i}. {rec}")
        
        print(f"\n📅 Report Generated: {self.report['timestamp']}")
        
        # Service URLs for quick access
        print(f"\n🔗 Service URLs:")
        for name, integration in self.report["integrations"].items():
            if "url" in integration and integration["status"] == "connected":
                print(f"   • {integration['description']}: {integration['url']}")
    
    def save_report(self):
        """Save report to file"""
        report_file = Path("final_integration_report.json")
        with open(report_file, 'w') as f:
            json.dump(self.report, f, indent=2)
        
        print(f"\n📁 Detailed report saved to: {report_file.absolute()}")
    
    def run_full_check(self):
        """Run complete integration check"""
        print("🚀 AI Agents Integration Lab - Final Status Check")
        print("=" * 80)
        
        # Add project root to Python path
        project_root = Path(__file__).parent
        if str(project_root) not in sys.path:
            sys.path.insert(0, str(project_root))
        
        self.check_service_integrations()
        self.check_agent_integrations() 
        self.check_file_integrations()
        self.generate_summary()
        self.print_report()
        self.save_report()
        
        return self.report["overall_status"] == "healthy"

def main():
    """Main function"""
    reporter = FinalIntegrationReport()
    success = reporter.run_full_check()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
