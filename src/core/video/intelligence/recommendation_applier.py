from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class RecommendationOverrideBuilder:
    """
    Converte recomendações em um arquivo sugerido de overrides.

    O arquivo sugerido nunca substitui automaticamente a
    configuração ativa do usuário.
    """

    def build(
        self,
        *,
        production_plan: dict[str, Any],
        recommendations: list[dict[str, Any]],
    ) -> dict[str, Any]:
        result = {
            "theme_pack": None,
            "camera_style": None,
            "mascot_intensity": None,
            "background_activity": None,
            "motion_intensity": None,
            "opening_duration": None,
            "outro_duration": None,
            "enable_pattern_breaks": None,
            "enable_audio_sync": None,
            "extra": {},
        }

        opening = dict(
            production_plan.get(
                "opening",
                {}
            )
        )

        pattern_breaks = dict(
            production_plan.get(
                "pattern_breaks",
                {}
            )
        )

        for recommendation in recommendations:
            code = str(
                recommendation.get(
                    "code",
                    ""
                )
            )

            proposed = dict(
                recommendation.get(
                    "proposed_change",
                    {}
                )
            )

            if code == "shorter_opening":
                current = float(
                    opening.get(
                        "duration",
                        4.2
                    )
                )

                delta = float(
                    proposed.get(
                        "opening_duration_delta",
                        -0.35
                    )
                )

                result[
                    "opening_duration"
                ] = round(
                    min(
                        max(
                            current + delta,
                            3.2,
                        ),
                        5.2,
                    ),
                    2,
                )

            elif code == "faster_middle":
                current_interval = int(
                    pattern_breaks.get(
                        "interval",
                        4
                    )
                )

                interval_delta = int(
                    proposed.get(
                        "pattern_break_interval_delta",
                        -1
                    )
                )

                result[
                    "enable_pattern_breaks"
                ] = True

                result["extra"][
                    "pattern_break_interval"
                ] = max(
                    min(
                        current_interval
                        + interval_delta,
                        8,
                    ),
                    2,
                )

                result["extra"][
                    "middle_entry_duration_delta"
                ] = float(
                    proposed.get(
                        "middle_entry_duration_delta",
                        -0.08
                    )
                )

        result["extra"][
            "source"
        ] = "moleza_intelligence_platform"

        result["extra"][
            "requires_manual_approval"
        ] = True

        return result

    def save(
        self,
        overrides: dict[str, Any],
        path,
    ) -> Path:
        path = Path(path)

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        path.write_text(
            json.dumps(
                overrides,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return path
