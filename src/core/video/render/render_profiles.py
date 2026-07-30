from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RenderProfile:
    nome: str
    fps_timeline: int
    escala_interna: float
    anti_aliasing: bool
    cinematic_fx: bool
    visual_fx: bool
    motion_blur: bool
    card_material: bool
    character_animation: bool
    camera_engine: bool
    nitidez_final: float
    contraste_final: float
    saturacao_final: float


class RenderProfileRegistry:
    PERFIS = {
        "preview": RenderProfile(
            nome="Preview Rápido",
            fps_timeline=12,
            escala_interna=0.75,
            anti_aliasing=False,
            cinematic_fx=False,
            visual_fx=True,
            motion_blur=False,
            card_material=True,
            character_animation=True,
            camera_engine=True,
            nitidez_final=1.00,
            contraste_final=1.00,
            saturacao_final=1.00,
        ),
        "balanced": RenderProfile(
            nome="Qualidade Equilibrada",
            fps_timeline=18,
            escala_interna=1.00,
            anti_aliasing=True,
            cinematic_fx=True,
            visual_fx=True,
            motion_blur=True,
            card_material=True,
            character_animation=True,
            camera_engine=True,
            nitidez_final=1.04,
            contraste_final=1.03,
            saturacao_final=1.04,
        ),
        "aaa": RenderProfile(
            nome="AAA Final",
            fps_timeline=24,
            escala_interna=1.10,
            anti_aliasing=True,
            cinematic_fx=True,
            visual_fx=True,
            motion_blur=True,
            card_material=True,
            character_animation=True,
            camera_engine=True,
            nitidez_final=1.08,
            contraste_final=1.05,
            saturacao_final=1.06,
        ),
    }

    def obter(
        self,
        nome: str = "balanced",
    ) -> RenderProfile:
        return self.PERFIS.get(
            str(nome).strip().lower(),
            self.PERFIS["balanced"],
        )
