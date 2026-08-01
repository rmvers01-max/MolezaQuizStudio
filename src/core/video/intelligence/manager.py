from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .analytics import PerformanceAnalyticsEngine
from .models import ProductionFingerprint
from .recommendations import RecommendationEngine
from .repository import IntelligenceRepository


class MolezaIntelligenceManager:
    def __init__(
        self,
        root,
    ):
        self.repository = (
            IntelligenceRepository(
                root
            )
        )

        self.analytics = (
            PerformanceAnalyticsEngine()
        )

        self.recommendations = (
            RecommendationEngine()
        )

    def register_production(
        self,
        *,
        title: str,
        quiz_type: str,
        total_questions: int,
        production_plan: dict[str, Any],
        story_plan: dict[str, Any],
    ) -> ProductionFingerprint:
        theme_pack = dict(
            production_plan.get(
                "theme_pack",
                {}
            )
        )

        opening = dict(
            production_plan.get(
                "opening",
                {}
            )
        )

        question_flow = dict(
            production_plan.get(
                "question_flow",
                {}
            )
        )

        pattern_breaks = dict(
            production_plan.get(
                "pattern_breaks",
                {}
            )
        )

        mascot = dict(
            production_plan.get(
                "mascot",
                {}
            )
        )

        outro = dict(
            production_plan.get(
                "outro",
                {}
            )
        )

        created_at = datetime.now(
            timezone.utc
        ).isoformat()

        production_id = hashlib.sha256(
            (
                f"{title}|{quiz_type}|"
                f"{total_questions}|{created_at}"
            ).encode("utf-8")
        ).hexdigest()[:16]

        chapters = tuple(
            str(item.get("code", ""))
            for item in story_plan.get(
                "chapters",
                []
            )
        )

        fingerprint = ProductionFingerprint(
            production_id=production_id,
            title=str(title),
            quiz_type=str(quiz_type),
            total_questions=max(
                int(total_questions),
                0,
            ),
            theme_pack=str(
                theme_pack.get(
                    "code",
                    ""
                )
            ),
            energy_level=float(
                production_plan.get(
                    "energy_level",
                    0.0
                )
            ),
            pacing_mode=str(
                production_plan.get(
                    "pacing_mode",
                    ""
                )
            ),
            opening_duration=float(
                opening.get(
                    "duration",
                    0.0
                )
            ),
            reveal_duration=float(
                question_flow.get(
                    "reveal_duration",
                    0.0
                )
            ),
            pattern_break_interval=int(
                pattern_breaks.get(
                    "interval",
                    0
                )
            ),
            mascot_intensity=float(
                mascot.get(
                    "intensity",
                    0.0
                )
            ),
            outro_duration=float(
                outro.get(
                    "duration",
                    0.0
                )
            ),
            story_chapters=chapters,
            created_at=created_at,
            metadata={
                "platform_version": "1.0",
            },
        )

        self.repository.append_production(
            fingerprint.to_dict()
        )

        return fingerprint

    def build_intelligence_report(
        self,
    ) -> dict[str, Any]:
        metrics = (
            self.repository
            .load_metrics()
        )

        analysis = self.analytics.analyze(
            metrics
        )

        recommendations = (
            self.recommendations
            .generate(
                analysis
            )
        )

        report = {
            "analysis": analysis,
            "recommendations": [
                item.to_dict()
                for item in recommendations
            ],
            "generated_at": datetime.now(
                timezone.utc
            ).isoformat(),
            "note": (
                "Recomendações baseadas somente nas métricas "
                "importadas pelo usuário."
            ),
        }

        self.repository.save_recommendations(
            report
        )

        return report
