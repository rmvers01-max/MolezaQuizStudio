from __future__ import annotations

import math
import random

from PIL import (
    Image,
    ImageDraw,
    ImageEnhance,
    ImageFilter,
)


class CinematicExperienceCompositor:
    def apply_pre_camera(
        self,
        *,
        image: Image.Image,
        experience,
        time: float,
        progress: float,
        focus,
        accent_color,
    ) -> Image.Image:
        result = image.convert("RGBA")

        result = self._lighting(
            result,
            experience=experience,
            time=time,
            focus=focus,
            accent_color=accent_color,
        )

        result = self._particles(
            result,
            experience=experience,
            time=time,
            progress=progress,
            accent_color=accent_color,
        )

        return result

    def apply_post_camera(
        self,
        *,
        image: Image.Image,
        experience,
        time: float,
        progress: float,
    ) -> Image.Image:
        result = image.convert("RGBA")

        result = self._temperature(
            result,
            amount=float(
                experience.color_temperature
            ),
        )

        if experience.vignette > 0:
            result = self._vignette(
                result,
                intensity=float(
                    experience.vignette
                ),
            )

        if experience.pulse > 0:
            pulse = (
                1.0
                + float(experience.pulse)
                * 0.045
                * math.sin(
                    time * 4.0
                    + progress * math.pi
                )
            )

            result = ImageEnhance.Brightness(
                result
            ).enhance(
                max(pulse, 0.82)
            )

        return result

    def _lighting(
        self,
        image,
        *,
        experience,
        time,
        focus,
        accent_color,
    ):
        layer = Image.new(
            "RGBA",
            image.size,
            (0, 0, 0, 0),
        )

        draw = ImageDraw.Draw(layer)

        x = int(
            getattr(
                focus,
                "x",
                image.width // 2,
            )
        )
        y = int(
            getattr(
                focus,
                "y",
                image.height // 2,
            )
        )

        intensity = max(
            min(
                float(
                    experience.light_intensity
                ),
                1.0,
            ),
            0.0,
        )

        radius = int(
            min(
                image.width,
                image.height,
            )
            * (
                0.42
                if experience.light_mode
                == "golden_burst"
                else 0.34
            )
        )

        if experience.light_mode == "focused_cool":
            color = (
                105,
                155,
                255,
                int(105 * intensity),
            )
        elif experience.light_mode == "golden_burst":
            color = (
                255,
                215,
                90,
                int(155 * intensity),
            )
        elif experience.light_mode == "dual_energy":
            color = (
                *tuple(accent_color),
                int(120 * intensity),
            )
        else:
            color = (
                255,
                255,
                255,
                int(90 * intensity),
            )

        drift_x = int(
            18 * math.sin(time * 1.4)
        )
        drift_y = int(
            12 * math.cos(time * 1.1)
        )

        draw.ellipse(
            (
                x - radius + drift_x,
                y - radius + drift_y,
                x + radius + drift_x,
                y + radius + drift_y,
            ),
            fill=color,
        )

        if experience.light_mode == "dual_energy":
            second_x = (
                image.width - x
            )

            draw.ellipse(
                (
                    second_x - radius,
                    y - radius,
                    second_x + radius,
                    y + radius,
                ),
                fill=(
                    90,
                    170,
                    255,
                    int(85 * intensity),
                ),
            )

        layer = layer.filter(
            ImageFilter.GaussianBlur(
                radius=max(
                    int(radius * 0.42),
                    18,
                )
            )
        )

        result = image.copy()
        result.alpha_composite(
            layer
        )

        return result

    def _particles(
        self,
        image,
        *,
        experience,
        time,
        progress,
        accent_color,
    ):
        intensity = max(
            min(
                float(
                    experience.particle_intensity
                ),
                1.0,
            ),
            0.0,
        )

        if intensity <= 0.01:
            return image

        layer = Image.new(
            "RGBA",
            image.size,
            (0, 0, 0, 0),
        )

        draw = ImageDraw.Draw(layer)

        amount = max(
            int(24 * intensity),
            4,
        )

        mode = str(
            experience.particle_mode
        )

        for index in range(amount):
            seed = (
                index * 7919
                + int(time * 24)
            )

            rng = random.Random(seed)

            x = int(
                (
                    rng.random()
                    * image.width
                    + time
                    * (
                        35
                        if mode
                        == "speed_streaks"
                        else 10
                    )
                )
                % image.width
            )

            y = int(
                (
                    rng.random()
                    * image.height
                    - time
                    * (
                        30
                        if mode
                        == "confetti_sparks"
                        else 8
                    )
                )
                % image.height
            )

            if mode == "speed_streaks":
                length = 18 + index % 24
                draw.line(
                    (
                        x,
                        y,
                        x + length,
                        y,
                    ),
                    fill=(
                        *tuple(accent_color),
                        int(95 + 95 * intensity),
                    ),
                    width=2 + index % 3,
                )

            elif mode == "confetti_sparks":
                size = 3 + index % 5
                color = (
                    (255, 220, 70, 210)
                    if index % 2 == 0
                    else (
                        *tuple(accent_color),
                        200,
                    )
                )

                draw.rectangle(
                    (
                        x,
                        y,
                        x + size,
                        y + size * 2,
                    ),
                    fill=color,
                )

            else:
                radius = 2 + index % 4
                alpha = int(
                    65
                    + 90 * intensity
                )

                draw.ellipse(
                    (
                        x - radius,
                        y - radius,
                        x + radius,
                        y + radius,
                    ),
                    fill=(
                        *tuple(accent_color),
                        alpha,
                    ),
                )

        if mode in {
            "floating_sparks",
            "slow_dust",
            "soft_bokeh",
        }:
            layer = layer.filter(
                ImageFilter.GaussianBlur(
                    radius=1.6
                    if mode != "soft_bokeh"
                    else 4.5
                )
            )

        result = image.copy()
        result.alpha_composite(
            layer
        )

        return result

    def _temperature(
        self,
        image,
        *,
        amount,
    ):
        if abs(amount) < 0.001:
            return image

        overlay = Image.new(
            "RGBA",
            image.size,
            (
                255,
                160,
                80,
                int(
                    min(
                        abs(amount) * 210,
                        30,
                    )
                ),
            )
            if amount > 0
            else (
                80,
                140,
                255,
                int(
                    min(
                        abs(amount) * 210,
                        30,
                    )
                ),
            ),
        )

        result = image.copy()
        result.alpha_composite(
            overlay
        )

        return result

    def _vignette(
        self,
        image,
        *,
        intensity,
    ):
        width, height = image.size

        mask = Image.new(
            "L",
            image.size,
            255,
        )

        draw = ImageDraw.Draw(mask)

        margin_x = int(
            width * 0.08
        )
        margin_y = int(
            height * 0.08
        )

        draw.ellipse(
            (
                margin_x,
                margin_y,
                width - margin_x,
                height - margin_y,
            ),
            fill=0,
        )

        mask = mask.filter(
            ImageFilter.GaussianBlur(
                radius=int(
                    min(width, height)
                    * 0.18
                )
            )
        )

        darkness = Image.new(
            "RGBA",
            image.size,
            (
                0,
                0,
                0,
                int(
                    180
                    * max(
                        min(intensity, 1.0),
                        0.0,
                    )
                ),
            ),
        )

        darkness.putalpha(
            mask.point(
                lambda value: int(
                    value
                    * max(
                        min(intensity, 1.0),
                        0.0,
                    )
                )
            )
        )

        result = image.copy()
        result.alpha_composite(
            darkness
        )

        return result
