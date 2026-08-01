from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from .repository import IntelligenceRepository


class MetricsImporter:
    """
    Importa métricas fornecidas pelo usuário.

    Formatos aceitos:
    - JSON com um objeto ou lista de objetos;
    - CSV com cabeçalhos correspondentes aos campos de métricas.
    """

    FIELD_ALIASES = {
        "id": "video_id",
        "video": "video_id",
        "video_title": "title",
        "titulo": "title",
        "tipo": "quiz_type",
        "tema": "theme_pack",
        "impressoes": "impressions",
        "visualizacoes": "views",
        "ctr": "ctr_percent",
        "duracao_media": (
            "average_view_duration_seconds"
        ),
        "percentual_medio": (
            "average_percentage_viewed"
        ),
        "likes": "likes",
        "comentarios": "comments",
        "inscritos": "subscribers_gained",
        "retencao_30s": (
            "first_30_seconds_retention"
        ),
    }

    NUMERIC_FIELDS = {
        "impressions": int,
        "views": int,
        "watch_time_hours": float,
        "average_view_duration_seconds": float,
        "average_percentage_viewed": float,
        "ctr_percent": float,
        "likes": int,
        "comments": int,
        "subscribers_gained": int,
        "first_30_seconds_retention": float,
    }

    def import_file(
        self,
        path,
        repository: IntelligenceRepository,
    ) -> dict[str, Any]:
        path = Path(path)

        if not path.exists():
            return {
                "imported": 0,
                "errors": [
                    "Arquivo não encontrado."
                ],
            }

        suffix = path.suffix.lower()

        if suffix == ".json":
            rows = self._read_json(path)
        elif suffix == ".csv":
            rows = self._read_csv(path)
        else:
            return {
                "imported": 0,
                "errors": [
                    "Formato não suportado. Use JSON ou CSV."
                ],
            }

        imported = 0
        errors = []

        for index, row in enumerate(
            rows,
            start=1,
        ):
            normalized = self._normalize(
                row
            )

            if not normalized.get(
                "video_id"
            ):
                errors.append(
                    f"Linha {index}: video_id ausente."
                )
                continue

            repository.append_metrics(
                normalized
            )

            imported += 1

        return {
            "imported": imported,
            "errors": errors,
        }

    def _read_json(
        self,
        path: Path,
    ) -> list[dict[str, Any]]:
        value = json.loads(
            path.read_text(
                encoding="utf-8"
            )
        )

        if isinstance(value, dict):
            return [value]

        if isinstance(value, list):
            return [
                item
                for item in value
                if isinstance(item, dict)
            ]

        return []

    def _read_csv(
        self,
        path: Path,
    ) -> list[dict[str, Any]]:
        with path.open(
            "r",
            encoding="utf-8-sig",
            newline="",
        ) as handle:
            return list(
                csv.DictReader(handle)
            )

    def _normalize(
        self,
        row: dict[str, Any],
    ) -> dict[str, Any]:
        normalized = {}

        for raw_key, raw_value in row.items():
            key = str(
                raw_key
            ).strip().lower()

            key = self.FIELD_ALIASES.get(
                key,
                key,
            )

            value = raw_value

            if (
                isinstance(value, str)
                and not value.strip()
            ):
                value = None

            caster = self.NUMERIC_FIELDS.get(
                key
            )

            if (
                caster is not None
                and value is not None
            ):
                try:
                    value = caster(
                        str(value)
                        .replace("%", "")
                        .replace(",", ".")
                    )
                except ValueError:
                    value = None

            normalized[key] = value

        normalized.setdefault(
            "title",
            ""
        )

        normalized.setdefault(
            "quiz_type",
            ""
        )

        normalized.setdefault(
            "theme_pack",
            ""
        )

        return normalized
