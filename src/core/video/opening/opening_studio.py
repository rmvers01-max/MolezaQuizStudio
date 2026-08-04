from __future__ import annotations

import math
import textwrap

import numpy as np
from PIL import (
    Image,
    ImageDraw,
    ImageFilter,
    ImageFont,
)
from moviepy import ImageSequenceClip

from ..animations import SmartEasing
from ..mascot_actor import MascotActorAnimator, MascotPerformanceDirector


class OpeningStudio:
    """
    AAA Opening Studio 2.0.

    A abertura funciona como um trailer curto:
    teaser visual -> gancho -> desafio -> transição para o jogo.
    """

    def __init__(
        self,
        largura=1280,
        altura=720,
        fps=24,
    ):
        self.largura = int(largura)
        self.altura = int(altura)
        self.fps = max(
            int(fps),
            18,
        )
        self.mascot_performance_director = MascotPerformanceDirector()
        self.mascot_actor_animator = MascotActorAnimator()

    def criar_clip(
        self,
        titulo: str,
        direcao: dict,
        brand_direction: dict,
        premium_theme,
    ):
        duracao = float(
            direcao.get(
                "duracao",
                4.15,
            )
        )

        total_quadros = max(
            int(round(duracao * self.fps)),
            2,
        )

        frames = []

        for index in range(total_quadros):
            time = index / self.fps
            progress = min(
                time / max(duracao, 0.001),
                1.0,
            )

            frame = self._render_frame(
                titulo=titulo,
                direction=direcao,
                brand_direction=brand_direction,
                premium_theme=premium_theme,
                time=time,
                progress=progress,
            )

            frames.append(
                np.asarray(
                    frame.convert("RGB")
                )
            )

        return ImageSequenceClip(
            frames,
            fps=self.fps,
        ).with_duration(
            duracao
        )

    def _render_frame(
        self,
        *,
        titulo,
        direction,
        brand_direction,
        premium_theme,
        time,
        progress,
    ):
        colors = self._colors(
            premium_theme,
            brand_direction,
            direction.get(
                "categoria",
                "general_knowledge",
            ),
        )

        image = self._background(
            colors=colors,
            time=time,
            camera_style=str(
                direction.get(
                    "camera_style",
                    "hero_push",
                )
            ),
        )

        self._particles(
            image=image,
            time=time,
            intensity=float(
                direction.get(
                    "intensidade",
                    0.84,
                )
            ),
            colors=colors,
        )

        draw = ImageDraw.Draw(image)

        # 0.0–0.9 s: teaser visual imediato.
        teaser_progress = self._interval(
            time,
            0.0,
            0.72,
        )

        self._draw_teasers(
            image=image,
            items=list(
                direction.get(
                    "teaser_items",
                    [],
                )
            ),
            progress=teaser_progress,
            colors=colors,
            time=time,
        )

        # Marca do canal entra cedo, mas não domina o primeiro quadro.
        brand_progress = self._interval(
            time,
            0.05,
            0.65,
        )

        brand_scale = max(
            SmartEasing.ease_out_back(
                brand_progress,
                overshoot=1.12,
            ),
            0.01,
        )

        self._center_text(
            draw=draw,
            text="MOLEZA QUIZ",
            y=36,
            size=max(
                int(35 * brand_scale),
                1,
            ),
            color=(255, 255, 255, 255),
            stroke=(54, 25, 105, 255),
            stroke_width=4,
            opacity=brand_progress,
        )

        # 0.45–1.55 s: gancho principal.
        hook_progress = self._interval(
            time,
            0.42,
            1.38,
        )

        hook_scale = max(
            SmartEasing.ease_out_back(
                hook_progress,
                overshoot=1.08,
            ),
            0.01,
        )

        hook = str(
            direction.get(
                "hook_texto",
                "VOCÊ CONSEGUE ACERTAR TODAS?",
            )
        )

        hook_lines = textwrap.wrap(
            hook,
            width=31,
        )[:2]

        hook_y = 196

        for line in hook_lines:
            self._center_text(
                draw=draw,
                text=line,
                y=hook_y,
                size=max(
                    int(
                        43 * hook_scale
                    ),
                    1,
                ),
                color=(
                    *colors["highlight"],
                    255,
                ),
                stroke=(48, 22, 84, 255),
                stroke_width=5,
                opacity=hook_progress,
            )
            hook_y += 54

        # Título aparece como subtítulo contextual.
        title_progress = self._interval(
            time,
            1.08,
            1.82,
        )

        title_lines = textwrap.wrap(
            str(titulo).upper(),
            width=34,
        )[:2]

        title_y = 325

        for line in title_lines:
            self._center_text(
                draw=draw,
                text=line,
                y=title_y,
                size=34,
                color=(255, 255, 255, 255),
                stroke=(40, 20, 75, 255),
                stroke_width=4,
                opacity=title_progress,
            )
            title_y += 43

        # Badge de quantidade.
        quantity_progress = self._interval(
            time,
            1.45,
            2.15,
        )

        if direction.get(
            "mostrar_quantidade",
            True,
        ):
            total = int(
                direction.get(
                    "total_perguntas",
                    1,
                )
            )

            label = (
                f"{total} DESAFIOS"
                if direction.get(
                    "categoria"
                ) != "preference"
                else f"{total} ESCOLHAS"
            )

            self._badge(
                image=image,
                text=label,
                center=(
                    self.largura // 2,
                    432,
                ),
                progress=quantity_progress,
                color=colors["secondary"],
            )

        # CTA para participação.
        challenge_progress = self._interval(
            time,
            2.00,
            2.85,
        )

        challenge = str(
            direction.get(
                "desafio_texto",
                "MARQUE UM PONTO PARA CADA ACERTO!",
            )
        )

        self._center_text(
            draw=draw,
            text=challenge,
            y=506,
            size=30,
            color=(255, 255, 255, 255),
            stroke=(55, 25, 95, 255),
            stroke_width=4,
            opacity=challenge_progress,
        )

        # Mascote atua em três estados durante a abertura.
        if direction.get(
            "usar_mascote",
            True,
        ):
            self._mascot_actor(
                image=image,
                direction=direction,
                time=time,
                progress=progress,
            )

        # Barra de energia prepara a primeira pergunta.
        self._energy_line(
            image=image,
            progress=self._interval(
                time,
                2.55,
                max(
                    float(
                        direction.get(
                            "duracao",
                            4.15,
                        )
                    )
                    - 0.35,
                    2.8,
                ),
            ),
            colors=colors,
        )

        # Transição cinematográfica final.
        self._transition(
            image=image,
            progress=self._interval(
                time,
                max(
                    float(
                        direction.get(
                            "duracao",
                            4.15,
                        )
                    )
                    - 0.55,
                    0.0,
                ),
                float(
                    direction.get(
                        "duracao",
                        4.15,
                    )
                ),
            ),
            style=str(
                direction.get(
                    "transition_style",
                    "light_wipe",
                )
            ),
            colors=colors,
        )

        return image


