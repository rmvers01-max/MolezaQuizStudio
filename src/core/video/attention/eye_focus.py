from __future__ import annotations

from dataclasses import dataclass

from PIL import Image, ImageDraw, ImageFilter


@dataclass(frozen=True, slots=True)
class FocusTarget:
    x: int
    y: int
    radius: int
    intensity: float


class EyeFocusDirector:
    """
    Define e reforça o ponto principal de atenção da cena.

    O efeito é propositalmente discreto:
    - luz suave;
    - vinheta invertida;
    - nenhum elemento é escondido ou deformado.
    """

    def resolve_knowledge_target(
        self,
        *,
        scene_kind: str,
        has_image: bool,
        width: int,
        height: int,
    ) -> FocusTarget:
        if scene_kind == "reveal":
            return FocusTarget(
                x=width // 2,
                y=int(height * 0.72),
                radius=int(width * 0.30),
                intensity=0.72,
            )

        if scene_kind == "countdown":
            return FocusTarget(
                x=width // 2,
                y=int(height * 0.48),
                radius=int(width * 0.34),
                intensity=0.35,
            )

        if has_image:
            return FocusTarget(
                x=int(width * 0.28),
                y=int(height * 0.52),
                radius=int(width * 0.25),
                intensity=0.48,
            )

        return FocusTarget(
            x=width // 2,
            y=int(height * 0.50),
            radius=int(width * 0.36),
            intensity=0.42,
        )

    def apply(
        self,
        image: Image.Image,
        target: FocusTarget,
        accent_color=(255, 220, 90),
    ) -> Image.Image:
        intensity = max(
            min(float(target.intensity), 1.0),
            0.0,
        )

        if intensity <= 0.01:
            return image

        glow = Image.new(
            "RGBA",
            image.size,
            (0, 0, 0, 0),
        )

        glow_draw = ImageDraw.Draw(glow)

        glow_draw.ellipse(
            (
                target.x - target.radius,
                target.y - target.radius,
                target.x + target.radius,
                target.y + target.radius,
            ),
            fill=(
                *tuple(accent_color),
                int(42 * intensity),
            ),
        )

        glow = glow.filter(
            ImageFilter.GaussianBlur(
                radius=max(
                    int(target.radius * 0.32),
                    18,
                )
            )
        )

        result = image.copy()
        result.alpha_composite(glow)

        vignette = Image.new(
            "RGBA",
            image.size,
            (0, 0, 0, 0),
        )

        vignette_draw = ImageDraw.Draw(vignette)
        border_alpha = int(34 * intensity)

        vignette_draw.rectangle(
            (0, 0, image.width, image.height),
            fill=(0, 0, 0, border_alpha),
        )

        mask = Image.new(
            "L",
            image.size,
            255,
        )

        mask_draw = ImageDraw.Draw(mask)

        mask_draw.ellipse(
            (
                target.x - int(target.radius * 1.15),
                target.y - int(target.radius * 1.15),
                target.x + int(target.radius * 1.15),
                target.y + int(target.radius * 1.15),
            ),
            fill=0,
        )

        mask = mask.filter(
            ImageFilter.GaussianBlur(
                radius=max(
                    int(target.radius * 0.30),
                    20,
                )
            )
        )

        vignette.putalpha(mask.point(
            lambda value: int(
                value * border_alpha / 255
            )
        ))

        result.alpha_composite(vignette)
        return result
