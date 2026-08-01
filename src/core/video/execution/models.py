from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class ExecutionSettings:
    theme_pack: dict[str, Any]
    opening_enabled: bool
    opening_duration: float
    question_entry_duration: float
    reveal_duration: float
    pattern_breaks_enabled: bool
    pattern_break_interval: int
    pattern_break_intensity: float
    mascot_enabled: bool
    mascot_intensity: float
    audio_sync_enabled: bool
    outro_enabled: bool
    outro_duration: float
    quality_profile: str
    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "theme_pack": dict(
                self.theme_pack
            ),
            "opening_enabled": (
                self.opening_enabled
            ),
            "opening_duration": (
                self.opening_duration
            ),
            "question_entry_duration": (
                self.question_entry_duration
            ),
            "reveal_duration": (
                self.reveal_duration
            ),
            "pattern_breaks_enabled": (
                self.pattern_breaks_enabled
            ),
            "pattern_break_interval": (
                self.pattern_break_interval
            ),
            "pattern_break_intensity": (
                self.pattern_break_intensity
            ),
            "mascot_enabled": (
                self.mascot_enabled
            ),
            "mascot_intensity": (
                self.mascot_intensity
            ),
            "audio_sync_enabled": (
                self.audio_sync_enabled
            ),
            "outro_enabled": (
                self.outro_enabled
            ),
            "outro_duration": (
                self.outro_duration
            ),
            "quality_profile": (
                self.quality_profile
            ),
            "metadata": dict(
                self.metadata
            ),
        }
