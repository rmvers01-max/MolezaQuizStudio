from __future__ import annotations

from .models import AudioMixProfile


class AudioMixProfileLibrary:
    @staticmethod
    def get(
        code: str = "balanced",
    ) -> AudioMixProfile:
        normalized = str(
            code or "balanced"
        ).lower()

        if normalized == "fast":
            return AudioMixProfile(
                code="fast",
                music_gain=0.90,
                narration_gain=1.00,
                sfx_gain=0.88,
                ducking_gain=0.48,
                ducking_attack=0.05,
                ducking_release=0.12,
                master_gain=0.92,
                limiter_ceiling=0.92,
                crossfade_duration=0.0,
                metadata={
                    "segmented_ducking": True,
                    "lightweight": True,
                },
            )

        if normalized == "quality":
            return AudioMixProfile(
                code="quality",
                music_gain=0.94,
                narration_gain=1.00,
                sfx_gain=0.92,
                ducking_gain=0.42,
                ducking_attack=0.10,
                ducking_release=0.22,
                master_gain=0.90,
                limiter_ceiling=0.90,
                crossfade_duration=0.08,
                metadata={
                    "segmented_ducking": True,
                    "lightweight": False,
                },
            )

        return AudioMixProfile(
            code="balanced",
            music_gain=0.92,
            narration_gain=1.00,
            sfx_gain=0.90,
            ducking_gain=0.45,
            ducking_attack=0.07,
            ducking_release=0.16,
            master_gain=0.91,
            limiter_ceiling=0.91,
            crossfade_duration=0.04,
            metadata={
                "segmented_ducking": True,
                "recommended_for_8gb": True,
            },
        )
