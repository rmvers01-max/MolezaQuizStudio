from copy import deepcopy
from pathlib import Path
from uuid import uuid4
from tkinter import colorchooser, filedialog, messagebox

import customtkinter as ctk

from core.thumbnail_document_manager import ThumbnailDocumentManager
from core.thumbnail_document_renderer import ThumbnailDocumentRenderer
from core.thumbnail_elements import (
    ImageElement,
    ShapeElement,
    TextElement,
    ThumbnailDocument
)
from ui.thumbnail_canvas import ThumbnailCanvas
from ui.thumbnail_editor_history import ThumbnailEditorHistoryController


class ThumbnailEditorPage(ctk.CTkFrame):
    """
    Editor visual de thumbnails.

    Recursos atuais:
    - adicionar textos, imagens e formas;
    - selecionar e arrastar elementos;
    - alterar posição e tamanho;
    - alterar textos e cores;
    - selecionar cores usando a paleta do Windows;
    - organizar camadas;
    - salvar e abrir documentos JSON;
    - exportar PNG ou JPG.
    """

    COR_PADRAO = "#FFFFFF"
    COR_CONTORNO_PADRAO = "#000000"

    def __init__(self, master):
        super().__init__(master)

        self.document_manager = ThumbnailDocumentManager()
        self.document_renderer = ThumbnailDocumentRenderer()

        self.elemento_selecionado = None
        self.elemento_copiado = None
        self.caminho_documento_atual = None
        self.documento_alterado = False

        self.historico_editor = ThumbnailEditorHistoryController(
            owner=self,
            obter_documento=self._obter_documento_atual,
            restaurar_documento=self._restaurar_documento_historico,
            limite=60
        )

        self.criar_interface()
        self.criar_documento_inicial()
        self.historico_editor.vincular_atalhos()
        self._vincular_atalhos_edicao()

    def criar_interface(self):
        self.grid_columnconfigure(
            0,
            weight=1
        )

        self.grid_rowconfigure(
            1,
            weight=1
        )

        self._criar_cabecalho()
        self._criar_area_editor()

    # =========================================================
    # CABEÇALHO
    # =========================================================

    def _criar_cabecalho(self):
        cabecalho = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        cabecalho.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=25,
            pady=(20, 12)
        )

        cabecalho.grid_columnconfigure(
            0,
            weight=1
        )

        area_titulo = ctk.CTkFrame(
            cabecalho,
            fg_color="transparent"
        )

        area_titulo.grid(
            row=0,
            column=0,
            sticky="w"
        )

        ctk.CTkLabel(
            area_titulo,
            text="Editor de Thumbnail",
            font=("Arial", 28, "bold")
        ).pack(
            anchor="w"
        )

        self.rotulo_arquivo = ctk.CTkLabel(
            area_titulo,
            text="Novo documento",
            text_color="gray70"
        )

        self.rotulo_arquivo.pack(
            anchor="w",
            pady=(4, 0)
        )

        area_botoes = ctk.CTkFrame(
            cabecalho,
            fg_color="transparent"
        )

        area_botoes.grid(
            row=0,
            column=1,
            sticky="e"
        )

        self.historico_editor.criar_botoes(
            area_botoes
        )

        ctk.CTkFrame(
            area_botoes,
            width=1,
            height=28,
            fg_color="gray35"
        ).pack(
            side="left",
            padx=6
        )

        ctk.CTkButton(
            area_botoes,
            text="Novo",
            width=90,
            command=self.novo_documento
        ).pack(
            side="left",
            padx=4
        )

        ctk.CTkButton(
            area_botoes,
            text="Abrir",
            width=90,
            command=self.abrir_documento
        ).pack(
            side="left",
            padx=4
        )

        ctk.CTkButton(
            area_botoes,
            text="Salvar",
            width=90,
            command=self.salvar_documento
        ).pack(
            side="left",
            padx=4
        )

        ctk.CTkButton(
            area_botoes,
            text="Salvar como",
            width=110,
            fg_color="gray35",
            hover_color="gray25",
            command=self.salvar_documento_como
        ).pack(
            side="left",
            padx=4
        )

        ctk.CTkButton(
            area_botoes,
            text="Exportar PNG",
            width=120,
            command=self.exportar_png
        ).pack(
            side="left",
            padx=4
        )

        ctk.CTkButton(
            area_botoes,
            text="Exportar JPG",
            width=120,
            fg_color="#8B5CF6",
            hover_color="#7C3AED",
            command=self.exportar_jpg
        ).pack(
            side="left",
            padx=4
        )

    # =========================================================
    # ÁREA PRINCIPAL
    # =========================================================

    def _criar_area_editor(self):
        area = ctk.CTkFrame(
            self
        )

        area.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=25,
            pady=(0, 25)
        )

        area.grid_columnconfigure(
            1,
            weight=1
        )

        area.grid_rowconfigure(
            0,
            weight=1
        )

        self._criar_barra_ferramentas(
            area
        )

        self._criar_area_canvas(
            area
        )

        self._criar_painel_lateral(
            area
        )

    # =========================================================
    # BARRA DE FERRAMENTAS
    # =========================================================

    def _criar_barra_ferramentas(
        self,
        area
    ):
        barra = ctk.CTkFrame(
            area,
            width=175
        )

        barra.grid(
            row=0,
            column=0,
            sticky="ns",
            padx=(10, 5),
            pady=10
        )

        barra.grid_propagate(
            False
        )

        ctk.CTkLabel(
            barra,
            text="Elementos",
            font=("Arial", 18, "bold")
        ).pack(
            pady=(20, 15)
        )

        ctk.CTkButton(
            barra,
            text="Adicionar texto",
            width=145,
            command=self.adicionar_texto
        ).pack(
            pady=6
        )

        ctk.CTkButton(
            barra,
            text="Adicionar imagem",
            width=145,
            command=self.adicionar_imagem
        ).pack(
            pady=6
        )

        ctk.CTkButton(
            barra,
            text="Retângulo",
            width=145,
            command=self.adicionar_retangulo
        ).pack(
            pady=6
        )

        ctk.CTkButton(
            barra,
            text="Círculo",
            width=145,
            command=self.adicionar_circulo
        ).pack(
            pady=6
        )

        ctk.CTkFrame(
            barra,
            height=2,
            fg_color="gray35"
        ).pack(
            fill="x",
            padx=15,
            pady=14
        )

        ctk.CTkLabel(
            barra,
            text="Edição",
            font=("Arial", 16, "bold")
        ).pack(
            pady=(0, 10)
        )

        ctk.CTkButton(
            barra,
            text="Copiar",
            width=145,
            fg_color="gray35",
            hover_color="gray25",
            command=self.copiar_elemento
        ).pack(
            pady=5
        )

        ctk.CTkButton(
            barra,
            text="Colar",
            width=145,
            fg_color="gray35",
            hover_color="gray25",
            command=self.colar_elemento
        ).pack(
            pady=5
        )

        ctk.CTkButton(
            barra,
            text="Duplicar",
            width=145,
            fg_color="gray35",
            hover_color="gray25",
            command=self.duplicar_elemento
        ).pack(
            pady=5
        )

        ctk.CTkFrame(
            barra,
            height=2,
            fg_color="gray35"
        ).pack(
            fill="x",
            padx=15,
            pady=18
        )

        ctk.CTkLabel(
            barra,
            text="Organização",
            font=("Arial", 16, "bold")
        ).pack(
            pady=(0, 10)
        )

        ctk.CTkButton(
            barra,
            text="Trazer para frente",
            width=145,
            fg_color="gray35",
            hover_color="gray25",
            command=self.trazer_para_frente
        ).pack(
            pady=5
        )

        ctk.CTkButton(
            barra,
            text="Enviar para trás",
            width=145,
            fg_color="gray35",
            hover_color="gray25",
            command=self.enviar_para_tras
        ).pack(
            pady=5
        )

        ctk.CTkButton(
            barra,
            text="Excluir elemento",
            width=145,
            fg_color="#A63D40",
            hover_color="#7F2E31",
            command=self.excluir_elemento
        ).pack(
            pady=(18, 5)
        )

    # =========================================================
    # CANVAS
    # =========================================================

    def _criar_area_canvas(
        self,
        area
    ):
        painel_canvas = ctk.CTkFrame(
            area
        )

        painel_canvas.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=5,
            pady=10
        )

        painel_canvas.grid_columnconfigure(
            0,
            weight=1
        )

        painel_canvas.grid_rowconfigure(
            1,
            weight=1
        )

        ctk.CTkLabel(
            painel_canvas,
            text="Área de edição — 1280 × 720",
            font=("Arial", 16, "bold")
        ).grid(
            row=0,
            column=0,
            pady=(12, 8)
        )

        container_canvas = ctk.CTkFrame(
            painel_canvas,
            fg_color="#090C12"
        )

        container_canvas.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=15,
            pady=(0, 15)
        )

        container_canvas.grid_columnconfigure(
            0,
            weight=1
        )

        container_canvas.grid_rowconfigure(
            0,
            weight=1
        )

        self.canvas_editor = ThumbnailCanvas(
            container_canvas,
            largura_preview=800,
            altura_preview=450,
            ao_selecionar=self.ao_selecionar_elemento,
            ao_alterar=self.ao_alterar_documento
        )

        self.canvas_editor.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=15,
            pady=15
        )

        self.status = ctk.CTkLabel(
            painel_canvas,
            text=(
                "Clique em um elemento para selecioná-lo. "
                "Arraste para alterar sua posição."
            ),
            text_color="gray70",
            wraplength=800
        )

        self.status.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=15,
            pady=(0, 12)
        )

    # =========================================================
    # PAINEL LATERAL
    # =========================================================

    def _criar_painel_lateral(
        self,
        area
    ):
        painel = ctk.CTkFrame(
            area,
            width=340
        )

        painel.grid(
            row=0,
            column=2,
            sticky="ns",
            padx=(5, 10),
            pady=10
        )

        painel.grid_propagate(
            False
        )

        painel.grid_columnconfigure(
            0,
            weight=1
        )

        painel.grid_rowconfigure(
            1,
            weight=1
        )

        ctk.CTkLabel(
            painel,
            text="Propriedades",
            font=("Arial", 18, "bold")
        ).grid(
            row=0,
            column=0,
            pady=(18, 10)
        )

        propriedades = ctk.CTkScrollableFrame(
            painel
        )

        propriedades.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=10,
            pady=(0, 8)
        )

        propriedades.grid_columnconfigure(
            1,
            weight=1
        )

        self._criar_campos_propriedades(
            propriedades
        )

        ctk.CTkLabel(
            painel,
            text="Camadas",
            font=("Arial", 17, "bold")
        ).grid(
            row=2,
            column=0,
            pady=(8, 5)
        )

        self.lista_camadas = ctk.CTkScrollableFrame(
            painel,
            height=180
        )

        self.lista_camadas.grid(
            row=3,
            column=0,
            sticky="ew",
            padx=10,
            pady=(0, 15)
        )

        self.lista_camadas.grid_columnconfigure(
            0,
            weight=1
        )

    # =========================================================
    # CAMPOS DE PROPRIEDADES
    # =========================================================

    def _criar_campos_propriedades(
        self,
        painel
    ):
        self.rotulo_tipo = ctk.CTkLabel(
            painel,
            text="Nenhum elemento selecionado",
            font=("Arial", 15, "bold")
        )

        self.rotulo_tipo.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="w",
            padx=5,
            pady=(5, 15)
        )

        self.campo_nome = self._criar_campo(
            painel,
            1,
            "Nome"
        )

        self.campo_x = self._criar_campo(
            painel,
            2,
            "Posição X"
        )

        self.campo_y = self._criar_campo(
            painel,
            3,
            "Posição Y"
        )

        self.campo_largura = self._criar_campo(
            painel,
            4,
            "Largura"
        )

        self.campo_altura = self._criar_campo(
            painel,
            5,
            "Altura"
        )

        self.campo_rotacao = self._criar_campo(
            painel,
            6,
            "Rotação"
        )

        self.campo_opacidade = self._criar_campo(
            painel,
            7,
            "Opacidade"
        )

        self.campo_texto = self._criar_campo(
            painel,
            8,
            "Texto"
        )

        self.campo_tamanho_fonte = self._criar_campo(
            painel,
            9,
            "Tamanho da fonte"
        )

        (
            self.campo_cor,
            self.amostra_cor,
            self.botao_cor
        ) = self._criar_seletor_cor(
            painel=painel,
            linha=10,
            titulo="Cor",
            comando=self.escolher_cor_principal
        )

        (
            self.campo_contorno,
            self.amostra_contorno,
            self.botao_contorno
        ) = self._criar_seletor_cor(
            painel=painel,
            linha=11,
            titulo="Contorno",
            comando=self.escolher_cor_contorno
        )

        self.campo_largura_contorno = self._criar_campo(
            painel,
            12,
            "Largura contorno"
        )

        self.botao_aplicar = ctk.CTkButton(
            painel,
            text="Aplicar propriedades",
            height=40,
            command=self.aplicar_propriedades
        )

        self.botao_aplicar.grid(
            row=13,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=5,
            pady=(18, 10)
        )

        self._definir_estado_campos(
            "disabled"
        )

    def _criar_campo(
        self,
        painel,
        linha,
        titulo
    ):
        ctk.CTkLabel(
            painel,
            text=titulo
        ).grid(
            row=linha,
            column=0,
            sticky="w",
            padx=5,
            pady=7
        )

        campo = ctk.CTkEntry(
            painel
        )

        campo.grid(
            row=linha,
            column=1,
            sticky="ew",
            padx=5,
            pady=7
        )

        return campo

    def _criar_seletor_cor(
        self,
        painel,
        linha,
        titulo,
        comando
    ):
        ctk.CTkLabel(
            painel,
            text=titulo
        ).grid(
            row=linha,
            column=0,
            sticky="w",
            padx=5,
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
            padx=5,
            pady=7
        )

        area.grid_columnconfigure(
            0,
            weight=1
        )

        campo = ctk.CTkEntry(
            area
        )

        campo.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(0, 5)
        )

        amostra = ctk.CTkLabel(
            area,
            text="",
            width=30,
            height=28,
            corner_radius=6,
            fg_color=self.COR_PADRAO
        )

        amostra.grid(
            row=0,
            column=1,
            padx=4
        )

        botao = ctk.CTkButton(
            area,
            text="Escolher",
            width=70,
            height=28,
            command=comando
        )

        botao.grid(
            row=0,
            column=2,
            padx=(4, 0)
        )

        return campo, amostra, botao

    # =========================================================
    # PALETA DE CORES
    # =========================================================

    def escolher_cor_principal(self):
        elemento = self.elemento_selecionado

        if elemento is None:
            self.status.configure(
                text="Selecione um texto ou uma forma primeiro."
            )
            return

        if elemento.bloqueado:
            self.status.configure(
                text="Este elemento está bloqueado."
            )
            return

        cor_atual = self._obter_cor_valida(
            self.campo_cor.get(),
            self.COR_PADRAO
        )

        _, cor_hexadecimal = colorchooser.askcolor(
            color=cor_atual,
            title="Escolha a cor do elemento",
            parent=self.winfo_toplevel()
        )

        if not cor_hexadecimal:
            return

        cor_hexadecimal = cor_hexadecimal.upper()

        self._definir_campo(
            self.campo_cor,
            cor_hexadecimal
        )

        self._atualizar_amostra_cor(
            self.amostra_cor,
            cor_hexadecimal
        )

        if isinstance(
            elemento,
            TextElement
        ):
            elemento.cor = cor_hexadecimal

        elif isinstance(
            elemento,
            ShapeElement
        ):
            elemento.cor = cor_hexadecimal

        else:
            self.status.configure(
                text=(
                    "A cor principal está disponível "
                    "para textos e formas."
                )
            )
            return

        self._atualizar_canvas_apos_cor(
            "Cor alterada."
        )

    def escolher_cor_contorno(self):
        elemento = self.elemento_selecionado

        if elemento is None:
            self.status.configure(
                text="Selecione um texto ou uma forma primeiro."
            )
            return

        if elemento.bloqueado:
            self.status.configure(
                text="Este elemento está bloqueado."
            )
            return

        cor_atual = self._obter_cor_valida(
            self.campo_contorno.get(),
            self.COR_CONTORNO_PADRAO
        )

        _, cor_hexadecimal = colorchooser.askcolor(
            color=cor_atual,
            title="Escolha a cor do contorno",
            parent=self.winfo_toplevel()
        )

        if not cor_hexadecimal:
            return

        cor_hexadecimal = cor_hexadecimal.upper()

        self._definir_campo(
            self.campo_contorno,
            cor_hexadecimal
        )

        self._atualizar_amostra_cor(
            self.amostra_contorno,
            cor_hexadecimal
        )

        if isinstance(
            elemento,
            TextElement
        ):
            elemento.cor_contorno = cor_hexadecimal

        elif isinstance(
            elemento,
            ShapeElement
        ):
            elemento.cor_contorno = cor_hexadecimal

        else:
            self.status.configure(
                text=(
                    "A cor de contorno está disponível "
                    "para textos e formas."
                )
            )
            return

        self._atualizar_canvas_apos_cor(
            "Cor do contorno alterada."
        )

    def _atualizar_canvas_apos_cor(
        self,
        mensagem
    ):
        self.canvas_editor.renderizar()

        self.documento_alterado = True
        self.historico_editor.registrar()

        self.atualizar_lista_camadas()
        self._atualizar_rotulo_arquivo()

        self.status.configure(
            text=mensagem
        )

    def _atualizar_amostras_atuais(self):
        cor = self._obter_cor_valida(
            self.campo_cor.get(),
            self.COR_PADRAO
        )

        contorno = self._obter_cor_valida(
            self.campo_contorno.get(),
            self.COR_CONTORNO_PADRAO
        )

        self._atualizar_amostra_cor(
            self.amostra_cor,
            cor
        )

        self._atualizar_amostra_cor(
            self.amostra_contorno,
            contorno
        )

    def _atualizar_amostra_cor(
        self,
        amostra,
        cor
    ):
        cor = self._obter_cor_valida(
            cor,
            "#777777"
        )

        try:
            amostra.configure(
                fg_color=cor
            )
        except ValueError:
            amostra.configure(
                fg_color="#777777"
            )

    def _obter_cor_valida(
        self,
        cor,
        padrao
    ):
        cor = str(
            cor
        ).strip()

        if (
            len(cor) == 7
            and cor.startswith("#")
        ):
            try:
                int(
                    cor[1:],
                    16
                )

                return cor.upper()

            except ValueError:
                pass

        return padrao

    # =========================================================
    # DOCUMENTO
    # =========================================================

    def criar_documento_inicial(self):
        documento = ThumbnailDocument(
            largura=1280,
            altura=720,
            cor_fundo="#6D28B2"
        )

        documento.adicionar_elemento(
            ShapeElement(
                nome="Fundo",
                x=0,
                y=0,
                largura=1280,
                altura=720,
                formato="retangulo",
                cor="#6D28B2",
                camada=0,
                bloqueado=True
            )
        )

        documento.adicionar_elemento(
            TextElement(
                nome="Título",
                x=180,
                y=30,
                largura=920,
                altura=110,
                texto="O QUE VOCÊ PREFERE?",
                tamanho_fonte=72,
                cor="#FFFFFF",
                cor_contorno="#43136E",
                largura_contorno=4,
                sombra=True,
                camada=1
            )
        )

        self.canvas_editor.definir_documento(
            documento
        )

        self.elemento_selecionado = None
        self.elemento_copiado = None
        self.caminho_documento_atual = None
        self.documento_alterado = False

        self.atualizar_lista_camadas()
        self._atualizar_rotulo_arquivo()
        self.historico_editor.iniciar(
            documento
        )

    def novo_documento(self):
        if not self._confirmar_descarte():
            return

        self.criar_documento_inicial()

        self.status.configure(
            text="Novo documento criado."
        )

    def abrir_documento(self):
        if not self._confirmar_descarte():
            return

        caminho = filedialog.askopenfilename(
            parent=self.winfo_toplevel(),
            title="Abrir projeto de thumbnail",
            filetypes=[
                (
                    "Projeto de thumbnail",
                    "*.json"
                ),
                (
                    "Todos os arquivos",
                    "*.*"
                )
            ]
        )

        if not caminho:
            return

        try:
            documento = self.document_manager.carregar(
                caminho
            )

            self.canvas_editor.definir_documento(
                documento
            )

            self.caminho_documento_atual = Path(
                caminho
            )

            self.documento_alterado = False
            self.elemento_selecionado = None

            self.atualizar_lista_camadas()
            self._atualizar_rotulo_arquivo()
            self.historico_editor.iniciar(
                documento
            )

            self.status.configure(
                text=f"Documento carregado: {caminho}"
            )

        except (
            OSError,
            ValueError
        ) as erro:
            messagebox.showerror(
                title="Erro ao abrir documento",
                message=str(erro),
                parent=self.winfo_toplevel()
            )

    def salvar_documento(self):
        if self.caminho_documento_atual is None:
            self.salvar_documento_como()
            return

        self._salvar_no_caminho(
            self.caminho_documento_atual
        )

    def salvar_documento_como(self):
        caminho = filedialog.asksaveasfilename(
            parent=self.winfo_toplevel(),
            title="Salvar projeto de thumbnail",
            defaultextension=".json",
            filetypes=[
                (
                    "Projeto de thumbnail",
                    "*.json"
                )
            ]
        )

        if not caminho:
            return

        self._salvar_no_caminho(
            caminho
        )

    def _salvar_no_caminho(
        self,
        caminho
    ):
        try:
            caminho_salvo = self.document_manager.salvar(
                documento=(
                    self.canvas_editor
                    .obter_documento()
                ),
                caminho_arquivo=caminho
            )

            self.caminho_documento_atual = caminho_salvo
            self.documento_alterado = False

            self._atualizar_rotulo_arquivo()

            self.status.configure(
                text=f"Documento salvo: {caminho_salvo}"
            )

        except OSError as erro:
            messagebox.showerror(
                title="Erro ao salvar documento",
                message=str(erro),
                parent=self.winfo_toplevel()
            )

    # =========================================================
    # EXPORTAÇÃO
    # =========================================================

    def exportar_png(self):
        self._exportar_imagem(
            extensao=".png",
            descricao="Imagem PNG"
        )

    def exportar_jpg(self):
        self._exportar_imagem(
            extensao=".jpg",
            descricao="Imagem JPG"
        )

    def _exportar_imagem(
        self,
        extensao,
        descricao
    ):
        caminho = filedialog.asksaveasfilename(
            parent=self.winfo_toplevel(),
            title="Exportar thumbnail",
            defaultextension=extensao,
            filetypes=[
                (
                    descricao,
                    f"*{extensao}"
                )
            ]
        )

        if not caminho:
            return

        try:
            caminho_exportado = self.document_renderer.salvar(
                documento=(
                    self.canvas_editor
                    .obter_documento()
                ),
                caminho_saida=caminho
            )

            self.status.configure(
                text=f"Thumbnail exportada: {caminho_exportado}"
            )

            messagebox.showinfo(
                title="Thumbnail exportada",
                message=(
                    "A thumbnail foi exportada com sucesso.\n\n"
                    f"{caminho_exportado}"
                ),
                parent=self.winfo_toplevel()
            )

        except OSError as erro:
            messagebox.showerror(
                title="Erro ao exportar",
                message=str(erro),
                parent=self.winfo_toplevel()
            )

    # =========================================================
    # ADICIONAR ELEMENTOS
    # =========================================================

    def adicionar_texto(self):
        documento = self.canvas_editor.obter_documento()

        self.canvas_editor.adicionar_elemento(
            TextElement(
                nome="Novo texto",
                x=340,
                y=280,
                largura=600,
                altura=110,
                texto="NOVO TEXTO",
                tamanho_fonte=64,
                cor="#FFFFFF",
                cor_contorno="#000000",
                largura_contorno=2,
                sombra=True,
                camada=self._proxima_camada(
                    documento
                )
            )
        )

        self._marcar_alterado(
            "Novo texto adicionado."
        )

    def adicionar_imagem(self):
        caminho = filedialog.askopenfilename(
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

        if not caminho:
            return

        documento = self.canvas_editor.obter_documento()

        self.canvas_editor.adicionar_elemento(
            ImageElement(
                nome=Path(caminho).stem,
                x=390,
                y=180,
                largura=500,
                altura=350,
                caminho=str(Path(caminho)),
                preencher_area=False,
                sombra=True,
                camada=self._proxima_camada(
                    documento
                )
            )
        )

        self._marcar_alterado(
            f"Imagem adicionada: {caminho}"
        )

    def adicionar_retangulo(self):
        documento = self.canvas_editor.obter_documento()

        self.canvas_editor.adicionar_elemento(
            ShapeElement(
                nome="Retângulo",
                x=390,
                y=250,
                largura=500,
                altura=240,
                formato="retangulo",
                cor="#FF8A1F",
                cor_contorno="#FFFFFF",
                largura_contorno=4,
                camada=self._proxima_camada(
                    documento
                )
            )
        )

        self._marcar_alterado(
            "Retângulo adicionado."
        )

    def adicionar_circulo(self):
        documento = self.canvas_editor.obter_documento()

        self.canvas_editor.adicionar_elemento(
            ShapeElement(
                nome="Círculo",
                x=540,
                y=260,
                largura=200,
                altura=200,
                formato="circulo",
                cor="#FF8A1F",
                cor_contorno="#FFFFFF",
                largura_contorno=6,
                camada=self._proxima_camada(
                    documento
                )
            )
        )

        self._marcar_alterado(
            "Círculo adicionado."
        )

    # =========================================================
    # SELEÇÃO E ALTERAÇÕES
    # =========================================================

    def ao_selecionar_elemento(
        self,
        elemento
    ):
        self.elemento_selecionado = elemento

        if elemento is None:
            self.rotulo_tipo.configure(
                text="Nenhum elemento selecionado"
            )

            self._limpar_campos()
            self._definir_estado_campos(
                "disabled"
            )

            return

        self.rotulo_tipo.configure(
            text=f"{elemento.nome} ({elemento.tipo})"
        )

        self._definir_estado_campos(
            "normal"
        )

        self._preencher_propriedades(
            elemento
        )

    def ao_alterar_documento(
        self,
        documento
    ):
        self.documento_alterado = True
        self.historico_editor.registrar(
            documento
        )

        self.atualizar_lista_camadas()
        self._atualizar_rotulo_arquivo()

        elemento = (
            self.canvas_editor
            .obter_elemento_selecionado()
        )

        if elemento is not None:
            self._preencher_propriedades(
                elemento
            )

    def aplicar_propriedades(self):
        elemento = self.elemento_selecionado

        if elemento is None:
            self.status.configure(
                text="Selecione um elemento primeiro."
            )
            return

        if elemento.bloqueado:
            self.status.configure(
                text="Este elemento está bloqueado."
            )
            return

        try:
            elemento.nome = (
                self.campo_nome.get().strip()
                or elemento.nome
            )

            elemento.mover(
                float(self.campo_x.get()),
                float(self.campo_y.get())
            )

            elemento.redimensionar(
                float(self.campo_largura.get()),
                float(self.campo_altura.get())
            )

            elemento.definir_rotacao(
                float(self.campo_rotacao.get())
            )

            elemento.definir_opacidade(
                int(self.campo_opacidade.get())
            )

            if isinstance(
                elemento,
                TextElement
            ):
                elemento.texto = self.campo_texto.get()

                elemento.tamanho_fonte = max(
                    int(self.campo_tamanho_fonte.get()),
                    1
                )

                elemento.cor = self._obter_cor_valida(
                    self.campo_cor.get(),
                    elemento.cor
                )

                elemento.cor_contorno = self._obter_cor_valida(
                    self.campo_contorno.get(),
                    elemento.cor_contorno
                )

                elemento.largura_contorno = max(
                    int(
                        self.campo_largura_contorno.get()
                    ),
                    0
                )

            elif isinstance(
                elemento,
                ShapeElement
            ):
                elemento.cor = self._obter_cor_valida(
                    self.campo_cor.get(),
                    elemento.cor
                )

                elemento.cor_contorno = self._obter_cor_valida(
                    self.campo_contorno.get(),
                    elemento.cor_contorno
                )

                elemento.largura_contorno = max(
                    int(
                        self.campo_largura_contorno.get()
                    ),
                    0
                )

            self._limitar_elemento(
                elemento
            )

            self.canvas_editor.renderizar()
            self.atualizar_lista_camadas()

            self.documento_alterado = True
            self.historico_editor.registrar()
            self._atualizar_rotulo_arquivo()
            self._atualizar_amostras_atuais()

            self.status.configure(
                text="Propriedades aplicadas."
            )

        except ValueError as erro:
            messagebox.showerror(
                title="Valor inválido",
                message=str(erro),
                parent=self.winfo_toplevel()
            )

    # =========================================================
    # COPIAR, COLAR E DUPLICAR
    # =========================================================

    def copiar_elemento(self):
        elemento = self.elemento_selecionado

        if elemento is None:
            self.status.configure(
                text="Selecione um elemento para copiar."
            )
            return

        if elemento.bloqueado:
            self.status.configure(
                text="Este elemento está bloqueado e não pode ser copiado."
            )
            return

        self.elemento_copiado = deepcopy(elemento)

        self.status.configure(
            text=f"Elemento '{elemento.nome}' copiado."
        )

    def colar_elemento(self):
        if self.elemento_copiado is None:
            self.status.configure(
                text="Nenhum elemento foi copiado."
            )
            return

        novo_elemento = deepcopy(self.elemento_copiado)
        novo_elemento.id = str(uuid4())
        novo_elemento.nome = self._gerar_nome_copia(
            novo_elemento.nome
        )
        novo_elemento.bloqueado = False

        documento = self.canvas_editor.obter_documento()
        novo_elemento.camada = self._proxima_camada(documento)

        self._deslocar_copia_para_area_visivel(
            novo_elemento,
            deslocamento=30
        )

        self.canvas_editor.adicionar_elemento(
            novo_elemento
        )

        self.elemento_selecionado = novo_elemento
        self.elemento_copiado = deepcopy(novo_elemento)

        self.status.configure(
            text=f"Elemento '{novo_elemento.nome}' colado."
        )

    def duplicar_elemento(self):
        elemento = self.elemento_selecionado

        if elemento is None:
            self.status.configure(
                text="Selecione um elemento para duplicar."
            )
            return

        if elemento.bloqueado:
            self.status.configure(
                text="Este elemento está bloqueado e não pode ser duplicado."
            )
            return

        self.elemento_copiado = deepcopy(elemento)
        self.colar_elemento()

    def _gerar_nome_copia(self, nome_original):
        nome = str(nome_original).strip() or "Elemento"

        if nome.endswith(" - cópia"):
            return nome

        return f"{nome} - cópia"

    def _deslocar_copia_para_area_visivel(
        self,
        elemento,
        deslocamento=30
    ):
        documento = self.canvas_editor.obter_documento()

        novo_x = elemento.x + deslocamento
        novo_y = elemento.y + deslocamento

        if novo_x + elemento.largura > documento.largura:
            novo_x = max(
                elemento.x - deslocamento,
                0
            )

        if novo_y + elemento.altura > documento.altura:
            novo_y = max(
                elemento.y - deslocamento,
                0
            )

        elemento.x = max(
            min(
                novo_x,
                documento.largura - elemento.largura
            ),
            0
        )

        elemento.y = max(
            min(
                novo_y,
                documento.altura - elemento.altura
            ),
            0
        )

    def _vincular_atalhos_edicao(self):
        janela = self.winfo_toplevel()

        janela.bind(
            "<Control-c>",
            self._atalho_copiar,
            add="+"
        )

        janela.bind(
            "<Control-C>",
            self._atalho_copiar,
            add="+"
        )

        janela.bind(
            "<Control-v>",
            self._atalho_colar,
            add="+"
        )

        janela.bind(
            "<Control-V>",
            self._atalho_colar,
            add="+"
        )

        janela.bind(
            "<Control-d>",
            self._atalho_duplicar,
            add="+"
        )

        janela.bind(
            "<Control-D>",
            self._atalho_duplicar,
            add="+"
        )

        janela.bind(
            "<Delete>",
            self._atalho_excluir,
            add="+"
        )

    def _atalho_copiar(self, evento=None):
        if self._foco_em_campo_de_texto():
            return None

        self.copiar_elemento()
        return "break"

    def _atalho_colar(self, evento=None):
        if self._foco_em_campo_de_texto():
            return None

        self.colar_elemento()
        return "break"

    def _atalho_duplicar(self, evento=None):
        if self._foco_em_campo_de_texto():
            return None

        self.duplicar_elemento()
        return "break"

    def _atalho_excluir(self, evento=None):
        if self._foco_em_campo_de_texto():
            return None

        self.excluir_elemento()
        return "break"

    def _foco_em_campo_de_texto(self):
        widget = self.focus_get()

        if widget is None:
            return False

        try:
            classe = widget.winfo_class()
        except Exception:
            return False

        return classe in {
            "Entry",
            "Text",
            "TEntry",
            "TText",
            "Spinbox"
        }

    # =========================================================
    # EXCLUSÃO E CAMADAS
    # =========================================================

    def excluir_elemento(self):
        elemento = self.elemento_selecionado

        if elemento is None:
            self.status.configure(
                text="Selecione um elemento primeiro."
            )
            return

        if elemento.bloqueado:
            self.status.configure(
                text="Este elemento está bloqueado."
            )
            return

        confirmar = messagebox.askyesno(
            title="Excluir elemento",
            message=f"Deseja excluir '{elemento.nome}'?",
            parent=self.winfo_toplevel()
        )

        if not confirmar:
            return

        if self.canvas_editor.remover_elemento_selecionado():
            self.elemento_selecionado = None

            self._marcar_alterado(
                "Elemento excluído."
            )

    def trazer_para_frente(self):
        if self.elemento_selecionado is None:
            self.status.configure(
                text="Selecione um elemento primeiro."
            )
            return

        self.canvas_editor.trazer_selecionado_para_frente()

        self._marcar_alterado(
            "Elemento trazido para frente."
        )

    def enviar_para_tras(self):
        if self.elemento_selecionado is None:
            self.status.configure(
                text="Selecione um elemento primeiro."
            )
            return

        self.canvas_editor.enviar_selecionado_para_tras()

        self._marcar_alterado(
            "Elemento enviado para trás."
        )

    def atualizar_lista_camadas(self):
        for widget in self.lista_camadas.winfo_children():
            widget.destroy()

        documento = self.canvas_editor.obter_documento()

        elementos = sorted(
            documento.elementos,
            key=lambda item: item.camada,
            reverse=True
        )

        for indice, elemento in enumerate(
            elementos
        ):
            texto = (
                f"{elemento.nome}\n"
                f"{elemento.tipo} • camada {elemento.camada}"
            )

            if elemento.bloqueado:
                texto += " • bloqueado"

            botao = ctk.CTkButton(
                self.lista_camadas,
                text=texto,
                anchor="w",
                height=48,
                fg_color=(
                    "#1F6AA5"
                    if (
                        self.elemento_selecionado
                        and elemento.id
                        == self.elemento_selecionado.id
                    )
                    else "gray30"
                ),
                hover_color="gray25",
                command=lambda elemento_id=elemento.id: (
                    self.canvas_editor.selecionar_elemento(
                        elemento_id
                    )
                )
            )

            botao.grid(
                row=indice,
                column=0,
                sticky="ew",
                padx=4,
                pady=3
            )

    # =========================================================
    # PREENCHIMENTO DOS CAMPOS
    # =========================================================

    def _preencher_propriedades(
        self,
        elemento
    ):
        valores = [
            (
                self.campo_nome,
                elemento.nome
            ),
            (
                self.campo_x,
                round(elemento.x, 1)
            ),
            (
                self.campo_y,
                round(elemento.y, 1)
            ),
            (
                self.campo_largura,
                round(elemento.largura, 1)
            ),
            (
                self.campo_altura,
                round(elemento.altura, 1)
            ),
            (
                self.campo_rotacao,
                round(elemento.rotacao, 1)
            ),
            (
                self.campo_opacidade,
                elemento.opacidade
            )
        ]

        for campo, valor in valores:
            self._definir_campo(
                campo,
                valor
            )

        if isinstance(
            elemento,
            TextElement
        ):
            self._definir_campo(
                self.campo_texto,
                elemento.texto
            )

            self._definir_campo(
                self.campo_tamanho_fonte,
                elemento.tamanho_fonte
            )

            self._definir_campo(
                self.campo_cor,
                elemento.cor
            )

            self._definir_campo(
                self.campo_contorno,
                elemento.cor_contorno
            )

            self._definir_campo(
                self.campo_largura_contorno,
                elemento.largura_contorno
            )

            self._definir_estado_visual(
                "normal"
            )

            self._definir_estado_botoes_cor(
                "normal"
            )

        elif isinstance(
            elemento,
            ShapeElement
        ):
            self._definir_campo(
                self.campo_texto,
                ""
            )

            self._definir_campo(
                self.campo_tamanho_fonte,
                ""
            )

            self._definir_campo(
                self.campo_cor,
                elemento.cor
            )

            self._definir_campo(
                self.campo_contorno,
                elemento.cor_contorno
            )

            self._definir_campo(
                self.campo_largura_contorno,
                elemento.largura_contorno
            )

            self.campo_texto.configure(
                state="disabled"
            )

            self.campo_tamanho_fonte.configure(
                state="disabled"
            )

            self._definir_estado_botoes_cor(
                "normal"
            )

        else:
            self._definir_campo(
                self.campo_texto,
                ""
            )

            self._definir_campo(
                self.campo_tamanho_fonte,
                ""
            )

            self._definir_campo(
                self.campo_cor,
                ""
            )

            self._definir_campo(
                self.campo_contorno,
                ""
            )

            self._definir_campo(
                self.campo_largura_contorno,
                ""
            )

            self._definir_estado_visual(
                "disabled"
            )

            self._definir_estado_botoes_cor(
                "disabled"
            )

        self._atualizar_amostras_atuais()

        if elemento.bloqueado:
            self._definir_estado_campos(
                "disabled"
            )

    # =========================================================
    # ESTADOS DOS CAMPOS
    # =========================================================

    def _definir_estado_campos(
        self,
        estado
    ):
        for campo in self._todos_campos():
            campo.configure(
                state=estado
            )

        self.botao_aplicar.configure(
            state=estado
        )

        self._definir_estado_botoes_cor(
            estado
        )

    def _definir_estado_visual(
        self,
        estado
    ):
        for campo in [
            self.campo_texto,
            self.campo_tamanho_fonte,
            self.campo_cor,
            self.campo_contorno,
            self.campo_largura_contorno
        ]:
            campo.configure(
                state=estado
            )

    def _definir_estado_botoes_cor(
        self,
        estado
    ):
        self.botao_cor.configure(
            state=estado
        )

        self.botao_contorno.configure(
            state=estado
        )

    def _todos_campos(self):
        return [
            self.campo_nome,
            self.campo_x,
            self.campo_y,
            self.campo_largura,
            self.campo_altura,
            self.campo_rotacao,
            self.campo_opacidade,
            self.campo_texto,
            self.campo_tamanho_fonte,
            self.campo_cor,
            self.campo_contorno,
            self.campo_largura_contorno
        ]

    def _limpar_campos(self):
        for campo in self._todos_campos():
            campo.configure(
                state="normal"
            )

            campo.delete(
                0,
                "end"
            )

        self._atualizar_amostra_cor(
            self.amostra_cor,
            "#777777"
        )

        self._atualizar_amostra_cor(
            self.amostra_contorno,
            "#777777"
        )

    def _definir_campo(
        self,
        campo,
        valor
    ):
        estado_anterior = campo.cget(
            "state"
        )

        campo.configure(
            state="normal"
        )

        campo.delete(
            0,
            "end"
        )

        campo.insert(
            0,
            str(valor)
        )

        campo.configure(
            state=estado_anterior
        )

    # =========================================================
    # AUXILIARES
    # =========================================================

    def _obter_documento_atual(self):
        return self.canvas_editor.obter_documento()

    def _restaurar_documento_historico(
        self,
        documento,
        mensagem
    ):
        self.canvas_editor.definir_documento(
            documento
        )

        self.elemento_selecionado = None
        self.documento_alterado = True

        self.atualizar_lista_camadas()
        self._atualizar_rotulo_arquivo()

        self.status.configure(
            text=mensagem
        )

    def _limitar_elemento(
        self,
        elemento
    ):
        documento = self.canvas_editor.obter_documento()

        elemento.x = max(
            min(
                elemento.x,
                documento.largura - elemento.largura
            ),
            0
        )

        elemento.y = max(
            min(
                elemento.y,
                documento.altura - elemento.altura
            ),
            0
        )

    def _proxima_camada(
        self,
        documento
    ):
        if not documento.elementos:
            return 0

        return (
            max(
                elemento.camada
                for elemento in documento.elementos
            )
            + 1
        )

    def _marcar_alterado(
        self,
        mensagem
    ):
        self.documento_alterado = True
        self.historico_editor.registrar()

        self.atualizar_lista_camadas()
        self._atualizar_rotulo_arquivo()

        self.status.configure(
            text=mensagem
        )

    def _atualizar_rotulo_arquivo(self):
        if self.caminho_documento_atual:
            texto = self.caminho_documento_atual.name
        else:
            texto = "Novo documento"

        if self.documento_alterado:
            texto += " *"

        self.rotulo_arquivo.configure(
            text=texto
        )

    def _confirmar_descarte(self):
        if not self.documento_alterado:
            return True

        return messagebox.askyesno(
            title="Alterações não salvas",
            message=(
                "Existem alterações que ainda não foram salvas.\n\n"
                "Deseja descartá-las?"
            ),
            parent=self.winfo_toplevel()
        )
