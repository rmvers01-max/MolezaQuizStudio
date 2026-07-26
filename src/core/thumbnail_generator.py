from pathlib import Path

from PIL import (
    Image,
    ImageDraw,
    ImageFilter,
    ImageFont,
    UnidentifiedImageError
)

from core.branding_manager import BrandingManager


class ThumbnailGenerator:
    LARGURA = 1280
    ALTURA = 720

    def __init__(self):
        self.fontes_windows = Path(
            "C:/Windows/Fonts"
        )

        self.branding_manager = (
            BrandingManager()
        )

    def gerar(
        self,
        pasta_projeto: Path,
        tema: str,
        quantidade_perguntas: int,
        texto_chamada: str = "VOCÊ CONSEGUE ACERTAR?",
        nome_arquivo: str = "thumbnail.png"
    ) -> Path:
        pasta_projeto = Path(
            pasta_projeto
        )

        pasta_projeto.mkdir(
            parents=True,
            exist_ok=True
        )

        caminho_saida = (
            pasta_projeto
            / nome_arquivo
        )

        imagem = Image.new(
            "RGB",
            (
                self.LARGURA,
                self.ALTURA
            ),
            "#132238"
        )

        self._desenhar_degrade(
            imagem
        )

        desenho = ImageDraw.Draw(
            imagem
        )

        self._desenhar_elementos_fundo(
            desenho
        )

        self._desenhar_sombra_principal(
            desenho
        )

        self._desenhar_identidade_canal(
            imagem=imagem,
            desenho=desenho
        )

        self._desenhar_chamada(
            desenho=desenho,
            texto=texto_chamada
        )

        self._desenhar_tema(
            desenho=desenho,
            tema=tema
        )

        self._desenhar_quantidade(
            desenho=desenho,
            quantidade_perguntas=(
                quantidade_perguntas
            )
        )

        self._desenhar_mascote(
            imagem=imagem,
            desenho=desenho
        )

        imagem.save(
            caminho_saida,
            format="PNG",
            optimize=True
        )

        return caminho_saida

    def _desenhar_degrade(
        self,
        imagem: Image.Image
    ):
        cor_inicio = (
            15,
            71,
            78
        )

        cor_fim = (
            7,
            28,
            51
        )

        desenho = ImageDraw.Draw(
            imagem
        )

        for y in range(
            self.ALTURA
        ):
            proporcao = (
                y
                / max(
                    self.ALTURA - 1,
                    1
                )
            )

            vermelho = int(
                cor_inicio[0]
                + (
                    cor_fim[0]
                    - cor_inicio[0]
                )
                * proporcao
            )

            verde = int(
                cor_inicio[1]
                + (
                    cor_fim[1]
                    - cor_inicio[1]
                )
                * proporcao
            )

            azul = int(
                cor_inicio[2]
                + (
                    cor_fim[2]
                    - cor_inicio[2]
                )
                * proporcao
            )

            desenho.line(
                (
                    0,
                    y,
                    self.LARGURA,
                    y
                ),
                fill=(
                    vermelho,
                    verde,
                    azul
                )
            )

    def _desenhar_elementos_fundo(
        self,
        desenho: ImageDraw.ImageDraw
    ):
        elementos = [
            (
                80,
                100,
                330,
                350
            ),
            (
                930,
                40,
                1270,
                380
            ),
            (
                970,
                440,
                1270,
                740
            ),
            (
                -120,
                470,
                190,
                780
            )
        ]

        for indice, coordenadas in enumerate(
            elementos
        ):
            if indice % 2 == 0:
                cor = "#174F55"
            else:
                cor = "#123D49"

            desenho.ellipse(
                coordenadas,
                fill=cor
            )

        for deslocamento in range(
            0,
            1500,
            120
        ):
            desenho.line(
                (
                    deslocamento,
                    0,
                    deslocamento - 360,
                    self.ALTURA
                ),
                fill="#164955",
                width=4
            )

    def _desenhar_sombra_principal(
        self,
        desenho: ImageDraw.ImageDraw
    ):
        desenho.rounded_rectangle(
            (
                80,
                90,
                1020,
                650
            ),
            radius=55,
            fill="#061B2C",
            outline="#1E6670",
            width=5
        )

        desenho.rounded_rectangle(
            (
                65,
                75,
                1005,
                635
            ),
            radius=55,
            fill="#0B3042",
            outline="#33A4A6",
            width=4
        )

    def _desenhar_identidade_canal(
        self,
        imagem: Image.Image,
        desenho: ImageDraw.ImageDraw
    ):
        caminho_logo = (
            self.branding_manager
            .obter_logo()
        )

        logo_adicionado = False

        if caminho_logo:
            logo_adicionado = (
                self._adicionar_imagem_transparente(
                    imagem_base=imagem,
                    caminho_imagem=caminho_logo,
                    caixa=(
                        105,
                        95,
                        430,
                        185
                    ),
                    alinhamento_horizontal="esquerda",
                    alinhamento_vertical="centro",
                    margem=8
                )
            )

        if not logo_adicionado:
            self._desenhar_selo_canal(
                desenho
            )

    def _desenhar_selo_canal(
        self,
        desenho: ImageDraw.ImageDraw
    ):
        fonte = self._carregar_fonte(
            tamanho=38,
            negrito=True
        )

        texto = "MOLEZA QUIZ"

        caixa = desenho.textbbox(
            (
                0,
                0
            ),
            texto,
            font=fonte
        )

        largura_texto = (
            caixa[2]
            - caixa[0]
        )

        x_inicial = 110
        y_inicial = 105

        desenho.rounded_rectangle(
            (
                x_inicial,
                y_inicial,
                x_inicial
                + largura_texto
                + 58,
                y_inicial
                + 68
            ),
            radius=24,
            fill="#F7C948"
        )

        desenho.text(
            (
                x_inicial + 29,
                y_inicial + 12
            ),
            texto,
            font=fonte,
            fill="#132238"
        )

    def _desenhar_chamada(
        self,
        desenho: ImageDraw.ImageDraw,
        texto: str
    ):
        texto = (
            texto.strip().upper()
            or "VOCÊ CONSEGUE ACERTAR?"
        )

        fonte = self._fonte_que_cabe(
            desenho=desenho,
            texto=texto,
            tamanho_inicial=64,
            tamanho_minimo=34,
            largura_maxima=820,
            negrito=True
        )

        desenho.text(
            (
                110,
                215
            ),
            texto,
            font=fonte,
            fill="#FFFFFF",
            stroke_width=2,
            stroke_fill="#071A29"
        )

    def _desenhar_tema(
        self,
        desenho: ImageDraw.ImageDraw,
        tema: str
    ):
        tema = (
            tema.strip().upper()
            or "QUIZ"
        )

        linhas, fonte = (
            self._quebrar_texto_com_fonte(
                desenho=desenho,
                texto=tema,
                largura_maxima=810,
                maximo_linhas=3,
                tamanho_inicial=92,
                tamanho_minimo=42
            )
        )

        y = 305

        for linha in linhas:
            caixa = desenho.textbbox(
                (
                    0,
                    0
                ),
                linha,
                font=fonte,
                stroke_width=3
            )

            altura_linha = (
                caixa[3]
                - caixa[1]
            )

            desenho.text(
                (
                    110,
                    y
                ),
                linha,
                font=fonte,
                fill="#F7C948",
                stroke_width=4,
                stroke_fill="#071A29"
            )

            y += (
                altura_linha
                + 14
            )

    def _desenhar_quantidade(
        self,
        desenho: ImageDraw.ImageDraw,
        quantidade_perguntas: int
    ):
        try:
            quantidade = int(
                quantidade_perguntas
            )

        except (
            TypeError,
            ValueError
        ):
            quantidade = 0

        if quantidade > 0:
            texto = (
                f"{quantidade} PERGUNTAS"
            )
        else:
            texto = "DESAFIO COMPLETO"

        fonte = self._carregar_fonte(
            tamanho=43,
            negrito=True
        )

        caixa = desenho.textbbox(
            (
                0,
                0
            ),
            texto,
            font=fonte
        )

        largura = (
            caixa[2]
            - caixa[0]
        )

        desenho.rounded_rectangle(
            (
                110,
                545,
                110 + largura + 56,
                610
            ),
            radius=22,
            fill="#E65353"
        )

        desenho.text(
            (
                138,
                556
            ),
            texto,
            font=fonte,
            fill="#FFFFFF"
        )

    def _desenhar_mascote(
        self,
        imagem: Image.Image,
        desenho: ImageDraw.ImageDraw
    ):
        caminho_mascote = (
            self.branding_manager
            .obter_mascote()
        )

        mascote_adicionado = False

        if caminho_mascote:
            mascote_adicionado = (
                self._adicionar_mascote_com_sombra(
                    imagem_base=imagem,
                    caminho_mascote=caminho_mascote
                )
            )

        if not mascote_adicionado:
            self._desenhar_mascote_simbolico(
                desenho
            )

    def _adicionar_mascote_com_sombra(
        self,
        imagem_base: Image.Image,
        caminho_mascote: Path
    ) -> bool:
        try:
            with Image.open(
                caminho_mascote
            ) as imagem_original:
                mascote = (
                    imagem_original
                    .convert("RGBA")
                    .copy()
                )

        except (
            OSError,
            ValueError,
            UnidentifiedImageError
        ):
            return False

        mascote = self._recortar_transparencia(
            mascote
        )

        if (
            mascote.width < 1
            or mascote.height < 1
        ):
            return False

        mascote.thumbnail(
            (
                310,
                430
            ),
            Image.Resampling.LANCZOS
        )

        if (
            mascote.width < 1
            or mascote.height < 1
        ):
            return False

        margem_sombra = 35

        largura_camada = (
            mascote.width
            + margem_sombra * 2
        )

        altura_camada = (
            mascote.height
            + margem_sombra * 2
        )

        camada_mascote = Image.new(
            "RGBA",
            (
                largura_camada,
                altura_camada
            ),
            (
                0,
                0,
                0,
                0
            )
        )

        mascara_original = mascote.getchannel(
            "A"
        )

        mascara_sombra = Image.new(
            "L",
            (
                largura_camada,
                altura_camada
            ),
            0
        )

        mascara_sombra.paste(
            mascara_original,
            (
                margem_sombra + 10,
                margem_sombra + 14
            )
        )

        mascara_sombra = (
            mascara_sombra
            .filter(
                ImageFilter.GaussianBlur(
                    radius=14
                )
            )
        )

        mascara_sombra = mascara_sombra.point(
            lambda valor: int(
                valor * 0.58
            )
        )

        sombra = Image.new(
            "RGBA",
            (
                largura_camada,
                altura_camada
            ),
            (
                0,
                0,
                0,
                0
            )
        )

        sombra.putalpha(
            mascara_sombra
        )

        camada_mascote.alpha_composite(
            sombra,
            (
                0,
                0
            )
        )

        camada_mascote.alpha_composite(
            mascote,
            (
                margem_sombra,
                margem_sombra
            )
        )

        posicao_x = (
            self.LARGURA
            - largura_camada
            - 5
        )

        posicao_y = (
            self.ALTURA
            - altura_camada
            + 8
        )

        posicao_x = max(
            posicao_x,
            0
        )

        posicao_y = max(
            posicao_y,
            0
        )

        base_rgba = imagem_base.convert(
            "RGBA"
        )

        base_rgba.alpha_composite(
            camada_mascote,
            (
                int(posicao_x),
                int(posicao_y)
            )
        )

        imagem_base.paste(
            base_rgba.convert("RGB")
        )

        return True

    def _recortar_transparencia(
        self,
        imagem: Image.Image
    ) -> Image.Image:
        if imagem.mode != "RGBA":
            imagem = imagem.convert(
                "RGBA"
            )

        canal_alpha = imagem.getchannel(
            "A"
        )

        caixa = canal_alpha.getbbox()

        if caixa is None:
            return imagem

        return imagem.crop(
            caixa
        )

    def _desenhar_mascote_simbolico(
        self,
        desenho: ImageDraw.ImageDraw
    ):
        desenho.ellipse(
            (
                1015,
                285,
                1205,
                525
            ),
            fill="#8B6A4E",
            outline="#F7C948",
            width=8
        )

        desenho.ellipse(
            (
                1045,
                330,
                1175,
                485
            ),
            fill="#C4A17E"
        )

        desenho.ellipse(
            (
                1060,
                345,
                1115,
                405
            ),
            fill="#EEE1CA"
        )

        desenho.ellipse(
            (
                1105,
                345,
                1160,
                405
            ),
            fill="#EEE1CA"
        )

        desenho.ellipse(
            (
                1080,
                365,
                1095,
                382
            ),
            fill="#132238"
        )

        desenho.ellipse(
            (
                1125,
                365,
                1140,
                382
            ),
            fill="#132238"
        )

        desenho.arc(
            (
                1080,
                390,
                1145,
                445
            ),
            start=10,
            end=170,
            fill="#132238",
            width=5
        )

    def _adicionar_imagem_transparente(
        self,
        imagem_base: Image.Image,
        caminho_imagem: Path,
        caixa: tuple,
        alinhamento_horizontal: str = "centro",
        alinhamento_vertical: str = "centro",
        margem: int = 0
    ) -> bool:
        caminho_imagem = Path(
            caminho_imagem
        )

        if not caminho_imagem.exists():
            return False

        try:
            with Image.open(
                caminho_imagem
            ) as imagem_original:
                elemento = (
                    imagem_original
                    .convert("RGBA")
                    .copy()
                )

        except (
            OSError,
            ValueError,
            UnidentifiedImageError
        ):
            return False

        elemento = self._recortar_transparencia(
            elemento
        )

        x1, y1, x2, y2 = caixa

        largura_disponivel = max(
            x2 - x1 - margem * 2,
            1
        )

        altura_disponivel = max(
            y2 - y1 - margem * 2,
            1
        )

        elemento.thumbnail(
            (
                largura_disponivel,
                altura_disponivel
            ),
            Image.Resampling.LANCZOS
        )

        if (
            elemento.width < 1
            or elemento.height < 1
        ):
            return False

        if alinhamento_horizontal == "esquerda":
            posicao_x = (
                x1
                + margem
            )

        elif alinhamento_horizontal == "direita":
            posicao_x = (
                x2
                - elemento.width
                - margem
            )

        else:
            posicao_x = (
                x1
                + (
                    x2
                    - x1
                    - elemento.width
                )
                // 2
            )

        if alinhamento_vertical == "topo":
            posicao_y = (
                y1
                + margem
            )

        elif alinhamento_vertical == "base":
            posicao_y = (
                y2
                - elemento.height
                - margem
            )

        else:
            posicao_y = (
                y1
                + (
                    y2
                    - y1
                    - elemento.height
                )
                // 2
            )

        base_rgba = imagem_base.convert(
            "RGBA"
        )

        base_rgba.alpha_composite(
            elemento,
            (
                int(posicao_x),
                int(posicao_y)
            )
        )

        imagem_base.paste(
            base_rgba.convert("RGB")
        )

        return True

    def _carregar_fonte(
        self,
        tamanho: int,
        negrito: bool = False
    ):
        nomes_fontes = []

        if negrito:
            nomes_fontes.extend(
                [
                    "arialbd.ttf",
                    "calibrib.ttf",
                    "segoeuib.ttf"
                ]
            )

        else:
            nomes_fontes.extend(
                [
                    "arial.ttf",
                    "calibri.ttf",
                    "segoeui.ttf"
                ]
            )

        for nome_fonte in nomes_fontes:
            caminho = (
                self.fontes_windows
                / nome_fonte
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

    def _fonte_que_cabe(
        self,
        desenho: ImageDraw.ImageDraw,
        texto: str,
        tamanho_inicial: int,
        tamanho_minimo: int,
        largura_maxima: int,
        negrito: bool = True
    ):
        for tamanho in range(
            tamanho_inicial,
            tamanho_minimo - 1,
            -2
        ):
            fonte = self._carregar_fonte(
                tamanho=tamanho,
                negrito=negrito
            )

            caixa = desenho.textbbox(
                (
                    0,
                    0
                ),
                texto,
                font=fonte
            )

            largura = (
                caixa[2]
                - caixa[0]
            )

            if largura <= largura_maxima:
                return fonte

        return self._carregar_fonte(
            tamanho=tamanho_minimo,
            negrito=negrito
        )

    def _quebrar_texto_com_fonte(
        self,
        desenho: ImageDraw.ImageDraw,
        texto: str,
        largura_maxima: int,
        maximo_linhas: int,
        tamanho_inicial: int,
        tamanho_minimo: int
    ):
        for tamanho in range(
            tamanho_inicial,
            tamanho_minimo - 1,
            -2
        ):
            fonte = self._carregar_fonte(
                tamanho=tamanho,
                negrito=True
            )

            linhas = self._quebrar_texto(
                desenho=desenho,
                texto=texto,
                fonte=fonte,
                largura_maxima=largura_maxima
            )

            if len(linhas) <= maximo_linhas:
                return linhas, fonte

        fonte = self._carregar_fonte(
            tamanho=tamanho_minimo,
            negrito=True
        )

        linhas = self._quebrar_texto(
            desenho=desenho,
            texto=texto,
            fonte=fonte,
            largura_maxima=largura_maxima
        )

        if len(linhas) > maximo_linhas:
            linhas = linhas[
                :maximo_linhas
            ]

            ultima_linha = (
                linhas[-1]
            )

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
                    font=fonte
                )

                largura = (
                    caixa[2]
                    - caixa[0]
                )

                if largura <= largura_maxima:
                    linhas[-1] = texto_teste
                    break

                ultima_linha = (
                    ultima_linha[:-1]
                )

        return linhas, fonte

    def _quebrar_texto(
        self,
        desenho: ImageDraw.ImageDraw,
        texto: str,
        fonte,
        largura_maxima: int
    ):
        palavras = texto.split()

        if not palavras:
            return [
                "QUIZ"
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
                font=fonte
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

        return linhas
