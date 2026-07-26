from pathlib import Path
from typing import Union

from core.branding_manager import BrandingManager
from core.thumbnail_composer import ThumbnailComposer


class ChoiceThumbnailGenerator:
    """
    Gerador do modelo de thumbnail:

        O QUE VOCÊ PREFERE?

        [ IMAGEM A ]   OU   [ IMAGEM B ]

        TEXTO INFERIOR

    O modelo utiliza automaticamente o mascote e o logotipo
    configurados em assets/branding.
    """

    LARGURA = 1280
    ALTURA = 720

    def __init__(self):
        self.branding_manager = BrandingManager()

    def gerar(
        self,
        pasta_projeto: Union[str, Path],
        imagem_esquerda: Union[str, Path],
        imagem_direita: Union[str, Path],
        titulo_superior: str = "O QUE VOCÊ PREFERE?",
        texto_inferior: str = "",
        nome_arquivo: str = "thumbnail_escolhas.png",
        texto_central: str = "OU"
    ) -> Path:
        pasta_projeto = Path(
            pasta_projeto
        )

        pasta_projeto.mkdir(
            parents=True,
            exist_ok=True
        )

        caminho_esquerda = Path(
            imagem_esquerda
        )

        caminho_direita = Path(
            imagem_direita
        )

        if not caminho_esquerda.exists():
            raise FileNotFoundError(
                "A imagem da opção esquerda não foi encontrada:\n"
                f"{caminho_esquerda}"
            )

        if not caminho_direita.exists():
            raise FileNotFoundError(
                "A imagem da opção direita não foi encontrada:\n"
                f"{caminho_direita}"
            )

        compositor = ThumbnailComposer(
            largura=self.LARGURA,
            altura=self.ALTURA,
            cor_fundo="#7D2FC5"
        )

        self._desenhar_fundo(
            compositor
        )

        self._adicionar_titulo_superior(
            compositor=compositor,
            titulo=titulo_superior
        )

        self._adicionar_opcoes(
            compositor=compositor,
            imagem_esquerda=caminho_esquerda,
            imagem_direita=caminho_direita
        )

        self._adicionar_texto_central(
            compositor=compositor,
            texto=texto_central
        )

        self._adicionar_faixa_inferior(
            compositor=compositor,
            texto=texto_inferior
        )

        self._adicionar_logotipo(
            compositor
        )

        self._adicionar_mascote(
            compositor
        )

        caminho_saida = (
            pasta_projeto
            / nome_arquivo
        )

        return compositor.salvar(
            caminho_saida
        )

    def _desenhar_fundo(
        self,
        compositor: ThumbnailComposer
    ):
        compositor.definir_fundo_degrade_vertical(
            cor_inicio="#963EE0",
            cor_fim="#6321A9"
        )

        compositor.adicionar_circulo(
            caixa=(
                -140,
                -180,
                430,
                390
            ),
            cor=(
                255,
                255,
                255,
                18
            )
        )

        compositor.adicionar_circulo(
            caixa=(
                920,
                250,
                1450,
                800
            ),
            cor=(
                255,
                255,
                255,
                15
            )
        )

        compositor.adicionar_linhas_diagonais(
            cor=(
                255,
                255,
                255,
                20
            ),
            espacamento=105,
            largura_linha=5,
            inclinacao=360
        )

        compositor.adicionar_circulo(
            caixa=(
                455,
                175,
                830,
                550
            ),
            cor=(
                255,
                255,
                255,
                12
            )
        )

    def _adicionar_titulo_superior(
        self,
        compositor: ThumbnailComposer,
        titulo: str
    ):
        titulo = (
            str(
                titulo
            ).strip().upper()
            or "O QUE VOCÊ PREFERE?"
        )

        compositor.adicionar_texto(
            texto=titulo,
            caixa=(
                250,
                12,
                1235,
                125
            ),
            tamanho_inicial=68,
            tamanho_minimo=34,
            cor="#FFFFFF",
            negrito=True,
            alinhamento_horizontal="centro",
            alinhamento_vertical="centro",
            maximo_linhas=1,
            contorno="#5B188F",
            largura_contorno=5,
            sombra=True,
            cor_sombra=(
                30,
                0,
                55,
                185
            ),
            deslocamento_sombra=(
                6,
                8
            )
        )

    def _adicionar_opcoes(
        self,
        compositor: ThumbnailComposer,
        imagem_esquerda: Path,
        imagem_direita: Path
    ):
        compositor.adicionar_imagem_em_moldura(
            caminho_imagem=imagem_esquerda,
            caixa=(
                62,
                145,
                580,
                560
            ),
            raio=34,
            cor_moldura="#FFFFFF",
            espessura_moldura=10,
            sombra=True,
            deslocamento_sombra=(
                12,
                16
            ),
            desfoque_sombra=18
        )

        compositor.adicionar_imagem_em_moldura(
            caminho_imagem=imagem_direita,
            caixa=(
                700,
                145,
                1218,
                560
            ),
            raio=34,
            cor_moldura="#FFFFFF",
            espessura_moldura=10,
            sombra=True,
            deslocamento_sombra=(
                12,
                16
            ),
            desfoque_sombra=18
        )

    def _adicionar_texto_central(
        self,
        compositor: ThumbnailComposer,
        texto: str
    ):
        texto = (
            str(
                texto
            ).strip().upper()
            or "OU"
        )

        compositor.adicionar_circulo(
            caixa=(
                570,
                300,
                710,
                440
            ),
            cor="#FF8A1F",
            contorno="#FFFFFF",
            largura_contorno=8
        )

        compositor.adicionar_texto(
            texto=texto,
            caixa=(
                580,
                310,
                700,
                430
            ),
            tamanho_inicial=66,
            tamanho_minimo=38,
            cor="#FFFFFF",
            negrito=True,
            alinhamento_horizontal="centro",
            alinhamento_vertical="centro",
            maximo_linhas=1,
            contorno="#D54B00",
            largura_contorno=4,
            sombra=True,
            cor_sombra=(
                115,
                35,
                0,
                170
            ),
            deslocamento_sombra=(
                4,
                6
            )
        )

    def _adicionar_faixa_inferior(
        self,
        compositor: ThumbnailComposer,
        texto: str
    ):
        texto = str(
            texto
        ).strip().upper()

        if not texto:
            texto = "FAÇA SUA ESCOLHA!"

        compositor.adicionar_retangulo(
            caixa=(
                0,
                580,
                1280,
                720
            ),
            cor="#6C28B2"
        )

        compositor.adicionar_retangulo(
            caixa=(
                0,
                580,
                1280,
                592
            ),
            cor="#B96EFF"
        )

        compositor.adicionar_texto(
            texto=texto,
            caixa=(
                235,
                590,
                1140,
                705
            ),
            tamanho_inicial=68,
            tamanho_minimo=34,
            cor="#FFFFFF",
            negrito=True,
            alinhamento_horizontal="centro",
            alinhamento_vertical="centro",
            maximo_linhas=1,
            contorno="#42106E",
            largura_contorno=5,
            sombra=True,
            cor_sombra=(
                30,
                0,
                50,
                180
            ),
            deslocamento_sombra=(
                5,
                7
            )
        )

    def _adicionar_logotipo(
        self,
        compositor: ThumbnailComposer
    ):
        caminho_logo = (
            self.branding_manager
            .obter_logo()
        )

        if caminho_logo is None:
            return

        compositor.adicionar_imagem(
            caminho_imagem=caminho_logo,
            caixa=(
                15,
                12,
                215,
                112
            ),
            preservar_proporcao=True,
            preencher_caixa=False,
            alinhamento_horizontal="esquerda",
            alinhamento_vertical="topo",
            sombra=True,
            deslocamento_sombra=(
                4,
                5
            ),
            desfoque_sombra=7,
            opacidade_sombra=95
        )

    def _adicionar_mascote(
        self,
        compositor: ThumbnailComposer
    ):
        caminho_mascote = (
            self.branding_manager
            .obter_mascote()
        )

        if caminho_mascote is None:
            return

        compositor.adicionar_imagem(
            caminho_imagem=caminho_mascote,
            caixa=(
                5,
                530,
                225,
                718
            ),
            preservar_proporcao=True,
            preencher_caixa=False,
            alinhamento_horizontal="esquerda",
            alinhamento_vertical="base",
            sombra=True,
            deslocamento_sombra=(
                7,
                9
            ),
            desfoque_sombra=11,
            opacidade_sombra=105
        )
