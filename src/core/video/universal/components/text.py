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
    load_font,
    wrap_lines,
)


class TitleComponent(UniversalComponent):
    def __init__(
        self,
        text: str,
    ):
        self.text = str(text)

    def render(
        self,
        image: Image.Image,
        box: ComponentBox,
        context: ComponentContext,
    ) -> None:
        draw = ImageDraw.Draw(image)

        font = fit_font(
            draw=draw,
            text=self.text,
            max_width=box.width - 30,
            start_size=42,
            min_size=25,
            bold=True,
        )

        color = tuple(
            context.theme_pack.get(
                "text_color",
                (30, 45, 70),
            )
        )

        x = box.x + centered_x(
            draw,
            self.text,
            font,
            box.width,
        )

        bounds = draw.textbbox(
            (0, 0),
            self.text,
            font=font,
        )

        y = box.y + int(
            (
                box.height
                - (
                    bounds[3]
                    - bounds[1]
                )
            )
            / 2
        )

        draw.text(
            (x, y),
            self.text,
            font=font,
            fill=color,
            stroke_width=2,
            stroke_fill=(255, 255, 255),
        )


class QuestionComponent(UniversalComponent):
    def __init__(
        self,
        text: str,
    ):
        self.text = str(text)

    def render(
        self,
        image: Image.Image,
        box: ComponentBox,
        context: ComponentContext,
    ) -> None:
        draw = ImageDraw.Draw(image)
        lines = wrap_lines(
            self.text,
            width=36,
            max_lines=3,
        )

        text_color = tuple(
            context.theme_pack.get(
                "text_color",
                (30, 45, 70),
            )
        )

        font = load_font(36, True)
        line_height = 46
        total_height = (
            len(lines)
            * line_height
        )

        y = box.y + max(
            int(
                (
                    box.height
                    - total_height
                )
                / 2
            ),
            0,
        )

        for line in lines:
            x = box.x + centered_x(
                draw,
                line,
                font,
                box.width,
            )

            draw.text(
                (x, y),
                line,
                font=font,
                fill=text_color,
                stroke_width=2,
                stroke_fill=(255, 255, 255),
            )

            y += line_height


class AnswerComponent(UniversalComponent):
    def __init__(
        self,
        text: str,
    ):
        self.text = str(text)

    def render(
        self,
        image: Image.Image,
        box: ComponentBox,
        context: ComponentContext,
    ) -> None:
        draw = ImageDraw.Draw(image)

        accent = tuple(
            context.theme_pack.get(
                "accent_color",
                (255, 215, 65),
            )
        )

        primary = tuple(
            context.theme_pack.get(
                "primary_color",
                (70, 120, 220),
            )
        )

        draw.rounded_rectangle(
            box.as_tuple(),
            radius=28,
            fill=(*accent, 245),
            outline=(255, 255, 255, 255),
            width=5,
        )

        label_font = load_font(25, True)
        answer_font = fit_font(
            draw=draw,
            text=self.text,
            max_width=box.width - 50,
            start_size=42,
            min_size=24,
            bold=True,
        )

        label = "RESPOSTA CORRETA"

        label_x = box.x + centered_x(
            draw,
            label,
            label_font,
            box.width,
        )

        draw.text(
            (label_x, box.y + 20),
            label,
            font=label_font,
            fill=primary,
        )

        answer_x = box.x + centered_x(
            draw,
            self.text,
            answer_font,
            box.width,
        )

        draw.text(
            (answer_x, box.y + 67),
            self.text,
            font=answer_font,
            fill=(35, 35, 55),
            stroke_width=2,
            stroke_fill=(255, 255, 255),
        )
