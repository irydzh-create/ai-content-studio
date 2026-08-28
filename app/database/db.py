from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from app.models import ContentPack


def init_db(database_path: str) -> None:
    with sqlite3.connect(database_path) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS content_packs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT NOT NULL,
                audience TEXT NOT NULL,
                platform TEXT NOT NULL,
                hook TEXT NOT NULL,
                reel_script TEXT NOT NULL,
                carousel_slides TEXT NOT NULL,
                video_prompts TEXT NOT NULL,
                caption TEXT NOT NULL,
                hashtags TEXT NOT NULL,
                cta TEXT NOT NULL,
                quality_notes TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )


def save_content_pack(database_path: str, pack: ContentPack) -> int:
    Path(database_path).parent.mkdir(parents=True, exist_ok=True)
    init_db(database_path)
    with sqlite3.connect(database_path) as connection:
        cursor = connection.execute(
            """
            INSERT INTO content_packs (
                topic, audience, platform, hook, reel_script, carousel_slides,
                video_prompts, caption, hashtags, cta, quality_notes, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                pack.topic,
                pack.audience,
                pack.platform,
                pack.hook,
                pack.reel_script,
                json.dumps(pack.carousel_slides, ensure_ascii=False),
                json.dumps(pack.video_prompts, ensure_ascii=False),
                pack.caption,
                json.dumps(pack.hashtags, ensure_ascii=False),
                pack.cta,
                json.dumps(pack.quality_notes, ensure_ascii=False),
                pack.created_at,
            ),
        )
        return int(cursor.lastrowid)

