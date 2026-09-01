from __future__ import annotations

from app.providers.base import LLMProvider


class TemplateProvider(LLMProvider):
    """Бесплатный режим без подключения языковой модели."""

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> str:
        return ""