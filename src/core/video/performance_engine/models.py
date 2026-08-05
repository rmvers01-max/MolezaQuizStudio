from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

@dataclass(frozen=True, slots=True)
class PerformanceProfile:
    code: str
    max_cache_items: int
    max_cache_megabytes: int
    reduced_blur: bool
    final_fps: int
    parallel_workers: int
    metadata: dict[str, Any] = field(default_factory=dict)
    def to_dict(self):
        return {
            "code":self.code,"max_cache_items":self.max_cache_items,
            "max_cache_megabytes":self.max_cache_megabytes,
            "reduced_blur":self.reduced_blur,"final_fps":self.final_fps,
            "parallel_workers":self.parallel_workers,
            "metadata":dict(self.metadata),
        }

@dataclass(slots=True)
class PerformanceMetrics:
    cache_hits: int=0
    cache_misses: int=0
    evictions: int=0
    bytes_cached: int=0
    timings: dict[str,float]=field(default_factory=dict)
    counters: dict[str,int]=field(default_factory=dict)
    def to_dict(self):
        total=self.cache_hits+self.cache_misses
        return {
            "cache_hits":self.cache_hits,"cache_misses":self.cache_misses,
            "cache_hit_rate":round(self.cache_hits/total,4) if total else 0.0,
            "evictions":self.evictions,"bytes_cached":self.bytes_cached,
            "timings":{k:round(v,6) for k,v in self.timings.items()},
            "counters":dict(self.counters),
        }
