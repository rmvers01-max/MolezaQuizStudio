from __future__ import annotations
import math
from PIL import Image, ImageEnhance
from ..animations import CharacterAnimationEngine, SmartEasing

class MascotActorAnimator:
    def __init__(self): self.engine=CharacterAnimationEngine()

    def render(self, *, performance, time: float, canvas_size,
               base_size=(210,210), anchor=None):
        beat=performance.beat_at(float(time))
        if beat is None: return None,0,0
        local=self._p(time,beat.start,beat.end)
        asset,dx,dy=self.engine.renderizar(
            pose=beat.pose, progresso=max(local,.01), tamanho_base=base_size,
            comportamento=beat.pose, intensidade=beat.intensity)
        if asset is None: return None,0,0
        asset=asset.convert('RGBA')
        scale=(1+.022*math.sin(time*3.1+performance.question_number))
        if beat.action in {'celebrate','approve'}:
            scale*=1+.09*math.sin(local*math.pi)
        w=max(int(asset.width*scale),1); h=max(int(asset.height*scale),1)
        asset=asset.resize((w,h),Image.Resampling.LANCZOS)
        if beat.action in {'suspense','anticipate'}:
            asset=ImageEnhance.Brightness(asset).enhance(.93+.07*math.sin(local*math.pi))
        cw,ch=canvas_size
        if anchor is None:
            x=18 if performance.preferred_side=='left' else cw-w-18
            y=ch-h-6
        else: x,y=anchor
        if beat.enter_style=='slide_bounce':
            eased=SmartEasing.ease_out_back(local,overshoot=1.08)
            x += int((-1 if performance.preferred_side=='left' else 1)*(1-eased)*150)
        if beat.exit_style in {'soft_exit','bounce_out'} and local>.78:
            ep=(local-.78)/.22
            x += int((-1 if performance.preferred_side=='left' else 1)*ep*70)
        x += 8 if beat.look_target in {'question','choices','answer'} and performance.preferred_side=='left' else -8 if beat.look_target in {'question','choices','answer'} else 0
        y += int(4*math.sin(time*2.9))+dy
        return asset,int(x+dx),int(y)

    def _p(self,t,a,b):
        return 1.0 if b<=a else max(0.,min((float(t)-a)/(b-a),1.))
