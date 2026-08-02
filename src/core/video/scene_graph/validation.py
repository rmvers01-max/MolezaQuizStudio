from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .geometry import Rect
from .nodes import SceneGraph, SceneNode


@dataclass(frozen=True, slots=True)
class SceneIssue:
    severity: str
    code: str
    message: str
    node_ids: tuple[str, ...]
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "severity": self.severity,
            "code": self.code,
            "message": self.message,
            "node_ids": list(self.node_ids),
            "metadata": dict(self.metadata),
        }


class SceneGraphValidator:
    def __init__(self, overlap_threshold: float = 0.12):
        self.overlap_threshold = float(overlap_threshold)

    def validate(self, graph: SceneGraph) -> list[SceneIssue]:
        issues: list[SceneIssue] = []
        viewport = Rect(0, 0, graph.width, graph.height)
        nodes = [node for node in graph.nodes() if node.visible]

        for node in nodes:
            if node.bounds.width <= 0 or node.bounds.height <= 0:
                issues.append(SceneIssue(
                    "error", "invalid_bounds",
                    f"O nó {node.node_id} possui dimensões inválidas.",
                    (node.node_id,),
                ))
                continue

            if node.bounds.clamp_inside(viewport) != node.bounds:
                issues.append(SceneIssue(
                    "warning", "outside_viewport",
                    f"O nó {node.node_id} ultrapassa a área do vídeo.",
                    (node.node_id,),
                    {"bounds": node.bounds.as_tuple()},
                ))

        protected = [node for node in nodes if node.safe_area]
        movable = [node for node in nodes if not node.allow_overlap]

        for index, first in enumerate(movable):
            for second in movable[index + 1:]:
                if first.z_index == second.z_index and first.bounds.intersects(second.bounds):
                    ratio = min(
                        first.bounds.overlap_ratio(second.bounds),
                        second.bounds.overlap_ratio(first.bounds),
                    )
                    if ratio >= self.overlap_threshold:
                        severity = "error" if first.safe_area or second.safe_area else "warning"
                        issues.append(SceneIssue(
                            severity,
                            "visual_overlap",
                            f"{first.node_id} e {second.node_id} ocupam a mesma área visual.",
                            (first.node_id, second.node_id),
                            {"overlap_ratio": round(ratio, 3)},
                        ))

        for safe in protected:
            for node in nodes:
                if node is safe or node.allow_overlap or node.priority >= safe.priority:
                    continue
                ratio = safe.bounds.overlap_ratio(node.bounds)
                if ratio >= self.overlap_threshold:
                    issues.append(SceneIssue(
                        "error", "safe_area_blocked",
                        f"{node.node_id} invade a área segura de {safe.node_id}.",
                        (safe.node_id, node.node_id),
                        {"overlap_ratio": round(ratio, 3)},
                    ))

        return issues
