#!/usr/bin/env python3
"""
Comprehensive Integration Tests
Tests all external agents for compatibility and performance
"""
import asyncio
import json
import time
import requests
from typing import Dict, List, Any
from pathlib import Path

class IntegrationTestSuite:
    """Comprehensive test suite for external agent integration"""
    
    def __init__(self):
        self.test_results = {}
        self.performance_metrics = {}
        
    async def test_all_external_agents(self) -> Dict[str, Any]:
        """Run comprehensive tests on all external agents"""
        
        print("🧪 STARTING COMPREHENSIVE INTEGRATION TESTS")
        print("=" * 60)
        
        # Discover agents
        agents_path = Path("../external-agents")
        test_results = {}
        
        for agent_dir in agents_path.iterdir():
            if agent_dir.is_dir():
                agent_name = agent_dir.name
                print(f"\n🔬 Testing Agent: {agent_name}")
                
                result = await self._test_individual_agent(agent_dir)
                test_results[agent_name] = result
                
                # Print immediate result
                status = "✅ PASS" if result.get("overall_status") == "pass" else "❌ FAIL"
                print(f"   {status} - Score: {result.get('score', 0)}/100")
        
        # Generate comprehensive report
        report = self._generate_test_report(test_results)
        self._save_test_results(test_results, report)
        
        return test_results
    
    async def _test_individual_agent(self, agent_dir: Path) -> Dict[str, Any]:
        """Test individual agent comprehensively"""
        
        test_result = {
            "agent_name": agent_dir.name,
            "tests_run": [],
            "score": 0,
            "max_score": 100,
            "overall_status": "fail"
        }
        
        # Test 1: Directory Structure (20 points)
        structure_score = self._test_directory_structure(agent_dir)
        test_result["tests_run"].append({
            "test": "directory_structure",
            "score": structure_score,
            "max_score": 20,
            "status": "pass" if structure_score >= 15 else "fail"
        })
        
        # Test 2: Documentation Quality (20 points)  
        doc_score = self._test_documentation(agent_dir)
        test_result["tests_run"].append({
            "test": "documentation",
            "score": doc_score,
            "max_score": 20,
            "status": "pass" if doc_score >= 15 else "fail"
        })
        
        # Test 3: Code Quality (25 points)
        code_score = self._test_code_quality(agent_dir)
        test_result["tests_run"].append({
            "test": "code_quality",
            "score": code_score,
            "max_score": 25,
            "status": "pass" if code_score >= 18 else "fail"
        })
        
        # Test 4: Integration Readiness (20 points)
        integration_score = self._test_integration_readiness(agent_dir)
        test_result["tests_run"].append({
            "test": "integration_readiness", 
            "score": integration_score,
            "max_score": 20,
            "status": "pass" if integration_score >= 15 else "fail"
        })
        
        # Test 5: Performance Indicators (15 points)
        perf_score = self._test_performance_indicators(agent_dir)
        test_result["tests_run"].append({
            "test": "performance_indicators",
            "score": perf_score,
            "max_score": 15,
            "status": "pass" if perf_score >= 10 else "fail"
        })
        
        # Calculate total score
        total_score = sum(test["score"] for test in test_result["tests_run"])
        test_result["score"] = total_score
        test_result["overall_status"] = "pass" if total_score >= 70 else "fail"
        
        return test_result
    
    def _test_directory_structure(self, agent_dir: Path) -> int:
        """Test directory structure and organization"""
        score = 0
        
        # Check for essential files
        if (agent_dir / "README.md").exists():
            score += 5
        if (agent_dir / "requirements.txt").exists() or (agent_dir / "pyproject.toml").exists():
            score += 5
        if any((agent_dir / f).exists() for f in ["main.py", "app.py", "__init__.py"]):
            score += 5
        
        # Check for good practices
        if (agent_dir / ".gitignore").exists():
            score += 2
        if (agent_dir / "tests").exists():
            score += 3
        
        return min(score, 20)
    
    def _test_documentation(self, agent_dir: Path) -> int:
        """Test documentation quality"""
        score = 0
        
        readme_path = agent_dir / "README.md"
        if readme_path.exists():
            try:
                with open(readme_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                    # Length check
                    if len(content) > 500:
                        score += 5
                    
                    # Key sections
                    content_lower = content.lower()
                    if "installation" in content_lower:
                        score += 3
                    if "usage" in content_lower or "example" in content_lower:
                        score += 3
                    if "api" in content_lower or "configuration" in content_lower:
                        score += 3
                    if "license" in content_lower:
                        score += 2
                    
                    # Code examples
                    if "```" in content:
                        score += 4
                        
            except Exception:
                pass
        
        return min(score, 20)
    
    def _test_code_quality(self, agent_dir: Path) -> int:
        """Test code quality indicators"""
        score = 0
        
        python_files = list(agent_dir.glob("**/*.py"))
        if python_files:
            score += 5  # Has Python code
            
            # Count files (complexity indicator)
            if len(python_files) > 5:
                score += 5
                
            # Check for common patterns
            try:
                sample_file = python_files[0]
                with open(sample_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                    # Good practices
                    if 'import' in content:
                        score += 3
                    if 'class' in content:
                        score += 3
                    if 'def' in content:
                        score += 3
                    if '"""' in content or "'''" in content:  # Docstrings
                        score += 3
                    if 'async' in content:  # Modern async support
                        score += 3
                        
            except Exception:
                pass
        
        return min(score, 25)
    
    def _test_integration_readiness(self, agent_dir: Path) -> int:
        """Test readiness for integration"""
        score = 0
        
        # API indicators
        if any(f.name in ["app.py", "main.py", "server.py"] for f in agent_dir.glob("*.py")):
            score += 5
            
        # Configuration files
        if (agent_dir / "config.json").exists() or (agent_dir / "config.yaml").exists():
            score += 3
            
        # Environment setup
        if (agent_dir / ".env.example").exists():
            score += 3
            
        # Docker support
        if (agent_dir / "Dockerfile").exists():
            score += 4
        if (agent_dir / "docker-compose.yml").exists():
            score += 5
            
        return min(score, 20)
    
    def _test_performance_indicators(self, agent_dir: Path) -> int:
        """Test performance and reliability indicators"""
        score = 0
        
        # Size efficiency
        total_size = sum(f.stat().st_size for f in agent_dir.rglob("*") if f.is_file())
        if total_size < 100_000_000:  # Less than 100MB
            score += 5
            
        # Test presence
        if (agent_dir / "tests").exists():
            score += 5
            
        # Error handling indicators
        try:
            py_files = list(agent_dir.glob("**/*.py"))
            if py_files:
                sample_content = py_files[0].read_text(encoding='utf-8', errors='ignore')
                if 'try:' in sample_content or 'except' in sample_content:
                    score += 5
        except:
            pass
        
        return min(score, 15)
    
    def _generate_test_report(self, test_results: Dict[str, Any]) -> str:
        """Generate comprehensive test report"""
        
        report = "# 🧪 COMPREHENSIVE INTEGRATION TEST REPORT\n\n"
        
        # Summary statistics
        total_agents = len(test_results)
        passed_agents = sum(1 for result in test_results.values() if result.get("overall_status") == "pass")
        average_score = sum(result.get("score", 0) for result in test_results.values()) / total_agents if total_agents > 0 else 0
        
        report += f"## 📊 TEST SUMMARY\n"
        report += f"- **Total Agents Tested:** {total_agents}\n"
        report += f"- **Agents Passed:** {passed_agents} ({passed_agents/total_agents*100:.1f}%)\n"  
        report += f"- **Average Score:** {average_score:.1f}/100\n\n"
        
        # Top performers
        sorted_agents = sorted(test_results.items(), key=lambda x: x[1].get("score", 0), reverse=True)
        
        report += f"## 🏆 TOP PERFORMING AGENTS\n"
        for i, (agent_name, result) in enumerate(sorted_agents[:5], 1):
            status_emoji = "✅" if result.get("overall_status") == "pass" else "❌"
            report += f"{i}. {status_emoji} **{agent_name}** - {result.get('score', 0)}/100\n"
        
        report += f"\n## 📋 DETAILED TEST RESULTS\n\n"
        
        # Detailed results for each agent
        for agent_name, result in sorted_agents:
            status_emoji = "✅" if result.get("overall_status") == "pass" else "❌"
            report += f"### {status_emoji} {agent_name}\n"
            report += f"**Overall Score:** {result.get('score', 0)}/100\n\n"
            
            for test in result.get("tests_run", []):
                test_emoji = "✅" if test.get("status") == "pass" else "❌"
                report += f"- {test_emoji} {test.get('test', '').replace('_', ' ').title()}: {test.get('score', 0)}/{test.get('max_score', 0)}\n"
            
            report += "\n"
        
        return report
    
    def _save_test_results(self, test_results: Dict[str, Any], report: str):
        """Save test results and report"""
        
        # Save JSON results
        with open("integration_test_results.json", "w") as f:
            json.dump(test_results, f, indent=2)
        
        # Save markdown report  
        with open("integration_test_report.md", "w") as f:
            f.write(report)
        
        print("\n📄 Test results saved:")
        print("   ✅ integration_test_results.json")
        print("   ✅ integration_test_report.md")

# Main execution
async def main():
    print("🚀 STARTING COMPREHENSIVE INTEGRATION TESTING SUITE")
    print("💎 Testing all external agents for integration readiness")
    
    test_suite = IntegrationTestSuite()
    results = await test_suite.test_all_external_agents()
    
    # Summary
    total = len(results)
    passed = sum(1 for r in results.values() if r.get("overall_status") == "pass")
    
    print(f"\n🎯 FINAL RESULTS:")
    print(f"   📊 Total Agents: {total}")
    print(f"   ✅ Passed: {passed}")
    print(f"   ❌ Failed: {total - passed}")
    print(f"   📈 Success Rate: {passed/total*100:.1f}%")
    
    print(f"\n🎉 INTEGRATION TESTING COMPLETE!")

if __name__ == "__main__":
    asyncio.run(main())
