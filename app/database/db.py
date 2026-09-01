from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from app.models import ContentPack


def initialize_database(database_path: str) -> None:
    Path(database_path).parent.mkdir(
        parents=True,
        exist_ok=True,
    )

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


def save_content_pack(
    database_path: str,
    content_pack: ContentPack,
) -> int:
    initialize_database(database_path)

    with sqlite3.connect(database_path) as connection:
        cursor = connection.execute(
            """
            INSERT INTO content_packs (
                topic,
                audience,
                platform,
                hook,
                reel_script,
                carousel_slides,
                video_prompts,
                caption,
                hashtags,
                cta,
                quality_notes,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                content_pack.topic,
                content_pack.audience,
                content_pack.platform,
                content_pack.hook,
                content_pack.reel_script,
                json.dumps(
                    content_pack.carousel_slides,
                    ensure_ascii=False,
                ),
                json.dumps(
                    content_pack.video_prompts,
                    ensure_ascii=False,
                ),
                content_pack.caption,
                json.dumps(
                    content_pack.hashtags,
                    ensure_ascii=False,
                ),
                content_pack.cta,
                json.dumps(
                    content_pack.quality_notes,
                    ensure_ascii=False,
                ),
                content_pack.created_at,
            ),
        )

        return int(cursor.lastrowid)