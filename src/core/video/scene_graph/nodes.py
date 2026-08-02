from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Any

from PIL import Image

from .context import SceneRenderContext
from .geometry import Rect


RenderFunction = Callable[[Image.Image, Rect, SceneRenderContext], Image.Image | None]


@dataclass(slots=True)
class SceneNode:
    node_id: str
    bounds: Rect
    z_index: int = 0
    visible: bool = True
    opacity: float = 1.0
    priority: int = 50
    safe_area: bool = False
    allow_overlap: bool = False
    clip_to_bounds: bool = False
    tags: set[str] = field(default_factory=set)
    metadata: dict[str, Any] = field(default_factory=dict)
    renderer: RenderFunction | None = None
    children: list["SceneNode"] = field(default_factory=list)

    def add(self, node: "SceneNode") -> "SceneNode":
        self.children.append(node)
        return node

    def walk(self):
        yield self
        for child in self.children:
            yield from child.walk()

    def render(
        self,
        canvas: Image.Image,
        context: SceneRenderContext,
    ) -> Image.Image:
        if not self.visible or self.opacity <= 0:
            return canvas

        result = canvas
        if self.renderer is not None:
            rendered = self.renderer(result, self.bounds, context)
            if rendered is not None:
                result = rendered

        for child in sorted(self.children, key=lambda item: item.z_index):
            result = child.render(result, context)

        return result


@dataclass(slots=True)
class SceneGraph:
    width: int
    height: int
    root: SceneNode
    metadata: dict[str, Any] = field(default_factory=dict)

    def nodes(self) -> list[SceneNode]:
        return [node for node in self.root.walk() if node is not self.root]

    def find(self, node_id: str) -> SceneNode | None:
        for node in self.root.walk():
            if node.node_id == node_id:
                return node
        return None

    def render(self, canvas: Image.Image, context: SceneRenderContext) -> Image.Image:
        return self.root.render(canvas, context)
