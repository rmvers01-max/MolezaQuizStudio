from __future__ import annotations

import math
import re
from typing import Any


class QuestionAnalyzer:
    """
    Analisa apenas características observáveis da pergunta.

    A dificuldade é uma estimativa editorial interna, não uma
    medição objetiva do conhecimento do público.
    """

    RARE_HINTS = (
        "qual destas",
        "qual desses",
        "identifique",
        "reconheça",
        "capital",
        "bandeira",
        "símbolo",
        "correto",
        "verdadeiro",
        "falso",
    )

    EASY_HINTS = (
        "brasil",
        "estados unidos",
        "frança",
        "alemanha",
        "italia",
        "portugal",
        "japão",
        "china",
        "argentina",
    )

    def analyze(
        self,
        *,
        question: dict[str, Any],
        quiz_type: str,
        question_number: int,
        total_questions: int,
    ) -> dict[str, float | str | bool]:
        text = str(
            question.get(
                "pergunta",
                ""
            )
        ).strip()

        alternatives = [
            str(value)
            for value in question.get(
                "alternativas",
                []
            )
        ]

        has_image = bool(
            question.get(
                "imagem"
            )
            or question.get(
                "imagem_a"
            )
            or question.get(
                "imagem_b"
            )
        )

        word_count = len(
            re.findall(
                r"\w+",
                text,
                flags=re.UNICODE,
            )
        )

        alternative_words = sum(
            len(
                re.findall(
                    r"\w+",
                    option,
                    flags=re.UNICODE,
                )
            )
            for option in alternatives
        )

        reading_score = min(
            (
                word_count * 4.2
                + alternative_words * 1.6
            ),
            100.0,
        )

        visual_complexity = (
            42.0
            if has_image
            else 18.0
        )

        visual_complexity += min(
            len(alternatives) * 7.5,
            35.0,
        )

        normalized = text.lower()

        rarity = sum(
            1
            for hint in self.RARE_HINTS
            if hint in normalized
        )

        familiarity = sum(
            1
            for hint in self.EASY_HINTS
            if hint in normalized
        )

        difficulty = (
            34.0
            + rarity * 9.0
            + max(
                len(alternatives) - 2,
                0,
            )
            * 6.0
            + (
                7.0
                if has_image
                else 0.0
            )
            - familiarity * 8.0
        )

        if quiz_type == "preferencia":
            difficulty = 24.0

        difficulty = min(
            max(difficulty, 8.0),
            96.0,
        )

        curiosity = min(
            38.0
            + (
                18.0
                if has_image
                else 4.0
            )
            + rarity * 8.0,
            96.0,
        )

        suspense = min(
            difficulty * 0.62
            + curiosity * 0.30,
            96.0,
        )

        fun = (
            82.0
            if quiz_type == "preferencia"
            else min(
                48.0
                + len(alternatives) * 5.0,
                82.0,
            )
        )

        emotion = self._emotion(
            curiosity=curiosity,
            suspense=suspense,
            fun=fun,
            difficulty=difficulty,
        )

        position_ratio = (
            question_number
            / max(
                total_questions,
                1,
            )
        )

        surprise = (
            question_number > 1
            and (
                question_number % 5 == 0
                or (
                    difficulty >= 78
                    and position_ratio >= 0.35
                )
            )
        )

        return {
            "difficulty": round(
                difficulty,
                2,
            ),
            "reading": round(
                reading_score,
                2,
            ),
            "visual_complexity": round(
                min(
                    visual_complexity,
                    100.0,
                ),
                2,
            ),
            "curiosity": round(
                curiosity,
                2,
            ),
            "suspense": round(
                suspense,
                2,
            ),
            "fun": round(
                fun,
                2,
            ),
            "emotion": emotion,
            "surprise": surprise,
            "word_count": word_count,
            "alternative_count": len(
                alternatives
            ),
            "has_image": has_image,
        }

    def _emotion(
        self,
        *,
        curiosity,
        suspense,
        fun,
        difficulty,
    ) -> str:
        scores = {
            "curiosity": curiosity,
            "suspense": suspense,
            "fun": fun,
            "challenge": difficulty,
        }

        return max(
            scores,
            key=scores.get,
        )
