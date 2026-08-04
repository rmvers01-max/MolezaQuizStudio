from __future__ import annotations

import hashlib

from .hook_library import OpeningHookLibrary
from .opening_profile import OpeningProfile
from .quality_analyzer import OpeningQualityAnalyzer


class OpeningDirector:
    """
    AAA Opening Director 2.0.

    Decide gancho, teaser, câmera, CTA, mascote e transição com base
    no conteúdo já analisado pelo Intelligent Production Engine.
    """

    CAMERA_BY_CATEGORY = {
        "flags_geography": "discovery_push",
        "preference": "competition_push",
        "animals": "soft_discovery",
        "food": "playful_bounce",
        "sports": "fast_push",
        "characters": "mystery_reveal",
        "general_knowledge": "hero_push",
    }

    TRANSITION_BY_CATEGORY = {
        "flags_geography": "flag_wipe",
        "preference": "split_choice",
        "animals": "soft_light_wipe",
        "food": "color_pop",
        "sports": "speed_wipe",
        "characters": "mystery_flash",
        "general_knowledge": "light_wipe",
    }

    MASCOT_BY_CATEGORY = {
        "flags_geography": (
            "wave",
            "thinking",
            "point_left",
        ),
        "preference": (
            "wave",
            "point_left",
            "point_right",
        ),
        "animals": (
            "wave",
            "happy",
            "point_left",
        ),
        "food": (
            "happy",
            "thinking",
            "celebrate",
        ),
        "sports": (
            "wave",
            "celebrate",
            "point_right",
        ),
        "characters": (
            "thinking",
            "happy",
            "point_left",
        ),
        "general_knowledge": (
            "wave",
            "thinking",
            "point_right",
        ),
    }

    def __init__(self):
        self.hooks = OpeningHookLibrary()
        self.quality = OpeningQualityAnalyzer()

    def escolher(
        self,
        titulo: str,
        total_perguntas: int,
        retention_plan: dict | None = None,
        quiz_type: str | None = None,
        production_plan: dict | None = None,
    ) -> dict:
        production_plan = dict(
            production_plan or {}
        )

        content_profile = dict(
            production_plan.get(
                "content_profile",
                {},
            )
        )

        category = str(
            content_profile.get(
                "category",
                "preference"
                if quiz_type == "preferencia"
                else "general_knowledge",
            )
        )

        hook_data = self.hooks.choose(
            category=category,
            title=titulo,
            total_questions=total_perguntas,
        )

        mode = str(
            production_plan.get(
                "production_mode",
                "",
            )
        )

        base_duration = (
            3.85
            if mode == "compact_high_energy"
            else 4.25
            if category == "preference"
            else 4.15
        )

        retention_limit = float(
            (
                retention_plan
                or {}
            ).get(
                "abertura_maxima",
                4.6,
            )
        )

        duration = min(
            max(
                base_duration,
                3.45,
            ),
            retention_limit,
            4.8,
        )

        intensity = {
            "preference": 0.94,
            "sports": 0.92,
            "characters": 0.90,
            "flags_geography": 0.86,
            "food": 0.90,
            "animals": 0.78,
            "general_knowledge": 0.82,
        }.get(
            category,
            0.82,
        )

        profile = OpeningProfile(
            nome=(
                f"AAA {category.replace('_', ' ').title()}"
            ),
            duracao=round(
                duration,
                2,
            ),
            hook_texto=hook_data[
                "hook"
            ],
            desafio_texto=hook_data[
                "cta"
            ],
            mostrar_quantidade=True,
            usar_mascote=True,
            intensidade=intensity,
            primeiro_quadro_impactante=True,
            categoria=category,
            camera_style=self.CAMERA_BY_CATEGORY.get(
                category,
                "hero_push",
            ),
            transition_style=(
                self.TRANSITION_BY_CATEGORY.get(
                    category,
                    "light_wipe",
                )
            ),
            mascot_sequence=(
                self.MASCOT_BY_CATEGORY.get(
                    category,
                    self.MASCOT_BY_CATEGORY[
                        "general_knowledge"
                    ],
                )
            ),
            teaser_items=tuple(
                hook_data["teasers"]
            ),
            metadata={
                "hook_index": hook_data[
                    "hook_index"
                ],
                "production_mode": mode,
                "theme_family": (
                    content_profile.get(
                        "theme_family",
                        content_profile.get(
                            "recommended_theme_family",
                            "",
                        ),
                    )
                ),
            },
        )

        result = profile.to_dict()
        result[
            "total_perguntas"
        ] = max(
            int(total_perguntas),
            1,
        )

        result[
            "quality"
        ] = self.quality.analyze(
            result
        )

        return result
