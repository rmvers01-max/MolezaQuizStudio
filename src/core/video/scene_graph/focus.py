from __future__ import annotations

from dataclasses import dataclass

from .nodes import SceneGraph, SceneNode


@dataclass(frozen=True, slots=True)
class GraphFocusTarget:
    node_id: str
    x: int
    y: int
    radius: int
    intensity: float


class SceneGraphFocusResolver:
    """Seleciona o foco usando os próprios nós da cena."""

    def resolve(self, graph: SceneGraph, scene_kind: str) -> GraphFocusTarget:
        preferred_tags = (
            ("answer", "primary") if scene_kind == "reveal"
            else ("timer", "primary") if scene_kind == "countdown"
            else ("image", "primary", "choice")
        )

        candidates = [
            node for node in graph.nodes()
            if node.visible and node.safe_area
        ]

        def score(node: SceneNode) -> tuple[int, int, int]:
            tag_score = 0
            for rank, tag in enumerate(reversed(preferred_tags), start=1):
                if tag in node.tags:
                    tag_score = rank
            return (tag_score, node.priority, node.bounds.area)

        node = max(candidates, key=score, default=graph.root)
        x, y = node.bounds.center
        radius = max(int(max(node.bounds.width, node.bounds.height) * 0.72), 120)
        intensity = 0.72 if scene_kind == "reveal" else 0.35 if scene_kind == "countdown" else 0.48
        return GraphFocusTarget(node.node_id, x, y, radius, intensity)
