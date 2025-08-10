#!/usr/bin/env python3
"""
Universal Agent Connector
The bridge between external agents and our OWL orchestration
"""
import asyncio
import json
import logging
from typing import Dict, Any, List
from dataclasses import dataclass
from enum import Enum

class AgentType(Enum):
    CONTROL = "control"
    MESSAGING = "messaging" 
    SALES = "sales"
    SOCIAL = "social"
    TESTING = "testing"
    PAYMENT = "payment"
    INFRASTRUCTURE = "infrastructure"

@dataclass
class AgentMetadata:
    name: str
    type: AgentType
    version: str
    api_endpoint: str
    capabilities: List[str]
    status: str = "active"

class UniversalAgentConnector:
    """Universal connector for all external agents"""
    
    def __init__(self):
        self.connected_agents = {}
        self.logger = logging.getLogger(__name__)
        
    async def connect_agent(self, metadata: AgentMetadata):
        """Connect an external agent to our system"""
        try:
            # Validate agent compatibility
            if self._validate_agent(metadata):
                self.connected_agents[metadata.name] = metadata
                self.logger.info(f"✅ Connected agent: {metadata.name}")
                return True
        except Exception as e:
            self.logger.error(f"❌ Failed to connect {metadata.name}: {e}")
            return False
    
    def _validate_agent(self, metadata: AgentMetadata) -> bool:
        """Validate agent meets our standards"""
        required_capabilities = ["process_task", "get_status", "handle_error"]
        return all(cap in metadata.capabilities for cap in required_capabilities)
    
    async def orchestrate_multi_agent_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Orchestrate task across multiple connected agents"""
        results = {}
        
        for agent_name, agent_metadata in self.connected_agents.items():
            if self._should_agent_handle_task(agent_metadata, task):
                try:
                    result = await self._execute_agent_task(agent_metadata, task)
                    results[agent_name] = result
                except Exception as e:
                    results[agent_name] = {"error": str(e)}
        
        return {
            "task_id": task.get("id"),
            "status": "completed",
            "results": results,
            "agents_used": len(results)
        }
    
    def _should_agent_handle_task(self, agent: AgentMetadata, task: Dict[str, Any]) -> bool:
        """Determine if agent should handle specific task"""
        task_type = task.get("type", "").lower()
        agent_capabilities = [cap.lower() for cap in agent.capabilities]
        return any(task_type in cap for cap in agent_capabilities)
    
    async def _execute_agent_task(self, agent: AgentMetadata, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute task on specific agent"""
        # This would interface with the actual agent API
        return {
            "agent": agent.name,
            "status": "success",
            "data": f"Task {task.get('id')} processed by {agent.name}"
        }

# Example usage
async def main():
    connector = UniversalAgentConnector()
    
    # Connect WhatsApp agent
    whatsapp_agent = AgentMetadata(
        name="evolution-whatsapp",
        type=AgentType.MESSAGING,
        version="1.0.0",
        api_endpoint="http://localhost:3000",
        capabilities=["send_message", "receive_message", "process_task", "get_status", "handle_error"]
    )
    
    await connector.connect_agent(whatsapp_agent)
    
    # Execute multi-agent task
    task = {
        "id": "customer_outreach_001",
        "type": "messaging",
        "data": {"message": "Hello from AI Agent System!", "recipient": "+1234567890"}
    }
    
    result = await connector.orchestrate_multi_agent_task(task)
    print(f"🎯 Task Result: {json.dumps(result, indent=2)}")

if __name__ == "__main__":
    asyncio.run(main())
