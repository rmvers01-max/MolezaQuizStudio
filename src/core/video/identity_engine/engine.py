from __future__ import annotations
import json
from dataclasses import replace
from pathlib import Path
from .dna import moleza_quiz_dna
from .models import IdentityPlan

class AAAIdentityEngine:
    CATEGORY_ACCENTS={
        "flags_geography":(255,215,65),"animals":(255,224,92),
        "food":(255,205,75),"sports":(255,220,65),
        "characters":(255,202,86),"preference":(255,215,65),
        "general_knowledge":(255,215,65),
    }
    def __init__(self): self.dna=moleza_quiz_dna()

    def create_plan(self,*,category,theme_pack,production_mode):
        original=dict(theme_pack or {})
        corrected=self._correct_theme(original,category)
        findings=[]
        if float(original.get("motion_intensity",.5))>self.dna.maximum_motion:
            findings.append("Movimento reduzido para preservar legibilidade.")
        if float(original.get("background_activity",.55))>.82:
            findings.append("Atividade do fundo reduzida.")
        return IdentityPlan(
            channel_dna=self.dna,category=str(category),
            corrected_theme_pack=corrected,
            rules={
                "family_safe":True,"organized_color":True,
                "maximum_motion":self.dna.maximum_motion,
                "maximum_vignette":self.dna.maximum_vignette,
                "maximum_particles":self.dna.maximum_particles,
                "avoid_dark_frames":True,"avoid_aggressive_shake":True,
                "mascot_presence":"balanced","voice_priority":True,
            },
            score=max(100-len(findings)*5,0),findings=tuple(findings),
            metadata={"identity_engine_version":"1.0","production_mode":production_mode},
        )

    def enforce_experience(self,experience):
        return replace(
            experience,
            camera_multiplier=min(float(experience.camera_multiplier),1.16),
            particle_intensity=min(float(experience.particle_intensity),self.dna.maximum_particles),
            vignette=min(float(experience.vignette),self.dna.maximum_vignette),
            metadata={**dict(experience.metadata),"identity_enforced":True,"channel_code":"moleza_quiz"},
        )

    def evaluate_scene(self,*,theme_pack,experience,mascot_performance):
        findings=[]; score=100
        if float(theme_pack.get("motion_intensity",.5))>self.dna.maximum_motion:
            findings.append("Movimento acima do DNA."); score-=12
        if float(experience.vignette)>self.dna.maximum_vignette:
            findings.append("Vinheta escura demais."); score-=10
        if float(experience.particle_intensity)>self.dna.maximum_particles:
            findings.append("Partículas acima do limite."); score-=8
        if mascot_performance is None:
            findings.append("Mascote sem performance registrada."); score-=4
        return {
            "score":max(score,0),
            "status":"signature_ready" if score>=92 else "approved" if score>=80 else "identity_review",
            "findings":findings,"channel_code":"moleza_quiz","identity_version":"1.0",
        }

    def _correct_theme(self,theme,category):
        theme.setdefault("code","moleza_vibrant")
        theme.setdefault("name","Moleza Vibrante")
        theme.setdefault("background_top",[90,55,180])
        theme.setdefault("background_bottom",[35,28,92])
        theme.setdefault("panel_color",[245,240,255])
        theme.setdefault("primary_color",[101,61,185])
        theme.setdefault("secondary_color",[245,84,132])
        theme["accent_color"]=list(self.CATEGORY_ACCENTS.get(category,self.dna.accent_color))
        theme["text_color"]=list(self.dna.text_color)
        theme["motion_intensity"]=min(float(theme.get("motion_intensity",.5)),self.dna.maximum_motion)
        theme["background_activity"]=min(float(theme.get("background_activity",.55)),.82)
        theme["identity_code"]="moleza_quiz"
        return theme

    def save(self,plan,path):
        path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(json.dumps(plan.to_dict(),ensure_ascii=False,indent=2),encoding="utf-8")
        return path
