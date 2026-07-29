from __future__ import annotations

import math

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter


class CinematicFXEngine:
    """
    Efeitos cinematográficos leves para cenas de quiz.

    Recursos:
    - bloom;
    - glow;
    - lens flare discreto;
    - raios de luz;
    - color grading;
    - aberração cromática muito suave;
    - profundidade de campo simulada.
    """

    def __init__(
        self,
        largura=1280,
        altura=720,
    ):
        self.largura = int(largura)
        self.altura = int(altura)

    def aplicar(
        self,
        imagem,
        tempo,
        intensidade=0.45,
        estilo="mixed_glow",
    ):
        intensidade = max(
            min(float(intensidade), 1.0),
            0.0,
        )

        if intensidade <= 0.01:
            return imagem

        resultado = imagem.copy()

        self.aplicar_raios(
            resultado,
            tempo=tempo,
            intensidade=intensidade * 0.55,
        )

        self.aplicar_lens_flare(
            resultado,
            tempo=tempo,
            intensidade=intensidade * 0.45,
        )

        self.aplicar_bloom(
            resultado,
            intensidade=intensidade * 0.55,
        )

        resultado = self.aplicar_color_grading(
            resultado,
            estilo=estilo,
            intensidade=intensidade,
        )

        resultado = self.aplicar_aberracao_cromatica(
            resultado,
            intensidade=intensidade * 0.18,
        )

        resultado = self.aplicar_profundidade_campo(
            resultado,
            intensidade=intensidade * 0.30,
        )

        return resultado

    def aplicar_bloom(
        self,
        imagem,
        intensidade=0.35,
    ):
        brilho = imagem.filter(
            ImageFilter.GaussianBlur(
                radius=12
            )
        )

        brilho = ImageEnhance.Brightness(
            brilho
        ).enhance(
            1.15
            + intensidade * 0.45
        )

        alpha = int(
            70 * intensidade
        )

        canal = brilho.getchannel(
            "A"
        ).point(
            lambda valor: int(
                valor
                * alpha
                / 255
            )
        )

        brilho.putalpha(
            canal
        )

        imagem.alpha_composite(
            brilho
        )

    def aplicar_lens_flare(
        self,
        imagem,
        tempo,
        intensidade=0.25,
    ):
        camada = Image.new(
            "RGBA",
            imagem.size,
            (0, 0, 0, 0),
        )

        desenho = ImageDraw.Draw(
            camada
        )

        x = int(
            self.largura
            * (
                0.72
                + 0.08
                * math.sin(
                    tempo * 0.45
                )
            )
        )

        y = int(
            self.altura
            * (
                0.20
                + 0.04
                * math.cos(
                    tempo * 0.40
                )
            )
        )

        tamanhos = (
            (82, 45),
            (42, 28),
            (20, 16),
        )

        deslocamentos = (
            (0, 0),
            (-115, 72),
            (-225, 142),
        )

        for (
            largura,
            altura
        ), (
            dx,
            dy
        ) in zip(
            tamanhos,
            deslocamentos,
        ):
            alpha = int(
                70
                * intensidade
            )

            desenho.ellipse(
                (
                    x + dx - largura,
                    y + dy - altura,
                    x + dx + largura,
                    y + dy + altura,
                ),
                fill=(
                    255,
                    240,
                    190,
                    alpha,
                ),
            )

        camada = camada.filter(
            ImageFilter.GaussianBlur(
                radius=14
            )
        )

        imagem.alpha_composite(
            camada
        )

    def aplicar_raios(
        self,
        imagem,
        tempo,
        intensidade=0.25,
    ):
        camada = Image.new(
            "RGBA",
            imagem.size,
            (0, 0, 0, 0),
        )

        desenho = ImageDraw.Draw(
            camada
        )

        origem_x = int(
            self.largura
            * (
                0.18
                + 0.06
                * math.sin(
                    tempo * 0.35
                )
            )
        )

        origem_y = -80

        alpha = int(
            45
            * intensidade
        )

        for indice in range(3):
            abertura = (
                180
                + indice * 100
            )

            desenho.polygon(
                [
                    (
                        origem_x
                        + indice * 50,
                        origem_y,
                    ),
                    (
                        origem_x
                        + 120
                        + indice * 60,
                        origem_y,
                    ),
                    (
                        origem_x
                        + abertura
                        + 260,
                        self.altura,
                    ),
                    (
                        origem_x
                        + abertura,
                        self.altura,
                    ),
                ],
                fill=(
                    255,
                    255,
                    255,
                    alpha,
                ),
            )

        camada = camada.filter(
            ImageFilter.GaussianBlur(
                radius=24
            )
        )

        imagem.alpha_composite(
            camada
        )

    def aplicar_color_grading(
        self,
        imagem,
        estilo="mixed_glow",
        intensidade=0.45,
    ):
        estilo = str(
            estilo or "mixed_glow"
        ).strip().lower()

        ajustes = {
            "pastel_glow": (
                1.05,
                1.06,
                1.04,
            ),
            "neon_glow": (
                1.08,
                1.10,
                1.14,
            ),
            "green_glow": (
                1.03,
                1.08,
                1.02,
            ),
            "game_glow": (
                1.08,
                1.07,
                1.12,
            ),
            "pink_glow": (
                1.10,
                1.04,
                1.08,
            ),
            "mixed_glow": (
                1.06,
                1.05,
                1.08,
            ),
        }

        brilho, contraste, cor = ajustes.get(
            estilo,
            ajustes["mixed_glow"],
        )

        fator = max(
            min(float(intensidade), 1.0),
            0.0,
        )

        imagem = ImageEnhance.Brightness(
            imagem
        ).enhance(
            1.0
            + (
                brilho - 1.0
            )
            * fator
        )

        imagem = ImageEnhance.Contrast(
            imagem
        ).enhance(
            1.0
            + (
                contraste - 1.0
            )
            * fator
        )

        imagem = ImageEnhance.Color(
            imagem
        ).enhance(
            1.0
            + (
                cor - 1.0
            )
            * fator
        )

        return imagem

    def aplicar_aberracao_cromatica(
        self,
        imagem,
        intensidade=0.08,
    ):
        deslocamento = max(
            int(
                round(
                    3
                    * intensidade
                )
            ),
            0,
        )

        if deslocamento <= 0:
            return imagem

        rgb = imagem.convert(
            "RGB"
        )

        r, g, b = rgb.split()

        r = self._deslocar_canal(
            r,
            deslocamento
        )

        b = self._deslocar_canal(
            b,
            -deslocamento
        )

        combinado = Image.merge(
            "RGB",
            (r, g, b)
        ).convert(
            "RGBA"
        )

        combinado.putalpha(
            imagem.getchannel("A")
        )

        return combinado

    def aplicar_profundidade_campo(
        self,
        imagem,
        intensidade=0.12,
    ):
        if intensidade <= 0.01:
            return imagem

        desfocada = imagem.filter(
            ImageFilter.GaussianBlur(
                radius=3.5
                * intensidade
            )
        )

        mascara = Image.new(
            "L",
            imagem.size,
            0,
        )

        desenho = ImageDraw.Draw(
            mascara
        )

        margem_x = int(
            self.largura * 0.16
        )

        margem_y = int(
            self.altura * 0.18
        )

        desenho.rounded_rectangle(
            (
                margem_x,
                margem_y,
                self.largura - margem_x,
                self.altura - margem_y,
            ),
            radius=60,
            fill=255,
        )

        mascara = mascara.filter(
            ImageFilter.GaussianBlur(
                radius=45
            )
        )

        return Image.composite(
            imagem,
            desfocada,
            mascara
        )

    def _deslocar_canal(
        self,
        canal,
        deslocamento,
    ):
        resultado = Image.new(
            "L",
            canal.size,
            0,
        )

        resultado.paste(
            canal,
            (deslocamento, 0),
        )

        return resultado
