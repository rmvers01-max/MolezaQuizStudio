from pathlib import Path
from typing import Optional

from PIL import Image, ImageDraw, ImageFont


class ThumbnailGenerator:
    LARGURA = 1280
    ALTURA = 720

    def __init__(self):
        self.fontes_windows = Path("C:/Windows/Fonts")

    def gerar(
        self,
        pasta_projeto: Path,
        tema: str,
        quantidade_perguntas: int,
        texto_chamada: str = "VOCÊ CONSEGUE ACERTAR?",
        nome_arquivo: str = "thumbnail.png"
    ) -> Path:
        pasta_projeto = Path(pasta_projeto)
        pasta_projeto.mkdir(
            parents=True,
            exist_ok=True
        )

        caminho_saida = pasta_projeto / nome_arquivo

        imagem = Image.new(
            "RGB",
            (
                self.LARGURA,
                self.ALTURA
            ),
            "#132238"
        )

        desenho = ImageDraw.Draw(imagem)

        self._desenhar_degrade(imagem)
        self._desenhar_elementos_fundo(desenho)
        self._desenhar_sombra_principal(desenho)
        self._desenhar_selo_canal(desenho)
        self._desenhar_chamada(
            desenho,
            texto_chamada
        )
        self._desenhar_tema(
            desenho,
            tema
        )
        self._desenhar_quantidade(
            desenho,
            quantidade_perguntas
        )
        self._desenhar_mascote_simbolico(
            desenho
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

        pixels = imagem.load()

        for y in range(self.ALTURA):
            proporcao = y / max(
                self.ALTURA - 1,
                1
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

            for x in range(self.LARGURA):
                pixels[x, y] = (
                    vermelho,
                    verde,
                    azul
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

        linhas, fonte = self._quebrar_texto_com_fonte(
            desenho=desenho,
            texto=tema,
            largura_maxima=810,
            maximo_linhas=3,
            tamanho_inicial=92,
            tamanho_minimo=42
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

            y += altura_linha + 14

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

        texto = (
            f"{quantidade} PERGUNTAS"
            if quantidade > 0
            else "DESAFIO COMPLETO"
        )

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

        largura = caixa[2] - caixa[0]

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

    def _desenhar_mascote_simbolico(
        self,
        desenho: ImageDraw.ImageDraw
    ):
        centro_x = 1110
        centro_y = 405

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

        fonte = self._carregar_fonte(
            tamanho=28,
            negrito=True
        )

        texto = "🦥"

        try:
            desenho.text(
                (
                    centro_x,
                    550
                ),
                texto,
                font=fonte,
                anchor="mm",
                fill="#FFFFFF"
            )
        except UnicodeEncodeError:
            pass

    def _carregar_fonte(
        self,
        tamanho: int,
        negrito: bool = False
    ) -> ImageFont.FreeTypeFont:
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

            largura = caixa[2] - caixa[0]

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
            linhas = linhas[:maximo_linhas]

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
                    font=fonte
                )

                largura = caixa[2] - caixa[0]

                if largura <= largura_maxima:
                    linhas[-1] = texto_teste
                    break

                ultima_linha = ultima_linha[:-1]

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
            return ["QUIZ"]

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

            largura = caixa[2] - caixa[0]

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
