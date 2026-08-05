from PIL import Image
from core.video.motion_graphics import (
    AAAMotionGraphicsDirector,
    MotionEasing,
    MotionGraphicsCompositor,
)

def test_easing_curves():
    assert 0 <= MotionEasing.ease_out_cubic(.5) <= 1
    assert 0 <= MotionEasing.ease_in_out_cubic(.5) <= 1
    assert 0 <= MotionEasing.ease_out_bounce(.5) <= 1.1

def test_preference_transition():
    plan = AAAMotionGraphicsDirector().create_plan(
        category="preference", scene_kind="question",
        question_number=3, fps=24,
    )
    assert plan.transition_style == "split_flash"
    assert plan.card_preset.entry_style == "scale_pop"

def test_reveal_particles():
    plan = AAAMotionGraphicsDirector().create_plan(
        category="flags_geography", scene_kind="reveal",
        question_number=8, fps=24,
    )
    assert plan.reveal_preset.particle_burst == "golden_sparks"

def test_compositor_preserves_size():
    plan = AAAMotionGraphicsDirector().create_plan(
        category="animals", scene_kind="countdown",
        question_number=4, fps=24,
    )
    source = Image.new("RGBA", (1280,720), (80,55,150,255))
    result = MotionGraphicsCompositor().animate_frame(
        image=source, plan=plan, time=1.0, duration=4.0,
        accent_color=(255,215,65),
    )
    assert result.size == source.size
    assert result.tobytes() != source.tobytes()
