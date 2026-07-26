class AIGenerator:

	def gerar(self, tema, quantidade):

		perguntas = []

		for i in range(int(quantidade)):

			perguntas.append({

				"pergunta": f"Pergunta criada por IA {i+1} sobre {tema}",

				"resposta": "Resposta IA"

			})

		return perguntas
