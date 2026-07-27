import json
import urllib.error
import urllib.request
from typing import Any


class OpenAIResponsesProvider:
    """
    Cliente HTTP leve para a Responses API.

    Não depende do pacote openai. Isso reduz conflitos de versões no projeto.
    """

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
            raise ValueError("Informe a chave da API.")

        if not self.model:
            raise ValueError("Informe o modelo da IA.")

    def gerar_texto(
        self,
        prompt: str,
        temperatura: float = 0.7,
    ) -> str:
        if not prompt.strip():
            raise ValueError("O prompt não pode ficar vazio.")

        payload = {
            "model": self.model,
            "input": prompt,
            "temperature": max(0.0, min(float(temperatura), 2.0)),
            "store": False,
        }

        requisicao = urllib.request.Request(
            url=f"{self.base_url}/responses",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(
                requisicao,
                timeout=self.timeout,
            ) as resposta:
                dados = json.loads(
                    resposta.read().decode("utf-8")
                )

        except urllib.error.HTTPError as erro:
            corpo = erro.read().decode("utf-8", errors="replace")
            mensagem = self._extrair_mensagem_erro(corpo)
            raise RuntimeError(
                f"Erro da API ({erro.code}): {mensagem}"
            ) from erro

        except urllib.error.URLError as erro:
            raise RuntimeError(
                "Não foi possível conectar ao provedor de IA. "
                "Verifique a internet e o endereço da API."
            ) from erro

        except TimeoutError as erro:
            raise RuntimeError(
                "A geração demorou mais que o tempo limite."
            ) from erro

        texto = self._extrair_texto(dados)

        if not texto.strip():
            raise RuntimeError(
                "O provedor respondeu, mas não devolveu texto."
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

    def _extrair_mensagem_erro(self, corpo: str) -> str:
        try:
            dados = json.loads(corpo)
            erro = dados.get("error", {})

            if isinstance(erro, dict):
                mensagem = erro.get("message")
                if mensagem:
                    return str(mensagem)

        except json.JSONDecodeError:
            pass

        return corpo.strip() or "Erro desconhecido."
