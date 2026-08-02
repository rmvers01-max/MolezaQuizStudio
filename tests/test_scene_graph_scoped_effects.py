from PIL import Image

from core.video.scene_graph import (
    Rect,
    ScopedMaterialRenderer,
)


def test_sheen_is_clipped_to_card_bounds():
    renderer = ScopedMaterialRenderer()

    original = Image.new(
        "RGBA",
        (320, 180),
        (10, 20, 30, 255),
    )

    bounds = Rect(
        80,
        50,
        160,
        80,
    )

    result = renderer.apply_sheen(
        canvas=original,
        bounds=bounds,
        progress=0.5,
        intensity=1.0,
        corner_radius=20,
    )

    assert result.getpixel(
        (20, 20)
    ) == original.getpixel(
        (20, 20)
    )

    assert result.getpixel(
        (160, 90)
    ) != original.getpixel(
        (160, 90)
    )


def test_inner_glow_does_not_modify_outside_target():
    renderer = ScopedMaterialRenderer()

    original = Image.new(
        "RGBA",
        (320, 180),
        (25, 25, 25, 255),
    )

    bounds = Rect(
        70,
        40,
        180,
        100,
    )

    result = renderer.apply_inner_glow(
        canvas=original,
        bounds=bounds,
        progress=0.5,
        color=(255, 220, 80),
        intensity=1.0,
        corner_radius=24,
    )

    assert result.getpixel(
        (10, 10)
    ) == original.getpixel(
        (10, 10)
    )
