from __future__ import annotations


class IntelligentTimingEngine:
    """
    Calcula tempos-base por pergunta.

    Esses valores são mínimos. A duração da narração continua
    tendo prioridade no LegacyVideoGenerator.
    """

    def calculate(
        self,
        *,
        analysis: dict,
        base_response_time: float,
        quiz_type: str,
    ) -> dict[str, float]:
        difficulty = float(
            analysis.get(
                "difficulty",
                40.0
            )
        )

        reading = float(
            analysis.get(
                "reading",
                30.0
            )
        )

        suspense = float(
            analysis.get(
                "suspense",
                35.0
            )
        )

        entry = (
            0.72
            + reading / 100 * 0.38
        )

        if quiz_type == "preferencia":
            entry = min(
                entry,
                0.92,
            )

        thinking = float(
            base_response_time
        )

        thinking += (
            difficulty - 50.0
        ) / 100 * 1.6

        thinking += (
            reading - 45.0
        ) / 100 * 0.7

        reveal = (
            1.45
            + suspense / 100 * 0.75
        )

        if bool(
            analysis.get(
                "surprise",
                False
            )
        ):
            reveal += 0.28

        return {
            "entry": round(
                min(
                    max(entry, 0.68),
                    1.35,
                ),
                2,
            ),
            "thinking": round(
                min(
                    max(thinking, 2.5),
                    8.0,
                ),
                2,
            ),
            "reveal": round(
                min(
                    max(reveal, 1.35),
                    2.85,
                ),
                2,
            ),
        }
