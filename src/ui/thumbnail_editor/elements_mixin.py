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


class ElementsMixin:
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
        if hasattr(self, "layers_controller"):
            self.layers_controller.atualizar()

