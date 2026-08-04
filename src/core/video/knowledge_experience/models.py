from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

@dataclass(frozen=True, slots=True)
class KnowledgeVisualProfile:
    code: str
    category: str
    question_style: str
    options_layout: str
    image_mode: str
    countdown_style: str
    reveal_style: str
    accent_color: tuple[int, int, int]
    secondary_color: tuple[int, int, int]
    background_mode: str
    motion_intensity: float
    particle_intensity: float
    show_explanation: bool
    curiosity_selected: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "code": self.code,
            "category": self.category,
            "question_style": self.question_style,
            "options_layout": self.options_layout,
            "image_mode": self.image_mode,
            "countdown_style": self.countdown_style,
            "reveal_style": self.reveal_style,
            "accent_color": list(self.accent_color),
            "secondary_color": list(self.secondary_color),
            "background_mode": self.background_mode,
            "motion_intensity": self.motion_intensity,
            "particle_intensity": self.particle_intensity,
            "show_explanation": self.show_explanation,
            "curiosity_selected": self.curiosity_selected,
            "metadata": dict(self.metadata),
        }
