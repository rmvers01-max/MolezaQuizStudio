from pathlib import Path

from PIL import Image


class MascotWidget:
    """
    Localiza e prepara automaticamente o mascote do Moleza Quiz.

    Suporta poses diferentes. Quando uma pose específica não existe,
    usa a imagem principal do mascote como fallback.
    """

    PASTAS = (
        Path("assets/mascots"),
        Path("assets/mascot"),
        Path("assets"),
    )

    NOMES_PADRAO = (
        "moleza.png",
        "mascote.png",
    )

    NOMES_POSE = {
        "idle": (
            "idle.png",
            "moleza_idle.png",
            "mascote_idle.png",
        ),
        "thinking": (
            "thinking.png",
            "pensando.png",
            "moleza_thinking.png",
            "moleza_pensando.png",
        ),
        "celebrate": (
            "celebrate.png",
            "comemorando.png",
            "happy.png",
            "moleza_celebrate.png",
            "moleza_comemorando.png",
        ),
        "wave": (
            "wave.png",
            "aceno.png",
            "moleza_wave.png",
        ),
    }

    def localizar(self) -> Path | None:
        for pasta in self.PASTAS:
            for nome in self.NOMES_PADRAO:
                caminho = pasta / nome

                if caminho.exists():
                    return caminho

        return None

    def localizar_pose(
        self,
        pose="idle"
    ) -> Path | None:
        nomes = self.NOMES_POSE.get(
            str(pose).strip().lower(),
            ()
        )

        for pasta in self.PASTAS:
            for nome in nomes:
                caminho = pasta / nome

                if caminho.exists():
                    return caminho

        return self.localizar()

    def preparar(
        self,
        tamanho=(170, 170),
    ) -> Image.Image | None:
        return self.preparar_pose(
            pose="idle",
            tamanho=tamanho
        )

    def preparar_pose(
        self,
        pose="idle",
        tamanho=(170, 170),
    ) -> Image.Image | None:
        caminho = self.localizar_pose(
            pose
        )

        if caminho is None:
            return None

        try:
            imagem = Image.open(
                caminho
            ).convert("RGBA")

            imagem.thumbnail(
                tamanho,
                Image.Resampling.LANCZOS,
            )

            return imagem

        except OSError:
            return None
