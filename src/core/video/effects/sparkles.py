import math
import random

import numpy as np
from PIL import Image, ImageDraw
from moviepy import ImageSequenceClip


class SparklesFactory:
    """
    Aplica partículas luminosas discretas durante a pergunta
    e a contagem para deixar a cena viva sem prejudicar a leitura.
    """

    def __init__(
        self,
        largura=1280,
        altura=720,
        fps=15,
        quantidade=28,
    ):
        self.largura = int(largura)
        self.altura = int(altura)
        self.fps = max(int(fps), 8)
        self.quantidade = max(int(quantidade), 10)

    def aplicar(
        self,
        caminho_frame,
        duracao,
        intensidade=0.65,
    ):
        base = Image.open(
            caminho_frame
        ).convert("RGBA")

        duracao = max(float(duracao), 0.2)

        total = max(
            int(round(duracao * self.fps)),
            4,
        )

        random.seed(
            hash(str(caminho_frame)) & 0xFFFF
        )

        particulas = []

        for _ in range(self.quantidade):
            particulas.append({
                "x": random.randint(30, self.largura - 30),
                "y": random.randint(40, self.altura - 40),
                "raio": random.randint(2, 6),
                "fase": random.uniform(0, math.pi * 2),
                "velocidade": random.uniform(1.2, 2.8),
                "deriva": random.uniform(-10, 10),
            })

        quadros = []

        for indice in range(total):
            t = indice / self.fps
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

            for particula in particulas:
                brilho = (
                    0.5
                    + 0.5
                    * math.sin(
                        particula["fase"]
                        + t
                        * particula["velocidade"]
                    )
                )

                alpha = int(
                    180
                    * intensidade
                    * brilho
                )

                x = (
                    particula["x"]
                    + particula["deriva"]
                    * math.sin(
                        t
                        + particula["fase"]
                    )
                )

                y = (
                    particula["y"]
                    + 6
                    * math.cos(
                        t * 0.8
                        + particula["fase"]
                    )
                )

                raio = particula["raio"]

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
