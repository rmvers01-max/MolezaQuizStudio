from __future__ import annotations

import math

from PIL import Image, ImageDraw

from .base import (
    ComponentBox,
    ComponentContext,
    UniversalComponent,
)
from .utils import (
    centered_x,
    load_font,
)


class TimerComponent(UniversalComponent):
    def __init__(
        self,
        value: int,
        maximum: int,
    ):
        self.value = max(
            int(value),
            0
        )
        self.maximum = max(
            int(maximum),
            1
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

        accent = tuple(
            context.theme_pack.get(
                "accent_color",
                (255, 215, 65),
            )
        )

        center = (
            box.x + box.width // 2,
            box.y + box.height // 2,
        )

        radius = max(
            min(
                box.width,
                box.height
            ) // 2 - 8,
            18,
        )

        draw.ellipse(
            (
                center[0] - radius,
                center[1] - radius,
                center[0] + radius,
                center[1] + radius,
            ),
            fill=(255, 255, 255, 230),
            outline=(*primary, 255),
            width=5,
        )

        proportion = min(
            max(
                self.value
                / self.maximum,
                0.0
            ),
            1.0
        )

        draw.arc(
            (
                center[0] - radius + 7,
                center[1] - radius + 7,
                center[0] + radius - 7,
                center[1] + radius - 7,
            ),
            start=-90,
            end=-90 + int(
                360 * proportion
            ),
            fill=accent,
            width=8,
        )

        text = str(self.value)
        font = load_font(35, True)

        bounds = draw.textbbox(
            (0, 0),
            text,
            font=font,
        )

        draw.text(
            (
                center[0]
                - (
                    bounds[2]
                    - bounds[0]
                ) / 2,
                center[1]
                - (
                    bounds[3]
                    - bounds[1]
                ) / 2
                - 3,
            ),
            text,
            font=font,
            fill=(35, 35, 60),
        )


class ProgressComponent(UniversalComponent):
    def __init__(
        self,
        current: int,
        total: int,
    ):
        self.current = max(
            int(current),
            0
        )
        self.total = max(
            int(total),
            1
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

        text_color = tuple(
            context.theme_pack.get(
                "text_color",
                (30, 45, 70),
            )
        )

        label = (
            f"{self.current} / {self.total}"
        )

        font = load_font(22, True)

        label_x = box.x + centered_x(
            draw,
            label,
            font,
            box.width,
        )

        draw.text(
            (label_x, box.y),
            label,
            font=font,
            fill=text_color,
        )

        bar_y = box.y + 32
        bar_height = max(
            box.height - 38,
            8
        )

        draw.rounded_rectangle(
            (
                box.x,
                bar_y,
                box.right,
                bar_y + bar_height,
            ),
            radius=bar_height // 2,
            fill=(215, 220, 235),
        )

        fill_width = int(
            box.width
            * min(
                self.current
                / self.total,
                1.0
            )
        )

        if fill_width > 0:
            draw.rounded_rectangle(
                (
                    box.x,
                    bar_y,
                    box.x + fill_width,
                    bar_y + bar_height,
                ),
                radius=bar_height // 2,
                fill=primary,
            )
