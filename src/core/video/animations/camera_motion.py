import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageEnhance
from moviepy import ImageSequenceClip


class CameraMotionFactory:
    """
    Movimento cinematográfico discreto para manter a cena viva.

    Aplica:
    - zoom lento;
    - pan horizontal;
    - microvariação de brilho;
    - sem alterar o tempo da cena.
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
        zoom_final=1.02,
        pan_horizontal=7,
        pulso_brilho=0.02,
    ):
        base = Image.open(
            Path(caminho_frame)
        ).convert("RGB")

        if base.size != (
            self.largura,
            self.altura,
        ):
            base = base.resize(
                (
                    self.largura,
                    self.altura,
                ),
                Image.Resampling.LANCZOS,
            )

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

            escala = (
                1.0
                + (
                    float(zoom_final)
                    - 1.0
                )
                * progresso
            )

            deslocamento_x = int(
                pan_horizontal
                * math.sin(
                    progresso
                    * math.pi
                )
            )

            quadro = self._recortar_zoom(
                base,
                escala,
                deslocamento_x,
            )

            brilho = (
                1.0
                + pulso_brilho
                * math.sin(
                    progresso
                    * math.pi
                    * 2
                )
            )

            quadro = ImageEnhance.Brightness(
                quadro
            ).enhance(
                brilho
            )

            quadros.append(
                np.asarray(quadro)
            )

        return ImageSequenceClip(
            quadros,
            fps=self.fps,
        ).with_duration(
            duracao
        )

    def _recortar_zoom(
        self,
        imagem,
        escala,
        deslocamento_x,
    ):
        largura = max(
            int(
                round(
                    self.largura
                    * escala
                )
            ),
            self.largura,
        )

        altura = max(
            int(
                round(
                    self.altura
                    * escala
                )
            ),
            self.altura,
        )

        ampliada = imagem.resize(
            (
                largura,
                altura,
            ),
            Image.Resampling.LANCZOS,
        )

        x = (
            largura
            - self.largura
        ) // 2 + deslocamento_x

        y = (
            altura
            - self.altura
        ) // 2

        x = max(
            0,
            min(
                largura - self.largura,
                x,
            ),
        )

        y = max(
            0,
            min(
                altura - self.altura,
                y,
            ),
        )

        return ampliada.crop(
            (
                x,
                y,
                x + self.largura,
                y + self.altura,
            )
        )
