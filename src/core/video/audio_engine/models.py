from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class AudioMixProfile:
    code: str
    music_gain: float
    narration_gain: float
    sfx_gain: float
    ducking_gain: float
    ducking_attack: float
    ducking_release: float
    master_gain: float
    limiter_ceiling: float
    crossfade_duration: float
    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "code": self.code,
            "music_gain": self.music_gain,
            "narration_gain": self.narration_gain,
            "sfx_gain": self.sfx_gain,
            "ducking_gain": self.ducking_gain,
            "ducking_attack": self.ducking_attack,
            "ducking_release": self.ducking_release,
            "master_gain": self.master_gain,
            "limiter_ceiling": self.limiter_ceiling,
            "crossfade_duration": self.crossfade_duration,
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True, slots=True)
class DuckingWindow:
    start: float
    end: float
    gain: float
    reason: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "start": self.start,
            "end": self.end,
            "gain": self.gain,
            "reason": self.reason,
        }


@dataclass(frozen=True, slots=True)
class AudioMixPlan:
    duration: float
    profile: AudioMixProfile
    ducking_windows: tuple[DuckingWindow, ...]
    narration_count: int
    foreground_count: int
    music_present: bool
    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "duration": self.duration,
            "profile": self.profile.to_dict(),
            "ducking_windows": [
                window.to_dict()
                for window in self.ducking_windows
            ],
            "narration_count": self.narration_count,
            "foreground_count": self.foreground_count,
            "music_present": self.music_present,
            "metadata": dict(self.metadata),
        }
