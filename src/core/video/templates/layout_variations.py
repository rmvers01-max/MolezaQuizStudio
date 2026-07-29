from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class LayoutVariation:
    nome: str
    caixa_a: tuple[int, int, int, int]
    caixa_b: tuple[int, int, int, int]
    caixa_ou: tuple[int, int, int, int]
    deslocamento_titulo_y: int = 0
    inclinacao_a: float = 0.0
    inclinacao_b: float = 0.0


class LayoutVariationRegistry:
    """
    Define variações automáticas de composição.

    A variação é escolhida pelo número da pergunta para evitar que
    todas as cenas usem exatamente a mesma organização.
    """

    VARIACOES = (
        LayoutVariation(
            nome="Clássico",
            caixa_a=(90, 275, 570, 535),
            caixa_b=(710, 275, 1190, 535),
            caixa_ou=(575, 325, 705, 455),
        ),
        LayoutVariation(
            nome="Elevado",
            caixa_a=(80, 250, 560, 510),
            caixa_b=(720, 300, 1200, 560),
            caixa_ou=(575, 330, 705, 460),
            deslocamento_titulo_y=-8,
        ),
        LayoutVariation(
            nome="Baixo",
            caixa_a=(110, 305, 590, 565),
            caixa_b=(690, 255, 1170, 515),
            caixa_ou=(575, 330, 705, 460),
            deslocamento_titulo_y=-14,
        ),
        LayoutVariation(
            nome="Compacto",
            caixa_a=(125, 285, 575, 525),
            caixa_b=(705, 285, 1155, 525),
            caixa_ou=(580, 335, 700, 445),
            deslocamento_titulo_y=-6,
        ),
    )

    def obter(
        self,
        numero_pergunta: int,
    ) -> LayoutVariation:
        indice = (
            max(int(numero_pergunta), 1)
            - 1
        ) % len(self.VARIACOES)

        return self.VARIACOES[indice]
