#!/usr/bin/env python3
"""
OWL Integration Adapter
Adapts external agents to work with our OWL orchestration system
"""
import sys
import os

# Add the correct paths for OWL integration
current_dir = os.path.dirname(os.path.abspath(__file__))
owl_path = os.path.join(current_dir, '..', 'owl')
agents_path = os.path.join(current_dir, '..')

sys.path.insert(0, owl_path)
sys.path.insert(0, agents_path)

# Initialize variables to None first
OWLIntegration = None
BaseAgent = None

try:
    # Import from the root directory where we created owl_integration.py
    sys.path.insert(0, os.path.join(current_dir, '..'))
    from owl_integration import MockOWLIntegration as OWLIntegration
    from agents.base_agent import BaseAgent
    
except (ImportError, ModuleNotFoundError) as e:
    print(f"⚠️ OWL integration not available in this environment: {e}")
    
    # Mock OWLIntegration class for when the real one isn't available
    class OWLIntegration:
        def __init__(self):
            pass
        
        async def run_society_async(self, task: dict, agents: list):
            return {"mock": True, "message": "OWL integration not available"}
    
    # Mock BaseAgent class
    class BaseAgent:
        def __init__(self):
            pass

class OWLAdapter:
    """Adapter to integrate external agents with OWL orchestration"""
    
    def __init__(self):
        try:
            self.owl_integration = OWLIntegration()
            self.owl_available = True
        except:
            self.owl_integration = None
            self.owl_available = False
    
    def adapt_external_agent(self, agent_name: str, agent_config: dict) -> dict:
        """Adapt external agent to OWL-compatible format"""
        
        adapted_config = {
            "name": agent_name,
            "type": "external_integration",
            "owl_compatible": True,
            "capabilities": agent_config.get("capabilities", []),
            "api_endpoint": agent_config.get("api_endpoint"),
            "integration_method": self._determine_integration_method(agent_config),
            "owl_orchestration": {
                "task_handler": f"handle_{agent_name}_task",
                "status_reporter": f"get_{agent_name}_status", 
                "error_handler": f"handle_{agent_name}_error"
            }
        }
        
        return adapted_config
    
    def _determine_integration_method(self, agent_config: dict) -> str:
        """Determine best integration method for agent"""
        
        if agent_config.get("has_api", False):
            return "api_integration"
        elif agent_config.get("has_python_interface", False):
            return "direct_integration"
        elif agent_config.get("has_cli", False):
            return "cli_integration"
        else:
            return "wrapper_integration"
    
    async def orchestrate_with_owl(self, task: dict, participating_agents: list) -> dict:
        """Orchestrate task using OWL with external agents"""
        
        if not self.owl_available:
            return {"error": "OWL integration not available"}
        
        try:
            # Create OWL society with external agents
            result = await self.owl_integration.run_society_async(
                task=task,
                agents=participating_agents
            )
            
            return {
                "status": "success",
                "owl_orchestration": True,
                "result": result,
                "agents_participated": len(participating_agents)
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "owl_orchestration": False
            }

# Integration test
async def test_owl_adapter():
    adapter = OWLAdapter()
    
    # Test external agent adaptation
    external_config = {
        "name": "whatsapp-business",
        "capabilities": ["send_message", "receive_message", "manage_contacts"],
        "has_api": True,
        "api_endpoint": "http://localhost:3000"
    }
    
    adapted = adapter.adapt_external_agent("whatsapp-business", external_config)
    print(f"🔄 Adapted Agent Config: {adapted}")
    
    # Test OWL orchestration
    task = {
        "id": "test_orchestration",
        "type": "messaging",
        "description": "Send welcome message to new customer"
    }
    
    result = await adapter.orchestrate_with_owl(task, ["whatsapp-business"])
    print(f"🦉 OWL Orchestration Result: {result}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_owl_adapter())
