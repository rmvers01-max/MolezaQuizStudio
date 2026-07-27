import customtkinter as ctk

from core.thumbnail_document_manager import ThumbnailDocumentManager
from core.thumbnail_document_renderer import ThumbnailDocumentRenderer
from ui.thumbnail_editor_history import ThumbnailEditorHistoryController

from .colors_mixin import ColorsMixin
from .document_mixin import DocumentMixin
from .elements_mixin import ElementsMixin
from .helpers_mixin import HelpersMixin
from .layout_mixin import LayoutMixin
from .properties_mixin import PropertiesMixin


class ThumbnailEditorPage(
    LayoutMixin,
    ColorsMixin,
    DocumentMixin,
    ElementsMixin,
    PropertiesMixin,
    HelpersMixin,
    ctk.CTkFrame,
):
    """Editor visual de thumbnails do Moleza Quiz Studio."""

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
