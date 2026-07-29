from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any


class LayerType(str, Enum):
    BACKGROUND = "background"
    PARTICLES = "particles"
    CARD = "card"
    IMAGE = "image"
    TEXT = "text"
    BADGE = "badge"
    TIMER = "timer"
    MASCOT = "mascot"
    EFFECT = "effect"


@dataclass(slots=True)
class AnimationSpec:
    nome: str
    inicio: float = 0.0
    duracao: float = 0.5
    parametros: dict[str, Any] = field(
        default_factory=dict
    )


@dataclass(slots=True)
class TimelineLayer:
    nome: str
    tipo: LayerType
    z_index: int
    inicio: float
    duracao: float
    origem: str | Path | None = None
    propriedades: dict[str, Any] = field(
        default_factory=dict
    )
    animacoes: list[AnimationSpec] = field(
        default_factory=list
    )

    @property
    def fim(self) -> float:
        return (
            float(self.inicio)
            + float(self.duracao)
        )


@dataclass(slots=True)
class TimelineScene:
    nome: str
    duracao: float
    largura: int = 1280
    altura: int = 720
    fps: int = 30
    camadas: list[TimelineLayer] = field(
        default_factory=list
    )
    metadados: dict[str, Any] = field(
        default_factory=dict
    )

    def adicionar_camada(
        self,
        camada: TimelineLayer
    ) -> TimelineLayer:
        self.camadas.append(
            camada
        )

        self.camadas.sort(
            key=lambda item: item.z_index
        )

        return camada

    def validar(self):
        if self.duracao <= 0:
            raise ValueError(
                "A duração da cena deve ser maior que zero."
            )

        for camada in self.camadas:
            if camada.inicio < 0:
                raise ValueError(
                    f"Camada {camada.nome}: início inválido."
                )

            if camada.duracao <= 0:
                raise ValueError(
                    f"Camada {camada.nome}: duração inválida."
                )

            if camada.fim > self.duracao + 0.001:
                raise ValueError(
                    f"Camada {camada.nome} ultrapassa "
                    "a duração da cena."
                )
