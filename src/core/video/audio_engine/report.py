from __future__ import annotations

import json
from pathlib import Path


class AAAAudioReportWriter:
    def save(
        self,
        engine,
        path,
    ):
        if engine.last_plan is None:
            return None

        path = Path(path)
        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        path.write_text(
            json.dumps(
                engine.last_plan.to_dict(),
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return path
