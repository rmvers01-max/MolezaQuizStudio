import os
from pathlib import Path
import threading

import customtkinter as ctk

from core.audio_generator import AudioGenerator
from core.project_manager import ProjectManager


class NarrationPage(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.project_manager = ProjectManager()
        self.audio_generator = AudioGenerator()

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
            text="Narração automática",
            font=("Arial", 28, "bold")
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            cabecalho,
            text=(
                "Gere arquivos de áudio para "
                "as perguntas e respostas do quiz."
            ),
            text_color="gray70"
        ).pack(
            anchor="w",
            pady=(5, 0)
        )

        # =====================================
        # PAINEL
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

        ctk.CTkLabel(
            painel,
            text="Selecione o projeto",
            font=("Arial", 20, "bold")
        ).pack(
            pady=(35, 10)
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
            pady=(0, 25)
        )

        # =====================================
        # VOZ
        # =====================================

        ctk.CTkLabel(
            painel,
            text="Voz da narração",
            font=("Arial", 18, "bold")
        ).pack(
            pady=(5, 8)
        )

        self.seletor_voz = ctk.CTkOptionMenu(
            painel,
            values=list(
                AudioGenerator.VOZES.keys()
            ),
            width=300
        )

        self.seletor_voz.set(
            "Francisca — Feminina"
        )

        self.seletor_voz.pack(
            pady=(0, 20)
        )

        # =====================================
        # VELOCIDADE
        # =====================================

        self.texto_velocidade = ctk.CTkLabel(
            painel,
            text="Velocidade da voz: 0%"
        )

        self.texto_velocidade.pack(
            pady=(5, 5)
        )

        self.velocidade = ctk.CTkSlider(
            painel,
            from_=-30,
            to=30,
            number_of_steps=60,
            width=350,
            command=self.atualizar_velocidade
        )

        self.velocidade.set(0)

        self.velocidade.pack(
            pady=(0, 25)
        )

        # =====================================
        # GERAR
        # =====================================

        self.botao_gerar = ctk.CTkButton(
            painel,
            text="GERAR NARRAÇÕES",
            width=240,
            height=45,
            command=self.iniciar_geracao
        )

        self.botao_gerar.pack(
            pady=(10, 15)
        )

        self.progresso = ctk.CTkProgressBar(
            painel,
            width=450,
            mode="determinate"
        )

        self.progresso.set(0)

        self.progresso.pack(
            pady=10
        )

        self.status = ctk.CTkLabel(
            painel,
            text=(
                "Selecione um projeto "
                "para começar."
            ),
            wraplength=650
        )

        self.status.pack(
            padx=20,
            pady=(10, 15)
        )

        self.botao_abrir_pasta = ctk.CTkButton(
            painel,
            text="Abrir pasta de áudios",
            width=200,
            state="disabled",
            command=self.abrir_pasta_audios
        )

        self.botao_abrir_pasta.pack(
            pady=(0, 30)
        )

    def carregar_projetos(self):
        nome_atual = (
            self.seletor_projeto.get()
            if hasattr(
                self,
                "seletor_projeto"
            )
            else ""
        )

        self.projetos = (
            self.project_manager
            .listar_projetos()
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

        if nome_atual in nomes:
            self.seletor_projeto.set(
                nome_atual
            )
        else:
            self.seletor_projeto.set(
                nomes[0]
            )

        self.status.configure(
            text=(
                f"{len(self.projetos)} "
                "projeto(s) encontrado(s)."
            )
        )

    def atualizar_velocidade(
        self,
        valor
    ):
        velocidade = int(
            round(valor)
        )

        sinal = (
            "+"
            if velocidade > 0
            else ""
        )

        self.texto_velocidade.configure(
            text=(
                "Velocidade da voz: "
                f"{sinal}{velocidade}%"
            )
        )

    def iniciar_geracao(self):
        if not self.projetos:
            self.status.configure(
                text=(
                    "Nenhum projeto "
                    "foi encontrado."
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
            self.project_manager
            .carregar_quiz(
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

        velocidade_numero = int(
            round(
                self.velocidade.get()
            )
        )

        velocidade = (
            f"{velocidade_numero:+d}%"
        )

        voz = self.seletor_voz.get()

        self.botao_gerar.configure(
            state="disabled",
            text="GERANDO..."
        )

        self.botao_abrir_pasta.configure(
            state="disabled"
        )

        self.progresso.set(0)

        self.status.configure(
            text=(
                "Iniciando a geração "
                "das narrações..."
            )
        )

        thread = threading.Thread(
            target=self.gerar_narracoes,
            args=(
                pasta_projeto,
                perguntas,
                voz,
                velocidade
            ),
            daemon=True
        )

        thread.start()

    def gerar_narracoes(
        self,
        pasta_projeto,
        perguntas,
        voz,
        velocidade
    ):
        try:
            pasta_audios = (
                self.audio_generator
                .gerar_narracoes(
                    pasta_projeto=(
                        pasta_projeto
                    ),
                    perguntas=perguntas,
                    nome_voz=voz,
                    velocidade=velocidade,
                    callback_progresso=(
                        self.receber_progresso
                    )
                )
            )

            self.after(
                0,
                self.geracao_concluida,
                pasta_audios
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
        percentual = (
            atual / total
            if total > 0
            else 0
        )

        self.progresso.set(
            percentual
        )

        self.status.configure(
            text=mensagem
        )

    def geracao_concluida(
        self,
        pasta_audios
    ):
        self.progresso.set(1)

        self.botao_gerar.configure(
            state="normal",
            text="GERAR NARRAÇÕES"
        )

        self.botao_abrir_pasta.configure(
            state="normal"
        )

        self.status.configure(
            text=(
                "Narrações criadas com sucesso:\n"
                f"{pasta_audios}"
            )
        )

    def geracao_falhou(
        self,
        mensagem
    ):
        self.progresso.set(0)

        self.botao_gerar.configure(
            state="normal",
            text="GERAR NARRAÇÕES"
        )

        self.status.configure(
            text=(
                "Erro ao gerar as narrações:\n"
                f"{mensagem}"
            )
        )

    def abrir_pasta_audios(self):
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
            return

        pasta_audios = (
            Path(pasta_projeto)
            / "audios"
        )

        if not pasta_audios.exists():
            self.status.configure(
                text=(
                    "A pasta de áudios "
                    "não foi encontrada."
                )
            )
            return

        try:
            os.startfile(
                str(pasta_audios)
            )

        except OSError as erro:
            self.status.configure(
                text=(
                    "Não foi possível abrir "
                    f"a pasta: {erro}"
                )
            )
