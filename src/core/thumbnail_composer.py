from pathlib import Path
from typing import Optional, Sequence, Union

from PIL import (
    Image,
    ImageDraw,
    ImageFilter,
    ImageFont,
    ImageOps,
    UnidentifiedImageError
)


Cor = Union[
    str,
    tuple[int, int, int],
    tuple[int, int, int, int]
]


class ThumbnailComposer:
    """
    Engine básica de composição de thumbnails por camadas.

    Permite adicionar:
    - fundos sólidos;
    - degradês;
    - imagens;
    - imagens dentro de molduras;
    - textos com contorno e sombra;
    - retângulos;
    - círculos;
    - faixas e elementos decorativos.

    Todas as operações são realizadas sobre uma imagem RGBA
    para preservar transparências durante a composição.
    """

    def __init__(
        self,
        largura: int = 1280,
        altura: int = 720,
        cor_fundo: Cor = "#101820"
    ):
        self.largura = int(largura)
        self.altura = int(altura)

        if self.largura < 1 or self.altura < 1:
            raise ValueError(
                "A largura e a altura devem ser maiores que zero."
            )

        self.imagem = Image.new(
            "RGBA",
            (
                self.largura,
                self.altura
            ),
            self._normalizar_cor(
                cor_fundo
            )
        )

        self.fontes_windows = Path(
            "C:/Windows/Fonts"
        )

    # =========================================================
    # FUNDO
    # =========================================================

    def definir_fundo_solido(
        self,
        cor: Cor
    ):
        self.imagem = Image.new(
            "RGBA",
            (
                self.largura,
                self.altura
            ),
            self._normalizar_cor(
                cor
            )
        )

    def definir_fundo_degrade_vertical(
        self,
        cor_inicio: Cor,
        cor_fim: Cor
    ):
        inicio = self._normalizar_cor(
            cor_inicio
        )

        fim = self._normalizar_cor(
            cor_fim
        )

        fundo = Image.new(
            "RGBA",
            (
                self.largura,
                self.altura
            ),
            inicio
        )

        desenho = ImageDraw.Draw(
            fundo
        )

        for y in range(
            self.altura
        ):
            proporcao = (
                y
                / max(
                    self.altura - 1,
                    1
                )
            )

            cor = tuple(
                int(
                    inicio[indice]
                    + (
                        fim[indice]
                        - inicio[indice]
                    )
                    * proporcao
                )
                for indice in range(4)
            )

            desenho.line(
                (
                    0,
                    y,
                    self.largura,
                    y
                ),
                fill=cor
            )

        self.imagem = fundo

    def definir_fundo_degrade_horizontal(
        self,
        cor_inicio: Cor,
        cor_fim: Cor
    ):
        inicio = self._normalizar_cor(
            cor_inicio
        )

        fim = self._normalizar_cor(
            cor_fim
        )

        fundo = Image.new(
            "RGBA",
            (
                self.largura,
                self.altura
            ),
            inicio
        )

        desenho = ImageDraw.Draw(
            fundo
        )

        for x in range(
            self.largura
        ):
            proporcao = (
                x
                / max(
                    self.largura - 1,
                    1
                )
            )

            cor = tuple(
                int(
                    inicio[indice]
                    + (
                        fim[indice]
                        - inicio[indice]
                    )
                    * proporcao
                )
                for indice in range(4)
            )

            desenho.line(
                (
                    x,
                    0,
                    x,
                    self.altura
                ),
                fill=cor
            )

        self.imagem = fundo

    # =========================================================
    # FORMAS
    # =========================================================

    def adicionar_retangulo(
        self,
        caixa: tuple[int, int, int, int],
        cor: Cor,
        raio: int = 0,
        contorno: Optional[Cor] = None,
        largura_contorno: int = 0
    ):
        camada = Image.new(
            "RGBA",
            self.imagem.size,
            (
                0,
                0,
                0,
                0
            )
        )

        desenho = ImageDraw.Draw(
            camada
        )

        preenchimento = self._normalizar_cor(
            cor
        )

        cor_contorno = (
            self._normalizar_cor(
                contorno
            )
            if contorno is not None
            else None
        )

        if raio > 0:
            desenho.rounded_rectangle(
                caixa,
                radius=int(raio),
                fill=preenchimento,
                outline=cor_contorno,
                width=max(
                    int(largura_contorno),
                    0
                )
            )

        else:
            desenho.rectangle(
                caixa,
                fill=preenchimento,
                outline=cor_contorno,
                width=max(
                    int(largura_contorno),
                    0
                )
            )

        self.imagem.alpha_composite(
            camada
        )

    def adicionar_circulo(
        self,
        caixa: tuple[int, int, int, int],
        cor: Cor,
        contorno: Optional[Cor] = None,
        largura_contorno: int = 0
    ):
        camada = Image.new(
            "RGBA",
            self.imagem.size,
            (
                0,
                0,
                0,
                0
            )
        )

        desenho = ImageDraw.Draw(
            camada
        )

        desenho.ellipse(
            caixa,
            fill=self._normalizar_cor(
                cor
            ),
            outline=(
                self._normalizar_cor(
                    contorno
                )
                if contorno is not None
                else None
            ),
            width=max(
                int(largura_contorno),
                0
            )
        )

        self.imagem.alpha_composite(
            camada
        )

    def adicionar_linhas_diagonais(
        self,
        cor: Cor,
        espacamento: int = 100,
        largura_linha: int = 4,
        inclinacao: int = 350
    ):
        camada = Image.new(
            "RGBA",
            self.imagem.size,
            (
                0,
                0,
                0,
                0
            )
        )

        desenho = ImageDraw.Draw(
            camada
        )

        espacamento = max(
            int(espacamento),
            20
        )

        for deslocamento in range(
            -self.altura,
            self.largura + self.altura,
            espacamento
        ):
            desenho.line(
                (
                    deslocamento,
                    0,
                    deslocamento - inclinacao,
                    self.altura
                ),
                fill=self._normalizar_cor(
                    cor
                ),
                width=max(
                    int(largura_linha),
                    1
                )
            )

        self.imagem.alpha_composite(
            camada
        )

    # =========================================================
    # IMAGENS
    # =========================================================

    def adicionar_imagem(
        self,
        caminho_imagem: Union[str, Path],
        caixa: tuple[int, int, int, int],
        preservar_proporcao: bool = True,
        preencher_caixa: bool = False,
        alinhamento_horizontal: str = "centro",
        alinhamento_vertical: str = "centro",
        opacidade: int = 255,
        sombra: bool = False,
        deslocamento_sombra: tuple[int, int] = (10, 12),
        desfoque_sombra: int = 14,
        opacidade_sombra: int = 115
    ) -> bool:
        elemento = self.carregar_imagem(
            caminho_imagem
        )

        if elemento is None:
            return False

        x1, y1, x2, y2 = caixa

        largura_caixa = max(
            x2 - x1,
            1
        )

        altura_caixa = max(
            y2 - y1,
            1
        )

        if preservar_proporcao:
            if preencher_caixa:
                elemento = ImageOps.fit(
                    elemento,
                    (
                        largura_caixa,
                        altura_caixa
                    ),
                    method=Image.Resampling.LANCZOS,
                    centering=(
                        0.5,
                        0.5
                    )
                )

            else:
                elemento.thumbnail(
                    (
                        largura_caixa,
                        altura_caixa
                    ),
                    Image.Resampling.LANCZOS
                )

        else:
            elemento = elemento.resize(
                (
                    largura_caixa,
                    altura_caixa
                ),
                Image.Resampling.LANCZOS
            )

        elemento = self._aplicar_opacidade(
            elemento,
            opacidade
        )

        posicao_x = self._calcular_posicao_horizontal(
            x1=x1,
            x2=x2,
            largura_elemento=elemento.width,
            alinhamento=alinhamento_horizontal
        )

        posicao_y = self._calcular_posicao_vertical(
            y1=y1,
            y2=y2,
            altura_elemento=elemento.height,
            alinhamento=alinhamento_vertical
        )

        if sombra:
            self._adicionar_sombra_imagem(
                elemento=elemento,
                posicao=(
                    posicao_x,
                    posicao_y
                ),
                deslocamento=deslocamento_sombra,
                desfoque=desfoque_sombra,
                opacidade=opacidade_sombra
            )

        self.imagem.alpha_composite(
            elemento,
            (
                int(posicao_x),
                int(posicao_y)
            )
        )

        return True

    def adicionar_imagem_em_moldura(
        self,
        caminho_imagem: Union[str, Path],
        caixa: tuple[int, int, int, int],
        raio: int = 30,
        cor_moldura: Cor = "#FFFFFF",
        espessura_moldura: int = 8,
        sombra: bool = True,
        cor_sombra: Cor = (
            0,
            0,
            0,
            130
        ),
        deslocamento_sombra: tuple[int, int] = (10, 14),
        desfoque_sombra: int = 16
    ) -> bool:
        elemento = self.carregar_imagem(
            caminho_imagem
        )

        if elemento is None:
            return False

        x1, y1, x2, y2 = caixa

        largura = max(
            x2 - x1,
            1
        )

        altura = max(
            y2 - y1,
            1
        )

        espessura = max(
            int(espessura_moldura),
            0
        )

        if sombra:
            camada_sombra = Image.new(
                "RGBA",
                self.imagem.size,
                (
                    0,
                    0,
                    0,
                    0
                )
            )

            mascara_sombra = Image.new(
                "L",
                self.imagem.size,
                0
            )

            desenho_mascara = ImageDraw.Draw(
                mascara_sombra
            )

            deslocamento_x, deslocamento_y = (
                deslocamento_sombra
            )

            desenho_mascara.rounded_rectangle(
                (
                    x1 + deslocamento_x,
                    y1 + deslocamento_y,
                    x2 + deslocamento_x,
                    y2 + deslocamento_y
                ),
                radius=raio,
                fill=255
            )

            mascara_sombra = mascara_sombra.filter(
                ImageFilter.GaussianBlur(
                    radius=max(
                        int(desfoque_sombra),
                        0
                    )
                )
            )

            cor_sombra_rgba = self._normalizar_cor(
                cor_sombra
            )

            sombra_colorida = Image.new(
                "RGBA",
                self.imagem.size,
                cor_sombra_rgba
            )

            sombra_colorida.putalpha(
                mascara_sombra.point(
                    lambda valor: int(
                        valor
                        * (
                            cor_sombra_rgba[3]
                            / 255
                        )
                    )
                )
            )

            camada_sombra.alpha_composite(
                sombra_colorida
            )

            self.imagem.alpha_composite(
                camada_sombra
            )

        self.adicionar_retangulo(
            caixa=caixa,
            cor=cor_moldura,
            raio=raio
        )

        caixa_interna = (
            x1 + espessura,
            y1 + espessura,
            x2 - espessura,
            y2 - espessura
        )

        largura_interna = max(
            caixa_interna[2]
            - caixa_interna[0],
            1
        )

        altura_interna = max(
            caixa_interna[3]
            - caixa_interna[1],
            1
        )

        imagem_recortada = ImageOps.fit(
            elemento,
            (
                largura_interna,
                altura_interna
            ),
            method=Image.Resampling.LANCZOS,
            centering=(
                0.5,
                0.5
            )
        )

        mascara = Image.new(
            "L",
            (
                largura_interna,
                altura_interna
            ),
            0
        )

        desenho_mascara = ImageDraw.Draw(
            mascara
        )

        raio_interno = max(
            raio - espessura,
            0
        )

        desenho_mascara.rounded_rectangle(
            (
                0,
                0,
                largura_interna,
                altura_interna
            ),
            radius=raio_interno,
            fill=255
        )

        imagem_recortada.putalpha(
            mascara
        )

        self.imagem.alpha_composite(
            imagem_recortada,
            (
                caixa_interna[0],
                caixa_interna[1]
            )
        )

        return True

    # =========================================================
    # TEXTOS
    # =========================================================

    def adicionar_texto(
        self,
        texto: str,
        caixa: tuple[int, int, int, int],
        tamanho_inicial: int = 72,
        tamanho_minimo: int = 24,
        cor: Cor = "#FFFFFF",
        negrito: bool = True,
        alinhamento_horizontal: str = "centro",
        alinhamento_vertical: str = "centro",
        maximo_linhas: int = 1,
        espacamento_linhas: int = 8,
        contorno: Optional[Cor] = None,
        largura_contorno: int = 0,
        sombra: bool = False,
        cor_sombra: Cor = (
            0,
            0,
            0,
            170
        ),
        deslocamento_sombra: tuple[int, int] = (6, 7)
    ):
        texto = str(
            texto
        ).strip()

        if not texto:
            return

        x1, y1, x2, y2 = caixa

        largura_maxima = max(
            x2 - x1,
            1
        )

        altura_maxima = max(
            y2 - y1,
            1
        )

        fonte, linhas = self._encontrar_fonte_e_linhas(
            texto=texto,
            largura_maxima=largura_maxima,
            altura_maxima=altura_maxima,
            tamanho_inicial=tamanho_inicial,
            tamanho_minimo=tamanho_minimo,
            negrito=negrito,
            maximo_linhas=maximo_linhas,
            espacamento_linhas=espacamento_linhas,
            largura_contorno=largura_contorno
        )

        camada = Image.new(
            "RGBA",
            self.imagem.size,
            (
                0,
                0,
                0,
                0
            )
        )

        desenho = ImageDraw.Draw(
            camada
        )

        alturas = []

        for linha in linhas:
            caixa_linha = desenho.textbbox(
                (
                    0,
                    0
                ),
                linha,
                font=fonte,
                stroke_width=max(
                    largura_contorno,
                    0
                )
            )

            alturas.append(
                caixa_linha[3]
                - caixa_linha[1]
            )

        altura_total = (
            sum(
                alturas
            )
            + max(
                len(linhas) - 1,
                0
            )
            * espacamento_linhas
        )

        if alinhamento_vertical == "topo":
            y_atual = y1

        elif alinhamento_vertical == "base":
            y_atual = (
                y2
                - altura_total
            )

        else:
            y_atual = (
                y1
                + (
                    altura_maxima
                    - altura_total
                )
                // 2
            )

        for indice, linha in enumerate(
            linhas
        ):
            caixa_linha = desenho.textbbox(
                (
                    0,
                    0
                ),
                linha,
                font=fonte,
                stroke_width=max(
                    largura_contorno,
                    0
                )
            )

            largura_linha = (
                caixa_linha[2]
                - caixa_linha[0]
            )

            if alinhamento_horizontal == "esquerda":
                x_texto = x1

            elif alinhamento_horizontal == "direita":
                x_texto = (
                    x2
                    - largura_linha
                )

            else:
                x_texto = (
                    x1
                    + (
                        largura_maxima
                        - largura_linha
                    )
                    // 2
                )

            if sombra:
                deslocamento_x, deslocamento_y = (
                    deslocamento_sombra
                )

                desenho.text(
                    (
                        x_texto + deslocamento_x,
                        y_atual + deslocamento_y
                    ),
                    linha,
                    font=fonte,
                    fill=self._normalizar_cor(
                        cor_sombra
                    ),
                    stroke_width=max(
                        largura_contorno,
                        0
                    ),
                    stroke_fill=self._normalizar_cor(
                        cor_sombra
                    )
                )

            desenho.text(
                (
                    x_texto,
                    y_atual
                ),
                linha,
                font=fonte,
                fill=self._normalizar_cor(
                    cor
                ),
                stroke_width=max(
                    largura_contorno,
                    0
                ),
                stroke_fill=(
                    self._normalizar_cor(
                        contorno
                    )
                    if contorno is not None
                    else None
                )
            )

            y_atual += (
                alturas[indice]
                + espacamento_linhas
            )

        self.imagem.alpha_composite(
            camada
        )

    # =========================================================
    # EXPORTAÇÃO
    # =========================================================

    def salvar(
        self,
        caminho_saida: Union[str, Path],
        qualidade: int = 95
    ) -> Path:
        caminho_saida = Path(
            caminho_saida
        )

        caminho_saida.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        extensao = caminho_saida.suffix.lower()

        if extensao in {
            ".jpg",
            ".jpeg"
        }:
            imagem_saida = self.imagem.convert(
                "RGB"
            )

            imagem_saida.save(
                caminho_saida,
                format="JPEG",
                quality=max(
                    min(
                        int(qualidade),
                        100
                    ),
                    1
                ),
                optimize=True
            )

        else:
            imagem_saida = self.imagem.convert(
                "RGBA"
            )

            imagem_saida.save(
                caminho_saida,
                format="PNG",
                optimize=True
            )

        return caminho_saida

    def obter_imagem(self) -> Image.Image:
        return self.imagem.copy()

    # =========================================================
    # MÉTODOS AUXILIARES
    # =========================================================

    def carregar_imagem(
        self,
        caminho_imagem: Union[str, Path]
    ) -> Optional[Image.Image]:
        caminho = Path(
            caminho_imagem
        )

        if not caminho.exists():
            return None

        try:
            with Image.open(
                caminho
            ) as imagem_original:
                imagem = (
                    imagem_original
                    .convert("RGBA")
                    .copy()
                )

            return self._recortar_transparencia(
                imagem
            )

        except (
            OSError,
            ValueError,
            UnidentifiedImageError
        ):
            return None

    def carregar_fonte(
        self,
        tamanho: int,
        negrito: bool = False
    ):
        tamanho = max(
            int(tamanho),
            1
        )

        if negrito:
            nomes = [
                "arialbd.ttf",
                "calibrib.ttf",
                "segoeuib.ttf",
                "impact.ttf"
            ]

        else:
            nomes = [
                "arial.ttf",
                "calibri.ttf",
                "segoeui.ttf"
            ]

        for nome in nomes:
            caminho = (
                self.fontes_windows
                / nome
            )

            if not caminho.exists():
                continue

            try:
                return ImageFont.truetype(
                    str(caminho),
                    tamanho
                )

            except OSError:
                continue

        return ImageFont.load_default()

    def _encontrar_fonte_e_linhas(
        self,
        texto: str,
        largura_maxima: int,
        altura_maxima: int,
        tamanho_inicial: int,
        tamanho_minimo: int,
        negrito: bool,
        maximo_linhas: int,
        espacamento_linhas: int,
        largura_contorno: int
    ):
        desenho_teste = ImageDraw.Draw(
            Image.new(
                "RGBA",
                (
                    10,
                    10
                )
            )
        )

        for tamanho in range(
            tamanho_inicial,
            tamanho_minimo - 1,
            -2
        ):
            fonte = self.carregar_fonte(
                tamanho=tamanho,
                negrito=negrito
            )

            linhas = self._quebrar_texto(
                desenho=desenho_teste,
                texto=texto,
                fonte=fonte,
                largura_maxima=largura_maxima,
                maximo_linhas=maximo_linhas,
                largura_contorno=largura_contorno
            )

            alturas = []

            for linha in linhas:
                caixa = desenho_teste.textbbox(
                    (
                        0,
                        0
                    ),
                    linha,
                    font=fonte,
                    stroke_width=max(
                        largura_contorno,
                        0
                    )
                )

                alturas.append(
                    caixa[3]
                    - caixa[1]
                )

            altura_total = (
                sum(
                    alturas
                )
                + max(
                    len(linhas) - 1,
                    0
                )
                * espacamento_linhas
            )

            if (
                len(linhas) <= maximo_linhas
                and altura_total <= altura_maxima
            ):
                return fonte, linhas

        fonte = self.carregar_fonte(
            tamanho=tamanho_minimo,
            negrito=negrito
        )

        linhas = self._quebrar_texto(
            desenho=desenho_teste,
            texto=texto,
            fonte=fonte,
            largura_maxima=largura_maxima,
            maximo_linhas=maximo_linhas,
            largura_contorno=largura_contorno
        )

        return fonte, linhas

    def _quebrar_texto(
        self,
        desenho: ImageDraw.ImageDraw,
        texto: str,
        fonte,
        largura_maxima: int,
        maximo_linhas: int,
        largura_contorno: int
    ) -> list[str]:
        palavras = texto.split()

        if not palavras:
            return [
                ""
            ]

        linhas = []
        linha_atual = palavras[0]

        for palavra in palavras[1:]:
            teste = (
                f"{linha_atual} {palavra}"
            )

            caixa = desenho.textbbox(
                (
                    0,
                    0
                ),
                teste,
                font=fonte,
                stroke_width=max(
                    largura_contorno,
                    0
                )
            )

            largura = (
                caixa[2]
                - caixa[0]
            )

            if largura <= largura_maxima:
                linha_atual = teste

            else:
                linhas.append(
                    linha_atual
                )

                linha_atual = palavra

        linhas.append(
            linha_atual
        )

        if len(linhas) <= maximo_linhas:
            return linhas

        linhas = linhas[
            :maximo_linhas
        ]

        ultima_linha = linhas[-1]

        while ultima_linha:
            texto_teste = (
                ultima_linha.rstrip()
                + "..."
            )

            caixa = desenho.textbbox(
                (
                    0,
                    0
                ),
                texto_teste,
                font=fonte,
                stroke_width=max(
                    largura_contorno,
                    0
                )
            )

            largura = (
                caixa[2]
                - caixa[0]
            )

            if largura <= largura_maxima:
                linhas[-1] = texto_teste
                break

            ultima_linha = ultima_linha[:-1]

        return linhas

    def _adicionar_sombra_imagem(
        self,
        elemento: Image.Image,
        posicao: tuple[int, int],
        deslocamento: tuple[int, int],
        desfoque: int,
        opacidade: int
    ):
        canal_alpha = elemento.getchannel(
            "A"
        )

        camada_sombra = Image.new(
            "RGBA",
            self.imagem.size,
            (
                0,
                0,
                0,
                0
            )
        )

        mascara = Image.new(
            "L",
            self.imagem.size,
            0
        )

        x, y = posicao
        dx, dy = deslocamento

        mascara.paste(
            canal_alpha,
            (
                x + dx,
                y + dy
            )
        )

        mascara = mascara.filter(
            ImageFilter.GaussianBlur(
                radius=max(
                    int(desfoque),
                    0
                )
            )
        )

        mascara = mascara.point(
            lambda valor: int(
                valor
                * (
                    max(
                        min(
                            int(opacidade),
                            255
                        ),
                        0
                    )
                    / 255
                )
            )
        )

        sombra = Image.new(
            "RGBA",
            self.imagem.size,
            (
                0,
                0,
                0,
                255
            )
        )

        sombra.putalpha(
            mascara
        )

        camada_sombra.alpha_composite(
            sombra
        )

        self.imagem.alpha_composite(
            camada_sombra
        )

    def _recortar_transparencia(
        self,
        imagem: Image.Image
    ) -> Image.Image:
        if imagem.mode != "RGBA":
            imagem = imagem.convert(
                "RGBA"
            )

        caixa = imagem.getchannel(
            "A"
        ).getbbox()

        if caixa is None:
            return imagem

        return imagem.crop(
            caixa
        )

    def _aplicar_opacidade(
        self,
        imagem: Image.Image,
        opacidade: int
    ) -> Image.Image:
        opacidade = max(
            min(
                int(opacidade),
                255
            ),
            0
        )

        if opacidade == 255:
            return imagem

        imagem = imagem.copy()

        canal_alpha = imagem.getchannel(
            "A"
        )

        canal_alpha = canal_alpha.point(
            lambda valor: int(
                valor
                * (
                    opacidade
                    / 255
                )
            )
        )

        imagem.putalpha(
            canal_alpha
        )

        return imagem

    def _calcular_posicao_horizontal(
        self,
        x1: int,
        x2: int,
        largura_elemento: int,
        alinhamento: str
    ) -> int:
        if alinhamento == "esquerda":
            return x1

        if alinhamento == "direita":
            return (
                x2
                - largura_elemento
            )

        return (
            x1
            + (
                x2
                - x1
                - largura_elemento
            )
            // 2
        )

    def _calcular_posicao_vertical(
        self,
        y1: int,
        y2: int,
        altura_elemento: int,
        alinhamento: str
    ) -> int:
        if alinhamento == "topo":
            return y1

        if alinhamento == "base":
            return (
                y2
                - altura_elemento
            )

        return (
            y1
            + (
                y2
                - y1
                - altura_elemento
            )
            // 2
        )

    def _normalizar_cor(
        self,
        cor: Cor
    ) -> tuple[int, int, int, int]:
        if isinstance(
            cor,
            str
        ):
            cor = cor.strip()

            if cor.startswith("#"):
                valor = cor.lstrip(
                    "#"
                )

                if len(valor) == 6:
                    return (
                        int(
                            valor[0:2],
                            16
                        ),
                        int(
                            valor[2:4],
                            16
                        ),
                        int(
                            valor[4:6],
                            16
                        ),
                        255
                    )

                if len(valor) == 8:
                    return (
                        int(
                            valor[0:2],
                            16
                        ),
                        int(
                            valor[2:4],
                            16
                        ),
                        int(
                            valor[4:6],
                            16
                        ),
                        int(
                            valor[6:8],
                            16
                        )
                    )

            raise ValueError(
                f"Cor inválida: {cor}"
            )

        valores = tuple(
            int(
                valor
            )
            for valor in cor
        )

        if len(valores) == 3:
            return (
                valores[0],
                valores[1],
                valores[2],
                255
            )

        if len(valores) == 4:
            return valores

        raise ValueError(
            f"Cor inválida: {cor}"
        )
