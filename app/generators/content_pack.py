from __future__ import annotations

import json
import re
from typing import Any

from app.models import ContentPack
from app.providers.base import LLMProvider
from app.providers.template import TemplateProvider


SYSTEM_PROMPT = """
Ты — редактор образовательного блога об искусственном интеллекте.

Пиши грамотно, естественно и только на русском языке.
Целевая аудитория — взрослые новички, которые изучают ИИ и IT.

Разрешено сохранять официальные названия и технические термины:
AI, IT, RAG, GPT, ChatGPT, Gemini, Google Flow, Python, Ollama,
API, JSON, Instagram, TikTok, YouTube Shorts.

Не переводи, не изменяй и не склоняй названия продуктов.
Не заменяй русские слова случайными иностранными словами.
Пиши «учиться», а не «learn».
Пиши «улучшается», а не «improves».
Пиши «качество», а не «quality».
Не используй слова «машинка» и «машина» для обозначения ИИ.
Используй слова «ИИ-система», «модель» или «алгоритм».

Требования к содержанию:
- объясняй тему простыми, но точными словами;
- каждый слайд и каждая сцена должны раскрывать новую мысль;
- не повторяй одинаковые предложения;
- добавь один понятный пример из повседневной жизни;
- не выдумывай исследования, цифры и факты;
- не обещай гарантированный результат;
- перед отправкой проверь грамматику и отсутствие случайных иностранных слов;
- возвращай только корректный JSON;
- не добавляй Markdown, пояснения или комментарии вокруг JSON.

""".strip()


def generate_content_pack(
    topic: str,
    audience: str,
    platform: str,
    provider: LLMProvider,
) -> ContentPack:
    topic = topic.strip()

    if not topic:
        raise RuntimeError("тема контента не может быть пустой")

    if isinstance(provider, TemplateProvider):
        return create_template_pack(
            topic=topic,
            audience=audience,
            platform=platform,
        )

    user_prompt = f"""
Создай один качественный пакет контента.

Тема: {topic}
Аудитория: {audience}
Платформы: {platform}

Требования:
- хук — до 12 слов, без кликбейта;
- сценарий Reels — 4 последовательные сцены на 20–30 секунд;
- карусель — ровно 6 разных по смыслу слайдов;
- первый слайд содержит хук;
- последний слайд содержит понятный следующий шаг;
- добавь один пример из повседневной жизни;
- создай ровно 3 визуальных промпта;
- каждый визуальный промпт должен содержать:
  1) описание кадра для создания изображения в Gemini;
  2) описание движения для анимации этого кадра в Google Flow;
- формат видео — вертикальный 9:16;
- визуальный стиль — Modern Tech Editorial;
- цвета: фон #F7F3EA, тёмно-синий #0B1F3A,
  оранжевый акцент #E66A2C;
- без логотипов, водяных знаков и текста внутри изображения.

Верни JSON строго такой структуры:

{{
  "hook": "короткий хук",
  "reel_script": "сцена 1; сцена 2; сцена 3; сцена 4",
  "carousel_slides": [
    "слайд 1",
    "слайд 2",
    "слайд 3",
    "слайд 4",
    "слайд 5",
    "слайд 6"
  ],
  "video_prompts": [
    "Сцена 1. Gemini: описание кадра. Google Flow: движение камеры и объектов.",
    "Сцена 2. Gemini: описание кадра. Google Flow: движение камеры и объектов.",
    "Сцена 3. Gemini: описание кадра. Google Flow: движение камеры и объектов."
  ],
  "caption": "подпись к публикации",
  "hashtags": [
    "#искусственныйинтеллект",
    "#ии",
    "#python",
    "#обучение",
    "#it"
  ],
  "cta": "призыв к одному простому действию",
  "quality_notes": [
    "что проверено в тексте",
    "что проверено в визуальных промптах"
  ]
}}
""".strip()

    raw_response = provider.generate(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=user_prompt,
    )

    data = parse_json_object(raw_response)
    validate_content_data(data)

    return ContentPack(
        topic=topic,
        audience=audience,
        platform=platform,
        hook=str(data["hook"]),
        reel_script=str(data["reel_script"]),
        carousel_slides=[
            str(item) for item in data["carousel_slides"]
        ],
        video_prompts=[
            str(item) for item in data["video_prompts"]
        ],
        caption=str(data["caption"]),
        hashtags=[
            str(item) for item in data["hashtags"]
        ],
        cta=str(data["cta"]),
        quality_notes=[
            str(item) for item in data.get("quality_notes", [])
        ],
    )


