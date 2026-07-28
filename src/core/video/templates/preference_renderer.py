from pathlib import Path
import math
import textwrap

from PIL import Image, ImageDraw, ImageFont, ImageOps

from ..legacy_generator import LegacyVideoGenerator


class ProfessionalPreferenceRenderer(LegacyVideoGenerator):
    """
    Primeiro renderer visual profissional para quizzes de preferência.

    Reaproveita toda a lógica de áudio, montagem e exportação do gerador
    legado, alterando somente a identidade visual dos frames.
    """

    COR_A = (255, 85, 115)
    COR_B = (66, 145, 255)
    COR_DESTAQUE = (255, 214, 75)
    COR_TEXTO = (255, 255, 255)
    COR_ESCURO = (24, 24, 45)

    def _criar_base(self):
        imagem = Image.new(
            "RGB",
            (self.largura, self.altura),
            self.COR_ESCURO
        )

        desenho = ImageDraw.Draw(imagem)

        cor_inicio = (88, 40, 170)
        cor_fim = (25, 18, 70)

        for y in range(self.altura):
            proporcao = y / max(self.altura - 1, 1)

            cor = tuple(
                int(
                    cor_inicio[indice]
                    + (
                        cor_fim[indice]
                        - cor_inicio[indice]
                    )
                    * proporcao
                )
                for indice in range(3)
            )

            desenho.line(
                (0, y, self.largura, y),
                fill=cor
            )

        # Bolhas decorativas.
        for caixa, cor in [
            ((-120, -80, 280, 320), (130, 90, 220)),
            ((1010, -100, 1390, 280), (70, 120, 230)),
            ((980, 500, 1360, 850), (180, 60, 170)),
            ((-150, 510, 240, 880), (80, 180, 190)),
        ]:
            desenho.ellipse(
                caixa,
                fill=cor
            )

        desenho.rounded_rectangle(
            (34, 28, 1246, 692),
            radius=42,
            fill=(255, 255, 255),
            outline=(255, 255, 255),
            width=3
        )

        desenho.rounded_rectangle(
            (50, 44, 1230, 676),
            radius=34,
            fill=(35, 28, 78)
        )

        return imagem, desenho

    def _desenhar_cabecalho(
        self,
        desenho,
        numero
    ):
        desenho.rounded_rectangle(
            (80, 62, 1200, 132),
            radius=24,
            fill=(255, 255, 255)
        )

        fonte_logo = self._carregar_fonte_negrito(34)
        fonte_numero = self._carregar_fonte_negrito(28)

        desenho.text(
            (110, 79),
            "MOLEZA QUIZ",
            font=fonte_logo,
            fill=(83, 45, 165)
        )

        texto_numero = f"PERGUNTA {numero}"

        caixa = desenho.textbbox(
            (0, 0),
            texto_numero,
            font=fonte_numero
        )

        largura = caixa[2] - caixa[0]

        desenho.rounded_rectangle(
            (
                1160 - largura - 44,
                76,
                1170,
                119
            ),
            radius=18,
            fill=(255, 214, 75)
        )

        desenho.text(
            (
                1148 - largura,
                82
            ),
            texto_numero,
            font=fonte_numero,
            fill=(47, 33, 75)
        )

    def _desenhar_pergunta_e_alternativas(
        self,
        imagem,
        desenho,
        pergunta
    ):
        texto_pergunta = str(
            pergunta.get(
                "pergunta",
                "O que você prefere?"
            )
        ).strip()

        alternativas = pergunta.get(
            "alternativas",
            []
        )

        alternativa_a = (
            str(alternativas[0]).strip()
            if len(alternativas) >= 1
            else "OPÇÃO A"
        )

        alternativa_b = (
            str(alternativas[1]).strip()
            if len(alternativas) >= 2
            else "OPÇÃO B"
        )

        fonte_pergunta = self._carregar_fonte_negrito(42)
        y = 154

        linhas = textwrap.wrap(
            texto_pergunta,
            width=42
        )[:2]

        for linha in linhas:
            caixa = desenho.textbbox(
                (0, 0),
                linha,
                font=fonte_pergunta
            )
            largura = caixa[2] - caixa[0]

            desenho.text(
                (
                    (self.largura - largura) / 2,
                    y
                ),
                linha,
                font=fonte_pergunta,
                fill=self.COR_TEXTO
            )

            y += 50

        topo_cartao = 275
        base_cartao = 535

        desenho.rounded_rectangle(
            (90, topo_cartao, 570, base_cartao),
            radius=34,
            fill=self.COR_A,
            outline=(255, 255, 255),
            width=5
        )

        desenho.rounded_rectangle(
            (710, topo_cartao, 1190, base_cartao),
            radius=34,
            fill=self.COR_B,
            outline=(255, 255, 255),
            width=5
        )

        caminho_imagem_a = self._obter_caminho_imagem(
            pergunta,
            indice=0
        )

        caminho_imagem_b = self._obter_caminho_imagem(
            pergunta,
            indice=1
        )

        self._desenhar_opcao(
            imagem_base=imagem,
            desenho=desenho,
            centro_x=330,
            topo=topo_cartao,
            letra="A",
            texto=alternativa_a,
            caminho_imagem=caminho_imagem_a,
            cor_cartao=self.COR_A
        )

        self._desenhar_opcao(
            imagem_base=imagem,
            desenho=desenho,
            centro_x=950,
            topo=topo_cartao,
            letra="B",
            texto=alternativa_b,
            caminho_imagem=caminho_imagem_b,
            cor_cartao=self.COR_B
        )

        desenho.ellipse(
            (590, 340, 690, 440),
            fill=self.COR_DESTAQUE,
            outline=(255, 255, 255),
            width=5
        )

        fonte_ou = self._carregar_fonte_negrito(34)

        caixa = desenho.textbbox(
            (0, 0),
            "OU",
            font=fonte_ou
        )

        largura = caixa[2] - caixa[0]
        altura = caixa[3] - caixa[1]

        desenho.text(
            (
                640 - largura / 2,
                390 - altura / 2 - 4
            ),
            "OU",
            font=fonte_ou,
            fill=(45, 34, 72)
        )

    def _desenhar_opcao(
        self,
        imagem_base,
        desenho,
        centro_x,
        topo,
        letra,
        texto,
        caminho_imagem,
        cor_cartao
    ):
        desenho.ellipse(
            (
                centro_x - 34,
                topo + 18,
                centro_x + 34,
                topo + 86
            ),
            fill=(255, 255, 255)
        )

        fonte_letra = self._carregar_fonte_negrito(34)

        caixa = desenho.textbbox(
            (0, 0),
            letra,
            font=fonte_letra
        )

        largura = caixa[2] - caixa[0]
        altura = caixa[3] - caixa[1]

        desenho.text(
            (
                centro_x - largura / 2,
                topo + 52 - altura / 2 - 4
            ),
            letra,
            font=fonte_letra,
            fill=(54, 38, 91)
        )

        imagem_adicionada = self._colar_imagem_opcao(
            imagem_base=imagem_base,
            caminho_imagem=caminho_imagem,
            centro_x=centro_x,
            topo=topo
        )

        fonte_texto = self._carregar_fonte_negrito(
            27 if imagem_adicionada else 31
        )

        linhas = textwrap.wrap(
            texto,
            width=21 if imagem_adicionada else 19
        )[:2 if imagem_adicionada else 3]

        if imagem_adicionada:
            y = topo + 208
        else:
            altura_total = len(linhas) * 40
            y = topo + 145 - altura_total / 2

        for linha in linhas:
            caixa = desenho.textbbox(
                (0, 0),
                linha,
                font=fonte_texto
            )

            largura = caixa[2] - caixa[0]

            desenho.text(
                (
                    centro_x - largura / 2,
                    y
                ),
                linha,
                font=fonte_texto,
                fill=(255, 255, 255)
            )

            y += 34 if imagem_adicionada else 40

    def _colar_imagem_opcao(
        self,
        imagem_base,
        caminho_imagem,
        centro_x,
        topo
    ) -> bool:
        if caminho_imagem is None:
            return False

        caminho = Path(
            caminho_imagem
        )

        if not caminho.exists() or not caminho.is_file():
            return False

        try:
            imagem_opcao = Image.open(
                caminho
            ).convert("RGBA")

            largura_alvo = 330
            altura_alvo = 118

            imagem_opcao = ImageOps.contain(
                imagem_opcao,
                (
                    largura_alvo,
                    altura_alvo
                ),
                method=Image.Resampling.LANCZOS
            )

            fundo = Image.new(
                "RGBA",
                (
                    largura_alvo,
                    altura_alvo
                ),
                (255, 255, 255, 245)
            )

            x = (
                largura_alvo
                - imagem_opcao.width
            ) // 2

            y = (
                altura_alvo
                - imagem_opcao.height
            ) // 2

            fundo.alpha_composite(
                imagem_opcao,
                (x, y)
            )

            mascara = Image.new(
                "L",
                (
                    largura_alvo,
                    altura_alvo
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
                    largura_alvo - 1,
                    altura_alvo - 1
                ),
                radius=22,
                fill=255
            )

            fundo.putalpha(
                mascara
            )

            destino_x = int(
                centro_x
                - largura_alvo / 2
            )

            destino_y = int(
                topo + 82
            )

            imagem_base.paste(
                fundo,
                (
                    destino_x,
                    destino_y
                ),
                fundo
            )

            return True

        except (
            OSError,
            ValueError
        ):
            return False

    def _obter_caminho_imagem(
        self,
        pergunta,
        indice
    ):
        campos_por_indice = {
            0: (
                "imagem_a",
                "imagem_esquerda",
                "imagem_opcao_a",
                "imagem_1"
            ),
            1: (
                "imagem_b",
                "imagem_direita",
                "imagem_opcao_b",
                "imagem_2"
            )
        }

        for campo in campos_por_indice.get(
            indice,
            ()
        ):
            valor = pergunta.get(
                campo
            )

            if valor:
                return valor

        imagens = pergunta.get(
            "imagens",
            []
        )

        if (
            isinstance(imagens, list)
            and indice < len(imagens)
            and imagens[indice]
        ):
            return imagens[indice]

        return None

    def _criar_frame_pergunta(
        self,
        caminho,
        numero,
        pergunta
    ):
        imagem, desenho = self._criar_base()

        self._desenhar_cabecalho(
            desenho,
            numero
        )

        self._desenhar_pergunta_e_alternativas(
            imagem,
            desenho,
            pergunta
        )

        self._desenhar_rodape(
            desenho,
            "ESCOLHA RÁPIDO!"
        )

        imagem.save(caminho)

    def _criar_frame_contagem(
        self,
        caminho,
        numero,
        pergunta,
        contador
    ):
        imagem, desenho = self._criar_base()

        self._desenhar_cabecalho(
            desenho,
            numero
        )

        self._desenhar_pergunta_e_alternativas(
            imagem,
            desenho,
            pergunta
        )

        centro_x = 640
        centro_y = 600
        raio = 52

        desenho.ellipse(
            (
                centro_x - raio,
                centro_y - raio,
                centro_x + raio,
                centro_y + raio
            ),
            fill=(255, 255, 255),
            outline=self.COR_DESTAQUE,
            width=8
        )

        fonte_contador = self._carregar_fonte_negrito(46)
        texto = str(contador)

        caixa = desenho.textbbox(
            (0, 0),
            texto,
            font=fonte_contador
        )

        largura = caixa[2] - caixa[0]
        altura = caixa[3] - caixa[1]

        desenho.text(
            (
                centro_x - largura / 2,
                centro_y - altura / 2 - 5
            ),
            texto,
            font=fonte_contador,
            fill=(67, 43, 120)
        )

        # Barra de tempo simples e clara.
        total_visual = max(int(contador), 1)
        largura_barra = 420
        x1 = centro_x - largura_barra / 2
        x2 = centro_x + largura_barra / 2

        desenho.rounded_rectangle(
            (x1, 655, x2, 671),
            radius=8,
            fill=(75, 66, 110)
        )

        proporcao = min(
            max(total_visual / 10, 0.08),
            1.0
        )

        desenho.rounded_rectangle(
            (
                x1,
                655,
                x1 + largura_barra * proporcao,
                671
            ),
            radius=8,
            fill=self.COR_DESTAQUE
        )

        imagem.save(caminho)

    def _criar_frame_escolha(
        self,
        caminho,
        numero,
        pergunta
    ):
        imagem, desenho = self._criar_base()

        self._desenhar_cabecalho(
            desenho,
            numero
        )

        desenho.rounded_rectangle(
            (120, 195, 1160, 545),
            radius=45,
            fill=(113, 68, 200),
            outline=(255, 255, 255),
            width=5
        )

        fonte_titulo = self._carregar_fonte_negrito(60)
        fonte_subtitulo = self._carregar_fonte_negrito(42)
        fonte_comentario = self._carregar_fonte_negrito(28)

        self._texto_centralizado(
            desenho,
            "TEMPO ESGOTADO!",
            y=270,
            fonte=fonte_titulo,
            cor=self.COR_DESTAQUE
        )

        self._texto_centralizado(
            desenho,
            "QUAL VOCÊ ESCOLHEU?",
            y=370,
            fonte=fonte_subtitulo,
            cor=(255, 255, 255)
        )

        self._texto_centralizado(
            desenho,
            "CONTE NOS COMENTÁRIOS!",
            y=470,
            fonte=fonte_comentario,
            cor=(235, 225, 255)
        )

        self._desenhar_rodape(
            desenho,
            "A ESCOLHA É TODA SUA!"
        )

        imagem.save(caminho)

    def _desenhar_rodape(
        self,
        desenho,
        texto
    ):
        fonte = self._carregar_fonte_negrito(25)

        caixa = desenho.textbbox(
            (0, 0),
            texto,
            font=fonte
        )

        largura = caixa[2] - caixa[0]

        desenho.rounded_rectangle(
            (
                640 - largura / 2 - 28,
                575,
                640 + largura / 2 + 28,
                625
            ),
            radius=18,
            fill=(255, 255, 255)
        )

        desenho.text(
            (
                640 - largura / 2,
                584
            ),
            texto,
            font=fonte,
            fill=(74, 45, 145)
        )

    def _texto_centralizado(
        self,
        desenho,
        texto,
        y,
        fonte,
        cor
    ):
        caixa = desenho.textbbox(
            (0, 0),
            texto,
            font=fonte
        )

        largura = caixa[2] - caixa[0]

        desenho.text(
            (
                (self.largura - largura) / 2,
                y
            ),
            texto,
            font=fonte,
            fill=cor
        )

    def _carregar_fonte_negrito(
        self,
        tamanho
    ):
        fontes = [
            Path("C:/Windows/Fonts/arialbd.ttf"),
            Path("C:/Windows/Fonts/calibrib.ttf"),
            Path("C:/Windows/Fonts/seguisb.ttf"),
        ]

        for caminho in fontes:
            if caminho.exists():
                return ImageFont.truetype(
                    str(caminho),
                    tamanho
                )

        return self._carregar_fonte(
            tamanho
        )
