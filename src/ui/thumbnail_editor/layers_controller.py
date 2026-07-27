from tkinter import simpledialog

import customtkinter as ctk

from core.thumbnail_elements import ImageElement, ShapeElement, TextElement


class LayersController:
    """Painel profissional de camadas do Editor de Thumbnail."""

    COR_NORMAL = "#2B303B"
    COR_ATIVA = "#1F6AA5"
    COR_HOVER = "#3A4050"
    COR_DESTINO = "#5B3BA4"

    def __init__(self, owner):
        self.owner = owner
        self.container = None
        self.linhas = []
        self.elemento_arrastado_id = None
        self.destino_arraste_id = None

    def definir_container(self, container):
        self.container = container
        self.atualizar()

    def atualizar(self):
        if self.container is None or not self.container.winfo_exists():
            return

        for widget in self.container.winfo_children():
            widget.destroy()

        self.linhas.clear()
        documento = self.owner.canvas_editor.obter_documento()
        elementos = sorted(
            documento.elementos,
            key=lambda item: item.camada,
            reverse=True,
        )

        if not elementos:
            ctk.CTkLabel(
                self.container,
                text="Nenhuma camada.",
                text_color="gray70",
            ).grid(row=0, column=0, sticky="ew", padx=6, pady=12)
            return

        for indice, elemento in enumerate(elementos):
            self._criar_linha(indice, elemento)

    def _criar_linha(self, indice, elemento):
        selecionado = (
            self.owner.elemento_selecionado is not None
            and self.owner.elemento_selecionado.id == elemento.id
        )

        linha = ctk.CTkFrame(
            self.container,
            fg_color=self.COR_ATIVA if selecionado else self.COR_NORMAL,
            corner_radius=7,
            height=46,
        )
        linha.grid(row=indice, column=0, sticky="ew", padx=3, pady=3)
        linha.grid_columnconfigure(2, weight=1)
        linha.grid_propagate(False)

        alca = ctk.CTkLabel(
            linha,
            text="☰",
            width=24,
            cursor="fleur",
            text_color="gray75",
        )
        alca.grid(row=0, column=0, padx=(6, 2), pady=5)

        icone = ctk.CTkLabel(
            linha,
            text=self._icone_elemento(elemento),
            width=26,
            font=("Arial", 16),
        )
        icone.grid(row=0, column=1, padx=2, pady=5)

        nome = ctk.CTkButton(
            linha,
            text=elemento.nome,
            anchor="w",
            height=32,
            fg_color="transparent",
            hover_color=self.COR_HOVER,
            command=lambda elemento_id=elemento.id: self.selecionar(elemento_id),
        )
        nome.grid(row=0, column=2, sticky="ew", padx=2, pady=5)
        nome.bind(
            "<Double-Button-1>",
            lambda evento, elemento_id=elemento.id: self.renomear(elemento_id),
            add="+",
        )

        botao_visivel = ctk.CTkButton(
            linha,
            text="👁" if elemento.visivel else "⊘",
            width=32,
            height=30,
            fg_color="transparent",
            hover_color=self.COR_HOVER,
            command=lambda elemento_id=elemento.id: self.alternar_visibilidade(elemento_id),
        )
        botao_visivel.grid(row=0, column=3, padx=1, pady=5)

        botao_bloqueio = ctk.CTkButton(
            linha,
            text="🔒" if elemento.bloqueado else "🔓",
            width=32,
            height=30,
            fg_color="transparent",
            hover_color=self.COR_HOVER,
            command=lambda elemento_id=elemento.id: self.alternar_bloqueio(elemento_id),
        )
        botao_bloqueio.grid(row=0, column=4, padx=(1, 5), pady=5)

        for widget in (linha, alca, icone):
            widget.bind(
                "<ButtonPress-1>",
                lambda evento, elemento_id=elemento.id: self._iniciar_arraste(elemento_id),
                add="+",
            )
            widget.bind("<B1-Motion>", self._mover_arraste, add="+")
            widget.bind("<ButtonRelease-1>", self._finalizar_arraste, add="+")

        self.linhas.append((elemento.id, linha))

    def selecionar(self, elemento_id):
        self.owner.canvas_editor.selecionar_elemento(elemento_id)

    def alternar_visibilidade(self, elemento_id):
        elemento = self._obter_elemento(elemento_id)
        if elemento is None:
            return

        elemento.visivel = not elemento.visivel
        if not elemento.visivel and self.owner.elemento_selecionado is elemento:
            self.owner.canvas_editor.selecionar_elemento(None)

        self.owner.canvas_editor.renderizar()
        self.owner._marcar_alterado(
            "Camada exibida." if elemento.visivel else "Camada ocultada."
        )

    def alternar_bloqueio(self, elemento_id):
        elemento = self._obter_elemento(elemento_id)
        if elemento is None:
            return

        elemento.bloqueado = not elemento.bloqueado
        self.owner.canvas_editor.renderizar()

        if self.owner.elemento_selecionado is elemento:
            self.owner.ao_selecionar_elemento(elemento)

        self.owner._marcar_alterado(
            "Camada bloqueada." if elemento.bloqueado else "Camada desbloqueada."
        )

    def renomear(self, elemento_id):
        elemento = self._obter_elemento(elemento_id)
        if elemento is None:
            return

        novo_nome = simpledialog.askstring(
            title="Renomear camada",
            prompt="Digite o novo nome da camada:",
            initialvalue=elemento.nome,
            parent=self.owner.winfo_toplevel(),
        )

        if novo_nome is None:
            return

        novo_nome = novo_nome.strip()
        if not novo_nome or novo_nome == elemento.nome:
            return

        elemento.nome = novo_nome
        if self.owner.elemento_selecionado is elemento:
            self.owner.ao_selecionar_elemento(elemento)

        self.owner._marcar_alterado("Camada renomeada.")

    def _iniciar_arraste(self, elemento_id):
        self.elemento_arrastado_id = elemento_id
        self.destino_arraste_id = elemento_id

    def _mover_arraste(self, evento):
        if self.elemento_arrastado_id is None:
            return

        destino = self._linha_no_y_raiz(evento.y_root)
        if destino is None:
            return

        self.destino_arraste_id = destino
        for elemento_id, linha in self.linhas:
            linha.configure(
                fg_color=(
                    self.COR_DESTINO
                    if elemento_id == destino
                    else self.COR_NORMAL
                )
            )

    def _finalizar_arraste(self, evento):
        origem = self.elemento_arrastado_id
        destino = self.destino_arraste_id
        self.elemento_arrastado_id = None
        self.destino_arraste_id = None

        if origem is None or destino is None or origem == destino:
            self.atualizar()
            return

        documento = self.owner.canvas_editor.obter_documento()
        exibidos = sorted(
            documento.elementos,
            key=lambda item: item.camada,
            reverse=True,
        )

        origem_elemento = next((item for item in exibidos if item.id == origem), None)
        destino_indice = next(
            (indice for indice, item in enumerate(exibidos) if item.id == destino),
            None,
        )

        if origem_elemento is None or destino_indice is None:
            self.atualizar()
            return

        exibidos.remove(origem_elemento)
        exibidos.insert(destino_indice, origem_elemento)

        # A lista visual é topo -> fundo; camada maior fica no topo.
        total = len(exibidos)
        for indice, elemento in enumerate(exibidos):
            elemento.camada = total - indice - 1

        documento.elementos.sort(key=lambda item: item.camada)
        self.owner.canvas_editor.renderizar()
        self.owner._marcar_alterado("Ordem das camadas alterada.")

    def _linha_no_y_raiz(self, y_root):
        for elemento_id, linha in self.linhas:
            topo = linha.winfo_rooty()
            base = topo + linha.winfo_height()
            if topo <= y_root <= base:
                return elemento_id
        return None

    def _obter_elemento(self, elemento_id):
        return self.owner.canvas_editor.obter_documento().obter_elemento(elemento_id)

    @staticmethod
    def _icone_elemento(elemento):
        if isinstance(elemento, TextElement):
            return "T"
        if isinstance(elemento, ImageElement):
            return "🖼"
        if isinstance(elemento, ShapeElement):
            return "●" if elemento.formato == "circulo" else "■"
        return "◆"
