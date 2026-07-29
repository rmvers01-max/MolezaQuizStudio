from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CameraProfile:
    nome: str
    zoom_inicial: float = 1.0
    zoom_final: float = 1.02
    pan_x: int = 0
    pan_y: int = 0
    rotacao: float = 0.0
    pulso_brilho: float = 0.0


class CameraProfileRegistry:
    """
    Perfis automáticos de câmera.

    O perfil é escolhido pelo número da pergunta para gerar variedade
    cinematográfica sem qualquer configuração manual.
    """

    PERFIS = (
        CameraProfile(
            nome="Zoom suave",
            zoom_final=1.020,
            pan_x=4,
            pan_y=0,
            rotacao=0.0,
            pulso_brilho=0.015,
        ),
        CameraProfile(
            nome="Pan direita",
            zoom_final=1.016,
            pan_x=12,
            pan_y=0,
            rotacao=0.15,
            pulso_brilho=0.012,
        ),
        CameraProfile(
            nome="Pan esquerda",
            zoom_final=1.018,
            pan_x=-12,
            pan_y=0,
            rotacao=-0.15,
            pulso_brilho=0.012,
        ),
        CameraProfile(
            nome="Subida suave",
            zoom_final=1.022,
            pan_x=0,
            pan_y=-8,
            rotacao=0.10,
            pulso_brilho=0.018,
        ),
        CameraProfile(
            nome="Descida suave",
            zoom_final=1.018,
            pan_x=0,
            pan_y=8,
            rotacao=-0.10,
            pulso_brilho=0.015,
        ),
    )

    def obter(
        self,
        numero_pergunta: int,
    ) -> CameraProfile:
        indice = (
            max(int(numero_pergunta), 1)
            - 1
        ) % len(self.PERFIS)

        return self.PERFIS[indice]
