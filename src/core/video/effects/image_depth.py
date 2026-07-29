from PIL import Image, ImageDraw, ImageFilter


class ImageDepthFactory:
    """Adiciona sombra, fundo claro, borda e brilho às imagens."""

    def preparar(
        self,
        imagem,
        padding=10,
        raio=18
    ):
        imagem = imagem.convert(
            "RGBA"
        )

        largura = (
            imagem.width
            + padding * 2
        )

        altura = (
            imagem.height
            + padding * 2
        )

        base = Image.new(
            "RGBA",
            (
                largura + 18,
                altura + 20
            ),
            (0, 0, 0, 0)
        )

        sombra = Image.new(
            "RGBA",
            base.size,
            (0, 0, 0, 0)
        )

        desenho_sombra = ImageDraw.Draw(
            sombra
        )

        desenho_sombra.rounded_rectangle(
            (
                12,
                14,
                12 + largura,
                14 + altura
            ),
            radius=raio,
            fill=(0, 0, 0, 95)
        )

        sombra = sombra.filter(
            ImageFilter.GaussianBlur(
                radius=9
            )
        )

        base.alpha_composite(
            sombra
        )

        painel = Image.new(
            "RGBA",
            (
                largura,
                altura
            ),
            (255, 255, 255, 240)
        )

        mascara = Image.new(
            "L",
            (
                largura,
                altura
            ),
            0
        )

        desenho_mascara = ImageDraw.Draw(
            mascara
        )

        desenho_mascara.rounded_rectangle(
            (
                0,
                0,
                largura - 1,
                altura - 1
            ),
            radius=raio,
            fill=255
        )

        painel.putalpha(
            mascara
        )

        painel.alpha_composite(
            imagem,
            (padding, padding)
        )

        desenho = ImageDraw.Draw(
            painel
        )

        desenho.rounded_rectangle(
            (
                1,
                1,
                largura - 2,
                altura - 2
            ),
            radius=raio,
            outline=(
                255,
                255,
                255,
                190
            ),
            width=3
        )

        brilho = Image.new(
            "RGBA",
            painel.size,
            (0, 0, 0, 0)
        )

        desenho_brilho = ImageDraw.Draw(
            brilho
        )

        desenho_brilho.rounded_rectangle(
            (
                8,
                8,
                largura - 8,
                max(
                    int(
                        altura * 0.34
                    ),
                    18
                )
            ),
            radius=max(
                raio - 6,
                8
            ),
            fill=(
                255,
                255,
                255,
                30
            )
        )

        brilho = brilho.filter(
            ImageFilter.GaussianBlur(
                radius=5
            )
        )

        painel.alpha_composite(
            brilho
        )

        base.alpha_composite(
            painel,
            (4, 4)
        )

        return base
