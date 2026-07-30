from __future__ import annotations

import math
import random
from pathlib import Path

import numpy as np
from PIL import (
    Image,
    ImageDraw,
    ImageEnhance,
    ImageFilter,
)
from moviepy import ImageSequenceClip


class UniversalLegacyMotionRenderer:
    """
    Aplica vida e movimento aos frames do renderizador legado.

    Isso permite que quizzes de conhecimento, incluindo bandeiras,
    recebam movimento enquanto a migração ao Universal Renderer
    ainda não foi concluída.
    """

    def __init__(
        self,
        largura=1280,
        altura=720,
        fps=18,
    ):
        self.largura = int(largura)
        self.altura = int(altura)
        self.fps = max(
            int(fps),
            12
        )

    def create_clip(
        self,
        image_path,
        duration,
        scene_kind,
        theme_pack,
        question_number=0,
    ):
        image_path = Path(
            image_path
        )

        base = Image.open(
            image_path
        ).convert("RGBA")

        duration = max(
            float(duration),
            0.1
        )

        total_frames = max(
            int(
                round(
                    duration
                    * self.fps
                )
            ),
            2
        )

        frames = []

        for index in range(
            total_frames
        ):
            time = index / self.fps
            progress = min(
                time / duration,
                1.0
            )

            frame = self._render_frame(
                base=base,
                time=time,
                progress=progress,
                scene_kind=scene_kind,
                theme_pack=theme_pack,
                question_number=question_number,
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
            duration
        )

    def _render_frame(
        self,
        base,
        time,
        progress,
        scene_kind,
        theme_pack,
        question_number,
    ):
        activity = float(
            theme_pack.get(
                "background_activity",
                0.50
            )
        )

        motion = float(
            theme_pack.get(
                "motion_intensity",
                0.50
            )
        )

        if scene_kind == "countdown":
            activity *= 0.48
            motion *= 0.45

        elif scene_kind == "reveal":
            activity *= 1.05
            motion *= 0.80

        elif scene_kind == "outro":
            activity *= 0.70
            motion *= 0.50

        frame = base.copy()

        frame = self._camera_breath(
            frame,
            time=time,
            progress=progress,
            intensity=motion,
            scene_kind=scene_kind,
            question_number=question_number,
        )

        self._ambient_lights(
            frame,
            time=time,
            pack=theme_pack,
            intensity=activity,
        )

        self._particles(
            frame,
            time=time,
            style=theme_pack.get(
                "particle_style",
                "sparkles"
            ),
            intensity=activity,
            seed=question_number,
        )

        if scene_kind == "reveal":
            self._reveal_glow(
                frame,
                progress=progress,
                color=tuple(
                    theme_pack.get(
                        "accent_color",
                        (255, 215, 65)
                    )
                ),
            )

        return frame

    def _camera_breath(
        self,
        image,
        time,
        progress,
        intensity,
        scene_kind,
        question_number,
    ):
        pulse = (
            0.5
            + 0.5
            * math.sin(
                time * 0.85
                + question_number
            )
        )

        zoom = (
            1.0
            + (
                0.006
                + 0.006 * pulse
            )
            * intensity
        )

        if scene_kind == "reveal":
            zoom += (
                0.008
                * math.sin(
                    progress * math.pi
                )
            )

        width = max(
            int(
                self.largura * zoom
            ),
            self.largura
        )

        height = max(
            int(
                self.altura * zoom
            ),
            self.altura
        )

        resized = image.resize(
            (width, height),
            Image.Resampling.LANCZOS
        )

        pan_x = int(
            4
            * intensity
            * math.sin(
                time * 0.45
                + question_number
            )
        )

        pan_y = int(
            3
            * intensity
            * math.cos(
                time * 0.40
                + question_number
            )
        )

        x = max(
            min(
                (
                    width
                    - self.largura
                ) // 2
                + pan_x,
                width - self.largura
            ),
            0
        )

        y = max(
            min(
                (
                    height
                    - self.altura
                ) // 2
                + pan_y,
                height - self.altura
            ),
            0
        )

        return resized.crop(
            (
                x,
                y,
                x + self.largura,
                y + self.altura,
            )
        )

    def _ambient_lights(
        self,
        image,
        time,
        pack,
        intensity,
    ):
        layer = Image.new(
            "RGBA",
            image.size,
            (0, 0, 0, 0)
        )

        draw = ImageDraw.Draw(
            layer
        )

        primary = tuple(
            pack.get(
                "primary_color",
                (115, 70, 205)
            )
        )

        secondary = tuple(
            pack.get(
                "secondary_color",
                (255, 95, 135)
            )
        )

        dx = int(
            55
            * math.sin(
                time * 0.38
            )
        )

        draw.ellipse(
            (
                -240 + dx,
                -180,
                520 + dx,
                570,
            ),
            fill=(
                *primary,
                int(
                    38 * intensity
                )
            ),
        )

        draw.ellipse(
            (
                760 - dx,
                -180,
                1500 - dx,
                540,
            ),
            fill=(
                *secondary,
                int(
                    34 * intensity
                )
            ),
        )

        layer = layer.filter(
            ImageFilter.GaussianBlur(
                radius=105
            )
        )

        image.alpha_composite(
            layer
        )

    def _particles(
        self,
        image,
        time,
        style,
        intensity,
        seed,
    ):
        random.seed(
            9200 + int(seed)
        )

        layer = Image.new(
            "RGBA",
            image.size,
            (0, 0, 0, 0)
        )

        draw = ImageDraw.Draw(
            layer
        )

        count = max(
            int(
                16 * intensity
            ),
            5
        )

        for index in range(
            count
        ):
            x_base = (
                index * 109
                + 47
            ) % self.largura

            y_base = (
                index * 71
                + 33
            ) % self.altura

            speed = (
                0.18
                + (
                    index % 3
                )
                * 0.07
            )

            x = (
                x_base
                + 15
                * math.sin(
                    time * speed
                    + index
                )
            )

            y = (
                y_base
                + 11
                * math.cos(
                    time
                    * speed
                    * 0.8
                    + index
                )
            )

            size = 2 + (
                index % 3
            )

            alpha = int(
                (
                    38
                    + (
                        index % 3
                    )
                    * 17
                )
                * intensity
            )

            if style == "map_stars":
                draw.arc(
                    (
                        x - size * 2,
                        y - size,
                        x + size * 2,
                        y + size,
                    ),
                    start=0,
                    end=300,
                    fill=(
                        185,
                        225,
                        255,
                        alpha,
                    ),
                    width=1,
                )

            elif style == "leaves":
                draw.ellipse(
                    (
                        x - size,
                        y - size // 2,
                        x + size,
                        y + size // 2,
                    ),
                    fill=(
                        175,
                        240,
                        165,
                        alpha,
                    ),
                )

            elif style in {
                "energy",
                "ribbons",
            }:
                draw.line(
                    (
                        x - size * 2,
                        y + size,
                        x + size * 2,
                        y - size,
                    ),
                    fill=(
                        255,
                        225,
                        110,
                        alpha,
                    ),
                    width=2,
                )

            else:
                draw.ellipse(
                    (
                        x - size,
                        y - size,
                        x + size,
                        y + size,
                    ),
                    fill=(
                        255,
                        255,
                        255,
                        alpha,
                    ),
                )

        layer = layer.filter(
            ImageFilter.GaussianBlur(
                radius=0.7
            )
        )

        image.alpha_composite(
            layer
        )

    def _reveal_glow(
        self,
        image,
        progress,
        color,
    ):
        pulse = math.sin(
            progress * math.pi
        )

        if pulse <= 0:
            return

        layer = Image.new(
            "RGBA",
            image.size,
            (0, 0, 0, 0)
        )

        draw = ImageDraw.Draw(
            layer
        )

        draw.rounded_rectangle(
            (
                70,
                60,
                self.largura - 70,
                self.altura - 60,
            ),
            radius=45,
            outline=(
                *color,
                int(
                    90 * pulse
                )
            ),
            width=8,
        )

        layer = layer.filter(
            ImageFilter.GaussianBlur(
                radius=10
            )
        )

        image.alpha_composite(
            layer
        )
