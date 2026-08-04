from __future__ import annotations
import json
from pathlib import Path

class CuriosityReportWriter:
    def save(self, plan, path, *, question_number: int):
        path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
        payload={"curiosity_engine_version":"1.0","question_number":question_number,**plan.to_dict()}
        path.write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8')
        return path
