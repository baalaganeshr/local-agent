#!/usr/bin/env python3
"""
AI Agents Marketplace Engine
The business logic for our AI agent marketplace
"""
import json
from datetime import datetime
from typing import Dict, List, Any
from dataclasses import dataclass, asdict
from enum import Enum

class AgentStatus(Enum):
    ACTIVE = "active"
    TESTING = "testing"  
    DEPRECATED = "deprecated"
    PREMIUM = "premium"

@dataclass
class MarketplaceAgent:
    name: str
    description: str
    category: str
    price_tier: str  # free, basic, premium, enterprise
    capabilities: List[str]
    integration_complexity: str
    test_score: int
    status: AgentStatus
    downloads: int = 0
    rating: float = 0.0
    reviews: List[str] = None
    last_updated: str = None
    
    def __post_init__(self):
        if self.reviews is None:
            self.reviews = []
        if self.last_updated is None:
            self.last_updated = datetime.now().isoformat()

class MarketplaceEngine:
    """Core marketplace functionality"""
    
    def __init__(self):
        self.agents_catalog = {}
        self.user_installations = {}
        self.revenue_metrics = {
            "total_revenue": 0,
            "monthly_active_agents": 0,
            "customer_count": 0
        }
    
    def add_agent_to_marketplace(self, agent: MarketplaceAgent) -> bool:
        """Add agent to marketplace catalog"""
        try:
            # Validate agent meets marketplace standards
            if self._validate_marketplace_agent(agent):
                self.agents_catalog[agent.name] = agent
                print(f"✅ Added to marketplace: {agent.name}")
                return True
            else:
                print(f"❌ Agent failed validation: {agent.name}")
                return False
        except Exception as e:
            print(f"❌ Error adding agent {agent.name}: {e}")
            return False
    
    def _validate_marketplace_agent(self, agent: MarketplaceAgent) -> bool:
        """Validate agent meets marketplace quality standards"""
        
        # Minimum test score requirement
        if agent.test_score < 70:
            return False
            
        # Must have description and capabilities
        if not agent.description or not agent.capabilities:
            return False
            
        # Category must be valid
        valid_categories = [
            "messaging", "sales", "social", "testing", 
            "payment", "control", "analytics", "content"
        ]
        if agent.category not in valid_categories:
            return False
            
        return True
    
    def search_agents(self, query: str = "", category: str = "", price_tier: str = "") -> List[MarketplaceAgent]:
        """Search agents in marketplace"""
        results = []
        
        for agent in self.agents_catalog.values():
            # Category filter
            if category and agent.category != category:
                continue
                
            # Price tier filter  
            if price_tier and agent.price_tier != price_tier:
                continue
                
            # Text search in name, description, capabilities
            if query:
                search_text = f"{agent.name} {agent.description} {' '.join(agent.capabilities)}".lower()
                if query.lower() not in search_text:
                    continue
            
            results.append(agent)
        
        # Sort by rating and downloads
        results.sort(key=lambda x: (x.rating, x.downloads), reverse=True)
        return results
    
    def get_agent_details(self, agent_name: str) -> Dict[str, Any]:
        """Get detailed information about specific agent"""
        if agent_name in self.agents_catalog:
            agent = self.agents_catalog[agent_name]
            return {
                **asdict(agent),
                "integration_guide": self._generate_integration_guide(agent),
                "pricing": self._get_agent_pricing(agent),
                "similar_agents": self._find_similar_agents(agent)[:3]
            }
        return {}
    
    def _generate_integration_guide(self, agent: MarketplaceAgent) -> Dict[str, str]:
        """Generate integration guide for agent"""
        complexity_guides = {
            "simple": "Ready to use with minimal configuration. Just install and run!",
            "medium": "Requires some setup and configuration. Follow our step-by-step guide.",
            "complex": "Advanced integration. Recommended for technical teams with Docker experience."
        }
        
        return {
            "complexity_level": agent.integration_complexity,
            "guide": complexity_guides.get(agent.integration_complexity, "Contact support for guidance"),
            "estimated_setup_time": self._estimate_setup_time(agent.integration_complexity),
            "requirements": self._get_integration_requirements(agent)
        }
    
    def _estimate_setup_time(self, complexity: str) -> str:
        time_estimates = {
            "simple": "5-15 minutes",
            "medium": "30-60 minutes", 
            "complex": "2-4 hours"
        }
        return time_estimates.get(complexity, "Variable")
    
    def _get_integration_requirements(self, agent: MarketplaceAgent) -> List[str]:
        """Get integration requirements based on agent"""
        base_requirements = ["Docker", "Python 3.11+", "OWL Framework"]
        
        if agent.category == "messaging":
            base_requirements.append("WhatsApp Business API Key")
        elif agent.category == "social":
            base_requirements.append("Social Media API Keys")
        elif agent.category == "payment":
            base_requirements.append("Payment Gateway API Keys")
            
        return base_requirements
    
    def _get_agent_pricing(self, agent: MarketplaceAgent) -> Dict[str, Any]:
        """Get pricing information for agent"""
        pricing_tiers = {
            "free": {"price": 0, "description": "Free for personal use", "limits": "1000 operations/month"},
            "basic": {"price": 29, "description": "Perfect for small businesses", "limits": "10,000 operations/month"},
            "premium": {"price": 99, "description": "For growing companies", "limits": "100,000 operations/month"},
            "enterprise": {"price": 299, "description": "Unlimited for large organizations", "limits": "Unlimited operations"}
        }
        
        return pricing_tiers.get(agent.price_tier, pricing_tiers["free"])
    
    def _find_similar_agents(self, agent: MarketplaceAgent) -> List[str]:
        """Find similar agents based on category and capabilities"""
        similar = []
        
        for name, other_agent in self.agents_catalog.items():
            if name == agent.name:
                continue
                
            # Same category gets priority
            if other_agent.category == agent.category:
                similar.append(name)
            # Similar capabilities
            elif any(cap in other_agent.capabilities for cap in agent.capabilities):
                similar.append(name)
        
        return similar
    
    def generate_marketplace_stats(self) -> Dict[str, Any]:
        """Generate marketplace statistics"""
        if not self.agents_catalog:
            return {"error": "No agents in marketplace"}
        
        # Category distribution
        category_stats = {}
        for agent in self.agents_catalog.values():
            category_stats[agent.category] = category_stats.get(agent.category, 0) + 1
        
        # Price tier distribution
        price_stats = {}
        for agent in self.agents_catalog.values():
            price_stats[agent.price_tier] = price_stats.get(agent.price_tier, 0) + 1
        
        # Quality metrics
        test_scores = [agent.test_score for agent in self.agents_catalog.values()]
        avg_quality = sum(test_scores) / len(test_scores) if test_scores else 0
        
        return {
            "total_agents": len(self.agents_catalog),
            "categories": category_stats,
            "price_tiers": price_stats,
            "average_quality_score": round(avg_quality, 1),
            "high_quality_agents": len([s for s in test_scores if s >= 80]),
            "revenue_potential": sum(
                self._get_agent_pricing(agent)["price"] 
                for agent in self.agents_catalog.values()
            ),
            "last_updated": datetime.now().isoformat()
        }

