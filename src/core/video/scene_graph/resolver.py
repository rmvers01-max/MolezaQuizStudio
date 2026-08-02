from __future__ import annotations

from .geometry import Rect
from .nodes import SceneGraph, SceneNode


class SafeAreaResolver:
    """Reposiciona somente nós explicitamente marcados como móveis."""

    def resolve(self, graph: SceneGraph) -> SceneGraph:
        viewport = Rect(0, 0, graph.width, graph.height)
        protected = [node for node in graph.nodes() if node.safe_area]

        for node in graph.nodes():
            node.bounds = node.bounds.clamp_inside(viewport)

            if not node.metadata.get("movable", False):
                continue

            for safe in protected:
                if node is safe or not node.bounds.intersects(safe.bounds):
                    continue

                candidates = (
                    Rect(18, node.bounds.y, node.bounds.width, node.bounds.height),
                    Rect(graph.width - node.bounds.width - 18, node.bounds.y, node.bounds.width, node.bounds.height),
                    Rect(node.bounds.x, 18, node.bounds.width, node.bounds.height),
                    Rect(node.bounds.x, graph.height - node.bounds.height - 18, node.bounds.width, node.bounds.height),
                )

                valid = [candidate.clamp_inside(viewport) for candidate in candidates]
                valid.sort(key=lambda candidate: safe.bounds.overlap_ratio(candidate))
                node.bounds = valid[0]

        return graph
