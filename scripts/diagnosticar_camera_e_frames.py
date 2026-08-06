from core.video.camera_director import AAACameraDirector
from core.video.templates.preference_renderer import ProfessionalPreferenceRenderer
plan=AAACameraDirector().create_plan(
    scene_kind="question",category="preference",question_number=3,
    difficulty=40,emotional_tone="fun",pattern_break=False,
    surprise=False,focus_x=.5,focus_y=.5,
)
renderer=ProfessionalPreferenceRenderer()
a=renderer._preparar_cena_timeline_segura({"camera_style":"hero_push"},numero=2,tipo="pergunta")
b=renderer._preparar_cena_timeline_segura({"camera_style":"hero_push"},numero=3,tipo="pergunta")
print(plan.primary_move.code,plan.primary_move.zoom_to)
print(a["scene_id"],b["scene_id"])
assert plan.primary_move.zoom_to==1.0
assert a["scene_id"]!=b["scene_id"]
assert b["camera_style"]=="static"
assert b["disable_frame_reuse"] is True
print("CAMERA E FRAMES OK")
