from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class StoryBeat:
    question_number: int
    chapter: str
    chapter_progress: float
    emotional_tone: str
    camera_multiplier: float
    lighting_multiplier: float
    particle_multiplier: float
    mascot_multiplier: float
    reveal_multiplier: float
    contrast_shift: float
    saturation_shift: float
    warmth_shift: float
    finale: bool
    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "question_number": self.question_number,
            "chapter": self.chapter,
            "chapter_progress": self.chapter_progress,
            "emotional_tone": self.emotional_tone,
            "camera_multiplier": self.camera_multiplier,
            "lighting_multiplier": self.lighting_multiplier,
            "particle_multiplier": self.particle_multiplier,
            "mascot_multiplier": self.mascot_multiplier,
            "reveal_multiplier": self.reveal_multiplier,
            "contrast_shift": self.contrast_shift,
            "saturation_shift": self.saturation_shift,
            "warmth_shift": self.warmth_shift,
            "finale": self.finale,
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True, slots=True)
class StoryArcPlan:
    title: str
    quiz_type: str
    total_questions: int
    beats: tuple[StoryBeat, ...]
    chapters: tuple[dict[str, Any], ...]
    finale_message: str
    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "quiz_type": self.quiz_type,
            "total_questions": self.total_questions,
            "beats": [
                beat.to_dict()
                for beat in self.beats
            ],
            "chapters": [
                dict(chapter)
                for chapter in self.chapters
            ],
            "finale_message": self.finale_message,
            "metadata": dict(self.metadata),
        }

    def beat(
        self,
        question_number: int,
    ) -> StoryBeat | None:
        for beat in self.beats:
            if (
                beat.question_number
                == int(question_number)
            ):
                return beat

        return None
