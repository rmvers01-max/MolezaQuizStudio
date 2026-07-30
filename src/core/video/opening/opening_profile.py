from __future__ import annotations

from dataclasses import dataclass


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
