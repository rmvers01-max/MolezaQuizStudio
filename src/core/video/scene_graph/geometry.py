from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Rect:
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

    @property
    def center(self) -> tuple[int, int]:
        return (
            self.x + self.width // 2,
            self.y + self.height // 2,
        )

    @property
    def area(self) -> int:
        return max(self.width, 0) * max(self.height, 0)

    def intersects(self, other: "Rect") -> bool:
        return not (
            self.right <= other.x
            or other.right <= self.x
            or self.bottom <= other.y
            or other.bottom <= self.y
        )

    def intersection(self, other: "Rect") -> "Rect | None":
        if not self.intersects(other):
            return None

        x1 = max(self.x, other.x)
        y1 = max(self.y, other.y)
        x2 = min(self.right, other.right)
        y2 = min(self.bottom, other.bottom)
        return Rect(x1, y1, x2 - x1, y2 - y1)

    def overlap_ratio(self, other: "Rect") -> float:
        overlap = self.intersection(other)
        if overlap is None or self.area <= 0:
            return 0.0
        return overlap.area / self.area

    def inset(self, amount: int) -> "Rect":
        amount = max(int(amount), 0)
        return Rect(
            self.x + amount,
            self.y + amount,
            max(self.width - amount * 2, 0),
            max(self.height - amount * 2, 0),
        )

    def clamp_inside(self, container: "Rect") -> "Rect":
        width = min(self.width, container.width)
        height = min(self.height, container.height)
        x = min(max(self.x, container.x), container.right - width)
        y = min(max(self.y, container.y), container.bottom - height)
        return Rect(x, y, width, height)

    def to_dict(self) -> dict[str, int]:
        return {
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height,
        }

    def as_tuple(self) -> tuple[int, int, int, int]:
        return (self.x, self.y, self.right, self.bottom)
