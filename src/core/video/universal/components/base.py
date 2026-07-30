from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from PIL import Image


@dataclass(frozen=True, slots=True)
class ComponentBox:
    x: int
    y: int
    width: int
    height: int

    @property
    def right(self) -> int:
        return self.x + self.width

    @property
    def bottom(self) -> int:
        return self.y + self.height

    def as_tuple(self) -> tuple[int, int, int, int]:
        return (
            self.x,
            self.y,
            self.right,
            self.bottom,
        )


@dataclass(slots=True)
class ComponentContext:
    width: int
    height: int
    theme_pack: dict[str, Any]
    scene_kind: str
    question_number: int = 0
    total_questions: int = 0
    progress: float = 0.0
    time: float = 0.0


class UniversalComponent(ABC):
    @abstractmethod
    def render(
        self,
        image: Image.Image,
        box: ComponentBox,
        context: ComponentContext,
    ) -> None:
        raise NotImplementedError
