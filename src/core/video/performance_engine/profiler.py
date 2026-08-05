from __future__ import annotations
import time
from contextlib import contextmanager

class PerformanceProfiler:
    def __init__(self,metrics):
        self.metrics=metrics
    @contextmanager
    def measure(self,name):
        started=time.perf_counter()
        try:
            yield
        finally:
            elapsed=time.perf_counter()-started
            self.metrics.timings[name]=self.metrics.timings.get(name,0.0)+elapsed
            key=f"{name}_calls"; self.metrics.counters[key]=self.metrics.counters.get(key,0)+1
