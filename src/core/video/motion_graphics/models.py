from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

@dataclass(frozen=True, slots=True)
class MotionPreset:
    code: str
    target: str
    entry_style: str
    exit_style: str
    easing: str
    duration: float
    scale_from: float
    scale_to: float
    glow: float
    blur: float
    shake: float
    particle_burst: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self):
        return {
            "code": self.code, "target": self.target,
            "entry_style": self.entry_style, "exit_style": self.exit_style,
            "easing": self.easing, "duration": self.duration,
            "scale_from": self.scale_from, "scale_to": self.scale_to,
            "glow": self.glow, "blur": self.blur, "shake": self.shake,
            "particle_burst": self.particle_burst,
            "metadata": dict(self.metadata),
        }

@dataclass(frozen=True, slots=True)
class MotionGraphicsPlan:
    scene_kind: str
    category: str
    question_number: int
    title_preset: MotionPreset
    card_preset: MotionPreset
    counter_preset: MotionPreset
    reveal_preset: MotionPreset
    badge_preset: MotionPreset
    progress_preset: MotionPreset
    transition_style: str
    fps: int
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self):
        return {
            "scene_kind": self.scene_kind,
            "category": self.category,
            "question_number": self.question_number,
            "title_preset": self.title_preset.to_dict(),
            "card_preset": self.card_preset.to_dict(),
            "counter_preset": self.counter_preset.to_dict(),
            "reveal_preset": self.reveal_preset.to_dict(),
            "badge_preset": self.badge_preset.to_dict(),
            "progress_preset": self.progress_preset.to_dict(),
            "transition_style": self.transition_style,
            "fps": self.fps,
            "metadata": dict(self.metadata),
        }
