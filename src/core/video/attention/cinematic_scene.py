from __future__ import annotations

import math

from PIL import Image

from .eye_focus import FocusTarget


class CinematicSceneDirector:
    """
    Microcâmera guiada pelo foco.

    A amplitude máxima é pequena para preservar a leitura.
    """

    def apply_camera(
        self,
        image: Image.Image,
        *,
        target: FocusTarget,
        time: float,
        progress: float,
        scene_kind: str,
        motion_intensity: float,
    ) -> Image.Image:
        motion_intensity = max(
            min(float(motion_intensity), 1.0),
            0.0,
        )

        if scene_kind == "countdown":
            motion_intensity *= 0.28

        breath = (
            0.5
            + 0.5
            * math.sin(
                time * 0.72
            )
        )

        zoom = (
            1.0
            + (
                0.004
                + 0.005 * breath
            )
            * motion_intensity
        )

        if scene_kind == "reveal":
            zoom += (
                0.010
                * math.sin(
                    min(
                        max(progress, 0.0),
                        1.0,
                    )
                    * math.pi
                )
                * motion_intensity
            )

        width = max(
            int(image.width * zoom),
            image.width,
        )

        height = max(
            int(image.height * zoom),
            image.height,
        )

        resized = image.resize(
            (width, height),
            Image.Resampling.LANCZOS,
        )

        target_offset_x = (
            target.x
            - image.width / 2
        )

        target_offset_y = (
            target.y
            - image.height / 2
        )

        max_x = width - image.width
        max_y = height - image.height

        center_x = max_x / 2
        center_y = max_y / 2

        x = int(
            center_x
            + target_offset_x
            * 0.018
            * motion_intensity
        )

        y = int(
            center_y
            + target_offset_y
            * 0.018
            * motion_intensity
        )

        x = max(
            min(x, max_x),
            0,
        )

        y = max(
            min(y, max_y),
            0,
        )

        return resized.crop(
            (
                x,
                y,
                x + image.width,
                y + image.height,
            )
        )
