from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class SceneRenderContext:
    width: int
    height: int
    time: float
    progress: float
    scene_kind: str
    question_number: int
    total_questions: int
    theme_pack: dict[str, Any]
    metadata: dict[str, Any] = field(default_factory=dict)
