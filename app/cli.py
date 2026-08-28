from __future__ import annotations

import argparse
import json
from dataclasses import asdict

from app.config import settings
from app.database.db import save_content_pack
from app.generators.content_pack import generate_content_pack
from app.providers import build_provider


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate AI content packages for Instagram and TikTok."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    generate = subparsers.add_parser("generate", help="Generate a content package.")
    generate.add_argument("--topic", required=True)
    generate.add_argument("--audience", default="початківці в AI та IT")
    generate.add_argument("--platform", default="instagram,tiktok")
    generate.add_argument("--save", action="store_true")

    args = parser.parse_args()

    if args.command == "generate":
        provider = build_provider(settings)
        pack = generate_content_pack(args.topic, args.audience, args.platform, provider)
        payload = asdict(pack)

        if args.save:
            payload["database_id"] = save_content_pack(settings.database_path, pack)

        print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

