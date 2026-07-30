from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RetentionProfile:
    nome: str
    abertura_maxima: float
    entrada_minima: float
    entrada_maxima: float
    resultado_minimo: float
    resultado_maximo: float
    mudanca_visual_maxima: float
    intervalo_pattern_break: int
    limite_texto_pergunta: int
    limite_texto_alternativa: int
    intensidade_base: float
    usar_cta_intermediario: bool
    usar_cta_final: bool
