from __future__ import annotations

import math
import random

from PIL import Image, ImageDraw, ImageFilter


class LivingBackgroundEngine:
    """
    Living Background Engine — Nível 1.

    Mantém a cena viva sem competir com a pergunta.
    """

    def __init__(
        self,
        largura=1280,
        altura=720,
    ):
        self.largura = int(largura)
        self.altura = int(altura)

    def aplicar(
        self,
        imagem,
        tempo,
        tema="moleza_vibrante",
        intensidade=0.45,
        densidade_conteudo=0.5,
        pattern_break=False,
    ):
        intensidade = max(
            min(float(intensidade), 1.0),
            0.0,
        )

        densidade_conteudo = max(
            min(float(densidade_conteudo), 1.0),
            0.0,
        )

        fator_adaptativo = (
            1.0
            - 0.55 * densidade_conteudo
        )

        if pattern_break:
            fator_adaptativo = min(
                fator_adaptativo + 0.12,
                1.0,
            )

        atividade = intensidade * fator_adaptativo

        if atividade <= 0.01:
            return imagem

        self._gradiente_respirando(
            imagem,
            tempo,
            tema,
            atividade,
        )

        self._luzes_ambiente(
            imagem,
            tempo,
            tema,
            atividade,
        )

        self._particulas_tematicas(
            imagem,
            tempo,
            tema,
            atividade,
        )

        self._parallax_sutil(
            imagem,
            tempo,
            atividade,
        )

        return imagem

    def _gradiente_respirando(
        self,
        imagem,
        tempo,
        tema,
        intensidade,
    ):
        camada = Image.new(
            "RGBA",
            imagem.size,
            (0, 0, 0, 0),
        )

        desenho = ImageDraw.Draw(
            camada
        )

        pulso = (
            0.5
            + 0.5
            * math.sin(
                tempo * 0.65
            )
        )

        cor_a, cor_b = self._cores_tema(
            tema
        )

        desenho.rectangle(
            (
                0,
                0,
                self.largura,
                self.altura // 2,
            ),
            fill=(
                *cor_a,
                int(
                    34
                    * intensidade
                    * (
                        0.75 + 0.25 * pulso
                    )
                ),
            ),
        )

        desenho.rectangle(
            (
                0,
                self.altura // 2,
                self.largura,
                self.altura,
            ),
            fill=(
                *cor_b,
                int(
                    30
                    * intensidade
                    * (
                        1.0 - 0.18 * pulso
                    )
                ),
            ),
        )

        camada = camada.filter(
            ImageFilter.GaussianBlur(
                radius=80
            )
        )

        imagem.alpha_composite(
            camada
        )

    def _luzes_ambiente(
        self,
        imagem,
        tempo,
        tema,
        intensidade,
    ):
        camada = Image.new(
            "RGBA",
            imagem.size,
            (0, 0, 0, 0),
        )

        desenho = ImageDraw.Draw(
            camada
        )

        cor_a, cor_b = self._cores_tema(
            tema
        )

        dx = int(
            70
            * math.sin(
                tempo * 0.42
            )
        )

        dy = int(
            35
            * math.cos(
                tempo * 0.36
            )
        )

        desenho.ellipse(
            (
                -220 + dx,
                -160 + dy,
                520 + dx,
                560 + dy,
            ),
            fill=(
                *cor_a,
                int(
                    52 * intensidade
                ),
            ),
        )

        desenho.ellipse(
            (
                760 - dx,
                -190 - dy,
                1480 - dx,
                520 - dy,
            ),
            fill=(
                *cor_b,
                int(
                    48 * intensidade
                ),
            ),
        )

        camada = camada.filter(
            ImageFilter.GaussianBlur(
                radius=105
            )
        )

        imagem.alpha_composite(
            camada
        )

    def _particulas_tematicas(
        self,
        imagem,
        tempo,
        tema,
        intensidade,
    ):
        random.seed(3501)

        camada = Image.new(
            "RGBA",
            imagem.size,
            (0, 0, 0, 0),
        )

        desenho = ImageDraw.Draw(
            camada
        )

        tipo = self._tipo_particula(
            tema
        )

        quantidade = max(
            int(
                24 * intensidade
            ),
            8,
        )

        for indice in range(
            quantidade
        ):
            profundidade = 1 + (
                indice % 3
            )

            velocidade = (
                0.22
                + 0.08 * profundidade
            )

            x_base = (
                indice * 101
                + 43
            ) % self.largura

            y_base = (
                indice * 67
                + 29
            ) % self.altura

            x = (
                x_base
                + 18
                * math.sin(
                    tempo
                    * velocidade
                    + indice
                )
            )

            y = (
                y_base
                + 12
                * math.cos(
                    tempo
                    * velocidade
                    * 0.8
                    + indice
                )
            )

            alpha = int(
                (
                    35
                    + profundidade * 18
                )
                * intensidade
            )

            tamanho = 2 + profundidade

            if tipo == "stars":
                desenho.line(
                    (
                        x - tamanho,
                        y,
                        x + tamanho,
                        y,
                    ),
                    fill=(
                        255,
                        255,
                        255,
                        alpha,
                    ),
                    width=1,
                )

                desenho.line(
                    (
                        x,
                        y - tamanho,
                        x,
                        y + tamanho,
                    ),
                    fill=(
                        255,
                        255,
                        255,
                        alpha,
                    ),
                    width=1,
                )

            elif tipo == "leaves":
                desenho.ellipse(
                    (
                        x - tamanho,
                        y - tamanho // 2,
                        x + tamanho,
                        y + tamanho // 2,
                    ),
                    fill=(
                        180,
                        245,
                        175,
                        alpha,
                    ),
                )

            elif tipo == "pixels":
                desenho.rectangle(
                    (
                        x - tamanho,
                        y - tamanho,
                        x + tamanho,
                        y + tamanho,
                    ),
                    fill=(
                        180,
                        220,
                        255,
                        alpha,
                    ),
                )

            else:
                desenho.ellipse(
                    (
                        x - tamanho,
                        y - tamanho,
                        x + tamanho,
                        y + tamanho,
                    ),
                    fill=(
                        255,
                        255,
                        255,
                        alpha,
                    ),
                )

        camada = camada.filter(
            ImageFilter.GaussianBlur(
                radius=0.8
            )
        )

        imagem.alpha_composite(
            camada
        )

    def _parallax_sutil(
        self,
        imagem,
        tempo,
        intensidade,
    ):
        camada = Image.new(
            "RGBA",
            imagem.size,
            (0, 0, 0, 0),
        )

        desenho = ImageDraw.Draw(
            camada
        )

        for plano in range(3):
            deslocamento = int(
                (
                    2 + plano
                )
                * intensidade
                * math.sin(
                    tempo
                    * (
                        0.18
                        + plano * 0.05
                    )
                    + plano
                )
            )

            alpha = int(
                12
                * intensidade
                * (
                    plano + 1
                )
            )

            desenho.arc(
                (
                    -100 + deslocamento,
                    90 + plano * 110,
                    self.largura
                    + 100
                    + deslocamento,
                    470 + plano * 90,
                ),
                start=190,
                end=350,
                fill=(
                    255,
                    255,
                    255,
                    alpha,
                ),
                width=2,
            )

        camada = camada.filter(
            ImageFilter.GaussianBlur(
                radius=2
            )
        )

        imagem.alpha_composite(
            camada
        )

    def _tipo_particula(
        self,
        tema,
    ):
        tema = str(
            tema or ""
        ).lower()

        if "jungle" in tema:
            return "leaves"

        if (
            "neon" in tema
            or "game" in tema
        ):
            return "pixels"

        if "princess" in tema:
            return "stars"

        return "sparkles"

    def _cores_tema(
        self,
        tema,
    ):
        tema = str(
            tema or ""
        ).lower()

        mapa = {
            "candy_party": (
                (255, 105, 185),
                (110, 145, 255),
            ),
            "neon_future": (
                (70, 255, 225),
                (180, 75, 255),
            ),
            "jungle_adventure": (
                (105, 220, 135),
                (245, 205, 75),
            ),
            "game_arena": (
                (65, 155, 255),
                (255, 75, 145),
            ),
            "princess_dream": (
                (255, 130, 215),
                (165, 120, 255),
            ),
        }

        return mapa.get(
            tema,
            (
                (255, 95, 165),
                (85, 155, 255),
            )
        )
