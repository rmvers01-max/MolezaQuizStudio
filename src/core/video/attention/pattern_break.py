from __future__ import annotations

from dataclasses import dataclass

from PIL import Image, ImageDraw, ImageFilter


@dataclass(frozen=True, slots=True)
class PatternBreakDecision:
    active: bool
    variant: int
    intensity: float
    camera_boost: float
    particle_boost: float
    mascot_boost: float
    accent_side: str


class PatternBreakDirector:
    """
    Cria quebras de padrão discretas e reproduzíveis.

    A regra evita que perguntas consecutivas pareçam idênticas,
    mas mantém a identidade e a legibilidade.
    """

    def decide(
        self,
        question_number: int,
        total_questions: int,
        scene_kind: str,
    ) -> PatternBreakDecision:
        number = max(
            int(question_number),
            1,
        )

        total = max(
            int(total_questions),
            1,
        )

        interval = (
            3
            if total <= 10
            else 4
            if total <= 24
            else 5
        )

        active = (
            scene_kind == "question"
            and number > 1
            and number % interval == 0
        )

        variant = (
            number
            + total
        ) % 4

        return PatternBreakDecision(
            active=active,
            variant=variant,
            intensity=(
                0.78
                if active
                else 0.0
            ),
            camera_boost=(
                0.18
                if active
                else 0.0
            ),
            particle_boost=(
                0.22
                if active
                else 0.0
            ),
            mascot_boost=(
                0.15
                if active
                else 0.0
            ),
            accent_side=(
                "left"
                if variant % 2 == 0
                else "right"
            ),
        )

    def apply_accent(
        self,
        image: Image.Image,
        decision: PatternBreakDecision,
        accent_color,
        progress: float,
    ) -> Image.Image:
        if not decision.active:
            return image

        progress = max(
            min(float(progress), 1.0),
            0.0,
        )

        pulse = min(
            progress / 0.32,
            1.0,
        )

        layer = Image.new(
            "RGBA",
            image.size,
            (0, 0, 0, 0),
        )

        draw = ImageDraw.Draw(layer)

        width = int(
            120
            + 150 * pulse
        )

        alpha = int(
            70
            * decision.intensity
            * (
                1.0 - 0.35 * progress
            )
        )

        if decision.accent_side == "left":
            polygon = (
                (0, 0),
                (width, 0),
                (width // 2, image.height),
                (0, image.height),
            )
        else:
            polygon = (
                (
                    image.width - width,
                    0
                ),
                (
                    image.width,
                    0
                ),
                (
                    image.width,
                    image.height
                ),
                (
                    image.width
                    - width // 2,
                    image.height
                ),
            )

        draw.polygon(
            polygon,
            fill=(
                *tuple(accent_color),
                alpha,
            ),
        )

        layer = layer.filter(
            ImageFilter.GaussianBlur(
                radius=32
            )
        )

        result = image.copy()
        result.alpha_composite(layer)

        return result
