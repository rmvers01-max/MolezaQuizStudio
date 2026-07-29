import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageEnhance
from moviepy import ImageSequenceClip

from .easing import ease_out_back, ease_out_cubic, pulse


class LayeredSceneAnimator:
    """
    Anima elementos independentes sobre um frame-base.

    Esta etapa permite que os cartões A e B entrem por lados opostos
    e que o selo "OU" apareça separadamente com efeito de pulso.
    """

    def __init__(
        self,
        largura: int = 1280,
        altura: int = 720,
        fps: int = 20,
    ):
        self.largura = int(largura)
        self.altura = int(altura)
        self.fps = max(int(fps), 10)

    def criar_entrada_opcoes(
        self,
        caminho_base,
        caminho_cartao_a,
        caminho_cartao_b,
        caminho_ou,
        duracao: float = 1.1,
        mascote=None,
        margem_direita=28,
        margem_inferior=18,
    ):
        base = self._abrir_rgba(caminho_base)
        cartao_a = self._abrir_rgba(caminho_cartao_a)
        cartao_b = self._abrir_rgba(caminho_cartao_b)
        selo_ou = self._abrir_rgba(caminho_ou)

        duracao = max(float(duracao), 0.3)

        total_quadros = max(
            int(round(duracao * self.fps)),
            4,
        )

        quadros = []

        posicao_final_a = (90, 275)
        posicao_final_b = (710, 275)
        posicao_final_ou = (575, 340)

        for indice in range(total_quadros):
            progresso = indice / max(total_quadros - 1, 1)

            progresso_a = ease_out_cubic(
                min(progresso / 0.72, 1.0)
            )

            progresso_b = ease_out_cubic(
                min(max((progresso - 0.12) / 0.72, 0.0), 1.0)
            )

            progresso_ou = ease_out_back(
                min(max((progresso - 0.42) / 0.58, 0.0), 1.0)
            )

            quadro = base.copy()

            x_a = int(
                -cartao_a.width
                + (
                    posicao_final_a[0]
                    + cartao_a.width
                )
                * progresso_a
            )

            x_b = int(
                self.largura
                - (
                    self.largura
                    - posicao_final_b[0]
                )
                * progresso_b
            )

            alpha_a = int(255 * progresso_a)
            alpha_b = int(255 * progresso_b)
            alpha_ou = int(255 * min(progresso_ou, 1.0))

            cartao_a_frame = self._com_alpha(
                cartao_a,
                alpha_a,
            )

            cartao_b_frame = self._com_alpha(
                cartao_b,
                alpha_b,
            )

            escala_ou = max(
                0.2,
                min(1.0, progresso_ou),
            )

            selo_frame = self._redimensionar_central(
                selo_ou,
                escala_ou,
            )

            selo_frame = self._com_alpha(
                selo_frame,
                alpha_ou,
            )

            quadro.alpha_composite(
                cartao_a_frame,
                (
                    x_a,
                    posicao_final_a[1],
                ),
            )

            quadro.alpha_composite(
                cartao_b_frame,
                (
                    x_b,
                    posicao_final_b[1],
                ),
            )

            x_ou = int(
                posicao_final_ou[0]
                + (
                    selo_ou.width
                    - selo_frame.width
                ) / 2
            )

            y_ou = int(
                posicao_final_ou[1]
                + (
                    selo_ou.height
                    - selo_frame.height
                ) / 2
            )

            quadro.alpha_composite(
                selo_frame,
                (
                    x_ou,
                    y_ou,
                ),
            )

            if mascote is not None:
                onda = math.sin(
                    progresso
                    * math.pi
                    * 2
                )

                escala_mascote = (
                    1.0
                    + 0.02
                    * onda
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

                x_mascote = (
                    self.largura
                    - mascote_frame.width
                    - margem_direita
                )

                y_mascote = (
                    self.altura
                    - mascote_frame.height
                    - margem_inferior
                    + int(4 * onda)
                )

                quadro.alpha_composite(
                    mascote_frame,
                    (
                        x_mascote,
                        y_mascote,
                    ),
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

    def criar_pulso_ou(
        self,
        caminho_frame,
        duracao: float = 1.0,
        intensidade: float = 0.045,
    ):
        imagem = self._abrir_rgba(caminho_frame)
        duracao = max(float(duracao), 0.2)

        total_quadros = max(
            int(round(duracao * self.fps)),
            4,
        )

        quadros = []

        caixa_ou = (
            590,
            340,
            690,
            440,
        )

        selo = imagem.crop(
            caixa_ou
        )

        base = imagem.copy()

        base.paste(
            (0, 0, 0, 0),
            caixa_ou
        )

        for indice in range(total_quadros):
            progresso = indice / max(total_quadros - 1, 1)

            escala = (
                1.0
                + intensidade
                * max(
                    pulse(
                        progresso,
                        ciclos=1.0,
                    ),
                    0.0,
                )
            )

            selo_frame = self._redimensionar_central(
                selo,
                escala,
            )

            quadro = base.copy()

            x = int(
                640 - selo_frame.width / 2
            )

            y = int(
                390 - selo_frame.height / 2
            )

            quadro.alpha_composite(
                selo_frame,
                (x, y),
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

    def _abrir_rgba(
        self,
        caminho,
    ) -> Image.Image:
        return Image.open(
            Path(caminho)
        ).convert("RGBA")

    def _com_alpha(
        self,
        imagem: Image.Image,
        alpha: int,
    ) -> Image.Image:
        resultado = imagem.copy()
        canal_alpha = resultado.getchannel("A")
        canal_alpha = canal_alpha.point(
            lambda valor: int(
                valor
                * max(0, min(alpha, 255))
                / 255
            )
        )
        resultado.putalpha(
            canal_alpha
        )
        return resultado

    def _redimensionar_central(
        self,
        imagem: Image.Image,
        escala: float,
    ) -> Image.Image:
        escala = max(float(escala), 0.05)

        largura = max(
            int(round(imagem.width * escala)),
            1,
        )

        altura = max(
            int(round(imagem.height * escala)),
            1,
        )

        return imagem.resize(
            (
                largura,
                altura,
            ),
            Image.Resampling.LANCZOS,
        )
