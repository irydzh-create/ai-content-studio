from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class ContentPack:
    topic: str
    audience: str
    platform: str
    hook: str
    reel_script: str
    carousel_slides: list[str]
    video_prompts: list[str]
    caption: str
    hashtags: list[str]
    cta: str
    quality_notes: list[str] = field(default_factory=list)
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )