from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Any

from PIL import Image

from .context import SceneRenderContext
from .geometry import Rect
from .materials import SceneMaskFactory


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
    clip_shape: str = "rectangle"
    corner_radius: int = 0
    parent_id: str | None = None
    tags: set[str] = field(default_factory=set)
    metadata: dict[str, Any] = field(default_factory=dict)
    renderer: RenderFunction | None = None
    children: list["SceneNode"] = field(default_factory=list)

    def add(self, node: "SceneNode") -> "SceneNode":
        node.parent_id = self.node_id
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
            if self.clip_to_bounds:
                layer = Image.new(
                    "RGBA",
                    canvas.size,
                    (0, 0, 0, 0),
                )

                rendered = self.renderer(
                    layer,
                    self.bounds,
                    context,
                )

                if rendered is not None:
                    layer = rendered

                mask = SceneMaskFactory().create(
                    canvas_size=canvas.size,
                    bounds=self.bounds,
                    shape=self.clip_shape,
                    corner_radius=self.corner_radius,
                    opacity=self.opacity,
                )

                clipped = Image.new(
                    "RGBA",
                    canvas.size,
                    (0, 0, 0, 0),
                )

                clipped.paste(
                    layer,
                    (0, 0),
                    mask,
                )

                result = canvas.copy()
                result.alpha_composite(
                    clipped
                )
            else:
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
