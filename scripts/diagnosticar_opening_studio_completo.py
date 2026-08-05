from __future__ import annotations

import sys

import core.video.opening.opening_studio as opening_module
from core.video.opening.opening_studio import OpeningStudio


REQUIRED = (
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
    "_colors",
    "_font",
    "_interval",
)


print("PYTHON:")
print(sys.executable)

print("\nARQUIVO IMPORTADO:")
print(opening_module.__file__)

print("\nMÉTODOS DA ABERTURA:")

for method_name in REQUIRED:
    print(
        f"{method_name}:",
        hasattr(
            OpeningStudio,
            method_name,
        ),
    )

missing = [
    method_name
    for method_name in REQUIRED
    if not hasattr(
        OpeningStudio,
        method_name,
    )
]

if missing:
    raise RuntimeError(
        "Métodos ausentes: "
        + ", ".join(missing)
    )

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

background = studio._background(
    colors=palette,
    time=0.5,
    camera_style="competition_push",
)

assert background.size == (
    1280,
    720,
)

print("\nOPENING STUDIO COMPLETO OK")
