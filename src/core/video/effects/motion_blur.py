from PIL import Image, ImageFilter


class MotionBlurEngine:
    """Desfoque direcional discreto durante entradas rápidas."""

    def intensidade_entrada(
        self,
        progresso,
        limite=0.72
    ):
        progresso = max(
            min(float(progresso), 1.0),
            0.0
        )

        if progresso >= limite:
            return 0.0

        local = progresso / max(
            limite,
            0.001
        )

        return max(
            1.0 - local,
            0.0
        )

    def aplicar_horizontal(
        self,
        imagem,
        intensidade,
        direcao=1
    ):
        intensidade = max(
            min(float(intensidade), 1.0),
            0.0
        )

        if intensidade <= 0.01:
            return imagem

        deslocamento = max(
            int(16 * intensidade),
            1
        )

        resultado = Image.new(
            "RGBA",
            imagem.size,
            (0, 0, 0, 0)
        )

        passos = 5

        for indice in range(passos):
            proporcao = indice / max(
                passos - 1,
                1
            )

            dx = int(
                deslocamento
                * proporcao
                * (
                    -1
                    if direcao < 0
                    else 1
                )
            )

            camada = Image.new(
                "RGBA",
                imagem.size,
                (0, 0, 0, 0)
            )

            camada.alpha_composite(
                imagem,
                (dx, 0)
            )

            alpha = int(
                255 / passos
            )

            canal = camada.getchannel(
                "A"
            ).point(
                lambda valor: int(
                    valor
                    * alpha
                    / 255
                )
            )

            camada.putalpha(
                canal
            )

            resultado.alpha_composite(
                camada
            )

        return resultado.filter(
            ImageFilter.GaussianBlur(
                radius=0.7
            )
        )
