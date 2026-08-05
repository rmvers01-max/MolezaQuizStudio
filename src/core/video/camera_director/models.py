from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class CameraMove:
    code: str
    move_type: str
    zoom_from: float
    zoom_to: float
    pan_x: float
    pan_y: float
    rotation: float
    shake: float
    focus_strength: float
    depth_strength: float
    duration: float
    easing: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "code": self.code,
            "move_type": self.move_type,
            "zoom_from": self.zoom_from,
            "zoom_to": self.zoom_to,
            "pan_x": self.pan_x,
            "pan_y": self.pan_y,
            "rotation": self.rotation,
            "shake": self.shake,
            "focus_strength": self.focus_strength,
            "depth_strength": self.depth_strength,
            "duration": self.duration,
            "easing": self.easing,
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True, slots=True)
class CameraPlan:
    scene_kind: str
    category: str
    question_number: int
    primary_move: CameraMove
    fallback_move: CameraMove
    target_x: float
    target_y: float
    safe_motion_limit: float
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "scene_kind": self.scene_kind,
            "category": self.category,
            "question_number": self.question_number,
            "primary_move": self.primary_move.to_dict(),
            "fallback_move": self.fallback_move.to_dict(),
            "target_x": self.target_x,
            "target_y": self.target_y,
            "safe_motion_limit": self.safe_motion_limit,
            "metadata": dict(self.metadata),
        }
