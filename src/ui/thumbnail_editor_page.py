from pathlib import Path
from tkinter import filedialog, messagebox

import customtkinter as ctk

from core.thumbnail_elements import (
    ImageElement,
    ShapeElement,
    TextElement,
    ThumbnailDocument,
    ThumbnailElement
)
from ui.thumbnail_canvas import ThumbnailCanvas


class ThumbnailEditorPage(ctk.CTkFrame):
    """
    Primeira página do editor visual de thumbnails.

    Nesta versão já é possível:
    - adicionar textos;
    - adicionar imagens;
    - adicionar retângulos e círculos;
    - selecionar elementos;
    - arrastar elementos;
    - editar posição e tamanho;
    - alterar texto e cores;
    - organizar camadas;
    - excluir elementos.
    """

    def __init__(self, master):
        super().__init__(master)

        self.elemento_selecionado = None
        self.atualizando_propriedades = False

        self.criar_interface()
        self.criar_documento_inicial()

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
            font=(
                "Arial",
                28,
                "bold"
            )
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            area_titulo,
            text=(
                "Adicione, selecione e mova elementos "
                "livremente sobre a thumbnail."
            ),
            text_color="gray70"
        ).pack(
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

        ctk.CTkButton(
            area_botoes,
            text="Novo documento",
            width=145,
            command=self.novo_documento
        ).pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            area_botoes,
            text="Atualizar canvas",
            width=145,
            fg_color="gray35",
            hover_color="gray25",
            command=self.atualizar_canvas
        ).pack(
            side="left",
            padx=5
        )

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
            0,
            weight=0
        )

        area.grid_columnconfigure(
            1,
            weight=1
        )

        area.grid_columnconfigure(
            2,
            weight=0
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
            font=(
                "Arial",
                18,
                "bold"
            )
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

        separador = ctk.CTkFrame(
            barra,
            height=2,
            fg_color="gray35"
        )

        separador.pack(
            fill="x",
            padx=15,
            pady=18
        )

        ctk.CTkLabel(
            barra,
            text="Organização",
            font=(
                "Arial",
                16,
                "bold"
            )
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
            font=(
                "Arial",
                16,
                "bold"
            )
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

    def _criar_painel_lateral(
        self,
        area
    ):
        painel = ctk.CTkFrame(
            area,
            width=310
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
            font=(
                "Arial",
                18,
                "bold"
            )
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
            font=(
                "Arial",
                17,
                "bold"
            )
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

    def _criar_campos_propriedades(
        self,
        painel
    ):
        linha = 0

        self.rotulo_tipo = ctk.CTkLabel(
            painel,
            text="Nenhum elemento selecionado",
            font=(
                "Arial",
                15,
                "bold"
            )
        )

        self.rotulo_tipo.grid(
            row=linha,
            column=0,
            columnspan=2,
            sticky="w",
            padx=5,
            pady=(5, 15)
        )

        linha += 1

        self.campo_nome = self._criar_campo(
            painel,
            linha,
            "Nome"
        )

        linha += 1

        self.campo_x = self._criar_campo(
            painel,
            linha,
            "Posição X"
        )

        linha += 1

        self.campo_y = self._criar_campo(
            painel,
            linha,
            "Posição Y"
        )

        linha += 1

        self.campo_largura = self._criar_campo(
            painel,
            linha,
            "Largura"
        )

        linha += 1

        self.campo_altura = self._criar_campo(
            painel,
            linha,
            "Altura"
        )

        linha += 1

        self.rotulo_texto = ctk.CTkLabel(
            painel,
            text="Texto"
        )

        self.rotulo_texto.grid(
            row=linha,
            column=0,
            sticky="w",
            padx=5,
            pady=7
        )

        self.campo_texto = ctk.CTkEntry(
            painel
        )

        self.campo_texto.grid(
            row=linha,
            column=1,
            sticky="ew",
            padx=5,
            pady=7
        )

        linha += 1

        self.campo_tamanho_fonte = self._criar_campo(
            painel,
            linha,
            "Tamanho da fonte"
        )

        linha += 1

        self.campo_cor = self._criar_campo(
            painel,
            linha,
            "Cor"
        )

        linha += 1

        self.campo_contorno = self._criar_campo(
            painel,
            linha,
            "Cor do contorno"
        )

        linha += 1

        self.campo_largura_contorno = self._criar_campo(
            painel,
            linha,
            "Largura contorno"
        )

        linha += 1

        self.botao_aplicar = ctk.CTkButton(
            painel,
            text="Aplicar propriedades",
            height=40,
            command=self.aplicar_propriedades
        )

        self.botao_aplicar.grid(
            row=linha,
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

    def criar_documento_inicial(self):
        documento = ThumbnailDocument(
            largura=1280,
            altura=720,
            cor_fundo="#6D28B2"
        )

        fundo = ShapeElement(
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

        titulo = TextElement(
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

        documento.adicionar_elemento(
            fundo
        )

        documento.adicionar_elemento(
            titulo
        )

        self.canvas_editor.definir_documento(
            documento
        )

        self.atualizar_lista_camadas()

    def novo_documento(self):
        confirmar = messagebox.askyesno(
            title="Novo documento",
            message=(
                "Deseja criar um novo documento?\n\n"
                "As alterações que ainda não foram salvas "
                "serão descartadas."
            ),
            parent=self.winfo_toplevel()
        )

        if not confirmar:
            return

        self.elemento_selecionado = None
        self.criar_documento_inicial()

        self.status.configure(
            text="Novo documento criado."
        )

    def adicionar_texto(self):
        documento = (
            self.canvas_editor
            .obter_documento()
        )

        elemento = TextElement(
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

        self.canvas_editor.adicionar_elemento(
            elemento
        )

        self.status.configure(
            text="Novo texto adicionado."
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

        documento = (
            self.canvas_editor
            .obter_documento()
        )

        elemento = ImageElement(
            nome=Path(
                caminho
            ).stem,
            x=390,
            y=180,
            largura=500,
            altura=350,
            caminho=str(
                Path(
                    caminho
                )
            ),
            preencher_area=False,
            sombra=True,
            camada=self._proxima_camada(
                documento
            )
        )

        self.canvas_editor.adicionar_elemento(
            elemento
        )

        self.status.configure(
            text=f"Imagem adicionada: {caminho}"
        )

    def adicionar_retangulo(self):
        documento = (
            self.canvas_editor
            .obter_documento()
        )

        elemento = ShapeElement(
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

        self.canvas_editor.adicionar_elemento(
            elemento
        )

        self.status.configure(
            text="Retângulo adicionado."
        )

    def adicionar_circulo(self):
        documento = (
            self.canvas_editor
            .obter_documento()
        )

        elemento = ShapeElement(
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

        self.canvas_editor.adicionar_elemento(
            elemento
        )

        self.status.configure(
            text="Círculo adicionado."
        )

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
            text=(
                f"{elemento.nome} "
                f"({elemento.tipo})"
            )
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
        self.atualizar_lista_camadas()

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
                text=(
                    "Este elemento está bloqueado "
                    "e não pode ser alterado."
                )
            )

            return

        try:
            nome = (
                self.campo_nome
                .get()
                .strip()
            )

            x = float(
                self.campo_x.get()
            )

            y = float(
                self.campo_y.get()
            )

            largura = float(
                self.campo_largura.get()
            )

            altura = float(
                self.campo_altura.get()
            )

            if largura < 1 or altura < 1:
                raise ValueError(
                    "Largura e altura devem ser maiores que zero."
                )

            elemento.nome = (
                nome
                or elemento.nome
            )

            elemento.mover(
                x,
                y
            )

            elemento.redimensionar(
                largura,
                altura
            )

            if isinstance(
                elemento,
                TextElement
            ):
                elemento.texto = (
                    self.campo_texto
                    .get()
                )

                elemento.tamanho_fonte = max(
                    int(
                        self.campo_tamanho_fonte
                        .get()
                    ),
                    1
                )

                elemento.cor = (
                    self.campo_cor
                    .get()
                    .strip()
                    or elemento.cor
                )

                elemento.cor_contorno = (
                    self.campo_contorno
                    .get()
                    .strip()
                    or elemento.cor_contorno
                )

                elemento.largura_contorno = max(
                    int(
                        self.campo_largura_contorno
                        .get()
                    ),
                    0
                )

            elif isinstance(
                elemento,
                ShapeElement
            ):
                elemento.cor = (
                    self.campo_cor
                    .get()
                    .strip()
                    or elemento.cor
                )

                elemento.cor_contorno = (
                    self.campo_contorno
                    .get()
                    .strip()
                    or elemento.cor_contorno
                )

                elemento.largura_contorno = max(
                    int(
                        self.campo_largura_contorno
                        .get()
                    ),
                    0
                )

            self._limitar_elemento(
                elemento
            )

            self.canvas_editor.renderizar()
            self.atualizar_lista_camadas()

            self.rotulo_tipo.configure(
                text=(
                    f"{elemento.nome} "
                    f"({elemento.tipo})"
                )
            )

            self.status.configure(
                text="Propriedades aplicadas."
            )

        except ValueError as erro:
            messagebox.showerror(
                title="Valor inválido",
                message=str(
                    erro
                ),
                parent=self.winfo_toplevel()
            )

    def excluir_elemento(self):
        elemento = self.elemento_selecionado

        if elemento is None:
            self.status.configure(
                text="Selecione um elemento primeiro."
            )

            return

        if elemento.bloqueado:
            self.status.configure(
                text=(
                    "Este elemento está bloqueado "
                    "e não pode ser excluído."
                )
            )

            return

        confirmar = messagebox.askyesno(
            title="Excluir elemento",
            message=(
                f"Deseja excluir o elemento "
                f"'{elemento.nome}'?"
            ),
            parent=self.winfo_toplevel()
        )

        if not confirmar:
            return

        removido = (
            self.canvas_editor
            .remover_elemento_selecionado()
        )

        if removido:
            self.elemento_selecionado = None
            self.atualizar_lista_camadas()

            self.status.configure(
                text="Elemento excluído."
            )

    def trazer_para_frente(self):
        if self.elemento_selecionado is None:
            self.status.configure(
                text="Selecione um elemento primeiro."
            )

            return

        self.canvas_editor.trazer_selecionado_para_frente()
        self.atualizar_lista_camadas()

        self.status.configure(
            text="Elemento trazido para frente."
        )

    def enviar_para_tras(self):
        if self.elemento_selecionado is None:
            self.status.configure(
                text="Selecione um elemento primeiro."
            )

            return

        self.canvas_editor.enviar_selecionado_para_tras()
        self.atualizar_lista_camadas()

        self.status.configure(
            text="Elemento enviado para trás."
        )

    def atualizar_canvas(self):
        self.canvas_editor.renderizar()
        self.atualizar_lista_camadas()

        self.status.configure(
            text="Canvas atualizado."
        )

    def atualizar_lista_camadas(self):
        for widget in (
            self.lista_camadas
            .winfo_children()
        ):
            widget.destroy()

        documento = (
            self.canvas_editor
            .obter_documento()
        )

        elementos = sorted(
            documento.elementos,
            key=lambda item: item.camada,
            reverse=True
        )

        if not elementos:
            ctk.CTkLabel(
                self.lista_camadas,
                text="Nenhuma camada."
            ).grid(
                row=0,
                column=0,
                pady=10
            )

            return

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
                    self.canvas_editor
                    .selecionar_elemento(
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

    def _preencher_propriedades(
        self,
        elemento
    ):
        self.atualizando_propriedades = True

        self._definir_campo(
            self.campo_nome,
            elemento.nome
        )

        self._definir_campo(
            self.campo_x,
            round(
                elemento.x,
                1
            )
        )

        self._definir_campo(
            self.campo_y,
            round(
                elemento.y,
                1
            )
        )

        self._definir_campo(
            self.campo_largura,
            round(
                elemento.largura,
                1
            )
        )

        self._definir_campo(
            self.campo_altura,
            round(
                elemento.altura,
                1
            )
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

            self._definir_estado_campos_texto(
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

            self._definir_estado_campos_visuais(
                "disabled"
            )

        if elemento.bloqueado:
            self._definir_estado_campos(
                "disabled"
            )

        self.atualizando_propriedades = False

    def _definir_estado_campos(
        self,
        estado
    ):
        campos = [
            self.campo_nome,
            self.campo_x,
            self.campo_y,
            self.campo_largura,
            self.campo_altura,
            self.campo_texto,
            self.campo_tamanho_fonte,
            self.campo_cor,
            self.campo_contorno,
            self.campo_largura_contorno
        ]

        for campo in campos:
            campo.configure(
                state=estado
            )

        self.botao_aplicar.configure(
            state=estado
        )

    def _definir_estado_campos_texto(
        self,
        estado
    ):
        self.campo_texto.configure(
            state=estado
        )

        self.campo_tamanho_fonte.configure(
            state=estado
        )

        self.campo_cor.configure(
            state=estado
        )

        self.campo_contorno.configure(
            state=estado
        )

        self.campo_largura_contorno.configure(
            state=estado
        )

    def _definir_estado_campos_visuais(
        self,
        estado
    ):
        self.campo_texto.configure(
            state=estado
        )

        self.campo_tamanho_fonte.configure(
            state=estado
        )

        self.campo_cor.configure(
            state=estado
        )

        self.campo_contorno.configure(
            state=estado
        )

        self.campo_largura_contorno.configure(
            state=estado
        )

    def _limpar_campos(self):
        campos = [
            self.campo_nome,
            self.campo_x,
            self.campo_y,
            self.campo_largura,
            self.campo_altura,
            self.campo_texto,
            self.campo_tamanho_fonte,
            self.campo_cor,
            self.campo_contorno,
            self.campo_largura_contorno
        ]

        for campo in campos:
            campo.configure(
                state="normal"
            )

            campo.delete(
                0,
                "end"
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
            str(
                valor
            )
        )

        campo.configure(
            state=estado_anterior
        )

    def _limitar_elemento(
        self,
        elemento
    ):
        documento = (
            self.canvas_editor
            .obter_documento()
        )

        elemento.x = max(
            min(
                elemento.x,
                documento.largura
                - elemento.largura
            ),
            0
        )

        elemento.y = max(
            min(
                elemento.y,
                documento.altura
                - elemento.altura
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
