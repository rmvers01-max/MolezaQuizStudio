import customtkinter as ctk

from ui.quiz_page import QuizPage


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class MainWindow(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Moleza Quiz Studio")
        self.geometry("1400x800")
        self.minsize(1000, 650)

        self.criar_interface()

    def criar_interface(self):

        # Menu lateral
        self.menu = ctk.CTkFrame(
            self,
            width=220,
            corner_radius=0
        )
        self.menu.pack(
            side="left",
            fill="y"
        )

        self.menu.pack_propagate(False)

        ctk.CTkLabel(
            self.menu,
            text="🦥\nMOLEZA QUIZ",
            font=("Arial", 25, "bold")
        ).pack(pady=(35, 30))

        ctk.CTkButton(
            self.menu,
            text="Criar Quiz",
            width=180,
            height=40,
            command=self.abrir_criador_quiz
        ).pack(pady=6)

        ctk.CTkButton(
            self.menu,
            text="Projetos",
            width=180,
            height=40,
            command=lambda: self.mostrar_mensagem(
                "Gerenciador de projetos será criado em breve."
            )
        ).pack(pady=6)

        ctk.CTkButton(
            self.menu,
            text="Vídeos",
            width=180,
            height=40,
            command=lambda: self.mostrar_mensagem(
                "O gerador de vídeos será criado nas próximas etapas."
            )
        ).pack(pady=6)

        ctk.CTkButton(
            self.menu,
            text="Exportar",
            width=180,
            height=40,
            command=lambda: self.mostrar_mensagem(
                "A tela de exportação será criada futuramente."
            )
        ).pack(pady=6)

        ctk.CTkButton(
            self.menu,
            text="Configurações",
            width=180,
            height=40,
            command=lambda: self.mostrar_mensagem(
                "A tela de configurações será criada futuramente."
            )
        ).pack(pady=6)

        # Área principal, onde as páginas serão exibidas
        self.conteudo = ctk.CTkFrame(
            self,
            corner_radius=0
        )
        self.conteudo.pack(
            side="left",
            fill="both",
            expand=True
        )

        # Abre a página do quiz ao iniciar
        self.abrir_criador_quiz()

    def limpar_conteudo(self):

        for widget in self.conteudo.winfo_children():
            widget.destroy()

    def abrir_criador_quiz(self):

        self.limpar_conteudo()

        pagina = QuizPage(self.conteudo)
        pagina.pack(
            fill="both",
            expand=True
        )

    def mostrar_mensagem(self, mensagem):

        self.limpar_conteudo()

        painel = ctk.CTkFrame(self.conteudo)
        painel.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=30
        )

        ctk.CTkLabel(
            painel,
            text=mensagem,
            font=("Arial", 22, "bold"),
            wraplength=600
        ).pack(
            expand=True,
            padx=30,
            pady=30
        )
