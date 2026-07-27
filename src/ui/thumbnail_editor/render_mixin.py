from typing import Optional

from PIL import Image, ImageOps, ImageTk, UnidentifiedImageError

from core.thumbnail_elements import (
    ImageElement,
    ShapeElement,
    TextElement,
    ThumbnailDocument,
    ThumbnailElement,
)


class RenderMixin:
    def renderizar(self):
        if not self.winfo_exists():
            return

        self.canvas.delete(
            "all"
        )

        largura_canvas = self.canvas.winfo_width()
        altura_canvas = self.canvas.winfo_height()

        if largura_canvas <= 1:
            largura_canvas = self.largura_preview

        if altura_canvas <= 1:
            altura_canvas = self.altura_preview

        largura_documento = max(
            int(self.documento.largura),
            1
        )

        altura_documento = max(
            int(self.documento.altura),
            1
        )

        escala_ajuste = min(
            largura_canvas / largura_documento,
            altura_canvas / altura_documento
        )

        escala_ajuste = max(
            escala_ajuste,
            0.0001
        )

        self.escala_ajuste = escala_ajuste

        escala = escala_ajuste * (self.zoom_percentual / 100)

        escala = max(
            escala,
            0.0001
        )

        largura_render = (
            largura_documento
            * escala
        )

        altura_render = (
            altura_documento
            * escala
        )

        origem_x = (
            largura_canvas
            - largura_render
        ) / 2

        origem_y = (
            altura_canvas
            - altura_render
        ) / 2

        self.escala_atual = escala
        self.origem_x = origem_x
        self.origem_y = origem_y

        self.canvas.create_rectangle(
            origem_x,
            origem_y,
            origem_x + largura_render,
            origem_y + altura_render,
            fill=self.documento.cor_fundo,
            outline="#555555",
            width=1,
            tags=("area_documento",)
        )

        elementos = sorted(
            self.documento.elementos,
            key=lambda item: item.camada
        )

        for elemento in elementos:
            if not elemento.visivel:
                continue

            try:
                self._renderizar_elemento(
                    elemento
                )

            except (
                OSError,
                ValueError,
                TypeError,
                UnidentifiedImageError
            ):
                self._renderizar_erro_elemento(
                    elemento
                )

        elemento_selecionado = (
            self.obter_elemento_selecionado()
        )

        if elemento_selecionado:
            self._renderizar_selecao(
                elemento_selecionado
            )

    def _renderizar_elemento(
        self,
        elemento: ThumbnailElement
    ):
        if isinstance(
            elemento,
            ShapeElement
        ):
            self._renderizar_forma(
                elemento
            )

        elif isinstance(
            elemento,
            TextElement
        ):
            self._renderizar_texto(
                elemento
            )

        elif isinstance(
            elemento,
            ImageElement
        ):
            self._renderizar_imagem(
                elemento
            )

    def _renderizar_forma(
        self,
        elemento: ShapeElement
    ):
        x1, y1 = self._documento_para_canvas(
            elemento.x,
            elemento.y
        )

        x2, y2 = self._documento_para_canvas(
            elemento.x + elemento.largura,
            elemento.y + elemento.altura
        )

        largura_contorno = max(
            int(
                elemento.largura_contorno
                * self.escala_atual
            ),
            0
        )

        if elemento.formato == "circulo":
            self.canvas.create_oval(
                x1,
                y1,
                x2,
                y2,
                fill=elemento.cor,
                outline=(
                    elemento.cor_contorno
                    if largura_contorno > 0
                    else ""
                ),
                width=largura_contorno,
                tags=(
                    "elemento",
                    elemento.id
                )
            )

        else:
            self.canvas.create_rectangle(
                x1,
                y1,
                x2,
                y2,
                fill=elemento.cor,
                outline=(
                    elemento.cor_contorno
                    if largura_contorno > 0
                    else ""
                ),
                width=largura_contorno,
                tags=(
                    "elemento",
                    elemento.id
                )
            )

    def _renderizar_texto(
        self,
        elemento: TextElement
    ):
        x1, y1 = self._documento_para_canvas(
            elemento.x,
            elemento.y
        )

        x2, y2 = self._documento_para_canvas(
            elemento.x + elemento.largura,
            elemento.y + elemento.altura
        )

        tamanho = max(
            int(
                elemento.tamanho_fonte
                * self.escala_atual
            ),
            8
        )

        estilo = (
            "bold"
            if elemento.negrito
            else "normal"
        )

        fonte = (
            elemento.fonte,
            tamanho,
            estilo
        )

        ancora = "center"

        posicao_x = (
            x1 + x2
        ) / 2

        if elemento.alinhamento == "esquerda":
            ancora = "w"
            posicao_x = x1

        elif elemento.alinhamento == "direita":
            ancora = "e"
            posicao_x = x2

        posicao_y = (
            y1 + y2
        ) / 2

        largura_texto = max(
            int(x2 - x1),
            1
        )

        if elemento.sombra:
            self.canvas.create_text(
                posicao_x
                + elemento.deslocamento_sombra_x
                * self.escala_atual,
                posicao_y
                + elemento.deslocamento_sombra_y
                * self.escala_atual,
                text=elemento.texto,
                fill=elemento.cor_sombra,
                font=fonte,
                anchor=ancora,
                width=largura_texto,
                tags=(
                    "elemento",
                    elemento.id
                )
            )

        self.canvas.create_text(
            posicao_x,
            posicao_y,
            text=elemento.texto,
            fill=elemento.cor,
            font=fonte,
            anchor=ancora,
            width=largura_texto,
            tags=(
                "elemento",
                elemento.id
            )
        )

    def _renderizar_imagem(
        self,
        elemento: ImageElement
    ):
        caminho = elemento.obter_caminho()

        x1, y1 = self._documento_para_canvas(
            elemento.x,
            elemento.y
        )

        x2, y2 = self._documento_para_canvas(
            elemento.x + elemento.largura,
            elemento.y + elemento.altura
        )

        largura_area = max(
            int(round(x2 - x1)),
            1
        )

        altura_area = max(
            int(round(y2 - y1)),
            1
        )

        if caminho is None:
            self._renderizar_placeholder_imagem(
                elemento=elemento,
                x1=x1,
                y1=y1,
                x2=x2,
                y2=y2,
                texto="Imagem não encontrada"
            )

            return

        try:
            data_modificacao = caminho.stat().st_mtime_ns

        except OSError:
            data_modificacao = 0

        chave_cache = (
            elemento.id,
            str(caminho.resolve()),
            data_modificacao,
            largura_area,
            altura_area,
            bool(elemento.preencher_area),
            bool(elemento.preservar_proporcao),
            int(elemento.opacidade)
        )

        imagem_tk = self.imagens_cache.get(
            chave_cache
        )

        if imagem_tk is None:
            try:
                with Image.open(
                    caminho
                ) as imagem_original:
                    imagem = (
                        imagem_original
                        .convert("RGBA")
                        .copy()
                    )

            except (
                OSError,
                ValueError,
                UnidentifiedImageError
            ):
                self._renderizar_placeholder_imagem(
                    elemento=elemento,
                    x1=x1,
                    y1=y1,
                    x2=x2,
                    y2=y2,
                    texto="Não foi possível abrir a imagem"
                )

                return

            if elemento.preencher_area:
                imagem = ImageOps.fit(
                    imagem,
                    (
                        largura_area,
                        altura_area
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
                        largura_area,
                        altura_area
                    ),
                    Image.Resampling.LANCZOS
                )

            else:
                imagem = imagem.resize(
                    (
                        largura_area,
                        altura_area
                    ),
                    Image.Resampling.LANCZOS
                )

            if imagem.width < 1 or imagem.height < 1:
                return

            if elemento.opacidade < 255:
                opacidade = max(
                    min(
                        int(elemento.opacidade),
                        255
                    ),
                    0
                )

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

            imagem_tk = ImageTk.PhotoImage(
                imagem,
                master=self.canvas
            )

            self.imagens_cache[
                chave_cache
            ] = imagem_tk

            self._limpar_cache_antigo(
                elemento.id,
                chave_cache
            )

        self.canvas.create_image(
            (
                x1 + x2
            ) / 2,
            (
                y1 + y2
            ) / 2,
            image=imagem_tk,
            anchor="center",
            tags=(
                "elemento",
                elemento.id
            )
        )

    def _renderizar_placeholder_imagem(
        self,
        elemento,
        x1,
        y1,
        x2,
        y2,
        texto
    ):
        self.canvas.create_rectangle(
            x1,
            y1,
            x2,
            y2,
            fill="#252B35",
            outline="#777777",
            width=1,
            tags=(
                "elemento",
                elemento.id
            )
        )

        self.canvas.create_text(
            (
                x1 + x2
            ) / 2,
            (
                y1 + y2
            ) / 2,
            text=texto,
            fill="#CCCCCC",
            width=max(
                int(x2 - x1 - 20),
                1
            ),
            justify="center",
            tags=(
                "elemento",
                elemento.id
            )
        )

    def _renderizar_erro_elemento(
        self,
        elemento
    ):
        x1, y1 = self._documento_para_canvas(
            elemento.x,
            elemento.y
        )

        x2, y2 = self._documento_para_canvas(
            elemento.x + elemento.largura,
            elemento.y + elemento.altura
        )

        self.canvas.create_rectangle(
            x1,
            y1,
            x2,
            y2,
            fill="#3B2023",
            outline="#E65353",
            width=2,
            tags=(
                "elemento",
                elemento.id
            )
        )

        self.canvas.create_text(
            (
                x1 + x2
            ) / 2,
            (
                y1 + y2
            ) / 2,
            text="Erro ao renderizar elemento",
            fill="#FFFFFF",
            width=max(
                int(x2 - x1 - 20),
                1
            ),
            tags=(
                "elemento",
                elemento.id
            )
        )

    def _limpar_cache_antigo(
        self,
        elemento_id,
        chave_atual
    ):
        chaves_antigas = [
            chave
            for chave in self.imagens_cache
            if (
                chave[0] == elemento_id
                and chave != chave_atual
            )
        ]

        for chave in chaves_antigas:
            self.imagens_cache.pop(
                chave,
                None
            )

    def _renderizar_selecao(
        self,
        elemento: ThumbnailElement
    ):
        x1, y1 = self._documento_para_canvas(
            elemento.x,
            elemento.y
        )

        x2, y2 = self._documento_para_canvas(
            elemento.x + elemento.largura,
            elemento.y + elemento.altura
        )

        self.canvas.create_rectangle(
            x1,
            y1,
            x2,
            y2,
            outline="#36A9FF",
            width=2,
            dash=(
                6,
                4
            ),
            tags=("selecao",)
        )

        pontos = self._obter_pontos_alcas_canvas(
            elemento
        )

        tamanho = self.TAMANHO_ALCA

        for alca, (
            ponto_x,
            ponto_y
        ) in pontos.items():
            self.canvas.create_rectangle(
                ponto_x - tamanho / 2,
                ponto_y - tamanho / 2,
                ponto_x + tamanho / 2,
                ponto_y + tamanho / 2,
                fill="#FFFFFF",
                outline="#36A9FF",
                width=2,
                tags=(
                    "selecao",
                    f"alca_{alca}"
                )
            )

        if elemento.bloqueado:
            self.canvas.create_text(
                x1 + 8,
                y1 + 8,
                text="🔒",
                anchor="nw",
                fill="#FFFFFF",
                tags=("selecao",)
            )
