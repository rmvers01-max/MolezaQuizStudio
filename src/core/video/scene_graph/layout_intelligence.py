from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .geometry import Rect
from .nodes import SceneGraph, SceneNode


@dataclass(frozen=True, slots=True)
class LayoutAdjustment:
    node_id: str
    reason: str
    before: Rect
    after: Rect
    severity: str = "info"
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "node_id": self.node_id,
            "reason": self.reason,
            "before": self.before.to_dict(),
            "after": self.after.to_dict(),
            "severity": self.severity,
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True, slots=True)
class LayoutIntelligenceReport:
    score: int
    adjustments: tuple[LayoutAdjustment, ...]
    warnings: tuple[str, ...]
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "score": self.score,
            "adjustments": [
                item.to_dict()
                for item in self.adjustments
            ],
            "warnings": list(self.warnings),
            "metadata": dict(self.metadata),
        }


class SceneLayoutIntelligence:
    """
    Corrige a composição antes da renderização.

    O motor prioriza legibilidade, áreas seguras e equilíbrio visual.
    """

    def optimize(
        self,
        *,
        graph: SceneGraph,
        question_text_length: int,
        alternative_lengths: list[int],
        has_image: bool,
        scene_kind: str,
    ) -> LayoutIntelligenceReport:
        adjustments: list[LayoutAdjustment] = []
        warnings: list[str] = []

        self._protect_question(
            graph,
            question_text_length,
            adjustments,
        )

        self._balance_choices(
            graph,
            alternative_lengths,
            has_image,
            adjustments,
            warnings,
        )

        self._protect_image(
            graph,
            has_image,
            adjustments,
        )

        if scene_kind == "reveal":
            self._protect_answer(
                graph,
                adjustments,
            )

        self._resolve_major_overlaps(
            graph,
            adjustments,
            warnings,
        )

        score = max(
            100
            - len(adjustments) * 3
            - len(warnings) * 7,
            0,
        )

        graph.metadata["layout_intelligence"] = {
            "score": score,
            "adjustment_count": len(adjustments),
            "warning_count": len(warnings),
        }

        return LayoutIntelligenceReport(
            score=score,
            adjustments=tuple(adjustments),
            warnings=tuple(warnings),
            metadata={
                "engine_version": "1.0",
                "scene_kind": scene_kind,
            },
        )

    def _protect_question(
        self,
        graph,
        text_length,
        adjustments,
    ):
        node = graph.find("question")
        if node is None:
            return

        extra_height = 30 if text_length > 90 else 18 if text_length > 60 else 0
        if extra_height <= 0:
            return

        before = node.bounds
        node.bounds = Rect(
            max(before.x - 20, 60),
            before.y,
            min(before.width + 40, graph.width - 120),
            before.height + extra_height,
        )

        adjustments.append(
            LayoutAdjustment(
                node.node_id,
                "Pergunta longa recebeu mais área vertical.",
                before,
                node.bounds,
                metadata={"text_length": text_length},
            )
        )

    def _balance_choices(
        self,
        graph,
        alternative_lengths,
        has_image,
        adjustments,
        warnings,
    ):
        choice_nodes = [
            node
            for node in graph.nodes()
            if (
                node.node_id.startswith("choice_")
                and not node.node_id.endswith("_sheen")
            )
        ]

        if not choice_nodes:
            return

        longest = max(alternative_lengths or [0])
        if longest <= 24:
            return

        for node in choice_nodes:
            before = node.bounds
            width_boost = 38 if longest > 42 else 22

            node.bounds = Rect(
                max(before.x - width_boost // 2, 70),
                before.y,
                min(
                    before.width + width_boost,
                    graph.width - before.x - 70,
                ),
                before.height + (12 if longest > 42 else 6),
            )

            adjustments.append(
                LayoutAdjustment(
                    node.node_id,
                    "Alternativa longa recebeu área adicional.",
                    before,
                    node.bounds,
                    metadata={"longest_alternative": longest},
                )
            )

            sheen = graph.find(f"{node.node_id}_sheen")
            if sheen is not None:
                sheen.bounds = node.bounds

        if has_image and longest > 50:
            warnings.append(
                "Imagem e alternativas longas competem por espaço."
            )

    def _protect_image(
        self,
        graph,
        has_image,
        adjustments,
    ):
        if not has_image:
            return

        node = graph.find("main_image")
        if node is None:
            return

        before = node.bounds
        min_width = int(graph.width * 0.26)
        min_height = int(graph.height * 0.32)

        new_width = max(before.width, min_width)
        new_height = max(before.height, min_height)

        if new_width == before.width and new_height == before.height:
            return

        node.bounds = Rect(
            before.x,
            before.y,
            new_width,
            new_height,
        )

        adjustments.append(
            LayoutAdjustment(
                node.node_id,
                "Imagem principal ampliada para preservar destaque.",
                before,
                node.bounds,
            )
        )

    def _protect_answer(
        self,
        graph,
        adjustments,
    ):
        node = graph.find("answer")
        if node is None:
            return

        before = node.bounds
        min_width = int(graph.width * 0.48)
        min_height = int(graph.height * 0.16)

        node.bounds = Rect(
            max(min(before.x, graph.width - min_width - 70), 70),
            max(min(before.y, graph.height - min_height - 60), 80),
            max(before.width, min_width),
            max(before.height, min_height),
        )

        if node.bounds != before:
            adjustments.append(
                LayoutAdjustment(
                    node.node_id,
                    "Resposta protegida para leitura e destaque.",
                    before,
                    node.bounds,
                )
            )

            glow = graph.find("answer_inner_glow")
            if glow is not None:
                glow.bounds = node.bounds

    def _resolve_major_overlaps(
        self,
        graph,
        adjustments,
        warnings,
    ):
        content = [
            node
            for node in graph.nodes()
            if (
                node.visible
                and node.safe_area
                and "content" in node.tags
            )
        ]

        for index, first in enumerate(content):
            for second in content[index + 1:]:
                if not first.bounds.intersects(second.bounds):
                    continue

                if (
                    first.parent_id == second.node_id
                    or second.parent_id == first.node_id
                ):
                    continue

                movable = first if first.priority < second.priority else second
                fixed = second if movable is first else first
                before = movable.bounds

                candidate = Rect(
                    movable.bounds.x,
                    min(
                        fixed.bounds.bottom + 12,
                        graph.height - movable.bounds.height - 40,
                    ),
                    movable.bounds.width,
                    movable.bounds.height,
                )

                if candidate.intersects(fixed.bounds):
                    warnings.append(
                        f"Colisão persistente entre {first.node_id} e {second.node_id}."
                    )
                    continue

                movable.bounds = candidate

                adjustments.append(
                    LayoutAdjustment(
                        movable.node_id,
                        f"Reposicionado para evitar colisão com {fixed.node_id}.",
                        before,
                        movable.bounds,
                        severity="warning",
                    )
                )
