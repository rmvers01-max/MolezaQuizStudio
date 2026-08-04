from __future__ import annotations
import json
from pathlib import Path

class EndingReportWriter:
    def save(self, direction, quality: dict, path) -> Path:
        path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
        payload = direction.to_dict() if hasattr(direction, 'to_dict') else dict(direction)
        payload = {'ending_version': '2.0', **payload, 'quality': dict(quality)}
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
        return path
