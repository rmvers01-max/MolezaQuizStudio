import json
import os
from pathlib import Path
from tkinter import filedialog, messagebox

import customtkinter as ctk
from PIL import Image

from core.choice_thumbnail_generator import ChoiceThumbnailGenerator
from core.project_manager import ProjectManager
from core.thumbnail_generator import ThumbnailGenerator


class PublicationPage(ctk.CTkFrame):
    MODELO_SIMPLES = "Thumbnail simples"
    MODELO_ESCOLHAS = "O que você prefere?"

    def __init__(self, master):
        super().__init__(master)

        self.project_manager = ProjectManager()
        self.thumbnail_generator = ThumbnailGenerator()
        self.choice_thumbnail_generator = ChoiceThumbnailGenerator()

        self.projetos = {}
        self.pasta_projeto_atual = None
        self.caminho_thumbnail_atual = None
        self.imagem_thumbnail_ctk = None

        self.caminho_imagem_esquerda = None
        self.caminho_imagem_direita = None

        self.criar_interface()
        self.carregar_projetos()

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
                "Prepare título, descrição, tags e thumbnails "
                "para publicação no YouTube."
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

        # Precisa existir antes de criar o painel de thumbnail,
        # pois alterar_modelo_thumbnail() já utiliza self.status.
        self.status = ctk.CTkLabel(
            conteudo,
            text="Selecione um projeto.",
            wraplength=1000
        )

        self._criar_painel_thumbnail(
            conteudo
        )

        self._criar_painel_botoes(
            conteudo
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
            font=("Arial", 20, "bold")
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
                "Escolha um modelo e configure os elementos. "
                "A imagem será criada em 1280 × 720."
            ),
            text_color="gray70"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=20,
            pady=(0, 15)
        )

        configuracoes = ctk.CTkFrame(
            painel
        )

        configuracoes.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=20,
            pady=(0, 15)
        )

        configuracoes.grid_columnconfigure(
            1,
            weight=1
        )

        ctk.CTkLabel(
            configuracoes,
            text="Modelo"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=15,
            pady=(15, 8)
        )

        self.seletor_modelo_thumbnail = ctk.CTkOptionMenu(
            configuracoes,
            values=[
                self.MODELO_SIMPLES,
                self.MODELO_ESCOLHAS
            ],
            command=self.alterar_modelo_thumbnail
        )

        self.seletor_modelo_thumbnail.grid(
            row=0,
            column=1,
            sticky="ew",
            padx=15,
            pady=(15, 8)
        )

        self.seletor_modelo_thumbnail.set(
            self.MODELO_SIMPLES
        )

        self.painel_modelo_simples = ctk.CTkFrame(
            configuracoes,
            fg_color="transparent"
        )

        self.painel_modelo_simples.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=15,
            pady=(5, 15)
        )

        self.painel_modelo_simples.grid_columnconfigure(
            1,
            weight=1
        )

        ctk.CTkLabel(
            self.painel_modelo_simples,
            text="Chamada"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=(0, 12),
            pady=5
        )

        self.campo_chamada_thumbnail = ctk.CTkEntry(
            self.painel_modelo_simples,
            placeholder_text="Texto de chamada"
        )

        self.campo_chamada_thumbnail.grid(
            row=0,
            column=1,
            sticky="ew",
            pady=5
        )

        self.campo_chamada_thumbnail.insert(
            0,
            "VOCÊ CONSEGUE ACERTAR?"
        )

        self.painel_modelo_escolhas = ctk.CTkFrame(
            configuracoes,
            fg_color="transparent"
        )

        self.painel_modelo_escolhas.grid_columnconfigure(
            1,
            weight=1
        )

        ctk.CTkLabel(
            self.painel_modelo_escolhas,
            text="Título superior"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=(0, 12),
            pady=5
        )

        self.campo_titulo_superior = ctk.CTkEntry(
            self.painel_modelo_escolhas
        )

        self.campo_titulo_superior.grid(
            row=0,
            column=1,
            sticky="ew",
            pady=5
        )

        self.campo_titulo_superior.insert(
            0,
            "O QUE VOCÊ PREFERE?"
        )

        ctk.CTkLabel(
            self.painel_modelo_escolhas,
            text="Texto inferior"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=(0, 12),
            pady=5
        )

        self.campo_texto_inferior = ctk.CTkEntry(
            self.painel_modelo_escolhas
        )

        self.campo_texto_inferior.grid(
            row=1,
            column=1,
            sticky="ew",
            pady=5
        )

        self.campo_texto_inferior.insert(
            0,
            "FAÇA SUA ESCOLHA!"
        )

        ctk.CTkLabel(
            self.painel_modelo_escolhas,
            text="Texto central"
        ).grid(
            row=2,
            column=0,
            sticky="w",
            padx=(0, 12),
            pady=5
        )

        self.campo_texto_central = ctk.CTkEntry(
            self.painel_modelo_escolhas,
            width=130
        )

        self.campo_texto_central.grid(
            row=2,
            column=1,
            sticky="w",
            pady=5
        )

        self.campo_texto_central.insert(
            0,
            "OU"
        )

        self._criar_seletor_imagem(
            painel=self.painel_modelo_escolhas,
            linha=3,
            titulo="Imagem esquerda",
            lado="esquerda"
        )

        self._criar_seletor_imagem(
            painel=self.painel_modelo_escolhas,
            linha=4,
            titulo="Imagem direita",
            lado="direita"
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

        self.alterar_modelo_thumbnail(
            self.MODELO_SIMPLES
        )

    def _criar_seletor_imagem(
        self,
        painel,
        linha,
        titulo,
        lado
    ):
        ctk.CTkLabel(
            painel,
            text=titulo
        ).grid(
            row=linha,
            column=0,
            sticky="w",
            padx=(0, 12),
            pady=7
        )

        area = ctk.CTkFrame(
            painel,
            fg_color="transparent"
        )

        area.grid(
            row=linha,
            column=1,
            sticky="ew",
            pady=7
        )

        area.grid_columnconfigure(
            0,
            weight=1
        )

        rotulo = ctk.CTkLabel(
            area,
            text="Nenhuma imagem selecionada.",
            anchor="w",
            text_color="gray70"
        )

        rotulo.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(0, 10)
        )

        if lado == "esquerda":
            self.rotulo_imagem_esquerda = rotulo
            comando = self.selecionar_imagem_esquerda
        else:
            self.rotulo_imagem_direita = rotulo
            comando = self.selecionar_imagem_direita

        ctk.CTkButton(
            area,
            text="Selecionar",
            width=110,
            command=comando
        ).grid(
            row=0,
            column=1
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

    def alterar_modelo_thumbnail(
        self,
        modelo
    ):
        self.painel_modelo_simples.grid_forget()
        self.painel_modelo_escolhas.grid_forget()

        if modelo == self.MODELO_ESCOLHAS:
            self.painel_modelo_escolhas.grid(
                row=1,
                column=0,
                columnspan=2,
                sticky="ew",
                padx=15,
                pady=(5, 15)
            )

            self.status.configure(
                text=(
                    "Modelo elaborado selecionado. "
                    "Escolha as duas imagens."
                )
            )

        else:
            self.painel_modelo_simples.grid(
                row=1,
                column=0,
                columnspan=2,
                sticky="ew",
                padx=15,
                pady=(5, 15)
            )

            self.status.configure(
                text="Modelo simples selecionado."
            )

    def selecionar_imagem_esquerda(self):
        caminho = self._selecionar_imagem()

        if not caminho:
            return

        self.caminho_imagem_esquerda = Path(
            caminho
        )

        self.rotulo_imagem_esquerda.configure(
            text=self.caminho_imagem_esquerda.name
        )

        self.status.configure(
            text=(
                "Imagem esquerda selecionada: "
                f"{self.caminho_imagem_esquerda}"
            )
        )

    def selecionar_imagem_direita(self):
        caminho = self._selecionar_imagem()

        if not caminho:
            return

        self.caminho_imagem_direita = Path(
            caminho
        )

        self.rotulo_imagem_direita.configure(
            text=self.caminho_imagem_direita.name
        )

        self.status.configure(
            text=(
                "Imagem direita selecionada: "
                f"{self.caminho_imagem_direita}"
            )
        )

    def _selecionar_imagem(self):
        return filedialog.askopenfilename(
            parent=self.winfo_toplevel(),
            title="Selecione uma imagem",
            filetypes=[
                (
                    "Arquivos de imagem",
                    "*.png *.jpg *.jpeg *.webp"
                ),
                (
                    "Todos os arquivos",
                    "*.*"
                )
            ]
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
                text="Nenhum projeto foi encontrado."
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
                text="Selecione um projeto válido."
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
            self._carregar_campos_publicacao(
                publicacao
            )

            self.status.configure(
                text="Dados de publicação carregados."
            )

        else:
            self.limpar_campos()

            self.status.configure(
                text=(
                    "Projeto carregado. Clique em "
                    "Gerar dados ou Gerar tudo."
                )
            )

        caminho_salvo = (
            publicacao.get(
                "thumbnail",
                ""
            )
            if publicacao
            else ""
        )

        caminhos_possiveis = []

        if caminho_salvo:
            caminhos_possiveis.append(
                Path(
                    caminho_salvo
                )
            )

        caminhos_possiveis.extend(
            [
                self.pasta_projeto_atual
                / "thumbnail.png",

                self.pasta_projeto_atual
                / "thumbnail_escolhas.png"
            ]
        )

        thumbnail_encontrada = None

        for caminho in caminhos_possiveis:
            if caminho.exists():
                thumbnail_encontrada = caminho
                break

        if thumbnail_encontrada:
            self.exibir_thumbnail(
                thumbnail_encontrada
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

    def _carregar_campos_publicacao(
        self,
        publicacao
    ):
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

        self._definir_entry(
            self.campo_chamada_thumbnail,
            chamada
        )

        modelo = publicacao.get(
            "modelo_thumbnail",
            self.MODELO_SIMPLES
        )

        if modelo not in {
            self.MODELO_SIMPLES,
            self.MODELO_ESCOLHAS
        }:
            modelo = self.MODELO_SIMPLES

        self.seletor_modelo_thumbnail.set(
            modelo
        )

        self.alterar_modelo_thumbnail(
            modelo
        )

        self._definir_entry(
            self.campo_titulo_superior,
            publicacao.get(
                "titulo_superior_thumbnail",
                "O QUE VOCÊ PREFERE?"
            )
        )

        self._definir_entry(
            self.campo_texto_inferior,
            publicacao.get(
                "texto_inferior_thumbnail",
                "FAÇA SUA ESCOLHA!"
            )
        )

        self._definir_entry(
            self.campo_texto_central,
            publicacao.get(
                "texto_central_thumbnail",
                "OU"
            )
        )

        caminho_esquerda = publicacao.get(
            "imagem_esquerda_thumbnail",
            ""
        )

        caminho_direita = publicacao.get(
            "imagem_direita_thumbnail",
            ""
        )

        self.caminho_imagem_esquerda = (
            Path(
                caminho_esquerda
            )
            if caminho_esquerda
            else None
        )

        self.caminho_imagem_direita = (
            Path(
                caminho_direita
            )
            if caminho_direita
            else None
        )

        self._atualizar_rotulos_imagens()

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

        quantidade = self._obter_quantidade(
            configuracao,
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

        modelo = (
            self.seletor_modelo_thumbnail.get()
        )

        if modelo == self.MODELO_ESCOLHAS:
            self._gerar_thumbnail_escolhas()
        else:
            self._gerar_thumbnail_simples()

    def _gerar_thumbnail_simples(self):
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

        quantidade = self._obter_quantidade(
            configuracao,
            perguntas
        )

        chamada = (
            self.campo_chamada_thumbnail
            .get()
            .strip()
        )

        if not chamada:
            chamada = "VOCÊ CONSEGUE ACERTAR?"

            self._definir_entry(
                self.campo_chamada_thumbnail,
                chamada
            )

        self.status.configure(
            text="Gerando thumbnail simples..."
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
                    quantidade_perguntas=quantidade,
                    texto_chamada=chamada,
                    nome_arquivo="thumbnail.png"
                )
            )

            self.exibir_thumbnail(
                caminho
            )

            self.status.configure(
                text=(
                    "Thumbnail simples gerada "
                    f"com sucesso: {caminho}"
                )
            )

        except Exception as erro:
            self._mostrar_erro_thumbnail(
                erro
            )

    def _gerar_thumbnail_escolhas(self):
        if self.caminho_imagem_esquerda is None:
            self.status.configure(
                text="Selecione a imagem esquerda."
            )
            return

        if self.caminho_imagem_direita is None:
            self.status.configure(
                text="Selecione a imagem direita."
            )
            return

        if not self.caminho_imagem_esquerda.exists():
            self.status.configure(
                text=(
                    "A imagem esquerda não foi encontrada. "
                    "Selecione-a novamente."
                )
            )
            return

        if not self.caminho_imagem_direita.exists():
            self.status.configure(
                text=(
                    "A imagem direita não foi encontrada. "
                    "Selecione-a novamente."
                )
            )
            return

        titulo_superior = (
            self.campo_titulo_superior
            .get()
            .strip()
            or "O QUE VOCÊ PREFERE?"
        )

        texto_inferior = (
            self.campo_texto_inferior
            .get()
            .strip()
            or "FAÇA SUA ESCOLHA!"
        )

        texto_central = (
            self.campo_texto_central
            .get()
            .strip()
            or "OU"
        )

        self.status.configure(
            text=(
                "Gerando thumbnail "
                "O que você prefere?..."
            )
        )

        self.update_idletasks()

        try:
            caminho = (
                self.choice_thumbnail_generator
                .gerar(
                    pasta_projeto=(
                        self.pasta_projeto_atual
                    ),
                    imagem_esquerda=(
                        self.caminho_imagem_esquerda
                    ),
                    imagem_direita=(
                        self.caminho_imagem_direita
                    ),
                    titulo_superior=titulo_superior,
                    texto_inferior=texto_inferior,
                    texto_central=texto_central,
                    nome_arquivo="thumbnail_escolhas.png"
                )
            )

            self.exibir_thumbnail(
                caminho
            )

            self.status.configure(
                text=(
                    "Thumbnail elaborada gerada "
                    f"com sucesso: {caminho}"
                )
            )

        except Exception as erro:
            self._mostrar_erro_thumbnail(
                erro
            )

    def _mostrar_erro_thumbnail(
        self,
        erro
    ):
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
                text="Gere uma thumbnail primeiro."
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
        self._definir_entry(
            self.campo_titulo,
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

        self._definir_entry(
            self.campo_chamada_thumbnail,
            "VOCÊ CONSEGUE ACERTAR?"
        )

        self._definir_entry(
            self.campo_titulo_superior,
            "O QUE VOCÊ PREFERE?"
        )

        self._definir_entry(
            self.campo_texto_inferior,
            "FAÇA SUA ESCOLHA!"
        )

        self._definir_entry(
            self.campo_texto_central,
            "OU"
        )

        self.seletor_modelo_thumbnail.set(
            self.MODELO_SIMPLES
        )

        self.alterar_modelo_thumbnail(
            self.MODELO_SIMPLES
        )

        self.caminho_imagem_esquerda = None
        self.caminho_imagem_direita = None

        self._atualizar_rotulos_imagens()
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

        if not titulo:
            self.status.configure(
                text="O título não pode ficar vazio."
            )
            return

        if not descricao:
            self.status.configure(
                text="A descrição não pode ficar vazia."
            )
            return

        if not tags:
            self.status.configure(
                text="As tags não podem ficar vazias."
            )
            return

        dados = {
            "titulo": titulo,
            "descricao": descricao,
            "tags": tags,

            "modelo_thumbnail": (
                self.seletor_modelo_thumbnail.get()
            ),

            "chamada_thumbnail": (
                self.campo_chamada_thumbnail
                .get()
                .strip()
            ),

            "titulo_superior_thumbnail": (
                self.campo_titulo_superior
                .get()
                .strip()
            ),

            "texto_inferior_thumbnail": (
                self.campo_texto_inferior
                .get()
                .strip()
            ),

            "texto_central_thumbnail": (
                self.campo_texto_central
                .get()
                .strip()
            ),

            "imagem_esquerda_thumbnail": (
                str(
                    self.caminho_imagem_esquerda
                )
                if self.caminho_imagem_esquerda
                else ""
            ),

            "imagem_direita_thumbnail": (
                str(
                    self.caminho_imagem_direita
                )
                if self.caminho_imagem_direita
                else ""
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
                text="Selecione um projeto primeiro."
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

    def _obter_quantidade(
        self,
        configuracao,
        perguntas
    ):
        quantidade = configuracao.get(
            "quantidade_perguntas",
            len(perguntas)
        )

        try:
            return int(
                quantidade
            )

        except (
            TypeError,
            ValueError
        ):
            return len(
                perguntas
            )

    def _definir_entry(
        self,
        campo,
        valor
    ):
        campo.delete(
            0,
            "end"
        )

        campo.insert(
            0,
            str(
                valor
            )
        )

    def _atualizar_rotulos_imagens(self):
        if (
            self.caminho_imagem_esquerda
            and self.caminho_imagem_esquerda.exists()
        ):
            texto_esquerda = (
                self.caminho_imagem_esquerda.name
            )
        else:
            texto_esquerda = (
                "Nenhuma imagem selecionada."
            )

        if (
            self.caminho_imagem_direita
            and self.caminho_imagem_direita.exists()
        ):
            texto_direita = (
                self.caminho_imagem_direita.name
            )
        else:
            texto_direita = (
                "Nenhuma imagem selecionada."
            )

        self.rotulo_imagem_esquerda.configure(
            text=texto_esquerda
        )

        self.rotulo_imagem_direita.configure(
            text=texto_direita
        )
