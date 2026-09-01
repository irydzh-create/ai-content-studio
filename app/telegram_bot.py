from __future__ import annotations

import asyncio
import os

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from app.config import settings
from app.generators.content_pack import generate_content_pack
from app.providers.openai_compatible import OpenAICompatibleProvider
from app.providers.template import TemplateProvider


DEFAULT_AUDIENCE = "новички, которые изучают ИИ и хотят перейти в IT"
DEFAULT_PLATFORM = "Instagram, TikTok, YouTube Shorts"


def create_provider():
    if settings.ai_provider == "template":
        return TemplateProvider()

    if settings.ai_provider == "ollama":
        return OpenAICompatibleProvider(
            base_url=settings.base_url,
            api_key=settings.api_key,
            model=settings.model,
        )

    raise RuntimeError(
        f"неизвестный AI_PROVIDER: {settings.ai_provider}"
    )


def format_content_pack(content_pack) -> str:
    slides = "\n".join(
        f"{index + 1}. {slide}"
        for index, slide in enumerate(content_pack.carousel_slides)
    )

    video_prompts = "\n".join(
        f"{index + 1}. {prompt}"
        for index, prompt in enumerate(content_pack.video_prompts)
    )

    hashtags = " ".join(content_pack.hashtags)

    return f"""
Готов пакет контента.

Тема:
{content_pack.topic}

Хук:
{content_pack.hook}

Сценарий Reels / Shorts:
{content_pack.reel_script}

Карусель:
{slides}

Промпты для Gemini / Google Flow:
{video_prompts}

Подпись:
{content_pack.caption}

Хэштеги:
{hashtags}

Призыв к действию:
{content_pack.cta}
""".strip()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = """
Привет! Я AI Content Studio.

Напиши тему, например:
Что такое ИИ простыми словами

Я подготовлю хук, сценарий короткого видео, карусель, подпись и промпты для Gemini / Google Flow.
""".strip()

    await update.message.reply_text(message)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await start(update, context)


async def handle_topic(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    topic = update.message.text.strip()

    if not topic:
        await update.message.reply_text("Напиши тему для генерации контента.")
        return

    await update.message.reply_text(
        "Генерирую пакет контента. Это может занять немного времени."
    )

    provider = create_provider()

    try:
        content_pack = await asyncio.to_thread(
            generate_content_pack,
            topic,
            DEFAULT_AUDIENCE,
            DEFAULT_PLATFORM,
            provider,
        )

    except Exception as error:
        await update.message.reply_text(
            f"Не получилось сгенерировать контент: {error}"
        )
        return

    await update.message.reply_text(
        format_content_pack(content_pack),
        disable_web_page_preview=True,
    )


def main() -> int:
    token = os.getenv("TELEGRAM_BOT_TOKEN")

    if not token:
        raise RuntimeError(
            "не найден TELEGRAM_BOT_TOKEN в .env"
        )

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_topic)
    )

    application.run_polling()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())