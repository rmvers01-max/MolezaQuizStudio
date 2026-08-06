from pathlib import Path
from PIL import Image
from core.video.camera_director import AAACameraCompositor, AAACameraDirector

def test_preference_camera_static():
    plan=AAACameraDirector().create_plan(
        scene_kind="question",category="preference",question_number=3,
        difficulty=40,emotional_tone="fun",pattern_break=False,
        surprise=False,focus_x=.5,focus_y=.5,
    )
    assert plan.primary_move.zoom_to==1.0
    assert plan.primary_move.pan_x==0.0

def test_camera_preserves_size():
    plan=AAACameraDirector().create_plan(
        scene_kind="reveal",category="flags_geography",question_number=5,
        difficulty=80,emotional_tone="victory",pattern_break=False,
        surprise=True,focus_x=.95,focus_y=.05,
    )
    image=Image.new("RGBA",(1280,720),(80,55,150,255))
    result=AAACameraCompositor().apply(image=image,plan=plan,time=2.0,duration=4.0)
    assert result.size==image.size

def test_scene_isolation_present():
    path=Path(__file__).resolve().parents[1]/"src/core/video/templates/preference_renderer.py"
    source=path.read_text(encoding="utf-8")
    assert "def _preparar_cena_timeline_segura" in source
    assert '"disable_frame_reuse"' in source
    assert "clear_frame_cache" in source
