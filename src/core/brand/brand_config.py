from __future__ import annotations

import json
from pathlib import Path

from .brand_registry import BrandRegistry


class BrandConfigManager:
    """Cria e mantém o arquivo de identidade do canal."""

    def __init__(
        self,
        caminho="config/brand_profile.json",
    ):
        self.caminho = Path(caminho)

    def garantir_arquivo(
        self,
        codigo="moleza_quiz",
    ) -> Path:
        if self.caminho.exists():
            return self.caminho

        self.caminho.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        perfil = (
            BrandRegistry()
            .obter(codigo)
        )

        self.caminho.write_text(
            json.dumps(
                perfil.para_metadados(),
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return self.caminho
