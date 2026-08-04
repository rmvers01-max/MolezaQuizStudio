from __future__ import annotations

import math
import random

from PIL import (
    Image,
    ImageDraw,
    ImageFilter,
    ImageFont,
)


class ThemeSpecificCompositor:
    """
    Desenha elementos temáticos diretamente no frame.

    Os motivos são decorativos e ficam atrás do conteúdo principal.
    """

    def apply(
        self,
        *,
        image: Image.Image,
        profile,
        time: float = 0.0,
        content_box: tuple[int, int, int, int] | None = None,
    ) -> Image.Image:
        canvas = image.convert("RGBA")
        layer = Image.new(
            "RGBA",
            canvas.size,
            (0, 0, 0, 0),
        )

        style = str(profile.motif_style)

        if style == "choice_shapes":
            self._choice_shapes(layer, profile, time)
        elif style == "map_compass":
            self._map_compass(layer, profile, time)
        elif style == "leaves_paws":
            self._leaves_paws(layer, profile, time)
        elif style == "food_shapes":
            self._food_shapes(layer, profile, time)
        elif style == "field_score":
            self._field_score(layer, profile, time)
        elif style == "stars_silhouettes":
            self._stars_mystery(layer, profile, time)
        else:
            self._knowledge_shapes(layer, profile, time)

        if content_box is not None:
            self._soft_frame(
                layer,
                content_box,
                profile,
            )

        canvas.alpha_composite(layer)
        return canvas

    def _choice_shapes(self, layer, profile, time):
        draw = ImageDraw.Draw(layer)
        width, height = layer.size

        left = (*profile.accent_color, 30)
        right = (*profile.secondary_color, 30)

        split = width // 2
        draw.polygon(
            ((0, 0), (split + 100, 0), (split - 70, height), (0, height)),
            fill=left,
        )
        draw.polygon(
            ((split - 100, 0), (width, 0), (width, height), (split + 70, height)),
            fill=right,
        )

        for index in range(14):
            x = int(
                (index * 109 + time * 28) % width
            )
            y = int(
                (index * 67 + 25 * math.sin(time + index)) % height
            )
            radius = 4 + index % 7
            color = (
                (*profile.accent_color, 80)
                if index % 2 == 0
                else (*profile.secondary_color, 70)
            )
            draw.ellipse(
                (x - radius, y - radius, x + radius, y + radius),
                fill=color,
            )

        self._center_label(
            draw,
            "OU",
            width // 2,
            height // 2,
            profile.accent_color,
            32,
        )

    def _map_compass(self, layer, profile, time):
        draw = ImageDraw.Draw(layer)
        width, height = layer.size

        for offset in range(-2, 4):
            y = int(height * 0.20 + offset * 62)
            draw.arc(
                (80, y - 90, width - 80, y + 90),
                190,
                350,
                fill=(*profile.secondary_color, 35),
                width=2,
            )

        center = (
            int(width * 0.82),
            int(height * 0.22),
        )
        radius = 74
        draw.ellipse(
            (
                center[0] - radius,
                center[1] - radius,
                center[0] + radius,
                center[1] + radius,
            ),
            outline=(*profile.accent_color, 70),
            width=3,
        )

        angle = time * 0.55
        tip = (
            center[0] + int(math.cos(angle) * radius * 0.75),
            center[1] + int(math.sin(angle) * radius * 0.75),
        )
        draw.line(
            (center, tip),
            fill=(*profile.accent_color, 100),
            width=4,
        )

        for index in range(7):
            x = 100 + index * 160
            draw.line(
                (x, 55, x - 45, 110),
                fill=(*profile.secondary_color, 28),
                width=3,
            )

    def _leaves_paws(self, layer, profile, time):
        draw = ImageDraw.Draw(layer)
        width, height = layer.size
        random.seed(431)

        for index in range(18):
            x = int(
                (random.randint(0, width) + time * (5 + index % 4)) % width
            )
            y = random.randint(0, height)
            size = 12 + index % 13

            draw.ellipse(
                (x - size, y - size // 2, x + size, y + size // 2),
                fill=(*profile.secondary_color, 35),
            )

            if index % 4 == 0:
                self._paw(
                    draw,
                    x,
                    y,
                    profile.accent_color,
                    34,
                )

    def _food_shapes(self, layer, profile, time):
        draw = ImageDraw.Draw(layer)
        width, height = layer.size

        for index in range(16):
            x = int(
                (70 + index * 89 + time * 16) % width
            )
            y = int(
                (40 + index * 57 + 13 * math.sin(time * 1.4 + index))
                % height
            )
            radius = 7 + index % 8
            draw.ellipse(
                (x - radius, y - radius, x + radius, y + radius),
                fill=(
                    (*profile.accent_color, 60)
                    if index % 2 == 0
                    else (*profile.secondary_color, 50)
                ),
            )

        for x in (150, width - 150):
            draw.ellipse(
                (x - 62, height - 155, x + 62, height - 31),
                outline=(*profile.accent_color, 42),
                width=4,
            )
            draw.ellipse(
                (x - 38, height - 131, x + 38, height - 55),
                outline=(*profile.secondary_color, 36),
                width=3,
            )

    def _field_score(self, layer, profile, time):
        draw = ImageDraw.Draw(layer)
        width, height = layer.size

        center_x = width // 2
        draw.line(
            (center_x, 40, center_x, height - 40),
            fill=(*profile.secondary_color, 30),
            width=3,
        )
        draw.ellipse(
            (
                center_x - 92,
                height // 2 - 92,
                center_x + 92,
                height // 2 + 92,
            ),
            outline=(*profile.accent_color, 38),
            width=4,
        )

        for index in range(10):
            x = int(
                (index * 142 + time * 75) % width
            )
            y = 90 + (index * 61) % (height - 180)
            draw.line(
                (x, y, x + 55, y),
                fill=(*profile.accent_color, 55),
                width=3,
            )

        draw.rounded_rectangle(
            (width - 250, 58, width - 66, 128),
            radius=14,
            outline=(*profile.accent_color, 60),
            width=3,
        )

    def _stars_mystery(self, layer, profile, time):
        draw = ImageDraw.Draw(layer)
        width, height = layer.size

        for index in range(22):
            x = int(
                (index * 83 + 29 + time * 7) % width
            )
            y = int(
                (index * 59 + 51 + 9 * math.sin(time + index))
                % height
            )
            size = 2 + index % 5
            self._star(
                draw,
                x,
                y,
                size,
                (*profile.accent_color, 70),
            )

        for center_x in (150, width - 150):
            draw.ellipse(
                (
                    center_x - 78,
                    height - 185,
                    center_x + 78,
                    height - 29,
                ),
                fill=(35, 25, 68, 26),
            )
            draw.ellipse(
                (
                    center_x - 43,
                    height - 152,
                    center_x + 43,
                    height - 66,
                ),
                fill=(*profile.secondary_color, 18),
            )

        self._center_label(
            draw,
            "?",
            width // 2,
            115,
            profile.accent_color,
            38,
        )

    def _knowledge_shapes(self, layer, profile, time):
        draw = ImageDraw.Draw(layer)
        width, height = layer.size

        for index in range(18):
            x = int(
                (index * 101 + time * 10) % width
            )
            y = int(
                (index * 71 + 18 * math.cos(time + index)) % height
            )
            size = 5 + index % 9

            if index % 3 == 0:
                draw.rounded_rectangle(
                    (x - size, y - size, x + size, y + size),
                    radius=4,
                    outline=(*profile.accent_color, 50),
                    width=2,
                )
            else:
                draw.ellipse(
                    (x - size, y - size, x + size, y + size),
                    outline=(*profile.secondary_color, 40),
                    width=2,
                )

        for text, x, y in (
            ("?", 120, 115),
            ("!", width - 135, 130),
            ("A", 145, height - 115),
        ):
            self._center_label(
                draw,
                text,
                x,
                y,
                profile.accent_color,
                24,
            )

    def _soft_frame(self, layer, box, profile):
        draw = ImageDraw.Draw(layer)
        x1, y1, x2, y2 = box
        draw.rounded_rectangle(
            (x1, y1, x2, y2),
            radius=34,
            outline=(*profile.accent_color, 45),
            width=3,
        )

    def _paw(self, draw, x, y, color, alpha):
        draw.ellipse(
            (x - 8, y - 2, x + 8, y + 14),
            fill=(*color, alpha),
        )
        for dx, dy in ((-13, -9), (-4, -14), (6, -14), (15, -8)):
            draw.ellipse(
                (x + dx - 4, y + dy - 4, x + dx + 4, y + dy + 4),
                fill=(*color, alpha),
            )

    def _star(self, draw, x, y, size, color):
        draw.line(
            (x - size, y, x + size, y),
            fill=color,
            width=1,
        )
        draw.line(
            (x, y - size, x, y + size),
            fill=color,
            width=1,
        )

    def _center_label(self, draw, text, x, y, color, size):
        try:
            font = ImageFont.truetype(
                "C:/Windows/Fonts/arialbd.ttf",
                max(int(size), 1),
            )
        except OSError:
            font = ImageFont.load_default()

        box = draw.textbbox(
            (0, 0),
            text,
            font=font,
        )
        width = box[2] - box[0]
        height = box[3] - box[1]

        draw.text(
            (
                x - width // 2,
                y - height // 2,
            ),
            text,
            font=font,
            fill=(*color, 80),
        )
