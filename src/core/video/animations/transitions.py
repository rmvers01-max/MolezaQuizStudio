import numpy as np
from PIL import Image, ImageEnhance
from moviepy import ImageSequenceClip


class TransitionFactory:
    """Cria transições curtas e automáticas entre perguntas."""

    def __init__(
        self,
        largura: int = 1280,
        altura: int = 720,
        fps: int = 20,
    ):
        self.largura = int(largura)
        self.altura = int(altura)
        self.fps = max(int(fps), 10)

    def criar_flash(
        self,
        caminho_imagem,
        duracao: float = 0.32,
    ):
        imagem = Image.open(
            caminho_imagem
        ).convert("RGB")

        if imagem.size != (
            self.largura,
            self.altura,
        ):
            imagem = imagem.resize(
                (
                    self.largura,
                    self.altura,
                ),
                Image.Resampling.LANCZOS,
            )

        total_quadros = max(
            int(round(duracao * self.fps)),
            4,
        )

        quadros = []

        for indice in range(total_quadros):
            progresso = indice / max(
                total_quadros - 1,
                1,
            )

            if progresso < 0.5:
                intensidade = progresso / 0.5
            else:
                intensidade = (
                    1.0
                    - progresso
                ) / 0.5

            brilho = (
                1.0
                + 0.85
                * max(
                    intensidade,
                    0.0,
                )
            )

            quadro = ImageEnhance.Brightness(
                imagem
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
