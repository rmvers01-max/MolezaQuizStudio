import ast
from pathlib import Path


REQUIRED = {
    "_render_frame",
    "_mascot_actor",
    "_draw_teasers",
    "_energy_line",
    "_transition",
    "_background",
    "_particles",
    "_badge",
    "_center_text",
    "_resolve_opening_colors",
    "_font",
    "_interval",
}


def test_required_methods_belong_to_opening_studio():
    path = (
        Path(__file__).resolve().parents[1]
        / "src"
        / "core"
        / "video"
        / "opening"
        / "opening_studio.py"
    )

    tree = ast.parse(
        path.read_text(
            encoding="utf-8"
        )
    )

    opening_class = next(
        node
        for node in tree.body
        if isinstance(
            node,
            ast.ClassDef,
        )
        and node.name
        == "OpeningStudio"
    )

    methods = {
        node.name
        for node in opening_class.body
        if isinstance(
            node,
            ast.FunctionDef,
        )
    }

    assert not (
        REQUIRED - methods
    )


def test_mascot_actor_is_not_top_level():
    path = (
        Path(__file__).resolve().parents[1]
        / "src"
        / "core"
        / "video"
        / "opening"
        / "opening_studio.py"
    )

    tree = ast.parse(
        path.read_text(
            encoding="utf-8"
        )
    )

    top_level_functions = {
        node.name
        for node in tree.body
        if isinstance(
            node,
            ast.FunctionDef,
        )
    }

    assert (
        "_mascot_actor"
        not in top_level_functions
    )
