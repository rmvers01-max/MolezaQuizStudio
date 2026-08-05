from __future__ import annotations
import json
from pathlib import Path

class MotionGraphicsReportWriter:
    def save(self, plan, path):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({
            "motion_graphics_version":"1.0",
            "plan":plan.to_dict(),
        }, ensure_ascii=False, indent=2), encoding="utf-8")
        return path