def _mascot_actor(self, *, image, direction, time, progress):
    duration=float(direction.get("duracao",4.15))
    performance=self.mascot_performance_director.create_performance(
        scene_kind="question", question_number=0, duration=duration,
        difficulty=45, surprise=True, focus_side="center",
        production_mode=direction.get("metadata",{}).get("production_mode","")
    )
    mascot,x,y=self.mascot_actor_animator.render(
        performance=performance,time=time,
        canvas_size=(self.largura,self.altura),base_size=(210,210))
    if mascot is not None:
        image.alpha_composite(mascot,(x,y))

    def _draw_teasers(
        self,
        *,
        image,
        items,
        progress,
        colors,
        time,
    ):
        if not items:
            return

        layer = Image.new(
            "RGBA",
            image.size,
            (0, 0, 0, 0),
        )
        draw = ImageDraw.Draw(layer)

        count = len(items)
        card_width = 118
        card_height = 92
        gap = 16

        total_width = (
            card_width * count
            + gap * (count - 1)
        )

        start_x = (
            self.largura
            - total_width
        ) // 2

        y = 88

        for index, item in enumerate(items):
            item_progress = max(
                min(
                    progress * 1.45
                    - index * 0.12,
                    1.0,
                ),
                0.0,
            )

            scale = max(
                SmartEasing.ease_out_back(
                    item_progress,
                    overshoot=1.08,
                ),
                0.01,
            )

            width = max(
                int(card_width * scale),
                1,
            )
            height = max(
                int(card_height * scale),
                1,
            )

            center_x = (
                start_x
                + index * (card_width + gap)
                + card_width // 2
            )

            x1 = center_x - width // 2
            y1 = y + (card_height - height) // 2
            x2 = x1 + width
            y2 = y1 + height

            shadow = (
                x1 + 5,
                y1 + 7,
                x2 + 5,
                y2 + 7,
            )

            draw.rounded_rectangle(
                shadow,
                radius=20,
                fill=(25, 15, 55, 90),
            )

            draw.rounded_rectangle(
                (x1, y1, x2, y2),
                radius=20,
                fill=(255, 255, 255, 225),
                outline=(
                    *colors["highlight"],
                    220,
                ),
                width=4,
            )

            font = self._font(
                43 if len(str(item)) <= 2 else 31,
                bold=True,
            )

            bbox = draw.textbbox(
                (0, 0),
                str(item),
                font=font,
            )

            text_x = (
                center_x
                - (bbox[2] - bbox[0]) // 2
            )

            text_y = (
                y1
                + (height - (bbox[3] - bbox[1])) // 2
                - 3
            )

            draw.text(
                (text_x, text_y),
                str(item),
                font=font,
                fill=(45, 35, 70, 255),
            )

        image.alpha_composite(layer)

    def _energy_line(
        self,
        *,
        image,
        progress,
        colors,
    ):
        if progress <= 0:
            return

        layer = Image.new(
            "RGBA",
            image.size,
            (0, 0, 0, 0),
        )

        draw = ImageDraw.Draw(layer)

        width = int(
            (self.largura - 260)
            * SmartEasing.ease_out_cubic(
                progress
            )
        )

        x1 = (
            self.largura - width
        ) // 2

        y = 582

        draw.rounded_rectangle(
            (
                130,
                y,
                self.largura - 130,
                y + 12,
            ),
            radius=6,
            fill=(255, 255, 255, 70),
        )

        draw.rounded_rectangle(
            (
                x1,
                y,
                x1 + width,
                y + 12,
            ),
            radius=6,
            fill=(
                *colors["highlight"],
                230,
            ),
        )

        layer = layer.filter(
            ImageFilter.GaussianBlur(
                radius=1.4,
            )
        )

        image.alpha_composite(layer)

    def _transition(
        self,
        *,
        image,
        progress,
        style,
        colors,
    ):
        if progress <= 0:
            return

        eased = self._ease_in_out_cubic(


            progress


        )

        layer = Image.new(
            "RGBA",
            image.size,
            (0, 0, 0, 0),
        )
        draw = ImageDraw.Draw(layer)

        if style in {
            "split_choice",
            "flag_wipe",
        }:
            half = int(
                self.largura
                * eased
                / 2
            )

            draw.rectangle(
                (
                    0,
                    0,
                    half,
                    self.altura,
                ),
                fill=(
                    *colors["primary"],
                    255,
                ),
            )

            draw.rectangle(
                (
                    self.largura - half,
                    0,
                    self.largura,
                    self.altura,
                ),
                fill=(
                    *colors["secondary"],
                    255,
                ),
            )
        else:
            x = int(
                -self.largura
                + self.largura * 2 * eased
            )

            draw.polygon(
                (
                    (x - 280, 0),
                    (x + 140, 0),
                    (x + 420, self.altura),
                    (x, self.altura),
                ),
                fill=(255, 255, 255, 245),
            )

            draw.polygon(
                (
                    (x - 500, 0),
                    (x - 250, 0),
                    (x + 30, self.altura),
                    (x - 220, self.altura),
                ),
                fill=(
                    *colors["highlight"],
                    220,
                ),
            )

            if progress > 0.72:
                alpha = int(
                    255
                    * (
                        progress - 0.72
                    )
                    / 0.28
                )

                draw.rectangle(
                    (
                        0,
                        0,
                        self.largura,
                        self.altura,
                    ),
                    fill=(
                        255,
                        255,
                        255,
                        alpha,
                    ),
                )

        image.alpha_composite(layer)

    def _background(
        self,
        *,
        colors,
        time,
        camera_style,
    ):
        image = Image.new(
            "RGBA",
            (
                self.largura,
                self.altura,
            ),
            (0, 0, 0, 255),
        )

        draw = ImageDraw.Draw(image)

        top = colors["top"]
        bottom = colors["bottom"]

        for y in range(self.altura):
            p = y / max(
                self.altura - 1,
                1,
            )

            color = tuple(
                int(
                    top[index]
                    + (
                        bottom[index]
                        - top[index]
                    )
                    * p
                )
                for index in range(3)
            )

            draw.line(
                (
                    0,
                    y,
                    self.largura,
                    y,
                ),
                fill=color,
            )

        light = Image.new(
            "RGBA",
            image.size,
            (0, 0, 0, 0),
        )

        light_draw = ImageDraw.Draw(light)

        movement = int(
            80 * math.sin(time * 0.85)
        )

        if camera_style in {
            "fast_push",
            "competition_push",
        }:
            movement *= 2

        light_draw.ellipse(
            (
                -180 + movement,
                -180,
                570 + movement,
                610,
            ),
            fill=(
                *colors["light_a"],
                100,
            ),
        )

        light_draw.ellipse(
            (
                700 - movement,
                -170,
                1480 - movement,
                600,
            ),
            fill=(
                *colors["light_b"],
                90,
            ),
        )

        light = light.filter(
            ImageFilter.GaussianBlur(
                radius=105,
            )
        )

        image.alpha_composite(light)

        return image

    def _particles(
        self,
        *,
        image,
        time,
        intensity,
        colors,
    ):
        draw = ImageDraw.Draw(image)

        amount = max(
            int(30 * intensity),
            10,
        )

        for index in range(amount):
            x = (
                index * 137
                + int(time * (18 + index % 5))
            ) % self.largura

            y = (
                index * 83
                + int(
                    14
                    * math.sin(
                        time * 1.2
                        + index
                    )
                )
            ) % self.altura

            radius = 2 + index % 4

            color = (
                colors["highlight"]
                if index % 2 == 0
                else colors["secondary"]
            )

            draw.ellipse(
                (
                    x - radius,
                    y - radius,
                    x + radius,
                    y + radius,
                ),
                fill=(
                    *color,
                    70 + index % 70,
                ),
            )

    def _badge(
        self,
        *,
        image,
        text,
        center,
        progress,
        color,
    ):
        if progress <= 0:
            return

        layer = Image.new(
            "RGBA",
            image.size,
            (0, 0, 0, 0),
        )

        draw = ImageDraw.Draw(layer)

        scale = max(
            SmartEasing.ease_out_back(
                progress,
                overshoot=1.10,
            ),
            0.01,
        )

        font = self._font(
            max(
                int(28 * scale),
                1,
            ),
            bold=True,
        )

        bbox = draw.textbbox(
            (0, 0),
            text,
            font=font,
        )

        width = (
            bbox[2] - bbox[0] + 52
        )

        height = (
            bbox[3] - bbox[1] + 25
        )

        x1 = center[0] - width // 2
        y1 = center[1] - height // 2

        draw.rounded_rectangle(
            (
                x1,
                y1,
                x1 + width,
                y1 + height,
            ),
            radius=height // 2,
            fill=(
                *color,
                int(230 * progress),
            ),
            outline=(
                255,
                255,
                255,
                int(220 * progress),
            ),
            width=3,
        )

        draw.text(
            (
                center[0]
                - (bbox[2] - bbox[0]) // 2,
                center[1]
                - (bbox[3] - bbox[1]) // 2
                - 2,
            ),
            text,
            font=font,
            fill=(
                255,
                255,
                255,
                int(255 * progress),
            ),
        )

        image.alpha_composite(layer)

    def _center_text(
        self,
        *,
        draw,
        text,
        y,
        size,
        color,
        stroke,
        stroke_width,
        opacity=1.0,
    ):
        if opacity <= 0:
            return

        font = self._font(
            max(int(size), 1),
            bold=True,
        )

        bbox = draw.textbbox(
            (0, 0),
            text,
            font=font,
            stroke_width=stroke_width,
        )

        x = (
            self.largura
            - (bbox[2] - bbox[0])
        ) // 2

        draw.text(
            (x, y),
            text,
            font=font,
            fill=(
                color[0],
                color[1],
                color[2],
                int(
                    color[3] * opacity
                ),
            ),
            stroke_width=stroke_width,
            stroke_fill=(
                stroke[0],
                stroke[1],
                stroke[2],
                int(
                    stroke[3] * opacity
                ),
            ),
        )

    def _colors(
        self,
        premium_theme,
        brand_direction,
        category,
    ):
        palettes = {
            "flags_geography": {
                "top": (48, 92, 190),
                "bottom": (39, 35, 105),
                "primary": (46, 105, 220),
                "secondary": (235, 65, 85),
                "highlight": (255, 221, 75),
                "light_a": (90, 190, 255),
                "light_b": (255, 100, 135),
            },
            "preference": {
                "top": (111, 48, 185),
                "bottom": (44, 25, 105),
                "primary": (255, 85, 120),
                "secondary": (66, 145, 255),
                "highlight": (255, 218, 75),
                "light_a": (255, 92, 150),
                "light_b": (75, 155, 255),
            },
            "animals": {
                "top": (55, 150, 120),
                "bottom": (24, 87, 95),
                "primary": (55, 175, 125),
                "secondary": (255, 157, 66),
                "highlight": (255, 230, 105),
                "light_a": (95, 225, 160),
                "light_b": (255, 185, 95),
            },
            "food": {
                "top": (235, 88, 112),
                "bottom": (116, 42, 112),
                "primary": (255, 98, 115),
                "secondary": (255, 165, 65),
                "highlight": (255, 235, 98),
                "light_a": (255, 135, 155),
                "light_b": (255, 190, 90),
            },
        }

        return palettes.get(
            category,
            {
                "top": (92, 55, 180),
                "bottom": (38, 28, 95),
                "primary": (112, 68, 210),
                "secondary": (61, 155, 225),
                "highlight": (255, 220, 70),
                "light_a": (145, 95, 255),
                "light_b": (65, 180, 255),
            },
        )

    def _font(
        self,
        size,
        bold=False,
    ):
        candidates = (
            (
                "C:/Windows/Fonts/arialbd.ttf",
                "C:/Windows/Fonts/Arial.ttf",
            )
            if bold
            else (
                "C:/Windows/Fonts/Arial.ttf",
                "C:/Windows/Fonts/arialbd.ttf",
            )
        )

        for path in candidates:
            try:
                return ImageFont.truetype(
                    path,
                    max(int(size), 1),
                )
            except OSError:
                continue

        return ImageFont.load_default()

    def _ease_in_out_cubic(
        self,
        value,
    ):
        t = max(
            min(
                float(value),
                1.0,
            ),
            0.0,
        )

        if t < 0.5:
            return 4.0 * t * t * t

        return (
            1.0
            - pow(
                -2.0 * t + 2.0,
                3,
            )
            / 2.0
        )

    def _interval(
        self,
        time,
        start,
        end,
    ):
        if end <= start:
            return 1.0

        return max(
            min(
                (time - start)
                / (end - start),
                1.0,
            ),
            0.0,
        )
