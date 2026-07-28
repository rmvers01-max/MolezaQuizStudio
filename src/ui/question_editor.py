from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import re
import unicodedata
import shutil
import uuid

import customtkinter as ctk
from PIL import Image, UnidentifiedImageError
from tkinter import filedialog, messagebox

from core.project_manager import ProjectManager
from ui.question_preview import QuestionPreviewGenerator


class QuestionEditorWindow(ctk.CTkToplevel):
    """Janela independente do Editor Visual de Perguntas."""

    def __init__(self, master):
        super().__init__(master)

        self.title("Editor de Perguntas — MolezaQuizStudio")
        self.geometry("1380x820")
        self.minsize(1120, 700)

        self.transient(master)
        self.after(
            100,
            self.lift
        )

        self.editor = QuestionEditor(
            self
        )

        self.editor.pack(
            fill="both",
            expand=True
        )


class QuestionEditor(ctk.CTkFrame):
    """
    Editor visual de quiz.

    Permite selecionar projeto, editar textos, associar imagens,
    reordenar, duplicar, excluir e salvar perguntas no quiz.json.
    """

    TIPOS_QUIZ = [
        "preferencia",
        "conhecimento"
    ]

    def __init__(self, master):
        super().__init__(master)

        self.project_manager = ProjectManager()
        self.preview_generator = QuestionPreviewGenerator()

        self.projetos: dict[str, Path] = {}
        self.pasta_projeto: Path | None = None
        self.perguntas: list[dict] = []
        self.indice_atual: int | None = None

        self.imagem_a_atual: str = ""
        self.imagem_b_atual: str = ""

        self.preview_a_ctk = None
        self.preview_b_ctk = None

        self._criando_interface = True

        self._criar_interface()
        self.carregar_projetos()

        self._criando_interface = False

    # =========================================================
    # INTERFACE
    # =========================================================

    def _criar_interface(self):
        self.grid_columnconfigure(
            1,
            weight=1
        )
        self.grid_rowconfigure(
            1,
            weight=1
        )

        self._criar_cabecalho()
        self._criar_painel_lista()
        self._criar_area_edicao()

    def _criar_cabecalho(self):
        cabecalho = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        cabecalho.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=22,
            pady=(18, 10)
        )

        cabecalho.grid_columnconfigure(
            1,
            weight=1
        )

        ctk.CTkLabel(
            cabecalho,
            text="Editor Visual de Perguntas",
            font=("Arial", 26, "bold")
        ).grid(
            row=0,
            column=0,
            sticky="w"
        )

        self.seletor_projeto = ctk.CTkOptionMenu(
            cabecalho,
            values=["Nenhum projeto encontrado"],
            width=310,
            command=self.ao_selecionar_projeto
        )

        self.seletor_projeto.grid(
            row=0,
            column=1,
            sticky="e",
            padx=(20, 8)
        )

        ctk.CTkButton(
            cabecalho,
            text="Atualizar",
            width=90,
            fg_color="gray35",
            hover_color="gray25",
            command=self.carregar_projetos
        ).grid(
            row=0,
            column=2,
            padx=4
        )

        ctk.CTkButton(
            cabecalho,
            text="AUTOASSOCIAR IMAGENS",
            width=175,
            fg_color="#C56B21",
            hover_color="#9F5419",
            command=self.autoassociar_imagens
        ).grid(
            row=0,
            column=3,
            padx=4
        )

        self.botao_salvar_tudo = ctk.CTkButton(
            cabecalho,
            text="SALVAR QUIZ",
            width=130,
            height=38,
            command=self.salvar_quiz
        )

        self.botao_salvar_tudo.grid(
            row=0,
            column=4,
            padx=(8, 0)
        )

    def _criar_painel_lista(self):
        painel = ctk.CTkFrame(
            self,
            width=300
        )

        painel.grid(
            row=1,
            column=0,
            sticky="ns",
            padx=(22, 8),
            pady=(0, 18)
        )

        painel.grid_propagate(
            False
        )

        painel.grid_columnconfigure(
            0,
            weight=1
        )

        ctk.CTkLabel(
            painel,
            text="Perguntas",
            font=("Arial", 19, "bold")
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=14,
            pady=(16, 8)
        )

        botoes = ctk.CTkFrame(
            painel,
            fg_color="transparent"
        )

        botoes.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=10,
            pady=(0, 8)
        )

        ctk.CTkButton(
            botoes,
            text="+ Nova",
            width=82,
            command=self.adicionar_pergunta
        ).pack(
            side="left",
            padx=3
        )

        ctk.CTkButton(
            botoes,
            text="Duplicar",
            width=82,
            fg_color="gray35",
            hover_color="gray25",
            command=self.duplicar_pergunta
        ).pack(
            side="left",
            padx=3
        )

        ctk.CTkButton(
            botoes,
            text="Excluir",
            width=82,
            fg_color="#A33B45",
            hover_color="#7F2D35",
            command=self.excluir_pergunta
        ).pack(
            side="left",
            padx=3
        )

        self.lista_perguntas = ctk.CTkScrollableFrame(
            painel,
            width=270
        )

        self.lista_perguntas.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=10,
            pady=8
        )

        painel.grid_rowconfigure(
            2,
            weight=1
        )

        mover = ctk.CTkFrame(
            painel,
            fg_color="transparent"
        )

        mover.grid(
            row=3,
            column=0,
            pady=(4, 12)
        )

        ctk.CTkButton(
            mover,
            text="↑ Subir",
            width=110,
            fg_color="gray35",
            hover_color="gray25",
            command=lambda: self.mover_pergunta(-1)
        ).pack(
            side="left",
            padx=4
        )

        ctk.CTkButton(
            mover,
            text="↓ Descer",
            width=110,
            fg_color="gray35",
            hover_color="gray25",
            command=lambda: self.mover_pergunta(1)
        ).pack(
            side="left",
            padx=4
        )

    def _criar_area_edicao(self):
        area = ctk.CTkScrollableFrame(
            self
        )

        area.grid(
            row=1,
            column=1,
            sticky="nsew",
            padx=(8, 22),
            pady=(0, 18)
        )

        area.grid_columnconfigure(
            0,
            weight=1
        )

        self.area_edicao = area

        ctk.CTkLabel(
            area,
            text="Dados da pergunta",
            font=("Arial", 21, "bold")
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=18,
            pady=(18, 10)
        )

        topo = ctk.CTkFrame(
            area
        )

        topo.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=18,
            pady=(0, 10)
        )

        topo.grid_columnconfigure(
            1,
            weight=1
        )

        ctk.CTkLabel(
            topo,
            text="Tipo de quiz"
        ).grid(
            row=0,
            column=0,
            padx=12,
            pady=12
        )

        self.tipo_quiz = ctk.CTkOptionMenu(
            topo,
            values=self.TIPOS_QUIZ,
            width=170
        )

        self.tipo_quiz.grid(
            row=0,
            column=1,
            sticky="w",
            padx=12,
            pady=12
        )

        self.rotulo_numero = ctk.CTkLabel(
            topo,
            text="Nenhuma pergunta selecionada",
            font=("Arial", 16, "bold")
        )

        self.rotulo_numero.grid(
            row=0,
            column=2,
            sticky="e",
            padx=12
        )

        ctk.CTkLabel(
            area,
            text="Pergunta"
        ).grid(
            row=2,
            column=0,
            sticky="w",
            padx=18,
            pady=(8, 4)
        )

        self.campo_pergunta = ctk.CTkTextbox(
            area,
            height=86
        )

        self.campo_pergunta.grid(
            row=3,
            column=0,
            sticky="ew",
            padx=18
        )

        opcoes = ctk.CTkFrame(
            area
        )

        opcoes.grid(
            row=4,
            column=0,
            sticky="ew",
            padx=18,
            pady=14
        )

        opcoes.grid_columnconfigure(
            (0, 1),
            weight=1
        )

        self.campo_a = self._criar_campo_opcao(
            opcoes,
            0,
            0,
            "Alternativa A"
        )

        self.campo_b = self._criar_campo_opcao(
            opcoes,
            0,
            1,
            "Alternativa B"
        )

        self.campo_c = self._criar_campo_opcao(
            opcoes,
            2,
            0,
            "Alternativa C"
        )

        self.campo_d = self._criar_campo_opcao(
            opcoes,
            2,
            1,
            "Alternativa D"
        )

        imagens = ctk.CTkFrame(
            area
        )

        imagens.grid(
            row=5,
            column=0,
            sticky="ew",
            padx=18,
            pady=(0, 14)
        )

        imagens.grid_columnconfigure(
            (0, 1),
            weight=1
        )

        self.preview_a = self._criar_painel_imagem(
            imagens,
            coluna=0,
            titulo="Imagem da alternativa A",
            selecionar=lambda: self.selecionar_imagem("a"),
            remover=lambda: self.remover_imagem("a")
        )

        self.preview_b = self._criar_painel_imagem(
            imagens,
            coluna=1,
            titulo="Imagem da alternativa B",
            selecionar=lambda: self.selecionar_imagem("b"),
            remover=lambda: self.remover_imagem("b")
        )

        detalhes = ctk.CTkFrame(
            area
        )

        detalhes.grid(
            row=6,
            column=0,
            sticky="ew",
            padx=18,
            pady=(0, 14)
        )

        detalhes.grid_columnconfigure(
            1,
            weight=1
        )

        ctk.CTkLabel(
            detalhes,
            text="Resposta"
        ).grid(
            row=0,
            column=0,
            padx=12,
            pady=10,
            sticky="w"
        )

        self.campo_resposta = ctk.CTkEntry(
            detalhes
        )

        self.campo_resposta.grid(
            row=0,
            column=1,
            sticky="ew",
            padx=12,
            pady=10
        )

        ctk.CTkLabel(
            detalhes,
            text="Narração"
        ).grid(
            row=1,
            column=0,
            padx=12,
            pady=10,
            sticky="nw"
        )

        self.campo_narracao = ctk.CTkTextbox(
            detalhes,
            height=90
        )

        self.campo_narracao.grid(
            row=1,
            column=1,
            sticky="ew",
            padx=12,
            pady=10
        )

        botoes = ctk.CTkFrame(
            area,
            fg_color="transparent"
        )

        botoes.grid(
            row=7,
            column=0,
            pady=(0, 10)
        )

        self.botao_aplicar = ctk.CTkButton(
            botoes,
            text="APLICAR ALTERAÇÕES",
            width=220,
            height=42,
            command=self.aplicar_alteracoes
        )

        self.botao_aplicar.pack(
            side="left",
            padx=6
        )

        ctk.CTkButton(
            botoes,
            text="RECARREGAR PERGUNTA",
            width=190,
            height=42,
            fg_color="gray35",
            hover_color="gray25",
            command=self.recarregar_pergunta
        ).pack(
            side="left",
            padx=6
        )

        ctk.CTkButton(
            botoes,
            text="PRÉVIA DO VÍDEO",
            width=170,
            height=42,
            fg_color="#C56B21",
            hover_color="#9F5419",
            command=self.abrir_previa_video
        ).pack(
            side="left",
            padx=6
        )

        self.status = ctk.CTkLabel(
            area,
            text="Selecione um projeto para começar.",
            wraplength=800
        )

        self.status.grid(
            row=8,
            column=0,
            sticky="ew",
            padx=18,
            pady=(5, 20)
        )

        self._definir_estado_editor(
            "disabled"
        )

    def _criar_campo_opcao(
        self,
        master,
        linha,
        coluna,
        titulo
    ):
        ctk.CTkLabel(
            master,
            text=titulo
        ).grid(
            row=linha,
            column=coluna,
            sticky="w",
            padx=12,
            pady=(10, 4)
        )

        campo = ctk.CTkEntry(
            master
        )

        campo.grid(
            row=linha + 1,
            column=coluna,
            sticky="ew",
            padx=12,
            pady=(0, 10)
        )

        return campo

    def _criar_painel_imagem(
        self,
        master,
        coluna,
        titulo,
        selecionar,
        remover
    ):
        painel = ctk.CTkFrame(
            master
        )

        painel.grid(
            row=0,
            column=coluna,
            sticky="nsew",
            padx=8,
            pady=8
        )

        ctk.CTkLabel(
            painel,
            text=titulo,
            font=("Arial", 16, "bold")
        ).pack(
            pady=(12, 8)
        )

        preview = ctk.CTkLabel(
            painel,
            text="Nenhuma imagem",
            width=360,
            height=190,
            fg_color="#22252D",
            corner_radius=14
        )

        preview.pack(
            fill="x",
            padx=12,
            pady=8
        )

        botoes = ctk.CTkFrame(
            painel,
            fg_color="transparent"
        )

        botoes.pack(
            pady=(4, 12)
        )

        ctk.CTkButton(
            botoes,
            text="Selecionar",
            width=110,
            command=selecionar
        ).pack(
            side="left",
            padx=4
        )

        ctk.CTkButton(
            botoes,
            text="Remover",
            width=100,
            fg_color="gray35",
            hover_color="gray25",
            command=remover
        ).pack(
            side="left",
            padx=4
        )

        return preview

    # =========================================================
    # PROJETOS E CARREGAMENTO
    # =========================================================

    def carregar_projetos(self):
        lista = self.project_manager.listar_projetos()

        self.projetos = {
            projeto.name: projeto
            for projeto in lista
        }

        nomes = list(
            self.projetos.keys()
        )

        if not nomes:
            nomes = [
                "Nenhum projeto encontrado"
            ]

        self.seletor_projeto.configure(
            values=nomes
        )

        atual = self.seletor_projeto.get()

        if atual not in nomes:
            atual = nomes[0]
            self.seletor_projeto.set(
                atual
            )

        if atual in self.projetos:
            self.ao_selecionar_projeto(
                atual
            )

    def ao_selecionar_projeto(
        self,
        nome
    ):
        pasta = self.projetos.get(
            nome
        )

        if pasta is None:
            self.pasta_projeto = None
            self.perguntas = []
            self.indice_atual = None
            self.atualizar_lista_perguntas()
            self._definir_estado_editor(
                "disabled"
            )
            return

        self.pasta_projeto = Path(
            pasta
        )

        self.perguntas = (
            self.project_manager
            .carregar_quiz(
                self.pasta_projeto
            )
        )

        self.perguntas = [
            dict(pergunta)
            for pergunta in self.perguntas
            if isinstance(
                pergunta,
                dict
            )
        ]

        self._renumerar_perguntas()
        self.atualizar_lista_perguntas()

        if self.perguntas:
            self.selecionar_pergunta(
                0
            )
        else:
            self.indice_atual = None
            self._limpar_editor()
            self._definir_estado_editor(
                "disabled"
            )
            self.status.configure(
                text=(
                    "O projeto ainda não possui perguntas. "
                    "Clique em + Nova."
                )
            )

    # =========================================================
    # LISTA E NAVEGAÇÃO
    # =========================================================

    def atualizar_lista_perguntas(self):
        for widget in (
            self.lista_perguntas
            .winfo_children()
        ):
            widget.destroy()

        for indice, pergunta in enumerate(
            self.perguntas
        ):
            selecionada = (
                indice
                == self.indice_atual
            )

            texto = str(
                pergunta.get(
                    "pergunta",
                    "Pergunta sem texto"
                )
            ).strip()

            if len(texto) > 34:
                texto = texto[:31] + "..."

            botao = ctk.CTkButton(
                self.lista_perguntas,
                text=(
                    f"{indice + 1}. "
                    f"{texto}"
                ),
                anchor="w",
                height=42,
                fg_color=(
                    "#6C4BC2"
                    if selecionada
                    else "gray30"
                ),
                hover_color="#563A9E",
                command=lambda i=indice: (
                    self.selecionar_pergunta(
                        i
                    )
                )
            )

            botao.pack(
                fill="x",
                padx=4,
                pady=3
            )

    def selecionar_pergunta(
        self,
        indice
    ):
        if not (
            0 <= indice < len(
                self.perguntas
            )
        ):
            return

        if (
            self.indice_atual is not None
            and self.indice_atual != indice
        ):
            self._aplicar_sem_mensagem()

        self.indice_atual = indice
        self._definir_estado_editor(
            "normal"
        )

        pergunta = self.perguntas[
            indice
        ]

        self.tipo_quiz.set(
            str(
                pergunta.get(
                    "tipo_quiz",
                    "conhecimento"
                )
            )
        )

        self._definir_textbox(
            self.campo_pergunta,
            pergunta.get(
                "pergunta",
                ""
            )
        )

        alternativas = pergunta.get(
            "alternativas",
            []
        )

        if not isinstance(
            alternativas,
            list
        ):
            alternativas = []

        campos = [
            self.campo_a,
            self.campo_b,
            self.campo_c,
            self.campo_d
        ]

        for posicao, campo in enumerate(
            campos
        ):
            valor = (
                alternativas[posicao]
                if posicao < len(
                    alternativas
                )
                else ""
            )

            self._definir_entry(
                campo,
                valor
            )

        self._definir_entry(
            self.campo_resposta,
            pergunta.get(
                "resposta",
                ""
            )
        )

        self._definir_textbox(
            self.campo_narracao,
            pergunta.get(
                "narracao",
                ""
            )
        )

        self.imagem_a_atual = str(
            pergunta.get(
                "imagem_a",
                pergunta.get(
                    "imagem_esquerda",
                    ""
                )
            )
            or ""
        )

        self.imagem_b_atual = str(
            pergunta.get(
                "imagem_b",
                pergunta.get(
                    "imagem_direita",
                    ""
                )
            )
            or ""
        )

        self._atualizar_preview_imagem(
            "a"
        )

        self._atualizar_preview_imagem(
            "b"
        )

        self.rotulo_numero.configure(
            text=(
                f"Pergunta {indice + 1} "
                f"de {len(self.perguntas)}"
            )
        )

        self.atualizar_lista_perguntas()

        self.status.configure(
            text=(
                "Edite os campos e clique em "
                "Aplicar alterações."
            )
        )

    # =========================================================
    # EDIÇÃO
    # =========================================================

    def aplicar_alteracoes(self):
        if self._aplicar_sem_mensagem():
            self.atualizar_lista_perguntas()

            self.status.configure(
                text=(
                    "Alterações aplicadas na memória. "
                    "Clique em Salvar Quiz para gravar."
                )
            )

    def _aplicar_sem_mensagem(self):
        if self.indice_atual is None:
            return False

        texto_pergunta = (
            self.campo_pergunta
            .get("1.0", "end")
            .strip()
        )

        if not texto_pergunta:
            return False

        alternativas = [
            campo.get().strip()
            for campo in [
                self.campo_a,
                self.campo_b,
                self.campo_c,
                self.campo_d
            ]
        ]

        alternativas = [
            alternativa
            for alternativa in alternativas
            if alternativa
        ]

        tipo = self.tipo_quiz.get()

        resposta = (
            ""
            if tipo == "preferencia"
            else self.campo_resposta.get().strip()
        )

        pergunta = self.perguntas[
            self.indice_atual
        ]

        pergunta.update({
            "numero": self.indice_atual + 1,
            "tipo_quiz": tipo,
            "pergunta": texto_pergunta,
            "alternativas": alternativas,
            "resposta": resposta,
            "narracao": (
                self.campo_narracao
                .get("1.0", "end")
                .strip()
            ),
            "imagem_a": self.imagem_a_atual,
            "imagem_b": self.imagem_b_atual
        })

        return True

    def recarregar_pergunta(self):
        if self.indice_atual is not None:
            self.selecionar_pergunta(
                self.indice_atual
            )

    def adicionar_pergunta(self):
        tipo = "preferencia"

        if self.perguntas:
            tipo = str(
                self.perguntas[0].get(
                    "tipo_quiz",
                    "conhecimento"
                )
            )

        nova = {
            "numero": len(
                self.perguntas
            ) + 1,
            "tipo_quiz": tipo,
            "pergunta": "Nova pergunta",
            "alternativas": [
                "Alternativa A",
                "Alternativa B"
            ],
            "resposta": (
                ""
                if tipo == "preferencia"
                else "Alternativa A"
            ),
            "narracao": "",
            "imagem_a": "",
            "imagem_b": ""
        }

        self.perguntas.append(
            nova
        )

        self._renumerar_perguntas()
        self.selecionar_pergunta(
            len(self.perguntas) - 1
        )

    def duplicar_pergunta(self):
        if self.indice_atual is None:
            return

        self._aplicar_sem_mensagem()

        copia = deepcopy(
            self.perguntas[
                self.indice_atual
            ]
        )

        copia["pergunta"] = (
            str(
                copia.get(
                    "pergunta",
                    ""
                )
            )
            + " — cópia"
        )

        destino = self.indice_atual + 1

        self.perguntas.insert(
            destino,
            copia
        )

        self._renumerar_perguntas()
        self.selecionar_pergunta(
            destino
        )

    def excluir_pergunta(self):
        if self.indice_atual is None:
            return

        resposta = messagebox.askyesno(
            "Excluir pergunta",
            (
                "Deseja realmente excluir a "
                "pergunta selecionada?"
            ),
            parent=self.winfo_toplevel()
        )

        if not resposta:
            return

        indice = self.indice_atual

        self.perguntas.pop(
            indice
        )

        self._renumerar_perguntas()

        if not self.perguntas:
            self.indice_atual = None
            self._limpar_editor()
            self._definir_estado_editor(
                "disabled"
            )
        else:
            self.indice_atual = min(
                indice,
                len(self.perguntas) - 1
            )

            self.selecionar_pergunta(
                self.indice_atual
            )

        self.atualizar_lista_perguntas()

    def mover_pergunta(
        self,
        direcao
    ):
        if self.indice_atual is None:
            return

        self._aplicar_sem_mensagem()

        destino = (
            self.indice_atual
            + direcao
        )

        if not (
            0 <= destino < len(
                self.perguntas
            )
        ):
            return

        pergunta = self.perguntas.pop(
            self.indice_atual
        )

        self.perguntas.insert(
            destino,
            pergunta
        )

        self.indice_atual = destino
        self._renumerar_perguntas()
        self.selecionar_pergunta(
            destino
        )

    # =========================================================
    # ASSOCIAÇÃO AUTOMÁTICA DE IMAGENS
    # =========================================================

    def autoassociar_imagens(self):
        if self.pasta_projeto is None:
            messagebox.showinfo(
                "Nenhum projeto",
                "Selecione um projeto antes de associar imagens.",
                parent=self.winfo_toplevel()
            )
            return

        self._aplicar_sem_mensagem()

        pasta_padrao = (
            self.pasta_projeto
            / "imagens"
        )

        pasta_escolhida = filedialog.askdirectory(
            parent=self.winfo_toplevel(),
            title=(
                "Selecione a pasta que contém "
                "as imagens das alternativas"
            ),
            initialdir=(
                str(pasta_padrao)
                if pasta_padrao.exists()
                else str(self.pasta_projeto)
            )
        )

        if not pasta_escolhida:
            return

        arquivos = self._listar_imagens(
            Path(pasta_escolhida)
        )

        if not arquivos:
            messagebox.showwarning(
                "Nenhuma imagem",
                (
                    "A pasta selecionada não contém "
                    "imagens PNG, JPG, JPEG ou WEBP."
                ),
                parent=self.winfo_toplevel()
            )
            return

        alteracoes = 0
        detalhes = []

        for numero, pergunta in enumerate(
            self.perguntas,
            start=1
        ):
            alternativas = pergunta.get(
                "alternativas",
                []
            )

            if not isinstance(
                alternativas,
                list
            ):
                continue

            for indice, campo in [
                (0, "imagem_a"),
                (1, "imagem_b")
            ]:
                if indice >= len(
                    alternativas
                ):
                    continue

                caminho_existente = str(
                    pergunta.get(
                        campo,
                        ""
                    )
                    or ""
                ).strip()

                if (
                    caminho_existente
                    and Path(
                        caminho_existente
                    ).exists()
                ):
                    continue

                alternativa = str(
                    alternativas[
                        indice
                    ]
                ).strip()

                encontrado = (
                    self._encontrar_melhor_imagem(
                        alternativa,
                        arquivos
                    )
                )

                if encontrado is None:
                    continue

                destino = self._copiar_imagem_para_projeto(
                    origem=encontrado,
                    numero_pergunta=numero,
                    lado=(
                        "a"
                        if indice == 0
                        else "b"
                    )
                )

                pergunta[campo] = str(
                    destino.resolve()
                )

                alteracoes += 1
                detalhes.append(
                    (
                        f"Pergunta {numero} — "
                        f"{alternativa}: "
                        f"{encontrado.name}"
                    )
                )

        if self.indice_atual is not None:
            self.selecionar_pergunta(
                self.indice_atual
            )

        if not alteracoes:
            messagebox.showinfo(
                "Nenhuma associação",
                (
                    "Nenhuma imagem compatível foi encontrada.\\n\\n"
                    "Dica: nomeie os arquivos usando o texto da "
                    "alternativa, por exemplo:\\n"
                    "pizza.png\\n"
                    "hamburguer.png"
                ),
                parent=self.winfo_toplevel()
            )
            return

        resumo = "\\n".join(
            detalhes[:12]
        )

        if len(detalhes) > 12:
            resumo += (
                f"\\n... e mais "
                f"{len(detalhes) - 12} associação(ões)."
            )

        self.status.configure(
            text=(
                f"{alteracoes} imagem(ns) associada(s). "
                "Clique em Salvar Quiz para gravar."
            )
        )

        messagebox.showinfo(
            "Imagens associadas",
            (
                f"{alteracoes} imagem(ns) foram associadas "
                f"automaticamente.\\n\\n{resumo}"
            ),
            parent=self.winfo_toplevel()
        )

    def _listar_imagens(
        self,
        pasta
    ) -> list[Path]:
        extensoes = {
            ".png",
            ".jpg",
            ".jpeg",
            ".webp"
        }

        return sorted(
            [
                caminho
                for caminho in pasta.rglob("*")
                if (
                    caminho.is_file()
                    and caminho.suffix.lower()
                    in extensoes
                )
            ],
            key=lambda caminho: caminho.name.lower()
        )

    def _encontrar_melhor_imagem(
        self,
        alternativa,
        arquivos
    ):
        alvo = self._normalizar_nome(
            alternativa
        )

        if not alvo:
            return None

        candidatos = []

        for arquivo in arquivos:
            nome = self._normalizar_nome(
                arquivo.stem
            )

            if not nome:
                continue

            pontuacao = self._pontuar_correspondencia(
                alvo,
                nome
            )

            if pontuacao > 0:
                candidatos.append(
                    (
                        pontuacao,
                        len(nome),
                        arquivo
                    )
                )

        if not candidatos:
            return None

        candidatos.sort(
            key=lambda item: (
                -item[0],
                item[1],
                item[2].name.lower()
            )
        )

        melhor_pontuacao, _, melhor = (
            candidatos[0]
        )

        return (
            melhor
            if melhor_pontuacao >= 55
            else None
        )

    def _pontuar_correspondencia(
        self,
        alvo,
        nome
    ) -> int:
        if alvo == nome:
            return 100

        if alvo in nome:
            return 90

        if nome in alvo:
            return 82

        palavras_alvo = set(
            alvo.split()
        )

        palavras_nome = set(
            nome.split()
        )

        if not palavras_alvo:
            return 0

        comuns = palavras_alvo.intersection(
            palavras_nome
        )

        if not comuns:
            return 0

        proporcao = (
            len(comuns)
            / len(palavras_alvo)
        )

        return int(
            proporcao * 75
        )

    def _normalizar_nome(
        self,
        texto
    ) -> str:
        normalizado = unicodedata.normalize(
            "NFKD",
            str(texto).lower()
        )

        sem_acentos = "".join(
            caractere
            for caractere in normalizado
            if not unicodedata.combining(
                caractere
            )
        )

        palavras = re.findall(
            r"[a-z0-9]+",
            sem_acentos
        )

        ignoradas = {
            "a",
            "o",
            "as",
            "os",
            "de",
            "da",
            "do",
            "das",
            "dos",
            "um",
            "uma",
            "com",
            "ou"
        }

        return " ".join(
            palavra
            for palavra in palavras
            if palavra not in ignoradas
        )

    def _copiar_imagem_para_projeto(
        self,
        origem,
        numero_pergunta,
        lado
    ) -> Path:
        pasta_imagens = (
            self.pasta_projeto
            / "imagens"
        )

        pasta_imagens.mkdir(
            parents=True,
            exist_ok=True
        )

        nome_base = self._normalizar_nome(
            origem.stem
        ).replace(
            " ",
            "_"
        )

        nome_base = (
            nome_base[:40]
            or "imagem"
        )

        destino = (
            pasta_imagens
            / (
                f"pergunta_"
                f"{numero_pergunta:03d}_"
                f"{lado}_"
                f"{nome_base}"
                f"{origem.suffix.lower()}"
            )
        )

        contador = 2
        destino_final = destino

        while (
            destino_final.exists()
            and destino_final.resolve()
            != origem.resolve()
        ):
            destino_final = (
                pasta_imagens
                / (
                    f"pergunta_"
                    f"{numero_pergunta:03d}_"
                    f"{lado}_"
                    f"{nome_base}_"
                    f"{contador}"
                    f"{origem.suffix.lower()}"
                )
            )

            contador += 1

        if destino_final.resolve() != origem.resolve():
            shutil.copy2(
                origem,
                destino_final
            )

        return destino_final

    # =========================================================
    # PRÉVIA DO VÍDEO
    # =========================================================

    def abrir_previa_video(self):
        if (
            self.indice_atual is None
            or self.pasta_projeto is None
        ):
            return

        if not self._aplicar_sem_mensagem():
            messagebox.showwarning(
                "Pergunta incompleta",
                "Informe o texto da pergunta antes de gerar a prévia.",
                parent=self.winfo_toplevel()
            )
            return

        pergunta = self.perguntas[
            self.indice_atual
        ]

        janela = ctk.CTkToplevel(
            self.winfo_toplevel()
        )

        janela.title(
            "Prévia do vídeo"
        )

        janela.geometry(
            "1160x780"
        )

        janela.minsize(
            900,
            650
        )

        janela.transient(
            self.winfo_toplevel()
        )

        janela.grid_columnconfigure(
            0,
            weight=1
        )

        janela.grid_rowconfigure(
            1,
            weight=1
        )

        barra = ctk.CTkFrame(
            janela
        )

        barra.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=18,
            pady=18
        )

        barra.grid_columnconfigure(
            0,
            weight=1
        )

        ctk.CTkLabel(
            barra,
            text=(
                f"Prévia da pergunta "
                f"{self.indice_atual + 1}"
            ),
            font=("Arial", 20, "bold")
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=12,
            pady=10
        )

        etapa = ctk.CTkOptionMenu(
            barra,
            values=[
                "Pergunta",
                "Contagem",
                "Resultado"
            ],
            width=150
        )

        etapa.set(
            "Pergunta"
        )

        etapa.grid(
            row=0,
            column=1,
            padx=6
        )

        contador = ctk.CTkOptionMenu(
            barra,
            values=[
                "5",
                "4",
                "3",
                "2",
                "1"
            ],
            width=80
        )

        contador.set(
            "5"
        )

        contador.grid(
            row=0,
            column=2,
            padx=6
        )

        painel_imagem = ctk.CTkFrame(
            janela
        )

        painel_imagem.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=18,
            pady=(0, 18)
        )

        painel_imagem.grid_columnconfigure(
            0,
            weight=1
        )

        painel_imagem.grid_rowconfigure(
            0,
            weight=1
        )

        preview_label = ctk.CTkLabel(
            painel_imagem,
            text="Gerando prévia...",
            fg_color="#171922",
            corner_radius=14
        )

        preview_label.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=14,
            pady=14
        )

        estado = {
            "imagem_ctk": None
        }

        def gerar():
            mapa_etapas = {
                "Pergunta": "pergunta",
                "Contagem": "contagem",
                "Resultado": "resultado"
            }

            try:
                caminho = (
                    self.preview_generator
                    .gerar(
                        pasta_projeto=(
                            self.pasta_projeto
                        ),
                        pergunta=pergunta,
                        numero=(
                            self.indice_atual
                            + 1
                        ),
                        etapa=mapa_etapas[
                            etapa.get()
                        ],
                        contador=int(
                            contador.get()
                        )
                    )
                )

                imagem = Image.open(
                    caminho
                ).convert("RGB")

                largura_disponivel = max(
                    janela.winfo_width()
                    - 90,
                    800
                )

                altura_disponivel = max(
                    janela.winfo_height()
                    - 170,
                    450
                )

                imagem.thumbnail(
                    (
                        largura_disponivel,
                        altura_disponivel
                    ),
                    Image.Resampling.LANCZOS
                )

                imagem_ctk = ctk.CTkImage(
                    light_image=imagem,
                    dark_image=imagem,
                    size=imagem.size
                )

                estado["imagem_ctk"] = (
                    imagem_ctk
                )

                preview_label.configure(
                    image=imagem_ctk,
                    text=""
                )

            except Exception as erro:
                preview_label.configure(
                    image=None,
                    text=(
                        "Não foi possível gerar "
                        f"a prévia:\n{erro}"
                    )
                )

        ctk.CTkButton(
            barra,
            text="ATUALIZAR PRÉVIA",
            width=160,
            command=gerar
        ).grid(
            row=0,
            column=3,
            padx=8
        )

        janela.after(
            150,
            gerar
        )

    def validar_imagens_da_pergunta(
        self,
        pergunta
    ) -> list[str]:
        problemas = []

        for campo, rotulo in [
            ("imagem_a", "Imagem A"),
            ("imagem_b", "Imagem B")
        ]:
            caminho = str(
                pergunta.get(
                    campo,
                    ""
                )
                or ""
            ).strip()

            if caminho and not Path(
                caminho
            ).exists():
                problemas.append(
                    f"{rotulo}: arquivo não encontrado"
                )

        return problemas

    # =========================================================
    # IMAGENS
    # =========================================================

    def selecionar_imagem(
        self,
        lado
    ):
        if (
            self.indice_atual is None
            or self.pasta_projeto is None
        ):
            return

        origem = filedialog.askopenfilename(
            parent=self.winfo_toplevel(),
            title="Selecionar imagem",
            filetypes=[
                (
                    "Imagens",
                    "*.png *.jpg *.jpeg *.webp"
                ),
                (
                    "Todos os arquivos",
                    "*.*"
                )
            ]
        )

        if not origem:
            return

        origem_path = Path(
            origem
        )

        try:
            with Image.open(
                origem_path
            ) as imagem:
                imagem.verify()

        except (
            OSError,
            UnidentifiedImageError
        ):
            messagebox.showerror(
                "Imagem inválida",
                "O arquivo selecionado não é uma imagem válida.",
                parent=self.winfo_toplevel()
            )
            return

        pasta_imagens = (
            self.pasta_projeto
            / "imagens"
        )

        pasta_imagens.mkdir(
            parents=True,
            exist_ok=True
        )

        sufixo = origem_path.suffix.lower()

        if sufixo not in {
            ".png",
            ".jpg",
            ".jpeg",
            ".webp"
        }:
            sufixo = ".png"

        destino = (
            pasta_imagens
            / (
                f"pergunta_"
                f"{self.indice_atual + 1:03d}_"
                f"{lado}_"
                f"{uuid.uuid4().hex[:8]}"
                f"{sufixo}"
            )
        )

        try:
            shutil.copy2(
                origem_path,
                destino
            )

        except OSError as erro:
            messagebox.showerror(
                "Erro ao copiar imagem",
                str(erro),
                parent=self.winfo_toplevel()
            )
            return

        caminho_salvo = str(
            destino.resolve()
        )

        if lado == "a":
            self.imagem_a_atual = caminho_salvo
        else:
            self.imagem_b_atual = caminho_salvo

        self._atualizar_preview_imagem(
            lado
        )

        self._aplicar_sem_mensagem()

        self.status.configure(
            text=(
                "Imagem copiada para a pasta do projeto."
            )
        )

    def remover_imagem(
        self,
        lado
    ):
        if lado == "a":
            self.imagem_a_atual = ""
        else:
            self.imagem_b_atual = ""

        self._atualizar_preview_imagem(
            lado
        )

        self._aplicar_sem_mensagem()

    def _atualizar_preview_imagem(
        self,
        lado
    ):
        caminho = (
            self.imagem_a_atual
            if lado == "a"
            else self.imagem_b_atual
        )

        preview = (
            self.preview_a
            if lado == "a"
            else self.preview_b
        )

        if not caminho:
            preview.configure(
                image=None,
                text="Nenhuma imagem"
            )

            if lado == "a":
                self.preview_a_ctk = None
            else:
                self.preview_b_ctk = None

            return

        caminho_path = Path(
            caminho
        )

        if not caminho_path.exists():
            preview.configure(
                image=None,
                text=(
                    "Arquivo não encontrado:\n"
                    f"{caminho_path.name}"
                )
            )
            return

        try:
            imagem = Image.open(
                caminho_path
            ).convert("RGBA")

            imagem.thumbnail(
                (340, 170),
                Image.Resampling.LANCZOS
            )

            imagem_ctk = ctk.CTkImage(
                light_image=imagem,
                dark_image=imagem,
                size=imagem.size
            )

            preview.configure(
                image=imagem_ctk,
                text=""
            )

            if lado == "a":
                self.preview_a_ctk = imagem_ctk
            else:
                self.preview_b_ctk = imagem_ctk

        except (
            OSError,
            UnidentifiedImageError
        ):
            preview.configure(
                image=None,
                text="Não foi possível abrir a imagem."
            )

    # =========================================================
    # SALVAMENTO
    # =========================================================

    def salvar_quiz(self):
        if self.pasta_projeto is None:
            messagebox.showinfo(
                "Nenhum projeto",
                "Selecione um projeto.",
                parent=self.winfo_toplevel()
            )
            return

        self._aplicar_sem_mensagem()
        self._renumerar_perguntas()

        problemas = []

        for indice, pergunta in enumerate(
            self.perguntas,
            start=1
        ):
            for problema in (
                self.validar_imagens_da_pergunta(
                    pergunta
                )
            ):
                problemas.append(
                    f"Pergunta {indice}: {problema}"
                )

        if problemas:
            resumo = "\n".join(
                problemas[:10]
            )

            continuar = messagebox.askyesno(
                "Imagens não encontradas",
                (
                    "Foram encontrados caminhos de imagem "
                    "inválidos:\n\n"
                    f"{resumo}\n\n"
                    "Deseja salvar mesmo assim?"
                ),
                parent=self.winfo_toplevel()
            )

            if not continuar:
                return

        try:
            caminho = (
                self.project_manager
                .salvar_quiz(
                    self.pasta_projeto,
                    self.perguntas
                )
            )

            tipos = {
                str(
                    pergunta.get(
                        "tipo_quiz",
                        "conhecimento"
                    )
                )
                for pergunta in self.perguntas
            }

            tipo_projeto = (
                "preferencia"
                if tipos == {
                    "preferencia"
                }
                else "conhecimento"
            )

            if hasattr(
                self.project_manager,
                "atualizar_configuracao_projeto"
            ):
                self.project_manager.atualizar_configuracao_projeto(
                    self.pasta_projeto,
                    {
                        "quantidade_perguntas": len(
                            self.perguntas
                        ),
                        "tipo_quiz": tipo_projeto
                    }
                )

            self.status.configure(
                text=(
                    "Quiz salvo com sucesso em:\n"
                    f"{caminho}"
                )
            )

            messagebox.showinfo(
                "Quiz salvo",
                (
                    f"{len(self.perguntas)} perguntas "
                    "foram salvas com sucesso."
                ),
                parent=self.winfo_toplevel()
            )

        except Exception as erro:
            messagebox.showerror(
                "Erro ao salvar",
                str(erro),
                parent=self.winfo_toplevel()
            )

    # =========================================================
    # AUXILIARES
    # =========================================================

    def _renumerar_perguntas(self):
        for numero, pergunta in enumerate(
            self.perguntas,
            start=1
        ):
            pergunta["numero"] = numero

    def _limpar_editor(self):
        self.tipo_quiz.set(
            "conhecimento"
        )

        self._definir_textbox(
            self.campo_pergunta,
            ""
        )

        for campo in [
            self.campo_a,
            self.campo_b,
            self.campo_c,
            self.campo_d,
            self.campo_resposta
        ]:
            self._definir_entry(
                campo,
                ""
            )

        self._definir_textbox(
            self.campo_narracao,
            ""
        )

        self.imagem_a_atual = ""
        self.imagem_b_atual = ""

        self._atualizar_preview_imagem(
            "a"
        )

        self._atualizar_preview_imagem(
            "b"
        )

        self.rotulo_numero.configure(
            text="Nenhuma pergunta selecionada"
        )

    def _definir_estado_editor(
        self,
        estado
    ):
        widgets = [
            self.tipo_quiz,
            self.campo_pergunta,
            self.campo_a,
            self.campo_b,
            self.campo_c,
            self.campo_d,
            self.campo_resposta,
            self.campo_narracao,
            self.botao_aplicar
        ]

        for widget in widgets:
            try:
                widget.configure(
                    state=estado
                )
            except Exception:
                pass

    def _definir_entry(
        self,
        campo,
        valor
    ):
        estado = campo.cget(
            "state"
        )

        if estado == "disabled":
            campo.configure(
                state="normal"
            )

        campo.delete(
            0,
            "end"
        )

        campo.insert(
            0,
            str(valor or "")
        )

        if estado == "disabled":
            campo.configure(
                state="disabled"
            )

    def _definir_textbox(
        self,
        campo,
        valor
    ):
        estado = campo.cget(
            "state"
        )

        if estado == "disabled":
            campo.configure(
                state="normal"
            )

        campo.delete(
            "1.0",
            "end"
        )

        campo.insert(
            "1.0",
            str(valor or "")
        )

        if estado == "disabled":
            campo.configure(
                state="disabled"
            )
