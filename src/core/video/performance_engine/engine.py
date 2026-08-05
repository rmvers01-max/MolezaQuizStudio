from __future__ import annotations
import threading
from .cache import LRUObjectCache, FontCache
from .models import PerformanceMetrics
from .policy import PerformancePolicy
from .profiler import PerformanceProfiler

class AAAPerformanceEngine:
    _instance=None
    _lock=threading.Lock()
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance=super().__new__(cls); cls._instance._initialized=False
            return cls._instance
    def __init__(self):
        if self._initialized:
            return
        self.profile=PerformancePolicy.create("balanced")
        self.metrics=PerformanceMetrics()
        self.cache=LRUObjectCache(
            self.profile.max_cache_items,
            self.profile.max_cache_megabytes*1024*1024,
            self.metrics,
        )
        self.fonts=FontCache()
        self.profiler=PerformanceProfiler(self.metrics)
        self._initialized=True
    def cached_image(self,key,factory):
        return self.cache.get_or_create(key,factory,True)
    def configure(self,mode):
        self.profile=PerformancePolicy.create(mode)
        self.cache.max_items=self.profile.max_cache_items
        self.cache.max_bytes=self.profile.max_cache_megabytes*1024*1024
        return self.profile
    def report(self):
        return {"performance_engine_version":"1.0",
                "profile":self.profile.to_dict(),
                "metrics":self.metrics.to_dict()}
