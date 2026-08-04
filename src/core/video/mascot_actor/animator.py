from __future__ import annotations
import math
from PIL import Image, ImageEnhance
from ..animations import CharacterAnimationEngine, SmartEasing


class MascotActorAnimator:
    def __init__(self):
        self.engine=CharacterAnimationEngine()

    def render(self, *, performance, time: float, canvas_size, base_size=(210,210), anchor=None):
        beat=performance.beat_at(float(time))
        if beat is None:
            return None,0,0
        local=self._progress(time,beat.start,beat.end)
        asset,dx,dy=self.engine.renderizar(
            pose=beat.pose,
            progresso=max(local,.01),
            tamanho_base=base_size,
            comportamento=beat.pose,
            intensidade=beat.intensity,
        )
        if asset is None:
            return None,0,0
        asset=asset.convert('RGBA')

        breathe=1+.020*math.sin(time*3.0+performance.question_number)
        action_scale=1.0
        if beat.enter_style=='soft_pop':
            action_scale*=.82+.18*SmartEasing.ease_out_back(local,overshoot=1.05)
        elif beat.enter_style=='impact_pop':
            action_scale*=.72+.28*SmartEasing.ease_out_back(local,overshoot=1.12)
        if beat.action in {'celebrate','approve'}:
            action_scale*=1+.09*math.sin(local*math.pi)
        elif beat.action in {'guide','encourage'}:
            action_scale*=1+.025*math.sin(local*math.pi*2)

        scale=max(breathe*action_scale,.01)
        w=max(int(asset.width*scale),1); h=max(int(asset.height*scale),1)
        asset=asset.resize((w,h),Image.Resampling.LANCZOS)
        if beat.action in {'suspense','anticipate'}:
            asset=ImageEnhance.Brightness(asset).enhance(.93+.07*math.sin(local*math.pi))

        cw,ch=canvas_size
        if anchor is None:
            x=18 if performance.preferred_side=='left' else cw-w-18
            y=ch-h-6
        else:
            x,y=anchor
            if performance.preferred_side=='right':
                x=x+max(base_size[0]-w,0)

        if beat.enter_style=='slide_bounce':
            eased=SmartEasing.ease_out_back(local,overshoot=1.08)
            x+=int((-1 if performance.preferred_side=='left' else 1)*(1-eased)*150)
        if beat.exit_style in {'soft_exit','bounce_out'} and local>.78:
            ep=(local-.78)/.22
            x+=int((-1 if performance.preferred_side=='left' else 1)*ep*70)

        if beat.look_target in {'question','choices','answer','timer'}:
            x+=8 if performance.preferred_side=='left' else -8
        y+=int(4*math.sin(time*2.9))+dy

        x=max(-w//3,min(int(x+dx),cw-w//2))
        y=max(-h//3,min(int(y),ch-h//2))
        return asset,x,y

    def _progress(self,t,a,b):
        return 1.0 if b<=a else max(0.,min((float(t)-a)/(b-a),1.))
