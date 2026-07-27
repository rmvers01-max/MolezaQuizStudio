from copy import deepcopy
from pathlib import Path
from tkinter import colorchooser, filedialog, messagebox
from uuid import uuid4

import customtkinter as ctk

from core.thumbnail_elements import (
    ImageElement,
    ShapeElement,
    TextElement,
    ThumbnailDocument,
)

from .canvas import ThumbnailCanvas
from .zoom_controller import ZoomController


class LayoutMixin:
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

        barra_canvas = ctk.CTkFrame(
            painel_canvas,
            fg_color="transparent"
        )

        barra_canvas.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=15,
            pady=(10, 8)
        )

        barra_canvas.grid_columnconfigure(
            0,
            weight=1
        )

        ctk.CTkLabel(
            barra_canvas,
            text="Área de edição — 1280 × 720",
            font=("Arial", 16, "bold")
        ).grid(
            row=0,
            column=0,
            sticky="w"
        )

        controles_zoom = ctk.CTkFrame(
            barra_canvas,
            fg_color="transparent"
        )

        controles_zoom.grid(
            row=0,
            column=1,
            sticky="e"
        )

        self.botao_zoom_menos = ctk.CTkButton(
            controles_zoom,
            text="−",
            width=34,
            height=30,
            command=self._diminuir_zoom
        )
        self.botao_zoom_menos.pack(side="left", padx=3)

        self.rotulo_zoom = ctk.CTkLabel(
            controles_zoom,
            text="100%",
            width=58
        )
        self.rotulo_zoom.pack(side="left", padx=3)

        self.botao_zoom_mais = ctk.CTkButton(
            controles_zoom,
            text="+",
            width=34,
            height=30,
            command=self._aumentar_zoom
        )
        self.botao_zoom_mais.pack(side="left", padx=3)

        ctk.CTkButton(
            controles_zoom,
            text="100%",
            width=58,
            height=30,
            fg_color="gray35",
            hover_color="gray25",
            command=self._zoom_tamanho_real
        ).pack(side="left", padx=3)

        ctk.CTkButton(
            controles_zoom,
            text="Ajustar",
            width=70,
            height=30,
            fg_color="gray35",
            hover_color="gray25",
            command=self._ajustar_zoom_tela
        ).pack(side="left", padx=3)

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
            ao_alterar=self.ao_alterar_documento,
            ao_zoom=self._ao_alterar_zoom
        )

        self.zoom_controller = ZoomController(
            canvas_editor=self.canvas_editor,
            ao_alterar=self._ao_alterar_zoom
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

    def _ao_alterar_zoom(self, percentual):
        if hasattr(self, "rotulo_zoom"):
            self.rotulo_zoom.configure(
                text=f"{int(percentual)}%"
            )

    def _aumentar_zoom(self):
        self.zoom_controller.aumentar()

    def _diminuir_zoom(self):
        self.zoom_controller.diminuir()

    def _zoom_tamanho_real(self):
        self.zoom_controller.tamanho_real()

    def _ajustar_zoom_tela(self):
        self.zoom_controller.ajustar_tela()

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

        self.layers_controller.definir_container(
            self.lista_camadas
        )

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
