import customtkinter as ctk

from utils.config import Config


class SettingsPage(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.config = Config()

        self.criar_interface()
        self.carregar_valores()

    def criar_interface(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

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
        ).pack(anchor="w")

        ctk.CTkLabel(
            cabecalho,
            text="Defina os valores padrão usados na criação dos quizzes.",
            text_color="gray70"
        ).pack(
            anchor="w",
            pady=(5, 0)
        )

        # =====================================
        # PAINEL
        # =====================================

        painel = ctk.CTkScrollableFrame(self)

        painel.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=30,
            pady=(0, 30)
        )

        painel.grid_columnconfigure(0, weight=1)

        formulario = ctk.CTkFrame(painel)

        formulario.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=15,
            pady=15
        )

        formulario.grid_columnconfigure(1, weight=1)

        # Quantidade padrão

        ctk.CTkLabel(
            formulario,
            text="Quantidade padrão de perguntas"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=20,
            pady=(25, 10)
        )

        self.quantidade = ctk.CTkEntry(
            formulario,
            width=160
        )

        self.quantidade.grid(
            row=0,
            column=1,
            sticky="w",
            padx=20,
            pady=(25, 10)
        )

        # Tempo

        ctk.CTkLabel(
            formulario,
            text="Tempo por pergunta"
        ).grid(
            row=1,
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
            row=1,
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
            row=2,
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
            row=2,
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
            row=3,
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
            row=3,
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
            row=4,
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
            row=4,
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
            row=5,
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

        self.status = ctk.CTkLabel(
            formulario,
            text=""
        )

        self.status.grid(
            row=6,
            column=0,
            columnspan=2,
            pady=(0, 25)
        )

    def carregar_valores(self):
        self.quantidade.delete(0, "end")
        self.quantidade.insert(
            0,
            str(
                self.config.get(
                    "quantidade_perguntas",
                    10
                )
            )
        )

        self.tempo.delete(0, "end")
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

    def restaurar_padrao(self):
        self.config.restaurar_padrao()
        self.carregar_valores()

        self.status.configure(
            text="Configurações padrão restauradas."
        )
