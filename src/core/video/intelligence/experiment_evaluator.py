from __future__ import annotations

from collections import defaultdict
from statistics import mean
from typing import Any


class ExperimentEvaluator:
    """
    Compara variantes somente quando os dados possuem experiment_id
    e variant_code.

    Não declara vencedor com amostra insuficiente.
    """

    def evaluate(
        self,
        metrics: list[dict[str, Any]],
        minimum_sample: int = 3,
    ) -> dict[str, Any]:
        groups = defaultdict(list)

        for item in metrics:
            experiment_id = item.get(
                "experiment_id"
            )

            variant_code = item.get(
                "variant_code"
            )

            if (
                not experiment_id
                or not variant_code
            ):
                continue

            groups[
                (
                    str(experiment_id),
                    str(variant_code),
                )
            ].append(item)

        experiments = {}

        for (
            experiment_id,
            variant_code,
        ), items in groups.items():
            experiments.setdefault(
                experiment_id,
                {}
            )

            percentages = [
                float(
                    item[
                        "average_percentage_viewed"
                    ]
                )
                for item in items
                if item.get(
                    "average_percentage_viewed"
                )
                is not None
            ]

            retention_30 = [
                float(
                    item[
                        "first_30_seconds_retention"
                    ]
                )
                for item in items
                if item.get(
                    "first_30_seconds_retention"
                )
                is not None
            ]

            experiments[
                experiment_id
            ][variant_code] = {
                "sample_size": len(items),
                "average_percentage_viewed": (
                    round(
                        mean(percentages),
                        3,
                    )
                    if percentages
                    else None
                ),
                "first_30_seconds_retention": (
                    round(
                        mean(retention_30),
                        3,
                    )
                    if retention_30
                    else None
                ),
            }

        results = {}

        for experiment_id, variants in (
            experiments.items()
        ):
            eligible = {
                code: data
                for code, data in variants.items()
                if data["sample_size"]
                >= minimum_sample
            }

            winner = None

            if len(eligible) >= 2:
                winner = max(
                    eligible,
                    key=lambda code: (
                        eligible[code].get(
                            "average_percentage_viewed"
                        )
                        or 0
                    ),
                )

            results[experiment_id] = {
                "variants": variants,
                "winner": winner,
                "status": (
                    "completed"
                    if winner
                    else "collecting_data"
                ),
                "minimum_sample": minimum_sample,
            }

        return {
            "experiments": results,
            "note": (
                "Resultado comparativo simples; não é teste "
                "estatístico conclusivo."
            ),
        }
