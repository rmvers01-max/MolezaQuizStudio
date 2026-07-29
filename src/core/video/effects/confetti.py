import math
import random
import numpy as np
from PIL import Image, ImageDraw
from moviepy import ImageSequenceClip


class ConfettiFactory:
    def __init__(
        self,
        largura=1280,
        altura=720,
        fps=20,
        quantidade=70,
    ):
        self.largura = int(largura)
        self.altura = int(altura)
        self.fps = max(int(fps), 10)
        self.quantidade = max(int(quantidade), 20)

    def aplicar(
        self,
        caminho_frame,
        duracao=1.2,
        mascote=None,
        margem_direita=28,
        margem_inferior=18,
    ):
        base = Image.open(caminho_frame).convert("RGB")
        duracao = max(float(duracao), 0.3)
        total = max(int(round(duracao * self.fps)), 4)

        random.seed(42)
        cores = [
            (255, 214, 75),
            (255, 90, 120),
            (75, 170, 255),
            (105, 220, 170),
            (190, 105, 255),
            (255, 255, 255),
        ]

        particulas = [
            {
                "x": random.randint(0, self.largura),
                "y": random.randint(-220, -10),
                "velocidade": random.uniform(180, 420),
                "oscilacao": random.uniform(10, 50),
                "fase": random.uniform(0, 6.28),
                "tamanho": random.randint(5, 13),
                "cor": random.choice(cores),
            }
            for _ in range(self.quantidade)
        ]

        quadros = []

        for indice in range(total):
            t = indice / self.fps
            quadro = base.copy()
            desenho = ImageDraw.Draw(quadro)

            for particula in particulas:
                x = (
                    particula["x"]
                    + particula["oscilacao"]
                    * math.sin(particula["fase"] + t * 4)
                )
                y = particula["y"] + particula["velocidade"] * t
                tamanho = particula["tamanho"]

                desenho.rounded_rectangle(
                    (
                        x,
                        y,
                        x + tamanho,
                        y + tamanho * 1.6,
                    ),
                    radius=2,
                    fill=particula["cor"],
                )

            if mascote is not None:
                progresso = indice / max(
                    total - 1,
                    1,
                )

                onda = math.sin(
                    progresso
                    * math.pi
                    * 4
                )

                escala = (
                    1.0
                    + 0.04
                    * max(
                        onda,
                        0.0,
                    )
                )

                largura_mascote = max(
                    int(
                        round(
                            mascote.width
                            * escala
                        )
                    ),
                    1,
                )

                altura_mascote = max(
                    int(
                        round(
                            mascote.height
                            * escala
                        )
                    ),
                    1,
                )

                mascote_frame = mascote.resize(
                    (
                        largura_mascote,
                        altura_mascote,
                    ),
                    Image.Resampling.LANCZOS,
                )

                x_mascote = (
                    self.largura
                    - mascote_frame.width
                    - margem_direita
                )

                y_mascote = (
                    self.altura
                    - mascote_frame.height
                    - margem_inferior
                    + int(8 * onda)
                )

                quadro.paste(
                    mascote_frame,
                    (
                        x_mascote,
                        y_mascote,
                    ),
                    mascote_frame,
                )

            quadros.append(np.asarray(quadro))

        return ImageSequenceClip(
            quadros,
            fps=self.fps,
        ).with_duration(duracao)
