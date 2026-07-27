from typing import Optional

from PIL import Image, ImageOps, ImageTk, UnidentifiedImageError

from core.thumbnail_elements import (
    ImageElement,
    ShapeElement,
    TextElement,
    ThumbnailDocument,
    ThumbnailElement,
)


class CanvasHelpersMixin:
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
