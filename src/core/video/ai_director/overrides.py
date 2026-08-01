from __future__ import annotations

import json
from pathlib import Path

from .models import CreativeOverride


class CreativeOverrideLoader:
    def load(self, path) -> CreativeOverride:
        path = Path(path)

        if not path.exists():
            return CreativeOverride()

        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return CreativeOverride()

        if not isinstance(data, dict):
            return CreativeOverride()

        return CreativeOverride(
            theme_pack=data.get("theme_pack"),
            camera_style=data.get("camera_style"),
            mascot_intensity=data.get("mascot_intensity"),
            background_activity=data.get("background_activity"),
            motion_intensity=data.get("motion_intensity"),
            opening_duration=data.get("opening_duration"),
            outro_duration=data.get("outro_duration"),
            enable_pattern_breaks=data.get("enable_pattern_breaks"),
            enable_audio_sync=data.get("enable_audio_sync"),
            extra=dict(data.get("extra", {})),
        )
