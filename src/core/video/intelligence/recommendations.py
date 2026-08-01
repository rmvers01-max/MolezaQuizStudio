from __future__ import annotations

from typing import Any

from .models import IntelligenceRecommendation


class RecommendationEngine:
    """
    Gera recomendações com base apenas nas métricas disponíveis.

    Quando a amostra é pequena, mantém recomendações conservadoras.
    """

    def generate(
        self,
        analysis: dict[str, Any],
    ) -> list[IntelligenceRecommendation]:
        sample_size = int(
            analysis.get(
                "sample_size",
                0
            )
        )

        averages = dict(
            analysis.get(
                "averages",
                {}
            )
        )

        recommendations = []

        if sample_size < 3:
            recommendations.append(
                IntelligenceRecommendation(
                    code="collect_more_data",
                    priority="high",
                    title=(
                        "Registrar métricas de mais vídeos"
                    ),
                    explanation=(
                        "Ainda não há dados suficientes para "
                        "alterar automaticamente o estilo."
                    ),
                    proposed_change={
                        "automatic_style_change": False,
                        "minimum_sample": 3,
                    },
                    evidence={
                        "sample_size": sample_size,
                    },
                )
            )

            return recommendations

        retention_30 = averages.get(
            "first_30_seconds_retention"
        )

        if (
            retention_30 is not None
            and retention_30 < 65
        ):
            recommendations.append(
                IntelligenceRecommendation(
                    code="shorter_opening",
                    priority="high",
                    title=(
                        "Testar abertura mais curta"
                    ),
                    explanation=(
                        "A retenção média nos primeiros 30 "
                        "segundos está abaixo do alvo interno."
                    ),
                    proposed_change={
                        "opening_duration_delta": -0.35,
                        "faster_first_question": True,
                    },
                    evidence={
                        "first_30_seconds_retention": (
                            retention_30
                        ),
                    },
                )
            )

        ctr = averages.get(
            "ctr_percent"
        )

        if (
            ctr is not None
            and ctr < 4.5
        ):
            recommendations.append(
                IntelligenceRecommendation(
                    code="thumbnail_title_review",
                    priority="high",
                    title=(
                        "Revisar título e thumbnail"
                    ),
                    explanation=(
                        "O CTR médio informado está baixo. "
                        "A renderização do vídeo não resolve "
                        "sozinha esse problema."
                    ),
                    proposed_change={
                        "video_render_change": False,
                        "review_title_thumbnail": True,
                    },
                    evidence={
                        "ctr_percent": ctr,
                    },
                )
            )

        avg_percentage = averages.get(
            "average_percentage_viewed"
        )

        if (
            avg_percentage is not None
            and avg_percentage < 45
        ):
            recommendations.append(
                IntelligenceRecommendation(
                    code="faster_middle",
                    priority="medium",
                    title=(
                        "Acelerar o bloco intermediário"
                    ),
                    explanation=(
                        "A porcentagem média assistida sugere "
                        "perda de ritmo ao longo do vídeo."
                    ),
                    proposed_change={
                        "middle_entry_duration_delta": -0.08,
                        "pattern_break_interval_delta": -1,
                    },
                    evidence={
                        "average_percentage_viewed": (
                            avg_percentage
                        ),
                    },
                )
            )

        if not recommendations:
            recommendations.append(
                IntelligenceRecommendation(
                    code="preserve_current_strategy",
                    priority="low",
                    title=(
                        "Manter a estratégia atual"
                    ),
                    explanation=(
                        "As métricas informadas não indicam uma "
                        "mudança urgente no estilo de produção."
                    ),
                    proposed_change={
                        "automatic_style_change": False,
                    },
                    evidence={
                        "sample_size": sample_size,
                    },
                )
            )

        return recommendations
