from pathlib import Path
import json
import re
from typing import Any


class ProjectManager:
    """Cria, lista e persiste os arquivos dos projetos."""

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
        return self.salvar_json(
            pasta_projeto=pasta_projeto,
            nome_arquivo="quiz.json",
            dados=perguntas
        )

    def salvar_configuracao_projeto(
        self,
        pasta_projeto,
        configuracao
    ):
        return self.salvar_json(
            pasta_projeto=pasta_projeto,
            nome_arquivo="config.json",
            dados=configuracao
        )

    def salvar_ai_content(
        self,
        pasta_projeto,
        dados
    ):
        return self.salvar_json(
            pasta_projeto=pasta_projeto,
            nome_arquivo="ai_content.json",
            dados=dados
        )

    def salvar_publicacao(
        self,
        pasta_projeto,
        dados
    ):
        return self.salvar_json(
            pasta_projeto=pasta_projeto,
            nome_arquivo="publicacao.json",
            dados=dados
        )

    def salvar_json(
        self,
        pasta_projeto,
        nome_arquivo,
        dados
    ):
        pasta = Path(pasta_projeto)
        pasta.mkdir(
            parents=True,
            exist_ok=True
        )

        caminho = pasta / nome_arquivo

        with open(
            caminho,
            "w",
            encoding="utf-8"
        ) as arquivo_json:
            json.dump(
                dados,
                arquivo_json,
                ensure_ascii=False,
                indent=4
            )

        return caminho

    def atualizar_configuracao_projeto(
        self,
        pasta_projeto,
        novos_dados
    ):
        configuracao = self.carregar_configuracao_projeto(
            pasta_projeto
        )

        if not isinstance(configuracao, dict):
            configuracao = {}

        configuracao.update(
            novos_dados
        )

        self.salvar_configuracao_projeto(
            pasta_projeto,
            configuracao
        )

        return configuracao

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
        dados = self.carregar_json(
            pasta_projeto=pasta_projeto,
            nome_arquivo="quiz.json",
            padrao=[]
        )

        if isinstance(dados, list):
            return dados

        if isinstance(dados, dict):
            perguntas = dados.get(
                "perguntas",
                []
            )

            if isinstance(perguntas, list):
                return perguntas

        return []

    def carregar_configuracao_projeto(
        self,
        pasta_projeto
    ):
        dados = self.carregar_json(
            pasta_projeto=pasta_projeto,
            nome_arquivo="config.json",
            padrao={}
        )

        return dados if isinstance(dados, dict) else {}

    def carregar_ai_content(
        self,
        pasta_projeto
    ):
        dados = self.carregar_json(
            pasta_projeto=pasta_projeto,
            nome_arquivo="ai_content.json",
            padrao={}
        )

        return dados if isinstance(dados, dict) else {}

    def carregar_publicacao(
        self,
        pasta_projeto
    ):
        dados = self.carregar_json(
            pasta_projeto=pasta_projeto,
            nome_arquivo="publicacao.json",
            padrao={}
        )

        return dados if isinstance(dados, dict) else {}

    def carregar_json(
        self,
        pasta_projeto,
        nome_arquivo,
        padrao=None
    ):
        caminho = Path(pasta_projeto) / nome_arquivo

        if not caminho.exists():
            return padrao

        try:
            with open(
                caminho,
                "r",
                encoding="utf-8"
            ) as arquivo_json:
                return json.load(
                    arquivo_json
                )

        except (
            json.JSONDecodeError,
            OSError
        ):
            return padrao

    def _limpar_nome(self, nome):
        nome = str(nome).strip()

        nome = re.sub(
            r'[<>:"/\\|?*]',
            "",
            nome
        )

        nome = re.sub(
            r"\s+",
            " ",
            nome
        )

        return nome or "Projeto sem nome"
