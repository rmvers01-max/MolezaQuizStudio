from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class OpeningProfile:
    nome: str
    duracao: float
    hook_texto: str
    desafio_texto: str
    mostrar_quantidade: bool
    usar_mascote: bool
    intensidade: float
    primeiro_quadro_impactante: bool
    categoria: str = "general_knowledge"
    camera_style: str = "discovery_push"
    transition_style: str = "light_wipe"
    mascot_sequence: tuple[str, ...] = (
        "wave",
        "thinking",
        "point_right",
    )
    teaser_items: tuple[str, ...] = ()
    audio_layers: tuple[str, ...] = (
        "ambient",
        "rise",
        "impact",
        "transition",
    )
    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "nome": self.nome,
            "duracao": self.duracao,
            "hook_texto": self.hook_texto,
            "desafio_texto": self.desafio_texto,
            "mostrar_quantidade": self.mostrar_quantidade,
            "usar_mascote": self.usar_mascote,
            "intensidade": self.intensidade,
            "primeiro_quadro_impactante": (
                self.primeiro_quadro_impactante
            ),
            "categoria": self.categoria,
            "camera_style": self.camera_style,
            "transition_style": self.transition_style,
            "mascot_sequence": list(
                self.mascot_sequence
            ),
            "teaser_items": list(
                self.teaser_items
            ),
            "audio_layers": list(
                self.audio_layers
            ),
            "metadata": dict(self.metadata),
        }
