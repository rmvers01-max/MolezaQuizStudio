from .base_provider import BaseAIProvider
from .http_utils import enviar_json


class OllamaProvider(BaseAIProvider):
    """Provedor local para Ollama."""

    def __init__(
        self,
        model: str,
        base_url: str = "http://localhost:11434",
        timeout: int = 300,
    ):
        self.model = model.strip()
        self.base_url = base_url.rstrip("/")
        self.timeout = max(int(timeout), 10)

        if not self.model:
            raise ValueError("Informe o modelo instalado no Ollama.")

    def gerar_texto(
        self,
        prompt: str,
        temperatura: float = 0.7,
    ) -> str:
        if not prompt.strip():
            raise ValueError("O prompt não pode ficar vazio.")

        dados = enviar_json(
            url=f"{self.base_url}/api/generate",
            payload={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": max(
                        0.0,
                        min(float(temperatura), 2.0),
                    )
                },
            },
            timeout=self.timeout,
        )

        texto = dados.get("response", "")

        if not isinstance(texto, str) or not texto.strip():
            raise RuntimeError(
                "O Ollama respondeu, mas não devolveu texto."
            )

        return texto.strip()
