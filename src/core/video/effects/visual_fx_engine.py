from __future__ import annotations

import math
import random

from PIL import Image, ImageDraw, ImageFilter


class VisualFXEngine:
    """
    Efeitos visuais procedurais para cenas em timeline.

    Recursos:
    - luz ambiente;
    - partículas em profundidades diferentes;
    - reflexo de brilho;
    - parallax sutil;
    - vinheta discreta.
    """

    def __init__(
        self,
        largura=1280,
        altura=720,
    ):
        self.largura = int(largura)
        self.altura = int(altura)

    def aplicar_ambiente(
        self,
        imagem,
        tempo,
        intensidade=0.55,
    ):
        camada = Image.new(
            "RGBA",
            imagem.size,
            (0, 0, 0, 0),
        )

        desenho = ImageDraw.Draw(
            camada
        )

        deslocamento = int(
            90
            * math.sin(
                tempo * 0.55
            )
        )

        desenho.ellipse(
            (
                -180 + deslocamento,
                30,
                520 + deslocamento,
                650,
            ),
            fill=(
                255,
                96,
                180,
                int(55 * intensidade),
            ),
        )

        desenho.ellipse(
            (
                760 - deslocamento,
                -100,
                1460 - deslocamento,
                520,
            ),
            fill=(
                75,
                165,
                255,
                int(55 * intensidade),
            ),
        )

        camada = camada.filter(
            ImageFilter.GaussianBlur(
                radius=90
            )
        )

        imagem.alpha_composite(
            camada
        )

    def aplicar_particulas(
        self,
        imagem,
        tempo,
        quantidade=30,
        intensidade=0.55,
    ):
        random.seed(2026)

        camada = Image.new(
            "RGBA",
            imagem.size,
            (0, 0, 0, 0),
        )

        desenho = ImageDraw.Draw(
            camada
        )

        for indice in range(
            max(int(quantidade), 10)
        ):
            profundidade = 1 + (
                indice % 3
            )

            velocidade = (
                4.0
                / profundidade
            )

            x_base = (
                indice * 83
                + 47
            ) % self.largura

            y_base = (
                indice * 61
                + 37
            ) % self.altura

            x = (
                x_base
                + 20
                * math.sin(
                    tempo * velocidade
                    + indice
                )
            )

            y = (
                y_base
                + 12
                * math.cos(
                    tempo * velocidade * 0.7
                    + indice
                )
            )

            raio = (
                2
                + profundidade * 2
            )

            alpha = int(
                (
                    45
                    + profundidade * 30
                )
                * intensidade
            )

            desenho.ellipse(
                (
                    x - raio,
                    y - raio,
                    x + raio,
                    y + raio,
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
                radius=1.2
            )
        )

        imagem.alpha_composite(
            camada
        )

    def aplicar_reflexo_cartoes(
        self,
        imagem,
        tempo,
        caixas,
        intensidade=0.24,
    ):
        camada = Image.new(
            "RGBA",
            imagem.size,
            (0, 0, 0, 0),
        )

        desenho = ImageDraw.Draw(
            camada
        )

        progresso = (
            tempo * 0.45
        ) % 1.0

        for caixa in caixas:
            x1, y1, x2, y2 = caixa

            largura = (
                x2 - x1
            )

            centro = (
                x1
                - 140
                + (
                    largura
                    + 280
                )
                * progresso
            )

            desenho.polygon(
                [
                    (
                        centro - 70,
                        y1,
                    ),
                    (
                        centro,
                        y1,
                    ),
                    (
                        centro + 90,
                        y2,
                    ),
                    (
                        centro + 20,
                        y2,
                    ),
                ],
                fill=(
                    255,
                    255,
                    255,
                    int(
                        255
                        * intensidade
                    ),
                ),
            )

        camada = camada.filter(
            ImageFilter.GaussianBlur(
                radius=14
            )
        )

        imagem.alpha_composite(
            camada
        )

    def aplicar_vinheta(
        self,
        imagem,
        intensidade=0.18,
    ):
        camada = Image.new(
            "L",
            imagem.size,
            0,
        )

        desenho = ImageDraw.Draw(
            camada
        )

        margem = 70

        desenho.ellipse(
            (
                -margem,
                -margem,
                self.largura + margem,
                self.altura + margem,
            ),
            fill=255,
        )

        camada = camada.filter(
            ImageFilter.GaussianBlur(
                radius=100
            )
        )

        invertida = Image.eval(
            camada,
            lambda valor: 255 - valor
        )

        escurecimento = Image.new(
            "RGBA",
            imagem.size,
            (
                0,
                0,
                0,
                int(
                    255
                    * intensidade
                ),
            ),
        )

        escurecimento.putalpha(
            invertida
        )

        imagem.alpha_composite(
            escurecimento
        )
