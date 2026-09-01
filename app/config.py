from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def load_env_file(file_path: str = ".env") -> None:
    """Загрузить переменные из .env без сторонних библиотек."""

    path = Path(file_path)

    if not path.exists():
        return

    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()

        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", maxsplit=1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")

        os.environ.setdefault(key, value)


load_env_file()


@dataclass(frozen=True)
class Settings:
    ai_provider: str
    model: str
    base_url: str
    api_key: str
    database_path: str


settings = Settings(
    ai_provider=os.getenv("AI_PROVIDER", "template").lower(),
    model=os.getenv("AI_MODEL", "llama3.1:8b"),
    base_url=os.getenv(
        "AI_BASE_URL",
        "http://127.0.0.1:11434/v1",
    ),
    api_key=os.getenv("AI_API_KEY", "ollama"),
    database_path=os.getenv(
        "DATABASE_PATH",
        "content_studio.db",
    ),
)