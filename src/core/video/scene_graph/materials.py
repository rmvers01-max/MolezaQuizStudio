from __future__ import annotations

import math

from PIL import (
    Image,
    ImageDraw,
    ImageFilter,
)

from .geometry import Rect


class SceneMaskFactory:
    def create(
        self,
        *,
        canvas_size: tuple[int, int],
        bounds: Rect,
        shape: str = "rectangle",
        corner_radius: int = 0,
        padding: int = 0,
        opacity: float = 1.0,
    ) -> Image.Image:
        width, height = canvas_size

        mask = Image.new(
            "L",
            (width, height),
            0,
        )

        draw = ImageDraw.Draw(mask)

        padded = Rect(
            x=max(
                bounds.x - padding,
                0,
            ),
            y=max(
                bounds.y - padding,
                0,
            ),
            width=min(
                bounds.width
                + padding * 2,
                width,
            ),
            height=min(
                bounds.height
                + padding * 2,
                height,
            ),
        )

        fill = int(
            255
            * max(
                min(
                    float(opacity),
                    1.0,
                ),
                0.0,
            )
        )

        if shape == "ellipse":
            draw.ellipse(
                padded.as_tuple(),
                fill=fill,
            )

        elif shape == "rounded_rectangle":
            draw.rounded_rectangle(
                padded.as_tuple(),
                radius=max(
                    int(corner_radius),
                    0,
                ),
                fill=fill,
            )

        else:
            draw.rectangle(
                padded.as_tuple(),
                fill=fill,
            )

        return mask


class ScopedMaterialRenderer:
    """
    Biblioteca de materiais ligados a nós da Scene Graph.
    """

    def __init__(self):
        self.mask_factory = (
            SceneMaskFactory()
        )

    def apply_sheen(
        self,
        *,
        canvas: Image.Image,
        bounds: Rect,
        progress: float,
        color=(255, 255, 255),
        intensity: float = 0.30,
        corner_radius: int = 22,
    ) -> Image.Image:
        progress = max(
            min(float(progress), 1.0),
            0.0,
        )

        intensity = max(
            min(float(intensity), 1.0),
            0.0,
        )

        layer = Image.new(
            "RGBA",
            canvas.size,
            (0, 0, 0, 0),
        )

        draw = ImageDraw.Draw(layer)

        travel = (
            bounds.width
            + bounds.height
        )

        center_x = int(
            bounds.x
            - bounds.height
            + travel
            * progress
        )

        band_width = max(
            int(bounds.width * 0.18),
            22,
        )

        polygon = (
            (
                center_x - band_width,
                bounds.y - 20,
            ),
            (
                center_x,
                bounds.y - 20,
            ),
            (
                center_x + band_width,
                bounds.bottom + 20,
            ),
            (
                center_x,
                bounds.bottom + 20,
            ),
        )

        draw.polygon(
            polygon,
            fill=(
                *tuple(color),
                int(130 * intensity),
            ),
        )

        layer = layer.filter(
            ImageFilter.GaussianBlur(
                radius=max(
                    int(
                        min(
                            bounds.width,
                            bounds.height,
                        )
                        * 0.045
                    ),
                    5,
                )
            )
        )

        mask = self.mask_factory.create(
            canvas_size=canvas.size,
            bounds=bounds,
            shape="rounded_rectangle",
            corner_radius=corner_radius,
        )

        clipped = Image.new(
            "RGBA",
            canvas.size,
            (0, 0, 0, 0),
        )

        clipped.paste(
            layer,
            (0, 0),
            mask,
        )

        result = canvas.copy()
        result.alpha_composite(
            clipped
        )

        return result

    def apply_inner_glow(
        self,
        *,
        canvas: Image.Image,
        bounds: Rect,
        progress: float,
        color,
        intensity: float = 0.60,
        corner_radius: int = 28,
        width: int = 8,
    ) -> Image.Image:
        pulse = math.sin(
            max(
                min(
                    float(progress),
                    1.0,
                ),
                0.0,
            )
            * math.pi
        )

        if pulse <= 0:
            return canvas

        layer = Image.new(
            "RGBA",
            canvas.size,
            (0, 0, 0, 0),
        )

        draw = ImageDraw.Draw(layer)

        draw.rounded_rectangle(
            bounds.as_tuple(),
            radius=max(
                int(corner_radius),
                0,
            ),
            outline=(
                *tuple(color),
                int(
                    210
                    * pulse
                    * max(
                        min(
                            float(intensity),
                            1.0,
                        ),
                        0.0,
                    )
                ),
            ),
            width=max(
                int(width),
                1,
            ),
        )

        softened = layer.filter(
            ImageFilter.GaussianBlur(
                radius=5
            )
        )

        mask = self.mask_factory.create(
            canvas_size=canvas.size,
            bounds=bounds,
            shape="rounded_rectangle",
            corner_radius=corner_radius,
        )

        clipped = Image.new(
            "RGBA",
            canvas.size,
            (0, 0, 0, 0),
        )

        clipped.paste(
            softened,
            (0, 0),
            mask,
        )

        clipped.alpha_composite(
            layer
        )

        result = canvas.copy()
        result.alpha_composite(
            clipped
        )

        return result

    def apply_focus_rim(
        self,
        *,
        canvas: Image.Image,
        bounds: Rect,
        color,
        intensity: float,
        corner_radius: int = 24,
    ) -> Image.Image:
        intensity = max(
            min(float(intensity), 1.0),
            0.0,
        )

        if intensity <= 0.01:
            return canvas

        layer = Image.new(
            "RGBA",
            canvas.size,
            (0, 0, 0, 0),
        )

        draw = ImageDraw.Draw(layer)

        draw.rounded_rectangle(
            bounds.as_tuple(),
            radius=corner_radius,
            outline=(
                *tuple(color),
                int(
                    92 * intensity
                ),
            ),
            width=5,
        )

        layer = layer.filter(
            ImageFilter.GaussianBlur(
                radius=7
            )
        )

        result = canvas.copy()
        result.alpha_composite(
            layer
        )

        return result
