from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class ThemeExperienceProfile:
    category: str
    engine_code: str
    background_mode: str
    motif_style: str
    transition_style: str
    countdown_style: str
    decorative_density: float
    motion_speed: float
    icon_set: tuple[str, ...]
    accent_color: tuple[int, int, int]
    secondary_color: tuple[int, int, int]
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "category": self.category,
            "engine_code": self.engine_code,
            "background_mode": self.background_mode,
            "motif_style": self.motif_style,
            "transition_style": self.transition_style,
            "countdown_style": self.countdown_style,
            "decorative_density": self.decorative_density,
            "motion_speed": self.motion_speed,
            "icon_set": list(self.icon_set),
            "accent_color": list(self.accent_color),
            "secondary_color": list(self.secondary_color),
            "metadata": dict(self.metadata),
        }
