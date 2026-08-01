from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from .fatigue_engine import ViewerFatigueEngine
from .models import (
    QuestionDirection,
    QuizDirectionPlan,
)
from .question_analyzer import QuestionAnalyzer
from .timing_engine import IntelligentTimingEngine


class IntelligentQuizDirector:
    def __init__(self):
        self.analyzer = QuestionAnalyzer()
        self.timing = IntelligentTimingEngine()
        self.fatigue = ViewerFatigueEngine()

    def create_plan(
        self,
        *,
        title: str,
        quiz_type: str,
        questions: list[dict[str, Any]],
        base_response_time: float,
        production_plan: dict[str, Any],
    ) -> QuizDirectionPlan:
        total = max(
            len(questions),
            1,
        )

        production_energy = float(
            production_plan.get(
                "energy_level",
                0.68
            )
        )

        directions = []
        surprise_points = []

        for number, question in enumerate(
            questions,
            start=1,
        ):
            analysis = self.analyzer.analyze(
                question=question,
                quiz_type=quiz_type,
                question_number=number,
                total_questions=total,
            )

            times = self.timing.calculate(
                analysis=analysis,
                base_response_time=(
                    base_response_time
                ),
                quiz_type=quiz_type,
            )

            surprise = bool(
                analysis["surprise"]
            )

            if surprise:
                surprise_points.append(
                    number
                )

            difficulty = float(
                analysis["difficulty"]
            )

            suspense = float(
                analysis["suspense"]
            )

            camera = (
                0.38
                + production_energy * 0.32
                + suspense / 100 * 0.18
            )

            background = (
                0.34
                + production_energy * 0.26
                - float(
                    analysis[
                        "visual_complexity"
                    ]
                )
                / 100
                * 0.16
            )

            mascot = (
                0.45
                + float(
                    analysis["fun"]
                )
                / 100
                * 0.36
            )

            reveal_intensity = (
                0.52
                + difficulty / 100 * 0.26
                + (
                    0.14
                    if surprise
                    else 0.0
                )
            )

            directions.append(
                QuestionDirection(
                    question_number=number,
                    difficulty_score=round(
                        difficulty,
                        2,
                    ),
                    reading_score=float(
                        analysis["reading"]
                    ),
                    visual_complexity_score=float(
                        analysis[
                            "visual_complexity"
                        ]
                    ),
                    curiosity_score=float(
                        analysis["curiosity"]
                    ),
                    suspense_score=round(
                        suspense,
                        2,
                    ),
                    fun_score=float(
                        analysis["fun"]
                    ),
                    emotion=str(
                        analysis["emotion"]
                    ),
                    entry_duration=float(
                        times["entry"]
                    ),
                    thinking_duration=float(
                        times["thinking"]
                    ),
                    reveal_duration=float(
                        times["reveal"]
                    ),
                    camera_intensity=round(
                        min(
                            max(camera, 0.25),
                            0.95,
                        ),
                        2,
                    ),
                    background_intensity=round(
                        min(
                            max(
                                background,
                                0.20,
                            ),
                            0.78,
                        ),
                        2,
                    ),
                    mascot_intensity=round(
                        min(
                            max(mascot, 0.35),
                            1.0,
                        ),
                        2,
                    ),
                    reveal_intensity=round(
                        min(
                            max(
                                reveal_intensity,
                                0.45,
                            ),
                            1.0,
                        ),
                        2,
                    ),
                    surprise_moment=surprise,
                    metadata={
                        "word_count": (
                            analysis[
                                "word_count"
                            ]
                        ),
                        "alternative_count": (
                            analysis[
                                "alternative_count"
                            ]
                        ),
                        "has_image": (
                            analysis[
                                "has_image"
                            ]
                        ),
                    },
                )
            )

        fatigue_points = (
            self.fatigue.calculate(
                total_questions=total,
                surprise_points=(
                    surprise_points
                ),
            )
        )

        return QuizDirectionPlan(
            quiz_type=str(quiz_type),
            title=str(title),
            total_questions=len(
                questions
            ),
            questions=tuple(
                directions
            ),
            fatigue_points=fatigue_points,
            surprise_points=tuple(
                surprise_points
            ),
            metadata={
                "director_version": "1.0",
                "seed": self._seed(
                    f"{title}|{quiz_type}"
                ),
                "difficulty_note": (
                    "Estimativa editorial interna; "
                    "não mede conhecimento real do público."
                ),
            },
        )

    def save(
        self,
        plan: QuizDirectionPlan,
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

    def _seed(
        self,
        value,
    ) -> int:
        digest = hashlib.sha256(
            str(value).encode(
                "utf-8"
            )
        ).hexdigest()

        return int(
            digest[:8],
            16,
        )
