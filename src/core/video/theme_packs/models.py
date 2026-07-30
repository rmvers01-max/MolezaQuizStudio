from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class UniversalThemePack:
    code: str
    name: str
    keywords: tuple[str, ...]
    background_top: tuple[int, int, int]
    background_bottom: tuple[int, int, int]
    panel_color: tuple[int, int, int]
    primary_color: tuple[int, int, int]
    secondary_color: tuple[int, int, int]
    accent_color: tuple[int, int, int]
    text_color: tuple[int, int, int]
    particle_style: str
    camera_style: str
    reveal_style: str
    mascot_style: str
    background_activity: float
    glow_intensity: float
    motion_intensity: float

    def to_dict(self) -> dict:
        return {
            "code": self.code,
            "name": self.name,
            "keywords": list(self.keywords),
            "background_top": list(
                self.background_top
            ),
            "background_bottom": list(
                self.background_bottom
            ),
            "panel_color": list(
                self.panel_color
            ),
            "primary_color": list(
                self.primary_color
            ),
            "secondary_color": list(
                self.secondary_color
            ),
            "accent_color": list(
                self.accent_color
            ),
            "text_color": list(
                self.text_color
            ),
            "particle_style": (
                self.particle_style
            ),
            "camera_style": (
                self.camera_style
            ),
            "reveal_style": (
                self.reveal_style
            ),
            "mascot_style": (
                self.mascot_style
            ),
            "background_activity": (
                self.background_activity
            ),
            "glow_intensity": (
                self.glow_intensity
            ),
            "motion_intensity": (
                self.motion_intensity
            ),
        }
