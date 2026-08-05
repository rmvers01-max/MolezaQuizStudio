from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
import threading

@dataclass(frozen=True, slots=True)
class CoreEvent:
    name: str
    payload: dict
    created_at: str = field(default_factory=lambda: datetime.now().isoformat(timespec="seconds"))

class EventBus:
    def __init__(self):
        self._history=[]; self._listeners={}; self._lock=threading.RLock()
    def subscribe(self,name,listener):
        with self._lock: self._listeners.setdefault(str(name),[]).append(listener)
    def emit(self,name,**payload):
        event=CoreEvent(str(name),dict(payload))
        with self._lock:
            self._history.append(event); listeners=list(self._listeners.get(event.name,()))
        for listener in listeners: listener(event)
        return event
    def history(self):
        with self._lock: return tuple(self._history)
