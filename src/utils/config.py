from pathlib import Path
import json


class Config:

    def __init__(self):
        self.arquivo = Path("data") / "config.json"

        self.dados_padrao = {
            "tempo_pergunta": 5,
            "quantidade_perguntas": 10,
            "resolucao": "1920x1080",
            "fps": 30,
            "voz": "Feminina alegre"
        }

        self.dados = {}

        self.carregar()

    def carregar(self):
        self.arquivo.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        if not self.arquivo.exists():
            self.dados = self.dados_padrao.copy()
            self.salvar()
            return

        try:
            with open(
                self.arquivo,
                "r",
                encoding="utf-8"
            ) as arquivo_json:
                dados_salvos = json.load(arquivo_json)

        except (json.JSONDecodeError, OSError):
            dados_salvos = {}

        # Mantém valores padrão caso alguma configuração esteja faltando
        self.dados = self.dados_padrao.copy()
        self.dados.update(dados_salvos)

        self.salvar()

    def salvar(self):
        with open(
            self.arquivo,
            "w",
            encoding="utf-8"
        ) as arquivo_json:
            json.dump(
                self.dados,
                arquivo_json,
                ensure_ascii=False,
                indent=4
            )

    def get(self, chave, valor_padrao=None):
        return self.dados.get(
            chave,
            valor_padrao
        )

    def set(self, chave, valor):
        self.dados[chave] = valor
        self.salvar()

    def atualizar(self, novos_dados):
        self.dados.update(novos_dados)
        self.salvar()

    def restaurar_padrao(self):
        self.dados = self.dados_padrao.copy()
        self.salvar()
