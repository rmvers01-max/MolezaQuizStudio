from __future__ import annotations

import sys

import core.video.opening.opening_studio as opening_module
from core.video.opening.opening_studio import OpeningStudio


print("PYTHON:")
print(sys.executable)

print("\nARQUIVO IMPORTADO:")
print(opening_module.__file__)

print("\nMÉTODOS:")
print(
    "_resolve_opening_colors:",
    hasattr(
        OpeningStudio,
        "_resolve_opening_colors",
    ),
)
print(
    "_colors:",
    hasattr(
        OpeningStudio,
        "_colors",
    ),
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

assert "top" in palette
assert "highlight" in palette

print("\nOPENING COLORS OK")
