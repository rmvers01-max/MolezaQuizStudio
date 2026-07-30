from __future__ import annotations

import textwrap
from pathlib import Path

from PIL import ImageDraw, ImageFont


def load_font(
    size: int,
    bold: bool = False,
):
    names = (
        ["arialbd.ttf", "calibrib.ttf"]
        if bold
        else ["arial.ttf", "calibri.ttf"]
    )

    for name in names:
        path = Path("C:/Windows/Fonts") / name

        if path.exists():
            return ImageFont.truetype(
                str(path),
                max(int(size), 1),
            )

    return ImageFont.load_default()


def fit_font(
    draw: ImageDraw.ImageDraw,
    text: str,
    max_width: int,
    start_size: int,
    min_size: int = 18,
    bold: bool = True,
):
    size = int(start_size)

    while size > min_size:
        font = load_font(size, bold)
        bounds = draw.textbbox(
            (0, 0),
            text,
            font=font,
        )

        if bounds[2] - bounds[0] <= max_width:
            return font

        size -= 2

    return load_font(min_size, bold)


def wrap_lines(
    text: str,
    width: int,
    max_lines: int = 3,
) -> list[str]:
    return textwrap.wrap(
        str(text),
        width=max(int(width), 8),
    )[:max_lines]


def centered_x(
    draw: ImageDraw.ImageDraw,
    text: str,
    font,
    width: int,
) -> int:
    bounds = draw.textbbox(
        (0, 0),
        text,
        font=font,
    )

    return int(
        (
            width
            - (
                bounds[2]
                - bounds[0]
            )
        )
        / 2
    )
