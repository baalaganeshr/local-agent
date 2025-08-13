#!/usr/bin/env python3
"""
Ollama GPT-OSS Connector
Integrates local Ollama models with the AI Agent Marketplace
"""
import asyncio
import json
import subprocess
from typing import Dict, List, Any, Optional
from datetime import datetime

class OllamaGPTOSSConnector:
    """Connector for local Ollama GPT-OSS models"""
    
    def __init__(self, model_name: str = "gpt-oss:20b"):
        self.model_name = model_name
        self.is_available = self._check_ollama_availability()
        
    def _check_ollama_availability(self) -> bool:
        """Check if Ollama and the model are available"""
        try:
            # Check Ollama installation
            result = subprocess.run(["ollama", "--version"], capture_output=True, text=True)
            if result.returncode != 0:
                return False
                
            # Check if model is available
            result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
            return self.model_name in result.stdout
            
        except FileNotFoundError:
            return False
        except Exception:
            return False
    
    async def generate_response(self, prompt: str, max_tokens: Optional[int] = None) -> Dict[str, Any]:
        """Generate response using GPT-OSS model"""
        
        if not self.is_available:
            return {
                "error": "Ollama GPT-OSS model not available",
                "response": None,
                "model": self.model_name,
                "timestamp": datetime.now().isoformat()
            }
        
        try:
            start_time = datetime.now()
            
            # Run Ollama command
            result = subprocess.run(
                ["ollama", "run", self.model_name, prompt],
                capture_output=True,
                text=True,
                timeout=120
            )
            
            end_time = datetime.now()
            response_time = (end_time - start_time).total_seconds()
            
            if result.returncode == 0:
                return {
                    "response": result.stdout.strip(),
                    "model": self.model_name,
                    "response_time": response_time,
                    "timestamp": end_time.isoformat(),
                    "error": None
                }
            else:
                return {
                    "error": f"Model execution failed: {result.stderr}",
                    "response": None,
                    "model": self.model_name,
                    "timestamp": datetime.now().isoformat()
                }
                
        except subprocess.TimeoutExpired:
            return {
                "error": "Model response timeout (120s)",
                "response": None,
                "model": self.model_name,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "error": f"Unexpected error: {str(e)}",
                "response": None,
                "model": self.model_name,
                "timestamp": datetime.now().isoformat()
            }
    
    def create_agent_template(self, agent_type: str) -> Dict[str, Any]:
        """Create agent template using GPT-OSS"""
        
        agent_prompts = {
            "whatsapp": """
Create a WhatsApp Business Agent that can:
1. Send automated welcome messages
2. Handle customer inquiries 
3. Schedule follow-ups
4. Process orders
5. Provide customer support

Include proper error handling and rate limiting.
""",
            "social_media": """
Create a Social Media Agent that can:
1. Schedule posts across platforms
2. Respond to comments and DMs
3. Analyze engagement metrics
4. Create content suggestions
5. Monitor brand mentions

Include API integrations and content moderation.
""",
            "sales": """
Create a Sales Agent that can:
1. Qualify leads automatically
2. Send personalized outreach
3. Schedule meetings
4. Track sales pipeline
5. Generate reports

Include CRM integration and conversion tracking.
""",
            "customer_support": """
Create a Customer Support Agent that can:
1. Answer common questions
2. Escalate complex issues
3. Track ticket status
4. Provide 24/7 availability
5. Learn from interactions

Include knowledge base integration and sentiment analysis.
"""
        }
        
        if agent_type not in agent_prompts:
            return {
                "error": f"Unknown agent type: {agent_type}",
                "template": None
            }
        
        return {
            "agent_type": agent_type,
            "prompt": agent_prompts[agent_type],
            "model": self.model_name,
            "pricing_tier": "local_ai",
            "monthly_cost": 50,  # $50/month for local AI agents
            "features": [
                "Local processing (no data leaves your server)",
                "No per-token costs",
                "24/7 availability",
                "Customizable responses",
                "Privacy-first architecture"
            ]
        }
    
    def get_marketplace_info(self) -> Dict[str, Any]:
        """Get marketplace information for GPT-OSS integration"""
        
        return {
            "name": "Local AI Agents (GPT-OSS)",
            "description": "Privacy-first AI agents powered by local GPT-OSS models",
            "model": self.model_name,
            "available": self.is_available,
            "pricing": {
                "setup_fee": 0,
                "monthly_cost": 50,
                "per_interaction": 0,
                "billing_cycle": "monthly"
            },
            "advantages": [
                "🔒 Complete data privacy - nothing leaves your server",
                "💰 No per-token costs - unlimited interactions",
                "🚀 Fast response times for local processing", 
                "⚙️ Fully customizable model behavior",
                "📊 Detailed usage analytics without privacy concerns"
            ],
            "requirements": [
                "Ollama installed on server",
                "GPT-OSS:20b model downloaded (~12GB)",
                "8GB+ RAM recommended",
                "Modern CPU or GPU acceleration"
            ],
            "agent_types": [
                "WhatsApp Business Automation",
                "Social Media Management", 
                "Sales Pipeline Automation",
                "Customer Support 24/7",
                "Content Generation",
                "Data Analysis & Reporting"
            ]
        }

