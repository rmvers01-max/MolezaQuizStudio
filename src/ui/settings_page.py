from pathlib import Path
from tkinter import filedialog, messagebox

import customtkinter as ctk
from PIL import Image, UnidentifiedImageError

from core.branding_manager import BrandingManager
from utils.config import Config


class SettingsPage(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.config = Config()
        self.branding_manager = BrandingManager()

        self.preview_mascote_ctk = None
        self.preview_logo_ctk = None

        self.criar_interface()
        self.carregar_valores()
        self.atualizar_identidade_visual()

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

        ctk.CTkLabel(
            cabecalho,
            text="Configurações",
            font=("Arial", 28, "bold")
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            cabecalho,
            text=(
                "Defina os valores padrão dos quizzes "
                "e a identidade visual do Moleza Quiz."
            ),
            text_color="gray70"
        ).pack(
            anchor="w",
            pady=(5, 0)
        )

        # =====================================
        # ÁREA ROLÁVEL
        # =====================================

        painel = ctk.CTkScrollableFrame(
            self
        )

        painel.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=30,
            pady=(0, 30)
        )

        painel.grid_columnconfigure(
            0,
            weight=1
        )

        self._criar_configuracoes_gerais(
            painel
        )

        self._criar_identidade_visual(
            painel
        )

        self.status = ctk.CTkLabel(
            painel,
            text="",
            wraplength=900
        )

        self.status.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=20,
            pady=(5, 25)
        )

    def _criar_configuracoes_gerais(
        self,
        painel
    ):
        formulario = ctk.CTkFrame(
            painel
        )

        formulario.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=15,
            pady=(15, 8)
        )

        formulario.grid_columnconfigure(
            1,
            weight=1
        )

        ctk.CTkLabel(
            formulario,
            text="Configurações gerais",
            font=("Arial", 20, "bold")
        ).grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="w",
            padx=20,
            pady=(22, 15)
        )

        # Quantidade padrão

        ctk.CTkLabel(
            formulario,
            text="Quantidade padrão de perguntas"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=20,
            pady=10
        )

        self.quantidade = ctk.CTkEntry(
            formulario,
            width=160
        )

        self.quantidade.grid(
            row=1,
            column=1,
            sticky="w",
            padx=20,
            pady=10
        )

        # Tempo

        ctk.CTkLabel(
            formulario,
            text="Tempo por pergunta"
        ).grid(
            row=2,
            column=0,
            sticky="w",
            padx=20,
            pady=10
        )

        self.tempo = ctk.CTkEntry(
            formulario,
            width=160
        )

        self.tempo.grid(
            row=2,
            column=1,
            sticky="w",
            padx=20,
            pady=10
        )

        # Resolução

        ctk.CTkLabel(
            formulario,
            text="Resolução do vídeo"
        ).grid(
            row=3,
            column=0,
            sticky="w",
            padx=20,
            pady=10
        )

        self.resolucao = ctk.CTkOptionMenu(
            formulario,
            values=[
                "1920x1080",
                "1080x1920",
                "1280x720"
            ],
            width=160
        )

        self.resolucao.grid(
            row=3,
            column=1,
            sticky="w",
            padx=20,
            pady=10
        )

        # FPS

        ctk.CTkLabel(
            formulario,
            text="Quadros por segundo (FPS)"
        ).grid(
            row=4,
            column=0,
            sticky="w",
            padx=20,
            pady=10
        )

        self.fps = ctk.CTkOptionMenu(
            formulario,
            values=[
                "24",
                "30",
                "60"
            ],
            width=160
        )

        self.fps.grid(
            row=4,
            column=1,
            sticky="w",
            padx=20,
            pady=10
        )

        # Voz

        ctk.CTkLabel(
            formulario,
            text="Voz padrão"
        ).grid(
            row=5,
            column=0,
            sticky="w",
            padx=20,
            pady=10
        )

        self.voz = ctk.CTkOptionMenu(
            formulario,
            values=[
                "Feminina alegre",
                "Feminina suave",
                "Masculina alegre",
                "Masculina suave"
            ],
            width=200
        )

        self.voz.grid(
            row=5,
            column=1,
            sticky="w",
            padx=20,
            pady=10
        )

        # Botões

        botoes = ctk.CTkFrame(
            formulario,
            fg_color="transparent"
        )

        botoes.grid(
            row=6,
            column=0,
            columnspan=2,
            pady=30
        )

        ctk.CTkButton(
            botoes,
            text="Salvar configurações",
            width=190,
            height=42,
            command=self.salvar_configuracoes
        ).pack(
            side="left",
            padx=8
        )

        ctk.CTkButton(
            botoes,
            text="Restaurar padrão",
            width=160,
            height=42,
            fg_color="gray35",
            hover_color="gray25",
            command=self.restaurar_padrao
        ).pack(
            side="left",
            padx=8
        )

    def _criar_identidade_visual(
        self,
        painel
    ):
        identidade = ctk.CTkFrame(
            painel
        )

        identidade.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=15,
            pady=8
        )

        identidade.grid_columnconfigure(
            0,
            weight=1
        )

        ctk.CTkLabel(
            identidade,
            text="Identidade visual do canal",
            font=("Arial", 20, "bold")
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=20,
            pady=(22, 5)
        )

        ctk.CTkLabel(
            identidade,
            text=(
                "Configure o mascote e o logotipo que serão usados "
                "nas futuras thumbnails do Moleza Quiz. "
                "Arquivos PNG com fundo transparente são recomendados."
            ),
            text_color="gray70",
            justify="left",
            wraplength=900
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=20,
            pady=(0, 18)
        )

        area_recursos = ctk.CTkFrame(
            identidade,
            fg_color="transparent"
        )

        area_recursos.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=20,
            pady=(0, 15)
        )

        area_recursos.grid_columnconfigure(
            0,
            weight=1
        )

        area_recursos.grid_columnconfigure(
            1,
            weight=1
        )

        self._criar_card_mascote(
            area_recursos
        )

        self._criar_card_logo(
            area_recursos
        )

        botoes = ctk.CTkFrame(
            identidade,
            fg_color="transparent"
        )

        botoes.grid(
            row=3,
            column=0,
            pady=(5, 25)
        )

        ctk.CTkButton(
            botoes,
            text="Atualizar visualizações",
            width=190,
            command=self.atualizar_identidade_visual
        ).pack(
            side="left",
            padx=7
        )

        ctk.CTkButton(
            botoes,
            text="Abrir pasta da identidade visual",
            width=235,
            fg_color="gray35",
            hover_color="gray25",
            command=self.abrir_pasta_branding
        ).pack(
            side="left",
            padx=7
        )

    def _criar_card_mascote(
        self,
        area_recursos
    ):
        card = ctk.CTkFrame(
            area_recursos
        )

        card.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 8),
            pady=5
        )

        card.grid_columnconfigure(
            0,
            weight=1
        )

        ctk.CTkLabel(
            card,
            text="Mascote Moleza Quiz",
            font=("Arial", 17, "bold")
        ).grid(
            row=0,
            column=0,
            padx=15,
            pady=(18, 5)
        )

        self.preview_mascote = ctk.CTkLabel(
            card,
            text="Mascote não configurado",
            width=300,
            height=220,
            fg_color="#151B24",
            corner_radius=12
        )

        self.preview_mascote.grid(
            row=1,
            column=0,
            padx=15,
            pady=12
        )

        self.rotulo_mascote = ctk.CTkLabel(
            card,
            text="Nenhum arquivo selecionado.",
            text_color="gray70",
            wraplength=360
        )

        self.rotulo_mascote.grid(
            row=2,
            column=0,
            padx=15,
            pady=(0, 12)
        )

        botoes = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        botoes.grid(
            row=3,
            column=0,
            pady=(0, 18)
        )

        ctk.CTkButton(
            botoes,
            text="Selecionar mascote",
            width=155,
            command=self.selecionar_mascote
        ).pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            botoes,
            text="Remover",
            width=90,
            fg_color="#A63D40",
            hover_color="#7F2E31",
            command=self.remover_mascote
        ).pack(
            side="left",
            padx=5
        )

    def _criar_card_logo(
        self,
        area_recursos
    ):
        card = ctk.CTkFrame(
            area_recursos
        )

        card.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(8, 0),
            pady=5
        )

        card.grid_columnconfigure(
            0,
            weight=1
        )

        ctk.CTkLabel(
            card,
            text="Logotipo ou nome do canal",
            font=("Arial", 17, "bold")
        ).grid(
            row=0,
            column=0,
            padx=15,
            pady=(18, 5)
        )

        self.preview_logo = ctk.CTkLabel(
            card,
            text="Logotipo não configurado",
            width=300,
            height=220,
            fg_color="#151B24",
            corner_radius=12
        )

        self.preview_logo.grid(
            row=1,
            column=0,
            padx=15,
            pady=12
        )

        self.rotulo_logo = ctk.CTkLabel(
            card,
            text="Nenhum arquivo selecionado.",
            text_color="gray70",
            wraplength=360
        )

        self.rotulo_logo.grid(
            row=2,
            column=0,
            padx=15,
            pady=(0, 12)
        )

        botoes = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        botoes.grid(
            row=3,
            column=0,
            pady=(0, 18)
        )

        ctk.CTkButton(
            botoes,
            text="Selecionar logotipo",
            width=155,
            command=self.selecionar_logo
        ).pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            botoes,
            text="Remover",
            width=90,
            fg_color="#A63D40",
            hover_color="#7F2E31",
            command=self.remover_logo
        ).pack(
            side="left",
            padx=5
        )

    def carregar_valores(self):
        self.quantidade.delete(
            0,
            "end"
        )

        self.quantidade.insert(
            0,
            str(
                self.config.get(
                    "quantidade_perguntas",
                    10
                )
            )
        )

        self.tempo.delete(
            0,
            "end"
        )

        self.tempo.insert(
            0,
            str(
                self.config.get(
                    "tempo_pergunta",
                    5
                )
            )
        )

        self.resolucao.set(
            self.config.get(
                "resolucao",
                "1920x1080"
            )
        )

        self.fps.set(
            str(
                self.config.get(
                    "fps",
                    30
                )
            )
        )

        self.voz.set(
            self.config.get(
                "voz",
                "Feminina alegre"
            )
        )

    def salvar_configuracoes(self):
        try:
            quantidade = int(
                self.quantidade.get()
            )

            tempo = int(
                self.tempo.get()
            )

            fps = int(
                self.fps.get()
            )

            if quantidade < 1 or quantidade > 100:
                raise ValueError(
                    "A quantidade deve ficar entre 1 e 100."
                )

            if tempo < 1 or tempo > 60:
                raise ValueError(
                    "O tempo deve ficar entre 1 e 60 segundos."
                )

            self.config.atualizar({
                "quantidade_perguntas": quantidade,
                "tempo_pergunta": tempo,
                "resolucao": self.resolucao.get(),
                "fps": fps,
                "voz": self.voz.get()
            })

            self.status.configure(
                text="Configurações salvas com sucesso."
            )

        except ValueError as erro:
            self.status.configure(
                text=f"Erro: {erro}"
            )

        except OSError as erro:
            self.status.configure(
                text=(
                    "Não foi possível salvar as configurações: "
                    f"{erro}"
                )
            )

    def restaurar_padrao(self):
        try:
            self.config.restaurar_padrao()
            self.carregar_valores()

            self.status.configure(
                text="Configurações padrão restauradas."
            )

        except OSError as erro:
            self.status.configure(
                text=(
                    "Não foi possível restaurar as configurações: "
                    f"{erro}"
                )
            )

    def selecionar_mascote(self):
        caminho = self._selecionar_arquivo_imagem(
            titulo="Selecione o mascote do Moleza Quiz"
        )

        if not caminho:
            return

        try:
            destino = (
                self.branding_manager
                .importar_mascote(
                    caminho
                )
            )

            self.atualizar_identidade_visual()

            self.status.configure(
                text=(
                    "Mascote importado com sucesso: "
                    f"{destino}"
                )
            )

        except (
            FileNotFoundError,
            ValueError,
            OSError
        ) as erro:
            messagebox.showerror(
                title="Erro ao importar mascote",
                message=str(erro),
                parent=self.winfo_toplevel()
            )

            self.status.configure(
                text=f"Erro ao importar mascote: {erro}"
            )

    def selecionar_logo(self):
        caminho = self._selecionar_arquivo_imagem(
            titulo=(
                "Selecione o logotipo ou a arte "
                "com o nome do canal"
            )
        )

        if not caminho:
            return

        try:
            destino = (
                self.branding_manager
                .importar_logo(
                    caminho
                )
            )

            self.atualizar_identidade_visual()

            self.status.configure(
                text=(
                    "Logotipo importado com sucesso: "
                    f"{destino}"
                )
            )

        except (
            FileNotFoundError,
            ValueError,
            OSError
        ) as erro:
            messagebox.showerror(
                title="Erro ao importar logotipo",
                message=str(erro),
                parent=self.winfo_toplevel()
            )

            self.status.configure(
                text=f"Erro ao importar logotipo: {erro}"
            )

    def remover_mascote(self):
        caminho = self.branding_manager.obter_mascote()

        if caminho is None:
            self.status.configure(
                text="Nenhum mascote está configurado."
            )

            return

        confirmar = messagebox.askyesno(
            title="Remover mascote",
            message=(
                "Deseja remover o mascote configurado?\n\n"
                "O arquivo original que você selecionou "
                "não será apagado."
            ),
            parent=self.winfo_toplevel()
        )

        if not confirmar:
            return

        try:
            removido = (
                self.branding_manager
                .remover_mascote()
            )

            self.atualizar_identidade_visual()

            if removido:
                self.status.configure(
                    text="Mascote removido."
                )
            else:
                self.status.configure(
                    text="O mascote não foi encontrado."
                )

        except OSError as erro:
            messagebox.showerror(
                title="Erro ao remover mascote",
                message=str(erro),
                parent=self.winfo_toplevel()
            )

    def remover_logo(self):
        caminho = self.branding_manager.obter_logo()

        if caminho is None:
            self.status.configure(
                text="Nenhum logotipo está configurado."
            )

            return

        confirmar = messagebox.askyesno(
            title="Remover logotipo",
            message=(
                "Deseja remover o logotipo configurado?\n\n"
                "O arquivo original que você selecionou "
                "não será apagado."
            ),
            parent=self.winfo_toplevel()
        )

        if not confirmar:
            return

        try:
            removido = (
                self.branding_manager
                .remover_logo()
            )

            self.atualizar_identidade_visual()

            if removido:
                self.status.configure(
                    text="Logotipo removido."
                )
            else:
                self.status.configure(
                    text="O logotipo não foi encontrado."
                )

        except OSError as erro:
            messagebox.showerror(
                title="Erro ao remover logotipo",
                message=str(erro),
                parent=self.winfo_toplevel()
            )

    def atualizar_identidade_visual(self):
        caminho_mascote = (
            self.branding_manager
            .obter_mascote()
        )

        caminho_logo = (
            self.branding_manager
            .obter_logo()
        )

        self.preview_mascote_ctk = (
            self._carregar_preview(
                caminho=caminho_mascote,
                tamanho_maximo=(280, 200)
            )
        )

        if self.preview_mascote_ctk:
            self.preview_mascote.configure(
                image=self.preview_mascote_ctk,
                text=""
            )

            self.rotulo_mascote.configure(
                text=str(
                    caminho_mascote
                )
            )
        else:
            self.preview_mascote.configure(
                image=None,
                text="Mascote não configurado"
            )

            self.rotulo_mascote.configure(
                text="Nenhum arquivo selecionado."
            )

        self.preview_logo_ctk = (
            self._carregar_preview(
                caminho=caminho_logo,
                tamanho_maximo=(280, 200)
            )
        )

        if self.preview_logo_ctk:
            self.preview_logo.configure(
                image=self.preview_logo_ctk,
                text=""
            )

            self.rotulo_logo.configure(
                text=str(
                    caminho_logo
                )
            )
        else:
            self.preview_logo.configure(
                image=None,
                text="Logotipo não configurado"
            )

            self.rotulo_logo.configure(
                text="Nenhum arquivo selecionado."
            )

    def abrir_pasta_branding(self):
        try:
            self.branding_manager.abrir_pasta_branding()

            self.status.configure(
                text=(
                    "Abrindo pasta da identidade visual: "
                    f"{self.branding_manager.pasta_branding}"
                )
            )

        except OSError as erro:
            messagebox.showerror(
                title="Erro",
                message=(
                    "Não foi possível abrir a pasta.\n\n"
                    f"{erro}"
                ),
                parent=self.winfo_toplevel()
            )

    def _selecionar_arquivo_imagem(
        self,
        titulo
    ):
        return filedialog.askopenfilename(
            parent=self.winfo_toplevel(),
            title=titulo,
            filetypes=[
                (
                    "Arquivos de imagem",
                    "*.png *.jpg *.jpeg *.webp"
                ),
                (
                    "PNG com transparência",
                    "*.png"
                ),
                (
                    "Todos os arquivos",
                    "*.*"
                )
            ]
        )

    def _carregar_preview(
        self,
        caminho,
        tamanho_maximo
    ):
        if caminho is None:
            return None

        caminho = Path(
            caminho
        )

        if not caminho.exists():
            return None

        try:
            with Image.open(caminho) as imagem_original:
                imagem = imagem_original.convert(
                    "RGBA"
                )

                imagem.thumbnail(
                    tamanho_maximo,
                    Image.Resampling.LANCZOS
                )

                imagem_preview = imagem.copy()

            largura = max(
                imagem_preview.width,
                1
            )

            altura = max(
                imagem_preview.height,
                1
            )

            return ctk.CTkImage(
                light_image=imagem_preview,
                dark_image=imagem_preview,
                size=(
                    largura,
                    altura
                )
            )

        except (
            OSError,
            ValueError,
            UnidentifiedImageError
        ):
            return None
