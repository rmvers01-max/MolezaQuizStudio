from __future__ import annotations

from pathlib import Path

from PIL import (
    Image,
    ImageDraw,
    ImageFilter,
    ImageOps,
)

from .base import (
    ComponentBox,
    ComponentContext,
    UniversalComponent,
)


class MainImageComponent(UniversalComponent):
    def __init__(
        self,
        path,
    ):
        self.path = Path(path) if path else None

    def render(
        self,
        image: Image.Image,
        box: ComponentBox,
        context: ComponentContext,
    ) -> None:
        draw = ImageDraw.Draw(image)

        primary = tuple(
            context.theme_pack.get(
                "primary_color",
                (70, 120, 220),
            )
        )

        shadow = Image.new(
            "RGBA",
            image.size,
            (0, 0, 0, 0),
        )

        shadow_draw = ImageDraw.Draw(shadow)

        shadow_draw.rounded_rectangle(
            (
                box.x + 10,
                box.y + 14,
                box.right + 10,
                box.bottom + 14,
            ),
            radius=30,
            fill=(0, 0, 0, 75),
        )

        shadow = shadow.filter(
            ImageFilter.GaussianBlur(
                radius=12
            )
        )

        image.alpha_composite(shadow)

        draw.rounded_rectangle(
            box.as_tuple(),
            radius=30,
            fill=(255, 255, 255, 248),
            outline=(*primary, 255),
            width=5,
        )

        if (
            self.path is None
            or not self.path.exists()
        ):
            return

        try:
            source = Image.open(
                self.path
            ).convert("RGBA")
        except OSError:
            return

        fitted = ImageOps.contain(
            source,
            (
                max(box.width - 36, 20),
                max(box.height - 36, 20),
            ),
            method=Image.Resampling.LANCZOS,
        )

        x = box.x + (
            box.width
            - fitted.width
        ) // 2

        y = box.y + (
            box.height
            - fitted.height
        ) // 2

        image.alpha_composite(
            fitted,
            (x, y),
        )
