from __future__ import annotations

def get_summary() -> dict:
    # Placeholder in-memory analytics that can be swapped for DB-backed logic
    return {
        "active_users": 12,
        "requests_24h": 482,
        "avg_latency_ms": 2870,
        "model_split": {"llama-lite": 0.62, "gpt-oss-20b": 0.38},
    }
