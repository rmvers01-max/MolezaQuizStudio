from __future__ import annotations

import math
from pathlib import Path

from PIL import Image


class CharacterAnimationEngine:
    """
    Motor de animação do mascote Moleza.

    Recursos:
    - seleção automática de pose;
    - respiração;
    - piscar simulado;
    - balanço vertical;
    - inclinação de cabeça;
    - reação de pensamento;
    - comemoração;
    - apontar para esquerda ou direita;
    - fallback automático quando uma pose não existe.
    """

    PASTAS = (
        Path("assets/mascots"),
        Path("assets/mascot"),
        Path("assets"),
    )

    NOMES_POSE = {
        "idle": (
            "idle.png",
            "moleza_idle.png",
            "mascote_idle.png",
            "moleza.png",
            "mascote.png",
        ),
        "thinking": (
            "thinking.png",
            "pensando.png",
            "moleza_thinking.png",
            "moleza_pensando.png",
        ),
        "celebrate": (
            "celebrate.png",
            "happy.png",
            "comemorando.png",
            "moleza_celebrate.png",
            "moleza_comemorando.png",
        ),
        "point_left": (
            "point_left.png",
            "apontando_esquerda.png",
            "moleza_point_left.png",
        ),
        "point_right": (
            "point_right.png",
            "apontando_direita.png",
            "moleza_point_right.png",
        ),
        "wave": (
            "wave.png",
            "aceno.png",
            "moleza_wave.png",
        ),
    }

    def localizar_pose(
        self,
        pose: str,
    ) -> Path | None:
        chave = str(
            pose or "idle"
        ).strip().lower()

        nomes = self.NOMES_POSE.get(
            chave,
            ()
        )

        for pasta in self.PASTAS:
            for nome in nomes:
                caminho = pasta / nome

                if caminho.exists():
                    return caminho

        if chave != "idle":
            return self.localizar_pose(
                "idle"
            )

        return None

    def carregar_pose(
        self,
        pose: str,
    ) -> Image.Image | None:
        caminho = self.localizar_pose(
            pose
        )

        if caminho is None:
            return None

        try:
            return Image.open(
                caminho
            ).convert("RGBA")

        except OSError:
            return None

    def renderizar(
        self,
        pose: str,
        progresso: float,
        tamanho_base=(185, 185),
        comportamento: str = "auto",
        intensidade: float = 1.0,
    ) -> tuple[Image.Image | None, int, int]:
        """
        Retorna:
        - imagem transformada;
        - deslocamento horizontal;
        - deslocamento vertical.
        """
        imagem = self.carregar_pose(
            pose
        )

        if imagem is None:
            return None, 0, 0

        progresso = max(
            0.0,
            min(
                float(progresso),
                1.0
            )
        )

        comportamento = (
            self._resolver_comportamento(
                pose,
                comportamento
            )
        )

        intensidade = max(
            float(intensidade),
            0.0
        )

        escala = 1.0
        escala_y = 1.0
        rotacao = 0.0
        deslocamento_x = 0
        deslocamento_y = 0

        onda_lenta = math.sin(
            progresso
            * math.pi
            * 2
        )

        if comportamento == "idle":
            escala = (
                1.0
                + 0.022
                * intensidade
                * onda_lenta
            )

            deslocamento_y = int(
                5
                * intensidade
                * onda_lenta
            )

            rotacao = (
                1.2
                * intensidade
                * math.sin(
                    progresso
                    * math.pi
                )
            )

            escala_y = self._piscar(
                progresso,
                intensidade
            )

        elif comportamento == "thinking":
            escala = (
                1.0
                + 0.018
                * intensidade
                * onda_lenta
            )

            deslocamento_y = int(
                7
                * intensidade
                * math.sin(
                    progresso
                    * math.pi
                    * 2
                )
            )

            deslocamento_x = int(
                4
                * intensidade
                * math.sin(
                    progresso
                    * math.pi
                )
            )

            rotacao = (
                -3.0
                * intensidade
                * math.sin(
                    progresso
                    * math.pi
                )
            )

            escala_y = self._piscar(
                progresso,
                intensidade * 0.75
            )

        elif comportamento == "celebrate":
            quique = abs(
                math.sin(
                    progresso
                    * math.pi
                    * 3
                )
            )

            escala = (
                1.0
                + 0.065
                * intensidade
                * quique
            )

            deslocamento_y = int(
                -14
                * intensidade
                * quique
            )

            rotacao = (
                4.0
                * intensidade
                * math.sin(
                    progresso
                    * math.pi
                    * 4
                )
            )

        elif comportamento == "point_left":
            escala = (
                1.0
                + 0.025
                * intensidade
                * onda_lenta
            )

            deslocamento_x = int(
                -7
                * intensidade
                * abs(
                    math.sin(
                        progresso
                        * math.pi
                        * 2
                    )
                )
            )

            deslocamento_y = int(
                3
                * intensidade
                * onda_lenta
            )

            rotacao = (
                -2.0
                * intensidade
            )

            escala_y = self._piscar(
                progresso,
                intensidade * 0.65
            )

        elif comportamento == "point_right":
            escala = (
                1.0
                + 0.025
                * intensidade
                * onda_lenta
            )

            deslocamento_x = int(
                7
                * intensidade
                * abs(
                    math.sin(
                        progresso
                        * math.pi
                        * 2
                    )
                )
            )

            deslocamento_y = int(
                3
                * intensidade
                * onda_lenta
            )

            rotacao = (
                2.0
                * intensidade
            )

            escala_y = self._piscar(
                progresso,
                intensidade * 0.65
            )

        elif comportamento == "wave":
            escala = (
                1.0
                + 0.025
                * intensidade
                * onda_lenta
            )

            deslocamento_y = int(
                5
                * intensidade
                * onda_lenta
            )

            rotacao = (
                4.5
                * intensidade
                * math.sin(
                    progresso
                    * math.pi
                    * 4
                )
            )

            escala_y = self._piscar(
                progresso,
                intensidade * 0.7
            )

        largura_base = max(
            int(tamanho_base[0]),
            1
        )

        altura_base = max(
            int(tamanho_base[1]),
            1
        )

        imagem.thumbnail(
            (
                max(
                    int(
                        largura_base
                        * escala
                    ),
                    1
                ),
                max(
                    int(
                        altura_base
                        * escala
                    ),
                    1
                ),
            ),
            Image.Resampling.LANCZOS
        )

        if escala_y != 1.0:
            nova_altura = max(
                int(
                    imagem.height
                    * escala_y
                ),
                1
            )

            imagem = imagem.resize(
                (
                    imagem.width,
                    nova_altura
                ),
                Image.Resampling.LANCZOS
            )

        if abs(rotacao) > 0.01:
            imagem = imagem.rotate(
                rotacao,
                resample=Image.Resampling.BICUBIC,
                expand=True
            )

        return (
            imagem,
            deslocamento_x,
            deslocamento_y
        )

    def _resolver_comportamento(
        self,
        pose,
        comportamento
    ):
        comportamento = str(
            comportamento or "auto"
        ).strip().lower()

        if comportamento != "auto":
            return comportamento

        pose = str(
            pose or "idle"
        ).strip().lower()

        mapa = {
            "idle": "idle",
            "thinking": "thinking",
            "celebrate": "celebrate",
            "point_left": "point_left",
            "point_right": "point_right",
            "wave": "wave",
        }

        return mapa.get(
            pose,
            "idle"
        )

    def _piscar(
        self,
        progresso,
        intensidade
    ):
        """
        Simula piscada breve sem exigir sprites extras.
        O efeito é propositalmente discreto.
        """
        ciclos = (
            progresso
            * 3.0
        )

        fase = ciclos % 1.0

        if 0.46 <= fase <= 0.54:
            distancia = abs(
                fase - 0.50
            ) / 0.04

            fechamento = max(
                1.0 - distancia,
                0.0
            )

            return (
                1.0
                - 0.07
                * intensidade
                * fechamento
            )

        return 1.0
