from __future__ import annotations
import json
from pathlib import Path
class MascotActorReportWriter:
    def save(self, performance, path):
        path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(json.dumps({"mascot_actor_version":"1.0",**performance.to_dict()},ensure_ascii=False,indent=2),encoding='utf-8')
        return path