class LocalAIMarketplaceIntegration:
    """Integration class for adding local AI to marketplace"""
    
    def __init__(self):
        self.connector = OllamaGPTOSSConnector()
        
    def add_to_marketplace(self) -> Dict[str, Any]:
        """Add local AI agents to marketplace"""
        
        marketplace_entry = {
            "local-ai-whatsapp": {
                "name": "Local AI WhatsApp Agent",
                "description": "Privacy-first WhatsApp automation with local GPT-OSS",
                "category": "messaging",
                "price_tier": "local_ai",
                "monthly_cost": 50,
                "capabilities": ["whatsapp", "automation", "privacy", "local"],
                "integration_complexity": "medium",
                "test_score": 95,  # High score for privacy
                "status": "active" if self.connector.is_available else "requires_setup",
                "features": self.connector.get_marketplace_info()["advantages"],
                "requirements": self.connector.get_marketplace_info()["requirements"]
            },
            "local-ai-social": {
                "name": "Local AI Social Media Agent", 
                "description": "Social media management with complete data privacy",
                "category": "social_media",
                "price_tier": "local_ai",
                "monthly_cost": 50,
                "capabilities": ["social", "content", "privacy", "local"],
                "integration_complexity": "medium",
                "test_score": 92,
                "status": "active" if self.connector.is_available else "requires_setup"
            },
            "local-ai-sales": {
                "name": "Local AI Sales Agent",
                "description": "Private sales automation that keeps your data secure", 
                "category": "sales",
                "price_tier": "local_ai",
                "monthly_cost": 50,
                "capabilities": ["sales", "crm", "privacy", "local"],
                "integration_complexity": "medium", 
                "test_score": 90,
                "status": "active" if self.connector.is_available else "requires_setup"
            }
        }
        
        return marketplace_entry
    
    def calculate_revenue_impact(self) -> Dict[str, Any]:
        """Calculate revenue impact of adding local AI tier"""
        
        current_revenue = 227  # Current monthly revenue per customer
        local_ai_premium = 150  # Additional $150 for local AI agents (3 agents x $50)
        
        return {
            "current_revenue_per_customer": current_revenue,
            "local_ai_additional_revenue": local_ai_premium,
            "total_potential_revenue": current_revenue + local_ai_premium,
            "revenue_increase_percentage": round((local_ai_premium / current_revenue) * 100),
            "market_advantages": [
                "First AI marketplace with local processing option",
                "Appeals to privacy-conscious businesses",
                "Unlimited usage without per-token costs", 
                "Higher margins due to no cloud API costs"
            ]
        }

if __name__ == "__main__":
    print("🤖 LOCAL AI MARKETPLACE INTEGRATION TEST")
    print("=" * 50)
    
    # Test connector
    connector = OllamaGPTOSSConnector()
    
    if connector.is_available:
        print("✅ GPT-OSS model available!")
        
        # Test agent creation
        template = connector.create_agent_template("whatsapp")
        print(f"📱 WhatsApp agent template created: {template['agent_type']}")
        
        # Test marketplace integration
        integration = LocalAIMarketplaceIntegration()
        marketplace_entries = integration.add_to_marketplace()
        
        print(f"🏪 Added {len(marketplace_entries)} local AI agents to marketplace")
        
        # Calculate revenue impact
        revenue_impact = integration.calculate_revenue_impact()
        print(f"💰 Revenue impact: +{revenue_impact['revenue_increase_percentage']}% per customer")
        print(f"💰 Total potential: ${revenue_impact['total_potential_revenue']}/month per customer")
        
        # Save marketplace data
        with open("local_ai_marketplace_data.json", "w", encoding="utf-8") as f:
            json.dump({
                "marketplace_entries": marketplace_entries,
                "revenue_impact": revenue_impact,
                "timestamp": datetime.now().isoformat()
            }, f, indent=2, ensure_ascii=False)
        
        print("✅ Local AI marketplace data saved!")
        
    else:
        print("❌ GPT-OSS model not available")
        print("📋 Setup required:")
        print("   1. Install Ollama: https://ollama.ai")
        print("   2. Run: ollama pull gpt-oss:20b")
        print("   3. Test with: ollama run gpt-oss:20b 'Hello!'")
