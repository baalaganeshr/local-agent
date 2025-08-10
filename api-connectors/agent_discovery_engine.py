#!/usr/bin/env python3
"""
Agent Discovery Engine
Automatically discovers and catalogs external agents
"""
import os
import json
import requests
from pathlib import Path
from typing import List, Dict, Any

class AgentDiscoveryEngine:
    """Discovers and catalogs available agents"""
    
    def __init__(self, external_agents_path: str = "../external-agents"):
        self.external_agents_path = Path(external_agents_path)
        self.discovered_agents = []
        
    def scan_external_agents(self) -> List[Dict[str, Any]]:
        """Scan external-agents directory and catalog all agents"""
        agents = []
        
        for agent_dir in self.external_agents_path.iterdir():
            if agent_dir.is_dir() and not agent_dir.name.startswith('.'):
                agent_info = self._analyze_agent_directory(agent_dir)
                if agent_info:
                    agents.append(agent_info)
        
        self.discovered_agents = agents
        return agents
    
    def _analyze_agent_directory(self, agent_dir: Path) -> Dict[str, Any]:
        """Analyze individual agent directory"""
        try:
            # Check for key files
            has_readme = (agent_dir / "README.md").exists()
            has_requirements = (agent_dir / "requirements.txt").exists() or (agent_dir / "pyproject.toml").exists()
            has_main = any((agent_dir / f).exists() for f in ["main.py", "app.py", "__init__.py"])
            
            # Extract metadata
            metadata = {
                "name": agent_dir.name,
                "path": str(agent_dir),
                "has_readme": has_readme,
                "has_requirements": has_requirements,
                "has_main": has_main,
                "language": self._detect_language(agent_dir),
                "capabilities": self._extract_capabilities(agent_dir),
                "integration_complexity": self._assess_complexity(agent_dir),
                "stars": self._get_github_stars(agent_dir),
                "last_updated": self._get_last_updated(agent_dir)
            }
            
            return metadata
            
        except Exception as e:
            print(f"Error analyzing {agent_dir.name}: {e}")
            return None
    
    def _detect_language(self, agent_dir: Path) -> str:
        """Detect primary programming language"""
        if list(agent_dir.glob("*.py")):
            return "python"
        elif list(agent_dir.glob("*.js")) or (agent_dir / "package.json").exists():
            return "javascript"
        elif list(agent_dir.glob("*.go")):
            return "go"
        else:
            return "unknown"
    
    def _extract_capabilities(self, agent_dir: Path) -> List[str]:
        """Extract agent capabilities from README or code"""
        capabilities = []
        
        readme_path = agent_dir / "README.md"
        if readme_path.exists():
            try:
                with open(readme_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read().lower()
                    
                    # Look for capability keywords
                    capability_keywords = [
                        "whatsapp", "telegram", "discord", "slack", "messaging",
                        "lead generation", "sales", "crm", "marketing",
                        "social media", "twitter", "linkedin", "instagram",
                        "testing", "qa", "automation", "playwright", "selenium",
                        "payment", "stripe", "paypal", "billing",
                        "web scraping", "data extraction", "crawling",
                        "ai", "llm", "gpt", "claude", "openai", "anthropic"
                    ]
                    
                    for keyword in capability_keywords:
                        if keyword in content:
                            capabilities.append(keyword)
            
            except Exception:
                pass
        
        return capabilities
    
    def _assess_complexity(self, agent_dir: Path) -> str:
        """Assess integration complexity"""
        score = 0
        
        # Simple factors
        if (agent_dir / "requirements.txt").exists():
            score += 1
        if (agent_dir / "setup.py").exists() or (agent_dir / "pyproject.toml").exists():
            score += 2
        if (agent_dir / "docker-compose.yml").exists() or (agent_dir / "Dockerfile").exists():
            score += 1
        
        # Count Python files (complexity indicator)
        py_files = len(list(agent_dir.glob("**/*.py")))
        if py_files > 50:
            score += 3
        elif py_files > 10:
            score += 2
        else:
            score += 1
        
        if score <= 3:
            return "simple"
        elif score <= 6:
            return "medium"
        else:
            return "complex"
    
    def _get_github_stars(self, agent_dir: Path) -> int:
        """Get GitHub stars (if available)"""
        # This would require GitHub API integration
        return 0
    
    def _get_last_updated(self, agent_dir: Path) -> str:
        """Get last updated timestamp"""
        try:
            return str(os.path.getmtime(agent_dir))
        except:
            return "unknown"
    
    def generate_integration_report(self) -> str:
        """Generate comprehensive integration report"""
        if not self.discovered_agents:
            self.scan_external_agents()
        
        report = "# 🎯 AI AGENT INTEGRATION DISCOVERY REPORT\n\n"
        report += f"## 📊 SUMMARY\n"
        report += f"- **Total Agents Discovered:** {len(self.discovered_agents)}\n"
        
        # Group by complexity
        complexity_groups = {}
        for agent in self.discovered_agents:
            complexity = agent.get('integration_complexity', 'unknown')
            if complexity not in complexity_groups:
                complexity_groups[complexity] = []
            complexity_groups[complexity].append(agent)
        
        for complexity, agents in complexity_groups.items():
            report += f"- **{complexity.title()} Integration:** {len(agents)} agents\n"
        
        report += "\n## 🎮 DETAILED AGENT ANALYSIS\n\n"
        
        for agent in sorted(self.discovered_agents, key=lambda x: x.get('integration_complexity', 'zz')):
            report += f"### {agent['name']}\n"
            report += f"- **Language:** {agent['language']}\n"
            report += f"- **Complexity:** {agent['integration_complexity']}\n"
            report += f"- **Capabilities:** {', '.join(agent['capabilities'][:5])}\n"
            report += f"- **Ready for Integration:** {'✅' if agent['has_main'] and agent['has_requirements'] else '⚠️'}\n\n"
        
        return report
    
    def save_discovery_report(self, filename: str = "agent_discovery_report.md"):
        """Save discovery report to file"""
        report = self.generate_integration_report()
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
        
        # Also save JSON data
        json_filename = filename.replace('.md', '.json')
        with open(json_filename, 'w') as f:
            json.dump(self.discovered_agents, f, indent=2)
        
        print(f"✅ Discovery report saved: {filename}")
        print(f"✅ JSON data saved: {json_filename}")

if __name__ == "__main__":
    engine = AgentDiscoveryEngine()
    agents = engine.scan_external_agents()
    print(f"🔍 Discovered {len(agents)} agents!")
    engine.save_discovery_report()
