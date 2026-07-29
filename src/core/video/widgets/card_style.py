from PIL import Image, ImageDraw, ImageFilter


class CardStyleFactory:
    """
    Desenha cartões com profundidade visual.

    Recursos:
    - sombra externa suave;
    - brilho superior;
    - borda interna;
    - leve faixa de reflexo;
    """

    def desenhar_cartao(
        self,
        imagem_base,
        caixa,
        cor,
        raio=34,
        sombra=(12, 16),
        intensidade_sombra=105,
        borda=(255, 255, 255),
        largura_borda=5,
    ):
        x1, y1, x2, y2 = caixa

        if imagem_base.mode != "RGBA":
            raise ValueError(
                "CardStyleFactory requer imagem-base em modo RGBA."
            )

        camada_sombra = Image.new(
            "RGBA",
            imagem_base.size,
            (0, 0, 0, 0),
        )

        desenho_sombra = ImageDraw.Draw(
            camada_sombra
        )

        desenho_sombra.rounded_rectangle(
            (
                x1 + sombra[0],
                y1 + sombra[1],
                x2 + sombra[0],
                y2 + sombra[1],
            ),
            radius=raio,
            fill=(
                0,
                0,
                0,
                intensidade_sombra,
            ),
        )

        camada_sombra = camada_sombra.filter(
            ImageFilter.GaussianBlur(
                radius=14
            )
        )

        imagem_base.alpha_composite(
            camada_sombra
        )

        desenho = ImageDraw.Draw(
            imagem_base
        )

        desenho.rounded_rectangle(
            caixa,
            radius=raio,
            fill=cor,
            outline=borda,
            width=largura_borda,
        )

        # Brilho superior.
        camada_brilho = Image.new(
            "RGBA",
            imagem_base.size,
            (0, 0, 0, 0),
        )

        desenho_brilho = ImageDraw.Draw(
            camada_brilho
        )

        altura = max(
            int(
                (y2 - y1)
                * 0.38
            ),
            1,
        )

        desenho_brilho.rounded_rectangle(
            (
                x1 + 8,
                y1 + 8,
                x2 - 8,
                y1 + altura,
            ),
            radius=max(
                raio - 8,
                8,
            ),
            fill=(
                255,
                255,
                255,
                28,
            ),
        )

        camada_brilho = camada_brilho.filter(
            ImageFilter.GaussianBlur(
                radius=7
            )
        )

        imagem_base.alpha_composite(
            camada_brilho
        )

        # Borda interna discreta.
        desenho.rounded_rectangle(
            (
                x1 + 10,
                y1 + 10,
                x2 - 10,
                y2 - 10,
            ),
            radius=max(
                raio - 10,
                8,
            ),
            outline=(
                255,
                255,
                255,
                45,
            ),
            width=2,
        )

    def criar_cartao_independente(
        self,
        tamanho,
        cor,
        raio=34,
    ):
        largura, altura = tamanho

        margem = 20

        imagem = Image.new(
            "RGBA",
            (
                largura + margem * 2,
                altura + margem * 2,
            ),
            (0, 0, 0, 0),
        )

        self.desenhar_cartao(
            imagem_base=imagem,
            caixa=(
                margem,
                margem,
                margem + largura - 1,
                margem + altura - 1,
            ),
            cor=cor,
            raio=raio,
            sombra=(7, 9),
            intensidade_sombra=90,
        )

        return imagem
