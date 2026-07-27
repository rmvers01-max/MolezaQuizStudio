from typing import Any

from .base_provider import BaseAIProvider
from .http_utils import enviar_json


class OpenAIProvider(BaseAIProvider):
    """Provedor oficial da OpenAI usando a Responses API."""

    def __init__(
        self,
        api_key: str,
        model: str,
        base_url: str = "https://api.openai.com/v1",
        timeout: int = 120,
    ):
        self.api_key = api_key.strip()
        self.model = model.strip()
        self.base_url = base_url.rstrip("/")
        self.timeout = max(int(timeout), 10)

        if not self.api_key:
            raise ValueError("Informe a chave da API da OpenAI.")

        if not self.model:
            raise ValueError("Informe o modelo da OpenAI.")

    def gerar_texto(
        self,
        prompt: str,
        temperatura: float = 0.7,
    ) -> str:
        if not prompt.strip():
            raise ValueError("O prompt não pode ficar vazio.")

        dados = enviar_json(
            url=f"{self.base_url}/responses",
            payload={
                "model": self.model,
                "input": prompt,
                "store": False,
            },
            headers={
                "Authorization": f"Bearer {self.api_key}",
            },
            timeout=self.timeout,
        )

        texto = self._extrair_texto(dados)

        if not texto.strip():
            raise RuntimeError(
                "A OpenAI respondeu, mas não devolveu texto."
            )

        return texto.strip()

    def _extrair_texto(self, dados: dict[str, Any]) -> str:
        texto_direto = dados.get("output_text")

        if isinstance(texto_direto, str) and texto_direto.strip():
            return texto_direto

        partes = []

        for item in dados.get("output", []):
            if not isinstance(item, dict):
                continue

            for conteudo in item.get("content", []):
                if not isinstance(conteudo, dict):
                    continue

                texto = conteudo.get("text")

                if isinstance(texto, str) and texto.strip():
                    partes.append(texto)

        return "\n".join(partes)
