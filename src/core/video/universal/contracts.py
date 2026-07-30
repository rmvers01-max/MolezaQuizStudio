from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class QuizSceneType(str, Enum):
    OPENING = "opening"
    QUESTION = "question"
    COUNTDOWN = "countdown"
    REVEAL = "reveal"
    CTA = "cta"
    OUTRO = "outro"


class FocusRole(str, Enum):
    PRIMARY = "primary"
    SECONDARY = "secondary"
    SUPPORT = "support"
    DECORATIVE = "decorative"


@dataclass(frozen=True, slots=True)
class SceneElement:
    element_id: str
    role: str
    content_type: str
    content: Any = None
    focus_role: FocusRole = FocusRole.SUPPORT
    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "element_id": self.element_id,
            "role": self.role,
            "content_type": self.content_type,
            "content": self.content,
            "focus_role": self.focus_role.value,
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True, slots=True)
class QuizScene:
    scene_id: str
    scene_type: QuizSceneType
    quiz_type: str
    question_number: int | None
    duration_hint: float
    layout_id: str
    elements: tuple[SceneElement, ...]
    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "scene_id": self.scene_id,
            "scene_type": self.scene_type.value,
            "quiz_type": self.quiz_type,
            "question_number": self.question_number,
            "duration_hint": self.duration_hint,
            "layout_id": self.layout_id,
            "elements": [
                element.to_dict()
                for element in self.elements
            ],
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True, slots=True)
class UniversalQuizPlan:
    quiz_type: str
    title: str
    total_questions: int
    adapter_name: str
    scenes: tuple[QuizScene, ...]
    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "quiz_type": self.quiz_type,
            "title": self.title,
            "total_questions": self.total_questions,
            "adapter_name": self.adapter_name,
            "scenes": [
                scene.to_dict()
                for scene in self.scenes
            ],
            "metadata": dict(self.metadata),
        }
