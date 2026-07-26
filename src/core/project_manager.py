from pathlib import Path
import json


class ProjectManager:

    def criar_projeto(self, nome):

        pasta = Path("output") / nome

        subpastas = [
            "imagens",
            "audios",
            "videos",
            "roteiro",
            "exportado"
        ]

        pasta.mkdir(parents=True, exist_ok=True)

        for sub in subpastas:
            (pasta / sub).mkdir(exist_ok=True)

        return pasta

    def salvar_quiz(self, pasta_projeto, perguntas):

        arquivo = pasta_projeto / "quiz.json"

        with open(arquivo, "w", encoding="utf-8") as f:
            json.dump(
                perguntas,
                f,
                ensure_ascii=False,
                indent=4
            )
