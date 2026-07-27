from .base_template import BaseVideoTemplate


class KnowledgeVideoTemplate(BaseVideoTemplate):
    tipo_quiz = "conhecimento"
    nome = "Quiz de conhecimento"

    def texto_encerramento_padrao(self) -> str:
        return "Comente quantos pontos você fez!"
