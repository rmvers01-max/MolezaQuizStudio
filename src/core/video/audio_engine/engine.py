from __future__ import annotations

from .mixer import AAAAudioMixer


class AAAAudioEngine:
    def __init__(
        self,
        profile: str = "balanced",
    ):
        self.profile = str(
            profile or "balanced"
        )
        self.mixer = AAAAudioMixer()

    def configure(
        self,
        profile: str,
    ):
        normalized = str(
            profile or "balanced"
        ).lower()

        if normalized not in {
            "balanced",
            "fast",
            "quality",
        }:
            normalized = "balanced"

        self.profile = normalized
        return self.profile

    def mix(
        self,
        *,
        duration,
        music_clip=None,
        foreground_clips=None,
        narration_clips=None,
    ):
        return self.mixer.mix(
            duration=duration,
            music_clip=music_clip,
            foreground_clips=(
                foreground_clips
            ),
            narration_clips=(
                narration_clips
            ),
            profile_code=self.profile,
        )

    @property
    def last_plan(self):
        return self.mixer.last_plan
