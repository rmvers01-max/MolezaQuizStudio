from pathlib import Path


def test_opening_studio_has_unique_color_resolver():
    path = (
        Path(__file__).resolve().parents[1]
        / "src"
        / "core"
        / "video"
        / "opening"
        / "opening_studio.py"
    )

    source = path.read_text(encoding="utf-8")

    assert "self._resolve_opening_colors(" in source
    assert "def _resolve_opening_colors(" in source
    assert "self._colors(" not in source
