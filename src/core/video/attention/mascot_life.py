from __future__ import annotations

from PIL import Image

from ..animations.character_engine import (
    CharacterAnimationEngine,
)
from .eye_focus import FocusTarget


class MascotLifeEngine:
    """
    Integra o mascote às cenas universais.

    Funciona com fallback silencioso quando uma pose ainda não existe.
    """

    def __init__(self):
        self.character = (
            CharacterAnimationEngine()
        )

    def render(
        self,
        image: Image.Image,
        *,
        scene_kind: str,
        progress: float,
        focus: FocusTarget,
        intensity: float = 1.0,
    ) -> Image.Image:
        pose, behavior = self._behavior(
            scene_kind
        )

        mascot, dx, dy = (
            self.character.renderizar(
                pose=pose,
                progresso=progress,
                tamanho_base=(178, 178),
                comportamento=behavior,
                intensidade=intensity,
            )
        )

        if mascot is None:
            return image

        # O mascote fica do lado oposto ao foco principal sempre que
        # possível, reduzindo o risco de cobrir conteúdo.
        if focus.x >= image.width // 2:
            x = 20 + dx
        else:
            x = (
                image.width
                - mascot.width
                - 18
                + dx
            )

        y = (
            image.height
            - mascot.height
            - 8
            + dy
        )

        result = image.copy()
        result.alpha_composite(
            mascot,
            (int(x), int(y)),
        )

        return result


    def render_asset(
        self,
        *,
        scene_kind: str,
        progress: float,
        intensity: float = 1.0,
        size: tuple[int, int] = (178, 178),
    ):
        pose, behavior = self._behavior(scene_kind)
        return self.character.renderizar(
            pose=pose,
            progresso=progress,
            tamanho_base=size,
            comportamento=behavior,
            intensidade=intensity,
        )

    def _behavior(
        self,
        scene_kind: str,
    ) -> tuple[str, str]:
        if scene_kind == "countdown":
            return "thinking", "thinking"

        if scene_kind == "reveal":
            return "celebrate", "celebrate"

        return "idle", "idle"
