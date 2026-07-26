import json
import os
from pathlib import Path
from tkinter import messagebox

import customtkinter as ctk
from PIL import Image

from core.project_manager import ProjectManager
from core.thumbnail_generator import ThumbnailGenerator


class PublicationPage(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.project_manager = ProjectManager()
        self.thumbnail_generator = ThumbnailGenerator()

        self.projetos = {}
        self.pasta_projeto_atual = None
        self.caminho_thumbnail_atual = None
        self.imagem_thumbnail_ctk = None

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

        cabecalho.grid_columnconfigure(
            0,
            weight=1
        )

        textos_cabecalho = ctk.CTkFrame(
            cabecalho,
            fg_color="transparent"
        )

        textos_cabecalho.grid(
            row=0,
            column=0,
            sticky="w"
        )

        ctk.CTkLabel(
            textos_cabecalho,
            text="Publicação",
            font=("Arial", 28, "bold")
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            textos_cabecalho,
            text=(
                "Prepare os dados e a thumbnail "
                "do vídeo para publicação no YouTube."
            ),
            text_color="gray70"
        ).pack(
            anchor="w",
            pady=(5, 0)
        )

        ctk.CTkButton(
            cabecalho,
            text="Atualizar projetos",
            width=150,
            command=self.carregar_projetos
        ).grid(
            row=0,
            column=1,
            sticky="e"
        )

        conteudo = ctk.CTkScrollableFrame(
            self
        )

        conteudo.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=30,
            pady=(0, 20)
        )

        conteudo.grid_columnconfigure(
            0,
            weight=1
        )

        self._criar_painel_projeto(
            conteudo
        )

        self._criar_painel_informacoes(
            conteudo
        )

        self._criar_painel_titulo(
            conteudo
        )

        self._criar_painel_descricao(
            conteudo
        )

        self._criar_painel_tags(
            conteudo
        )

        self._criar_painel_thumbnail(
            conteudo
        )

        self._criar_painel_botoes(
            conteudo
        )

        self.status = ctk.CTkLabel(
            conteudo,
            text="Selecione um projeto.",
            wraplength=900
        )

        self.status.grid(
            row=7,
            column=0,
            sticky="ew",
            padx=20,
            pady=(5, 25)
        )

    def _criar_painel_projeto(
        self,
        conteudo
    ):
        painel = ctk.CTkFrame(
            conteudo
        )

        painel.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=10,
            pady=(10, 8)
        )

        painel.grid_columnconfigure(
            1,
            weight=1
        )

        ctk.CTkLabel(
            painel,
            text="Projeto",
            font=("Arial", 17, "bold")
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=(20, 10),
            pady=20
        )

        self.seletor_projeto = ctk.CTkOptionMenu(
            painel,
            values=["Nenhum projeto encontrado"],
            command=self.selecionar_projeto
        )

        self.seletor_projeto.grid(
            row=0,
            column=1,
            sticky="ew",
            padx=10,
            pady=20
        )

        ctk.CTkButton(
            painel,
            text="Carregar",
            width=110,
            command=self.carregar_projeto_selecionado
        ).grid(
            row=0,
            column=2,
            padx=(10, 20),
            pady=20
        )

    def _criar_painel_informacoes(
        self,
        conteudo
    ):
        painel = ctk.CTkFrame(
            conteudo
        )

        painel.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=10,
            pady=8
        )

        painel.grid_columnconfigure(
            0,
            weight=1
        )

        self.rotulo_projeto = ctk.CTkLabel(
            painel,
            text="Nenhum projeto selecionado.",
            font=("Arial", 16, "bold")
        )

        self.rotulo_projeto.grid(
            row=0,
            column=0,
            sticky="w",
            padx=20,
            pady=(18, 5)
        )

        self.rotulo_detalhes = ctk.CTkLabel(
            painel,
            text=(
                "Selecione um projeto para gerar "
                "os dados de publicação."
            ),
            text_color="gray70",
            justify="left"
        )

        self.rotulo_detalhes.grid(
            row=1,
            column=0,
            sticky="w",
            padx=20,
            pady=(0, 18)
        )

    def _criar_painel_titulo(
        self,
        conteudo
    ):
        painel = ctk.CTkFrame(
            conteudo
        )

        painel.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=10,
            pady=8
        )

        painel.grid_columnconfigure(
            0,
            weight=1
        )

        linha = ctk.CTkFrame(
            painel,
            fg_color="transparent"
        )

        linha.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=20,
            pady=(18, 8)
        )

        linha.grid_columnconfigure(
            0,
            weight=1
        )

        ctk.CTkLabel(
            linha,
            text="Título do vídeo",
            font=("Arial", 17, "bold")
        ).grid(
            row=0,
            column=0,
            sticky="w"
        )

        self.contador_titulo = ctk.CTkLabel(
            linha,
            text="0 caracteres",
            text_color="gray70"
        )

        self.contador_titulo.grid(
            row=0,
            column=1,
            sticky="e"
        )

        self.campo_titulo = ctk.CTkEntry(
            painel,
            placeholder_text="O título aparecerá aqui."
        )

        self.campo_titulo.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=20,
            pady=(0, 8)
        )

        self.campo_titulo.bind(
            "<KeyRelease>",
            self.atualizar_contador_titulo
        )

        ctk.CTkButton(
            painel,
            text="Copiar título",
            width=130,
            fg_color="gray35",
            hover_color="gray25",
            command=lambda: self.copiar_texto(
                self.campo_titulo.get(),
                "Título"
            )
        ).grid(
            row=2,
            column=0,
            sticky="e",
            padx=20,
            pady=(0, 18)
        )

    def _criar_painel_descricao(
        self,
        conteudo
    ):
        painel = ctk.CTkFrame(
            conteudo
        )

        painel.grid(
            row=3,
            column=0,
            sticky="ew",
            padx=10,
            pady=8
        )

        painel.grid_columnconfigure(
            0,
            weight=1
        )

        ctk.CTkLabel(
            painel,
            text="Descrição",
            font=("Arial", 17, "bold")
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=20,
            pady=(18, 8)
        )

        self.campo_descricao = ctk.CTkTextbox(
            painel,
            height=230,
            wrap="word"
        )

        self.campo_descricao.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=20,
            pady=(0, 8)
        )

        ctk.CTkButton(
            painel,
            text="Copiar descrição",
            width=140,
            fg_color="gray35",
            hover_color="gray25",
            command=lambda: self.copiar_texto(
                self.campo_descricao.get(
                    "0.0",
                    "end"
                ).strip(),
                "Descrição"
            )
        ).grid(
            row=2,
            column=0,
            sticky="e",
            padx=20,
            pady=(0, 18)
        )

    def _criar_painel_tags(
        self,
        conteudo
    ):
        painel = ctk.CTkFrame(
            conteudo
        )

        painel.grid(
            row=4,
            column=0,
            sticky="ew",
            padx=10,
            pady=8
        )

        painel.grid_columnconfigure(
            0,
            weight=1
        )

        ctk.CTkLabel(
            painel,
            text="Tags",
            font=("Arial", 17, "bold")
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=20,
            pady=(18, 5)
        )

        ctk.CTkLabel(
            painel,
            text="Separe as tags por vírgulas.",
            text_color="gray70"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=20,
            pady=(0, 8)
        )

        self.campo_tags = ctk.CTkTextbox(
            painel,
            height=110,
            wrap="word"
        )

        self.campo_tags.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=20,
            pady=(0, 8)
        )

        ctk.CTkButton(
            painel,
            text="Copiar tags",
            width=130,
            fg_color="gray35",
            hover_color="gray25",
            command=lambda: self.copiar_texto(
                self.campo_tags.get(
                    "0.0",
                    "end"
                ).strip(),
                "Tags"
            )
        ).grid(
            row=3,
            column=0,
            sticky="e",
            padx=20,
            pady=(0, 18)
        )

    def _criar_painel_thumbnail(
        self,
        conteudo
    ):
        painel = ctk.CTkFrame(
            conteudo
        )

        painel.grid(
            row=5,
            column=0,
            sticky="ew",
            padx=10,
            pady=8
        )

        painel.grid_columnconfigure(
            0,
            weight=1
        )

        ctk.CTkLabel(
            painel,
            text="Thumbnail do vídeo",
            font=("Arial", 17, "bold")
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=20,
            pady=(18, 5)
        )

        ctk.CTkLabel(
            painel,
            text=(
                "A imagem será criada em 1280 × 720 "
                "e salva como thumbnail.png."
            ),
            text_color="gray70"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=20,
            pady=(0, 10)
        )

        self.campo_chamada_thumbnail = ctk.CTkEntry(
            painel,
            placeholder_text="Texto de chamada da thumbnail"
        )

        self.campo_chamada_thumbnail.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=20,
            pady=(0, 12)
        )

        self.campo_chamada_thumbnail.insert(
            0,
            "VOCÊ CONSEGUE ACERTAR?"
        )

        self.preview_thumbnail = ctk.CTkLabel(
            painel,
            text=(
                "A thumbnail aparecerá aqui "
                "depois de ser gerada."
            ),
            width=640,
            height=360,
            corner_radius=12,
            fg_color="#101820"
        )

        self.preview_thumbnail.grid(
            row=3,
            column=0,
            padx=20,
            pady=(0, 15)
        )

        linha_botoes = ctk.CTkFrame(
            painel,
            fg_color="transparent"
        )

        linha_botoes.grid(
            row=4,
            column=0,
            sticky="e",
            padx=20,
            pady=(0, 18)
        )

        ctk.CTkButton(
            linha_botoes,
            text="Gerar thumbnail",
            width=160,
            command=self.gerar_thumbnail
        ).pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            linha_botoes,
            text="Abrir thumbnail",
            width=150,
            fg_color="gray35",
            hover_color="gray25",
            command=self.abrir_thumbnail
        ).pack(
            side="left",
            padx=5
        )

    def _criar_painel_botoes(
        self,
        conteudo
    ):
        painel = ctk.CTkFrame(
            conteudo,
            fg_color="transparent"
        )

        painel.grid(
            row=6,
            column=0,
            sticky="ew",
            padx=10,
            pady=(15, 10)
        )

        ctk.CTkButton(
            painel,
            text="GERAR DADOS",
            width=180,
            height=44,
            command=self.gerar_dados_publicacao
        ).pack(
            side="left",
            padx=(0, 8)
        )

        ctk.CTkButton(
            painel,
            text="GERAR TUDO",
            width=180,
            height=44,
            command=self.gerar_tudo
        ).pack(
            side="left",
            padx=8
        )

        ctk.CTkButton(
            painel,
            text="SALVAR",
            width=150,
            height=44,
            command=self.salvar_publicacao
        ).pack(
            side="left",
            padx=8
        )

        ctk.CTkButton(
            painel,
            text="Abrir pasta",
            width=140,
            height=44,
            fg_color="gray35",
            hover_color="gray25",
            command=self.abrir_pasta_projeto
        ).pack(
            side="left",
            padx=8
        )

    def carregar_projetos(self):
        self.projetos.clear()

        try:
            pastas = (
                self.project_manager
                .listar_projetos()
            )
        except OSError as erro:
            self.seletor_projeto.configure(
                values=[
                    "Erro ao carregar projetos"
                ]
            )

            self.seletor_projeto.set(
                "Erro ao carregar projetos"
            )

            self.status.configure(
                text=(
                    "Erro ao carregar projetos: "
                    f"{erro}"
                )
            )

            return

        for pasta in pastas:
            self.projetos[
                pasta.name
            ] = pasta

        nomes = list(
            self.projetos.keys()
        )

        if not nomes:
            self.seletor_projeto.configure(
                values=[
                    "Nenhum projeto encontrado"
                ]
            )

            self.seletor_projeto.set(
                "Nenhum projeto encontrado"
            )

            self.pasta_projeto_atual = None

            self.status.configure(
                text=(
                    "Nenhum projeto foi encontrado."
                )
            )

            return

        self.seletor_projeto.configure(
            values=nomes
        )

        nome_atual = (
            self.seletor_projeto.get()
        )

        if nome_atual not in self.projetos:
            self.seletor_projeto.set(
                nomes[0]
            )

        self.carregar_projeto_selecionado()

    def selecionar_projeto(
        self,
        nome_projeto
    ):
        if nome_projeto in self.projetos:
            self.carregar_projeto(
                self.projetos[
                    nome_projeto
                ]
            )

    def carregar_projeto_selecionado(self):
        nome_projeto = (
            self.seletor_projeto.get()
        )

        pasta_projeto = (
            self.projetos.get(
                nome_projeto
            )
        )

        if pasta_projeto is None:
            self.status.configure(
                text=(
                    "Selecione um projeto válido."
                )
            )

            return

        self.carregar_projeto(
            pasta_projeto
        )

    def carregar_projeto(
        self,
        pasta_projeto
    ):
        self.pasta_projeto_atual = Path(
            pasta_projeto
        )

        configuracao = (
            self._carregar_configuracao()
        )

        perguntas = (
            self._carregar_perguntas()
        )

        tema = configuracao.get(
            "tema",
            self.pasta_projeto_atual.name
        )

        quantidade = configuracao.get(
            "quantidade_perguntas",
            len(perguntas)
        )

        self.rotulo_projeto.configure(
            text=f"Projeto: {tema}"
        )

        self.rotulo_detalhes.configure(
            text=(
                f"Pasta: {self.pasta_projeto_atual}\n"
                f"Perguntas: {quantidade}"
            )
        )

        publicacao = (
            self.carregar_publicacao_salva()
        )

        if publicacao:
            self.preencher_campos(
                titulo=publicacao.get(
                    "titulo",
                    ""
                ),
                descricao=publicacao.get(
                    "descricao",
                    ""
                ),
                tags=publicacao.get(
                    "tags",
                    ""
                )
            )

            chamada = publicacao.get(
                "chamada_thumbnail",
                "VOCÊ CONSEGUE ACERTAR?"
            )

            self.campo_chamada_thumbnail.delete(
                0,
                "end"
            )

            self.campo_chamada_thumbnail.insert(
                0,
                chamada
            )

            self.status.configure(
                text=(
                    "Dados de publicação carregados."
                )
            )
        else:
            self.limpar_campos()

            self.status.configure(
                text=(
                    "Projeto carregado. Clique em "
                    "Gerar dados ou Gerar tudo."
                )
            )

        caminho_thumbnail = (
            self.pasta_projeto_atual
            / "thumbnail.png"
        )

        if caminho_thumbnail.exists():
            self.exibir_thumbnail(
                caminho_thumbnail
            )
        else:
            self.caminho_thumbnail_atual = None
            self.imagem_thumbnail_ctk = None

            self.preview_thumbnail.configure(
                image=None,
                text=(
                    "A thumbnail aparecerá aqui "
                    "depois de ser gerada."
                )
            )

    def gerar_dados_publicacao(self):
        if not self._projeto_selecionado():
            return

        configuracao = (
            self._carregar_configuracao()
        )

        perguntas = (
            self._carregar_perguntas()
        )

        tema = str(
            configuracao.get(
                "tema",
                self.pasta_projeto_atual.name
            )
        ).strip()

        quantidade = (
            configuracao.get(
                "quantidade_perguntas",
                len(perguntas)
            )
        )

        try:
            quantidade = int(
                quantidade
            )
        except (
            TypeError,
            ValueError
        ):
            quantidade = len(
                perguntas
            )

        titulo = self.gerar_titulo(
            tema=tema,
            quantidade=quantidade
        )

        descricao = self.gerar_descricao(
            tema=tema,
            quantidade=quantidade
        )

        tags = self.gerar_tags(
            tema=tema
        )

        self.preencher_campos(
            titulo=titulo,
            descricao=descricao,
            tags=tags
        )

        self.status.configure(
            text=(
                "Título, descrição e tags gerados. "
                "Você pode editar antes de salvar."
            )
        )

    def gerar_thumbnail(self):
        if not self._projeto_selecionado():
            return

        configuracao = (
            self._carregar_configuracao()
        )

        perguntas = (
            self._carregar_perguntas()
        )

        tema = str(
            configuracao.get(
                "tema",
                self.pasta_projeto_atual.name
            )
        ).strip()

        quantidade = (
            configuracao.get(
                "quantidade_perguntas",
                len(perguntas)
            )
        )

        try:
            quantidade = int(
                quantidade
            )
        except (
            TypeError,
            ValueError
        ):
            quantidade = len(
                perguntas
            )

        chamada = (
            self.campo_chamada_thumbnail
            .get()
            .strip()
        )

        if not chamada:
            chamada = (
                "VOCÊ CONSEGUE ACERTAR?"
            )

            self.campo_chamada_thumbnail.insert(
                0,
                chamada
            )

        self.status.configure(
            text="Gerando thumbnail..."
        )

        self.update_idletasks()

        try:
            caminho = (
                self.thumbnail_generator
                .gerar(
                    pasta_projeto=(
                        self.pasta_projeto_atual
                    ),
                    tema=tema,
                    quantidade_perguntas=(
                        quantidade
                    ),
                    texto_chamada=chamada
                )
            )

            self.exibir_thumbnail(
                caminho
            )

            self.status.configure(
                text=(
                    "Thumbnail gerada com sucesso: "
                    f"{caminho}"
                )
            )

        except Exception as erro:
            messagebox.showerror(
                title="Erro ao gerar thumbnail",
                message=(
                    "Não foi possível gerar "
                    "a thumbnail.\n\n"
                    f"{erro}"
                ),
                parent=self.winfo_toplevel()
            )

            self.status.configure(
                text=(
                    "Erro ao gerar thumbnail: "
                    f"{erro}"
                )
            )

    def gerar_tudo(self):
        if not self._projeto_selecionado():
            return

        self.gerar_dados_publicacao()
        self.gerar_thumbnail()
        self.salvar_publicacao()

    def exibir_thumbnail(
        self,
        caminho_thumbnail
    ):
        caminho_thumbnail = Path(
            caminho_thumbnail
        )

        if not caminho_thumbnail.exists():
            return

        try:
            with Image.open(
                caminho_thumbnail
            ) as imagem_original:
                imagem = (
                    imagem_original
                    .convert("RGB")
                    .copy()
                )

            self.imagem_thumbnail_ctk = (
                ctk.CTkImage(
                    light_image=imagem,
                    dark_image=imagem,
                    size=(
                        640,
                        360
                    )
                )
            )

            self.preview_thumbnail.configure(
                image=self.imagem_thumbnail_ctk,
                text=""
            )

            self.caminho_thumbnail_atual = (
                caminho_thumbnail
            )

        except (
            OSError,
            ValueError
        ) as erro:
            self.preview_thumbnail.configure(
                image=None,
                text=(
                    "Não foi possível visualizar "
                    f"a thumbnail.\n{erro}"
                )
            )

    def abrir_thumbnail(self):
        caminho = (
            self.caminho_thumbnail_atual
        )

        if caminho is None:
            self.status.configure(
                text=(
                    "Gere uma thumbnail primeiro."
                )
            )

            return

        caminho = Path(
            caminho
        )

        if not caminho.exists():
            self.status.configure(
                text=(
                    "O arquivo da thumbnail "
                    "não foi encontrado."
                )
            )

            return

        try:
            os.startfile(
                str(
                    caminho.resolve()
                )
            )
        except OSError as erro:
            messagebox.showerror(
                title="Erro",
                message=(
                    "Não foi possível abrir "
                    "a thumbnail.\n\n"
                    f"{erro}"
                ),
                parent=self.winfo_toplevel()
            )

    def gerar_titulo(
        self,
        tema,
        quantidade
    ):
        return (
            f"Você consegue acertar? "
            f"{quantidade} perguntas sobre {tema}!"
        )

    def gerar_descricao(
        self,
        tema,
        quantidade
    ):
        return (
            f"Você sabe tudo sobre {tema}?\n\n"
            f"Neste vídeo do Moleza Quiz, você terá "
            f"{quantidade} perguntas para testar seus "
            "conhecimentos e se divertir com toda "
            "a família.\n\n"
            "Responda antes que o tempo acabe e conte "
            "nos comentários quantas perguntas você "
            "acertou!\n\n"
            "Inscreva-se no canal e ative as "
            "notificações para não perder os "
            "próximos desafios.\n\n"
            "#MolezaQuiz #Quiz #Desafio"
        )

    def gerar_tags(
        self,
        tema
    ):
        tema_limpo = tema.strip()

        tags = [
            "Moleza Quiz",
            "quiz",
            "quiz infantil",
            "quiz para família",
            "jogo de perguntas",
            "perguntas e respostas",
            "desafio",
            "teste seus conhecimentos",
            tema_limpo,
            f"quiz de {tema_limpo}",
            f"perguntas sobre {tema_limpo}",
            "vídeo de quiz",
            "quiz divertido",
            "quiz em português",
            "brincadeira em família"
        ]

        tags_unicas = []
        tags_normalizadas = set()

        for tag in tags:
            tag = tag.strip()

            if not tag:
                continue

            chave = tag.lower()

            if chave in tags_normalizadas:
                continue

            tags_normalizadas.add(
                chave
            )

            tags_unicas.append(
                tag
            )

        return ", ".join(
            tags_unicas
        )

    def preencher_campos(
        self,
        titulo,
        descricao,
        tags
    ):
        self.campo_titulo.delete(
            0,
            "end"
        )

        self.campo_titulo.insert(
            0,
            titulo
        )

        self.campo_descricao.delete(
            "0.0",
            "end"
        )

        self.campo_descricao.insert(
            "0.0",
            descricao
        )

        self.campo_tags.delete(
            "0.0",
            "end"
        )

        self.campo_tags.insert(
            "0.0",
            tags
        )

        self.atualizar_contador_titulo()

    def limpar_campos(self):
        self.campo_titulo.delete(
            0,
            "end"
        )

        self.campo_descricao.delete(
            "0.0",
            "end"
        )

        self.campo_tags.delete(
            "0.0",
            "end"
        )

        self.campo_chamada_thumbnail.delete(
            0,
            "end"
        )

        self.campo_chamada_thumbnail.insert(
            0,
            "VOCÊ CONSEGUE ACERTAR?"
        )

        self.atualizar_contador_titulo()

    def atualizar_contador_titulo(
        self,
        evento=None
    ):
        quantidade = len(
            self.campo_titulo.get()
        )

        self.contador_titulo.configure(
            text=f"{quantidade} caracteres"
        )

    def salvar_publicacao(self):
        if not self._projeto_selecionado():
            return

        titulo = (
            self.campo_titulo
            .get()
            .strip()
        )

        descricao = (
            self.campo_descricao
            .get(
                "0.0",
                "end"
            )
            .strip()
        )

        tags = (
            self.campo_tags
            .get(
                "0.0",
                "end"
            )
            .strip()
        )

        chamada_thumbnail = (
            self.campo_chamada_thumbnail
            .get()
            .strip()
        )

        if not titulo:
            self.status.configure(
                text=(
                    "O título não pode ficar vazio."
                )
            )

            return

        if not descricao:
            self.status.configure(
                text=(
                    "A descrição não pode "
                    "ficar vazia."
                )
            )

            return

        if not tags:
            self.status.configure(
                text=(
                    "As tags não podem ficar vazias."
                )
            )

            return

        dados = {
            "titulo": titulo,
            "descricao": descricao,
            "tags": tags,
            "chamada_thumbnail": (
                chamada_thumbnail
            ),
            "thumbnail": (
                str(
                    self.caminho_thumbnail_atual
                )
                if self.caminho_thumbnail_atual
                else ""
            )
        }

        arquivo_publicacao = (
            self.pasta_projeto_atual
            / "publicacao.json"
        )

        try:
            with open(
                arquivo_publicacao,
                "w",
                encoding="utf-8"
            ) as arquivo_json:
                json.dump(
                    dados,
                    arquivo_json,
                    ensure_ascii=False,
                    indent=4
                )

            self.status.configure(
                text=(
                    "Dados salvos com sucesso em: "
                    f"{arquivo_publicacao}"
                )
            )

        except OSError as erro:
            self.status.configure(
                text=(
                    "Não foi possível salvar "
                    f"os dados: {erro}"
                )
            )

    def carregar_publicacao_salva(self):
        if self.pasta_projeto_atual is None:
            return {}

        arquivo_publicacao = (
            self.pasta_projeto_atual
            / "publicacao.json"
        )

        if not arquivo_publicacao.exists():
            return {}

        try:
            with open(
                arquivo_publicacao,
                "r",
                encoding="utf-8"
            ) as arquivo_json:
                dados = json.load(
                    arquivo_json
                )

            if isinstance(
                dados,
                dict
            ):
                return dados

        except (
            OSError,
            json.JSONDecodeError
        ):
            return {}

        return {}

    def copiar_texto(
        self,
        texto,
        nome_campo
    ):
        texto = texto.strip()

        if not texto:
            self.status.configure(
                text=f"{nome_campo} está vazio."
            )

            return

        try:
            self.clipboard_clear()

            self.clipboard_append(
                texto
            )

            self.update()

            self.status.configure(
                text=(
                    f"{nome_campo} copiado para "
                    "a área de transferência."
                )
            )

        except Exception as erro:
            self.status.configure(
                text=(
                    "Não foi possível copiar "
                    f"o conteúdo: {erro}"
                )
            )

    def abrir_pasta_projeto(self):
        if not self._projeto_selecionado():
            return

        if not self.pasta_projeto_atual.exists():
            self.status.configure(
                text=(
                    "A pasta do projeto "
                    "não foi encontrada."
                )
            )

            return

        try:
            os.startfile(
                str(
                    self.pasta_projeto_atual
                    .resolve()
                )
            )

            self.status.configure(
                text=(
                    "Abrindo pasta do projeto: "
                    f"{self.pasta_projeto_atual}"
                )
            )

        except OSError as erro:
            messagebox.showerror(
                title="Erro",
                message=(
                    "Não foi possível abrir "
                    "a pasta.\n\n"
                    f"{erro}"
                ),
                parent=self.winfo_toplevel()
            )

    def _projeto_selecionado(self):
        if self.pasta_projeto_atual is None:
            self.status.configure(
                text=(
                    "Selecione um projeto primeiro."
                )
            )

            return False

        return True

    def _carregar_configuracao(self):
        try:
            dados = (
                self.project_manager
                .carregar_configuracao_projeto(
                    self.pasta_projeto_atual
                )
            )

            if isinstance(
                dados,
                dict
            ):
                return dados

        except Exception:
            pass

        caminho = (
            self.pasta_projeto_atual
            / "config.json"
        )

        return self._ler_json(
            caminho,
            padrao={}
        )

    def _carregar_perguntas(self):
        try:
            dados = (
                self.project_manager
                .carregar_quiz(
                    self.pasta_projeto_atual
                )
            )

            if isinstance(
                dados,
                list
            ):
                return dados

        except Exception:
            pass

        caminho = (
            self.pasta_projeto_atual
            / "quiz.json"
        )

        dados = self._ler_json(
            caminho,
            padrao=[]
        )

        if isinstance(
            dados,
            list
        ):
            return dados

        if isinstance(
            dados,
            dict
        ):
            perguntas = dados.get(
                "perguntas",
                []
            )

            if isinstance(
                perguntas,
                list
            ):
                return perguntas

        return []

    def _ler_json(
        self,
        caminho,
        padrao
    ):
        caminho = Path(
            caminho
        )

        if not caminho.exists():
            return padrao

        try:
            with open(
                caminho,
                "r",
                encoding="utf-8"
            ) as arquivo:
                return json.load(
                    arquivo
                )

        except (
            OSError,
            json.JSONDecodeError
        ):
            return padrao
