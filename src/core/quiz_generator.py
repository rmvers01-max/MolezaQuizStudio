from core.ai_generator import AIGenerator
from core.project_manager import ProjectManager


class QuizGenerator:

    def __init__(self):

        self.ai = AIGenerator()
        self.project = ProjectManager()

    def gerar_quiz(self, tema, quantidade):

        pasta = self.project.criar_projeto(tema)

        perguntas = self.ai.gerar(
            tema,
            quantidade
        )

        self.project.salvar_quiz(
            pasta,
            perguntas
        )

        return perguntas
