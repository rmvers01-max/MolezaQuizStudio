from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import (
    StoryArcPlan,
    StoryBeat,
)


class CinematicStoryDirector:
    """
    Constrói uma progressão narrativa para o vídeo inteiro.

    O motor não altera o conteúdo da pergunta. Ele organiza a
    intensidade visual ao longo da produção.
    """

    CHAPTERS = (
        {
            "code": "warm_up",
            "start": 0.00,
            "end": 0.18,
            "tone": "curiosity",
            "camera": 0.82,
            "lighting": 0.88,
            "particles": 0.78,
            "mascot": 0.82,
            "reveal": 0.82,
            "contrast": -0.03,
            "saturation": -0.02,
            "warmth": 0.02,
        },
        {
            "code": "engagement",
            "start": 0.18,
            "end": 0.50,
            "tone": "fun",
            "camera": 0.94,
            "lighting": 0.98,
            "particles": 0.92,
            "mascot": 0.94,
            "reveal": 0.94,
            "contrast": 0.00,
            "saturation": 0.02,
            "warmth": 0.01,
        },
        {
            "code": "escalation",
            "start": 0.50,
            "end": 0.78,
            "tone": "challenge",
            "camera": 1.05,
            "lighting": 1.06,
            "particles": 1.02,
            "mascot": 1.02,
            "reveal": 1.08,
            "contrast": 0.03,
            "saturation": 0.04,
            "warmth": 0.00,
        },
        {
            "code": "climax",
            "start": 0.78,
            "end": 0.93,
            "tone": "suspense",
            "camera": 1.12,
            "lighting": 1.12,
            "particles": 1.08,
            "mascot": 1.08,
            "reveal": 1.15,
            "contrast": 0.05,
            "saturation": 0.05,
            "warmth": -0.01,
        },
        {
            "code": "grand_finale",
            "start": 0.93,
            "end": 1.01,
            "tone": "victory",
            "camera": 1.16,
            "lighting": 1.18,
            "particles": 1.15,
            "mascot": 1.16,
            "reveal": 1.22,
            "contrast": 0.06,
            "saturation": 0.07,
            "warmth": 0.04,
        },
    )

    def create_plan(
        self,
        *,
        title: str,
        quiz_type: str,
        total_questions: int,
        question_plan: dict[str, Any],
    ) -> StoryArcPlan:
        total = max(
            int(total_questions),
            1,
        )

        question_directions = {
            int(item["question_number"]): item
            for item in question_plan.get(
                "questions",
                []
            )
            if "question_number" in item
        }

        beats = []

        for number in range(
            1,
            total + 1,
        ):
            ratio = (
                number / total
            )

            chapter = self._chapter(
                ratio
            )

            local_progress = self._local_progress(
                ratio,
                chapter,
            )

            question_direction = (
                question_directions.get(
                    number,
                    {}
                )
            )

            surprise = bool(
                question_direction.get(
                    "surprise_moment",
                    False
                )
            )

            suspense = float(
                question_direction.get(
                    "suspense_score",
                    45.0
                )
            )

            reveal_boost = (
                0.10
                if surprise
                else 0.0
            )

            camera_boost = (
                suspense
                / 100
                * 0.08
            )

            finale = (
                chapter["code"]
                == "grand_finale"
            )

            beats.append(
                StoryBeat(
                    question_number=number,
                    chapter=str(
                        chapter["code"]
                    ),
                    chapter_progress=round(
                        local_progress,
                        3,
                    ),
                    emotional_tone=str(
                        chapter["tone"]
                    ),
                    camera_multiplier=round(
                        min(
                            float(
                                chapter["camera"]
                            )
                            + camera_boost,
                            1.30,
                        ),
                        3,
                    ),
                    lighting_multiplier=round(
                        float(
                            chapter["lighting"]
                        ),
                        3,
                    ),
                    particle_multiplier=round(
                        min(
                            float(
                                chapter["particles"]
                            )
                            + (
                                0.08
                                if surprise
                                else 0.0
                            ),
                            1.30,
                        ),
                        3,
                    ),
                    mascot_multiplier=round(
                        min(
                            float(
                                chapter["mascot"]
                            )
                            + (
                                0.08
                                if surprise
                                else 0.0
                            ),
                            1.30,
                        ),
                        3,
                    ),
                    reveal_multiplier=round(
                        min(
                            float(
                                chapter["reveal"]
                            )
                            + reveal_boost,
                            1.35,
                        ),
                        3,
                    ),
                    contrast_shift=float(
                        chapter["contrast"]
                    ),
                    saturation_shift=float(
                        chapter["saturation"]
                    ),
                    warmth_shift=float(
                        chapter["warmth"]
                    ),
                    finale=finale,
                    metadata={
                        "surprise_source": (
                            surprise
                        ),
                        "question_suspense": (
                            suspense
                        ),
                    },
                )
            )

        return StoryArcPlan(
            title=str(title),
            quiz_type=str(quiz_type),
            total_questions=total,
            beats=tuple(beats),
            chapters=tuple(
                {
                    key: value
                    for key, value
                    in chapter.items()
                    if key not in {
                        "camera",
                        "lighting",
                        "particles",
                        "mascot",
                        "reveal",
                        "contrast",
                        "saturation",
                        "warmth",
                    }
                }
                for chapter in self.CHAPTERS
            ),
            finale_message=(
                self._finale_message(
                    quiz_type
                )
            ),
            metadata={
                "director_version": "1.0",
                "purpose": (
                    "narrative_visual_progression"
                ),
            },
        )

    def save(
        self,
        plan: StoryArcPlan,
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

    def _chapter(
        self,
        ratio: float,
    ) -> dict[str, Any]:
        for chapter in self.CHAPTERS:
            if (
                float(chapter["start"])
                <= ratio
                < float(chapter["end"])
            ):
                return chapter

        return self.CHAPTERS[-1]

    def _local_progress(
        self,
        ratio: float,
        chapter: dict[str, Any],
    ) -> float:
        start = float(
            chapter["start"]
        )

        end = float(
            chapter["end"]
        )

        if end <= start:
            return 1.0

        return min(
            max(
                (
                    ratio - start
                )
                / (
                    end - start
                ),
                0.0,
            ),
            1.0,
        )

    def _finale_message(
        self,
        quiz_type: str,
    ) -> str:
        if quiz_type == "preferencia":
            return (
                "Quantas escolhas foram iguais às suas?"
            )

        return (
            "Quantas respostas você acertou?"
        )
