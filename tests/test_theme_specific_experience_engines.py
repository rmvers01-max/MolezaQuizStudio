from PIL import Image

from core.video.theme_experience import (
    ThemeSpecificCompositor,
    ThemeSpecificExperienceDirector,
)


def test_preference_uses_dual_world():
    profile = (
        ThemeSpecificExperienceDirector()
        .choose(
            category="preference",
            question_number=3,
            scene_kind="question",
        )
    )

    assert profile.background_mode == "dual_world"
    assert profile.transition_style == "split_flash"


def test_flags_use_map_and_compass():
    profile = (
        ThemeSpecificExperienceDirector()
        .choose(
            category="flags_geography",
            question_number=2,
            scene_kind="countdown",
        )
    )

    assert profile.motif_style == "map_compass"
    assert profile.countdown_style == "radial_compass"


def test_compositor_changes_frame_without_resizing():
    profile = (
        ThemeSpecificExperienceDirector()
        .choose(
            category="animals",
            question_number=4,
            scene_kind="question",
        )
    )

    source = Image.new(
        "RGBA",
        (1280, 720),
        (80, 55, 150, 255),
    )

    result = ThemeSpecificCompositor().apply(
        image=source,
        profile=profile,
        time=0.8,
        content_box=(50, 50, 1230, 670),
    )

    assert result.size == source.size
    assert result.tobytes() != source.tobytes()


def test_all_main_categories_have_unique_engines():
    director = ThemeSpecificExperienceDirector()

    categories = (
        "preference",
        "flags_geography",
        "animals",
        "food",
        "sports",
        "characters",
        "general_knowledge",
    )

    codes = {
        director.choose(
            category=category
        ).engine_code
        for category in categories
    }

    assert len(codes) == len(categories)
