import unicodedata
from typing import Any

from .base_template import BaseVideoTemplate
from .knowledge_template import KnowledgeVideoTemplate
from .preference_template import PreferenceVideoTemplate


class VideoTemplateRegistry:
    def __init__(self):
        self._templates: dict[str, BaseVideoTemplate] = {
            "preferencia": PreferenceVideoTemplate(),
            "conhecimento": KnowledgeVideoTemplate(),
        }

    def obter(self, tipo_quiz: str) -> BaseVideoTemplate:
        return self._templates.get(
            str(tipo_quiz).strip().lower(),
            self._templates["conhecimento"],
        )

    def identificar_tipo(
        self,
        perguntas: list[dict[str, Any]],
        titulo_quiz: str = "",
    ) -> str:
        tipos = {
            str(pergunta.get("tipo_quiz", "")).strip().lower()
            for pergunta in perguntas
            if isinstance(pergunta, dict)
        }

        if "preferencia" in tipos:
            return "preferencia"

        if perguntas and all(
            not str(pergunta.get("resposta", "")).strip()
            for pergunta in perguntas
            if isinstance(pergunta, dict)
        ):
            return "preferencia"

        titulo = self._normalizar(titulo_quiz)
        expressoes = (
            "o que voce prefere",
            "qual voce prefere",
            "voce escolheria",
            "voce prefere",
            "faca sua escolha",
            "isto ou aquilo",
        )

        if any(expressao in titulo for expressao in expressoes):
            return "preferencia"

        return "conhecimento"

    def preparar_perguntas(
        self,
        perguntas: list[dict[str, Any]],
        titulo_quiz: str = "",
    ) -> tuple[str, list[dict[str, Any]]]:
        tipo = self.identificar_tipo(
            perguntas=perguntas,
            titulo_quiz=titulo_quiz,
        )
        template = self.obter(tipo)

        return (
            tipo,
            [
                template.preparar_pergunta(pergunta)
                for pergunta in perguntas
            ],
        )

    def _normalizar(self, texto: str) -> str:
        normalizado = unicodedata.normalize(
            "NFKD",
            str(texto).lower(),
        )

        return "".join(
            caractere
            for caractere in normalizado
            if not unicodedata.combining(caractere)
        )
