from __future__ import annotations
import json
from pathlib import Path
from .events import EventBus
from .pipeline import RenderPipeline
from .registry import ServiceRegistry

class AAACoreEngine:
    REQUIRED=("legacy_renderer","preference_renderer","template_registry","universal_registry","creative_director","production_engine","identity_engine","performance_engine")
    def __init__(self,strict=True):
        self.strict=bool(strict); self.services=ServiceRegistry(); self.events=EventBus(); self.pipeline=RenderPipeline(); self.last_health_report=None
    def register(self,name,service,replace=False): return self.services.register(name,service,replace)
    def resolve(self,name,required=True): return self.services.resolve(name,required)
    def validate(self):
        missing=[name for name in self.REQUIRED if not self.services.contains(name)]
        report={"healthy":not missing,"score":max(100-len(missing)*15,0),"missing_services":missing,"registered_services":list(self.services.names())}
        self.last_health_report=report
        if self.strict and missing: raise RuntimeError("AAA Core Engine: serviços ausentes: "+", ".join(missing))
        return report
    def emit(self,name,**payload): return self.events.emit(name,**payload)
    def run_pipeline(self,context): return self.pipeline.execute(context)
    def save_report(self,path):
        path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(json.dumps({"core_engine_version":"2.0","services":self.services.snapshot(),"pipeline_stages":list(self.pipeline.stages()),"health":self.last_health_report,"events":[{"name":e.name,"payload":e.payload,"created_at":e.created_at} for e in self.events.history()]},ensure_ascii=False,indent=2,default=str),encoding="utf-8")
        return path
