import math
from pathlib import Path

import numpy as np
from PIL import Image
from moviepy import ImageSequenceClip


class CardMotionFactory:
    """
    Anima cartões de alternativas com movimento contínuo discreto.

    Os cartões fazem movimentos opostos para criar profundidade
    sem prejudicar a leitura.
    """

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
        amplitude_vertical=4,
        amplitude_horizontal=2,
    ):
        base = Image.open(
            Path(caminho_frame)
        ).convert("RGBA")

        duracao = max(float(duracao), 0.2)
        total = max(
            int(round(duracao * self.fps)),
            4,
        )

        caixa_a = (90, 275, 570, 535)
        caixa_b = (710, 275, 1190, 535)

        cartao_a = base.crop(
            caixa_a
        )

        cartao_b = base.crop(
            caixa_b
        )

        fundo = base.copy()

        fundo.paste(
            (35, 28, 78, 255),
            caixa_a
        )

        fundo.paste(
            (35, 28, 78, 255),
            caixa_b
        )

        quadros = []

        for indice in range(total):
            progresso = indice / max(
                total - 1,
                1,
            )

            onda = math.sin(
                progresso
                * math.pi
                * 2
            )

            onda_oposta = math.sin(
                progresso
                * math.pi
                * 2
                + math.pi
            )

            quadro = fundo.copy()

            x_a = (
                caixa_a[0]
                + int(
                    amplitude_horizontal
                    * onda
                )
            )

            y_a = (
                caixa_a[1]
                + int(
                    amplitude_vertical
                    * onda
                )
            )

            x_b = (
                caixa_b[0]
                + int(
                    amplitude_horizontal
                    * onda_oposta
                )
            )

            y_b = (
                caixa_b[1]
                + int(
                    amplitude_vertical
                    * onda_oposta
                )
            )

            quadro.alpha_composite(
                cartao_a,
                (x_a, y_a),
            )

            quadro.alpha_composite(
                cartao_b,
                (x_b, y_b),
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
