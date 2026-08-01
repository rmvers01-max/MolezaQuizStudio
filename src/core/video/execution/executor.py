from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import ExecutionSettings


class ProductionPlanExecutor:
    """
    Converte o plano criativo em configurações seguras de execução.

    As durações são limitadas a faixas razoáveis para impedir que
    um arquivo de override inválido torne o vídeo ilegível.
    """

    def build_settings(
        self,
        production_plan: dict[str, Any],
    ) -> ExecutionSettings:
        plan = dict(
            production_plan or {}
        )

        opening = dict(
            plan.get(
                "opening",
                {}
            )
        )

        question_flow = dict(
            plan.get(
                "question_flow",
                {}
            )
        )

        pattern_breaks = dict(
            plan.get(
                "pattern_breaks",
                {}
            )
        )

        mascot = dict(
            plan.get(
                "mascot",
                {}
            )
        )

        audio = dict(
            plan.get(
                "audio",
                {}
            )
        )

        outro = dict(
            plan.get(
                "outro",
                {}
            )
        )

        quality = dict(
            plan.get(
                "quality",
                {}
            )
        )

        return ExecutionSettings(
            theme_pack=dict(
                plan.get(
                    "theme_pack",
                    {}
                )
            ),
            opening_enabled=bool(
                opening.get(
                    "enabled",
                    True
                )
            ),
            opening_duration=self._clamp(
                opening.get(
                    "duration",
                    4.2
                ),
                3.2,
                5.2,
            ),
            question_entry_duration=self._clamp(
                question_flow.get(
                    "entry_duration",
                    0.90
                ),
                0.65,
                1.40,
            ),
            reveal_duration=self._clamp(
                question_flow.get(
                    "reveal_duration",
                    1.90
                ),
                1.30,
                3.20,
            ),
            pattern_breaks_enabled=bool(
                pattern_breaks.get(
                    "enabled",
                    True
                )
            ),
            pattern_break_interval=max(
                min(
                    int(
                        pattern_breaks.get(
                            "interval",
                            4
                        )
                    ),
                    8,
                ),
                2,
            ),
            pattern_break_intensity=self._clamp(
                pattern_breaks.get(
                    "intensity",
                    0.82
                ),
                0.0,
                1.0,
            ),
            mascot_enabled=bool(
                mascot.get(
                    "enabled",
                    True
                )
            ),
            mascot_intensity=self._clamp(
                mascot.get(
                    "intensity",
                    0.80
                ),
                0.0,
                1.25,
            ),
            audio_sync_enabled=bool(
                audio.get(
                    "sync_enabled",
                    True
                )
            ),
            outro_enabled=bool(
                outro.get(
                    "enabled",
                    True
                )
            ),
            outro_duration=self._clamp(
                outro.get(
                    "duration",
                    5.0
                ),
                3.5,
                8.0,
            ),
            quality_profile=str(
                quality.get(
                    "profile",
                    "balanced"
                )
            ),
            metadata={
                "source": (
                    "ai_production_plan"
                ),
                "executor_version": "1.0",
                "automation": dict(
                    plan.get(
                        "automation",
                        {}
                    )
                ),
            },
        )

    def save_report(
        self,
        settings: ExecutionSettings,
        path,
    ) -> Path:
        path = Path(path)

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        path.write_text(
            json.dumps(
                settings.to_dict(),
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return path

    def _clamp(
        self,
        value,
        minimum: float,
        maximum: float,
    ) -> float:
        try:
            numeric = float(value)
        except (
            TypeError,
            ValueError,
        ):
            numeric = minimum

        return round(
            min(
                max(
                    numeric,
                    minimum,
                ),
                maximum,
            ),
            3,
        )
