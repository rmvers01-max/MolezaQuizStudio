import customtkinter as ctk

from core.quiz_generator import QuizGenerator


class QuizPage(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.generator = QuizGenerator()

        self.criar_interface()

    def criar_interface(self):

        # Permite que as colunas acompanhem o tamanho da janela
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Título da página
        titulo = ctk.CTkLabel(
            self,
            text="Criar Quiz",
            font=("Arial", 28, "bold")
        )
        titulo.grid(
            row=0,
            column=0,
            columnspan=2,
            pady=(25, 20)
        )

        # Painel de configurações
        painel_configuracoes = ctk.CTkFrame(self)
        painel_configuracoes.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=(20, 10),
            pady=(0, 20)
        )

        ctk.CTkLabel(
            painel_configuracoes,
            text="Configurações do Quiz",
            font=("Arial", 22, "bold")
        ).pack(pady=(25, 20))

        ctk.CTkLabel(
            painel_configuracoes,
            text="Tema"
        ).pack(anchor="w", padx=30)

        self.tema = ctk.CTkEntry(
            painel_configuracoes,
            width=350,
            placeholder_text="Ex.: Animais, futebol, Bíblia..."
        )
        self.tema.pack(padx=30, pady=(5, 15))

        ctk.CTkLabel(
            painel_configuracoes,
            text="Quantidade de perguntas"
        ).pack(anchor="w", padx=30)

        self.quantidade = ctk.CTkEntry(
            painel_configuracoes,
            width=120
        )
        self.quantidade.insert(0, "10")
        self.quantidade.pack(padx=30, pady=(5, 15))

        ctk.CTkLabel(
            painel_configuracoes,
            text="Tempo por pergunta"
        ).pack(anchor="w", padx=30)

        self.tempo = ctk.CTkEntry(
            painel_configuracoes,
            width=120
        )
        self.tempo.insert(0, "5")
        self.tempo.pack(padx=30, pady=(5, 15))

        self.botao_gerar = ctk.CTkButton(
            painel_configuracoes,
            text="GERAR QUIZ",
            width=220,
            height=45,
            command=self.gerar_quiz
        )
        self.botao_gerar.pack(pady=25)

        self.status = ctk.CTkLabel(
            painel_configuracoes,
            text="Preencha os dados e clique em Gerar Quiz."
        )
        self.status.pack(pady=(0, 20))

        # Painel de prévia
        painel_previa = ctk.CTkFrame(self)
        painel_previa.grid(
            row=1,
            column=1,
            sticky="nsew",
            padx=(10, 20),
            pady=(0, 20)
        )

        ctk.CTkLabel(
            painel_previa,
            text="Prévia",
            font=("Arial", 22, "bold")
        ).pack(pady=(25, 15))

        self.caixa = ctk.CTkTextbox(
            painel_previa,
            width=420,
            height=550
        )
        self.caixa.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20)
        )

        self.caixa.insert(
            "0.0",
            "As perguntas do quiz aparecerão aqui."
        )

    def gerar_quiz(self):

        tema = self.tema.get().strip()
        quantidade_texto = self.quantidade.get().strip()

        if not tema:
            self.status.configure(
                text="Informe um tema para o quiz."
            )
            return

        try:
            quantidade = int(quantidade_texto)

            if quantidade < 1 or quantidade > 100:
                raise ValueError

        except ValueError:
            self.status.configure(
                text="A quantidade deve ser um número entre 1 e 100."
            )
            return

        try:
            self.status.configure(text="Gerando quiz...")
            self.update_idletasks()

            perguntas = self.generator.gerar_quiz(
                tema,
                quantidade
            )

            self.caixa.delete("0.0", "end")

            for numero, pergunta in enumerate(perguntas, start=1):

                texto = (
                    f"{numero}. {pergunta['pergunta']}\n"
                    f"Resposta: {pergunta['resposta']}\n\n"
                )

                self.caixa.insert("end", texto)

            self.status.configure(
                text=f"{len(perguntas)} perguntas geradas e salvas."
            )

        except Exception as erro:
            self.status.configure(
                text=f"Erro ao gerar o quiz: {erro}"
            )
