from __future__ import annotations
import math
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter
from .easing import MotionEasing
from ..performance_engine import AAAPerformanceEngine

class MotionGraphicsCompositor:
    def __init__(self):
        self.performance_engine = AAAPerformanceEngine()

    def animate_frame(self, *, image, plan, time, duration, accent_color):
        result = image.convert("RGBA")
        progress = MotionEasing.clamp(float(time)/max(float(duration),.001))
        result = self._glow(result, accent_color, time)
        result = self._shine(result, progress, accent_color)
        if plan.scene_kind == "countdown":
            pulse = 1 + .025*math.sin(time*math.pi*2)
            result = ImageEnhance.Brightness(result).enhance(max(pulse,.9))
        if plan.scene_kind == "reveal":
            result = self._burst(result, progress, accent_color)
        return result

    def transform_layer(self, *, layer, preset, progress):
        p = MotionEasing.clamp(progress)
        fn = {
            "spring": MotionEasing.spring,
            "ease_out_bounce": MotionEasing.ease_out_bounce,
            "ease_in_out_cubic": MotionEasing.ease_in_out_cubic,
            "ease_out_back": MotionEasing.ease_out_back,
        }.get(preset.easing, MotionEasing.ease_out_cubic)
        eased = fn(p)
        scale = preset.scale_from + (preset.scale_to-preset.scale_from)*eased
        size = (max(int(layer.width*scale),1), max(int(layer.height*scale),1))
        out = layer.resize(size, Image.Resampling.LANCZOS)
        radius = preset.blur*8*(1-p)
        return out.filter(ImageFilter.GaussianBlur(radius)) if radius > .05 else out

    def _glow(self, image, color, time):
        layer = Image.new("RGBA", image.size, (0,0,0,0))
        draw = ImageDraw.Draw(layer)
        w,h = image.size
        cx = int(w*.5 + math.sin(time*.8)*w*.08)
        cy = int(h*.45 + math.cos(time*.7)*h*.05)
        r = int(min(w,h)*.30)
        draw.ellipse((cx-r,cy-r,cx+r,cy+r), fill=(*color,34))
        factor = .24 if self.performance_engine.profile.reduced_blur else .45
        minimum = 12 if self.performance_engine.profile.reduced_blur else 24
        layer = layer.filter(ImageFilter.GaussianBlur(max(int(r*factor),minimum)))
        out = image.copy(); out.alpha_composite(layer); return out

    def _shine(self, image, progress, color):
        layer = Image.new("RGBA", image.size, (0,0,0,0))
        draw = ImageDraw.Draw(layer)
        w,h = image.size
        x = int(-w*.35 + progress*w*1.7)
        draw.polygon(((x-130,0),(x+70,0),(x+250,h),(x+50,h)), fill=(255,255,255,28))
        draw.polygon(((x-220,0),(x-110,0),(x+60,h),(x-50,h)), fill=(*color,20))
        radius = 7 if self.performance_engine.profile.reduced_blur else 14
        layer = layer.filter(ImageFilter.GaussianBlur(radius))
        out = image.copy(); out.alpha_composite(layer); return out

    def _burst(self, image, progress, color):
        layer = Image.new("RGBA", image.size, (0,0,0,0))
        draw = ImageDraw.Draw(layer)
        w,h = image.size
        burst = MotionEasing.pulse(min(progress*1.7,1))
        for i in range(16):
            a = i/16*math.pi*2
            d = 45 + burst*150
            x = int(w/2 + math.cos(a)*d); y = int(h/2 + math.sin(a)*d)
            r = 2+i%4
            draw.ellipse((x-r,y-r,x+r,y+r), fill=(*color,int(150*burst)))
        out = image.copy(); out.alpha_composite(layer); return out
