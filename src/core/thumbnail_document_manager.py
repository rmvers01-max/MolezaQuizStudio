import json
from pathlib import Path
from typing import Union

from core.thumbnail_elements import (
    ImageElement,
    ShapeElement,
    TextElement,
    ThumbnailDocument,
    ThumbnailElement
)


class ThumbnailDocumentManager:
    """
    Salva e carrega documentos do Editor de Thumbnail em JSON.
    """

    VERSAO = 1

    def salvar(
        self,
        documento: ThumbnailDocument,
        caminho_arquivo: Union[str, Path]
    ) -> Path:
        caminho_arquivo = Path(caminho_arquivo)

        if caminho_arquivo.suffix.lower() != ".json":
            caminho_arquivo = caminho_arquivo.with_suffix(".json")

        caminho_arquivo.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        dados = {
            "versao": self.VERSAO,
            "documento": documento.para_dict()
        }

        with open(
            caminho_arquivo,
            "w",
            encoding="utf-8"
        ) as arquivo:
            json.dump(
                dados,
                arquivo,
                ensure_ascii=False,
                indent=4
            )

        return caminho_arquivo

    def carregar(
        self,
        caminho_arquivo: Union[str, Path]
    ) -> ThumbnailDocument:
        caminho_arquivo = Path(caminho_arquivo)

        if not caminho_arquivo.exists():
            raise FileNotFoundError(
                f"O arquivo não foi encontrado:\n{caminho_arquivo}"
            )

        try:
            with open(
                caminho_arquivo,
                "r",
                encoding="utf-8"
            ) as arquivo:
                dados = json.load(arquivo)

        except json.JSONDecodeError as erro:
            raise ValueError(
                "O arquivo selecionado não contém um documento válido."
            ) from erro

        if not isinstance(dados, dict):
            raise ValueError(
                "A estrutura do documento é inválida."
            )

        dados_documento = dados.get(
            "documento",
            dados
        )

        if not isinstance(dados_documento, dict):
            raise ValueError(
                "Os dados do documento são inválidos."
            )

        documento = ThumbnailDocument(
            largura=self._converter_int(
                dados_documento.get("largura"),
                1280
            ),
            altura=self._converter_int(
                dados_documento.get("altura"),
                720
            ),
            cor_fundo=str(
                dados_documento.get(
                    "cor_fundo",
                    "#101820"
                )
            )
        )

        elementos = dados_documento.get(
            "elementos",
            []
        )

        if not isinstance(elementos, list):
            raise ValueError(
                "A lista de elementos do documento é inválida."
            )

        for dados_elemento in elementos:
            elemento = self._criar_elemento(
                dados_elemento
            )

            if elemento is not None:
                documento.adicionar_elemento(
                    elemento
                )

        documento.ordenar_camadas()

        return documento

    def _criar_elemento(
        self,
        dados
    ):
        if not isinstance(dados, dict):
            return None

        tipo = str(
            dados.get(
                "tipo",
                "elemento"
            )
        ).lower()

        dados_comuns = self._obter_dados_comuns(
            dados
        )

        if tipo == "texto":
            return TextElement(
                **dados_comuns,
                texto=str(
                    dados.get(
                        "texto",
                        "Novo texto"
                    )
                ),
                fonte=str(
                    dados.get(
                        "fonte",
                        "Arial"
                    )
                ),
                tamanho_fonte=self._converter_int(
                    dados.get("tamanho_fonte"),
                    64
                ),
                negrito=bool(
                    dados.get(
                        "negrito",
                        True
                    )
                ),
                cor=str(
                    dados.get(
                        "cor",
                        "#FFFFFF"
                    )
                ),
                alinhamento=str(
                    dados.get(
                        "alinhamento",
                        "centro"
                    )
                ),
                cor_contorno=str(
                    dados.get(
                        "cor_contorno",
                        "#000000"
                    )
                ),
                largura_contorno=self._converter_int(
                    dados.get("largura_contorno"),
                    0
                ),
                sombra=bool(
                    dados.get(
                        "sombra",
                        False
                    )
                ),
                cor_sombra=str(
                    dados.get(
                        "cor_sombra",
                        "#000000"
                    )
                ),
                deslocamento_sombra_x=self._converter_int(
                    dados.get("deslocamento_sombra_x"),
                    6
                ),
                deslocamento_sombra_y=self._converter_int(
                    dados.get("deslocamento_sombra_y"),
                    6
                )
            )

        if tipo == "imagem":
            return ImageElement(
                **dados_comuns,
                caminho=str(
                    dados.get(
                        "caminho",
                        ""
                    )
                ),
                preservar_proporcao=bool(
                    dados.get(
                        "preservar_proporcao",
                        True
                    )
                ),
                preencher_area=bool(
                    dados.get(
                        "preencher_area",
                        False
                    )
                ),
                borda=bool(
                    dados.get(
                        "borda",
                        False
                    )
                ),
                cor_borda=str(
                    dados.get(
                        "cor_borda",
                        "#FFFFFF"
                    )
                ),
                largura_borda=self._converter_int(
                    dados.get("largura_borda"),
                    0
                ),
                raio_borda=self._converter_int(
                    dados.get("raio_borda"),
                    0
                ),
                sombra=bool(
                    dados.get(
                        "sombra",
                        False
                    )
                ),
                desfoque_sombra=self._converter_int(
                    dados.get("desfoque_sombra"),
                    12
                ),
                opacidade_sombra=self._converter_int(
                    dados.get("opacidade_sombra"),
                    110
                )
            )

        if tipo == "forma":
            return ShapeElement(
                **dados_comuns,
                formato=str(
                    dados.get(
                        "formato",
                        "retangulo"
                    )
                ),
                cor=str(
                    dados.get(
                        "cor",
                        "#7D2FC5"
                    )
                ),
                cor_contorno=str(
                    dados.get(
                        "cor_contorno",
                        "#FFFFFF"
                    )
                ),
                largura_contorno=self._converter_int(
                    dados.get("largura_contorno"),
                    0
                ),
                raio=self._converter_int(
                    dados.get("raio"),
                    0
                )
            )

        return ThumbnailElement(
            **dados_comuns
        )

    def _obter_dados_comuns(
        self,
        dados
    ):
        return {
            "nome": str(
                dados.get(
                    "nome",
                    "Elemento"
                )
            ),
            "x": self._converter_float(
                dados.get("x"),
                0
            ),
            "y": self._converter_float(
                dados.get("y"),
                0
            ),
            "largura": max(
                self._converter_float(
                    dados.get("largura"),
                    100
                ),
                1
            ),
            "altura": max(
                self._converter_float(
                    dados.get("altura"),
                    100
                ),
                1
            ),
            "id": str(
                dados.get(
                    "id",
                    ""
                )
            ) or self._gerar_id_temporario(),
            "visivel": bool(
                dados.get(
                    "visivel",
                    True
                )
            ),
            "bloqueado": bool(
                dados.get(
                    "bloqueado",
                    False
                )
            ),
            "opacidade": max(
                0,
                min(
                    self._converter_int(
                        dados.get("opacidade"),
                        255
                    ),
                    255
                )
            ),
            "rotacao": self._converter_float(
                dados.get("rotacao"),
                0
            ),
            "camada": self._converter_int(
                dados.get("camada"),
                0
            )
        }

    def _gerar_id_temporario(self):
        from uuid import uuid4

        return str(uuid4())

    def _converter_int(
        self,
        valor,
        padrao
    ):
        try:
            return int(valor)
        except (
            TypeError,
            ValueError
        ):
            return int(padrao)

    def _converter_float(
        self,
        valor,
        padrao
    ):
        try:
            return float(valor)
        except (
            TypeError,
            ValueError
        ):
            return float(padrao)
