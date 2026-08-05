from __future__ import annotations
import os
from .models import PerformanceProfile

class PerformancePolicy:
    @staticmethod
    def create(mode="balanced"):
        mode=str(mode or "balanced").lower()
        cpus=max(int(os.cpu_count() or 2),1)
        if mode=="fast":
            return PerformanceProfile("fast",128,256,True,24,max(min(cpus-1,3),1),{"ram_gb":8})
        if mode=="quality":
            return PerformanceProfile("quality",256,512,False,24,max(min(cpus-1,4),1),{"ram_gb":16})
        return PerformanceProfile("balanced",192,384,True,24,max(min(cpus-1,3),1),{"ram_gb":8,"default":True})
