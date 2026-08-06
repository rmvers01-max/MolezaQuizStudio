from __future__ import annotations

from moviepy import (
    CompositeAudioClip,
    concatenate_audioclips,
)

from .ducking import AudioDuckingPlanner
from .models import AudioMixPlan
from .profiles import AudioMixProfileLibrary


class AAAAudioMixer:
    """
    Mixagem segura e leve para MoviePy.

    Não analisa todos os samples do vídeo, evitando alto uso de RAM.
    O limiter é preventivo: aplica ganho mestre conservador.
    """

    def __init__(self):
        self.ducking_planner = (
            AudioDuckingPlanner()
        )
        self.last_plan = None

    def mix(
        self,
        *,
        duration: float,
        music_clip=None,
        foreground_clips=None,
        narration_clips=None,
        profile_code: str = "balanced",
    ):
        foreground_clips = list(
            foreground_clips or []
        )
        narration_clips = list(
            narration_clips
            if narration_clips is not None
            else foreground_clips
        )

        profile = (
            AudioMixProfileLibrary.get(
                profile_code
            )
        )

        windows = (
            self.ducking_planner
            .create_windows(
                foreground_clips,
                duration=float(duration),
                gain=profile.ducking_gain,
                attack=profile.ducking_attack,
                release=profile.ducking_release,
            )
        )

        sources = []

        if music_clip is not None:
            prepared_music = (
                self._duck_music(
                    music_clip,
                    duration=float(duration),
                    windows=windows,
                    base_gain=profile.music_gain,
                )
            )

            sources.append(
                prepared_music
            )

        narration_ids = {
            id(clip)
            for clip in narration_clips
        }

        for clip in foreground_clips:
            gain = (
                profile.narration_gain
                if id(clip) in narration_ids
                else profile.sfx_gain
            )

            sources.append(
                clip.with_volume_scaled(
                    gain
                )
            )

        if not sources:
            self.last_plan = AudioMixPlan(
                duration=float(duration),
                profile=profile,
                ducking_windows=windows,
                narration_count=len(
                    narration_clips
                ),
                foreground_count=len(
                    foreground_clips
                ),
                music_present=False,
                metadata={
                    "audio_engine_version": "2.0",
                    "empty_mix": True,
                },
            )
            return None

        mixed = CompositeAudioClip(
            sources
        ).with_duration(
            float(duration)
        )

        mixed = mixed.with_volume_scaled(
            profile.master_gain
        )

        self.last_plan = AudioMixPlan(
            duration=float(duration),
            profile=profile,
            ducking_windows=windows,
            narration_count=len(
                narration_clips
            ),
            foreground_count=len(
                foreground_clips
            ),
            music_present=(
                music_clip is not None
            ),
            metadata={
                "audio_engine_version": "2.0",
                "limiter_mode": (
                    "preventive_master_gain"
                ),
                "limiter_ceiling": (
                    profile.limiter_ceiling
                ),
            },
        )

        return mixed

    def _duck_music(
        self,
        music_clip,
        *,
        duration: float,
        windows,
        base_gain: float,
    ):
        if not windows:
            return (
                music_clip
                .with_duration(
                    duration
                )
                .with_volume_scaled(
                    base_gain
                )
            )

        segments = []
        cursor = 0.0

        for window in windows:
            if window.start > cursor:
                segments.append(
                    music_clip.subclipped(
                        cursor,
                        window.start,
                    ).with_volume_scaled(
                        base_gain
                    )
                )

            if window.end > window.start:
                segments.append(
                    music_clip.subclipped(
                        window.start,
                        window.end,
                    ).with_volume_scaled(
                        base_gain
                        * window.gain
                    )
                )

            cursor = max(
                cursor,
                window.end,
            )

        if cursor < duration:
            segments.append(
                music_clip.subclipped(
                    cursor,
                    duration,
                ).with_volume_scaled(
                    base_gain
                )
            )

        if not segments:
            return (
                music_clip
                .with_duration(
                    duration
                )
                .with_volume_scaled(
                    base_gain
                )
            )

        return concatenate_audioclips(
            segments
        ).with_duration(
            duration
        )
