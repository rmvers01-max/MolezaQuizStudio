from __future__ import annotations

import hashlib

from .brand_profile import BrandProfile
from .brand_registry import BrandRegistry


class BrandDirector:
    """
    Diretor central da identidade do canal.

    Decide automaticamente:
    - identidade visual;
    - comportamento do mascote;
    - intensidade de efeitos;
    - ritmo base;
    - consistência entre vídeos.
    """

    def __init__(
        self,
        codigo_marca="moleza_quiz",
    ):
        self.registry = BrandRegistry()
        self.profile = self.registry.obter(
            codigo_marca
        )

    def obter_perfil(self) -> BrandProfile:
        return self.profile

    def criar_direcao_video(
        self,
        titulo_quiz: str,
        total_perguntas: int,
    ) -> dict:
        assinatura = self._assinatura(
            titulo_quiz
        )

        variacao = int(
            assinatura[:8],
            16
        )

        energia = (
            0.65
            + (
                variacao % 21
            ) / 100
        )

        energia = min(
            energia,
            0.85
        )

        return {
            "brand": (
                self.profile
                .para_metadados()
            ),
            "titulo_quiz": (
                str(titulo_quiz)
            ),
            "total_perguntas": int(
                total_perguntas
            ),
            "energia_video": energia,
            "variacao_criativa": (
                variacao % 7
            ),
            "mascote_frequencia": (
                self._frequencia_mascote(
                    total_perguntas
                )
            ),
            "cta": self._direcao_cta(
                total_perguntas
            ),
            "ritmo": {
                "abertura_max_segundos": (
                    self.profile
                    .regras
                    .get(
                        "abertura_max_segundos",
                        5.0
                    )
                ),
                "mudanca_visual_max_segundos": 4.0,
                "contagem_padrao": 5,
                "transicao_curta": True,
            },
        }

    def aplicar_na_cena(
        self,
        cena,
        numero_pergunta: int,
        etapa: str,
    ):
        direcao = dict(
            cena.metadados.get(
                "brand_direction",
                {}
            )
        )

        energia = float(
            direcao.get(
                "energia_video",
                0.72
            )
        )

        cena.metadados[
            "brand_scene"
        ] = {
            "numero_pergunta": int(
                numero_pergunta
            ),
            "etapa": str(etapa),
            "energia": energia,
            "variacao": (
                (
                    int(numero_pergunta)
                    + int(
                        direcao.get(
                            "variacao_criativa",
                            0
                        )
                    )
                )
                % 7
            ),
            "preservar_identidade": True,
        }

        return cena

    def _frequencia_mascote(
        self,
        total_perguntas: int,
    ) -> dict:
        total = max(
            int(total_perguntas),
            1
        )

        return {
            "entrada": True,
            "contagem": True,
            "resultado": True,
            "reacao_especial_a_cada": (
                5
                if total >= 15
                else 3
            ),
        }

    def _direcao_cta(
        self,
        total_perguntas: int,
    ) -> dict:
        total = max(
            int(total_perguntas),
            1
        )

        pontos = []

        if total >= 10:
            pontos.append(
                max(
                    int(total * 0.35),
                    3
                )
            )

        if total >= 20:
            pontos.append(
                max(
                    int(total * 0.72),
                    7
                )
            )

        return {
            "usar_cta_curto": True,
            "perguntas_cta": pontos,
            "cta_final": True,
            "tom": "divertido e não invasivo",
        }

    def _assinatura(
        self,
        texto: str,
    ) -> str:
        return hashlib.sha256(
            str(texto).encode(
                "utf-8"
            )
        ).hexdigest()
