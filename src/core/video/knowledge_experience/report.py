from __future__ import annotations
import json
from pathlib import Path

class KnowledgeRendererReportWriter:
    def save(self, *, profile, reveal_plan, path):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({
            "knowledge_renderer_version": "2.0",
            "visual_profile": profile.to_dict(),
            "reveal_plan": dict(reveal_plan),
        }, ensure_ascii=False, indent=2), encoding="utf-8")
        return path
