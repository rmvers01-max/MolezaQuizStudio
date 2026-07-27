from pathlib import Path
from typing import Optional, Union

from PIL import (
    Image,
    ImageColor,
    ImageDraw,
    ImageFilter,
    ImageFont,
    ImageOps,
    UnidentifiedImageError
)

from core.thumbnail_elements import (
    ImageElement,
    ShapeElement,
    TextElement,
    ThumbnailDocument,
    ThumbnailElement
)


class ThumbnailDocumentRenderer:
    """
    Renderiza um ThumbnailDocument como imagem final.

    O renderizador trabalha na resolução real do documento,
    normalmente 1280 × 720, sem depender da resolução do canvas
    mostrado na interface.
    """

    def __init__(self):
        self.pasta_fontes_windows = Path(
            "C:/Windows/Fonts"
        )

    def renderizar(
        self,
        documento: ThumbnailDocument
    ) -> Image.Image:
        largura = max(
            int(documento.largura),
            1
        )

        altura = max(
            int(documento.altura),
            1
        )

        imagem_final = Image.new(
            "RGBA",
            (
                largura,
                altura
            ),
            self._normalizar_cor(
                documento.cor_fundo
            )
        )

        elementos = sorted(
            documento.elementos,
            key=lambda elemento: elemento.camada
        )

        for elemento in elementos:
            if not elemento.visivel:
                continue

            camada = self._renderizar_elemento(
                elemento=elemento,
                tamanho_documento=(
                    largura,
                    altura
                )
            )

            if camada is None:
                continue

            imagem_final.alpha_composite(
                camada
            )

        return imagem_final

    def salvar(
        self,
        documento: ThumbnailDocument,
        caminho_saida: Union[str, Path],
        qualidade_jpeg: int = 95
    ) -> Path:
        caminho_saida = Path(
            caminho_saida
        )

        caminho_saida.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        imagem = self.renderizar(
            documento
        )

        extensao = caminho_saida.suffix.lower()

        if extensao in {
            ".jpg",
            ".jpeg"
        }:
            imagem.convert(
                "RGB"
            ).save(
                caminho_saida,
                format="JPEG",
                quality=max(
                    min(
                        int(qualidade_jpeg),
                        100
                    ),
                    1
                ),
                optimize=True
            )

        else:
            imagem.save(
                caminho_saida,
                format="PNG",
                optimize=True
            )

        return caminho_saida

    def _renderizar_elemento(
        self,
        elemento: ThumbnailElement,
        tamanho_documento: tuple[int, int]
    ) -> Optional[Image.Image]:
        if isinstance(
            elemento,
            TextElement
        ):
            return self._renderizar_texto(
                elemento,
                tamanho_documento
            )

        if isinstance(
            elemento,
            ImageElement
        ):
            return self._renderizar_imagem(
                elemento,
                tamanho_documento
            )

        if isinstance(
            elemento,
            ShapeElement
        ):
            return self._renderizar_forma(
                elemento,
                tamanho_documento
            )

        return None

    def _renderizar_forma(
        self,
        elemento: ShapeElement,
        tamanho_documento: tuple[int, int]
    ) -> Image.Image:
        camada = self._criar_camada_transparente(
            tamanho_documento
        )

        largura = max(
            int(round(elemento.largura)),
            1
        )

        altura = max(
            int(round(elemento.altura)),
            1
        )

        elemento_local = Image.new(
            "RGBA",
            (
                largura,
                altura
            ),
            (
                0,
                0,
                0,
                0
            )
        )

        desenho = ImageDraw.Draw(
            elemento_local
        )

        cor = self._normalizar_cor(
            elemento.cor,
            elemento.opacidade
        )

        cor_contorno = self._normalizar_cor(
            elemento.cor_contorno,
            elemento.opacidade
        )

        largura_contorno = max(
            int(elemento.largura_contorno),
            0
        )

        caixa = (
            0,
            0,
            largura - 1,
            altura - 1
        )

        if elemento.formato == "circulo":
            desenho.ellipse(
                caixa,
                fill=cor,
                outline=(
                    cor_contorno
                    if largura_contorno > 0
                    else None
                ),
                width=largura_contorno
            )

        else:
            raio = max(
                min(
                    int(elemento.raio),
                    largura // 2,
                    altura // 2
                ),
                0
            )

            if raio > 0:
                desenho.rounded_rectangle(
                    caixa,
                    radius=raio,
                    fill=cor,
                    outline=(
                        cor_contorno
                        if largura_contorno > 0
                        else None
                    ),
                    width=largura_contorno
                )

            else:
                desenho.rectangle(
                    caixa,
                    fill=cor,
                    outline=(
                        cor_contorno
                        if largura_contorno > 0
                        else None
                    ),
                    width=largura_contorno
                )

        elemento_local = self._aplicar_rotacao(
            elemento_local,
            elemento.rotacao
        )

        self._compor_elemento_centralizado(
            camada=camada,
            elemento=elemento_local,
            x=elemento.x,
            y=elemento.y,
            largura_original=elemento.largura,
            altura_original=elemento.altura
        )

        return camada

    def _renderizar_texto(
        self,
        elemento: TextElement,
        tamanho_documento: tuple[int, int]
    ) -> Image.Image:
        camada = self._criar_camada_transparente(
            tamanho_documento
        )

        largura = max(
            int(round(elemento.largura)),
            1
        )

        altura = max(
            int(round(elemento.altura)),
            1
        )

        margem = max(
            int(elemento.largura_contorno),
            0
        ) + 20

        area_texto = Image.new(
            "RGBA",
            (
                largura + margem * 2,
                altura + margem * 2
            ),
            (
                0,
                0,
                0,
                0
            )
        )

        desenho = ImageDraw.Draw(
            area_texto
        )

        fonte = self._carregar_fonte(
            nome_fonte=elemento.fonte,
            tamanho=elemento.tamanho_fonte,
            negrito=elemento.negrito
        )

        texto = str(
            elemento.texto
        )

        cor = self._normalizar_cor(
            elemento.cor,
            elemento.opacidade
        )

        cor_contorno = self._normalizar_cor(
            elemento.cor_contorno,
            elemento.opacidade
        )

        largura_contorno = max(
            int(elemento.largura_contorno),
            0
        )

        linhas = self._quebrar_texto(
            desenho=desenho,
            texto=texto,
            fonte=fonte,
            largura_maxima=largura,
            largura_contorno=largura_contorno
        )

        alturas = []
        larguras = []

        for linha in linhas:
            caixa = desenho.textbbox(
                (
                    0,
                    0
                ),
                linha,
                font=fonte,
                stroke_width=largura_contorno
            )

            larguras.append(
                caixa[2] - caixa[0]
            )

            alturas.append(
                caixa[3] - caixa[1]
            )

        espacamento = max(
            int(elemento.tamanho_fonte * 0.12),
            4
        )

        altura_total = (
            sum(alturas)
            + max(
                len(linhas) - 1,
                0
            )
            * espacamento
        )

        y_atual = (
            margem
            + max(
                (
                    altura
                    - altura_total
                )
                // 2,
                0
            )
        )

        for indice, linha in enumerate(
            linhas
        ):
            largura_linha = larguras[indice]

            if elemento.alinhamento == "esquerda":
                x_texto = margem

            elif elemento.alinhamento == "direita":
                x_texto = (
                    margem
                    + largura
                    - largura_linha
                )

            else:
                x_texto = (
                    margem
                    + (
                        largura
                        - largura_linha
                    )
                    // 2
                )

            if elemento.sombra:
                desenho.text(
                    (
                        x_texto
                        + elemento.deslocamento_sombra_x,
                        y_atual
                        + elemento.deslocamento_sombra_y
                    ),
                    linha,
                    font=fonte,
                    fill=self._normalizar_cor(
                        elemento.cor_sombra,
                        elemento.opacidade
                    ),
                    stroke_width=largura_contorno,
                    stroke_fill=self._normalizar_cor(
                        elemento.cor_sombra,
                        elemento.opacidade
                    )
                )

            desenho.text(
                (
                    x_texto,
                    y_atual
                ),
                linha,
                font=fonte,
                fill=cor,
                stroke_width=largura_contorno,
                stroke_fill=(
                    cor_contorno
                    if largura_contorno > 0
                    else None
                )
            )

            y_atual += (
                alturas[indice]
                + espacamento
            )

        area_texto = self._aplicar_rotacao(
            area_texto,
            elemento.rotacao
        )

        self._compor_elemento_centralizado(
            camada=camada,
            elemento=area_texto,
            x=elemento.x - margem,
            y=elemento.y - margem,
            largura_original=elemento.largura + margem * 2,
            altura_original=elemento.altura + margem * 2
        )

        return camada

    def _renderizar_imagem(
        self,
        elemento: ImageElement,
        tamanho_documento: tuple[int, int]
    ) -> Optional[Image.Image]:
        caminho = elemento.obter_caminho()

        if caminho is None:
            return None

        try:
            with Image.open(
                caminho
            ) as imagem_original:
                imagem = imagem_original.convert(
                    "RGBA"
                ).copy()

        except (
            OSError,
            ValueError,
            UnidentifiedImageError
        ):
            return None

        largura = max(
            int(round(elemento.largura)),
            1
        )

        altura = max(
            int(round(elemento.altura)),
            1
        )

        if elemento.preencher_area:
            imagem = ImageOps.fit(
                imagem,
                (
                    largura,
                    altura
                ),
                method=Image.Resampling.LANCZOS,
                centering=(
                    0.5,
                    0.5
                )
            )

        elif elemento.preservar_proporcao:
            imagem.thumbnail(
                (
                    largura,
                    altura
                ),
                Image.Resampling.LANCZOS
            )

        else:
            imagem = imagem.resize(
                (
                    largura,
                    altura
                ),
                Image.Resampling.LANCZOS
            )

        imagem = self._aplicar_opacidade(
            imagem,
            elemento.opacidade
        )

        if elemento.borda:
            imagem = self._adicionar_borda_imagem(
                imagem=imagem,
                cor=elemento.cor_borda,
                largura=elemento.largura_borda,
                raio=elemento.raio_borda
            )

        if elemento.rotacao:
            imagem = self._aplicar_rotacao(
                imagem,
                elemento.rotacao
            )

        camada = self._criar_camada_transparente(
            tamanho_documento
        )

        x = (
            elemento.x
            + (
                elemento.largura
                - imagem.width
            )
            / 2
        )

        y = (
            elemento.y
            + (
                elemento.altura
                - imagem.height
            )
            / 2
        )

        if elemento.sombra:
            self._adicionar_sombra(
                camada=camada,
                imagem=imagem,
                x=x,
                y=y,
                deslocamento=(
                    10,
                    12
                ),
                desfoque=elemento.desfoque_sombra,
                opacidade=elemento.opacidade_sombra
            )

        camada.alpha_composite(
            imagem,
            (
                int(round(x)),
                int(round(y))
            )
        )

        return camada

    def _adicionar_borda_imagem(
        self,
        imagem: Image.Image,
        cor: str,
        largura: int,
        raio: int
    ) -> Image.Image:
        largura = max(
            int(largura),
            0
        )

        if largura == 0:
            return imagem

        nova_largura = (
            imagem.width
            + largura * 2
        )

        nova_altura = (
            imagem.height
            + largura * 2
        )

        resultado = Image.new(
            "RGBA",
            (
                nova_largura,
                nova_altura
            ),
            (
                0,
                0,
                0,
                0
            )
        )

        desenho = ImageDraw.Draw(
            resultado
        )

        cor_borda = self._normalizar_cor(
            cor
        )

        raio = max(
            min(
                int(raio),
                nova_largura // 2,
                nova_altura // 2
            ),
            0
        )

        if raio > 0:
            desenho.rounded_rectangle(
                (
                    0,
                    0,
                    nova_largura - 1,
                    nova_altura - 1
                ),
                radius=raio,
                fill=cor_borda
            )

            mascara = Image.new(
                "L",
                imagem.size,
                0
            )

            desenho_mascara = ImageDraw.Draw(
                mascara
            )

            desenho_mascara.rounded_rectangle(
                (
                    0,
                    0,
                    imagem.width - 1,
                    imagem.height - 1
                ),
                radius=max(
                    raio - largura,
                    0
                ),
                fill=255
            )

            imagem = imagem.copy()
            imagem.putalpha(
                Image.composite(
                    imagem.getchannel("A"),
                    Image.new(
                        "L",
                        imagem.size,
                        0
                    ),
                    mascara
                )
            )

        else:
            desenho.rectangle(
                (
                    0,
                    0,
                    nova_largura - 1,
                    nova_altura - 1
                ),
                fill=cor_borda
            )

        resultado.alpha_composite(
            imagem,
            (
                largura,
                largura
            )
        )

        return resultado

    def _adicionar_sombra(
        self,
        camada: Image.Image,
        imagem: Image.Image,
        x: float,
        y: float,
        deslocamento: tuple[int, int],
        desfoque: int,
        opacidade: int
    ):
        mascara = imagem.getchannel(
            "A"
        )

        sombra_local = Image.new(
            "RGBA",
            imagem.size,
            (
                0,
                0,
                0,
                255
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

        fator_opacidade = (
            max(
                min(
                    int(opacidade),
                    255
                ),
                0
            )
            / 255
        )

        mascara = mascara.point(
            lambda valor: int(
                valor * fator_opacidade
            )
        )

        sombra_local.putalpha(
            mascara
        )

        deslocamento_x, deslocamento_y = deslocamento

        camada.alpha_composite(
            sombra_local,
            (
                int(round(x + deslocamento_x)),
                int(round(y + deslocamento_y))
            )
        )

    def _compor_elemento_centralizado(
        self,
        camada: Image.Image,
        elemento: Image.Image,
        x: float,
        y: float,
        largura_original: float,
        altura_original: float
    ):
        centro_x = (
            x
            + largura_original / 2
        )

        centro_y = (
            y
            + altura_original / 2
        )

        posicao_x = int(
            round(
                centro_x
                - elemento.width / 2
            )
        )

        posicao_y = int(
            round(
                centro_y
                - elemento.height / 2
            )
        )

        camada.alpha_composite(
            elemento,
            (
                posicao_x,
                posicao_y
            )
        )

    def _aplicar_rotacao(
        self,
        imagem: Image.Image,
        angulo: float
    ) -> Image.Image:
        angulo = float(
            angulo
        ) % 360

        if angulo == 0:
            return imagem

        return imagem.rotate(
            -angulo,
            expand=True,
            resample=Image.Resampling.BICUBIC
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

    def _quebrar_texto(
        self,
        desenho: ImageDraw.ImageDraw,
        texto: str,
        fonte,
        largura_maxima: int,
        largura_contorno: int
    ) -> list[str]:
        linhas_finais = []

        blocos = texto.splitlines()

        if not blocos:
            blocos = [
                texto
            ]

        for bloco in blocos:
            palavras = bloco.split()

            if not palavras:
                linhas_finais.append(
                    ""
                )
                continue

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
                    stroke_width=largura_contorno
                )

                largura = (
                    caixa[2]
                    - caixa[0]
                )

                if largura <= largura_maxima:
                    linha_atual = teste

                else:
                    linhas_finais.append(
                        linha_atual
                    )

                    linha_atual = palavra

            linhas_finais.append(
                linha_atual
            )

        return linhas_finais

    def _carregar_fonte(
        self,
        nome_fonte: str,
        tamanho: int,
        negrito: bool
    ):
        tamanho = max(
            int(tamanho),
            1
        )

        candidatos = []

        nome_normalizado = str(
            nome_fonte
        ).strip()

        if nome_normalizado:
            caminho_informado = Path(
                nome_normalizado
            )

            if caminho_informado.exists():
                candidatos.append(
                    caminho_informado
                )

            nome_arquivo = (
                nome_normalizado
                if nome_normalizado.lower().endswith(
                    (
                        ".ttf",
                        ".otf"
                    )
                )
                else f"{nome_normalizado}.ttf"
            )

            candidatos.append(
                self.pasta_fontes_windows
                / nome_arquivo
            )

        nome_fonte_lower = nome_normalizado.lower()

        if negrito:
            if "impact" in nome_fonte_lower:
                nomes_padrao = [
                    "impact.ttf",
                    "arialbd.ttf",
                    "calibrib.ttf",
                    "segoeuib.ttf"
                ]

            else:
                nomes_padrao = [
                    "arialbd.ttf",
                    "calibrib.ttf",
                    "segoeuib.ttf",
                    "impact.ttf"
                ]

        else:
            nomes_padrao = [
                "arial.ttf",
                "calibri.ttf",
                "segoeui.ttf"
            ]

        for nome in nomes_padrao:
            candidatos.append(
                self.pasta_fontes_windows
                / nome
            )

        for caminho in candidatos:
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

    def _normalizar_cor(
        self,
        cor,
        opacidade: Optional[int] = None
    ) -> tuple[int, int, int, int]:
        try:
            if isinstance(
                cor,
                str
            ):
                valores = ImageColor.getcolor(
                    cor,
                    "RGBA"
                )

            elif len(cor) == 3:
                valores = (
                    int(cor[0]),
                    int(cor[1]),
                    int(cor[2]),
                    255
                )

            else:
                valores = (
                    int(cor[0]),
                    int(cor[1]),
                    int(cor[2]),
                    int(cor[3])
                )

        except (
            ValueError,
            TypeError,
            IndexError
        ):
            valores = (
                255,
                255,
                255,
                255
            )

        if opacidade is None:
            return valores

        opacidade = max(
            min(
                int(opacidade),
                255
            ),
            0
        )

        alpha = int(
            valores[3]
            * (
                opacidade
                / 255
            )
        )

        return (
            valores[0],
            valores[1],
            valores[2],
            alpha
        )

    def _criar_camada_transparente(
        self,
        tamanho: tuple[int, int]
    ) -> Image.Image:
        return Image.new(
            "RGBA",
            tamanho,
            (
                0,
                0,
                0,
                0
            )
        )
