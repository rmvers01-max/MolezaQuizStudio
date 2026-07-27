import json
import urllib.error
import urllib.request
from typing import Any


def enviar_json(
    url: str,
    payload: dict[str, Any],
    headers: dict[str, str] | None = None,
    timeout: int = 120,
) -> dict[str, Any]:
    requisicao = urllib.request.Request(
        url=url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            **(headers or {}),
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(
            requisicao,
            timeout=max(int(timeout), 10),
        ) as resposta:
            return json.loads(resposta.read().decode("utf-8"))

    except urllib.error.HTTPError as erro:
        corpo = erro.read().decode("utf-8", errors="replace")
        mensagem = extrair_mensagem_erro(corpo)
        raise RuntimeError(
            f"Erro da API ({erro.code}): {mensagem}"
        ) from erro

    except urllib.error.URLError as erro:
        raise RuntimeError(
            "Não foi possível conectar ao provedor de IA. "
            "Verifique a internet, o endereço da API e se o serviço está ativo."
        ) from erro

    except TimeoutError as erro:
        raise RuntimeError(
            "A geração demorou mais que o tempo limite."
        ) from erro


def extrair_mensagem_erro(corpo: str) -> str:
    try:
        dados = json.loads(corpo)
        erro = dados.get("error", {})

        if isinstance(erro, dict):
            mensagem = erro.get("message")
            if mensagem:
                return str(mensagem)

        mensagem = dados.get("message")
        if mensagem:
            return str(mensagem)

    except json.JSONDecodeError:
        pass

    return corpo.strip() or "Erro desconhecido."