def parse_json_object(raw_response: str) -> dict[str, Any]:
    cleaned_response = raw_response.strip()

    if cleaned_response.startswith("```"):
        cleaned_response = re.sub(
            r"^```(?:json)?\s*",
            "",
            cleaned_response,
            flags=re.IGNORECASE,
        )
        cleaned_response = re.sub(
            r"\s*```$",
            "",
            cleaned_response,
        )

    try:
        result = json.loads(cleaned_response)

    except json.JSONDecodeError:
        match = re.search(
            r"\{.*\}",
            cleaned_response,
            flags=re.DOTALL,
        )

        if not match:
            raise RuntimeError(
                "модель не вернула JSON с пакетом контента"
            )

        try:
            result = json.loads(match.group(0))
        except json.JSONDecodeError as error:
            raise RuntimeError(
                "не удалось разобрать JSON от модели"
            ) from error

    if not isinstance(result, dict):
        raise RuntimeError("ответ модели должен быть JSON-объектом")

    return result


def validate_content_data(data: dict[str, Any]) -> None:
    required_fields = {
        "hook",
        "reel_script",
        "carousel_slides",
        "video_prompts",
        "caption",
        "hashtags",
        "cta",
    }

    missing_fields = required_fields.difference(data)

    if missing_fields:
        missing = ", ".join(sorted(missing_fields))
        raise RuntimeError(
            f"в ответе модели отсутствуют поля: {missing}"
        )

    if not isinstance(data["carousel_slides"], list):
        raise RuntimeError("carousel_slides должен быть списком")

    if not isinstance(data["video_prompts"], list):
        raise RuntimeError("video_prompts должен быть списком")

    if not isinstance(data["hashtags"], list):
        raise RuntimeError("hashtags должен быть списком")


def create_template_pack(
    topic: str,
    audience: str,
    platform: str,
) -> ContentPack:
    topic_label = topic.rstrip(".!?")

    return ContentPack(
        topic=topic,
        audience=audience,
        platform=platform,
        hook=f"{topic_label}: объясняю простыми словами.",
        reel_script=(
            f"Что такое {topic_label}? "
            "Разберём без сложных терминов. "
            "Сначала определим основную идею, "
            "затем посмотрим на простой пример "
            "и выберем один шаг для практики."
        ),
        carousel_slides=[
            f"{topic_label}: простое объяснение",
            "Зачем это нужно",
            "Как это работает",
            "Пример из реальной жизни",
            "Что попробовать самостоятельно",
            "Сохрани, чтобы повторить позже",
        ],
        video_prompts=[
            (
                "Вертикальная сцена 9:16: современное рабочее место, "
                f"визуальная метафора темы «{topic_label}»."
            ),
            (
                "Вертикальная сцена 9:16: новичок изучает ИИ "
                "за ноутбуком, чистая editorial-композиция."
            ),
            (
                "Вертикальная сцена 9:16: понятная визуализация "
                f"результата применения темы «{topic_label}»."
            ),
        ],
        caption=(
            f"{topic_label} можно понять без сложной теории. "
            "Начни с одного небольшого примера и попробуй "
            "повторить его самостоятельно."
        ),
        hashtags=[
            "#искусственныйинтеллект",
            "#ии",
            "#python",
            "#обучение",
            "#it",
        ],
        cta="Сохрани публикацию и напиши, какую тему разобрать дальше.",
        quality_notes=[
            "Есть понятный хук.",
            "Материал рассчитан на новичков.",
            "Есть практический следующий шаг.",
        ],
    )