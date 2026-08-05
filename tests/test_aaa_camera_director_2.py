from PIL import Image

from core.video.camera_director import (
    AAACameraCompositor,
    AAACameraDirector,
)


def test_reveal_surprise_uses_hero_camera():
    plan = AAACameraDirector().create_plan(
        scene_kind="reveal",
        category="flags_geography",
        question_number=10,
        difficulty=80,
        emotional_tone="victory",
        pattern_break=False,
        surprise=True,
        focus_x=0.50,
        focus_y=0.45,
    )

    assert (
        plan.primary_move.code
        == "hero_reveal_01"
    )


def test_countdown_uses_suspense_camera():
    plan = AAACameraDirector().create_plan(
        scene_kind="countdown",
        category="general_knowledge",
        question_number=4,
        difficulty=55,
        emotional_tone="challenge",
        pattern_break=False,
        surprise=False,
        focus_x=0.50,
        focus_y=0.50,
    )

    assert (
        plan.primary_move.code
        == "suspense_focus_01"
    )


def test_preference_uses_balanced_camera():
    plan = AAACameraDirector().create_plan(
        scene_kind="question",
        category="preference",
        question_number=3,
        difficulty=40,
        emotional_tone="fun",
        pattern_break=False,
        surprise=False,
        focus_x=0.50,
        focus_y=0.50,
    )

    assert (
        plan.primary_move.code
        == "choice_balance_01"
    )


def test_camera_compositor_preserves_frame_size():
    plan = AAACameraDirector().create_plan(
        scene_kind="question",
        category="animals",
        question_number=2,
        difficulty=45,
        emotional_tone="curiosity",
        pattern_break=False,
        surprise=False,
        focus_x=0.55,
        focus_y=0.48,
    )

    image = Image.new(
        "RGBA",
        (1280, 720),
        (80, 55, 150, 255),
    )

    result = AAACameraCompositor().apply(
        image=image,
        plan=plan,
        time=1.2,
        duration=4.0,
    )

    assert result.size == image.size
