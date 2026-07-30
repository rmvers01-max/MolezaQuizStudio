from __future__ import annotations

import hashlib

from .opening_profile import OpeningProfile


class OpeningDirector:
    """
    Decide automaticamente o formato da abertura.

    Princípios:
    - primeira pergunta em poucos segundos;
    - promessa clara;
    - desafio imediato;
    - identidade do canal;
    - texto curto e legível.
    """

    PERFIS = (
        OpeningProfile(
            nome="Desafio rápido",
            duracao=4.1,
            hook_texto="VOCÊ CONSEGUE ESCOLHER?",
            desafio_texto="PREPARE-SE!",
            mostrar_quantidade=True,
            usar_mascote=True,
            intensidade=0.82,
            primeiro_quadro_impactante=True,
        ),
        OpeningProfile(
            nome="Escolha impossível",
            duracao=4.3,
            hook_texto="ESCOLHAS IMPOSSÍVEIS!",
            desafio_texto="VAMOS COMEÇAR!",
            mostrar_quantidade=True,
            usar_mascote=True,
            intensidade=0.86,
            primeiro_quadro_impactante=True,
        ),
        OpeningProfile(
            nome="Quiz relâmpago",
            duracao=3.9,
            hook_texto="DECIDA RÁPIDO!",
            desafio_texto="VALENDO!",
            mostrar_quantidade=True,
            usar_mascote=True,
            intensidade=0.88,
            primeiro_quadro_impactante=True,
        ),
    )

    def escolher(
        self,
        titulo: str,
        total_perguntas: int,
        retention_plan: dict | None = None,
    ) -> dict:
        digest = hashlib.sha256(
            str(titulo).encode(
                "utf-8"
            )
        ).hexdigest()

        indice = int(
            digest[:8],
            16
        ) % len(
            self.PERFIS
        )

        perfil = self.PERFIS[
            indice
        ]

        limite_retencao = float(
            (
                retention_plan
                or {}
            ).get(
                "abertura_maxima",
                4.5
            )
        )

        duracao = min(
            perfil.duracao,
            limite_retencao
        )

        return {
            "nome": perfil.nome,
            "duracao": duracao,
            "hook_texto": (
                perfil.hook_texto
            ),
            "desafio_texto": (
                perfil.desafio_texto
            ),
            "mostrar_quantidade": (
                perfil.mostrar_quantidade
            ),
            "usar_mascote": (
                perfil.usar_mascote
            ),
            "intensidade": (
                perfil.intensidade
            ),
            "primeiro_quadro_impactante": (
                perfil
                .primeiro_quadro_impactante
            ),
            "total_perguntas": max(
                int(total_perguntas),
                1
            ),
        }
