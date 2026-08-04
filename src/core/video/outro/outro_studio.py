from __future__ import annotations
import math, textwrap
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from moviepy import ImageSequenceClip
from ..mascot_actor import MascotActorAnimator, MascotPerformanceDirector

class OutroStudio:
    def __init__(self, width=1280, height=720, fps=18):
        self.width, self.height, self.fps = int(width), int(height), max(int(fps), 12)
        self.actor_director = MascotPerformanceDirector()
        self.actor_animator = MascotActorAnimator()

    def create_clip(self, *, text: str = '', duration: float = 5.2, theme_pack: dict, direction=None):
        if direction is None:
            direction = {
                'duration': duration, 'headline': 'VOCÊ FOI INCRÍVEL!',
                'supporting_text': text, 'primary_cta': 'INSCREVA-SE NO CANAL!',
                'secondary_cta': 'ESCOLHA O PRÓXIMO QUIZ!',
                'curiosity_closer': 'Até a próxima aventura!',
                'quiz_type': 'conhecimento', 'category': 'general_knowledge',
                'show_score_prompt': True, 'show_comment_prompt': True,
                'celebration_style': 'golden_confetti',
            }
        elif hasattr(direction, 'to_dict'):
            direction = direction.to_dict()
        direction = dict(direction)
        duration = max(float(direction.get('duration', duration)), 4.5)
        frames=[]
        for i in range(max(int(round(duration*self.fps)),2)):
            t=i/self.fps; p=min(t/duration,1.0)
            frames.append(np.asarray(self._frame(direction,t,p,theme_pack).convert('RGB')))
        return ImageSequenceClip(frames, fps=self.fps).with_duration(duration)

    def _frame(self, d, time, progress, theme):
        top=tuple(theme.get('background_top',(90,55,180))); bottom=tuple(theme.get('background_bottom',(35,28,92)))
        accent=tuple(theme.get('accent_color',(255,215,65))); primary=tuple(theme.get('primary_color',(115,70,205)))
        img=Image.new('RGBA',(self.width,self.height),(*bottom,255)); draw=ImageDraw.Draw(img)
        for y in range(self.height):
            q=y/max(self.height-1,1); c=tuple(int(top[k]+(bottom[k]-top[k])*q) for k in range(3)); draw.line((0,y,self.width,y),fill=(*c,255))
        glow=Image.new('RGBA',img.size,(0,0,0,0)); gd=ImageDraw.Draw(glow); dx=int(70*math.sin(time*.65))
        gd.ellipse((-160+dx,-160,600+dx,600),fill=(*primary,85)); gd.ellipse((680-dx,-160,1460-dx,600),fill=(*accent,75))
        glow=glow.filter(ImageFilter.GaussianBlur(110)); img.alpha_composite(glow); draw=ImageDraw.Draw(img)
        self._confetti(draw,time,d.get('celebration_style','golden_confetti'),accent)
        enter=self._interval(time,.05,.8)
        self._center(draw,'MOLEZA QUIZ',35,max(int(34*self._back(enter)),1),(255,255,255),primary,4)
        self._center(draw,str(d.get('headline','VOCÊ FOI INCRÍVEL!')),92,46,(255,255,255),(45,22,85),5)
        lines=textwrap.wrap(str(d.get('supporting_text','')),width=46)[:2]
        for n,line in enumerate(lines): self._center(draw,line,158+n*36,27,accent,(45,22,85),3)
        # Próximo vídeo
        box=(110,265,690,570); pulse=.5+.5*math.sin(time*2.2)
        draw.rounded_rectangle(box,radius=32,fill=(255,255,255,35),outline=(*accent,int(180+70*pulse)),width=6)
        self._center_in_box(draw,'PRÓXIMO QUIZ',box,30,(255,255,255),primary,3,y_offset=-85)
        self._center_in_box(draw,str(d.get('secondary_cta','ESCOLHA SUA PRÓXIMA AVENTURA!')),box,24,accent,(45,22,85),3,y_offset=70)
        # Inscrição
        sub=(780,300,1080,555); draw.rounded_rectangle(sub,radius=42,fill=(255,255,255,38),outline=(255,255,255,210),width=5)
        self._center_in_box(draw,'INSCREVA-SE',sub,29,(255,255,255),primary,3,y_offset=-70)
        self._center_in_box(draw,'🔔  LIKE  👍',sub,25,accent,(45,22,85),2,y_offset=70)
        # CTA inferior
        cta=(165,606,1115,676); draw.rounded_rectangle(cta,radius=30,fill=(*primary,225),outline=(*accent,255),width=4)
        self._center_in_box(draw,str(d.get('primary_cta','COMENTE SEU RESULTADO!')),cta,25,(255,255,255),(45,22,85),3)
        # Mascote
        perf=self.actor_director.create_performance(scene_kind='reveal',question_number=999,duration=float(d.get('duration',5.2)),difficulty=45,surprise=True,correct_reveal=True,focus_side='left',production_mode='compact_high_energy')
        mascot,x,y=self.actor_animator.render(performance=perf,time=time,canvas_size=(self.width,self.height),base_size=(220,220),anchor=(1030,420))
        if mascot is not None: img.alpha_composite(mascot,(min(x,self.width-mascot.width),min(y,self.height-mascot.height)))
        # Curiosidade/assinatura curta
        if time > float(d.get('duration',5.2))*.60:
            alpha=self._interval(time,float(d.get('duration',5.2))*.60,float(d.get('duration',5.2))*.88)
            self._center(draw,str(d.get('curiosity_closer','ATÉ A PRÓXIMA AVENTURA!')),225,22,(255,255,255),(45,22,85),3,alpha)
        return img

    def _confetti(self,draw,time,style,accent):
        for i in range(34):
            x=(i*97+int(time*(18+i%7)))%self.width; y=(i*61+int(time*(35+i%5)))%self.height
            color=(255,220,70,190) if i%2==0 else (*accent,180)
            if style=='choice_confetti' and i%3==0: color=(245,84,132,190)
            draw.rectangle((x,y,x+3+i%4,y+7+i%5),fill=color)

    def _font(self,size,bold=True):
        paths=('C:/Windows/Fonts/arialbd.ttf','C:/Windows/Fonts/Arial.ttf') if bold else ('C:/Windows/Fonts/Arial.ttf',)
        for p in paths:
            try:return ImageFont.truetype(p,max(int(size),1))
            except OSError:pass
        return ImageFont.load_default()

    def _center(self,draw,text,y,size,fill,stroke,sw,opacity=1.0):
        font=self._font(size); b=draw.textbbox((0,0),text,font=font,stroke_width=sw); x=(self.width-(b[2]-b[0]))//2
        draw.text((x,y),text,font=font,fill=(*fill[:3],int(255*opacity)),stroke_width=sw,stroke_fill=(*stroke[:3],int(255*opacity)))

    def _center_in_box(self,draw,text,box,size,fill,stroke,sw,y_offset=0):
        lines=textwrap.wrap(text,width=29)[:2]; total=len(lines)*34
        for i,line in enumerate(lines):
            font=self._font(size); b=draw.textbbox((0,0),line,font=font,stroke_width=sw); x=(box[0]+box[2]-(b[2]-b[0]))//2; y=(box[1]+box[3]-total)//2+i*34+y_offset
            draw.text((x,y),line,font=font,fill=fill,stroke_width=sw,stroke_fill=stroke)

    def _interval(self,t,a,b): return max(min((t-a)/max(b-a,.001),1.0),0.0)
    def _back(self,p):
        c1=1.70158; c3=c1+1; q=p-1; return 1+c3*q*q*q+c1*q*q
