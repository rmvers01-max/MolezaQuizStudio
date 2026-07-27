from typing import Callable, Optional

import customtkinter as ctk
from PIL import Image, ImageOps, ImageTk, UnidentifiedImageError

from core.thumbnail_elements import (
    ImageElement,
    ShapeElement,
    TextElement,
    ThumbnailDocument,
    ThumbnailElement
)


class ThumbnailCanvas(ctk.CTkFrame):
    """
    Canvas visual para edição de thumbnails.

    Recursos:
    - renderização dos elementos;
    - seleção por clique;
    - movimentação com o mouse;
    - indicação visual da seleção;
    - conversão entre coordenadas do editor e 1280 × 720;
    - cache correto de imagens usando ImageTk.PhotoImage.
    """

    LARGURA_DOCUMENTO = 1280
    ALTURA_DOCUMENTO = 720

    def __init__(
        self,
        master,
        largura_preview: int = 800,
        altura_preview: int = 450,
        ao_selecionar: Optional[
            Callable[[Optional[ThumbnailElement]], None]
        ] = None,
        ao_alterar: Optional[
            Callable[[ThumbnailDocument], None]
        ] = None
    ):
        super().__init__(
            master,
            fg_color="transparent"
        )

        self.largura_preview = max(
            int(largura_preview),
            1
        )

        self.altura_preview = max(
            int(altura_preview),
            1
        )

        self.ao_selecionar = ao_selecionar
        self.ao_alterar = ao_alterar

        self.documento = ThumbnailDocument(
            largura=self.LARGURA_DOCUMENTO,
            altura=self.ALTURA_DOCUMENTO
        )

        self.elemento_selecionado_id = None

        self.arrastando = False
        self.ultimo_x_documento = 0.0
        self.ultimo_y_documento = 0.0

        self.escala_atual = 1.0
        self.origem_x = 0.0
        self.origem_y = 0.0

        # Guarda referências de ImageTk.PhotoImage.
        # Sem essas referências, o Tkinter pode remover as imagens.
        self.imagens_cache = {}

        self._renderizacao_agendada = None

        self._criar_interface()

        self.after_idle(
            self.renderizar
        )

    def _criar_interface(self):
        self.grid_columnconfigure(
            0,
            weight=1
        )

        self.grid_rowconfigure(
            0,
            weight=1
        )

        self.canvas = ctk.CTkCanvas(
            self,
            width=self.largura_preview,
            height=self.altura_preview,
            highlightthickness=1,
            highlightbackground="#4A4A4A",
            background="#101820",
            cursor="arrow"
        )

        self.canvas.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.canvas.bind(
            "<Button-1>",
            self._ao_clicar
        )

        self.canvas.bind(
            "<B1-Motion>",
            self._ao_arrastar
        )

        self.canvas.bind(
            "<ButtonRelease-1>",
            self._ao_soltar
        )

        self.canvas.bind(
            "<Configure>",
            self._ao_redimensionar_canvas
        )

    # =========================================================
    # DOCUMENTO E ELEMENTOS
    # =========================================================

    def definir_documento(
        self,
        documento: ThumbnailDocument
    ):
        self.documento = documento

        self.elemento_selecionado_id = None
        self.arrastando = False

        self.imagens_cache.clear()

        self.renderizar()

        self._notificar_selecao(
            None
        )

    def obter_documento(
        self
    ) -> ThumbnailDocument:
        return self.documento

    def adicionar_elemento(
        self,
        elemento: ThumbnailElement
    ):
        self.documento.adicionar_elemento(
            elemento
        )

        self.elemento_selecionado_id = elemento.id

        self.renderizar()

        self._notificar_selecao(
            elemento
        )

        self._notificar_alteracao()

    def remover_elemento_selecionado(
        self
    ) -> bool:
        if self.elemento_selecionado_id is None:
            return False

        removido = self.documento.remover_elemento(
            self.elemento_selecionado_id
        )

        if not removido:
            return False

        self.elemento_selecionado_id = None
        self.arrastando = False

        self.renderizar()

        self._notificar_selecao(
            None
        )

        self._notificar_alteracao()

        return True

    def selecionar_elemento(
        self,
        elemento_id: Optional[str]
    ):
        self.elemento_selecionado_id = elemento_id

        elemento = None

        if elemento_id:
            elemento = self.documento.obter_elemento(
                elemento_id
            )

        self.renderizar()

        self._notificar_selecao(
            elemento
        )

    def obter_elemento_selecionado(
        self
    ) -> Optional[ThumbnailElement]:
        if not self.elemento_selecionado_id:
            return None

        return self.documento.obter_elemento(
            self.elemento_selecionado_id
        )

    def trazer_selecionado_para_frente(
        self
    ):
        if not self.elemento_selecionado_id:
            return

        self.documento.trazer_para_frente(
            self.elemento_selecionado_id
        )

        self.renderizar()
        self._notificar_alteracao()

    def enviar_selecionado_para_tras(
        self
    ):
        if not self.elemento_selecionado_id:
            return

        self.documento.enviar_para_tras(
            self.elemento_selecionado_id
        )

        self.renderizar()
        self._notificar_alteracao()

    # =========================================================
    # RENDERIZAÇÃO
    # =========================================================

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

        escala = min(
            largura_canvas / largura_documento,
            altura_canvas / altura_documento
        )

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

            # O Canvas do Tkinter exige ImageTk.PhotoImage.
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

        tamanho_alca = 8

        pontos = [
            (
                x1,
                y1
            ),
            (
                x2,
                y1
            ),
            (
                x1,
                y2
            ),
            (
                x2,
                y2
            )
        ]

        for ponto_x, ponto_y in pontos:
            self.canvas.create_rectangle(
                ponto_x - tamanho_alca / 2,
                ponto_y - tamanho_alca / 2,
                ponto_x + tamanho_alca / 2,
                ponto_y + tamanho_alca / 2,
                fill="#FFFFFF",
                outline="#36A9FF",
                width=2,
                tags=("selecao",)
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

    # =========================================================
    # MOUSE
    # =========================================================

    def _ao_clicar(
        self,
        evento
    ):
        documento_x, documento_y = (
            self._canvas_para_documento(
                evento.x,
                evento.y
            )
        )

        if not self._ponto_dentro_documento(
            documento_x,
            documento_y
        ):
            self.selecionar_elemento(
                None
            )

            self.arrastando = False
            return

        elemento = (
            self.documento
            .obter_elemento_no_ponto(
                documento_x,
                documento_y
            )
        )

        if elemento is None:
            self.selecionar_elemento(
                None
            )

            self.arrastando = False
            return

        self.selecionar_elemento(
            elemento.id
        )

        if elemento.bloqueado:
            self.arrastando = False
            return

        self.arrastando = True

        self.ultimo_x_documento = documento_x
        self.ultimo_y_documento = documento_y

    def _ao_arrastar(
        self,
        evento
    ):
        if not self.arrastando:
            return

        elemento = (
            self.obter_elemento_selecionado()
        )

        if elemento is None or elemento.bloqueado:
            self.arrastando = False
            return

        documento_x, documento_y = (
            self._canvas_para_documento(
                evento.x,
                evento.y
            )
        )

        delta_x = (
            documento_x
            - self.ultimo_x_documento
        )

        delta_y = (
            documento_y
            - self.ultimo_y_documento
        )

        elemento.deslocar(
            delta_x,
            delta_y
        )

        self._limitar_elemento_ao_documento(
            elemento
        )

        self.ultimo_x_documento = documento_x
        self.ultimo_y_documento = documento_y

        self.renderizar()

    def _ao_soltar(
        self,
        evento
    ):
        if self.arrastando:
            self._notificar_alteracao()

        self.arrastando = False

    def _ao_redimensionar_canvas(
        self,
        evento
    ):
        if self._renderizacao_agendada is not None:
            try:
                self.after_cancel(
                    self._renderizacao_agendada
                )

            except ValueError:
                pass

        self._renderizacao_agendada = self.after(
            40,
            self._renderizar_apos_redimensionamento
        )

    def _renderizar_apos_redimensionamento(
        self
    ):
        self._renderizacao_agendada = None
        self.renderizar()

    # =========================================================
    # CONVERSÕES E LIMITES
    # =========================================================

    def _limitar_elemento_ao_documento(
        self,
        elemento: ThumbnailElement
    ):
        largura_maxima = max(
            self.documento.largura
            - elemento.largura,
            0
        )

        altura_maxima = max(
            self.documento.altura
            - elemento.altura,
            0
        )

        elemento.x = max(
            min(
                elemento.x,
                largura_maxima
            ),
            0
        )

        elemento.y = max(
            min(
                elemento.y,
                altura_maxima
            ),
            0
        )

    def _documento_para_canvas(
        self,
        x: float,
        y: float
    ) -> tuple[float, float]:
        return (
            self.origem_x
            + x
            * self.escala_atual,
            self.origem_y
            + y
            * self.escala_atual
        )

    def _canvas_para_documento(
        self,
        x: float,
        y: float
    ) -> tuple[float, float]:
        escala = max(
            self.escala_atual,
            0.0001
        )

        return (
            (
                x
                - self.origem_x
            )
            / escala,
            (
                y
                - self.origem_y
            )
            / escala
        )

    def _ponto_dentro_documento(
        self,
        x,
        y
    ):
        return (
            0 <= x <= self.documento.largura
            and 0 <= y <= self.documento.altura
        )

    # =========================================================
    # NOTIFICAÇÕES
    # =========================================================

    def _notificar_selecao(
        self,
        elemento: Optional[ThumbnailElement]
    ):
        if callable(
            self.ao_selecionar
        ):
            self.ao_selecionar(
                elemento
            )

    def _notificar_alteracao(
        self
    ):
        if callable(
            self.ao_alterar
        ):
            self.ao_alterar(
                self.documento
            )
