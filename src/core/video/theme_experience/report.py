from __future__ import annotations

import json
from pathlib import Path


class ThemeExperienceReportWriter:
    def save(self, profile, path):
        path = Path(path)
        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )
        path.write_text(
            json.dumps(
                {
                    "theme_experience_version": "1.0",
                    "profile": profile.to_dict(),
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
        return path
