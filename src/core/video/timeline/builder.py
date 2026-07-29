from __future__ import annotations

from .models import (
    AnimationSpec,
    LayerType,
    TimelineLayer,
    TimelineScene,
)


class TimelineSceneBuilder:
    """
    Construtor de cenas em camadas.

    Nesta etapa, ele cria a estrutura lógica da cena.
    O renderizador atual continua sendo usado como fallback,
    permitindo migração gradual e segura.
    """

    def __init__(
        self,
        nome: str,
        duracao: float,
        largura: int = 1280,
        altura: int = 720,
        fps: int = 30,
    ):
        self.scene = TimelineScene(
            nome=nome,
            duracao=float(duracao),
            largura=int(largura),
            altura=int(altura),
            fps=int(fps),
        )

    def adicionar(
        self,
        nome: str,
        tipo: LayerType,
        z_index: int,
        inicio: float,
        duracao: float,
        origem=None,
        propriedades=None,
        animacoes=None,
    ):
        camada = TimelineLayer(
            nome=nome,
            tipo=tipo,
            z_index=int(z_index),
            inicio=float(inicio),
            duracao=float(duracao),
            origem=origem,
            propriedades=dict(
                propriedades or {}
            ),
            animacoes=list(
                animacoes or []
            ),
        )

        self.scene.adicionar_camada(
            camada
        )

        return self

    def construir(self) -> TimelineScene:
        self.scene.validar()
        return self.scene


def animacao(
    nome: str,
    inicio: float = 0.0,
    duracao: float = 0.5,
    **parametros
) -> AnimationSpec:
    return AnimationSpec(
        nome=nome,
        inicio=float(inicio),
        duracao=float(duracao),
        parametros=parametros,
    )
