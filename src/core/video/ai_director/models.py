from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class CreativeOverride:
    theme_pack: str | None = None
    camera_style: str | None = None
    mascot_intensity: float | None = None
    background_activity: float | None = None
    motion_intensity: float | None = None
    opening_duration: float | None = None
    outro_duration: float | None = None
    enable_pattern_breaks: bool | None = None
    enable_audio_sync: bool | None = None
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class ProductionPlan:
    title: str
    quiz_type: str
    total_questions: int
    audience: str
    energy_level: float
    pacing_mode: str
    theme_pack: dict[str, Any]
    opening: dict[str, Any]
    question_flow: dict[str, Any]
    pattern_breaks: dict[str, Any]
    mascot: dict[str, Any]
    audio: dict[str, Any]
    outro: dict[str, Any]
    quality: dict[str, Any]
    automation: dict[str, Any]
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "quiz_type": self.quiz_type,
            "total_questions": self.total_questions,
            "audience": self.audience,
            "energy_level": self.energy_level,
            "pacing_mode": self.pacing_mode,
            "theme_pack": dict(self.theme_pack),
            "opening": dict(self.opening),
            "question_flow": dict(self.question_flow),
            "pattern_breaks": dict(self.pattern_breaks),
            "mascot": dict(self.mascot),
            "audio": dict(self.audio),
            "outro": dict(self.outro),
            "quality": dict(self.quality),
            "automation": dict(self.automation),
            "metadata": dict(self.metadata),
        }
