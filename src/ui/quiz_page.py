import customtkinter as ctk

from core.quiz_generator import QuizGenerator
from utils.config import Config
from ui.question_editor import QuestionEditorWindow


class QuizPage(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.generator = QuizGenerator()
        self.config = Config()

        self.criar_interface()
        self.carregar_valores_padrao()

    def criar_interface(self):
        self.grid_columnconfigure(
            0,
            weight=1
        )

        self.grid_columnconfigure(
            1,
            weight=1
        )

        self.grid_rowconfigure(
            1,
            weight=1
        )

        # =====================================
        # CABEÇALHO
        # =====================================

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

        # =====================================
        # PAINEL DE CONFIGURAÇÕES
        # =====================================

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
        ).pack(
            pady=(25, 20)
        )

        # Tema

        ctk.CTkLabel(
            painel_configuracoes,
            text="Tema"
        ).pack(
            anchor="w",
            padx=30
        )

        self.tema = ctk.CTkEntry(
            painel_configuracoes,
            width=350,
            placeholder_text=(
                "Ex.: Animais, futebol, Bíblia..."
            )
        )

        self.tema.pack(
            padx=30,
            pady=(5, 15)
        )

        # Quantidade

        ctk.CTkLabel(
            painel_configuracoes,
            text="Quantidade de perguntas"
        ).pack(
            anchor="w",
            padx=30
        )

        self.quantidade = ctk.CTkEntry(
            painel_configuracoes,
            width=120
        )

        self.quantidade.pack(
            padx=30,
            pady=(5, 15)
        )

        # Tempo

        ctk.CTkLabel(
            painel_configuracoes,
            text="Tempo por pergunta"
        ).pack(
            anchor="w",
            padx=30
        )

        self.tempo = ctk.CTkEntry(
            painel_configuracoes,
            width=120
        )

        self.tempo.pack(
            padx=30,
            pady=(5, 15)
        )

        # Botão

        self.botao_gerar = ctk.CTkButton(
            painel_configuracoes,
            text="GERAR QUIZ",
            width=220,
            height=45,
            command=self.gerar_quiz
        )

        self.botao_gerar.pack(
            pady=(20, 10)
        )

        self.botao_editor = ctk.CTkButton(
            painel_configuracoes,
            text="ABRIR EDITOR DE PERGUNTAS",
            width=260,
            height=42,
            fg_color="#6C4BC2",
            hover_color="#563A9E",
            command=self.abrir_editor_perguntas
        )

        self.botao_editor.pack(
            pady=(0, 15)
        )

        # Status

        self.status = ctk.CTkLabel(
            painel_configuracoes,
            text=(
                "Preencha os dados e clique em "
                "Gerar Quiz."
            ),
            wraplength=350
        )

        self.status.pack(
            padx=20,
            pady=(0, 20)
        )

        # =====================================
        # PAINEL DE PRÉVIA
        # =====================================

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
        ).pack(
            pady=(25, 15)
        )

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

    def carregar_valores_padrao(self):
        quantidade_padrao = self.config.get(
            "quantidade_perguntas",
            10
        )

        tempo_padrao = self.config.get(
            "tempo_pergunta",
            5
        )

        self.quantidade.delete(
            0,
            "end"
        )

        self.quantidade.insert(
            0,
            str(quantidade_padrao)
        )

        self.tempo.delete(
            0,
            "end"
        )

        self.tempo.insert(
            0,
            str(tempo_padrao)
        )

    def gerar_quiz(self):
        tema = self.tema.get().strip()

        quantidade_texto = (
            self.quantidade.get().strip()
        )

        tempo_texto = (
            self.tempo.get().strip()
        )

        if not tema:
            self.status.configure(
                text="Informe um tema para o quiz."
            )
            return

        try:
            quantidade = int(
                quantidade_texto
            )

            if quantidade < 1 or quantidade > 100:
                raise ValueError(
                    "A quantidade deve ficar entre "
                    "1 e 100."
                )

            tempo = int(
                tempo_texto
            )

            if tempo < 1 or tempo > 60:
                raise ValueError(
                    "O tempo deve ficar entre "
                    "1 e 60 segundos."
                )

        except ValueError as erro:
            self.status.configure(
                text=f"Erro: {erro}"
            )
            return

        try:
            self.botao_gerar.configure(
                state="disabled",
                text="GERANDO..."
            )

            self.status.configure(
                text="Gerando e salvando o quiz..."
            )

            self.update_idletasks()

            perguntas = self.generator.gerar_quiz(
                tema=tema,
                quantidade=quantidade,
                tempo_pergunta=tempo
            )

            self.mostrar_perguntas(
                perguntas
            )

            self.status.configure(
                text=(
                    f"{len(perguntas)} perguntas "
                    "geradas e salvas com sucesso."
                )
            )

        except Exception as erro:
            self.status.configure(
                text=f"Erro ao gerar o quiz: {erro}"
            )

        finally:
            self.botao_gerar.configure(
                state="normal",
                text="GERAR QUIZ"
            )

    def abrir_editor_perguntas(self):
        QuestionEditorWindow(
            self.winfo_toplevel()
        )

    def mostrar_perguntas(self, perguntas):
        self.caixa.delete(
            "0.0",
            "end"
        )

        if not perguntas:
            self.caixa.insert(
                "0.0",
                "Nenhuma pergunta foi gerada."
            )
            return

        for numero, pergunta in enumerate(
            perguntas,
            start=1
        ):
            texto_pergunta = pergunta.get(
                "pergunta",
                "Pergunta sem texto"
            )

            resposta = pergunta.get(
                "resposta",
                "Resposta não informada"
            )

            alternativas = pergunta.get(
                "alternativas",
                []
            )

            self.caixa.insert(
                "end",
                f"{numero}. {texto_pergunta}\n"
            )

            for indice, alternativa in enumerate(
                alternativas
            ):
                letra = chr(
                    65 + indice
                )

                self.caixa.insert(
                    "end",
                    f"{letra}) {alternativa}\n"
                )

            self.caixa.insert(
                "end",
                f"Resposta: {resposta}\n\n"
            )
