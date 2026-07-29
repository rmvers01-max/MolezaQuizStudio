from __future__ import annotations

import math

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter


class CardMaterialEngine:
    """
    Renderiza cartões premium em múltiplas camadas.

    Recursos:
    - gradiente principal;
    - sombra externa;
    - sombra interna;
    - borda iluminada;
    - highlight superior;
    - glow externo;
    - reflexo especular mascarado;
    - respeito total aos cantos arredondados.
    """

    def __init__(
        self,
        largura=1280,
        altura=720,
    ):
        self.largura = int(largura)
        self.altura = int(altura)

    def renderizar(
        self,
        imagem_base,
        caixa,
        cor,
        progresso,
        raio=34,
        glow=0.35,
        intensidade_reflexo=0.24,
        resultado=False,
    ):
        x1, y1, x2, y2 = map(
            int,
            caixa
        )

        largura = max(
            x2 - x1,
            1
        )

        altura = max(
            y2 - y1,
            1
        )

        margem = 34

        material = Image.new(
            "RGBA",
            (
                largura + margem * 2,
                altura + margem * 2,
            ),
            (0, 0, 0, 0)
        )

        caixa_local = (
            margem,
            margem,
            margem + largura,
            margem + altura,
        )

        # Sombra externa.
        sombra = Image.new(
            "RGBA",
            material.size,
            (0, 0, 0, 0)
        )

        desenho_sombra = ImageDraw.Draw(
            sombra
        )

        desenho_sombra.rounded_rectangle(
            (
                caixa_local[0] + 10,
                caixa_local[1] + 14,
                caixa_local[2] + 10,
                caixa_local[3] + 14,
            ),
            radius=raio,
            fill=(0, 0, 0, 105)
        )

        sombra = sombra.filter(
            ImageFilter.GaussianBlur(
                radius=14
            )
        )

        material.alpha_composite(
            sombra
        )

        # Glow externo.
        if glow > 0.01:
            camada_glow = Image.new(
                "RGBA",
                material.size,
                (0, 0, 0, 0)
            )

            desenho_glow = ImageDraw.Draw(
                camada_glow
            )

            cor_glow = self._clarear(
                cor,
                0.32
            )

            desenho_glow.rounded_rectangle(
                caixa_local,
                radius=raio,
                fill=(
                    *cor_glow,
                    int(
                        100
                        * max(
                            min(glow, 1.0),
                            0.0
                        )
                    )
                )
            )

            camada_glow = camada_glow.filter(
                ImageFilter.GaussianBlur(
                    radius=18
                )
            )

            material.alpha_composite(
                camada_glow
            )

        # Máscara arredondada principal.
        mascara = Image.new(
            "L",
            material.size,
            0
        )

        desenho_mascara = ImageDraw.Draw(
            mascara
        )

        desenho_mascara.rounded_rectangle(
            caixa_local,
            radius=raio,
            fill=255
        )

        # Gradiente base.
        camada_base = Image.new(
            "RGBA",
            material.size,
            (0, 0, 0, 0)
        )

        desenho_base = ImageDraw.Draw(
            camada_base
        )

        cor_topo = self._clarear(
            cor,
            0.18
        )

        cor_base = self._escurecer(
            cor,
            0.10
        )

        for y in range(
            caixa_local[1],
            caixa_local[3] + 1
        ):
            p = (
                y - caixa_local[1]
            ) / max(
                caixa_local[3]
                - caixa_local[1],
                1
            )

            linha = tuple(
                int(
                    cor_topo[i]
                    + (
                        cor_base[i]
                        - cor_topo[i]
                    )
                    * p
                )
                for i in range(3)
            )

            desenho_base.line(
                (
                    caixa_local[0],
                    y,
                    caixa_local[2],
                    y
                ),
                fill=(
                    *linha,
                    255
                )
            )

        camada_base.putalpha(
            mascara
        )

        material.alpha_composite(
            camada_base
        )

        # Sombra interna.
        sombra_interna = Image.new(
            "RGBA",
            material.size,
            (0, 0, 0, 0)
        )

        desenho_interno = ImageDraw.Draw(
            sombra_interna
        )

        desenho_interno.rounded_rectangle(
            (
                caixa_local[0] + 8,
                caixa_local[1] + 8,
                caixa_local[2] - 8,
                caixa_local[3] - 8,
            ),
            radius=max(
                raio - 8,
                8
            ),
            outline=(0, 0, 0, 55),
            width=5
        )

        sombra_interna = sombra_interna.filter(
            ImageFilter.GaussianBlur(
                radius=5
            )
        )

        sombra_interna.putalpha(
            Image.composite(
                sombra_interna.getchannel("A"),
                Image.new(
                    "L",
                    material.size,
                    0
                ),
                mascara
            )
        )

        material.alpha_composite(
            sombra_interna
        )

        # Highlight superior.
        highlight = Image.new(
            "RGBA",
            material.size,
            (0, 0, 0, 0)
        )

        desenho_highlight = ImageDraw.Draw(
            highlight
        )

        desenho_highlight.rounded_rectangle(
            (
                caixa_local[0] + 10,
                caixa_local[1] + 8,
                caixa_local[2] - 10,
                caixa_local[1]
                + max(
                    int(
                        altura * 0.34
                    ),
                    20
                )
            ),
            radius=max(
                raio - 10,
                8
            ),
            fill=(255, 255, 255, 30)
        )

        highlight = highlight.filter(
            ImageFilter.GaussianBlur(
                radius=7
            )
        )

        highlight.putalpha(
            Image.composite(
                highlight.getchannel("A"),
                Image.new(
                    "L",
                    material.size,
                    0
                ),
                mascara
            )
        )

        material.alpha_composite(
            highlight
        )

        # Reflexo especular mascarado.
        reflexo = Image.new(
            "RGBA",
            material.size,
            (0, 0, 0, 0)
        )

        desenho_reflexo = ImageDraw.Draw(
            reflexo
        )

        progresso_reflexo = (
            progresso * 0.55
        ) % 1.0

        inicio_interno = (
            caixa_local[0]
            - 120
        )

        fim_interno = (
            caixa_local[2]
            + 120
        )

        centro = (
            inicio_interno
            + (
                fim_interno
                - inicio_interno
            )
            * progresso_reflexo
        )

        desenho_reflexo.polygon(
            [
                (
                    centro - 70,
                    caixa_local[1] - 10
                ),
                (
                    centro,
                    caixa_local[1] - 10
                ),
                (
                    centro + 105,
                    caixa_local[3] + 10
                ),
                (
                    centro + 35,
                    caixa_local[3] + 10
                ),
            ],
            fill=(
                255,
                255,
                255,
                int(
                    255
                    * max(
                        min(
                            intensidade_reflexo,
                            1.0
                        ),
                        0.0
                    )
                )
            )
        )

        reflexo = reflexo.filter(
            ImageFilter.GaussianBlur(
                radius=12
            )
        )

        # A máscara é aplicada depois do blur.
        alpha_reflexo = reflexo.getchannel(
            "A"
        )

        alpha_reflexo = Image.composite(
            alpha_reflexo,
            Image.new(
                "L",
                material.size,
                0
            ),
            mascara
        )

        reflexo.putalpha(
            alpha_reflexo
        )

        material.alpha_composite(
            reflexo
        )

        # Borda iluminada em duas camadas.
        borda = Image.new(
            "RGBA",
            material.size,
            (0, 0, 0, 0)
        )

        desenho_borda = ImageDraw.Draw(
            borda
        )

        desenho_borda.rounded_rectangle(
            caixa_local,
            radius=raio,
            outline=(255, 255, 255, 235),
            width=5
        )

        desenho_borda.rounded_rectangle(
            (
                caixa_local[0] + 6,
                caixa_local[1] + 6,
                caixa_local[2] - 6,
                caixa_local[3] - 6,
            ),
            radius=max(
                raio - 6,
                8
            ),
            outline=(255, 255, 255, 55),
            width=2
        )

        material.alpha_composite(
            borda
        )

        imagem_base.alpha_composite(
            material,
            (
                x1 - margem,
                y1 - margem
            )
        )

    def _clarear(
        self,
        cor,
        quantidade
    ):
        quantidade = max(
            min(float(quantidade), 1.0),
            0.0
        )

        return tuple(
            int(
                componente
                + (
                    255
                    - componente
                )
                * quantidade
            )
            for componente in cor
        )

    def _escurecer(
        self,
        cor,
        quantidade
    ):
        quantidade = max(
            min(float(quantidade), 1.0),
            0.0
        )

        return tuple(
            int(
                componente
                * (
                    1.0
                    - quantidade
                )
            )
            for componente in cor
        )
