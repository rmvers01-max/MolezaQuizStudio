from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class IntelligenceRepository:
    def __init__(
        self,
        root,
    ):
        self.root = Path(root)

        self.root.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.productions_path = (
            self.root
            / "production_history.jsonl"
        )

        self.metrics_path = (
            self.root
            / "video_metrics.jsonl"
        )

        self.recommendations_path = (
            self.root
            / "latest_recommendations.json"
        )

    def append_production(
        self,
        production: dict[str, Any],
    ) -> None:
        self._append_jsonl(
            self.productions_path,
            production,
        )

    def append_metrics(
        self,
        metrics: dict[str, Any],
    ) -> None:
        self._append_jsonl(
            self.metrics_path,
            metrics,
        )

    def load_productions(
        self,
    ) -> list[dict[str, Any]]:
        return self._load_jsonl(
            self.productions_path
        )

    def load_metrics(
        self,
    ) -> list[dict[str, Any]]:
        return self._load_jsonl(
            self.metrics_path
        )

    def save_recommendations(
        self,
        report: dict[str, Any],
    ) -> Path:
        self.recommendations_path.write_text(
            json.dumps(
                report,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return self.recommendations_path

    def _append_jsonl(
        self,
        path: Path,
        payload: dict[str, Any],
    ) -> None:
        with path.open(
            "a",
            encoding="utf-8",
        ) as handle:
            handle.write(
                json.dumps(
                    payload,
                    ensure_ascii=False,
                )
            )

            handle.write("\n")

    def _load_jsonl(
        self,
        path: Path,
    ) -> list[dict[str, Any]]:
        if not path.exists():
            return []

        items = []

        for line in path.read_text(
            encoding="utf-8"
        ).splitlines():
            line = line.strip()

            if not line:
                continue

            try:
                value = json.loads(line)
            except json.JSONDecodeError:
                continue

            if isinstance(value, dict):
                items.append(value)

        return items
