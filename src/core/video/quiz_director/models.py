from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class QuestionDirection:
    question_number: int
    difficulty_score: float
    reading_score: float
    visual_complexity_score: float
    curiosity_score: float
    suspense_score: float
    fun_score: float
    emotion: str
    entry_duration: float
    thinking_duration: float
    reveal_duration: float
    camera_intensity: float
    background_intensity: float
    mascot_intensity: float
    reveal_intensity: float
    surprise_moment: bool
    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "question_number": self.question_number,
            "difficulty_score": self.difficulty_score,
            "reading_score": self.reading_score,
            "visual_complexity_score": (
                self.visual_complexity_score
            ),
            "curiosity_score": self.curiosity_score,
            "suspense_score": self.suspense_score,
            "fun_score": self.fun_score,
            "emotion": self.emotion,
            "entry_duration": self.entry_duration,
            "thinking_duration": self.thinking_duration,
            "reveal_duration": self.reveal_duration,
            "camera_intensity": self.camera_intensity,
            "background_intensity": (
                self.background_intensity
            ),
            "mascot_intensity": self.mascot_intensity,
            "reveal_intensity": self.reveal_intensity,
            "surprise_moment": self.surprise_moment,
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True, slots=True)
class QuizDirectionPlan:
    quiz_type: str
    title: str
    total_questions: int
    questions: tuple[QuestionDirection, ...]
    fatigue_points: tuple[int, ...]
    surprise_points: tuple[int, ...]
    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "quiz_type": self.quiz_type,
            "title": self.title,
            "total_questions": self.total_questions,
            "questions": [
                question.to_dict()
                for question in self.questions
            ],
            "fatigue_points": list(
                self.fatigue_points
            ),
            "surprise_points": list(
                self.surprise_points
            ),
            "metadata": dict(self.metadata),
        }

    def question(
        self,
        number: int,
    ) -> QuestionDirection | None:
        for item in self.questions:
            if item.question_number == int(number):
                return item

        return None
