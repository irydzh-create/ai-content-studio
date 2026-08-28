from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    ai_provider: str = os.getenv("AI_PROVIDER", "template")
    model: str = os.getenv("AI_MODEL", "llama3.1:8b")
    base_url: str = os.getenv("AI_BASE_URL", "http://127.0.0.1:11434/v1")
    api_key: str = os.getenv("AI_API_KEY", os.getenv("OPENAI_API_KEY", "ollama"))
    database_path: str = os.getenv("DATABASE_PATH", "content_studio.db")


settings = Settings()

