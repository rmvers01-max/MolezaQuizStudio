from typing import Callable, Optional

import customtkinter as ctk

from core.thumbnail_elements import ThumbnailDocument, ThumbnailElement

from .canvas_helpers_mixin import CanvasHelpersMixin
from .interaction_mixin import InteractionMixin
from .render_mixin import RenderMixin


class ThumbnailCanvas(
    RenderMixin,
    InteractionMixin,
    CanvasHelpersMixin,
    ctk.CTkFrame,
):
    """Canvas modular do Editor de Thumbnail."""

    LARGURA_DOCUMENTO = 1280
    ALTURA_DOCUMENTO = 720

    TAMANHO_ALCA = 10
    AREA_CLIQUE_ALCA = 14
    TAMANHO_MINIMO_ELEMENTO = 30

    ALCA_SUPERIOR_ESQUERDA = "superior_esquerda"
    ALCA_SUPERIOR_DIREITA = "superior_direita"
    ALCA_INFERIOR_ESQUERDA = "inferior_esquerda"
    ALCA_INFERIOR_DIREITA = "inferior_direita"
    ALCA_MEIO_SUPERIOR = "meio_superior"
    ALCA_MEIO_INFERIOR = "meio_inferior"
    ALCA_MEIO_ESQUERDA = "meio_esquerda"
    ALCA_MEIO_DIREITA = "meio_direita"
    ALCA_ROTACAO = "rotacao"

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
        ] = None,
        ao_zoom: Optional[Callable[[int], None]] = None
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
        self.ao_zoom = ao_zoom

        self.documento = ThumbnailDocument(
            largura=self.LARGURA_DOCUMENTO,
            altura=self.ALTURA_DOCUMENTO
        )

        self.elemento_selecionado_id = None

        self.arrastando = False
        self.redimensionando = False
        self.girando = False

        self.alca_ativa = None

        self.ultimo_x_documento = 0.0
        self.ultimo_y_documento = 0.0

        self.inicio_x_documento = 0.0
        self.inicio_y_documento = 0.0

        self.geometria_inicial = None
        self.angulo_mouse_inicial = 0.0
        self.rotacao_inicial = 0.0

        self.escala_atual = 1.0
        self.escala_ajuste = 1.0
        self.zoom_percentual = 100
        self.origem_x = 0.0
        self.origem_y = 0.0

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
            "<Motion>",
            self._ao_mover_mouse
        )

        self.canvas.bind(
            "<Leave>",
            self._ao_sair_canvas
        )

        self.canvas.bind(
            "<Configure>",
            self._ao_redimensionar_canvas
        )

        self.canvas.bind(
            "<Control-MouseWheel>",
            self._ao_zoom_roda
        )


    def definir_zoom(self, percentual: int):
        self.zoom_percentual = max(25, min(int(percentual), 400))
        self.renderizar()
        self._notificar_zoom()

    def obter_zoom(self) -> int:
        return int(self.zoom_percentual)

    def aumentar_zoom(self):
        self.definir_zoom(self.zoom_percentual + 25)

    def diminuir_zoom(self):
        self.definir_zoom(self.zoom_percentual - 25)

    def ajustar_zoom_tela(self):
        self.zoom_percentual = 100
        self.renderizar()
        self._notificar_zoom()

    def _ao_zoom_roda(self, evento):
        if evento.delta > 0:
            self.aumentar_zoom()
        elif evento.delta < 0:
            self.diminuir_zoom()
        return "break"

    def _notificar_zoom(self):
        if callable(self.ao_zoom):
            self.ao_zoom(self.obter_zoom())

    def definir_documento(
        self,
        documento: ThumbnailDocument
    ):
        self.documento = documento

        self.elemento_selecionado_id = None

        self.arrastando = False
        self.redimensionando = False
        self.girando = False
        self.alca_ativa = None
        self.geometria_inicial = None

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
        self.redimensionando = False
        self.girando = False
        self.alca_ativa = None
        self.geometria_inicial = None

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

        self.arrastando = False
        self.redimensionando = False
        self.girando = False
        self.alca_ativa = None
        self.geometria_inicial = None

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
