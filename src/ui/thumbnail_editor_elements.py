from pathlib import Path
from tkinter import filedialog, messagebox

import customtkinter as ctk

from core.thumbnail_elements import ImageElement, ShapeElement, TextElement


class ThumbnailEditorElementsMixin:
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
        self.registrar_historico(documento)

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
            self._atualizar_rotulo_arquivo()
            self._atualizar_amostras_atuais()

            self.registrar_historico()

            self.status.configure(
                text="Propriedades aplicadas."
            )

        except ValueError as erro:
            messagebox.showerror(
                title="Valor inválido",
                message=str(erro),
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
        self.registrar_historico()

        self.atualizar_lista_camadas()
        self._atualizar_rotulo_arquivo()

        self.status.configure(
            text=mensagem
        )

