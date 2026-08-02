from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .nodes import SceneGraph
from .validation import SceneIssue


class SceneGraphDiagnostics:
    def graph_to_dict(self, graph: SceneGraph, issues: list[SceneIssue] | None = None) -> dict[str, Any]:
        return {
            "width": graph.width,
            "height": graph.height,
            "metadata": dict(graph.metadata),
            "nodes": [
                {
                    "node_id": node.node_id,
                    "bounds": node.bounds.as_tuple(),
                    "z_index": node.z_index,
                    "priority": node.priority,
                    "parent_id": node.parent_id,
                    "clip_to_bounds": node.clip_to_bounds,
                    "clip_shape": node.clip_shape,
                    "corner_radius": node.corner_radius,
                    "safe_area": node.safe_area,
                    "allow_overlap": node.allow_overlap,
                    "tags": sorted(node.tags),
                    "metadata": dict(node.metadata),
                }
                for node in graph.nodes()
            ],
            "issues": [issue.to_dict() for issue in (issues or [])],
        }

    def save(self, graph: SceneGraph, path, issues: list[SceneIssue] | None = None) -> Path:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(self.graph_to_dict(graph, issues), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return path
