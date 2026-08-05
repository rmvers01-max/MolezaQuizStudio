from PIL import Image
from core.video.performance_engine import (
    AAAPerformanceEngine, LRUObjectCache,
    PerformanceMetrics, PerformancePolicy,
)

def test_balanced_profile():
    p=PerformancePolicy.create("balanced")
    assert p.max_cache_megabytes<=384
    assert p.parallel_workers<=3
    assert p.reduced_blur is True

def test_cache_hit():
    m=PerformanceMetrics()
    c=LRUObjectCache(4,10*1024*1024,m)
    calls={"n":0}
    def factory():
        calls["n"]+=1
        return Image.new("RGBA",(100,100),(0,0,0,255))
    c.get_or_create("x",factory)
    c.get_or_create("x",factory)
    assert calls["n"]==1
    assert m.cache_hits==1

def test_font_cache():
    e=AAAPerformanceEngine()
    assert e.fonts.get(36,True) is e.fonts.get(36,True)
