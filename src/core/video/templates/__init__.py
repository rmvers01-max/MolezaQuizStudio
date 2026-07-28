from .base_template import BaseVideoTemplate, TemplateContext
from .knowledge_template import KnowledgeVideoTemplate
from .preference_template import PreferenceVideoTemplate
from .preference_renderer import ProfessionalPreferenceRenderer
from .preference_schema import CAMPOS_DE_IMAGEM_ACEITOS, exemplo_pergunta_com_imagens
from .registry import VideoTemplateRegistry

__all__ = [
    "BaseVideoTemplate",
    "TemplateContext",
    "KnowledgeVideoTemplate",
    "PreferenceVideoTemplate",
    "ProfessionalPreferenceRenderer",
    "CAMPOS_DE_IMAGEM_ACEITOS",
    "exemplo_pergunta_com_imagens",
    "VideoTemplateRegistry",
]
