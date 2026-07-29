import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageEnhance
from moviepy import ImageSequenceClip


class MascotAnimationFactory:
    """
    Anima o mascote sempre em primeiro plano e aplica um movimento
    de câmera muito suave na cena para evitar quadros totalmente parados.
    """

    def __init__(
        self,
        largura=1280,
        altura=720,
        fps=20,
    ):
        self.largura = int(largura)
        self.altura = int(altura)
        self.fps = max(int(fps), 10)

    def animar_sobre_frame(
        self,
        caminho_frame,
        mascote,
        duracao,
        margem_direita=28,
        margem_inferior=18,
        intensidade_balanco=5,
        intensidade_respiracao=0.025,
        zoom_final=1.018,
        deslocamento_horizontal=5,
        brilho_pulso=0.025,
    ):
        base = Image.open(
            Path(caminho_frame)
        ).convert("RGBA")

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

            onda = math.sin(
                progresso
                * math.pi
                * 2
            )

            balanco = int(
                intensidade_balanco
                * onda
            )

            escala_mascote = (
                1.0
                + intensidade_respiracao
                * onda
            )

            escala_cena = (
                1.0
                + (
                    float(zoom_final)
                    - 1.0
                )
                * progresso
            )

            cena = self._zoom_e_deslocamento(
                base,
                escala=escala_cena,
                deslocamento_x=int(
                    deslocamento_horizontal
                    * math.sin(
                        progresso
                        * math.pi
                    )
                ),
            )

            brilho = (
                1.0
                + brilho_pulso
                * max(
                    onda,
                    0.0,
                )
            )

            cena = ImageEnhance.Brightness(
                cena
            ).enhance(
                brilho
            )

            largura_mascote = max(
                int(
                    round(
                        mascote.width
                        * escala_mascote
                    )
                ),
                1,
            )

            altura_mascote = max(
                int(
                    round(
                        mascote.height
                        * escala_mascote
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

            x = (
                self.largura
                - mascote_frame.width
                - margem_direita
            )

            y = (
                self.altura
                - mascote_frame.height
                - margem_inferior
                + balanco
            )

            cena.alpha_composite(
                mascote_frame,
                (x, y),
            )

            quadros.append(
                np.asarray(
                    cena.convert("RGB")
                )
            )

        return ImageSequenceClip(
            quadros,
            fps=self.fps,
        ).with_duration(
            duracao
        )

    def _zoom_e_deslocamento(
        self,
        imagem,
        escala,
        deslocamento_x=0,
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
        ) // 2

        y = (
            altura
            - self.altura
        ) // 2

        x = max(
            0,
            min(
                largura - self.largura,
                x + deslocamento_x,
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
