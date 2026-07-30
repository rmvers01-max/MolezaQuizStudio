from __future__ import annotations

import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
from moviepy import ImageSequenceClip

from .render_profiles import RenderProfile


class AAARenderPipeline:
    """
    Consolida as etapas finais do render.

    Ordem:
    1. composição de camadas;
    2. câmera;
    3. Visual FX;
    4. Character Engine;
    5. Card Material Engine;
    6. Cinematic FX;
    7. anti-aliasing;
    8. color finish;
    9. nitidez final.
    """

    def __init__(
        self,
        profile: RenderProfile,
    ):
        self.profile = profile

    def finalizar_frame(
        self,
        imagem: Image.Image,
    ) -> Image.Image:
        resultado = imagem.convert("RGBA")

        if self.profile.anti_aliasing:
            resultado = self._anti_aliasing(
                resultado
            )

        resultado = ImageEnhance.Contrast(
            resultado
        ).enhance(
            self.profile.contraste_final
        )

        resultado = ImageEnhance.Color(
            resultado
        ).enhance(
            self.profile.saturacao_final
        )

        if self.profile.nitidez_final > 1.0:
            resultado = ImageEnhance.Sharpness(
                resultado
            ).enhance(
                self.profile.nitidez_final
            )

        return resultado

    def criar_clip(
        self,
        quadros,
        duracao,
    ):
        return ImageSequenceClip(
            [
                np.asarray(
                    quadro.convert("RGB")
                )
                for quadro in quadros
            ],
            fps=self.profile.fps_timeline,
        ).with_duration(
            duracao
        )

    def _anti_aliasing(
        self,
        imagem,
    ):
        largura, altura = imagem.size

        escala = max(
            float(
                self.profile.escala_interna
            ),
            1.0
        )

        if escala <= 1.0:
            return imagem

        ampliada = imagem.resize(
            (
                int(largura * escala),
                int(altura * escala),
            ),
            Image.Resampling.LANCZOS,
        )

        suavizada = ampliada.filter(
            ImageFilter.GaussianBlur(
                radius=0.25
            )
        )

        return suavizada.resize(
            (largura, altura),
            Image.Resampling.LANCZOS,
        )
