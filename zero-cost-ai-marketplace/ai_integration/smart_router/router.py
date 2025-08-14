from dataclasses import dataclass

@dataclass
class ModelChoice:
    name: str
    reason: str

class SmartRouter:
    def choose(self, prompt: str) -> ModelChoice:
        if len(prompt) < 150:
            return ModelChoice(name="llama-lite", reason="Short prompt, low-cost model")
        return ModelChoice(name="gpt-oss-20b", reason="Long/complex prompt, higher-capacity model")
