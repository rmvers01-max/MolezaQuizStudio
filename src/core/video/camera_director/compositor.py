from __future__ import annotations

import math

from PIL import (
    Image,
    ImageEnhance,
    ImageFilter,
)

from ..motion_graphics import MotionEasing


class AAACameraCompositor:
    def apply(
        self,
        *,
        image: Image.Image,
        plan,
        time: float,
        duration: float,
    ) -> Image.Image:
        move = plan.primary_move
        progress = self._progress(
            time,
            min(
                max(float(duration), 0.001),
                max(float(move.duration), 0.001),
            ),
        )

        eased = self._ease(
            progress,
            move.easing,
        )

        zoom = (
            float(move.zoom_from)
            + (
                float(move.zoom_to)
                - float(move.zoom_from)
            )
            * eased
        )

        zoom = min(
            zoom,
            1.0 + float(plan.safe_motion_limit) * 0.18,
        )

        result = self._zoom_and_pan(
            image=image,
            zoom=zoom,
            pan_x=float(move.pan_x) * eased,
            pan_y=float(move.pan_y) * eased,
            target_x=float(plan.target_x),
            target_y=float(plan.target_y),
        )

        if float(move.shake) > 0:
            result = self._shake(
                result,
                strength=float(move.shake),
                time=time,
            )

        if float(move.depth_strength) > 0:
            result = self._depth(
                result,
                amount=float(move.depth_strength),
            )

        return result

    def _zoom_and_pan(
        self,
        *,
        image,
        zoom,
        pan_x,
        pan_y,
        target_x,
        target_y,
    ):
        width, height = image.size

        scaled_width = max(
            int(width * zoom),
            width,
        )
        scaled_height = max(
            int(height * zoom),
            height,
        )

        scaled = image.resize(
            (scaled_width, scaled_height),
            Image.Resampling.LANCZOS,
        )

        extra_x = scaled_width - width
        extra_y = scaled_height - height

        focus_x = max(min(target_x, 1.0), 0.0)
        focus_y = max(min(target_y, 1.0), 0.0)

        left = int(
            extra_x * focus_x
            + pan_x * width
        )
        top = int(
            extra_y * focus_y
            + pan_y * height
        )

        left = max(
            min(left, extra_x),
            0,
        )
        top = max(
            min(top, extra_y),
            0,
        )

        return scaled.crop(
            (
                left,
                top,
                left + width,
                top + height,
            )
        )

    def _shake(
        self,
        image,
        *,
        strength,
        time,
    ):
        width, height = image.size

        dx = int(
            math.sin(time * 17.0)
            * width
            * strength
            * 0.004
        )
        dy = int(
            math.cos(time * 19.0)
            * height
            * strength
            * 0.004
        )

        padded = Image.new(
            "RGBA",
            (
                width + 12,
                height + 12,
            ),
            (0, 0, 0, 255),
        )
        padded.alpha_composite(
            image,
            (6 + dx, 6 + dy),
        )

        return padded.crop(
            (
                6,
                6,
                6 + width,
                6 + height,
            )
        )

    def _depth(
        self,
        image,
        *,
        amount,
    ):
        blurred = image.filter(
            ImageFilter.GaussianBlur(
                radius=max(
                    float(amount) * 2.5,
                    0.0,
                )
            )
        )

        return Image.blend(
            image,
            blurred,
            alpha=min(
                max(float(amount) * 0.08, 0.0),
                0.08,
            ),
        )

    def _ease(
        self,
        progress,
        easing,
    ):
        if easing == "ease_out_back":
            return MotionEasing.ease_out_back(
                progress
            )
        if easing == "ease_out_cubic":
            return MotionEasing.ease_out_cubic(
                progress
            )
        if easing == "ease_in_out_cubic":
            return MotionEasing.ease_in_out_cubic(
                progress
            )
        return MotionEasing.clamp(
            progress
        )

    def _progress(
        self,
        time,
        duration,
    ):
        if duration <= 0:
            return 1.0

        return MotionEasing.clamp(
            float(time)
            / float(duration)
        )
