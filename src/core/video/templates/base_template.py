from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class TemplateContext:
    tipo_quiz: str
    titulo_quiz: str
    total_perguntas: int


class BaseVideoTemplate(ABC):
    tipo_quiz = "conhecimento"
    nome = "Template base"

    def preparar_pergunta(
        self,
        pergunta: dict[str, Any],
    ) -> dict[str, Any]:
        preparada = dict(pergunta)
        preparada["tipo_quiz"] = self.tipo_quiz
        return preparada

    @abstractmethod
    def texto_encerramento_padrao(self) -> str:
        raise NotImplementedError
