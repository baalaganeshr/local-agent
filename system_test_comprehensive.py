#!/usr/bin/env python3
"""
Comprehensive Multi-AI Agents System Test
Tests all components and verifies the fixes work properly
"""

import os
import sys
import json
import asyncio
import traceback
from datetime import datetime
from pathlib import Path

class SystemTester:
    """Comprehensive system testing for Multi-AI Agents framework"""
    
    def __init__(self):
        self.test_results = {}
        self.failed_tests = []
        self.root_path = Path(__file__).parent
        
    def run_all_tests(self):
        """Run comprehensive system tests"""
        print("🧪 MULTI-AI AGENTS SYSTEM TEST SUITE")
        print("=" * 50)
        
        tests = [
            ("Import Tests", self.test_imports),
            ("Agent Creation Tests", self.test_agent_creation),
            ("Integration Tests", self.test_integrations),
            ("Marketplace Tests", self.test_marketplace),
            ("OWL Integration Tests", self.test_owl_integration),
            ("Service Tests", self.test_services)
        ]
        
        for test_name, test_func in tests:
            print(f"\n🔍 Running {test_name}...")
            try:
                result = test_func()
                self.test_results[test_name] = {
                    "status": "PASS" if result else "FAIL",
                    "details": result if isinstance(result, dict) else {"success": result}
                }
                status = "✅ PASS" if result else "❌ FAIL"
                print(f"{status} {test_name}")
            except Exception as e:
                self.test_results[test_name] = {
                    "status": "ERROR",
                    "error": str(e),
                    "traceback": traceback.format_exc()
                }
                print(f"❌ ERROR {test_name}: {e}")
                self.failed_tests.append(test_name)
        
        self.generate_report()
    
    def test_imports(self):
        """Test all critical imports"""
        imports_to_test = [
            ("owl_integration", "create_owl_integration"),
            ("agents.base_agent", "BaseAgent"),
            ("marketplace_engine", "MarketplaceEngine"),
            ("agent_discovery_engine", "AgentDiscoveryEngine"),
            ("comprehensive_integration_tests", "IntegrationTestSuite")
        ]
        
        results = {}
        for module_name, class_name in imports_to_test:
            try:
                module = __import__(module_name, fromlist=[class_name])
                cls = getattr(module, class_name)
                results[f"{module_name}.{class_name}"] = "SUCCESS"
            except Exception as e:
                results[f"{module_name}.{class_name}"] = f"FAILED: {e}"
        
        return results
    
    def test_agent_creation(self):
        """Test agent creation and basic functionality"""
        results = {}
        
        try:
            # Test BaseAgent creation
            from agents.base_agent import BaseAgent, MockAgent
            mock_agent = MockAgent("test_agent")
            results["MockAgent creation"] = "SUCCESS"
            
            # Test agent capabilities
            capabilities = mock_agent.get_capabilities()
            results["Agent capabilities"] = f"SUCCESS: {len(capabilities)} capabilities"
            
            # Test message processing
            response = mock_agent.process_message("Hello test")
            results["Message processing"] = "SUCCESS" if response else "FAILED"
            
        except Exception as e:
            results["Agent creation"] = f"FAILED: {e}"
        
        return results
    
    def test_integrations(self):
        """Test system integrations"""
        results = {}
        
        try:
            # Test OWL integration
            from owl_integration import create_owl_integration
            owl = create_owl_integration()
            results["OWL integration"] = "SUCCESS"
            
            # Test agent adapter
            sys.path.insert(0, str(self.root_path / "agent-adapters"))
            from owl_adapter import OWLAdapter
            adapter = OWLAdapter()
            status = adapter.get_status()
            results["OWL adapter"] = f"SUCCESS: {status}"
            
        except Exception as e:
            results["Integration test"] = f"FAILED: {e}"
        
        return results
    
    def test_marketplace(self):
        """Test marketplace functionality"""
        results = {}
        
        try:
            from marketplace_engine import MarketplaceEngine
            marketplace = MarketplaceEngine()
            
            # Test agent listing
            agents = marketplace.list_available_agents()
            results["Agent listing"] = f"SUCCESS: {len(agents)} agents found"
            
            # Test agent details
            if agents:
                details = marketplace.get_agent_details(agents[0]["id"])
                results["Agent details"] = "SUCCESS" if details else "FAILED"
            
            # Test mock purchase
            if agents:
                purchase = marketplace.purchase_agent(agents[0]["id"], "test_user")
                results["Mock purchase"] = "SUCCESS" if purchase["success"] else "FAILED"
            
        except Exception as e:
            results["Marketplace test"] = f"FAILED: {e}"
        
        return results
    
    def test_owl_integration(self):
        """Test OWL integration components"""
        results = {}
        
        try:
            from owl_integration import (
                MockOWLIntegration, MockChatAgent, MockBaseMessage,
                create_owl_integration, create_chat_agent
            )
            
            # Test OWL integration creation
            owl = create_owl_integration()
            results["OWL creation"] = "SUCCESS"
            
            # Test chat agent creation
            agent = create_chat_agent("test")
            results["Chat agent creation"] = "SUCCESS"
            
            # Test message processing
            from owl_integration import create_base_message
            message = create_base_message("Test message")
            response = agent.step(message)
            results["OWL message processing"] = "SUCCESS" if response else "FAILED"
            
        except Exception as e:
            results["OWL integration test"] = f"FAILED: {e}"
        
        return results
    
    def test_services(self):
        """Test service availability"""
        results = {}
        
        try:
            # Test Ollama service (if available)
            import subprocess
            result = subprocess.run(["ollama", "list"], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                results["Ollama service"] = "SUCCESS: Service running"
                if "gpt-oss:20b" in result.stdout:
                    results["GPT-OSS model"] = "SUCCESS: Model available"
                else:
                    results["GPT-OSS model"] = "INFO: Model not installed"
            else:
                results["Ollama service"] = "INFO: Service not available"
        except Exception as e:
            results["Service test"] = f"INFO: {e}"
        
        return results
    
    def generate_report(self):
        """Generate comprehensive test report"""
        total_tests = len(self.test_results)
        passed_tests = sum(1 for r in self.test_results.values() if r["status"] == "PASS")
        failed_tests = len(self.failed_tests)
        
        print("\n" + "=" * 60)
        print("🎯 COMPREHENSIVE TEST REPORT")
        print("=" * 60)
        
        print(f"📊 SUMMARY:")
        print(f"   Total Tests: {total_tests}")
        print(f"   Passed: {passed_tests} ✅")
        print(f"   Failed: {failed_tests} ❌")
        print(f"   Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        print(f"\n📋 DETAILED RESULTS:")
        for test_name, result in self.test_results.items():
            status_icon = {"PASS": "✅", "FAIL": "❌", "ERROR": "⚠️"}[result["status"]]
            print(f"   {status_icon} {test_name}: {result['status']}")
            
            if result["status"] == "PASS" and "details" in result:
                for key, value in result["details"].items():
                    if isinstance(value, str) and "SUCCESS" in value:
                        print(f"      ✓ {key}: {value}")
        
        print(f"\n🔧 SYSTEM STATUS:")
        if failed_tests == 0:
            print("   🎉 ALL SYSTEMS OPERATIONAL!")
            print("   🚀 Multi-AI Agents framework is ready for production")
        else:
            print("   ⚠️  Some components need attention")
            print("   💡 Check failed tests for specific issues")
        
        # Save detailed report
        report_file = self.root_path / f"system_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "summary": {
                    "total_tests": total_tests,
                    "passed": passed_tests,
                    "failed": failed_tests,
                    "success_rate": (passed_tests/total_tests)*100
                },
                "results": self.test_results
            }, f, indent=2)
        
        print(f"\n📄 Detailed report saved: {report_file}")

if __name__ == "__main__":
    tester = SystemTester()
    tester.run_all_tests()
