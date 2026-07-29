import math
import numpy as np
from PIL import Image, ImageDraw
from moviepy import ImageSequenceClip


class AnimatedBackgroundFactory:
    """Gera fundo animado leve sem depender de vídeos externos."""

    def __init__(
        self,
        largura: int = 1280,
        altura: int = 720,
        fps: int = 15,
    ):
        self.largura = int(largura)
        self.altura = int(altura)
        self.fps = max(int(fps), 8)

    def criar(
        self,
        duracao: float,
    ):
        duracao = max(float(duracao), 0.1)

        total_quadros = max(
            int(round(duracao * self.fps)),
            2,
        )

        quadros = []

        for indice in range(total_quadros):
            progresso = indice / max(
                total_quadros - 1,
                1,
            )

            imagem = Image.new(
                "RGB",
                (
                    self.largura,
                    self.altura,
                ),
                (25, 18, 70),
            )

            desenho = ImageDraw.Draw(
                imagem
            )

            for y in range(
                self.altura
            ):
                proporcao = (
                    y
                    / max(
                        self.altura - 1,
                        1,
                    )
                )

                cor = (
                    int(
                        88
                        - 45
                        * proporcao
                    ),
                    int(
                        40
                        - 18
                        * proporcao
                    ),
                    int(
                        170
                        - 65
                        * proporcao
                    ),
                )

                desenho.line(
                    (
                        0,
                        y,
                        self.largura,
                        y,
                    ),
                    fill=cor,
                )

            deslocamento = int(
                60
                * math.sin(
                    progresso
                    * math.pi
                    * 2
                )
            )

            bolhas = [
                (
                    -120 + deslocamento,
                    -80,
                    280 + deslocamento,
                    320,
                    (130, 90, 220),
                ),
                (
                    1010 - deslocamento,
                    -100,
                    1390 - deslocamento,
                    280,
                    (70, 120, 230),
                ),
                (
                    980 + deslocamento,
                    500,
                    1360 + deslocamento,
                    850,
                    (180, 60, 170),
                ),
                (
                    -150 - deslocamento,
                    510,
                    240 - deslocamento,
                    880,
                    (80, 180, 190),
                ),
            ]

            for (
                x1,
                y1,
                x2,
                y2,
                cor,
            ) in bolhas:
                desenho.ellipse(
                    (
                        x1,
                        y1,
                        x2,
                        y2,
                    ),
                    fill=cor,
                )

            quadros.append(
                np.asarray(imagem)
            )

        return ImageSequenceClip(
            quadros,
            fps=self.fps,
        ).with_duration(
            duracao
        )
