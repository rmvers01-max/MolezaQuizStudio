import customtkinter as ctk

from ui.export_page import ExportPage
from ui.narration_page import NarrationPage
from ui.projects_page import ProjectsPage
from ui.publication_page import PublicationPage
from ui.quiz_page import QuizPage
from ui.settings_page import SettingsPage
from ui.thumbnail_editor_page import ThumbnailEditorPage
from ui.video_page import VideoPage


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class MainWindow(ctk.CTk):
    COR_MENU = "#171A22"
    COR_MENU_SECUNDARIA = "#20242E"

    COR_BOTAO = "#2B303B"
    COR_BOTAO_HOVER = "#3A4050"
    COR_BOTAO_ATIVO = "#7C3AED"
    COR_BOTAO_ATIVO_HOVER = "#6D28D9"

    COR_TEXTO_SECUNDARIO = "#A8A8B3"
    COR_SEPARADOR = "#343946"

    def __init__(self):
        super().__init__()

        self.title(
            "Moleza Quiz Studio"
        )

        self.geometry(
            "1400x800"
        )

        self.minsize(
            1100,
            680
        )

        self.botao_ativo = None
        self.botoes_menu = []

        self.criar_interface()

    def criar_interface(self):
        self.grid_columnconfigure(
            1,
            weight=1
        )

        self.grid_rowconfigure(
            0,
            weight=1
        )

        self._criar_menu_lateral()
        self._criar_area_principal()

        self.abrir_criador_quiz()

    # =========================================================
    # MENU LATERAL
    # =========================================================

    def _criar_menu_lateral(self):
        self.menu = ctk.CTkFrame(
            self,
            width=245,
            corner_radius=0,
            fg_color=self.COR_MENU
        )

        self.menu.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.menu.grid_propagate(
            False
        )

        self.menu.grid_columnconfigure(
            0,
            weight=1
        )

        self.menu.grid_rowconfigure(
            1,
            weight=1
        )

        self._criar_cabecalho_menu()

        self.menu_rolavel = ctk.CTkScrollableFrame(
            self.menu,
            fg_color="transparent",
            corner_radius=0,
            scrollbar_button_color="#393F4D",
            scrollbar_button_hover_color="#4A5162"
        )

        self.menu_rolavel.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=10,
            pady=(0, 10)
        )

        self.menu_rolavel.grid_columnconfigure(
            0,
            weight=1
        )

        self._criar_secao_producao()
        self._criar_secao_estudio()
        self._criar_secao_publicacao()
        self._criar_secao_sistema()

        self._criar_rodape_menu()

    def _criar_cabecalho_menu(self):
        cabecalho = ctk.CTkFrame(
            self.menu,
            fg_color=self.COR_MENU_SECUNDARIA,
            corner_radius=0
        )

        cabecalho.grid(
            row=0,
            column=0,
            sticky="ew"
        )

        ctk.CTkLabel(
            cabecalho,
            text="🦥",
            font=("Arial", 40)
        ).pack(
            pady=(22, 2)
        )

        ctk.CTkLabel(
            cabecalho,
            text="MOLEZA QUIZ",
            font=("Arial", 24, "bold"),
            text_color="#FFFFFF"
        ).pack()

        ctk.CTkLabel(
            cabecalho,
            text="STUDIO",
            font=("Arial", 12, "bold"),
            text_color="#BFA7FF"
        ).pack(
            pady=(0, 20)
        )

    def _criar_secao_producao(self):
        self._adicionar_titulo_secao(
            "PRODUÇÃO"
        )

        self.botao_criar_quiz = self._adicionar_botao_menu(
            texto="Criar Quiz",
            icone="✏️",
            comando=self.abrir_criador_quiz
        )

        self.botao_projetos = self._adicionar_botao_menu(
            texto="Projetos",
            icone="📁",
            comando=self.abrir_projetos
        )

        self.botao_narracao = self._adicionar_botao_menu(
            texto="Narração",
            icone="🎙️",
            comando=self.abrir_narracao
        )

        self.botao_videos = self._adicionar_botao_menu(
            texto="Vídeos",
            icone="🎬",
            comando=self.abrir_videos
        )

        self.botao_exportar = self._adicionar_botao_menu(
            texto="Exportar",
            icone="📤",
            comando=self.abrir_exportacao
        )

        self._adicionar_separador()

    def _criar_secao_estudio(self):
        self._adicionar_titulo_secao(
            "ESTÚDIO"
        )

        self.botao_editor_thumbnail = self._adicionar_botao_menu(
            texto="Editor de Thumbnail",
            icone="🎨",
            comando=self.abrir_editor_thumbnail
        )

        self._adicionar_botao_indisponivel(
            texto="Templates",
            icone="🧩"
        )

        self._adicionar_botao_indisponivel(
            texto="Banco de imagens",
            icone="🖼️"
        )

        self._adicionar_separador()

    def _criar_secao_publicacao(self):
        self._adicionar_titulo_secao(
            "YOUTUBE"
        )

        self.botao_publicacao = self._adicionar_botao_menu(
            texto="Publicação",
            icone="🚀",
            comando=self.abrir_publicacao
        )

        self._adicionar_separador()

    def _criar_secao_sistema(self):
        self._adicionar_titulo_secao(
            "SISTEMA"
        )

        self.botao_configuracoes = self._adicionar_botao_menu(
            texto="Configurações",
            icone="⚙️",
            comando=self.abrir_configuracoes
        )

    def _criar_rodape_menu(self):
        rodape = ctk.CTkFrame(
            self.menu,
            fg_color=self.COR_MENU_SECUNDARIA,
            corner_radius=0
        )

        rodape.grid(
            row=2,
            column=0,
            sticky="ew"
        )

        ctk.CTkLabel(
            rodape,
            text="Moleza Quiz Studio",
            font=("Arial", 11, "bold"),
            text_color=self.COR_TEXTO_SECUNDARIO
        ).pack(
            pady=(10, 2)
        )

        ctk.CTkLabel(
            rodape,
            text="Desenvolvimento em andamento",
            font=("Arial", 10),
            text_color="#727887"
        ).pack(
            pady=(0, 10)
        )

    def _adicionar_titulo_secao(self, texto):
        ctk.CTkLabel(
            self.menu_rolavel,
            text=texto,
            font=("Arial", 11, "bold"),
            text_color=self.COR_TEXTO_SECUNDARIO,
            anchor="w"
        ).pack(
            fill="x",
            padx=10,
            pady=(12, 6)
        )

    def _adicionar_botao_menu(
        self,
        texto,
        icone,
        comando
    ):
        botao = ctk.CTkButton(
            self.menu_rolavel,
            text=f"{icone}  {texto}",
            height=42,
            corner_radius=9,
            anchor="w",
            font=("Arial", 13, "bold"),
            fg_color=self.COR_BOTAO,
            hover_color=self.COR_BOTAO_HOVER,
            command=lambda: self._executar_navegacao(
                botao,
                comando
            )
        )

        botao.pack(
            fill="x",
            padx=4,
            pady=4
        )

        self.botoes_menu.append(
            botao
        )

        return botao

    def _adicionar_botao_indisponivel(
        self,
        texto,
        icone
    ):
        botao = ctk.CTkButton(
            self.menu_rolavel,
            text=f"{icone}  {texto}",
            height=40,
            corner_radius=9,
            anchor="w",
            font=("Arial", 12),
            fg_color="#242832",
            hover_color="#242832",
            text_color="#747A88",
            state="disabled"
        )

        botao.pack(
            fill="x",
            padx=4,
            pady=4
        )

        return botao

    def _adicionar_separador(self):
        separador = ctk.CTkFrame(
            self.menu_rolavel,
            height=1,
            fg_color=self.COR_SEPARADOR
        )

        separador.pack(
            fill="x",
            padx=10,
            pady=(14, 4)
        )

    def _executar_navegacao(
        self,
        botao,
        comando
    ):
        self._destacar_botao(
            botao
        )

        comando()

    def _destacar_botao(
        self,
        botao
    ):
        for item in self.botoes_menu:
            item.configure(
                fg_color=self.COR_BOTAO,
                hover_color=self.COR_BOTAO_HOVER
            )

        if botao is not None:
            botao.configure(
                fg_color=self.COR_BOTAO_ATIVO,
                hover_color=self.COR_BOTAO_ATIVO_HOVER
            )

        self.botao_ativo = botao

    # =========================================================
    # ÁREA PRINCIPAL
    # =========================================================

    def _criar_area_principal(self):
        self.conteudo = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color="#10131A"
        )

        self.conteudo.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

    def limpar_conteudo(self):
        for widget in self.conteudo.winfo_children():
            widget.destroy()

    def _abrir_pagina(
        self,
        classe_pagina
    ):
        self.limpar_conteudo()

        pagina = classe_pagina(
            self.conteudo
        )

        pagina.pack(
            fill="both",
            expand=True
        )

    # =========================================================
    # NAVEGAÇÃO
    # =========================================================

    def abrir_criador_quiz(self):
        self._destacar_botao(
            self.botao_criar_quiz
        )

        self._abrir_pagina(
            QuizPage
        )

    def abrir_projetos(self):
        self._destacar_botao(
            self.botao_projetos
        )

        self._abrir_pagina(
            ProjectsPage
        )

    def abrir_narracao(self):
        self._destacar_botao(
            self.botao_narracao
        )

        self._abrir_pagina(
            NarrationPage
        )

    def abrir_videos(self):
        self._destacar_botao(
            self.botao_videos
        )

        self._abrir_pagina(
            VideoPage
        )

    def abrir_exportacao(self):
        self._destacar_botao(
            self.botao_exportar
        )

        self._abrir_pagina(
            ExportPage
        )

    def abrir_editor_thumbnail(self):
        self._destacar_botao(
            self.botao_editor_thumbnail
        )

        self._abrir_pagina(
            ThumbnailEditorPage
        )

    def abrir_publicacao(self):
        self._destacar_botao(
            self.botao_publicacao
        )

        self._abrir_pagina(
            PublicationPage
        )

    def abrir_configuracoes(self):
        self._destacar_botao(
            self.botao_configuracoes
        )

        self._abrir_pagina(
            SettingsPage
        )
