from __future__ import annotations

import math

import numpy as np
from PIL import (
    Image,
    ImageDraw,
    ImageFilter,
    ImageFont,
)
from moviepy import ImageSequenceClip

from ..animations.character_engine import (
    CharacterAnimationEngine,
)


class OutroStudio:
    """
    Tela final animada, preparada para os slots do YouTube.
    """

    def __init__(
        self,
        width=1280,
        height=720,
        fps=18,
    ):
        self.width = int(width)
        self.height = int(height)
        self.fps = max(int(fps), 12)
        self.character = (
            CharacterAnimationEngine()
        )

    def create_clip(
        self,
        *,
        text: str,
        duration: float,
        theme_pack: dict,
    ):
        duration = max(
            float(duration),
            3.5,
        )

        total_frames = max(
            int(round(duration * self.fps)),
            2,
        )

        frames = []

        for index in range(total_frames):
            time = index / self.fps
            progress = min(
                time / duration,
                1.0,
            )

            frame = self._frame(
                text=text,
                time=time,
                progress=progress,
                theme_pack=theme_pack,
            )

            frames.append(
                np.asarray(
                    frame.convert("RGB")
                )
            )

        return ImageSequenceClip(
            frames,
            fps=self.fps,
        ).with_duration(duration)

    def _frame(
        self,
        *,
        text,
        time,
        progress,
        theme_pack,
    ):
        top = tuple(
            theme_pack.get(
                "background_top",
                (90, 55, 180),
            )
        )

        bottom = tuple(
            theme_pack.get(
                "background_bottom",
                (35, 28, 92),
            )
        )

        accent = tuple(
            theme_pack.get(
                "accent_color",
                (255, 215, 65),
            )
        )

        primary = tuple(
            theme_pack.get(
                "primary_color",
                (115, 70, 205),
            )
        )

        image = Image.new(
            "RGBA",
            (self.width, self.height),
            (*bottom, 255),
        )

        draw = ImageDraw.Draw(image)

        for y in range(self.height):
            p = y / max(
                self.height - 1,
                1,
            )

            color = tuple(
                int(
                    top[i]
                    + (
                        bottom[i]
                        - top[i]
                    )
                    * p
                )
                for i in range(3)
            )

            draw.line(
                (0, y, self.width, y),
                fill=(*color, 255),
            )

        light = Image.new(
            "RGBA",
            image.size,
            (0, 0, 0, 0),
        )

        light_draw = ImageDraw.Draw(light)

        dx = int(
            55 * math.sin(time * 0.42)
        )

        light_draw.ellipse(
            (
                -180 + dx,
                -160,
                570 + dx,
                580,
            ),
            fill=(*primary, 70),
        )

        light_draw.ellipse(
            (
                720 - dx,
                -180,
                1470 - dx,
                560,
            ),
            fill=(*accent, 55),
        )

        light = light.filter(
            ImageFilter.GaussianBlur(
                radius=105
            )
        )

        image.alpha_composite(light)
        draw = ImageDraw.Draw(image)

        title_font = self._font(44, True)
        body_font = self._font(28, True)
        small_font = self._font(22, True)

        self._center_text(
            draw,
            "VOCÊ FOI INCRÍVEL!",
            y=52,
            font=title_font,
            fill=(255, 255, 255),
            stroke=primary,
            stroke_width=4,
        )

        self._center_text(
            draw,
            str(text),
            y=118,
            font=body_font,
            fill=accent,
            stroke=(45, 28, 85),
            stroke_width=3,
        )

        pulse = (
            0.5
            + 0.5
            * math.sin(
                time * 2.0
            )
        )

        outline_alpha = int(
            180 + 70 * pulse
        )

        video_box = (
            145,
            225,
            760,
            565,
        )

        subscribe_box = (
            845,
            285,
            1095,
            535,
        )

        draw.rounded_rectangle(
            video_box,
            radius=34,
            fill=(255, 255, 255, 32),
            outline=(
                *accent,
                outline_alpha,
            ),
            width=6,
        )

        draw.rounded_rectangle(
            subscribe_box,
            radius=125,
            fill=(255, 255, 255, 34),
            outline=(
                255,
                255,
                255,
                outline_alpha,
            ),
            width=6,
        )

        self._center_in_box(
            draw,
            "PRÓXIMO DESAFIO",
            video_box,
            small_font,
            (255, 255, 255),
        )

        self._center_in_box(
            draw,
            "INSCREVA-SE",
            subscribe_box,
            small_font,
            (255, 255, 255),
        )

        mascot, mx, my = (
            self.character.renderizar(
                pose="point_left",
                progresso=progress,
                tamanho_base=(185, 185),
                comportamento="point_left",
                intensidade=1.0,
            )
        )

        if mascot is not None:
            image.alpha_composite(
                mascot,
                (
                    self.width
                    - mascot.width
                    - 20
                    + mx,
                    self.height
                    - mascot.height
                    - 6
                    + my,
                ),
            )

        return image

    def _center_text(
        self,
        draw,
        text,
        *,
        y,
        font,
        fill,
        stroke,
        stroke_width,
    ):
        bounds = draw.textbbox(
            (0, 0),
            text,
            font=font,
            stroke_width=stroke_width,
        )

        x = int(
            (
                self.width
                - (
                    bounds[2]
                    - bounds[0]
                )
            )
            / 2
        )

        draw.text(
            (x, y),
            text,
            font=font,
            fill=fill,
            stroke_width=stroke_width,
            stroke_fill=stroke,
        )

    def _center_in_box(
        self,
        draw,
        text,
        box,
        font,
        fill,
    ):
        bounds = draw.textbbox(
            (0, 0),
            text,
            font=font,
        )

        text_width = bounds[2] - bounds[0]
        text_height = bounds[3] - bounds[1]

        x = int(
            (
                box[0] + box[2]
                - text_width
            )
            / 2
        )

        y = int(
            (
                box[1] + box[3]
                - text_height
            )
            / 2
        )

        draw.text(
            (x, y),
            text,
            font=font,
            fill=fill,
        )

    def _font(
        self,
        size,
        bold=False,
    ):
        candidates = (
            [
                "C:/Windows/Fonts/arialbd.ttf",
                "C:/Windows/Fonts/calibrib.ttf",
            ]
            if bold
            else [
                "C:/Windows/Fonts/arial.ttf",
                "C:/Windows/Fonts/calibri.ttf",
            ]
        )

        for candidate in candidates:
            try:
                return ImageFont.truetype(
                    candidate,
                    size,
                )
            except OSError:
                continue

        return ImageFont.load_default()
