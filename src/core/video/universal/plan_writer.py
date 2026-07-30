from __future__ import annotations

import json
from pathlib import Path

from .contracts import UniversalQuizPlan


class UniversalPlanWriter:
    def save(
        self,
        plan: UniversalQuizPlan,
        path,
    ) -> Path:
        path = Path(path)

        path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        path.write_text(
            json.dumps(
                plan.to_dict(),
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return path
