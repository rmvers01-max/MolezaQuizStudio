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

        # =====================================
        # LISTA DE PROJETOS
        # =====================================

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

            configuracao = (
                self.project_manager
                .carregar_configuracao_projeto(
                    pasta_projeto
                )
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

            ctk.CTkLabel(
                cartao,
                text=pasta_projeto.name,
                font=("Arial", 18, "bold")
            ).grid(
                row=0,
                column=0,
                sticky="w",
                padx=20,
                pady=(15, 3)
            )

            tempo = configuracao.get(
                "tempo_pergunta",
                "não informado"
            )

            detalhes = (
                f"{len(perguntas)} perguntas"
                f"  •  {tempo} segundos por pergunta"
            )

            ctk.CTkLabel(
                cartao,
                text=detalhes,
                text_color="gray70"
            ).grid(
                row=1,
                column=0,
                sticky="w",
                padx=20,
                pady=(0, 15)
            )

            ctk.CTkButton(
                cartao,
                text="Editar",
                width=110,
                command=lambda pasta=pasta_projeto: (
                    self.abrir_editor(pasta)
                )
            ).grid(
                row=0,
                column=1,
                rowspan=2,
                padx=20,
                pady=15
            )

    def abrir_editor(self, pasta_projeto):

        perguntas = self.project_manager.carregar_quiz(
            pasta_projeto
        )

        EditorProjeto(
            master=self,
            pasta_projeto=pasta_projeto,
            perguntas=perguntas,
            project_manager=self.project_manager,
            ao_salvar=self.atualizar_lista
        )


class EditorProjeto(ctk.CTkToplevel):

    def __init__(
        self,
        master,
        pasta_projeto,
        perguntas,
        project_manager,
        ao_salvar
    ):
        super().__init__(master)

        self.pasta_projeto = pasta_projeto
        self.perguntas = perguntas
        self.project_manager = project_manager
        self.ao_salvar = ao_salvar

        self.indice_atual = 0

        self.title(
            f"Editar projeto — {pasta_projeto.name}"
        )

        self.geometry("900x720")
        self.minsize(760, 620)

        self.transient(master.winfo_toplevel())
        self.grab_set()

        self.criar_interface()

        if not self.perguntas:
            self.adicionar_pergunta()
        else:
            self.mostrar_pergunta_atual()

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
            padx=25,
            pady=(20, 10)
        )

        cabecalho.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            cabecalho,
            text=self.pasta_projeto.name,
            font=("Arial", 25, "bold")
        ).grid(
            row=0,
            column=0,
            sticky="w"
        )

        self.contador = ctk.CTkLabel(
            cabecalho,
            text=""
        )

        self.contador.grid(
            row=0,
            column=1,
            sticky="e"
        )

        # =====================================
        # FORMULÁRIO
        # =====================================

        formulario = ctk.CTkScrollableFrame(self)

        formulario.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=25,
            pady=10
        )

        formulario.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            formulario,
            text="Pergunta"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=20,
            pady=(20, 5)
        )

        self.campo_pergunta = ctk.CTkTextbox(
            formulario,
            height=100
        )

        self.campo_pergunta.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=20,
            pady=(0, 15)
        )

        self.campos_alternativas = []

        letras = ["A", "B", "C", "D"]

        for indice, letra in enumerate(letras):

            linha = 2 + (indice * 2)

            ctk.CTkLabel(
                formulario,
                text=f"Alternativa {letra}"
            ).grid(
                row=linha,
                column=0,
                sticky="w",
                padx=20,
                pady=(5, 5)
            )

            campo = ctk.CTkEntry(formulario)

            campo.grid(
                row=linha + 1,
                column=0,
                sticky="ew",
                padx=20,
                pady=(0, 10)
            )

            self.campos_alternativas.append(campo)

        ctk.CTkLabel(
            formulario,
            text="Resposta correta"
        ).grid(
            row=10,
            column=0,
            sticky="w",
            padx=20,
            pady=(10, 5)
        )

        self.campo_resposta = ctk.CTkEntry(
            formulario,
            placeholder_text=(
                "Ex.: Leão, alternativa B ou 2"
            )
        )

        self.campo_resposta.grid(
            row=11,
            column=0,
            sticky="ew",
            padx=20,
            pady=(0, 20)
        )

        # =====================================
        # NAVEGAÇÃO
        # =====================================

        navegacao = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        navegacao.grid(
            row=2,
            column=0,
            pady=(5, 10)
        )

        self.botao_anterior = ctk.CTkButton(
            navegacao,
            text="← Anterior",
            width=130,
            command=self.pergunta_anterior
        )

        self.botao_anterior.pack(
            side="left",
            padx=5
        )

        self.botao_proxima = ctk.CTkButton(
            navegacao,
            text="Próxima →",
            width=130,
            command=self.proxima_pergunta
        )

        self.botao_proxima.pack(
            side="left",
            padx=5
        )

        # =====================================
        # AÇÕES
        # =====================================

        acoes = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        acoes.grid(
            row=3,
            column=0,
            pady=(0, 10)
        )

        ctk.CTkButton(
            acoes,
            text="Adicionar pergunta",
            width=160,
            command=self.adicionar_pergunta
        ).pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            acoes,
            text="Excluir pergunta",
            width=150,
            fg_color="#A33A3A",
            hover_color="#7F2D2D",
            command=self.excluir_pergunta
        ).pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            acoes,
            text="Salvar projeto",
            width=160,
            command=self.salvar_projeto
        ).pack(
            side="left",
            padx=5
        )

        self.status = ctk.CTkLabel(
            self,
            text=""
        )

        self.status.grid(
            row=4,
            column=0,
            pady=(0, 15)
        )

    def mostrar_pergunta_atual(self):

        if not self.perguntas:
            return

        pergunta = self.perguntas[
            self.indice_atual
        ]

        self.campo_pergunta.delete(
            "0.0",
            "end"
        )

        self.campo_pergunta.insert(
            "0.0",
            pergunta.get(
                "pergunta",
                ""
            )
        )

        alternativas = pergunta.get(
            "alternativas",
            []
        )

        for indice, campo in enumerate(
            self.campos_alternativas
        ):
            campo.delete(
                0,
                "end"
            )

            if indice < len(alternativas):
                campo.insert(
                    0,
                    str(alternativas[indice])
                )

        self.campo_resposta.delete(
            0,
            "end"
        )

        self.campo_resposta.insert(
            0,
            str(
                pergunta.get(
                    "resposta",
                    ""
                )
            )
        )

        self.atualizar_contador()

    def guardar_pergunta_atual(self):

        if not self.perguntas:
            return

        texto_pergunta = (
            self.campo_pergunta
            .get("0.0", "end")
            .strip()
        )

        alternativas = []

        for campo in self.campos_alternativas:

            alternativa = campo.get().strip()

            if alternativa:
                alternativas.append(alternativa)

        resposta = (
            self.campo_resposta
            .get()
            .strip()
        )

        self.perguntas[
            self.indice_atual
        ] = {
            "pergunta": texto_pergunta,
            "alternativas": alternativas,
            "resposta": resposta
        }

    def atualizar_contador(self):

        total = len(self.perguntas)

        if total == 0:
            texto = "Nenhuma pergunta"
        else:
            texto = (
                f"Pergunta "
                f"{self.indice_atual + 1} "
                f"de {total}"
            )

        self.contador.configure(
            text=texto
        )

        self.botao_anterior.configure(
            state=(
                "normal"
                if self.indice_atual > 0
                else "disabled"
            )
        )

        self.botao_proxima.configure(
            state=(
                "normal"
                if self.indice_atual < total - 1
                else "disabled"
            )
        )

    def pergunta_anterior(self):

        if self.indice_atual <= 0:
            return

        self.guardar_pergunta_atual()

        self.indice_atual -= 1

        self.mostrar_pergunta_atual()

    def proxima_pergunta(self):

        if self.indice_atual >= len(
            self.perguntas
        ) - 1:
            return

        self.guardar_pergunta_atual()

        self.indice_atual += 1

        self.mostrar_pergunta_atual()

    def adicionar_pergunta(self):

        if self.perguntas:
            self.guardar_pergunta_atual()

        nova_pergunta = {
            "pergunta": "",
            "alternativas": [
                "",
                "",
                "",
                ""
            ],
            "resposta": ""
        }

        self.perguntas.append(
            nova_pergunta
        )

        self.indice_atual = (
            len(self.perguntas) - 1
        )

        self.mostrar_pergunta_atual()

        self.status.configure(
            text="Nova pergunta adicionada."
        )

    def excluir_pergunta(self):

        if not self.perguntas:
            return

        self.perguntas.pop(
            self.indice_atual
        )

        if not self.perguntas:
            self.adicionar_pergunta()
            return

        if self.indice_atual >= len(
            self.perguntas
        ):
            self.indice_atual = (
                len(self.perguntas) - 1
            )

        self.mostrar_pergunta_atual()

        self.status.configure(
            text="Pergunta excluída."
        )

    def salvar_projeto(self):

        self.guardar_pergunta_atual()

        perguntas_validas = []

        for pergunta in self.perguntas:

            texto = pergunta.get(
                "pergunta",
                ""
            ).strip()

            if texto:
                perguntas_validas.append(
                    pergunta
                )

        if not perguntas_validas:

            self.status.configure(
                text=(
                    "O projeto precisa ter pelo "
                    "menos uma pergunta preenchida."
                )
            )

            return

        self.perguntas = perguntas_validas

        self.project_manager.salvar_quiz(
            self.pasta_projeto,
            self.perguntas
        )

        self.indice_atual = min(
            self.indice_atual,
            len(self.perguntas) - 1
        )

        self.mostrar_pergunta_atual()

        self.status.configure(
            text="Projeto salvo com sucesso."
        )

        self.ao_salvar()
