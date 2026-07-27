from datetime import datetime
from pathlib import Path
from typing import Any

from core.project_manager import ProjectManager


class AIProjectService:
    """
    Converte um resultado da Central de IA nos arquivos utilizados
    pelas outras páginas do Moleza Quiz Studio.
    """

    def __init__(
        self,
        project_manager: ProjectManager | None = None
    ):
        self.project_manager = (
            project_manager
            or ProjectManager()
        )

    def salvar_resultado(
        self,
        pasta_projeto,
        pedido,
        resultado
    ) -> dict[str, Path]:
        pasta = Path(
            pasta_projeto
        )

        tipo_quiz = self._identificar_tipo_quiz(
            tema=pedido.tema,
            perguntas=resultado.perguntas
        )

        perguntas = self._converter_perguntas(
            resultado.perguntas,
            tipo_quiz=tipo_quiz
        )

        dados_ia = resultado.para_dict()
        dados_ia["solicitacao"] = {
            "tema": pedido.tema,
            "publico": pedido.publico,
            "formato": pedido.formato,
            "quantidade_perguntas": (
                pedido.quantidade_perguntas
            ),
            "estilo": pedido.estilo,
            "observacoes": pedido.observacoes,
            "nome_canal": pedido.nome_canal
        }
        dados_ia["gerado_em"] = (
            datetime.now()
            .astimezone()
            .isoformat(timespec="seconds")
        )

        publicacao_anterior = (
            self.project_manager
            .carregar_publicacao(
                pasta
            )
        )

        publicacao = {
            **publicacao_anterior,
            "titulo": resultado.titulo,
            "descricao": (
                self._montar_descricao(
                    resultado.descricao,
                    resultado.hashtags
                )
            ),
            "tags": ", ".join(
                resultado.tags
            ),
            "texto_thumbnail": (
                resultado.texto_thumbnail
            ),
            "prompt_thumbnail": (
                resultado.prompt_thumbnail
            ),
            "titulo_alternativo": (
                resultado.titulo_alternativo
            ),
            "hashtags": resultado.hashtags
        }

        configuracao = (
            self.project_manager
            .atualizar_configuracao_projeto(
                pasta,
                {
                    "tema": pedido.tema,
                    "quantidade_perguntas": len(
                        perguntas
                    ),
                    "publico": pedido.publico,
                    "formato": pedido.formato,
                    "estilo": pedido.estilo,
                    "status": "conteudo_ia_criado",
                    "origem_quiz": "central_ia",
                    "tipo_quiz": tipo_quiz
                }
            )
        )

        caminho_ia = (
            self.project_manager
            .salvar_ai_content(
                pasta,
                dados_ia
            )
        )

        caminho_quiz = (
            self.project_manager
            .salvar_quiz(
                pasta,
                perguntas
            )
        )

        caminho_publicacao = (
            self.project_manager
            .salvar_publicacao(
                pasta,
                publicacao
            )
        )

        return {
            "ai_content": caminho_ia,
            "quiz": caminho_quiz,
            "publicacao": caminho_publicacao,
            "configuracao": pasta / "config.json"
        }

    def _converter_perguntas(
        self,
        perguntas,
        tipo_quiz: str = "conhecimento"
    ) -> list[dict[str, Any]]:
        convertidas = []

        for indice, item in enumerate(
            perguntas,
            start=1
        ):
            if not isinstance(item, dict):
                continue

            texto = str(
                item.get(
                    "pergunta",
                    ""
                )
            ).strip()

            if not texto:
                continue

            alternativas = item.get(
                "alternativas"
            )

            if not isinstance(
                alternativas,
                list
            ):
                alternativas = item.get(
                    "opcoes",
                    []
                )

            if not isinstance(
                alternativas,
                list
            ):
                alternativas = []

            alternativas = [
                str(alternativa).strip()
                for alternativa in alternativas
                if str(alternativa).strip()
            ]

            resposta_bruta = item.get(
                "resposta",
                ""
            )

            resposta = (
                str(resposta_bruta).strip()
                if resposta_bruta is not None
                else ""
            )

            narracao = str(
                item.get(
                    "narracao",
                    texto
                )
            ).strip()

            if tipo_quiz == "preferencia":
                resposta = ""

            convertidas.append({
                "numero": indice,
                "tipo_quiz": tipo_quiz,
                "pergunta": texto,
                "alternativas": alternativas,
                "resposta": resposta,
                "narracao": narracao
            })

        if not convertidas:
            raise ValueError(
                "A resposta da IA não contém perguntas válidas."
            )

        return convertidas

    def _identificar_tipo_quiz(
        self,
        tema,
        perguntas
    ) -> str:
        tema_normalizado = self._normalizar_texto(
            tema
        )

        expressoes_preferencia = (
            "o que voce prefere",
            "qual voce prefere",
            "voce prefere",
            "voce escolheria",
            "qual voce escolheria",
            "faca sua escolha",
            "escolha um",
            "isto ou aquilo",
            "this or that"
        )

        if any(
            expressao in tema_normalizado
            for expressao in expressoes_preferencia
        ):
            return "preferencia"

        perguntas_validas = [
            item
            for item in perguntas
            if isinstance(item, dict)
        ]

        if perguntas_validas and all(
            not str(
                item.get(
                    "resposta",
                    ""
                )
            ).strip()
            for item in perguntas_validas
        ):
            return "preferencia"

        return "conhecimento"

    def _normalizar_texto(
        self,
        texto
    ) -> str:
        import unicodedata

        normalizado = unicodedata.normalize(
            "NFKD",
            str(texto).lower()
        )

        return "".join(
            caractere
            for caractere in normalizado
            if not unicodedata.combining(
                caractere
            )
        )

    def _montar_descricao(
        self,
        descricao,
        hashtags
    ):
        descricao = str(
            descricao
        ).strip()

        hashtags_validas = [
            str(item).strip()
            for item in hashtags
            if str(item).strip()
        ]

        if not hashtags_validas:
            return descricao

        linha_hashtags = " ".join(
            hashtags_validas
        )

        if linha_hashtags in descricao:
            return descricao

        return (
            f"{descricao}\n\n"
            f"{linha_hashtags}"
        )
