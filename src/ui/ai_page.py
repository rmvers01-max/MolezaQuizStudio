import json
import os
import threading
from pathlib import Path
from tkinter import filedialog, messagebox

import customtkinter as ctk

from core.ai import (
    AIContentGenerator,
    AIContentRequest,
    OpenAIResponsesProvider,
)


class AIPage(ctk.CTkFrame):
    """Central de geração de conteúdo do Moleza Quiz Studio."""

    def __init__(self, master):
        super().__init__(master)

        self.resultado_atual = None
        self.gerando = False

        self._criar_interface()
        self._carregar_padrao_ambiente()

    def _criar_interface(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._criar_cabecalho()
        self._criar_conteudo()

    def _criar_cabecalho(self):
        cabecalho = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )
        cabecalho.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=28,
            pady=(22, 12),
        )
        cabecalho.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            cabecalho,
            text="Central de IA",
            font=("Arial", 28, "bold"),
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            cabecalho,
            text=(
                "Gere títulos, SEO, roteiro de perguntas "
                "e direção criativa para a thumbnail."
            ),
            text_color="gray70",
        ).grid(row=1, column=0, sticky="w", pady=(4, 0))

        self.botao_gerar = ctk.CTkButton(
            cabecalho,
            text="✨ Gerar pacote completo",
            width=210,
            height=42,
            command=self.gerar_conteudo,
        )
        self.botao_gerar.grid(
            row=0,
            column=1,
            rowspan=2,
            padx=(15, 0),
        )

    def _criar_conteudo(self):
        conteudo = ctk.CTkFrame(self)
        conteudo.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=28,
            pady=(0, 25),
        )
        conteudo.grid_columnconfigure(1, weight=1)
        conteudo.grid_rowconfigure(0, weight=1)

        self._criar_formulario(conteudo)
        self._criar_resultado(conteudo)

    def _criar_formulario(self, master):
        painel = ctk.CTkScrollableFrame(
            master,
            width=390,
        )
        painel.grid(
            row=0,
            column=0,
            sticky="ns",
            padx=(10, 5),
            pady=10,
        )
        painel.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            painel,
            text="Configuração da geração",
            font=("Arial", 19, "bold"),
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=10,
            pady=(12, 16),
        )

        self.campo_tema = self._campo(
            painel,
            1,
            "Tema do vídeo",
            "Ex.: O que você prefere? Edição doces",
        )

        self.publico = self._opcao(
            painel,
            2,
            "Público",
            ["Família", "Infantil", "Adolescentes", "Geral"],
            "Família",
        )

        self.formato = self._opcao(
            painel,
            3,
            "Formato",
            ["Vídeo longo", "Shorts", "TikTok/Reels"],
            "Vídeo longo",
        )

        self.quantidade = self._campo(
            painel,
            4,
            "Quantidade de perguntas",
            "10",
        )

        self.estilo = self._campo(
            painel,
            5,
            "Estilo",
            "Infantil, alegre e colorido",
        )

        ctk.CTkLabel(
            painel,
            text="Observações",
        ).grid(
            row=6,
            column=0,
            sticky="w",
            padx=10,
            pady=(10, 5),
        )

        self.observacoes = ctk.CTkTextbox(
            painel,
            height=90,
        )
        self.observacoes.grid(
            row=7,
            column=0,
            sticky="ew",
            padx=10,
        )

        ctk.CTkFrame(
            painel,
            height=1,
            fg_color="gray35",
        ).grid(
            row=8,
            column=0,
            sticky="ew",
            padx=10,
            pady=18,
        )

        ctk.CTkLabel(
            painel,
            text="Provedor de IA",
            font=("Arial", 17, "bold"),
        ).grid(
            row=9,
            column=0,
            sticky="w",
            padx=10,
            pady=(0, 10),
        )

        self.campo_base_url = self._campo(
            painel,
            10,
            "Endereço da API",
            "https://api.openai.com/v1",
        )

        self.campo_modelo = self._campo(
            painel,
            11,
            "Modelo",
            "gpt-5-mini",
        )

        ctk.CTkLabel(
            painel,
            text="Chave da API",
        ).grid(
            row=12,
            column=0,
            sticky="w",
            padx=10,
            pady=(10, 5),
        )

        self.campo_api_key = ctk.CTkEntry(
            painel,
            show="•",
        )
        self.campo_api_key.grid(
            row=13,
            column=0,
            sticky="ew",
            padx=10,
        )

        ctk.CTkLabel(
            painel,
            text=(
                "A chave fica somente na memória nesta versão "
                "e não é salva pelo programa."
            ),
            text_color="gray65",
            wraplength=340,
            justify="left",
        ).grid(
            row=14,
            column=0,
            sticky="w",
            padx=10,
            pady=(7, 14),
        )

    def _criar_resultado(self, master):
        painel = ctk.CTkFrame(master)
        painel.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(5, 10),
            pady=10,
        )
        painel.grid_columnconfigure(0, weight=1)
        painel.grid_rowconfigure(1, weight=1)

        barra = ctk.CTkFrame(
            painel,
            fg_color="transparent",
        )
        barra.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=15,
            pady=(12, 8),
        )
        barra.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            barra,
            text="Resultado",
            font=("Arial", 19, "bold"),
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkButton(
            barra,
            text="Copiar",
            width=90,
            fg_color="gray35",
            hover_color="gray25",
            command=self.copiar_resultado,
        ).grid(row=0, column=1, padx=4)

        ctk.CTkButton(
            barra,
            text="Salvar JSON",
            width=105,
            command=self.salvar_json,
        ).grid(row=0, column=2, padx=4)

        ctk.CTkButton(
            barra,
            text="Salvar TXT",
            width=100,
            command=self.salvar_txt,
        ).grid(row=0, column=3, padx=4)

        self.saida = ctk.CTkTextbox(
            painel,
            font=("Consolas", 13),
            wrap="word",
        )
        self.saida.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=15,
            pady=(0, 10),
        )
        self.saida.insert(
            "1.0",
            (
                "Informe o tema e a chave da API, "
                "depois clique em “Gerar pacote completo”."
            ),
        )
        self.saida.configure(state="disabled")

        self.status = ctk.CTkLabel(
            painel,
            text="Pronto.",
            text_color="gray70",
            anchor="w",
        )
        self.status.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=15,
            pady=(0, 12),
        )

    def _campo(self, master, linha, titulo, placeholder):
        ctk.CTkLabel(
            master,
            text=titulo,
        ).grid(
            row=linha * 2 - 1,
            column=0,
            sticky="w",
            padx=10,
            pady=(10, 5),
        )

        campo = ctk.CTkEntry(
            master,
            placeholder_text=placeholder,
        )
        campo.grid(
            row=linha * 2,
            column=0,
            sticky="ew",
            padx=10,
        )
        return campo

    def _opcao(
        self,
        master,
        linha,
        titulo,
        valores,
        padrao,
    ):
        ctk.CTkLabel(
            master,
            text=titulo,
        ).grid(
            row=linha * 2 - 1,
            column=0,
            sticky="w",
            padx=10,
            pady=(10, 5),
        )

        menu = ctk.CTkOptionMenu(
            master,
            values=valores,
        )
        menu.grid(
            row=linha * 2,
            column=0,
            sticky="ew",
            padx=10,
        )
        menu.set(padrao)
        return menu

    def _carregar_padrao_ambiente(self):
        self._definir_entry(
            self.campo_base_url,
            os.getenv(
                "MOLEZA_AI_BASE_URL",
                "https://api.openai.com/v1",
            ),
        )
        self._definir_entry(
            self.campo_modelo,
            os.getenv(
                "MOLEZA_AI_MODEL",
                "gpt-5-mini",
            ),
        )

        chave = os.getenv("OPENAI_API_KEY", "")
        if chave:
            self._definir_entry(self.campo_api_key, chave)

    def gerar_conteudo(self):
        if self.gerando:
            return

        try:
            quantidade = int(
                self.quantidade.get().strip() or "10"
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
                observacoes=self.observacoes.get(
                    "1.0",
                    "end",
                ).strip(),
            )
            pedido.validar()

            provider = OpenAIResponsesProvider(
                api_key=self.campo_api_key.get(),
                model=self.campo_modelo.get(),
                base_url=self.campo_base_url.get(),
            )

        except ValueError as erro:
            messagebox.showerror(
                "Dados inválidos",
                str(erro),
                parent=self.winfo_toplevel(),
            )
            return

        self.gerando = True
        self.botao_gerar.configure(
            state="disabled",
            text="Gerando...",
        )
        self.status.configure(
            text="A IA está criando o pacote de conteúdo..."
        )

        thread = threading.Thread(
            target=self._executar_geracao,
            args=(pedido, provider),
            daemon=True,
        )
        thread.start()

    def _executar_geracao(self, pedido, provider):
        try:
            resultado = AIContentGenerator(provider).gerar(
                pedido
            )
            self.after(
                0,
                lambda: self._finalizar_sucesso(resultado),
            )

        except Exception as erro:
            self.after(
                0,
                lambda mensagem=str(erro): (
                    self._finalizar_erro(mensagem)
                ),
            )

    def _finalizar_sucesso(self, resultado):
        self.resultado_atual = resultado
        texto = self._formatar_resultado(resultado)

        self._definir_saida(texto)
        self.status.configure(
            text="Pacote gerado com sucesso."
        )
        self._restaurar_botao()

    def _finalizar_erro(self, mensagem):
        self.status.configure(text=f"Erro: {mensagem}")
        self._restaurar_botao()

        messagebox.showerror(
            "Erro na geração",
            mensagem,
            parent=self.winfo_toplevel(),
        )

    def _restaurar_botao(self):
        self.gerando = False
        self.botao_gerar.configure(
            state="normal",
            text="✨ Gerar pacote completo",
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
            "PERGUNTAS",
        ]

        for pergunta in resultado.perguntas:
            if isinstance(pergunta, dict):
                numero = pergunta.get("numero", "")
                enunciado = pergunta.get("pergunta", "")
                opcoes = pergunta.get("opcoes", [])
                resposta = pergunta.get("resposta", "")
                narracao = pergunta.get("narracao", "")

                linhas.extend([
                    "",
                    f"{numero}. {enunciado}",
                    f"Opções: {' | '.join(map(str, opcoes))}",
                    f"Resposta: {resposta}",
                    f"Narração: {narracao}",
                ])

        if resultado.observacoes_estrategicas:
            linhas.extend(["", "OBSERVAÇÕES ESTRATÉGICAS"])
            linhas.extend(
                f"• {item}"
                for item in resultado.observacoes_estrategicas
            )

        return "\n".join(linhas)

    def copiar_resultado(self):
        texto = self.saida.get("1.0", "end").strip()
        if not texto:
            return

        self.clipboard_clear()
        self.clipboard_append(texto)
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
            filetypes=[("Arquivo JSON", "*.json")],
        )
        if not caminho:
            return

        Path(caminho).write_text(
            json.dumps(
                self.resultado_atual.para_dict(),
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
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
            filetypes=[("Arquivo de texto", "*.txt")],
        )
        if not caminho:
            return

        Path(caminho).write_text(
            self.saida.get("1.0", "end").strip(),
            encoding="utf-8",
        )
        self.status.configure(
            text=f"TXT salvo: {caminho}"
        )

    def _avisar_sem_resultado(self):
        messagebox.showinfo(
            "Nenhum resultado",
            "Gere um pacote antes de salvar.",
            parent=self.winfo_toplevel(),
        )

    def _definir_saida(self, texto):
        self.saida.configure(state="normal")
        self.saida.delete("1.0", "end")
        self.saida.insert("1.0", texto)
        self.saida.configure(state="disabled")

    def _definir_entry(self, campo, valor):
        campo.delete(0, "end")
        campo.insert(0, str(valor))
