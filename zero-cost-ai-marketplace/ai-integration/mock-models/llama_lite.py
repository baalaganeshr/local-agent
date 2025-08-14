import asyncio
import random

async def generate(prompt: str) -> str:
    await asyncio.sleep(random.uniform(1.8, 2.6))
    return f"[LLaMA-Lite mock] {prompt[:400]}"
