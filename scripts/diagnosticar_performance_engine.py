from PIL import Image
from core.video.performance_engine import AAAPerformanceEngine
engine=AAAPerformanceEngine()
calls={"n":0}
def factory():
    calls["n"]+=1
    return Image.new("RGBA",(320,180),(80,55,150,255))
engine.cached_image(("diag",1),factory)
engine.cached_image(("diag",1),factory)
assert calls["n"]==1
assert engine.metrics.cache_hits>=1
print("PERFORMANCE ENGINE OK")
print(engine.report())
