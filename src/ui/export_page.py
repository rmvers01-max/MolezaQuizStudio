import os
from pathlib import Path

import customtkinter as ctk

from core.project_manager import ProjectManager


class ExportPage(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.project_manager = ProjectManager()

        self.criar_interface()
        self.atualizar_lista()

    def criar_interface(self):
        self.grid_columnconfigure(
            0,
            weight=1
        )

        self.grid_rowconfigure(
            1,
            weight=1
        )

        # =====================================
        # CABEÇALHO
        # =====================================

        cabecalho = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        cabecalho.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=30,
            pady=(25, 15)
        )

        cabecalho.grid_columnconfigure(
            0,
            weight=1
        )

        textos = ctk.CTkFrame(
            cabecalho,
            fg_color="transparent"
        )

        textos.grid(
            row=0,
            column=0,
            sticky="w"
        )

        ctk.CTkLabel(
            textos,
            text="Vídeos exportados",
            font=("Arial", 28, "bold")
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            textos,
            text=(
                "Visualize os vídeos gerados "
                "pelo Moleza Quiz Studio."
            ),
            text_color="gray70"
        ).pack(
            anchor="w",
            pady=(5, 0)
        )

        ctk.CTkButton(
            cabecalho,
            text="Atualizar",
            width=120,
            command=self.atualizar_lista
        ).grid(
            row=0,
            column=1,
            sticky="e"
        )

        # =====================================
        # LISTA DE VÍDEOS
        # =====================================

        self.lista = ctk.CTkScrollableFrame(
            self
        )

        self.lista.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=30,
            pady=(0, 20)
        )

        self.lista.grid_columnconfigure(
            0,
            weight=1
        )

        # =====================================
        # STATUS
        # =====================================

        self.status = ctk.CTkLabel(
            self,
            text=""
        )

        self.status.grid(
            row=2,
            column=0,
            pady=(0, 20)
        )

    def atualizar_lista(self):
        for widget in self.lista.winfo_children():
            widget.destroy()

        videos = self.localizar_videos()

        if not videos:
            ctk.CTkLabel(
                self.lista,
                text=(
                    "Nenhum vídeo exportado "
                    "foi encontrado."
                ),
                font=("Arial", 18)
            ).grid(
                row=0,
                column=0,
                padx=20,
                pady=50
            )

            self.status.configure(
                text="Nenhum vídeo disponível."
            )

            return

        for indice, dados_video in enumerate(
            videos
        ):
            self.criar_cartao_video(
                indice=indice,
                dados_video=dados_video
            )

        self.status.configure(
            text=(
                f"{len(videos)} vídeo(s) "
                "encontrado(s)."
            )
        )

    def localizar_videos(self):
        videos = []

        projetos = (
            self.project_manager
            .listar_projetos()
        )

        for pasta_projeto in projetos:
            pasta_exportado = (
                pasta_projeto
                / "exportado"
            )

            if not pasta_exportado.exists():
                continue

            for caminho_video in (
                pasta_exportado.glob("*.mp4")
            ):
                try:
                    tamanho_bytes = (
                        caminho_video
                        .stat()
                        .st_size
                    )

                    modificacao = (
                        caminho_video
                        .stat()
                        .st_mtime
                    )

                except OSError:
                    tamanho_bytes = 0
                    modificacao = 0

                videos.append({
                    "projeto": pasta_projeto.name,
                    "caminho": caminho_video,
                    "tamanho": tamanho_bytes,
                    "modificacao": modificacao
                })

        videos.sort(
            key=lambda item: item["modificacao"],
            reverse=True
        )

        return videos

    def criar_cartao_video(
        self,
        indice,
        dados_video
    ):
        caminho_video = dados_video[
            "caminho"
        ]

        cartao = ctk.CTkFrame(
            self.lista
        )

        cartao.grid(
            row=indice,
            column=0,
            sticky="ew",
            padx=10,
            pady=8
        )

        cartao.grid_columnconfigure(
            0,
            weight=1
        )

        # Informações do vídeo

        informacoes = ctk.CTkFrame(
            cartao,
            fg_color="transparent"
        )

        informacoes.grid(
            row=0,
            column=0,
            sticky="w",
            padx=20,
            pady=15
        )

        ctk.CTkLabel(
            informacoes,
            text=caminho_video.name,
            font=("Arial", 17, "bold")
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            informacoes,
            text=(
                f"Projeto: "
                f"{dados_video['projeto']}"
            ),
            text_color="gray70"
        ).pack(
            anchor="w",
            pady=(4, 0)
        )

        tamanho = self.formatar_tamanho(
            dados_video["tamanho"]
        )

        ctk.CTkLabel(
            informacoes,
            text=f"Tamanho: {tamanho}",
            text_color="gray70"
        ).pack(
            anchor="w",
            pady=(2, 0)
        )

        # Botões

        botoes = ctk.CTkFrame(
            cartao,
            fg_color="transparent"
        )

        botoes.grid(
            row=0,
            column=1,
            padx=20,
            pady=15
        )

        ctk.CTkButton(
            botoes,
            text="Reproduzir",
            width=115,
            command=lambda caminho=caminho_video: (
                self.abrir_video(caminho)
            )
        ).pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            botoes,
            text="Abrir pasta",
            width=115,
            fg_color="gray35",
            hover_color="gray25",
            command=lambda caminho=caminho_video: (
                self.abrir_pasta(caminho)
            )
        ).pack(
            side="left",
            padx=5
        )

    def abrir_video(
        self,
        caminho_video
    ):
        caminho_video = Path(
            caminho_video
        )

        if not caminho_video.exists():
            self.status.configure(
                text=(
                    "O arquivo de vídeo "
                    "não foi encontrado."
                )
            )

            self.atualizar_lista()
            return

        try:
            os.startfile(
                str(caminho_video)
            )

            self.status.configure(
                text=(
                    f"Abrindo: "
                    f"{caminho_video.name}"
                )
            )

        except OSError as erro:
            self.status.configure(
                text=(
                    "Não foi possível abrir "
                    f"o vídeo: {erro}"
                )
            )

    def abrir_pasta(
        self,
        caminho_video
    ):
        caminho_video = Path(
            caminho_video
        )

        pasta = caminho_video.parent

        if not pasta.exists():
            self.status.configure(
                text=(
                    "A pasta do vídeo "
                    "não foi encontrada."
                )
            )

            return

        try:
            os.startfile(
                str(pasta)
            )

            self.status.configure(
                text=(
                    f"Abrindo pasta: "
                    f"{pasta}"
                )
            )

        except OSError as erro:
            self.status.configure(
                text=(
                    "Não foi possível abrir "
                    f"a pasta: {erro}"
                )
            )

    def formatar_tamanho(
        self,
        tamanho_bytes
    ):
        tamanho = float(
            tamanho_bytes
        )

        unidades = [
            "B",
            "KB",
            "MB",
            "GB"
        ]

        for unidade in unidades:
            if tamanho < 1024:
                return (
                    f"{tamanho:.1f} "
                    f"{unidade}"
                )

            tamanho /= 1024

        return f"{tamanho:.1f} TB"
