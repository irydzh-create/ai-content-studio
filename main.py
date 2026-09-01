from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict

from app.config import settings
from app.database.db import save_content_pack
from app.generators.content_pack import generate_content_pack
from app.providers import build_provider


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="AI Content Studio — генератор контента на Python и Ollama."
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    generate_parser = subparsers.add_parser(
        "generate",
        help="Создать пакет контента.",
    )

    generate_parser.add_argument(
        "--topic",
        required=True,
        help="Тема публикации.",
    )

    generate_parser.add_argument(
        "--audience",
        default="новички, которые изучают ИИ и хотят перейти в IT",
        help="Целевая аудитория.",
    )

    generate_parser.add_argument(
        "--platform",
        default="Instagram, TikTok, YouTube Shorts",
        help="Площадки публикации.",
    )

    generate_parser.add_argument(
        "--save",
        action="store_true",
        help="Сохранить результат в SQLite.",
    )

    return parser


def main() -> int:
    parser = create_parser()
    args = parser.parse_args()

    try:
        provider = build_provider(settings)

        content_pack = generate_content_pack(
            topic=args.topic,
            audience=args.audience,
            platform=args.platform,
            provider=provider,
        )

        result = asdict(content_pack)

        if args.save:
            result["database_id"] = save_content_pack(
                settings.database_path,
                content_pack,
            )

        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    except RuntimeError as error:
        print(f"\nОшибка генерации: {error}", file=sys.stderr)

        if settings.ai_provider == "ollama":
            print(
                "Проверь, запущен ли Ollama и установлена ли выбранная модель.",
                file=sys.stderr,
            )

        return 1


if __name__ == "__main__":
    raise SystemExit(main())