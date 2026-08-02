from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class EffectBinding:
    """
    Descreve a relação entre um efeito e o nó que ele afeta.

    O efeito deixa de ser apenas uma camada global e passa a
    possuir alvo, máscara e política de recorte explícitos.
    """

    target_node_id: str
    scope: str = "target"
    clip_to_target: bool = True
    clip_shape: str = "rounded_rectangle"
    corner_radius: int = 22
    padding: int = 0
    blend_mode: str = "normal"
    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "target_node_id": (
                self.target_node_id
            ),
            "scope": self.scope,
            "clip_to_target": (
                self.clip_to_target
            ),
            "clip_shape": (
                self.clip_shape
            ),
            "corner_radius": (
                self.corner_radius
            ),
            "padding": self.padding,
            "blend_mode": (
                self.blend_mode
            ),
            "metadata": dict(
                self.metadata
            ),
        }
