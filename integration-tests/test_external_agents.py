#!/usr/bin/env python3
"""
External Agent Integration Test Suite

This test suite validates the integration of external AI agents with our 
Multi-AI Agents framework, ensuring compatibility and quality standards.
"""

import asyncio
import json
import sys
import os
from datetime import datetime
from typing import Dict, Any, List

# Add project paths
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

class ExternalAgentTester:
    """Comprehensive tester for external agent integrations."""
    
    def __init__(self):
        self.test_results = {
            "timestamp": datetime.now().isoformat(),
            "tests_run": 0,
            "tests_passed": 0,
            "tests_failed": 0,
            "success_rate": 0.0,
            "details": []
        }
    
    def record_test(self, test_name: str, success: bool, details: str = ""):
        """Record a test result."""
        self.test_results["tests_run"] += 1
        if success:
            self.test_results["tests_passed"] += 1
            print(f"✅ {test_name}: PASSED")
        else:
            self.test_results["tests_failed"] += 1
            print(f"❌ {test_name}: FAILED - {details}")
        
        self.test_results["details"].append({
            "test": test_name,
            "status": "PASSED" if success else "FAILED",
            "details": details,
            "timestamp": datetime.now().isoformat()
        })
    
    async def test_owl_integration(self):
        """Test OWL framework integration."""
        print("\n🦉 Testing OWL Framework Integration")
        print("=" * 50)
        
        try:
            from owl_integration import owl_integration, OWL_AVAILABLE
            
            # Test 1: Import and status check
            status = owl_integration.get_status()
            self.record_test("OWL Framework Import", OWL_AVAILABLE, 
                           f"OWL Available: {status.get('owl_available')}")
            
            if not OWL_AVAILABLE:
                self.record_test("OWL Society Creation", False, "OWL not available")
                return False
            
            # Test 2: Create society
            society = owl_integration.create_society(
                task="Test task: Create a simple website plan",
                user_role_name="Client",
                assistant_role_name="WebDeveloper"
            )
            
            success = society is not None
            self.record_test("OWL Society Creation", success, 
                           "Society created successfully" if success else "Failed to create society")
            
            if success:
                # Test 3: Execute society
                result, history, tokens = owl_integration.run_society_sync(society, max_iterations=2)
                execution_success = len(result) > 0 and isinstance(tokens, dict)
                self.record_test("OWL Society Execution", execution_success,
                               f"Result length: {len(result)}, Tokens: {tokens}")
            
            return True
            
        except Exception as e:
            self.record_test("OWL Integration Test", False, str(e))
            return False
    
    async def test_base_agent_compatibility(self):
        """Test BaseAgent compatibility with external frameworks."""
        print("\n🤖 Testing BaseAgent Compatibility")
        print("=" * 50)
        
        try:
            from agents.base_agent import BaseAgent
            
            # Create test agent
            class TestAgent(BaseAgent):
                def get_capabilities(self):
                    return ["test_capability", "owl_integration"]
                
                async def process_task(self, task_data):
                    return {"status": "success", "result": "test completed"}
            
            agent = TestAgent(agent_id="test_agent", role_type="TestAgent")
            self.record_test("BaseAgent Creation", True, f"Agent ID: {agent.agent_id}")
            
            # Test OWL methods
            if hasattr(agent, 'owl_process_task'):
                task_result = await agent.owl_process_task("Test task")
                success = task_result.get('success', False)
                self.record_test("BaseAgent OWL Methods", success, 
                               f"Task result: {task_result.get('result', 'No result')[:100]}...")
            else:
                self.record_test("BaseAgent OWL Methods", False, "owl_process_task method not found")
            
            return True
            
        except Exception as e:
            self.record_test("BaseAgent Compatibility", False, str(e))
            return False
    
    async def test_agent_ecosystem(self):
        """Test the complete agent ecosystem."""
        print("\n🌐 Testing Agent Ecosystem")
        print("=" * 50)
        
        try:
            # Test agent imports
            agents_tested = 0
            agents_working = 0
            
            agent_modules = [
                ("Website Supervisor", "agents.website_agents.website_supervisor.supervisor", "WebsiteSupervisor"),
                ("Frontend Designer", "agents.website_agents.frontend_design.frontend_designer", "FrontendDesigner"),
                ("Backend Developer", "agents.website_agents.backend_developer.backend_developer", "BackendDeveloper"),
                ("API Integrator", "agents.website_agents.api_integration.api_integrator", "APIIntegrator"),
                ("E-commerce Specialist", "agents.website_agents.ecommerce_specialist.ecommerce_specialist", "EcommerceSpecialist")
            ]
            
            for agent_name, module_path, class_name in agent_modules:
                try:
                    module = __import__(module_path, fromlist=[class_name])
                    agent_class = getattr(module, class_name)
                    
                    # Try to instantiate
                    agent = agent_class(f"test_{agent_name.lower().replace(' ', '_')}")
                    capabilities = agent.get_capabilities() if hasattr(agent, 'get_capabilities') else []
                    
                    agents_tested += 1
                    agents_working += 1
                    
                    print(f"   ✅ {agent_name}: {len(capabilities)} capabilities")
                    
                except Exception as e:
                    agents_tested += 1
                    print(f"   ❌ {agent_name}: {str(e)}")
            
            success = agents_working >= 3  # At least 3 agents should work
            self.record_test("Agent Ecosystem Test", success, 
                           f"{agents_working}/{agents_tested} agents operational")
            
            return success
            
        except Exception as e:
            self.record_test("Agent Ecosystem Test", False, str(e))
            return False
    
    async def test_performance_benchmarks(self):
        """Test performance benchmarks."""
        print("\n📊 Testing Performance Benchmarks")
        print("=" * 50)
        
        try:
            import time
            
            # Test OWL response time
            if 'owl_integration' in sys.modules:
                from owl_integration import owl_integration
                
                start_time = time.time()
                society = owl_integration.create_society(
                    task="Quick test task",
                    user_role_name="User",
                    assistant_role_name="Assistant"
                )
                creation_time = time.time() - start_time
                
                success = creation_time < 5.0  # Should create society in under 5 seconds
                self.record_test("OWL Society Creation Performance", success,
                               f"Creation time: {creation_time:.2f}s")
            
            # Test memory usage (basic check)
            import psutil
            process = psutil.Process()
            memory_mb = process.memory_info().rss / 1024 / 1024
            
            memory_ok = memory_mb < 1000  # Less than 1GB
            self.record_test("Memory Usage", memory_ok, f"Memory usage: {memory_mb:.1f}MB")
            
            return True
            
        except ImportError:
            self.record_test("Performance Benchmarks", False, "psutil not available")
            return False
        except Exception as e:
            self.record_test("Performance Benchmarks", False, str(e))
            return False
    
    async def run_all_tests(self):
        """Run the complete test suite."""
        print("🚀 AI Agents Integration Test Suite")
        print("=" * 60)
        print(f"🕐 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Run all test categories
        await self.test_owl_integration()
        await self.test_base_agent_compatibility()
        await self.test_agent_ecosystem()
        await self.test_performance_benchmarks()
        
        # Calculate success rate
        if self.test_results["tests_run"] > 0:
            self.test_results["success_rate"] = (
                self.test_results["tests_passed"] / self.test_results["tests_run"]
            ) * 100
        
        # Final summary
        print("\n" + "=" * 60)
        print("🏁 INTEGRATION TEST SUMMARY")
        print("=" * 60)
        print(f"📊 Tests Run: {self.test_results['tests_run']}")
        print(f"✅ Tests Passed: {self.test_results['tests_passed']}")
        print(f"❌ Tests Failed: {self.test_results['tests_failed']}")
        print(f"📈 Success Rate: {self.test_results['success_rate']:.1f}%")
        
        if self.test_results["success_rate"] >= 80:
            print("\n🎉 INTEGRATION TEST: SUCCESS!")
            print("✅ External agent integration is ready for production")
        elif self.test_results["success_rate"] >= 60:
            print("\n⚠️ INTEGRATION TEST: PARTIAL SUCCESS")
            print("🔧 Some components need attention before production")
        else:
            print("\n❌ INTEGRATION TEST: NEEDS WORK")
            print("🛠️ Critical issues need to be resolved")
        
        return self.test_results["success_rate"] >= 80
    
    def save_results(self, filename: str = "integration_test_results.json"):
        """Save test results to JSON file."""
        results_path = os.path.join(
            os.path.dirname(__file__), "results", filename
        )
        
        # Create results directory if it doesn't exist
        os.makedirs(os.path.dirname(results_path), exist_ok=True)
        
        with open(results_path, 'w') as f:
            json.dump(self.test_results, f, indent=2)
        
        print(f"\n📁 Test results saved to: {results_path}")

async def main():
    """Main test runner."""
    tester = ExternalAgentTester()
    
    try:
        success = await tester.run_all_tests()
        tester.save_results()
        
        return success
        
    except KeyboardInterrupt:
        print("\n🛑 Test suite interrupted by user")
        return False
    except Exception as e:
        print(f"\n💥 Test suite failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
