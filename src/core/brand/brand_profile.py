from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class BrandProfile:
    nome_canal: str
    codigo: str
    publico: str
    faixa_etaria: str
    idioma: str
    personalidade: tuple[str, ...]
    mascote: str
    slogan: str
    cores_principais: tuple[tuple[int, int, int], ...]
    cores_secundarias: tuple[tuple[int, int, int], ...]
    estilo_visual: str
    ritmo: str
    intensidade_visual: float
    intensidade_mascote: float
    frequencia_cta: str
    regras: dict[str, object] = field(
        default_factory=dict
    )

    def para_metadados(self) -> dict:
        return {
            "nome_canal": self.nome_canal,
            "codigo": self.codigo,
            "publico": self.publico,
            "faixa_etaria": self.faixa_etaria,
            "idioma": self.idioma,
            "personalidade": list(
                self.personalidade
            ),
            "mascote": self.mascote,
            "slogan": self.slogan,
            "cores_principais": [
                list(cor)
                for cor in self.cores_principais
            ],
            "cores_secundarias": [
                list(cor)
                for cor in self.cores_secundarias
            ],
            "estilo_visual": self.estilo_visual,
            "ritmo": self.ritmo,
            "intensidade_visual": (
                self.intensidade_visual
            ),
            "intensidade_mascote": (
                self.intensidade_mascote
            ),
            "frequencia_cta": (
                self.frequencia_cta
            ),
            "regras": dict(
                self.regras
            ),
        }
