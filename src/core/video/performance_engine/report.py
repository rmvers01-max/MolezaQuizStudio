from __future__ import annotations
import json
from pathlib import Path
class PerformanceReportWriter:
    def save(self,engine,path):
        path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(json.dumps(engine.report(),ensure_ascii=False,indent=2),encoding="utf-8")
        return path
