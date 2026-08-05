from core.video.core_engine import AAACoreEngine, ServiceRegistry

def test_registry():
    registry=ServiceRegistry(); value=object(); registry.register("x",value); assert registry.resolve("x") is value

def test_pipeline_order():
    engine=AAACoreEngine(strict=False); calls=[]
    engine.pipeline.add_stage("b",lambda c:calls.append("b"),order=20)
    engine.pipeline.add_stage("a",lambda c:calls.append("a"),order=10)
    context=engine.run_pipeline({})
    assert calls==["a","b"]
    assert context["core_pipeline_executed"]==["a","b"]

def test_events():
    engine=AAACoreEngine(strict=False); engine.emit("before_render",question=1)
    assert engine.events.history()[0].name=="before_render"

def test_health_detects_missing():
    engine=AAACoreEngine(strict=False); report=engine.validate()
    assert report["healthy"] is False
    assert report["missing_services"]
