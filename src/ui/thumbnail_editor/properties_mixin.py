from copy import deepcopy
from pathlib import Path
from tkinter import colorchooser, filedialog, messagebox
from uuid import uuid4

import customtkinter as ctk

from core.thumbnail_elements import (
    ImageElement,
    ShapeElement,
    TextElement,
    ThumbnailDocument,
)


class PropertiesMixin:
    def _preencher_propriedades(
        self,
        elemento
    ):
        valores = [
            (
                self.campo_nome,
                elemento.nome
            ),
            (
                self.campo_x,
                round(elemento.x, 1)
            ),
            (
                self.campo_y,
                round(elemento.y, 1)
            ),
            (
                self.campo_largura,
                round(elemento.largura, 1)
            ),
            (
                self.campo_altura,
                round(elemento.altura, 1)
            ),
            (
                self.campo_rotacao,
                round(elemento.rotacao, 1)
            ),
            (
                self.campo_opacidade,
                elemento.opacidade
            )
        ]

        for campo, valor in valores:
            self._definir_campo(
                campo,
                valor
            )

        if isinstance(
            elemento,
            TextElement
        ):
            self._definir_campo(
                self.campo_texto,
                elemento.texto
            )

            self._definir_campo(
                self.campo_tamanho_fonte,
                elemento.tamanho_fonte
            )

            self._definir_campo(
                self.campo_cor,
                elemento.cor
            )

            self._definir_campo(
                self.campo_contorno,
                elemento.cor_contorno
            )

            self._definir_campo(
                self.campo_largura_contorno,
                elemento.largura_contorno
            )

            self._definir_estado_visual(
                "normal"
            )

            self._definir_estado_botoes_cor(
                "normal"
            )

        elif isinstance(
            elemento,
            ShapeElement
        ):
            self._definir_campo(
                self.campo_texto,
                ""
            )

            self._definir_campo(
                self.campo_tamanho_fonte,
                ""
            )

            self._definir_campo(
                self.campo_cor,
                elemento.cor
            )

            self._definir_campo(
                self.campo_contorno,
                elemento.cor_contorno
            )

            self._definir_campo(
                self.campo_largura_contorno,
                elemento.largura_contorno
            )

            self.campo_texto.configure(
                state="disabled"
            )

            self.campo_tamanho_fonte.configure(
                state="disabled"
            )

            self._definir_estado_botoes_cor(
                "normal"
            )

        else:
            self._definir_campo(
                self.campo_texto,
                ""
            )

            self._definir_campo(
                self.campo_tamanho_fonte,
                ""
            )

            self._definir_campo(
                self.campo_cor,
                ""
            )

            self._definir_campo(
                self.campo_contorno,
                ""
            )

            self._definir_campo(
                self.campo_largura_contorno,
                ""
            )

            self._definir_estado_visual(
                "disabled"
            )

            self._definir_estado_botoes_cor(
                "disabled"
            )

        self._atualizar_amostras_atuais()

        if elemento.bloqueado:
            self._definir_estado_campos(
                "disabled"
            )

    def _definir_estado_campos(
        self,
        estado
    ):
        for campo in self._todos_campos():
            campo.configure(
                state=estado
            )

        self.botao_aplicar.configure(
            state=estado
        )

        self._definir_estado_botoes_cor(
            estado
        )

    def _definir_estado_visual(
        self,
        estado
    ):
        for campo in [
            self.campo_texto,
            self.campo_tamanho_fonte,
            self.campo_cor,
            self.campo_contorno,
            self.campo_largura_contorno
        ]:
            campo.configure(
                state=estado
            )

    def _definir_estado_botoes_cor(
        self,
        estado
    ):
        self.botao_cor.configure(
            state=estado
        )

        self.botao_contorno.configure(
            state=estado
        )

    def _todos_campos(self):
        return [
            self.campo_nome,
            self.campo_x,
            self.campo_y,
            self.campo_largura,
            self.campo_altura,
            self.campo_rotacao,
            self.campo_opacidade,
            self.campo_texto,
            self.campo_tamanho_fonte,
            self.campo_cor,
            self.campo_contorno,
            self.campo_largura_contorno
        ]

    def _limpar_campos(self):
        for campo in self._todos_campos():
            campo.configure(
                state="normal"
            )

            campo.delete(
                0,
                "end"
            )

        self._atualizar_amostra_cor(
            self.amostra_cor,
            "#777777"
        )

        self._atualizar_amostra_cor(
            self.amostra_contorno,
            "#777777"
        )

    def _definir_campo(
        self,
        campo,
        valor
    ):
        estado_anterior = campo.cget(
            "state"
        )

        campo.configure(
            state="normal"
        )

        campo.delete(
            0,
            "end"
        )

        campo.insert(
            0,
            str(valor)
        )

        campo.configure(
            state=estado_anterior
        )
