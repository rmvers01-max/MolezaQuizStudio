import threading

import customtkinter as ctk

from core.project_manager import ProjectManager
from core.video_generator import VideoGenerator


class VideoPage(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.project_manager = ProjectManager()
        self.video_generator = VideoGenerator()

        self.projetos = []

        self.criar_interface()
        self.carregar_projetos()

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
            text="Gerador de Vídeos",
            font=("Arial", 28, "bold")
        ).pack(anchor="w")

        ctk.CTkLabel(
            cabecalho,
            text=(
                "Crie um teste rápido ou renderize "
                "todas as perguntas do projeto."
            ),
            text_color="gray70"
        ).pack(
            anchor="w",
            pady=(5, 0)
        )

        # =====================================
        # PAINEL PRINCIPAL
        # =====================================

        painel = ctk.CTkFrame(self)

        painel.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=30,
            pady=(0, 30)
        )

        ctk.CTkLabel(
            painel,
            text="Selecione o projeto",
            font=("Arial", 20, "bold")
        ).pack(
            pady=(30, 10)
        )

        self.seletor_projeto = ctk.CTkOptionMenu(
            painel,
            values=[
                "Nenhum projeto encontrado"
            ],
            width=350
        )

        self.seletor_projeto.pack(
            pady=10
        )

        ctk.CTkButton(
            painel,
            text="Atualizar projetos",
            width=160,
            command=self.carregar_projetos
        ).pack(
            pady=(0, 18)
        )

        ctk.CTkLabel(
            painel,
            text="Tempo para responder"
        ).pack(
            pady=(5, 5)
        )

        self.tempo = ctk.CTkEntry(
            painel,
            width=120
        )

        self.tempo.insert(
            0,
            "5"
        )

        self.tempo.pack(
            pady=(0, 15)
        )

        ctk.CTkLabel(
            painel,
            text="Modo de geração"
        ).pack(
            pady=(5, 5)
        )

        self.modo = ctk.CTkOptionMenu(
            painel,
            values=[
                "Teste — 3 perguntas",
                "Vídeo completo"
            ],
            width=250
        )

        self.modo.set(
            "Teste — 3 perguntas"
        )

        self.modo.pack(
            pady=(0, 15)
        )

        self.botao_gerar = ctk.CTkButton(
            painel,
            text="GERAR VÍDEO",
            width=250,
            height=45,
            command=self.iniciar_geracao
        )

        self.botao_gerar.pack(
            pady=(20, 15)
        )

        self.progresso = ctk.CTkProgressBar(
            painel,
            width=450,
            mode="determinate"
        )

        self.progresso.pack(
            pady=10
        )

        self.progresso.set(0)

        self.status = ctk.CTkLabel(
            painel,
            text=(
                "Selecione um projeto "
                "para começar."
            ),
            wraplength=700
        )

        self.status.pack(
            padx=20,
            pady=(10, 30)
        )

    def carregar_projetos(self):
        self.projetos = (
            self.project_manager.listar_projetos()
        )

        nomes = [
            projeto.name
            for projeto in self.projetos
        ]

        if not nomes:
            nomes = [
                "Nenhum projeto encontrado"
            ]

        self.seletor_projeto.configure(
            values=nomes
        )

        self.seletor_projeto.set(
            nomes[0]
        )

        self.status.configure(
            text=(
                f"{len(self.projetos)} "
                "projeto(s) encontrado(s)."
            )
        )

    def iniciar_geracao(self):
        if not self.projetos:
            self.status.configure(
                text="Nenhum projeto foi encontrado."
            )
            return

        try:
            tempo = int(
                self.tempo.get().strip()
            )

            if tempo < 1 or tempo > 15:
                raise ValueError

        except ValueError:
            self.status.configure(
                text=(
                    "O tempo deve ser um número "
                    "entre 1 e 15 segundos."
                )
            )
            return

        nome_selecionado = (
            self.seletor_projeto.get()
        )

        pasta_projeto = next(
            (
                projeto
                for projeto in self.projetos
                if projeto.name
                == nome_selecionado
            ),
            None
        )

        if pasta_projeto is None:
            self.status.configure(
                text=(
                    "Não foi possível localizar "
                    "o projeto selecionado."
                )
            )
            return

        perguntas = (
            self.project_manager.carregar_quiz(
                pasta_projeto
            )
        )

        if not perguntas:
            self.status.configure(
                text=(
                    "O projeto não possui "
                    "perguntas."
                )
            )
            return

        if self.modo.get() == "Vídeo completo":
            limite_perguntas = None
        else:
            limite_perguntas = 3

        self.botao_gerar.configure(
            state="disabled",
            text="GERANDO..."
        )

        self.progresso.set(0)

        self.status.configure(
            text="Preparando a geração do vídeo..."
        )

        thread = threading.Thread(
            target=self.gerar_video,
            args=(
                pasta_projeto,
                perguntas,
                tempo,
                limite_perguntas
            ),
            daemon=True
        )

        thread.start()

    def gerar_video(
        self,
        pasta_projeto,
        perguntas,
        tempo,
        limite_perguntas
    ):
        try:
            caminho_video = (
                self.video_generator.gerar_video(
                    pasta_projeto=pasta_projeto,
                    perguntas=perguntas,
                    tempo_resposta=tempo,
                    limite_perguntas=limite_perguntas,
                    callback_progresso=(
                        self.receber_progresso
                    )
                )
            )

            self.after(
                0,
                self.geracao_concluida,
                caminho_video
            )

        except Exception as erro:
            self.after(
                0,
                self.geracao_falhou,
                str(erro)
            )

    def receber_progresso(
        self,
        atual,
        total,
        mensagem
    ):
        self.after(
            0,
            self.atualizar_progresso,
            atual,
            total,
            mensagem
        )

    def atualizar_progresso(
        self,
        atual,
        total,
        mensagem
    ):
        if total > 0:
            percentual = atual / total
        else:
            percentual = 0

        self.progresso.set(
            percentual
        )

        self.status.configure(
            text=mensagem
        )

    def geracao_concluida(
        self,
        caminho_video
    ):
        self.progresso.set(1)

        self.botao_gerar.configure(
            state="normal",
            text="GERAR VÍDEO"
        )

        self.status.configure(
            text=(
                "Vídeo criado com sucesso:\n"
                f"{caminho_video}"
            )
        )

    def geracao_falhou(
        self,
        mensagem
    ):
        self.progresso.set(0)

        self.botao_gerar.configure(
            state="normal",
            text="GERAR VÍDEO"
        )

        self.status.configure(
            text=(
                "Erro ao gerar o vídeo:\n"
                f"{mensagem}"
            )
        )
