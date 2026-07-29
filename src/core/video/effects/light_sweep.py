import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from moviepy import ImageSequenceClip


class LightSweepFactory:
    """Reflexo de luz discreto atravessando os cartões."""

    def __init__(
        self,
        largura=1280,
        altura=720,
        fps=18,
    ):
        self.largura = int(largura)
        self.altura = int(altura)
        self.fps = max(int(fps), 10)

    def aplicar(
        self,
        caminho_frame,
        duracao,
        intensidade=0.22,
    ):
        base = Image.open(
            Path(caminho_frame)
        ).convert("RGBA")

        duracao = max(float(duracao), 0.2)

        total = max(
            int(round(duracao * self.fps)),
            4,
        )

        quadros = []

        for indice in range(total):
            progresso = indice / max(
                total - 1,
                1,
            )

            quadro = base.copy()

            camada = Image.new(
                "RGBA",
                (
                    self.largura,
                    self.altura,
                ),
                (0, 0, 0, 0),
            )

            desenho = ImageDraw.Draw(
                camada
            )

            x_centro = int(
                -180
                + (
                    self.largura
                    + 360
                )
                * progresso
            )

            largura_faixa = 120

            desenho.polygon(
                [
                    (
                        x_centro
                        - largura_faixa,
                        250,
                    ),
                    (
                        x_centro,
                        250,
                    ),
                    (
                        x_centro
                        + largura_faixa,
                        560,
                    ),
                    (
                        x_centro,
                        560,
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
                    radius=18
                )
            )

            quadro.alpha_composite(
                camada
            )

            quadros.append(
                np.asarray(
                    quadro.convert("RGB")
                )
            )

        return ImageSequenceClip(
            quadros,
            fps=self.fps,
        ).with_duration(
            duracao
        )
