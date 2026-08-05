from core.video.opening.opening_studio import OpeningStudio


def test_opening_has_both_color_method_names():
    assert hasattr(
        OpeningStudio,
        "_resolve_opening_colors",
    )
    assert hasattr(
        OpeningStudio,
        "_colors",
    )


def test_color_resolver_returns_complete_palette():
    studio = OpeningStudio(
        largura=1280,
        altura=720,
        fps=24,
    )

    palette = studio._resolve_opening_colors(
        None,
        {},
        "preference",
    )

    assert "top" in palette
    assert "highlight" in palette
