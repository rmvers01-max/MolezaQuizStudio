from __future__ import annotations
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class ChoiceVisualProfile:
    code: str
    color_a: tuple[int, int, int]
    color_b: tuple[int, int, int]
    accent: tuple[int, int, int]
    card_glow: float
    image_scale: float
    or_scale: float
    countdown_energy: float
    background_mode: str
    transition_style: str
    metadata: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "code": self.code,
            "color_a": list(self.color_a),
            "color_b": list(self.color_b),
            "accent": list(self.accent),
            "card_glow": self.card_glow,
            "image_scale": self.image_scale,
            "or_scale": self.or_scale,
            "countdown_energy": self.countdown_energy,
            "background_mode": self.background_mode,
            "transition_style": self.transition_style,
            "metadata": dict(self.metadata),
        }
