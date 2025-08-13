#!/usr/bin/env python3
"""
Base Agent Module - Foundation for all agent implementations
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging
import asyncio

class BaseAgent(ABC):
    """Base class for all agents in the Multi-ai-agents system"""
    
    def __init__(self, agent_name: str, config: Optional[Dict[str, Any]] = None):
        self.agent_name = agent_name
        self.config = config or {}
        self.logger = logging.getLogger(f"agent.{agent_name}")
        self.created_at = datetime.now()
        self.status = "initialized"
        self.message_history = []
    
    @abstractmethod
    def process_message(self, message: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Process an incoming message and return a response"""
        pass
    
    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """Return list of capabilities this agent supports"""
        pass
    
    def get_status(self) -> Dict[str, Any]:
        """Get current agent status"""
        return {
            "name": self.agent_name,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "message_count": len(self.message_history),
            "capabilities": self.get_capabilities()
        }
    
    def log_message(self, message: str, message_type: str = "info"):
        """Log a message to the agent's history"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "type": message_type,
            "message": message
        }
        self.message_history.append(log_entry)
        
        if message_type == "error":
            self.logger.error(message)
        elif message_type == "warning":
            self.logger.warning(message)
        else:
            self.logger.info(message)
    
    async def process_message_async(self, message: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Async version of process_message"""
        # Default implementation runs sync version in executor
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.process_message, message, context)
    
    def validate_config(self) -> bool:
        """Validate agent configuration"""
        required_fields = getattr(self, 'REQUIRED_CONFIG_FIELDS', [])
        for field in required_fields:
            if field not in self.config:
                self.log_message(f"Missing required config field: {field}", "error")
                return False
        return True

class MockAgent(BaseAgent):
    """Mock agent implementation for testing and fallback scenarios"""
    
    def __init__(self, agent_name: str = "mock_agent", config: Optional[Dict[str, Any]] = None):
        super().__init__(agent_name, config)
        self.status = "active"
    
    def process_message(self, message: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Process message with mock response"""
        self.log_message(f"Processing: {message}")
        return f"Mock response to: {message} (from {self.agent_name})"
    
    def get_capabilities(self) -> List[str]:
        """Return mock capabilities"""
        return [
            "message_processing",
            "mock_responses", 
            "logging",
            "status_reporting"
        ]

# Export for import
__all__ = ['BaseAgent', 'MockAgent']
