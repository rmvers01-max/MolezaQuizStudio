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


class ColorsMixin:
    def escolher_cor_principal(self):
        elemento = self.elemento_selecionado

        if elemento is None:
            self.status.configure(
                text="Selecione um texto ou uma forma primeiro."
            )
            return

        if elemento.bloqueado:
            self.status.configure(
                text="Este elemento está bloqueado."
            )
            return

        cor_atual = self._obter_cor_valida(
            self.campo_cor.get(),
            self.COR_PADRAO
        )

        _, cor_hexadecimal = colorchooser.askcolor(
            color=cor_atual,
            title="Escolha a cor do elemento",
            parent=self.winfo_toplevel()
        )

        if not cor_hexadecimal:
            return

        cor_hexadecimal = cor_hexadecimal.upper()

        self._definir_campo(
            self.campo_cor,
            cor_hexadecimal
        )

        self._atualizar_amostra_cor(
            self.amostra_cor,
            cor_hexadecimal
        )

        if isinstance(
            elemento,
            TextElement
        ):
            elemento.cor = cor_hexadecimal

        elif isinstance(
            elemento,
            ShapeElement
        ):
            elemento.cor = cor_hexadecimal

        else:
            self.status.configure(
                text=(
                    "A cor principal está disponível "
                    "para textos e formas."
                )
            )
            return

        self._atualizar_canvas_apos_cor(
            "Cor alterada."
        )

    def escolher_cor_contorno(self):
        elemento = self.elemento_selecionado

        if elemento is None:
            self.status.configure(
                text="Selecione um texto ou uma forma primeiro."
            )
            return

        if elemento.bloqueado:
            self.status.configure(
                text="Este elemento está bloqueado."
            )
            return

        cor_atual = self._obter_cor_valida(
            self.campo_contorno.get(),
            self.COR_CONTORNO_PADRAO
        )

        _, cor_hexadecimal = colorchooser.askcolor(
            color=cor_atual,
            title="Escolha a cor do contorno",
            parent=self.winfo_toplevel()
        )

        if not cor_hexadecimal:
            return

        cor_hexadecimal = cor_hexadecimal.upper()

        self._definir_campo(
            self.campo_contorno,
            cor_hexadecimal
        )

        self._atualizar_amostra_cor(
            self.amostra_contorno,
            cor_hexadecimal
        )

        if isinstance(
            elemento,
            TextElement
        ):
            elemento.cor_contorno = cor_hexadecimal

        elif isinstance(
            elemento,
            ShapeElement
        ):
            elemento.cor_contorno = cor_hexadecimal

        else:
            self.status.configure(
                text=(
                    "A cor de contorno está disponível "
                    "para textos e formas."
                )
            )
            return

        self._atualizar_canvas_apos_cor(
            "Cor do contorno alterada."
        )

    def _atualizar_canvas_apos_cor(
        self,
        mensagem
    ):
        self.canvas_editor.renderizar()

        self.documento_alterado = True
        self.historico_editor.registrar()

        self.atualizar_lista_camadas()
        self._atualizar_rotulo_arquivo()

        self.status.configure(
            text=mensagem
        )

    def _atualizar_amostras_atuais(self):
        cor = self._obter_cor_valida(
            self.campo_cor.get(),
            self.COR_PADRAO
        )

        contorno = self._obter_cor_valida(
            self.campo_contorno.get(),
            self.COR_CONTORNO_PADRAO
        )

        self._atualizar_amostra_cor(
            self.amostra_cor,
            cor
        )

        self._atualizar_amostra_cor(
            self.amostra_contorno,
            contorno
        )

    def _atualizar_amostra_cor(
        self,
        amostra,
        cor
    ):
        cor = self._obter_cor_valida(
            cor,
            "#777777"
        )

        try:
            amostra.configure(
                fg_color=cor
            )
        except ValueError:
            amostra.configure(
                fg_color="#777777"
            )

    def _obter_cor_valida(
        self,
        cor,
        padrao
    ):
        cor = str(
            cor
        ).strip()

        if (
            len(cor) == 7
            and cor.startswith("#")
        ):
            try:
                int(
                    cor[1:],
                    16
                )

                return cor.upper()

            except ValueError:
                pass

        return padrao
