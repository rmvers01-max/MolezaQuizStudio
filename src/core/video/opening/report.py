from __future__ import annotations

import json
from pathlib import Path


class OpeningReportWriter:
    def save(
        self,
        direction: dict,
        path,
    ) -> Path:
        path = Path(path)

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        payload = {
            "opening_version": "2.0",
            "opening_type": direction.get(
                "nome"
            ),
            "category": direction.get(
                "categoria"
            ),
            "hook": direction.get(
                "hook_texto"
            ),
            "cta": direction.get(
                "desafio_texto"
            ),
            "duration": direction.get(
                "duracao"
            ),
            "energy": direction.get(
                "intensidade"
            ),
            "camera": direction.get(
                "camera_style"
            ),
            "transition": direction.get(
                "transition_style"
            ),
            "mascot_sequence": direction.get(
                "mascot_sequence",
                [],
            ),
            "teaser_items": direction.get(
                "teaser_items",
                [],
            ),
            "audio_layers": direction.get(
                "audio_layers",
                [],
            ),
            "quality": direction.get(
                "quality",
                {},
            ),
            "metadata": direction.get(
                "metadata",
                {},
            ),
        }

        path.write_text(
            json.dumps(
                payload,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return path
