from __future__ import annotations
import math, textwrap
import numpy as np
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
from moviepy import ImageSequenceClip

class CuriosityExperienceStudio:
    def __init__(self, width=1280, height=720, fps=18):
        self.width=int(width); self.height=int(height); self.fps=max(int(fps),12)

    def create_clip(self, *, plan, theme_pack: dict, question_number: int=1):
        if not plan.enabled or not plan.items: return None
        total=max(int(round(plan.duration*self.fps)),2)
        frames=[]
        for i in range(total):
            t=i/self.fps; p=min(t/max(plan.duration,.001),1.0)
            frames.append(np.asarray(self._frame(plan, theme_pack, question_number, t, p).convert('RGB')))
        return ImageSequenceClip(frames, fps=self.fps).with_duration(plan.duration)

    def _frame(self, plan, theme, number, t, p):
        top=tuple(theme.get('background_top',[48,55,135])); bottom=tuple(theme.get('background_bottom',[20,30,85])); accent=tuple(theme.get('accent_color',[255,215,65]))
        im=Image.new('RGBA',(self.width,self.height),(0,0,0,255)); d=ImageDraw.Draw(im)
        for y in range(self.height):
            q=y/max(self.height-1,1); c=tuple(int(top[k]+(bottom[k]-top[k])*q) for k in range(3)); d.line((0,y,self.width,y),fill=c)
        self._lights(im,t,accent); self._particles(im,t,accent)
        item_index=min(int(p*len(plan.items)),len(plan.items)-1)
        item=plan.items[item_index]
        local=(p*len(plan.items))-item_index
        self._header(im,item.title,number,local,accent)
        self._card(im,item,local,accent)
        self._mascot_hint(im,local,accent)
        if p>0.82: self._next(im,(p-.82)/.18,plan.transition_text,accent)
        return im

    def _header(self, im, title, number, p, accent):
        d=ImageDraw.Draw(im); font=self._font(42,True); small=self._font(22,True)
        d.rounded_rectangle((70,35,1210,105),radius=28,fill=(35,20,85,230),outline=accent+(255,),width=4)
        d.text((95,56),f'PERGUNTA {number}',font=small,fill=(255,255,255,255))
        self._center(d,title,55,font,accent+(255,),4,(55,25,95,255))

    def _card(self, im, item, p, accent):
        layer=Image.new('RGBA',im.size,(0,0,0,0)); d=ImageDraw.Draw(layer)
        scale=.92+.08*min(max(p,0),1); w=int(1050*scale); h=int(470*scale); x=(self.width-w)//2; y=145+(470-h)//2
        d.rounded_rectangle((x+8,y+12,x+w+8,y+h+12),radius=38,fill=(5,10,35,90))
        d.rounded_rectangle((x,y,x+w,y+h),radius=38,fill=(248,248,255,242),outline=accent+(255,),width=6)
        image_box=(x+40,y+50,x+390,y+h-50)
        self._image_or_icon(layer,item,image_box,accent)
        tx=x+425; maxw=w-470
        subject_font=self._font(34,True); body_font=self._font(30,True)
        if item.subject:
            d.text((tx,y+62),item.subject.upper(),font=subject_font,fill=(105,55,175,255))
        lines=textwrap.wrap(item.text,width=31)[:7]
        yy=y+125
        for line in lines:
            d.text((tx,yy),line,font=body_font,fill=(42,35,70,255)); yy+=44
        im.alpha_composite(layer)

    def _image_or_icon(self, layer, item, box, accent):
        d=ImageDraw.Draw(layer); x1,y1,x2,y2=box
        d.rounded_rectangle(box,radius=30,fill=(45,35,105,245),outline=accent+(240,),width=4)
        if item.image_path and Path(item.image_path).exists():
            try:
                img=Image.open(item.image_path).convert('RGBA'); img=ImageOps.fit(img,(x2-x1,y2-y1),method=Image.Resampling.LANCZOS)
                mask=Image.new('L',img.size,0); md=ImageDraw.Draw(mask); md.rounded_rectangle((0,0,img.width,img.height),radius=28,fill=255)
                layer.paste(img,(x1,y1),mask)
                return
            except Exception: pass
        font=self._font(96,False); bbox=d.textbbox((0,0),item.icon,font=font); d.text(((x1+x2-(bbox[2]-bbox[0]))//2,(y1+y2-(bbox[3]-bbox[1]))//2-10),item.icon,font=font,fill=(255,255,255,255))

    def _mascot_hint(self, im, p, accent):
        d=ImageDraw.Draw(im); x=35; y=585; r=55+int(4*math.sin(p*math.pi))
        d.ellipse((x,y,x+r*2,y+r*2),fill=(255,255,255,235),outline=accent+(255,),width=5)
        font=self._font(52,False); d.text((x+26,y+22),'💡',font=font,fill=(255,210,60,255))

    def _next(self, im, p, text, accent):
        layer=Image.new('RGBA',im.size,(0,0,0,0)); d=ImageDraw.Draw(layer); alpha=int(235*min(max(p,0),1))
        d.rounded_rectangle((250,600,1030,685),radius=28,fill=(52,28,110,alpha),outline=accent+(alpha,),width=4)
        self._center(d,text,623,self._font(29,True),(255,255,255,alpha),3,(40,15,80,alpha)); im.alpha_composite(layer)

    def _lights(self, im,t,accent):
        layer=Image.new('RGBA',im.size,(0,0,0,0)); d=ImageDraw.Draw(layer); dx=int(70*math.sin(t*.9))
        d.ellipse((-120+dx,-180,540+dx,520),fill=accent+(80,)); d.ellipse((760-dx,-160,1430-dx,510),fill=(80,150,255,75)); layer=layer.filter(ImageFilter.GaussianBlur(90)); im.alpha_composite(layer)

    def _particles(self,im,t,accent):
        d=ImageDraw.Draw(im)
        for i in range(22):
            x=(i*151+int(t*(11+i%4)))%self.width; y=(i*97+int(12*math.sin(t+i)))%self.height; r=2+i%3
            d.ellipse((x-r,y-r,x+r,y+r),fill=accent+(80+i%70,))

    def _center(self,d,text,y,font,fill,sw,stroke):
        b=d.textbbox((0,0),text,font=font,stroke_width=sw); x=(self.width-(b[2]-b[0]))//2; d.text((x,y),text,font=font,fill=fill,stroke_width=sw,stroke_fill=stroke)

    def _font(self,size,bold=False):
        paths=['C:/Windows/Fonts/arialbd.ttf','C:/Windows/Fonts/Arial.ttf'] if bold else ['C:/Windows/Fonts/Arial.ttf','C:/Windows/Fonts/arialbd.ttf']
        for p in paths:
            try:return ImageFont.truetype(p,max(int(size),1))
            except OSError:pass
        return ImageFont.load_default()
