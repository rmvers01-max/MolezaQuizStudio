from typing import Optional

from PIL import Image, ImageOps, ImageTk, UnidentifiedImageError

from core.thumbnail_elements import (
    ImageElement,
    ShapeElement,
    TextElement,
    ThumbnailDocument,
    ThumbnailElement,
)


class InteractionMixin:
    def _ao_clicar(
        self,
        evento
    ):
        elemento_selecionado = (
            self.obter_elemento_selecionado()
        )

        if (
            elemento_selecionado is not None
            and not elemento_selecionado.bloqueado
        ):
            alca = self._obter_alca_no_ponto_canvas(
                evento.x,
                evento.y,
                elemento_selecionado
            )

            if alca is not None:
                documento_x, documento_y = (
                    self._canvas_para_documento(
                        evento.x,
                        evento.y
                    )
                )

                self.redimensionando = True
                self.arrastando = False

                self.alca_ativa = alca

                self.inicio_x_documento = documento_x
                self.inicio_y_documento = documento_y

                self.geometria_inicial = {
                    "x": elemento_selecionado.x,
                    "y": elemento_selecionado.y,
                    "largura": elemento_selecionado.largura,
                    "altura": elemento_selecionado.altura
                }

                return

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

            return

        self.selecionar_elemento(
            elemento.id
        )

        if elemento.bloqueado:
            return

        self.arrastando = True
        self.redimensionando = False

        self.ultimo_x_documento = documento_x
        self.ultimo_y_documento = documento_y

    def _ao_arrastar(
        self,
        evento
    ):
        elemento = (
            self.obter_elemento_selecionado()
        )

        if elemento is None or elemento.bloqueado:
            self.arrastando = False
            self.redimensionando = False
            return

        documento_x, documento_y = (
            self._canvas_para_documento(
                evento.x,
                evento.y
            )
        )

        if self.redimensionando:
            self._redimensionar_elemento_com_mouse(
                elemento=elemento,
                documento_x=documento_x,
                documento_y=documento_y
            )

            self.renderizar()
            return

        if not self.arrastando:
            return

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
        houve_alteracao = (
            self.arrastando
            or self.redimensionando
        )

        self.arrastando = False
        self.redimensionando = False

        self.alca_ativa = None
        self.geometria_inicial = None

        if houve_alteracao:
            self._notificar_alteracao()

        self._atualizar_cursor(
            evento.x,
            evento.y
        )

    def _ao_mover_mouse(
        self,
        evento
    ):
        if self.arrastando:
            self.canvas.configure(
                cursor="fleur"
            )
            return

        if self.redimensionando:
            self.canvas.configure(
                cursor="sizing"
            )
            return

        self._atualizar_cursor(
            evento.x,
            evento.y
        )

    def _ao_sair_canvas(
        self,
        evento
    ):
        if not self.arrastando and not self.redimensionando:
            self.canvas.configure(
                cursor="arrow"
            )

    def _atualizar_cursor(
        self,
        x,
        y
    ):
        elemento = (
            self.obter_elemento_selecionado()
        )

        if (
            elemento is not None
            and not elemento.bloqueado
        ):
            alca = self._obter_alca_no_ponto_canvas(
                x,
                y,
                elemento
            )

            if alca is not None:
                self.canvas.configure(
                    cursor="sizing"
                )
                return

        documento_x, documento_y = (
            self._canvas_para_documento(
                x,
                y
            )
        )

        elemento_no_ponto = (
            self.documento
            .obter_elemento_no_ponto(
                documento_x,
                documento_y
            )
        )

        if (
            elemento_no_ponto is not None
            and not elemento_no_ponto.bloqueado
        ):
            self.canvas.configure(
                cursor="fleur"
            )
        else:
            self.canvas.configure(
                cursor="arrow"
            )

    def _redimensionar_elemento_com_mouse(
        self,
        elemento: ThumbnailElement,
        documento_x: float,
        documento_y: float
    ):
        if (
            self.geometria_inicial is None
            or self.alca_ativa is None
        ):
            return

        inicial_x = self.geometria_inicial["x"]
        inicial_y = self.geometria_inicial["y"]

        inicial_largura = (
            self.geometria_inicial["largura"]
        )

        inicial_altura = (
            self.geometria_inicial["altura"]
        )

        direita_inicial = (
            inicial_x
            + inicial_largura
        )

        base_inicial = (
            inicial_y
            + inicial_altura
        )

        novo_x = inicial_x
        novo_y = inicial_y
        nova_largura = inicial_largura
        nova_altura = inicial_altura

        if self.alca_ativa == self.ALCA_SUPERIOR_ESQUERDA:
            novo_x = documento_x
            novo_y = documento_y

            nova_largura = (
                direita_inicial
                - novo_x
            )

            nova_altura = (
                base_inicial
                - novo_y
            )

        elif self.alca_ativa == self.ALCA_SUPERIOR_DIREITA:
            novo_y = documento_y

            nova_largura = (
                documento_x
                - inicial_x
            )

            nova_altura = (
                base_inicial
                - novo_y
            )

        elif self.alca_ativa == self.ALCA_INFERIOR_ESQUERDA:
            novo_x = documento_x

            nova_largura = (
                direita_inicial
                - novo_x
            )

            nova_altura = (
                documento_y
                - inicial_y
            )

        elif self.alca_ativa == self.ALCA_INFERIOR_DIREITA:
            nova_largura = (
                documento_x
                - inicial_x
            )

            nova_altura = (
                documento_y
                - inicial_y
            )

        nova_largura = max(
            nova_largura,
            self.TAMANHO_MINIMO_ELEMENTO
        )

        nova_altura = max(
            nova_altura,
            self.TAMANHO_MINIMO_ELEMENTO
        )

        preservar_proporcao = (
            isinstance(
                elemento,
                ImageElement
            )
            and elemento.preservar_proporcao
            and inicial_altura > 0
        )

        if preservar_proporcao:
            proporcao = (
                inicial_largura
                / inicial_altura
            )

            delta_largura = abs(
                nova_largura
                - inicial_largura
            )

            delta_altura = abs(
                nova_altura
                - inicial_altura
            )

            if delta_largura >= delta_altura:
                nova_altura = (
                    nova_largura
                    / proporcao
                )
            else:
                nova_largura = (
                    nova_altura
                    * proporcao
                )

            if self.alca_ativa in {
                self.ALCA_SUPERIOR_ESQUERDA,
                self.ALCA_INFERIOR_ESQUERDA
            }:
                novo_x = (
                    direita_inicial
                    - nova_largura
                )

            if self.alca_ativa in {
                self.ALCA_SUPERIOR_ESQUERDA,
                self.ALCA_SUPERIOR_DIREITA
            }:
                novo_y = (
                    base_inicial
                    - nova_altura
                )

        novo_x, novo_y, nova_largura, nova_altura = (
            self._limitar_redimensionamento(
                x=novo_x,
                y=novo_y,
                largura=nova_largura,
                altura=nova_altura,
                alca=self.alca_ativa,
                direita_inicial=direita_inicial,
                base_inicial=base_inicial
            )
        )

        elemento.x = novo_x
        elemento.y = novo_y

        elemento.largura = max(
            nova_largura,
            self.TAMANHO_MINIMO_ELEMENTO
        )

        elemento.altura = max(
            nova_altura,
            self.TAMANHO_MINIMO_ELEMENTO
        )

    def _limitar_redimensionamento(
        self,
        x,
        y,
        largura,
        altura,
        alca,
        direita_inicial,
        base_inicial
    ):
        largura_documento = (
            self.documento.largura
        )

        altura_documento = (
            self.documento.altura
        )

        if x < 0:
            x = 0

            if alca in {
                self.ALCA_SUPERIOR_ESQUERDA,
                self.ALCA_INFERIOR_ESQUERDA
            }:
                largura = direita_inicial

        if y < 0:
            y = 0

            if alca in {
                self.ALCA_SUPERIOR_ESQUERDA,
                self.ALCA_SUPERIOR_DIREITA
            }:
                altura = base_inicial

        if x + largura > largura_documento:
            largura = max(
                largura_documento - x,
                self.TAMANHO_MINIMO_ELEMENTO
            )

        if y + altura > altura_documento:
            altura = max(
                altura_documento - y,
                self.TAMANHO_MINIMO_ELEMENTO
            )

        largura = max(
            largura,
            self.TAMANHO_MINIMO_ELEMENTO
        )

        altura = max(
            altura,
            self.TAMANHO_MINIMO_ELEMENTO
        )

        return (
            x,
            y,
            largura,
            altura
        )

    def _obter_pontos_alcas_canvas(
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

        return {
            self.ALCA_SUPERIOR_ESQUERDA: (
                x1,
                y1
            ),
            self.ALCA_SUPERIOR_DIREITA: (
                x2,
                y1
            ),
            self.ALCA_INFERIOR_ESQUERDA: (
                x1,
                y2
            ),
            self.ALCA_INFERIOR_DIREITA: (
                x2,
                y2
            )
        }

    def _obter_alca_no_ponto_canvas(
        self,
        x,
        y,
        elemento
    ):
        pontos = self._obter_pontos_alcas_canvas(
            elemento
        )

        area = self.AREA_CLIQUE_ALCA

        for alca, (
            ponto_x,
            ponto_y
        ) in pontos.items():
            if (
                abs(x - ponto_x) <= area
                and abs(y - ponto_y) <= area
            ):
                return alca

        return None
