import os
from pathlib import Path
from typing import Optional

from PIL import Image, UnidentifiedImageError


class BrandingManager:
    EXTENSOES_PERMITIDAS = {
        ".png",
        ".jpg",
        ".jpeg",
        ".webp"
    }

    def __init__(self):
        self.pasta_raiz = Path(__file__).resolve().parents[2]
        self.pasta_branding = self.pasta_raiz / "assets" / "branding"

        self.caminho_mascote = self.pasta_branding / "mascote.png"
        self.caminho_logo = self.pasta_branding / "logo.png"

        self.criar_pastas()

    def criar_pastas(self):
        self.pasta_branding.mkdir(
            parents=True,
            exist_ok=True
        )

    def importar_mascote(
        self,
        caminho_origem
    ) -> Path:
        return self._importar_imagem(
            caminho_origem=caminho_origem,
            caminho_destino=self.caminho_mascote
        )

    def importar_logo(
        self,
        caminho_origem
    ) -> Path:
        return self._importar_imagem(
            caminho_origem=caminho_origem,
            caminho_destino=self.caminho_logo
        )

    def obter_mascote(self) -> Optional[Path]:
        if self.caminho_mascote.exists():
            return self.caminho_mascote

        return None

    def obter_logo(self) -> Optional[Path]:
        if self.caminho_logo.exists():
            return self.caminho_logo

        return None

    def remover_mascote(self) -> bool:
        return self._remover_arquivo(
            self.caminho_mascote
        )

    def remover_logo(self) -> bool:
        return self._remover_arquivo(
            self.caminho_logo
        )

    def abrir_pasta_branding(self):
        self.criar_pastas()

        if os.name == "nt":
            os.startfile(
                str(
                    self.pasta_branding.resolve()
                )
            )

            return

        raise OSError(
            "A abertura automática da pasta está disponível "
            "apenas no Windows."
        )

    def _importar_imagem(
        self,
        caminho_origem,
        caminho_destino: Path
    ) -> Path:
        origem = Path(
            caminho_origem
        )

        if not origem.exists():
            raise FileNotFoundError(
                f"O arquivo não foi encontrado:\n{origem}"
            )

        if not origem.is_file():
            raise ValueError(
                "O caminho selecionado não é um arquivo."
            )

        extensao = origem.suffix.lower()

        if extensao not in self.EXTENSOES_PERMITIDAS:
            extensoes = ", ".join(
                sorted(
                    self.EXTENSOES_PERMITIDAS
                )
            )

            raise ValueError(
                "Formato de imagem não permitido.\n\n"
                f"Formatos aceitos: {extensoes}"
            )

        self.criar_pastas()

        try:
            with Image.open(origem) as imagem_original:
                imagem_original.load()

                imagem = imagem_original.convert(
                    "RGBA"
                )

                imagem.save(
                    caminho_destino,
                    format="PNG",
                    optimize=True
                )

        except UnidentifiedImageError as erro:
            raise ValueError(
                "O arquivo selecionado não é uma imagem válida."
            ) from erro

        except OSError as erro:
            raise OSError(
                "Não foi possível processar a imagem selecionada."
            ) from erro

        return caminho_destino

    def _remover_arquivo(
        self,
        caminho: Path
    ) -> bool:
        if not caminho.exists():
            return False

        caminho.unlink()

        return True

