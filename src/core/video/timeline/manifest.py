from __future__ import annotations

import json
from pathlib import Path
from enum import Enum


class TimelineManifestWriter:
    """Salva a descrição da cena para depuração e futuras edições."""

    def salvar(
        self,
        cena,
        caminho,
    ) -> Path:
        caminho = Path(
            caminho
        )

        caminho.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        dados = self._converter(
            cena
        )

        caminho.write_text(
            json.dumps(
                dados,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return caminho

    def _converter(self, valor):
        if isinstance(valor, Enum):
            return valor.value

        if isinstance(valor, Path):
            return str(valor)

        if hasattr(valor, "__dataclass_fields__"):
            return {
                campo: self._converter(
                    getattr(valor, campo)
                )
                for campo in valor.__dataclass_fields__
            }

        if isinstance(valor, dict):
            return {
                str(chave): self._converter(
                    item
                )
                for chave, item in valor.items()
            }

        if isinstance(valor, (list, tuple)):
            return [
                self._converter(item)
                for item in valor
            ]

        return valor
