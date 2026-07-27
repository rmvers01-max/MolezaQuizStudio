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


class DocumentMixin:
    def criar_documento_inicial(self):
        documento = ThumbnailDocument(
            largura=1280,
            altura=720,
            cor_fundo="#6D28B2"
        )

        documento.adicionar_elemento(
            ShapeElement(
                nome="Fundo",
                x=0,
                y=0,
                largura=1280,
                altura=720,
                formato="retangulo",
                cor="#6D28B2",
                camada=0,
                bloqueado=True
            )
        )

        documento.adicionar_elemento(
            TextElement(
                nome="Título",
                x=180,
                y=30,
                largura=920,
                altura=110,
                texto="O QUE VOCÊ PREFERE?",
                tamanho_fonte=72,
                cor="#FFFFFF",
                cor_contorno="#43136E",
                largura_contorno=4,
                sombra=True,
                camada=1
            )
        )

        self.canvas_editor.definir_documento(
            documento
        )

        self.elemento_selecionado = None
        self.elemento_copiado = None
        self.caminho_documento_atual = None
        self.documento_alterado = False

        self.atualizar_lista_camadas()
        self._atualizar_rotulo_arquivo()
        self.historico_editor.iniciar(
            documento
        )

    def novo_documento(self):
        if not self._confirmar_descarte():
            return

        self.criar_documento_inicial()

        self.status.configure(
            text="Novo documento criado."
        )

    def abrir_documento(self):
        if not self._confirmar_descarte():
            return

        caminho = filedialog.askopenfilename(
            parent=self.winfo_toplevel(),
            title="Abrir projeto de thumbnail",
            filetypes=[
                (
                    "Projeto de thumbnail",
                    "*.json"
                ),
                (
                    "Todos os arquivos",
                    "*.*"
                )
            ]
        )

        if not caminho:
            return

        try:
            documento = self.document_manager.carregar(
                caminho
            )

            self.canvas_editor.definir_documento(
                documento
            )

            self.caminho_documento_atual = Path(
                caminho
            )

            self.documento_alterado = False
            self.elemento_selecionado = None

            self.atualizar_lista_camadas()
            self._atualizar_rotulo_arquivo()
            self.historico_editor.iniciar(
                documento
            )

            self.status.configure(
                text=f"Documento carregado: {caminho}"
            )

        except (
            OSError,
            ValueError
        ) as erro:
            messagebox.showerror(
                title="Erro ao abrir documento",
                message=str(erro),
                parent=self.winfo_toplevel()
            )

    def salvar_documento(self):
        if self.caminho_documento_atual is None:
            self.salvar_documento_como()
            return

        self._salvar_no_caminho(
            self.caminho_documento_atual
        )

    def salvar_documento_como(self):
        caminho = filedialog.asksaveasfilename(
            parent=self.winfo_toplevel(),
            title="Salvar projeto de thumbnail",
            defaultextension=".json",
            filetypes=[
                (
                    "Projeto de thumbnail",
                    "*.json"
                )
            ]
        )

        if not caminho:
            return

        self._salvar_no_caminho(
            caminho
        )

    def _salvar_no_caminho(
        self,
        caminho
    ):
        try:
            caminho_salvo = self.document_manager.salvar(
                documento=(
                    self.canvas_editor
                    .obter_documento()
                ),
                caminho_arquivo=caminho
            )

            self.caminho_documento_atual = caminho_salvo
            self.documento_alterado = False

            self._atualizar_rotulo_arquivo()

            self.status.configure(
                text=f"Documento salvo: {caminho_salvo}"
            )

        except OSError as erro:
            messagebox.showerror(
                title="Erro ao salvar documento",
                message=str(erro),
                parent=self.winfo_toplevel()
            )

    def exportar_png(self):
        self._exportar_imagem(
            extensao=".png",
            descricao="Imagem PNG"
        )

    def exportar_jpg(self):
        self._exportar_imagem(
            extensao=".jpg",
            descricao="Imagem JPG"
        )

    def _exportar_imagem(
        self,
        extensao,
        descricao
    ):
        caminho = filedialog.asksaveasfilename(
            parent=self.winfo_toplevel(),
            title="Exportar thumbnail",
            defaultextension=extensao,
            filetypes=[
                (
                    descricao,
                    f"*{extensao}"
                )
            ]
        )

        if not caminho:
            return

        try:
            caminho_exportado = self.document_renderer.salvar(
                documento=(
                    self.canvas_editor
                    .obter_documento()
                ),
                caminho_saida=caminho
            )

            self.status.configure(
                text=f"Thumbnail exportada: {caminho_exportado}"
            )

            messagebox.showinfo(
                title="Thumbnail exportada",
                message=(
                    "A thumbnail foi exportada com sucesso.\n\n"
                    f"{caminho_exportado}"
                ),
                parent=self.winfo_toplevel()
            )

        except OSError as erro:
            messagebox.showerror(
                title="Erro ao exportar",
                message=str(erro),
                parent=self.winfo_toplevel()
            )
