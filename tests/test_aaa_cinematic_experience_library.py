from PIL import Image

from core.video.cinematic_experience import (
    CinematicExperienceCompositor,
    CinematicExperienceDirector,
)


class Focus:
    x = 640
    y = 360


def test_reveal_surprise_uses_victory():
    experience = (
        CinematicExperienceDirector()
        .choose(
            scene_kind="reveal",
            emotional_tone="victory",
            difficulty=80,
            surprise=True,
            pattern_break=False,
            question_number=10,
            total_questions=10,
        )
    )

    assert experience.code == "victory_01"


def test_countdown_uses_suspense():
    experience = (
        CinematicExperienceDirector()
        .choose(
            scene_kind="countdown",
            emotional_tone="challenge",
            difficulty=60,
            surprise=False,
            pattern_break=False,
            question_number=4,
            total_questions=10,
        )
    )

    assert experience.code == "suspense_01"


def test_compositor_keeps_canvas_size():
    director = CinematicExperienceDirector()
    experience = director.choose(
        scene_kind="question",
        emotional_tone="curiosity",
        difficulty=40,
        surprise=False,
        pattern_break=False,
        question_number=1,
        total_questions=10,
    )

    image = Image.new(
        "RGBA",
        (1280, 720),
        (40, 50, 90, 255),
    )

    result = (
        CinematicExperienceCompositor()
        .apply_pre_camera(
            image=image,
            experience=experience,
            time=0.5,
            progress=0.3,
            focus=Focus(),
            accent_color=(
                255,
                220,
                70,
            ),
        )
    )

    assert result.size == (1280, 720)
