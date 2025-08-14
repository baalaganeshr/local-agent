import asyncio
import random
from typing import Tuple

MODELS = ["llama-lite", "gpt-oss-20b"]

async def generate_reply(prompt: str, tier: str | None = None) -> Tuple[str, str, int]:
    """
    Generate a mock AI reply, simulating tier-aware routing and realistic latency.

    - Short prompts prefer llama-lite
    - Premium/Enterprise slightly favor gpt-oss-20b
    - Latency between 2s and 8s
    """
    prompt = prompt or ""
    base_choice = "llama-lite" if len(prompt) < 180 else "gpt-oss-20b"

    if (tier or "basic").lower() == "basic":
        model = base_choice if base_choice == "llama-lite" else ("llama-lite" if random.random() < 0.6 else "gpt-oss-20b")
    elif (tier or "basic").lower() == "premium":
        model = base_choice if base_choice == "gpt-oss-20b" else ("gpt-oss-20b" if random.random() < 0.6 else "llama-lite")
    else:  # enterprise
        model = "gpt-oss-20b" if random.random() < 0.7 else base_choice

    wait_s = random.uniform(2.0, 8.0)
    await asyncio.sleep(wait_s)

    lead = {
        "llama-lite": "[LLaMA-Lite mock]",
        "gpt-oss-20b": "[GPT-OSS-20B mock]",
    }.get(model, "[Mock]")

    # Lightweight heuristic to sound helpful without being verbose
    snippet = prompt.strip().splitlines()[0][:200] if prompt else "How can I help today?"
    reply = f"{lead} {snippet}".strip()
    return reply, model, int(wait_s * 1000)
