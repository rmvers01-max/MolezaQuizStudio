from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class CinematicExperience:
    code: str
    emotion: str
    camera_style: str
    camera_multiplier: float
    light_mode: str
    light_intensity: float
    particle_mode: str
    particle_intensity: float
    color_temperature: float
    vignette: float
    pulse: float
    mascot_action: str
    audio_cue: str
    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "code": self.code,
            "emotion": self.emotion,
            "camera_style": self.camera_style,
            "camera_multiplier": self.camera_multiplier,
            "light_mode": self.light_mode,
            "light_intensity": self.light_intensity,
            "particle_mode": self.particle_mode,
            "particle_intensity": self.particle_intensity,
            "color_temperature": self.color_temperature,
            "vignette": self.vignette,
            "pulse": self.pulse,
            "mascot_action": self.mascot_action,
            "audio_cue": self.audio_cue,
            "metadata": dict(self.metadata),
        }
