from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

@dataclass(frozen=True, slots=True)
class CuriosityItem:
    title: str
    text: str
    subject: str = ""
    image_path: str | None = None
    icon: str = "💡"
    source_label: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "text": self.text,
            "subject": self.subject,
            "image_path": self.image_path,
            "icon": self.icon,
            "source_label": self.source_label,
            "metadata": dict(self.metadata),
        }

@dataclass(frozen=True, slots=True)
class CuriosityPlan:
    enabled: bool
    quiz_type: str
    category: str
    items: tuple[CuriosityItem, ...]
    duration: float
    transition_text: str
    mascot_pose: str
    visual_style: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "enabled": self.enabled,
            "quiz_type": self.quiz_type,
            "category": self.category,
            "items": [item.to_dict() for item in self.items],
            "duration": self.duration,
            "transition_text": self.transition_text,
            "mascot_pose": self.mascot_pose,
            "visual_style": self.visual_style,
            "metadata": dict(self.metadata),
        }
