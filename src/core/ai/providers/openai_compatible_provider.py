from .base_provider import BaseAIProvider
from .http_utils import enviar_json


class OpenAICompatibleProvider(BaseAIProvider):
    """Cliente para APIs compatíveis com Chat Completions."""

    def __init__(
        self,
        api_key: str,
        model: str,
        base_url: str,
        timeout: int = 120,
        usar_temperatura: bool = True,
    ):
        self.api_key = api_key.strip()
        self.model = model.strip()
        self.base_url = base_url.rstrip("/")
        self.timeout = max(int(timeout), 10)
        self.usar_temperatura = bool(usar_temperatura)

        if not self.model:
            raise ValueError("Informe o modelo do provedor.")

        if not self.base_url:
            raise ValueError("Informe o endereço da API.")

    def gerar_texto(
        self,
        prompt: str,
        temperatura: float = 0.7,
    ) -> str:
        if not prompt.strip():
            raise ValueError("O prompt não pode ficar vazio.")

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        }

        if self.usar_temperatura:
            payload["temperature"] = max(
                0.0,
                min(float(temperatura), 2.0),
            )

        headers = {}

        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        dados = enviar_json(
            url=f"{self.base_url}/chat/completions",
            payload=payload,
            headers=headers,
            timeout=self.timeout,
        )

        try:
            texto = dados["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as erro:
            raise RuntimeError(
                "O provedor respondeu em um formato inesperado."
            ) from erro

        if not isinstance(texto, str) or not texto.strip():
            raise RuntimeError(
                "O provedor respondeu, mas não devolveu texto."
            )

        return texto.strip()
