import customtkinter as ctk

from ui.export_page import ExportPage
from ui.projects_page import ProjectsPage
from ui.quiz_page import QuizPage
from ui.settings_page import SettingsPage
from ui.video_page import VideoPage


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class MainWindow(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title(
            "Moleza Quiz Studio"
        )

        self.geometry(
            "1400x800"
        )

        self.minsize(
            1000,
            650
        )

        self.criar_interface()

    def criar_interface(self):

        # =====================================
        # MENU LATERAL
        # =====================================

        self.menu = ctk.CTkFrame(
            self,
            width=220,
            corner_radius=0
        )

        self.menu.pack(
            side="left",
            fill="y"
        )

        self.menu.pack_propagate(
            False
        )

        ctk.CTkLabel(
            self.menu,
            text="🦥\nMOLEZA QUIZ",
            font=("Arial", 25, "bold")
        ).pack(
            pady=(35, 30)
        )

        self.botao_criar_quiz = (
            ctk.CTkButton(
                self.menu,
                text="Criar Quiz",
                width=180,
                height=40,
                command=(
                    self.abrir_criador_quiz
                )
            )
        )

        self.botao_criar_quiz.pack(
            pady=6
        )

        self.botao_projetos = (
            ctk.CTkButton(
                self.menu,
                text="Projetos",
                width=180,
                height=40,
                command=(
                    self.abrir_projetos
                )
            )
        )

        self.botao_projetos.pack(
            pady=6
        )

        self.botao_videos = (
            ctk.CTkButton(
                self.menu,
                text="Vídeos",
                width=180,
                height=40,
                command=(
                    self.abrir_videos
                )
            )
        )

        self.botao_videos.pack(
            pady=6
        )

        self.botao_exportar = (
            ctk.CTkButton(
                self.menu,
                text="Exportar",
                width=180,
                height=40,
                command=(
                    self.abrir_exportacao
                )
            )
        )

        self.botao_exportar.pack(
            pady=6
        )

        self.botao_configuracoes = (
            ctk.CTkButton(
                self.menu,
                text="Configurações",
                width=180,
                height=40,
                command=(
                    self.abrir_configuracoes
                )
            )
        )

        self.botao_configuracoes.pack(
            pady=6
        )

        # =====================================
        # ÁREA PRINCIPAL
        # =====================================

        self.conteudo = ctk.CTkFrame(
            self,
            corner_radius=0
        )

        self.conteudo.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.abrir_criador_quiz()

    def limpar_conteudo(self):
        for widget in (
            self.conteudo
            .winfo_children()
        ):
            widget.destroy()

    def abrir_criador_quiz(self):
        self.limpar_conteudo()

        pagina = QuizPage(
            self.conteudo
        )

        pagina.pack(
            fill="both",
            expand=True
        )

    def abrir_projetos(self):
        self.limpar_conteudo()

        pagina = ProjectsPage(
            self.conteudo
        )

        pagina.pack(
            fill="both",
            expand=True
        )

    def abrir_videos(self):
        self.limpar_conteudo()

        pagina = VideoPage(
            self.conteudo
        )

        pagina.pack(
            fill="both",
            expand=True
        )

    def abrir_exportacao(self):
        self.limpar_conteudo()

        pagina = ExportPage(
            self.conteudo
        )

        pagina.pack(
            fill="both",
            expand=True
        )

    def abrir_configuracoes(self):
        self.limpar_conteudo()

        pagina = SettingsPage(
            self.conteudo
        )

        pagina.pack(
            fill="both",
            expand=True
        )
