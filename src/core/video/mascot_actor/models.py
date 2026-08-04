from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

@dataclass(frozen=True, slots=True)
class MascotBeat:
    start: float
    end: float
    pose: str
    action: str
    look_target: str
    intensity: float
    enter_style: str = "hold"
    exit_style: str = "hold"
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self):
        return {
            "start": self.start, "end": self.end, "pose": self.pose,
            "action": self.action, "look_target": self.look_target,
            "intensity": self.intensity, "enter_style": self.enter_style,
            "exit_style": self.exit_style, "metadata": dict(self.metadata),
        }

@dataclass(frozen=True, slots=True)
class MascotPerformance:
    scene_kind: str
    question_number: int
    beats: tuple[MascotBeat, ...]
    preferred_side: str
    energy: float
    metadata: dict[str, Any] = field(default_factory=dict)

    def beat_at(self, time: float):
        for beat in self.beats:
            if beat.start <= time <= beat.end:
                return beat
        return self.beats[-1] if self.beats else None

    def to_dict(self):
        return {
            "scene_kind": self.scene_kind,
            "question_number": self.question_number,
            "beats": [b.to_dict() for b in self.beats],
            "preferred_side": self.preferred_side,
            "energy": self.energy,
            "metadata": dict(self.metadata),
        }
