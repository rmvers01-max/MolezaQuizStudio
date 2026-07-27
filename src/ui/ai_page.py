import json
import os
import threading
from pathlib import Path
from tkinter import filedialog, messagebox

import customtkinter as ctk

from core.ai import (
    AIContentGenerator,
    AIContentRequest,
    AIProviderFactory,
)
from core.ai_project_service import AIProjectService
from core.project_manager import ProjectManager


class AIPage(ctk.CTkFrame):
    """Central de geração e integração de conteúdo por IA."""

    NOVO_PROJETO = "➕ Criar novo projeto com o tema"

    def __init__(self, master):
        super().__init__(master)

        self.project_manager = ProjectManager()
        self.project_service = AIProjectService(
            self.project_manager
        )

        self.resultado_atual = None
        self.pedido_atual = None
        self.pasta_projeto_atual = None
        self.projetos = {}
        self.gerando = False

        self._criar_interface()
        self._carregar_padrao_ambiente()
        self.carregar_projetos()

    def _criar_interface(self):
        self.grid_columnconfigure(
            0,
            weight=1
        )
        self.grid_rowconfigure(
            1,
            weight=1
        )

        self._criar_cabecalho()
        self._criar_conteudo()

    def _criar_cabecalho(self):
        cabecalho = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        cabecalho.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=28,
            pady=(22, 12)
        )
        cabecalho.grid_columnconfigure(
            0,
            weight=1
        )

        ctk.CTkLabel(
            cabecalho,
            text="Central de IA",
            font=("Arial", 28, "bold")
        ).grid(
            row=0,
            column=0,
            sticky="w"
        )

        ctk.CTkLabel(
            cabecalho,
            text=(
                "Gere o conteúdo e envie o quiz e o SEO "
                "diretamente para um projeto."
            ),
            text_color="gray70"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            pady=(4, 0)
        )

        self.botao_gerar = ctk.CTkButton(
            cabecalho,
            text="✨ Gerar pacote completo",
            width=210,
            height=42,
            command=self.gerar_conteudo
        )
        self.botao_gerar.grid(
            row=0,
            column=1,
            rowspan=2,
            padx=(15, 0)
        )

    def _criar_conteudo(self):
        conteudo = ctk.CTkFrame(
            self
        )
        conteudo.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=28,
            pady=(0, 25)
        )
        conteudo.grid_columnconfigure(
            1,
            weight=1
        )
        conteudo.grid_rowconfigure(
            0,
            weight=1
        )

        self._criar_formulario(
            conteudo
        )
        self._criar_resultado(
            conteudo
        )

    def _criar_formulario(self, master):
        painel = ctk.CTkScrollableFrame(
            master,
            width=390
        )
        painel.grid(
            row=0,
            column=0,
            sticky="ns",
            padx=(10, 5),
            pady=10
        )
        painel.grid_columnconfigure(
            0,
            weight=1
        )

        linha = 0

        ctk.CTkLabel(
            painel,
            text="Projeto de destino",
            font=("Arial", 19, "bold")
        ).grid(
            row=linha,
            column=0,
            sticky="w",
            padx=10,
            pady=(12, 10)
        )
        linha += 1

        self.seletor_projeto = ctk.CTkOptionMenu(
            painel,
            values=[self.NOVO_PROJETO],
            command=self._ao_selecionar_projeto
        )
        self.seletor_projeto.grid(
            row=linha,
            column=0,
            sticky="ew",
            padx=10
        )
        linha += 1

        ctk.CTkButton(
            painel,
            text="Atualizar projetos",
            fg_color="gray35",
            hover_color="gray25",
            command=self.carregar_projetos
        ).grid(
            row=linha,
            column=0,
            sticky="ew",
            padx=10,
            pady=(7, 14)
        )
        linha += 1

        self.rotulo_destino = ctk.CTkLabel(
            painel,
            text=(
                "Um novo projeto será criado usando o tema."
            ),
            text_color="gray65",
            wraplength=340,
            justify="left"
        )
        self.rotulo_destino.grid(
            row=linha,
            column=0,
            sticky="w",
            padx=10,
            pady=(0, 8)
        )
        linha += 1

        ctk.CTkFrame(
            painel,
            height=1,
            fg_color="gray35"
        ).grid(
            row=linha,
            column=0,
            sticky="ew",
            padx=10,
            pady=12
        )
        linha += 1

        ctk.CTkLabel(
            painel,
            text="Configuração da geração",
            font=("Arial", 19, "bold")
        ).grid(
            row=linha,
            column=0,
            sticky="w",
            padx=10,
            pady=(0, 8)
        )
        linha += 1

        self.campo_tema, linha = self._criar_campo(
            painel,
            linha,
            "Tema do vídeo",
            "Ex.: O que você prefere? Edição doces"
        )

        self.publico, linha = self._criar_opcao(
            painel,
            linha,
            "Público",
            [
                "Família",
                "Infantil",
                "Adolescentes",
                "Geral"
            ],
            "Família"
        )

        self.formato, linha = self._criar_opcao(
            painel,
            linha,
            "Formato",
            [
                "Vídeo longo",
                "Shorts",
                "TikTok/Reels"
            ],
            "Vídeo longo"
        )

        self.quantidade, linha = self._criar_campo(
            painel,
            linha,
            "Quantidade de perguntas",
            "10"
        )

        self.estilo, linha = self._criar_campo(
            painel,
            linha,
            "Estilo",
            "Infantil, alegre e colorido"
        )

        ctk.CTkLabel(
            painel,
            text="Observações"
        ).grid(
            row=linha,
            column=0,
            sticky="w",
            padx=10,
            pady=(10, 5)
        )
        linha += 1

        self.observacoes = ctk.CTkTextbox(
            painel,
            height=90
        )
        self.observacoes.grid(
            row=linha,
            column=0,
            sticky="ew",
            padx=10
        )
        linha += 1

        ctk.CTkFrame(
            painel,
            height=1,
            fg_color="gray35"
        ).grid(
            row=linha,
            column=0,
            sticky="ew",
            padx=10,
            pady=18
        )
        linha += 1

        ctk.CTkLabel(
            painel,
            text="Provedor de IA",
            font=("Arial", 17, "bold")
        ).grid(
            row=linha,
            column=0,
            sticky="w",
            padx=10,
            pady=(0, 8)
        )
        linha += 1

        self.provedor, linha = self._criar_opcao(
            painel,
            linha,
            "Provedor",
            AIProviderFactory.PROVEDORES,
            AIProviderFactory.OPENAI
        )
        self.provedor.configure(
            command=self._ao_alterar_provedor
        )

        self.campo_base_url, linha = self._criar_campo(
            painel,
            linha,
            "Endereço da API",
            "https://api.openai.com/v1"
        )

        self.campo_modelo, linha = self._criar_campo(
            painel,
            linha,
            "Modelo",
            "gpt-5-mini"
        )

        ctk.CTkLabel(
            painel,
            text="Chave da API"
        ).grid(
            row=linha,
            column=0,
            sticky="w",
            padx=10,
            pady=(10, 5)
        )
        linha += 1

        self.campo_api_key = ctk.CTkEntry(
            painel,
            show="•"
        )
        self.campo_api_key.grid(
            row=linha,
            column=0,
            sticky="ew",
            padx=10
        )
        linha += 1

        ctk.CTkLabel(
            painel,
            text=(
                "A chave permanece somente na memória "
                "e não é salva nos arquivos do projeto."
            ),
            text_color="gray65",
            wraplength=340,
            justify="left"
        ).grid(
            row=linha,
            column=0,
            sticky="w",
            padx=10,
            pady=(7, 14)
        )

    def _criar_resultado(self, master):
        painel = ctk.CTkFrame(
            master
        )
        painel.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(5, 10),
            pady=10
        )
        painel.grid_columnconfigure(
            0,
            weight=1
        )
        painel.grid_rowconfigure(
            1,
            weight=1
        )

        barra = ctk.CTkFrame(
            painel,
            fg_color="transparent"
        )
        barra.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=15,
            pady=(12, 8)
        )
        barra.grid_columnconfigure(
            0,
            weight=1
        )

        ctk.CTkLabel(
            barra,
            text="Resultado",
            font=("Arial", 19, "bold")
        ).grid(
            row=0,
            column=0,
            sticky="w"
        )

        ctk.CTkButton(
            barra,
            text="Salvar no projeto",
            width=135,
            command=self.salvar_no_projeto
        ).grid(
            row=0,
            column=1,
            padx=4
        )

        ctk.CTkButton(
            barra,
            text="Copiar",
            width=85,
            fg_color="gray35",
            hover_color="gray25",
            command=self.copiar_resultado
        ).grid(
            row=0,
            column=2,
            padx=4
        )

        ctk.CTkButton(
            barra,
            text="Salvar JSON",
            width=105,
            command=self.salvar_json
        ).grid(
            row=0,
            column=3,
            padx=4
        )

        ctk.CTkButton(
            barra,
            text="Salvar TXT",
            width=100,
            command=self.salvar_txt
        ).grid(
            row=0,
            column=4,
            padx=4
        )

        self.saida = ctk.CTkTextbox(
            painel,
            font=("Consolas", 13),
            wrap="word"
        )
        self.saida.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=15,
            pady=(0, 10)
        )
        self.saida.insert(
            "1.0",
            (
                "Escolha o projeto, informe o tema e a chave "
                "da API e clique em “Gerar pacote completo”."
            )
        )
        self.saida.configure(
            state="disabled"
        )

        self.status = ctk.CTkLabel(
            painel,
            text="Pronto.",
            text_color="gray70",
            anchor="w",
            wraplength=850
        )
        self.status.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=15,
            pady=(0, 12)
        )

    def _criar_campo(
        self,
        master,
        linha,
        titulo,
        placeholder
    ):
        ctk.CTkLabel(
            master,
            text=titulo
        ).grid(
            row=linha,
            column=0,
            sticky="w",
            padx=10,
            pady=(10, 5)
        )
        linha += 1

        campo = ctk.CTkEntry(
            master,
            placeholder_text=placeholder
        )
        campo.grid(
            row=linha,
            column=0,
            sticky="ew",
            padx=10
        )

        return campo, linha + 1

    def _criar_opcao(
        self,
        master,
        linha,
        titulo,
        valores,
        padrao
    ):
        ctk.CTkLabel(
            master,
            text=titulo
        ).grid(
            row=linha,
            column=0,
            sticky="w",
            padx=10,
            pady=(10, 5)
        )
        linha += 1

        menu = ctk.CTkOptionMenu(
            master,
            values=valores
        )
        menu.grid(
            row=linha,
            column=0,
            sticky="ew",
            padx=10
        )
        menu.set(
            padrao
        )

        return menu, linha + 1

    def carregar_projetos(self):
        projetos = (
            self.project_manager
            .listar_projetos()
        )

        self.projetos = {
            projeto.name: projeto
            for projeto in projetos
        }

        valores = [
            self.NOVO_PROJETO,
            *self.projetos.keys()
        ]

        self.seletor_projeto.configure(
            values=valores
        )

        atual = self.seletor_projeto.get()

        if atual not in valores:
            atual = self.NOVO_PROJETO

        self.seletor_projeto.set(
            atual
        )

        self._ao_selecionar_projeto(
            atual
        )

    def _ao_selecionar_projeto(
        self,
        nome
    ):
        if nome == self.NOVO_PROJETO:
            self.pasta_projeto_atual = None
            self.rotulo_destino.configure(
                text=(
                    "Um novo projeto será criado usando o tema."
                )
            )
            return

        self.pasta_projeto_atual = (
            self.projetos.get(
                nome
            )
        )

        if self.pasta_projeto_atual:
            self.rotulo_destino.configure(
                text=(
                    "Destino: "
                    f"{self.pasta_projeto_atual}"
                )
            )

            configuracao = (
                self.project_manager
                .carregar_configuracao_projeto(
                    self.pasta_projeto_atual
                )
            )

            tema = configuracao.get(
                "tema",
                ""
            )

            if tema and not self.campo_tema.get().strip():
                self._definir_entry(
                    self.campo_tema,
                    tema
                )

    def _ao_alterar_provedor(self, provedor):
        configuracoes = {
            AIProviderFactory.SIMULACAO: {
                "url": "offline",
                "modelo": "simulador-moleza",
            },
            AIProviderFactory.OPENAI: {
                "url": "https://api.openai.com/v1",
                "modelo": "gpt-5-mini",
            },
            AIProviderFactory.OPENROUTER: {
                "url": "https://openrouter.ai/api/v1",
                "modelo": "openai/gpt-4.1-mini",
            },
            AIProviderFactory.OLLAMA: {
                "url": "http://localhost:11434",
                "modelo": "llama3.2",
            },
            AIProviderFactory.LM_STUDIO: {
                "url": "http://localhost:1234/v1",
                "modelo": "modelo-local",
            },
            AIProviderFactory.COMPATIVEL: {
                "url": "",
                "modelo": "",
            },
        }

        configuracao = configuracoes.get(
            provedor,
            configuracoes[AIProviderFactory.OPENAI]
        )

        self._definir_entry(
            self.campo_base_url,
            configuracao["url"]
        )
        self._definir_entry(
            self.campo_modelo,
            configuracao["modelo"]
        )

        simulacao = (
            provedor
            == AIProviderFactory.SIMULACAO
        )

        chave_obrigatoria = provedor in {
            AIProviderFactory.OPENAI,
            AIProviderFactory.OPENROUTER,
        }

        self.campo_api_key.configure(
            placeholder_text=(
                "Não utilizada no modo simulação"
                if simulacao
                else (
                    "Obrigatória"
                    if chave_obrigatoria
                    else "Opcional para servidor local"
                )
            ),
            state=(
                "disabled"
                if simulacao
                else "normal"
            )
        )

        self.campo_base_url.configure(
            state=(
                "disabled"
                if simulacao
                else "normal"
            )
        )

        self.campo_modelo.configure(
            state=(
                "disabled"
                if simulacao
                else "normal"
            )
        )

        if hasattr(self, "status") and simulacao:
            self.status.configure(
                text=(
                    "Modo Simulação ativo: não usa internet "
                    "nem créditos de API."
                )
            )

    def _carregar_padrao_ambiente(self):
        provedor = os.getenv(
            "MOLEZA_AI_PROVIDER",
            AIProviderFactory.SIMULACAO
        )

        if provedor not in AIProviderFactory.PROVEDORES:
            provedor = AIProviderFactory.OPENAI

        self.provedor.set(
            provedor
        )
        self._ao_alterar_provedor(
            provedor
        )

        self._definir_entry(
            self.campo_base_url,
            os.getenv(
                "MOLEZA_AI_BASE_URL",
                "https://api.openai.com/v1"
            )
        )
        self._definir_entry(
            self.campo_modelo,
            os.getenv(
                "MOLEZA_AI_MODEL",
                "gpt-5-mini"
            )
        )

        chave = os.getenv(
            "OPENAI_API_KEY",
            ""
        )

        if chave:
            self._definir_entry(
                self.campo_api_key,
                chave
            )

    def gerar_conteudo(self):
        if self.gerando:
            return

        try:
            pedido, provider = (
                self._obter_pedido_provider()
            )

        except ValueError as erro:
            messagebox.showerror(
                "Dados inválidos",
                str(erro),
                parent=self.winfo_toplevel()
            )
            return

        self.pedido_atual = pedido
        self.gerando = True

        self.botao_gerar.configure(
            state="disabled",
            text="Gerando..."
        )
        self.status.configure(
            text=(
                "Gerando conteúdo em modo simulação..."
                if (
                    self.provedor.get()
                    == AIProviderFactory.SIMULACAO
                )
                else "A IA está criando o pacote de conteúdo..."
            )
        )

        thread = threading.Thread(
            target=self._executar_geracao,
            args=(pedido, provider),
            daemon=True
        )
        thread.start()

    def _obter_pedido_provider(self):
        quantidade = int(
            self.quantidade.get().strip()
            or "10"
        )

        pedido = AIContentRequest(
            tema=self.campo_tema.get().strip(),
            publico=self.publico.get(),
            formato=self.formato.get(),
            quantidade_perguntas=quantidade,
            estilo=(
                self.estilo.get().strip()
                or "Infantil, alegre e colorido"
            ),
            observacoes=(
                self.observacoes
                .get("1.0", "end")
                .strip()
            )
        )
        pedido.validar()

        provider = AIProviderFactory.criar(
            provedor=self.provedor.get(),
            api_key=self.campo_api_key.get(),
            model=self.campo_modelo.get(),
            base_url=self.campo_base_url.get()
        )

        return pedido, provider

    def _executar_geracao(
        self,
        pedido,
        provider
    ):
        try:
            resultado = (
                AIContentGenerator(provider)
                .gerar(pedido)
            )

            self.after(
                0,
                lambda: self._finalizar_sucesso(
                    pedido,
                    resultado
                )
            )

        except Exception as erro:
            self.after(
                0,
                lambda mensagem=str(erro): (
                    self._finalizar_erro(
                        mensagem
                    )
                )
            )

    def _finalizar_sucesso(
        self,
        pedido,
        resultado
    ):
        self.pedido_atual = pedido
        self.resultado_atual = resultado

        self._definir_saida(
            self._formatar_resultado(
                resultado
            )
        )

        try:
            caminhos = (
                self._salvar_resultado_no_projeto()
            )

            self.status.configure(
                text=(
                    "Pacote gerado e salvo. "
                    f"Quiz: {caminhos['quiz'].name}; "
                    "Publicação pronta para carregar."
                )
            )

        except Exception as erro:
            self.status.configure(
                text=(
                    "Pacote gerado, mas não foi possível "
                    f"salvar no projeto: {erro}"
                )
            )

        self._restaurar_botao()

    def salvar_no_projeto(self):
        if (
            self.resultado_atual is None
            or self.pedido_atual is None
        ):
            self._avisar_sem_resultado()
            return

        try:
            caminhos = (
                self._salvar_resultado_no_projeto()
            )

            messagebox.showinfo(
                "Conteúdo salvo",
                (
                    "Os arquivos foram atualizados:\n\n"
                    f"{caminhos['ai_content']}\n"
                    f"{caminhos['quiz']}\n"
                    f"{caminhos['publicacao']}"
                ),
                parent=self.winfo_toplevel()
            )

            self.status.configure(
                text=(
                    "Conteúdo salvo no projeto com sucesso."
                )
            )

        except Exception as erro:
            messagebox.showerror(
                "Erro ao salvar no projeto",
                str(erro),
                parent=self.winfo_toplevel()
            )

    def _salvar_resultado_no_projeto(self):
        pasta = self._obter_ou_criar_projeto()

        caminhos = (
            self.project_service
            .salvar_resultado(
                pasta_projeto=pasta,
                pedido=self.pedido_atual,
                resultado=self.resultado_atual
            )
        )

        self.pasta_projeto_atual = pasta
        self.carregar_projetos()
        self.seletor_projeto.set(
            pasta.name
        )
        self._ao_selecionar_projeto(
            pasta.name
        )

        return caminhos

    def _obter_ou_criar_projeto(self):
        selecionado = (
            self.seletor_projeto.get()
        )

        if (
            selecionado != self.NOVO_PROJETO
            and selecionado in self.projetos
        ):
            return self.projetos[
                selecionado
            ]

        tema = (
            self.pedido_atual.tema
            if self.pedido_atual
            else self.campo_tema.get().strip()
        )

        return (
            self.project_manager
            .criar_projeto(
                tema
            )
        )

    def _finalizar_erro(self, mensagem):
        self.status.configure(
            text=f"Erro: {mensagem}"
        )
        self._restaurar_botao()

        messagebox.showerror(
            "Erro na geração",
            mensagem,
            parent=self.winfo_toplevel()
        )

    def _restaurar_botao(self):
        self.gerando = False
        self.botao_gerar.configure(
            state="normal",
            text="✨ Gerar pacote completo"
        )

    def _formatar_resultado(self, resultado):
        linhas = [
            "TÍTULO",
            resultado.titulo,
            "",
            "TÍTULO ALTERNATIVO",
            resultado.titulo_alternativo,
            "",
            "TEXTO DA THUMBNAIL",
            resultado.texto_thumbnail,
            "",
            "PROMPT DA THUMBNAIL",
            resultado.prompt_thumbnail,
            "",
            "DESCRIÇÃO",
            resultado.descricao,
            "",
            "HASHTAGS",
            " ".join(resultado.hashtags),
            "",
            "TAGS",
            ", ".join(resultado.tags),
            "",
            "INTRODUÇÃO",
            resultado.introducao,
            "",
            "CHAMADA PARA INSCRIÇÃO",
            resultado.chamada_inscricao,
            "",
            "PERGUNTAS"
        ]

        for pergunta in resultado.perguntas:
            if not isinstance(
                pergunta,
                dict
            ):
                continue

            numero = pergunta.get(
                "numero",
                ""
            )
            enunciado = pergunta.get(
                "pergunta",
                ""
            )
            opcoes = pergunta.get(
                "opcoes",
                pergunta.get(
                    "alternativas",
                    []
                )
            )
            resposta = pergunta.get(
                "resposta",
                ""
            )
            narracao = pergunta.get(
                "narracao",
                ""
            )

            linhas.extend([
                "",
                f"{numero}. {enunciado}",
                (
                    "Opções: "
                    f"{' | '.join(map(str, opcoes))}"
                ),
                f"Resposta: {resposta}",
                f"Narração: {narracao}"
            ])

        if resultado.observacoes_estrategicas:
            linhas.extend([
                "",
                "OBSERVAÇÕES ESTRATÉGICAS"
            ])
            linhas.extend(
                f"• {item}"
                for item in (
                    resultado
                    .observacoes_estrategicas
                )
            )

        return "\n".join(
            linhas
        )

    def copiar_resultado(self):
        texto = (
            self.saida
            .get("1.0", "end")
            .strip()
        )

        if not texto:
            return

        self.clipboard_clear()
        self.clipboard_append(
            texto
        )
        self.status.configure(
            text="Resultado copiado."
        )

    def salvar_json(self):
        if self.resultado_atual is None:
            self._avisar_sem_resultado()
            return

        caminho = filedialog.asksaveasfilename(
            parent=self.winfo_toplevel(),
            title="Salvar pacote de IA",
            defaultextension=".json",
            filetypes=[
                ("Arquivo JSON", "*.json")
            ]
        )

        if not caminho:
            return

        Path(caminho).write_text(
            json.dumps(
                self.resultado_atual.para_dict(),
                ensure_ascii=False,
                indent=2
            ),
            encoding="utf-8"
        )

        self.status.configure(
            text=f"JSON salvo: {caminho}"
        )

    def salvar_txt(self):
        if self.resultado_atual is None:
            self._avisar_sem_resultado()
            return

        caminho = filedialog.asksaveasfilename(
            parent=self.winfo_toplevel(),
            title="Salvar conteúdo",
            defaultextension=".txt",
            filetypes=[
                ("Arquivo de texto", "*.txt")
            ]
        )

        if not caminho:
            return

        Path(caminho).write_text(
            self.saida.get(
                "1.0",
                "end"
            ).strip(),
            encoding="utf-8"
        )

        self.status.configure(
            text=f"TXT salvo: {caminho}"
        )

    def _avisar_sem_resultado(self):
        messagebox.showinfo(
            "Nenhum resultado",
            "Gere um pacote antes de salvar.",
            parent=self.winfo_toplevel()
        )

    def _definir_saida(
        self,
        texto
    ):
        self.saida.configure(
            state="normal"
        )
        self.saida.delete(
            "1.0",
            "end"
        )
        self.saida.insert(
            "1.0",
            texto
        )
        self.saida.configure(
            state="disabled"
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
            str(valor)
        )
