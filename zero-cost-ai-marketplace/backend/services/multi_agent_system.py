from typing import Dict, Any

from backend.services.bulletproof_client import BulletproofClient

class AgentType:
    CHAT = "chat_agent"
    CODE = "code_agent"
    BUSINESS = "business_agent"
    TECHNICAL = "technical_agent"

class MultiAgentRouter:
    def __init__(self) -> None:
        self.client = BulletproofClient()
        self.agents = {
            AgentType.CHAT: {"model": "llama3.2:3b", "system": "You are a helpful chat assistant."},
            AgentType.CODE: {"model": "gpt-oss:20b", "system": "You are a professional code generator."},
            AgentType.BUSINESS: {"model": "gpt-oss:20b", "system": "You are a business strategy expert."},
            AgentType.TECHNICAL: {"model": "gpt-oss:20b", "system": "You are a technical architect."},
        }

    def classify_request(self, prompt: str) -> str:
        p = (prompt or "").lower()
        if any(k in p for k in ["code", "function", "python", "javascript", "programming"]):
            return AgentType.CODE
        if any(k in p for k in ["business", "revenue", "strategy", "market", "profit"]):
            return AgentType.BUSINESS
        if any(k in p for k in ["architecture", "system", "technical", "infrastructure"]):
            return AgentType.TECHNICAL
        return AgentType.CHAT

    async def process_request(self, prompt: str, customer_tier: str) -> Dict[str, Any]:
        agent_type = self.classify_request(prompt)
        agent_cfg = self.agents[agent_type]
        if (customer_tier or "basic").lower() == "basic":
            agent_cfg = {"model": "llama3.2:3b", "system": agent_cfg["system"]}
        enhanced = f"{agent_cfg['system']}\n\nUser: {prompt}\n\nAssistant:"
        resp = await self.client.call_ollama(agent_cfg["model"], enhanced)
        if resp.success:
            return {
                "success": True,
                "response": resp.data,
                "agent_used": agent_type,
                "model_used": agent_cfg["model"],
                "response_time": resp.response_time,
                "status": "operational",
            }
        return self.generate_fallback_response(prompt, agent_type)

    def generate_fallback_response(self, prompt: str, agent_type: str) -> Dict[str, Any]:
        fb = {
            AgentType.CHAT: "I understand your message. How can I help you today?",
            AgentType.CODE: "Here's a code template:\n\n```python\n# Your solution here\ndef main():\n    pass\n```",
            AgentType.BUSINESS: "Focus on customer value and operational efficiency to grow revenue sustainably.",
            AgentType.TECHNICAL: "Prioritize scalability, security, and maintainability in your architecture.",
        }
        return {
            "success": True,
            "response": fb.get(agent_type, fb[AgentType.CHAT]),
            "agent_used": agent_type,
            "model_used": "fallback",
            "response_time": 0.5,
            "status": "fallback_active",
        }
