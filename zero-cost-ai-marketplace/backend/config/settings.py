from __future__ import annotations
import os
from typing import List

class Settings:
    def __init__(self) -> None:
        self.cors_allow_origins: List[str] = [o.strip() for o in os.getenv("CORS_ALLOW_ORIGINS", "http://localhost:8080").split(",") if o.strip()]
        self.default_tier: str = os.getenv("DEFAULT_TIER", "basic")
        self.database_url: str = os.getenv("DATABASE_URL", "sqlite:///./data/app.db")

settings = Settings()
