from __future__ import annotations
import threading
from collections import OrderedDict
from PIL import Image, ImageFont
from .models import PerformanceMetrics

class LRUObjectCache:
    def __init__(self,max_items=192,max_bytes=384*1024*1024,metrics=None):
        self.max_items=max(int(max_items),1)
        self.max_bytes=max(int(max_bytes),1)
        self.metrics=metrics or PerformanceMetrics()
        self._items=OrderedDict(); self._bytes=0
        self._lock=threading.RLock()

    def get(self,key,copy_value=True):
        with self._lock:
            if key not in self._items:
                self.metrics.cache_misses+=1
                return None
            value,size=self._items.pop(key)
            self._items[key]=(value,size)
            self.metrics.cache_hits+=1
            return value.copy() if copy_value and isinstance(value,Image.Image) else value

    def put(self,key,value):
        size=value.width*value.height*len(value.getbands()) if isinstance(value,Image.Image) else 1024
        with self._lock:
            if key in self._items:
                _,old=self._items.pop(key); self._bytes-=old
            stored=value.copy() if isinstance(value,Image.Image) else value
            self._items[key]=(stored,size); self._bytes+=size
            while len(self._items)>self.max_items or self._bytes>self.max_bytes:
                _,(_,removed)=self._items.popitem(last=False)
                self._bytes-=removed; self.metrics.evictions+=1
            self.metrics.bytes_cached=self._bytes

    def get_or_create(self,key,factory,copy_value=True):
        cached=self.get(key,copy_value)
        if cached is not None:
            return cached
        value=factory(); self.put(key,value)
        return value.copy() if copy_value and isinstance(value,Image.Image) else value

    def clear(self):
        with self._lock:
            self._items.clear(); self._bytes=0; self.metrics.bytes_cached=0

class FontCache:
    def __init__(self):
        self._items={}; self._lock=threading.RLock()

    def get(self,size,bold=False):
        key=("bold" if bold else "regular",max(int(size),1))
        with self._lock:
            if key in self._items:
                return self._items[key]
            candidates=(("C:/Windows/Fonts/arialbd.ttf","C:/Windows/Fonts/Arial.ttf")
                        if bold else
                        ("C:/Windows/Fonts/Arial.ttf","C:/Windows/Fonts/arialbd.ttf"))
            for path in candidates:
                try:
                    font=ImageFont.truetype(path,key[1]); self._items[key]=font; return font
                except OSError:
                    pass
            font=ImageFont.load_default(); self._items[key]=font; return font
