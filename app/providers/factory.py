from __future__ import annotations

from app.config import Settings
from app.providers.base import LLMProvider
from app.providers.openai_compatible import OpenAICompatibleProvider
from app.providers.template import TemplateProvider


def build_provider(settings: Settings) -> LLMProvider:
    if settings.ai_provider in {"ollama", "openai"}:
        return OpenAICompatibleProvider(
            base_url=settings.base_url,
            api_key=settings.api_key,
            model=settings.model,
        )
    return TemplateProvider()

