from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class PipelineStage:
    name: str
    handler: object
    order: int=100
    enabled: bool=True

class RenderPipeline:
    def __init__(self): self._stages=[]
    def add_stage(self,name,handler,order=100,enabled=True):
        self._stages.append(PipelineStage(str(name),handler,int(order),bool(enabled)))
        self._stages.sort(key=lambda item:(item.order,item.name))
    def execute(self,context):
        executed=[]
        for stage in self._stages:
            if stage.enabled:
                stage.handler(context); executed.append(stage.name)
        context["core_pipeline_executed"]=executed
        return context
    def stages(self): return tuple(stage.name for stage in self._stages if stage.enabled)
