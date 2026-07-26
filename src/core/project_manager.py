from pathlib import Path
import json
import re


class ProjectManager:

    def __init__(self):
        self.pasta_output = Path("output")
        self.pasta_output.mkdir(
            parents=True,
            exist_ok=True
        )

    def criar_projeto(self, nome):
        nome_seguro = self._limpar_nome(nome)

        pasta_projeto = self.pasta_output / nome_seguro

        subpastas = [
            "imagens",
            "audios",
            "videos",
            "roteiro",
            "exportado"
        ]

        pasta_projeto.mkdir(
            parents=True,
            exist_ok=True
        )

        for subpasta in subpastas:
            (pasta_projeto / subpasta).mkdir(
                exist_ok=True
            )

        return pasta_projeto

    def salvar_quiz(self, pasta_projeto, perguntas):
        arquivo_quiz = Path(pasta_projeto) / "quiz.json"

        with open(
            arquivo_quiz,
            "w",
            encoding="utf-8"
        ) as arquivo_json:
            json.dump(
                perguntas,
                arquivo_json,
                ensure_ascii=False,
                indent=4
            )

    def salvar_configuracao_projeto(
        self,
        pasta_projeto,
        configuracao
    ):
        arquivo_configuracao = (
            Path(pasta_projeto) / "config.json"
        )

        with open(
            arquivo_configuracao,
            "w",
            encoding="utf-8"
        ) as arquivo_json:
            json.dump(
                configuracao,
                arquivo_json,
                ensure_ascii=False,
                indent=4
            )

    def listar_projetos(self):
        projetos = []

        for caminho in self.pasta_output.iterdir():
            if caminho.is_dir():
                projetos.append(caminho)

        projetos.sort(
            key=lambda projeto: projeto.stat().st_mtime,
            reverse=True
        )

        return projetos

    def carregar_quiz(self, pasta_projeto):
        arquivo_quiz = Path(pasta_projeto) / "quiz.json"

        if not arquivo_quiz.exists():
            return []

        try:
            with open(
                arquivo_quiz,
                "r",
                encoding="utf-8"
            ) as arquivo_json:
                return json.load(arquivo_json)

        except (
            json.JSONDecodeError,
            OSError
        ):
            return []

    def carregar_configuracao_projeto(
        self,
        pasta_projeto
    ):
        arquivo_configuracao = (
            Path(pasta_projeto) / "config.json"
        )

        if not arquivo_configuracao.exists():
            return {}

        try:
            with open(
                arquivo_configuracao,
                "r",
                encoding="utf-8"
            ) as arquivo_json:
                return json.load(arquivo_json)

        except (
            json.JSONDecodeError,
            OSError
        ):
            return {}

    def _limpar_nome(self, nome):
        nome = nome.strip()

        nome = re.sub(
            r'[<>:"/\\|?*]',
            "",
            nome
        )

        return nome or "Projeto sem nome"
