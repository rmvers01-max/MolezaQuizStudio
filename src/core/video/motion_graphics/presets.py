from __future__ import annotations
from .models import MotionPreset

class MotionPresetLibrary:
    def title(self, category):
        return MotionPreset(f"title_{category}_01","title","slide_down_overshoot","soft_fade","ease_out_back",.72,.88,1,.42,.14,0,"sparkles")
    def card(self, category):
        return MotionPreset(f"card_{category}_01","card","scale_pop","soft_slide","spring",.58,.80,1,.36,.10,0,None)
    def counter(self, category):
        return MotionPreset(f"counter_{category}_01","counter","bounce_pulse","flash_out","ease_out_bounce",.42,.72,1,.52,.08,.03,"light_dots")
    def reveal(self, category):
        return MotionPreset(f"reveal_{category}_01","answer","hero_pulse","hold","ease_out_back",.68,.92,1,.72,.06,.05,"golden_sparks")
    def badge(self, category):
        return MotionPreset(f"badge_{category}_01","badge","fade_scale","fade_scale","ease_out_cubic",.45,.84,1,.30,.05,0,None)
    def progress(self, category):
        return MotionPreset(f"progress_{category}_01","progress","fill_shine","hold","ease_in_out_cubic",.55,1,1,.32,0,0,None)
