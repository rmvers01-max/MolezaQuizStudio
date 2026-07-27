import json
import re

from .models import AIContentRequest, AIContentResult
from .prompt_builder import MolezaPromptBuilder


class AIContentGenerator:
    def __init__(
        self,
        provider,
        prompt_builder: MolezaPromptBuilder | None = None,
    ):
        self.provider = provider
        self.prompt_builder = prompt_builder or MolezaPromptBuilder()

    def gerar(
        self,
        pedido: AIContentRequest,
    ) -> AIContentResult:
        prompt = self.prompt_builder.criar_prompt(pedido)
        resposta = self.provider.gerar_texto(prompt)
        dados = self._converter_resposta_json(resposta)

        resultado = AIContentResult.de_dict(dados)
        resultado.validar()

        return resultado

    def _converter_resposta_json(self, resposta: str) -> dict:
        texto = resposta.strip()

        if texto.startswith("```"):
            texto = re.sub(
                r"^```(?:json)?\s*",
                "",
                texto,
                flags=re.IGNORECASE,
            )
            texto = re.sub(r"\s*```$", "", texto)

        try:
            dados = json.loads(texto)

        except json.JSONDecodeError:
            inicio = texto.find("{")
            fim = texto.rfind("}")

            if inicio < 0 or fim <= inicio:
                raise ValueError(
                    "A IA não devolveu um JSON reconhecível."
                )

            try:
                dados = json.loads(texto[inicio: fim + 1])

            except json.JSONDecodeError as erro:
                raise ValueError(
                    "A resposta da IA contém JSON inválido."
                ) from erro

        if not isinstance(dados, dict):
            raise ValueError(
                "A resposta da IA deve ser um objeto JSON."
            )

        return dados
