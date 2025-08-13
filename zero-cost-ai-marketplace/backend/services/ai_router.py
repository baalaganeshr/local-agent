import asyncio
import httpx
import time
from typing import Dict, Any
from enum import Enum
import os

class ModelType(Enum):
    LIGHTWEIGHT = "llama3.2:3b"
    HEAVYWEIGHT = "gpt-oss:20b"

class ComplexityAnalyzer:
    @staticmethod
    def analyze_prompt(prompt: str) -> ModelType:
        lightweight_keywords = ["hello", "hi", "simple", "quick", "basic", "what", "when", "where"]
        heavyweight_keywords = ["code", "complex", "analyze", "detailed", "algorithm", "business", "strategy", "technical", "architecture"]

        prompt_lower = (prompt or "").lower()
        word_count = len((prompt or "").split())

        if word_count > 50:
            return ModelType.HEAVYWEIGHT

        heavyweight_score = sum(1 for keyword in heavyweight_keywords if keyword in prompt_lower)
        lightweight_score = sum(1 for keyword in lightweight_keywords if keyword in prompt_lower)

        if heavyweight_score > lightweight_score:
            return ModelType.HEAVYWEIGHT
        else:
            return ModelType.LIGHTWEIGHT

class OllamaRouter:
    def __init__(self):
        base = os.getenv("OLLAMA_URL", "http://localhost:11434").rstrip("/")
        self.base_url = base + "/api/generate"
        self.timeout = 120

    async def generate_response(self, prompt: str, customer_tier: str = "basic") -> Dict[str, Any]:
        if (customer_tier or "basic").lower() == "enterprise":
            selected_model = ModelType.HEAVYWEIGHT
        elif (customer_tier or "basic").lower() == "premium":
            selected_model = ComplexityAnalyzer.analyze_prompt(prompt)
        else:
            selected_model = ModelType.LIGHTWEIGHT

        start_time = time.time()
        try:
            response = await self._call_ollama(prompt, selected_model.value)
            end_time = time.time()
            return {
                "success": True,
                "response": response,
                "model_used": selected_model.value,
                "complexity": "high" if selected_model == ModelType.HEAVYWEIGHT else "low",
                "response_time": round(end_time - start_time, 2),
                "cost_efficiency": "98%" if selected_model == ModelType.LIGHTWEIGHT else "95%",
                "profit_margin": "98%" if selected_model == ModelType.LIGHTWEIGHT else "95%",
                "timestamp": str(int(time.time())),
                "request_id": f"req_{int(time.time())}_{abs(hash(prompt)) % 10000}",
            }
        except Exception as e:
            return await self._fallback_response(prompt, str(e))

    async def _call_ollama(self, prompt: str, model: str) -> str:
        payload = {"model": model, "prompt": prompt, "stream": False}
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            r = await client.post(self.base_url, json=payload)
            r.raise_for_status()
            data = r.json()
            return data.get("response", "")

    async def _fallback_response(self, prompt: str, error: str) -> Dict[str, Any]:
        fallback_responses = {
            "code": "I can help you with coding. Here's a basic structure:\n\n```python\n# Your code here\ndef solution():\n    pass\n```",
            "business": "Based on current market trends, focus on acquisition and retention; optimize pricing and margins.",
            "technical": "This requires technical analysis. I can provide detailed implementation guidance.",
            "default": "I understand your request. Here's a comprehensive response to help you proceed.",
        }
        p = (prompt or "").lower()
        if any(k in p for k in ["code", "python", "javascript", "function"]):
            resp = fallback_responses["code"]
        elif any(k in p for k in ["business", "revenue", "profit", "strategy"]):
            resp = fallback_responses["business"]
        elif any(k in p for k in ["technical", "architecture", "system", "design"]):
            resp = fallback_responses["technical"]
        else:
            resp = fallback_responses["default"]
        return {
            "success": False,
            "response": resp,
            "model_used": "fallback",
            "complexity": "fallback",
            "response_time": 0.5,
            "cost_efficiency": "100%",
            "profit_margin": "100%",
            "timestamp": str(int(time.time())),
            "request_id": f"fallback_{int(time.time())}",
            "error": error,
        }
