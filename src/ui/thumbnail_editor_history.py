from typing import Callable, Optional

import customtkinter as ctk

from core.thumbnail_elements import ThumbnailDocument
from core.thumbnail_history import ThumbnailHistory


class ThumbnailEditorHistoryController:
    """Integra o histórico do editor aos botões e atalhos de teclado."""

    def __init__(
        self,
        owner,
        obter_documento: Callable[[], ThumbnailDocument],
        restaurar_documento: Callable[[ThumbnailDocument, str], None],
        limite: int = 60
    ):
        self.owner = owner
        self.obter_documento = obter_documento
        self.restaurar_documento = restaurar_documento
        self.historico = ThumbnailHistory(limite=limite)

        self.botao_desfazer: Optional[ctk.CTkButton] = None
        self.botao_refazer: Optional[ctk.CTkButton] = None
        self.atalhos_ativos = False

    def criar_botoes(self, master):
        self.botao_desfazer = ctk.CTkButton(
            master,
            text="↶ Desfazer",
            width=105,
            fg_color="gray35",
            hover_color="gray25",
            command=self.desfazer
        )
        self.botao_desfazer.pack(side="left", padx=4)

        self.botao_refazer = ctk.CTkButton(
            master,
            text="↷ Refazer",
            width=100,
            fg_color="gray35",
            hover_color="gray25",
            command=self.refazer
        )
        self.botao_refazer.pack(side="left", padx=4)

        self.atualizar_botoes()

    def vincular_atalhos(self):
        if self.atalhos_ativos:
            return

        raiz = self.owner.winfo_toplevel()
        raiz.bind("<Control-z>", self._atalho_desfazer, add="+")
        raiz.bind("<Control-y>", self._atalho_refazer, add="+")
        raiz.bind("<Control-Shift-Z>", self._atalho_refazer, add="+")
        raiz.bind("<Control-Shift-z>", self._atalho_refazer, add="+")
        self.atalhos_ativos = True

    def iniciar(self, documento: Optional[ThumbnailDocument] = None):
        documento = documento or self.obter_documento()
        self.historico.iniciar(documento)
        self.atualizar_botoes()

    def registrar(self, documento: Optional[ThumbnailDocument] = None) -> bool:
        documento = documento or self.obter_documento()
        registrado = self.historico.registrar(documento)
        self.atualizar_botoes()
        return registrado

    def desfazer(self):
        documento = self.historico.desfazer()
        if documento is None:
            self.atualizar_botoes()
            return

        self.restaurar_documento(documento, "Alteração desfeita.")
        self.atualizar_botoes()

    def refazer(self):
        documento = self.historico.refazer()
        if documento is None:
            self.atualizar_botoes()
            return

        self.restaurar_documento(documento, "Alteração refeita.")
        self.atualizar_botoes()

    def atualizar_botoes(self):
        if self.botao_desfazer is not None:
            self.botao_desfazer.configure(
                state="normal" if self.historico.pode_desfazer() else "disabled"
            )

        if self.botao_refazer is not None:
            self.botao_refazer.configure(
                state="normal" if self.historico.pode_refazer() else "disabled"
            )

    def _atalho_desfazer(self, evento=None):
        self.desfazer()
        return "break"

    def _atalho_refazer(self, evento=None):
        self.refazer()
        return "break"
