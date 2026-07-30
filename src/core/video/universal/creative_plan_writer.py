from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class UniversalCreativePlanWriter:
    def save(
        self,
        creative_plan: dict[
            str,
            Any
        ],
        path,
    ) -> Path:
        path = Path(path)

        path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        path.write_text(
            json.dumps(
                creative_plan,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return path
