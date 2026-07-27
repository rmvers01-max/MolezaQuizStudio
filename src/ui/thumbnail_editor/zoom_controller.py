class ZoomController:
    """Controla o zoom do canvas entre 25% e 400%."""

    ZOOM_MINIMO = 25
    ZOOM_MAXIMO = 400
    PASSO_ZOOM = 25

    def __init__(self, canvas_editor, ao_alterar=None):
        self.canvas_editor = canvas_editor
        self.ao_alterar = ao_alterar

    def definir(self, percentual):
        valor = max(
            self.ZOOM_MINIMO,
            min(int(round(float(percentual))), self.ZOOM_MAXIMO)
        )
        self.canvas_editor.definir_zoom(valor)
        self._notificar(valor)
        return valor

    def aumentar(self):
        return self.definir(
            self.canvas_editor.obter_zoom() + self.PASSO_ZOOM
        )

    def diminuir(self):
        return self.definir(
            self.canvas_editor.obter_zoom() - self.PASSO_ZOOM
        )

    def tamanho_real(self):
        return self.definir(100)

    def ajustar_tela(self):
        self.canvas_editor.ajustar_zoom_tela()
        self._notificar(self.canvas_editor.obter_zoom())
        return self.canvas_editor.obter_zoom()

    def _notificar(self, valor):
        if callable(self.ao_alterar):
            self.ao_alterar(valor)
