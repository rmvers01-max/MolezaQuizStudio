from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass(frozen=True, slots=True)
class ExperimentVariant:
    code: str
    label: str
    description: str
    creative_overrides: dict[str, Any]
    hypothesis: str
    primary_metric: str
    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "code": self.code,
            "label": self.label,
            "description": self.description,
            "creative_overrides": dict(
                self.creative_overrides
            ),
            "hypothesis": self.hypothesis,
            "primary_metric": self.primary_metric,
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True, slots=True)
class ABTestPlan:
    experiment_id: str
    title: str
    quiz_type: str
    created_at: str
    variants: tuple[ExperimentVariant, ...]
    recommended_variant: str
    status: str
    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "experiment_id": self.experiment_id,
            "title": self.title,
            "quiz_type": self.quiz_type,
            "created_at": self.created_at,
            "variants": [
                variant.to_dict()
                for variant in self.variants
            ],
            "recommended_variant": (
                self.recommended_variant
            ),
            "status": self.status,
            "metadata": dict(self.metadata),
        }


class ABTestPlanner:
    """
    Gera variantes conservadoras para o próximo vídeo.

    Nenhuma variante é aplicada automaticamente.
    """

    def create_plan(
        self,
        *,
        title: str,
        quiz_type: str,
        production_plan: dict[str, Any],
        recommendations: list[dict[str, Any]],
    ) -> ABTestPlan:
        created_at = datetime.now(
            timezone.utc
        ).isoformat()

        experiment_id = hashlib.sha256(
            (
                f"{title}|{quiz_type}|{created_at}"
            ).encode("utf-8")
        ).hexdigest()[:16]

        control = ExperimentVariant(
            code="control",
            label="Controle",
            description=(
                "Mantém todas as decisões automáticas atuais."
            ),
            creative_overrides={},
            hypothesis=(
                "O estilo atual continua sendo a melhor referência."
            ),
            primary_metric=(
                "average_percentage_viewed"
            ),
        )

        variants = [control]

        recommendation_codes = {
            str(item.get("code", ""))
            for item in recommendations
        }

        if "shorter_opening" in recommendation_codes:
            current_duration = float(
                production_plan.get(
                    "opening",
                    {}
                ).get(
                    "duration",
                    4.2
                )
            )

            variants.append(
                ExperimentVariant(
                    code="opening_shorter",
                    label="Abertura mais curta",
                    description=(
                        "Reduz a abertura sem remover o hook."
                    ),
                    creative_overrides={
                        "opening_duration": round(
                            max(
                                current_duration - 0.35,
                                3.2,
                            ),
                            2,
                        )
                    },
                    hypothesis=(
                        "Uma primeira pergunta mais rápida pode "
                        "melhorar a retenção inicial."
                    ),
                    primary_metric=(
                        "first_30_seconds_retention"
                    ),
                )
            )

        if "faster_middle" in recommendation_codes:
            current_interval = int(
                production_plan.get(
                    "pattern_breaks",
                    {}
                ).get(
                    "interval",
                    4
                )
            )

            variants.append(
                ExperimentVariant(
                    code="middle_faster",
                    label="Meio mais dinâmico",
                    description=(
                        "Aumenta a frequência das mudanças "
                        "visuais no bloco intermediário."
                    ),
                    creative_overrides={
                        "enable_pattern_breaks": True,
                        "extra": {
                            "pattern_break_interval": max(
                                current_interval - 1,
                                2,
                            ),
                            "middle_entry_duration_delta": -0.08,
                        },
                    },
                    hypothesis=(
                        "Um bloco intermediário mais dinâmico pode "
                        "elevar o percentual médio assistido."
                    ),
                    primary_metric=(
                        "average_percentage_viewed"
                    ),
                )
            )

        if len(variants) == 1:
            variants.append(
                ExperimentVariant(
                    code="energy_soft_test",
                    label="Variação leve de energia",
                    description=(
                        "Testa uma pequena redução de movimento "
                        "sem mudar a identidade visual."
                    ),
                    creative_overrides={
                        "motion_intensity": 0.46,
                        "background_activity": 0.50,
                    },
                    hypothesis=(
                        "Menos estímulo pode melhorar a leitura "
                        "em quizzes com muitas alternativas."
                    ),
                    primary_metric=(
                        "average_percentage_viewed"
                    ),
                )
            )

        return ABTestPlan(
            experiment_id=experiment_id,
            title=str(title),
            quiz_type=str(quiz_type),
            created_at=created_at,
            variants=tuple(variants),
            recommended_variant=(
                variants[1].code
                if len(variants) > 1
                else "control"
            ),
            status="planned",
            metadata={
                "automatic_application": False,
                "minimum_sample_per_variant": 3,
            },
        )

    def save(
        self,
        plan: ABTestPlan,
        path,
    ) -> Path:
        path = Path(path)

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        path.write_text(
            json.dumps(
                plan.to_dict(),
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return path
