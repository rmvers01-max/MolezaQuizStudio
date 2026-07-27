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


class HelpersMixin:
    def _obter_documento_atual(self):
        return self.canvas_editor.obter_documento()

    def _restaurar_documento_historico(
        self,
        documento,
        mensagem
    ):
        self.canvas_editor.definir_documento(
            documento
        )

        self.elemento_selecionado = None
        self.documento_alterado = True

        self.atualizar_lista_camadas()
        self._atualizar_rotulo_arquivo()

        self.status.configure(
            text=mensagem
        )

    def _limitar_elemento(
        self,
        elemento
    ):
        documento = self.canvas_editor.obter_documento()

        elemento.x = max(
            min(
                elemento.x,
                documento.largura - elemento.largura
            ),
            0
        )

        elemento.y = max(
            min(
                elemento.y,
                documento.altura - elemento.altura
            ),
            0
        )

    def _proxima_camada(
        self,
        documento
    ):
        if not documento.elementos:
            return 0

        return (
            max(
                elemento.camada
                for elemento in documento.elementos
            )
            + 1
        )

    def _marcar_alterado(
        self,
        mensagem
    ):
        self.documento_alterado = True
        self.historico_editor.registrar()

        self.atualizar_lista_camadas()
        self._atualizar_rotulo_arquivo()

        self.status.configure(
            text=mensagem
        )

    def _atualizar_rotulo_arquivo(self):
        if self.caminho_documento_atual:
            texto = self.caminho_documento_atual.name
        else:
            texto = "Novo documento"

        if self.documento_alterado:
            texto += " *"

        self.rotulo_arquivo.configure(
            text=texto
        )

    def _confirmar_descarte(self):
        if not self.documento_alterado:
            return True

        return messagebox.askyesno(
            title="Alterações não salvas",
            message=(
                "Existem alterações que ainda não foram salvas.\n\n"
                "Deseja descartá-las?"
            ),
            parent=self.winfo_toplevel()
        )
