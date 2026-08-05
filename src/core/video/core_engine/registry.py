from __future__ import annotations
import threading

class ServiceRegistry:
    def __init__(self):
        self._services={}
        self._lock=threading.RLock()
    def register(self,name,service,replace=False):
        name=str(name).strip()
        if not name: raise ValueError("Nome de serviço vazio.")
        with self._lock:
            if name in self._services and not replace: return self._services[name]
            self._services[name]=service
            return service
    def resolve(self,name,required=True):
        with self._lock: value=self._services.get(str(name))
        if value is None and required: raise KeyError(f"Serviço não registrado: {name}")
        return value
    def contains(self,name):
        with self._lock: return str(name) in self._services
    def names(self):
        with self._lock: return tuple(sorted(self._services))
    def snapshot(self):
        with self._lock: return {k:type(v).__name__ for k,v in self._services.items()}
