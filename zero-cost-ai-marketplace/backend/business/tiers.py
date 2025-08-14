from __future__ import annotations

_Tiers = [
    {"name": "basic", "rate_limit": 30, "priority": 1},
    {"name": "premium", "rate_limit": 120, "priority": 2},
    {"name": "enterprise", "rate_limit": 600, "priority": 3},
]

def get_tiers() -> list[dict]:
    return list(_Tiers)
