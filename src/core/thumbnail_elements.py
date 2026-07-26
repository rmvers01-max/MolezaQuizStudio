from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Optional
from uuid import uuid4


@dataclass
class ThumbnailElement:
    """
    Elemento genérico utilizado pelo editor de thumbnails.

    Todos os elementos possuem:
    - identificador único;
    - nome;
    - posição;
    - dimensões;
    - visibilidade;
    - bloqueio;
    - opacidade;
    - rotação;
    - ordem da camada.
    """

    nome: str
    x: float
    y: float
    largura: float
    altura: float

    id: str = field(
        default_factory=lambda: str(uuid4())
    )

    tipo: str = "elemento"
    visivel: bool = True
    bloqueado: bool = False
    opacidade: int = 255
    rotacao: float = 0.0
    camada: int = 0

    def mover(
        self,
        novo_x: float,
        novo_y: float
    ):
        if self.bloqueado:
            return

        self.x = float(novo_x)
        self.y = float(novo_y)

    def deslocar(
        self,
        delta_x: float,
        delta_y: float
    ):
        if self.bloqueado:
            return

        self.x += float(delta_x)
        self.y += float(delta_y)

    def redimensionar(
        self,
        nova_largura: float,
        nova_altura: float
    ):
        if self.bloqueado:
            return

        self.largura = max(
            float(nova_largura),
            1.0
        )

        self.altura = max(
            float(nova_altura),
            1.0
        )

    def definir_opacidade(
        self,
        valor: int
    ):
        self.opacidade = max(
            0,
            min(
                int(valor),
                255
            )
        )

    def definir_rotacao(
        self,
        angulo: float
    ):
        if self.bloqueado:
            return

        self.rotacao = float(angulo) % 360

    def contem_ponto(
        self,
        ponto_x: float,
        ponto_y: float
    ) -> bool:
        if not self.visivel:
            return False

        return (
            self.x <= ponto_x <= self.x + self.largura
            and self.y <= ponto_y <= self.y + self.altura
        )

    def obter_caixa(
        self
    ) -> tuple[float, float, float, float]:
        return (
            self.x,
            self.y,
            self.x + self.largura,
            self.y + self.altura
        )

    def para_dict(
        self
    ) -> dict[str, Any]:
        return asdict(
            self
        )


@dataclass
class TextElement(ThumbnailElement):
    tipo: str = "texto"

    texto: str = "Novo texto"
    fonte: str = "Arial"
    tamanho_fonte: int = 64
    negrito: bool = True

    cor: str = "#FFFFFF"
    alinhamento: str = "centro"

    cor_contorno: str = "#000000"
    largura_contorno: int = 0

    sombra: bool = False
    cor_sombra: str = "#000000"
    deslocamento_sombra_x: int = 6
    deslocamento_sombra_y: int = 6

    def definir_texto(
        self,
        texto: str
    ):
        self.texto = str(
            texto
        )

    def definir_tamanho_fonte(
        self,
        tamanho: int
    ):
        self.tamanho_fonte = max(
            int(tamanho),
            1
        )


@dataclass
class ImageElement(ThumbnailElement):
    tipo: str = "imagem"

    caminho: str = ""
    preservar_proporcao: bool = True
    preencher_area: bool = False

    borda: bool = False
    cor_borda: str = "#FFFFFF"
    largura_borda: int = 0
    raio_borda: int = 0

    sombra: bool = False
    desfoque_sombra: int = 12
    opacidade_sombra: int = 110

    def obter_caminho(
        self
    ) -> Optional[Path]:
        if not self.caminho:
            return None

        caminho = Path(
            self.caminho
        )

        if not caminho.exists():
            return None

        return caminho

    def definir_caminho(
        self,
        caminho
    ):
        self.caminho = str(
            Path(
                caminho
            )
        )


@dataclass
class ShapeElement(ThumbnailElement):
    tipo: str = "forma"

    formato: str = "retangulo"
    cor: str = "#7D2FC5"

    cor_contorno: str = "#FFFFFF"
    largura_contorno: int = 0
    raio: int = 0


@dataclass
class ThumbnailDocument:
    """
    Documento completo do editor.

    As coordenadas são armazenadas na resolução real da thumbnail,
    normalmente 1280 × 720.
    """

    largura: int = 1280
    altura: int = 720
    cor_fundo: str = "#101820"

    elementos: list[ThumbnailElement] = field(
        default_factory=list
    )

    def adicionar_elemento(
        self,
        elemento: ThumbnailElement
    ):
        if elemento.camada == 0 and self.elementos:
            maior_camada = max(
                item.camada
                for item in self.elementos
            )

            elemento.camada = maior_camada + 1

        self.elementos.append(
            elemento
        )

        self.ordenar_camadas()

    def remover_elemento(
        self,
        elemento_id: str
    ) -> bool:
        quantidade_anterior = len(
            self.elementos
        )

        self.elementos = [
            elemento
            for elemento in self.elementos
            if elemento.id != elemento_id
        ]

        return (
            len(self.elementos)
            != quantidade_anterior
        )

    def obter_elemento(
        self,
        elemento_id: str
    ) -> Optional[ThumbnailElement]:
        for elemento in self.elementos:
            if elemento.id == elemento_id:
                return elemento

        return None

    def obter_elemento_no_ponto(
        self,
        x: float,
        y: float
    ) -> Optional[ThumbnailElement]:
        elementos_ordenados = sorted(
            self.elementos,
            key=lambda item: item.camada,
            reverse=True
        )

        for elemento in elementos_ordenados:
            if elemento.contem_ponto(
                x,
                y
            ):
                return elemento

        return None

    def trazer_para_frente(
        self,
        elemento_id: str
    ):
        elemento = self.obter_elemento(
            elemento_id
        )

        if elemento is None:
            return

        maior_camada = max(
            (
                item.camada
                for item in self.elementos
            ),
            default=0
        )

        elemento.camada = maior_camada + 1
        self.ordenar_camadas()

    def enviar_para_tras(
        self,
        elemento_id: str
    ):
        elemento = self.obter_elemento(
            elemento_id
        )

        if elemento is None:
            return

        menor_camada = min(
            (
                item.camada
                for item in self.elementos
            ),
            default=0
        )

        elemento.camada = menor_camada - 1
        self.ordenar_camadas()

    def ordenar_camadas(
        self
    ):
        self.elementos.sort(
            key=lambda item: item.camada
        )

    def para_dict(
        self
    ) -> dict[str, Any]:
        return {
            "largura": self.largura,
            "altura": self.altura,
            "cor_fundo": self.cor_fundo,
            "elementos": [
                elemento.para_dict()
                for elemento in self.elementos
            ]
        }
