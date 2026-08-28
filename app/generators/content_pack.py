from __future__ import annotations

import json
import re

from app.models import ContentPack
from app.providers.base import LLMProvider
from app.providers.template import TemplateProvider


SYSTEM_PROMPT = """
You are an AI content strategist for educational Instagram and TikTok content.
Return concise, practical content in Ukrainian. Do not invent fake statistics.
Focus on AI, LLMs, Python, productivity, and beginner-friendly IT learning.
"""


def generate_content_pack(
    topic: str,
    audience: str,
    platform: str,
    provider: LLMProvider,
) -> ContentPack:
    if isinstance(provider, TemplateProvider):
        return _template_pack(topic, audience, platform)

    user_prompt = f"""
Create one content package as valid JSON only.

Topic: {topic}
Audience: {audience}
Platform: {platform}

JSON schema:
{{
  "hook": "short opening hook",
  "reel_script": "script for a 30-45 second short video",
  "carousel_slides": ["slide 1", "slide 2", "slide 3", "slide 4", "slide 5", "slide 6"],
  "video_prompts": ["prompt 1", "prompt 2", "prompt 3"],
  "caption": "post caption",
  "hashtags": ["#tag1", "#tag2", "#tag3", "#tag4", "#tag5"],
  "cta": "call to action",
  "quality_notes": ["note 1", "note 2"]
}}
"""
    raw = provider.generate(SYSTEM_PROMPT, user_prompt)
    data = _parse_json_object(raw)

    return ContentPack(
        topic=topic,
        audience=audience,
        platform=platform,
        hook=data["hook"],
        reel_script=data["reel_script"],
        carousel_slides=list(data["carousel_slides"]),
        video_prompts=list(data["video_prompts"]),
        caption=data["caption"],
        hashtags=list(data["hashtags"]),
        cta=data["cta"],
        quality_notes=list(data.get("quality_notes", [])),
    )


def _parse_json_object(raw: str) -> dict:
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", raw, flags=re.DOTALL)
        if not match:
            raise
        return json.loads(match.group(0))


def _template_pack(topic: str, audience: str, platform: str) -> ContentPack:
    topic_label = _topic_label(topic)
    return ContentPack(
        topic=topic,
        audience=audience,
        platform=platform,
        hook=f"{topic_label}: поясню простими словами за 30 секунд.",
        reel_script=(
            f"Сьогодні розберемо тему: {topic_label}. "
            "Спочатку поясни проблему, потім покажи маленький приклад, "
            "а в кінці дай один практичний крок, який глядач може повторити."
        ),
        carousel_slides=[
            f"{topic_label}: просте пояснення",
            "Навіщо це потрібно в реальному житті",
            "Одна типова помилка новачків",
            "Міні-приклад без складної теорії",
            "Як спробувати це сьогодні",
            "Збережи, якщо вивчаєш AI",
        ],
        video_prompts=[
            f"Create a clean vertical 9:16 educational video scene about {topic_label}.",
            f"Show a beginner-friendly AI workspace with notes about {topic_label}.",
            f"Generate a modern carousel visual concept explaining {topic_label}.",
        ],
        caption=(
            f"{topic_label} можна зрозуміти без складних термінів. "
            "Почни з маленького прикладу і поступово збирай систему знань."
        ),
        hashtags=["#ai", "#llm", "#python", "#штучнийінтелект", "#навчання"],
        cta="Збережи пост і напиши тему, яку розібрати наступною.",
        quality_notes=[
            "Є хук на початку.",
            "Є практичний крок для аудиторії.",
            "Контент не обіцяє гарантований результат.",
        ],
    )


def _topic_label(topic: str) -> str:
    normalized = topic.strip().rstrip(".!?")
    return normalized[0].upper() + normalized[1:] if normalized else "AI-тема дня"
