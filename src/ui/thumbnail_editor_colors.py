from tkinter import colorchooser

from core.thumbnail_elements import ShapeElement, TextElement


class ThumbnailEditorColorsMixin:
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

        self.atualizar_lista_camadas()
        self._atualizar_rotulo_arquivo()

        self.registrar_historico()

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

