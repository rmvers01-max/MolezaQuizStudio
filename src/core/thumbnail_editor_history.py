import customtkinter as ctk


class ThumbnailEditorHistoryMixin:
    def configurar_historico(self):
        self.restaurando_historico = False

        self.bind_all(
            "<Control-z>",
            self.desfazer
        )

        self.bind_all(
            "<Control-y>",
            self.refazer
        )

        self.bind_all(
            "<Control-Shift-Z>",
            self.refazer
        )

        self.bind_all(
            "<Control-Shift-z>",
            self.refazer
        )

        self._atualizar_botoes_historico()

    def iniciar_historico(self, documento):
        self.historico.iniciar(
            documento
        )

        self._atualizar_botoes_historico()

    def registrar_historico(self, documento=None):
        if self.restaurando_historico:
            return

        if documento is None:
            documento = (
                self.canvas_editor
                .obter_documento()
            )

        self.historico.registrar(
            documento
        )

        self._atualizar_botoes_historico()

    def desfazer(self, evento=None):
        documento = self.historico.desfazer()

        if documento is None:
            self.status.configure(
                text="Não há alterações para desfazer."
            )

            self._atualizar_botoes_historico()
            return "break"

        self._restaurar_estado_historico(
            documento,
            "Alteração desfeita."
        )

        return "break"

    def refazer(self, evento=None):
        documento = self.historico.refazer()

        if documento is None:
            self.status.configure(
                text="Não há alterações para refazer."
            )

            self._atualizar_botoes_historico()
            return "break"

        self._restaurar_estado_historico(
            documento,
            "Alteração refeita."
        )

        return "break"

    def _restaurar_estado_historico(
        self,
        documento,
        mensagem
    ):
        self.restaurando_historico = True
        self.historico.iniciar_restauracao()

        try:
            self.elemento_selecionado = None

            self.canvas_editor.definir_documento(
                documento
            )

            self.documento_alterado = True

            self.atualizar_lista_camadas()
            self._atualizar_rotulo_arquivo()

            self.status.configure(
                text=mensagem
            )

        finally:
            self.historico.finalizar_restauracao()
            self.restaurando_historico = False

        self._atualizar_botoes_historico()

    def _atualizar_botoes_historico(self):
        if not hasattr(self, "botao_desfazer"):
            return

        estado_desfazer = (
            "normal"
            if self.historico.pode_desfazer()
            else "disabled"
        )

        estado_refazer = (
            "normal"
            if self.historico.pode_refazer()
            else "disabled"
        )

        self.botao_desfazer.configure(
            state=estado_desfazer
        )

        self.botao_refazer.configure(
            state=estado_refazer
        )
