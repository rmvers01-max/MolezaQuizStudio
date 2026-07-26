from core.ai_generator import AIGenerator
from core.project_manager import ProjectManager


class QuizGenerator:

    def __init__(self):
        self.ai = AIGenerator()
        self.project_manager = ProjectManager()

    def gerar_quiz(
        self,
        tema,
        quantidade,
        tempo_pergunta=5
    ):
        pasta_projeto = (
            self.project_manager.criar_projeto(tema)
        )

        perguntas = self.ai.gerar(
            tema,
            quantidade
        )

        configuracao_projeto = {
            "tema": tema,
            "quantidade_perguntas": quantidade,
            "tempo_pergunta": tempo_pergunta,
            "status": "quiz_criado"
        }

        self.project_manager.salvar_quiz(
            pasta_projeto,
            perguntas
        )

        self.project_manager.salvar_configuracao_projeto(
            pasta_projeto,
            configuracao_projeto
        )

        return perguntas
