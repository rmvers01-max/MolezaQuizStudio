from pathlib import Path
import json


class Config:

	def __init__(self):

		self.arquivo = Path("data") / "config.json"

		self.dados_padrao = {

			"modelo_ia": "gpt-5.5",

			"tempo_pergunta": 5,

			"quantidade": 30,

			"resolucao": "1080x1920",

			"fps": 30,

			"voz": "pt-BR",

			"api_key": ""

		}

		self.carregar()

	def carregar(self):

		self.arquivo.parent.mkdir(exist_ok=True)

		if not self.arquivo.exists():

			self.salvar()

		with open(self.arquivo, "r", encoding="utf-8") as f:

			self.dados = json.load(f)

	def salvar(self):

		with open(self.arquivo, "w", encoding="utf-8") as f:

			json.dump(
				self.dados_padrao,
				f,
				indent=4,
				ensure_ascii=False
			)

	def get(self, chave):

		return self.dados[chave]

	def set(self, chave, valor):

		self.dados[chave] = valor

		with open(self.arquivo, "w", encoding="utf-8") as f:

			json.dump(
				self.dados,
				f,
				indent=4,
				ensure_ascii=False
			)