# Example usage and testing
def create_sample_marketplace():
    """Create sample marketplace with test agents"""
    marketplace = MarketplaceEngine()
    
    # Add sample agents
    sample_agents = [
        MarketplaceAgent(
            name="evolution-whatsapp", 
            description="Complete WhatsApp Business solution with multi-channel support",
            category="messaging",
            price_tier="basic",
            capabilities=["whatsapp", "messaging", "automation", "api"],
            integration_complexity="medium",
            test_score=85,
            status=AgentStatus.ACTIVE,
            rating=4.7,
            downloads=1250
        ),
        MarketplaceAgent(
            name="langchain-social",
            description="AI-powered social media content generation and posting",
            category="social", 
            price_tier="premium",
            capabilities=["twitter", "linkedin", "content", "ai"],
            integration_complexity="simple",
            test_score=92,
            status=AgentStatus.ACTIVE,
            rating=4.9,
            downloads=2100
        ),
        MarketplaceAgent(
            name="sales-outreach",
            description="Automated lead generation and sales outreach system",
            category="sales",
            price_tier="premium", 
            capabilities=["lead generation", "crm", "automation", "analytics"],
            integration_complexity="complex",
            test_score=78,
            status=AgentStatus.TESTING,
            rating=4.5,
            downloads=890
        )
    ]
    
    for agent in sample_agents:
        marketplace.add_agent_to_marketplace(agent)
    
    return marketplace

def main():
    print("🏪 AI AGENTS MARKETPLACE ENGINE TEST")
    print("=" * 50)
    
    # Create sample marketplace
    marketplace = create_sample_marketplace()
    
    # Test search functionality
    print("\n🔍 SEARCH TESTS:")
    messaging_agents = marketplace.search_agents(category="messaging")
    print(f"   Messaging agents found: {len(messaging_agents)}")
    
    premium_agents = marketplace.search_agents(price_tier="premium")  
    print(f"   Premium agents found: {len(premium_agents)}")
    
    ai_agents = marketplace.search_agents(query="ai")
    print(f"   AI-related agents found: {len(ai_agents)}")
    
    # Test agent details
    print("\n📋 AGENT DETAILS TEST:")
    details = marketplace.get_agent_details("evolution-whatsapp")
    if details:
        print(f"   Agent: {details['name']}")
        print(f"   Price: ${details['pricing']['price']}/month")
        print(f"   Setup time: {details['integration_guide']['estimated_setup_time']}")
    
    # Generate marketplace stats
    print("\n📊 MARKETPLACE STATISTICS:")
    stats = marketplace.generate_marketplace_stats()
    print(f"   Total agents: {stats['total_agents']}")
    print(f"   Average quality: {stats['average_quality_score']}/100")
    print(f"   Revenue potential: ${stats['revenue_potential']}/month per customer")
    
    # Save marketplace data
    with open("marketplace_data.json", "w") as f:
        # Convert agents to dict for JSON serialization
        agents_dict = {}
        for name, agent in marketplace.agents_catalog.items():
            agent_dict = asdict(agent)
            agent_dict['status'] = agent.status.value  # Convert enum to string
            agents_dict[name] = agent_dict
            
        json.dump({
            "agents": agents_dict,
            "stats": stats
        }, f, indent=2)
    
    print(f"\n✅ Marketplace data saved to: marketplace_data.json")
    print(f"🎉 MARKETPLACE ENGINE TEST COMPLETE!")

if __name__ == "__main__":
    main()
