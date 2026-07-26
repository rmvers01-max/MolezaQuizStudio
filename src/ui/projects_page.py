import customtkinter as ctk

from core.project_manager import ProjectManager


class ProjectsPage(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.project_manager = ProjectManager()

        self.criar_interface()
        self.atualizar_lista()

    def criar_interface(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        cabecalho = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        cabecalho.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=25,
            pady=(25, 15)
        )

        cabecalho.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            cabecalho,
            text="Projetos",
            font=("Arial", 28, "bold")
        ).grid(
            row=0,
            column=0,
            sticky="w"
        )

        ctk.CTkButton(
            cabecalho,
            text="Atualizar",
            width=110,
            command=self.atualizar_lista
        ).grid(
            row=0,
            column=1
        )

        self.lista = ctk.CTkScrollableFrame(self)
        self.lista.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=25,
            pady=(0, 25)
        )

        self.lista.grid_columnconfigure(0, weight=1)

    def atualizar_lista(self):
        for widget in self.lista.winfo_children():
            widget.destroy()

        projetos = self.project_manager.listar_projetos()

        if not projetos:
            ctk.CTkLabel(
                self.lista,
                text="Nenhum projeto encontrado.",
                font=("Arial", 18)
            ).grid(
                row=0,
                column=0,
                padx=20,
                pady=40
            )
            return

        for indice, pasta_projeto in enumerate(projetos):
            perguntas = self.project_manager.carregar_quiz(
                pasta_projeto
            )

            cartao = ctk.CTkFrame(self.lista)
            cartao.grid(
                row=indice,
                column=0,
                sticky="ew",
                padx=10,
                pady=8
            )

            cartao.grid_columnconfigure(0, weight=1)

            nome = ctk.CTkLabel(
                cartao,
                text=pasta_projeto.name,
                font=("Arial", 18, "bold")
            )
            nome.grid(
                row=0,
                column=0,
                sticky="w",
                padx=20,
                pady=(15, 3)
            )

            detalhes = ctk.CTkLabel(
                cartao,
                text=f"{len(perguntas)} perguntas",
                text_color="gray70"
            )
            detalhes.grid(
                row=1,
                column=0,
                sticky="w",
                padx=20,
                pady=(0, 15)
            )

            ctk.CTkButton(
                cartao,
                text="Visualizar",
                width=110,
                command=lambda pasta=pasta_projeto: (
                    self.visualizar_projeto(pasta)
                )
            ).grid(
                row=0,
                column=1,
                rowspan=2,
                padx=20,
                pady=15
            )

    def visualizar_projeto(self, pasta_projeto):
        perguntas = self.project_manager.carregar_quiz(
            pasta_projeto
        )

        janela = ctk.CTkToplevel(self)
        janela.title(f"Projeto — {pasta_projeto.name}")
        janela.geometry("750x600")
        janela.transient(self.winfo_toplevel())
        janela.grab_set()

        ctk.CTkLabel(
            janela,
            text=pasta_projeto.name,
            font=("Arial", 25, "bold")
        ).pack(pady=(25, 10))

        ctk.CTkLabel(
            janela,
            text=f"{len(perguntas)} perguntas"
        ).pack(pady=(0, 15))

        caixa = ctk.CTkTextbox(
            janela,
            width=680,
            height=450
        )
        caixa.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(0, 25)
        )

        if not perguntas:
            caixa.insert(
                "0.0",
                "Este projeto não possui perguntas salvas."
            )
            return

        for numero, pergunta in enumerate(perguntas, start=1):
            texto_pergunta = pergunta.get(
                "pergunta",
                "Pergunta sem texto"
            )

            resposta = pergunta.get(
                "resposta",
                "Resposta não informada"
            )

            caixa.insert(
                "end",
                (
                    f"{numero}. {texto_pergunta}\n"
                    f"Resposta: {resposta}\n\n"
                )
            )
