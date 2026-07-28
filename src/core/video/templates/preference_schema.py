from typing import Any


def exemplo_pergunta_com_imagens() -> dict[str, Any]:
    """Exemplo do formato aceito pelo template de preferência."""
    return {
        "tipo_quiz": "preferencia",
        "pergunta": "O que você prefere comer?",
        "alternativas": [
            "Pizza",
            "Hambúrguer"
        ],
        "resposta": "",
        "imagem_a": "imagens/pizza.png",
        "imagem_b": "imagens/hamburguer.png"
    }


CAMPOS_DE_IMAGEM_ACEITOS = {
    "opcao_a": (
        "imagem_a",
        "imagem_esquerda",
        "imagem_opcao_a",
        "imagem_1"
    ),
    "opcao_b": (
        "imagem_b",
        "imagem_direita",
        "imagem_opcao_b",
        "imagem_2"
    ),
    "lista": "imagens"
}
