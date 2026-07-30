from __future__ import annotations

from PIL import Image, ImageDraw

from .base import (
    ComponentBox,
    ComponentContext,
    UniversalComponent,
)
from .utils import (
    centered_x,
    fit_font,
)


class ChoiceComponent(UniversalComponent):
    def __init__(
        self,
        text: str,
        index: int,
        highlighted: bool = False,
    ):
        self.text = str(text)
        self.index = int(index)
        self.highlighted = bool(
            highlighted
        )

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

        secondary = tuple(
            context.theme_pack.get(
                "secondary_color",
                (50, 180, 155),
            )
        )

        accent = tuple(
            context.theme_pack.get(
                "accent_color",
                (255, 215, 65),
            )
        )

        fill = (
            accent
            if self.highlighted
            else (
                primary
                if self.index % 2
                else secondary
            )
        )

        draw.rounded_rectangle(
            box.as_tuple(),
            radius=22,
            fill=(*fill, 245),
            outline=(255, 255, 255, 255),
            width=4,
        )

        label = chr(
            64 + min(
                max(self.index, 1),
                26
            )
        )

        circle_x = box.x + 30
        circle_y = box.y + box.height // 2

        draw.ellipse(
            (
                circle_x - 19,
                circle_y - 19,
                circle_x + 19,
                circle_y + 19,
            ),
            fill=(255, 255, 255, 240),
        )

        letter_font = fit_font(
            draw=draw,
            text=label,
            max_width=28,
            start_size=25,
            min_size=18,
            bold=True,
        )

        draw.text(
            (
                circle_x - 8,
                circle_y - 16,
            ),
            label,
            font=letter_font,
            fill=(45, 45, 70),
        )

        font = fit_font(
            draw=draw,
            text=self.text,
            max_width=box.width - 95,
            start_size=28,
            min_size=18,
            bold=True,
        )

        text_area_width = box.width - 80
        x = (
            box.x
            + 68
            + centered_x(
                draw,
                self.text,
                font,
                text_area_width,
            )
        )

        bounds = draw.textbbox(
            (0, 0),
            self.text,
            font=font,
        )

        y = box.y + (
            box.height
            - (
                bounds[3]
                - bounds[1]
            )
        ) // 2 - 2

        draw.text(
            (x, y),
            self.text,
            font=font,
            fill=(255, 255, 255),
            stroke_width=2,
            stroke_fill=(40, 35, 70),
        )
