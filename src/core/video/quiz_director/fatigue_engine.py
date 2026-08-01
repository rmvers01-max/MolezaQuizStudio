from __future__ import annotations


class ViewerFatigueEngine:
    """
    Marca pontos onde o vídeo corre maior risco de parecer repetitivo.

    O cálculo considera posição e distância desde a última mudança.
    """

    def calculate(
        self,
        *,
        total_questions: int,
        surprise_points: list[int],
    ) -> tuple[int, ...]:
        total = max(
            int(total_questions),
            1,
        )

        surprises = set(
            int(value)
            for value in surprise_points
        )

        points = []

        last_change = 1

        for number in range(
            2,
            total + 1,
        ):
            if number in surprises:
                last_change = number
                continue

            distance = (
                number - last_change
            )

            if distance >= 4:
                points.append(number)
                last_change = number

        return tuple(points)
