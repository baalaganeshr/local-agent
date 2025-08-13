import asyncio
import random

async def generate(prompt: str) -> str:
    await asyncio.sleep(random.uniform(3.2, 5.0))
    return f"[GPT-OSS-20B mock] {prompt[:400]}"
