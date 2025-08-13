#!/usr/bin/env python3
"""
OWL Integration - Mock Implementation for Missing OWL/CAMEL Framework
Provides fallback functionality when real OWL and CAMEL frameworks are not available
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import json
import logging

# Mock implementations since real frameworks are not available
OWL_AVAILABLE = False
CAMEL_AVAILABLE = False

class MockOWLIntegration:
    """Mock OWL Integration for when real framework is not available"""
    
    def __init__(self):
        self.available = False
        self.agents = []
        self.logger = logging.getLogger(__name__)
        
    async def run_society_async(self, task: Dict[str, Any], agents: List[str]) -> Dict[str, Any]:
        """Mock society run method"""
        self.logger.info(f"Mock OWL society run: {task.get('type', 'unknown')} task")
        return {
            "status": "completed",
            "mock_mode": True,
            "agents_involved": agents,
            "timestamp": datetime.now().isoformat(),
            "result": "Mock OWL result - real OWL framework not available"
        }
    
    def create_agent(self, agent_type: str, config: Dict[str, Any]) -> "MockChatAgent":
        """Create a mock agent"""
        agent = MockChatAgent(agent_type, config)
        self.agents.append(agent)
        return agent
    
    def get_available_agents(self) -> List[Dict[str, Any]]:
        """Get list of available mock agents"""
        return [
            {
                "id": agent.agent_id,
                "type": agent.agent_type,
                "status": "active",
                "config": agent.config
            }
            for agent in self.agents
        ]

class MockChatAgent:
    """Mock Chat Agent implementation"""
    
    def __init__(self, agent_type: str, config: Dict[str, Any]):
        self.agent_type = agent_type
        self.agent_id = f"mock_{agent_type}_{datetime.now().strftime('%H%M%S')}"
        self.config = config
        self.conversation_history = []
    
    def step(self, input_message: "MockBaseMessage") -> Dict[str, Any]:
        """Mock agent step method"""
        response = {
            "agent_id": self.agent_id,
            "response": f"Mock response to: {input_message.content}",
            "timestamp": datetime.now().isoformat(),
            "mock_mode": True
        }
        self.conversation_history.append(response)
        return response
    
    def get_history(self) -> List[Dict[str, Any]]:
        """Get conversation history"""
        return self.conversation_history

class MockBaseMessage:
    """Mock base message class"""
    
    def __init__(self, content: str, role_type: str = "user"):
        self.content = content
        self.role_type = role_type
        self.timestamp = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary"""
        return {
            "content": self.content,
            "role_type": self.role_type,
            "timestamp": self.timestamp
        }

class MockRolePlaying:
    """Mock role playing society"""
    
    def __init__(self, assistant_agent, user_agent, task_prompt: str):
        self.assistant_agent = assistant_agent
        self.user_agent = user_agent
        self.task_prompt = task_prompt
        self.conversation_log = []
    
    def step(self) -> Dict[str, Any]:
        """Execute one step of role playing"""
        response = {
            "step_count": len(self.conversation_log) + 1,
            "task_prompt": self.task_prompt,
            "assistant_response": "Mock assistant response",
            "user_response": "Mock user response",
            "mock_mode": True
        }
        self.conversation_log.append(response)
        return response

# Factory functions for easy integration
def create_owl_integration() -> MockOWLIntegration:
    """Create OWL integration instance"""
    return MockOWLIntegration()

def create_chat_agent(agent_type: str = "assistant", config: Optional[Dict[str, Any]] = None) -> MockChatAgent:
    """Create chat agent instance"""
    if config is None:
        config = {"model_type": "mock", "temperature": 0.7}
    return MockChatAgent(agent_type, config)

def create_base_message(content: str, role_type: str = "user") -> MockBaseMessage:
    """Create base message instance"""
    return MockBaseMessage(content, role_type)

def create_role_playing(task_prompt: str) -> MockRolePlaying:
    """Create role playing society"""
    assistant = create_chat_agent("assistant")
    user = create_chat_agent("user")
    return MockRolePlaying(assistant, user, task_prompt)

# Export all classes and functions for import
__all__ = [
    'MockOWLIntegration',
    'MockChatAgent', 
    'MockBaseMessage',
    'MockRolePlaying',
    'create_owl_integration',
    'create_chat_agent',
    'create_base_message',
    'create_role_playing',
    'OWL_AVAILABLE',
    'CAMEL_AVAILABLE'
]
