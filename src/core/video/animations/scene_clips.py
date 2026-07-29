from pathlib import Path

import numpy as np
from PIL import Image, ImageEnhance
from moviepy import ImageClip, ImageSequenceClip, concatenate_videoclips

from .easing import ease_out_back, ease_out_cubic, pulse


class SceneClipFactory:
    """
    Cria animações curtas a partir dos frames renderizados.

    O motor trabalha com sequências curtas para evitar consumo excessivo
    de memória. Depois da entrada animada, o restante da cena permanece
    como ImageClip estático.
    """

    def __init__(
        self,
        largura: int = 1280,
        altura: int = 720,
        fps_animacao: int = 15,
    ):
        self.largura = int(largura)
        self.altura = int(altura)
        self.fps_animacao = max(int(fps_animacao), 8)

    def criar_entrada(
        self,
        caminho_imagem,
        duracao_total: float,
        duracao_animacao: float = 0.75,
    ):
        duracao_total = max(float(duracao_total), 0.1)
        duracao_animacao = min(
            max(float(duracao_animacao), 0.1),
            duracao_total,
        )

        imagem = self._abrir_imagem(caminho_imagem)
        quadros = []

        total_quadros = max(
            int(round(duracao_animacao * self.fps_animacao)),
            2,
        )

        for indice in range(total_quadros):
            progresso = indice / max(total_quadros - 1, 1)
            suavizado = ease_out_cubic(progresso)

            escala = 0.92 + (0.08 * suavizado)
            brilho = 0.72 + (0.28 * suavizado)

            quadro = self._aplicar_zoom_central(
                imagem,
                escala,
            )

            quadro = ImageEnhance.Brightness(
                quadro
            ).enhance(
                brilho
            )

            quadros.append(
                np.asarray(quadro)
            )

        clip_entrada = ImageSequenceClip(
            quadros,
            fps=self.fps_animacao,
        )

        restante = duracao_total - clip_entrada.duration

        if restante <= 0.01:
            return clip_entrada

        clip_estatico = ImageClip(
            str(caminho_imagem)
        ).with_duration(
            restante
        )

        return concatenate_videoclips(
            [
                clip_entrada,
                clip_estatico,
            ],
            method="compose",
        )

    def criar_pulso(
        self,
        caminho_imagem,
        duracao: float = 1.0,
        intensidade: float = 0.018,
    ):
        duracao = max(float(duracao), 0.1)
        imagem = self._abrir_imagem(caminho_imagem)

        total_quadros = max(
            int(round(duracao * self.fps_animacao)),
            2,
        )

        quadros = []

        for indice in range(total_quadros):
            progresso = indice / max(total_quadros - 1, 1)
            escala = (
                1.0
                + intensidade
                * max(
                    pulse(progresso, ciclos=1.0),
                    0.0,
                )
            )

            quadro = self._aplicar_zoom_central(
                imagem,
                escala,
            )

            quadros.append(
                np.asarray(quadro)
            )

        return ImageSequenceClip(
            quadros,
            fps=self.fps_animacao,
        ).with_duration(
            duracao
        )


    def criar_movimento_suave(
        self,
        caminho_imagem,
        duracao: float,
        zoom_inicial: float = 1.0,
        zoom_final: float = 1.035,
    ):
        duracao = max(float(duracao), 0.1)
        imagem = self._abrir_imagem(caminho_imagem)

        total_quadros = max(
            int(round(duracao * self.fps_animacao)),
            2,
        )

        quadros = []

        for indice in range(total_quadros):
            progresso = indice / max(total_quadros - 1, 1)

            escala = (
                float(zoom_inicial)
                + (
                    float(zoom_final)
                    - float(zoom_inicial)
                )
                * progresso
            )

            quadro = self._aplicar_zoom_central(
                imagem,
                escala,
            )

            quadros.append(
                np.asarray(quadro)
            )

        return ImageSequenceClip(
            quadros,
            fps=self.fps_animacao,
        ).with_duration(
            duracao
        )

    def criar_resultado(
        self,
        caminho_imagem,
        duracao_total: float,
        duracao_animacao: float = 0.65,
    ):
        duracao_total = max(float(duracao_total), 0.1)
        duracao_animacao = min(
            max(float(duracao_animacao), 0.1),
            duracao_total,
        )

        imagem = self._abrir_imagem(caminho_imagem)
        total_quadros = max(
            int(round(duracao_animacao * self.fps_animacao)),
            2,
        )

        quadros = []

        for indice in range(total_quadros):
            progresso = indice / max(total_quadros - 1, 1)
            suavizado = ease_out_back(progresso)
            escala = 0.86 + 0.14 * suavizado

            quadro = self._aplicar_zoom_central(
                imagem,
                escala,
            )

            quadros.append(
                np.asarray(quadro)
            )

        clip_entrada = ImageSequenceClip(
            quadros,
            fps=self.fps_animacao,
        )

        restante = duracao_total - clip_entrada.duration

        if restante <= 0.01:
            return clip_entrada

        clip_estatico = ImageClip(
            str(caminho_imagem)
        ).with_duration(
            restante
        )

        return concatenate_videoclips(
            [
                clip_entrada,
                clip_estatico,
            ],
            method="compose",
        )

    def _abrir_imagem(self, caminho) -> Image.Image:
        imagem = Image.open(
            Path(caminho)
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

        return imagem

    def _aplicar_zoom_central(
        self,
        imagem: Image.Image,
        escala: float,
    ) -> Image.Image:
        escala = max(float(escala), 0.1)

        nova_largura = max(
            int(round(self.largura * escala)),
            1,
        )

        nova_altura = max(
            int(round(self.altura * escala)),
            1,
        )

        redimensionada = imagem.resize(
            (
                nova_largura,
                nova_altura,
            ),
            Image.Resampling.LANCZOS,
        )

        tela = Image.new(
            "RGB",
            (
                self.largura,
                self.altura,
            ),
            (20, 15, 50),
        )

        x = (
            self.largura
            - nova_largura
        ) // 2

        y = (
            self.altura
            - nova_altura
        ) // 2

        tela.paste(
            redimensionada,
            (x, y),
        )

        return tela
