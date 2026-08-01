from __future__ import annotations

import hashlib
from typing import Any

from core.video.theme_packs import UniversalThemePackRegistry

from .models import CreativeOverride, ProductionPlan


class AICreativeDirector:
    def __init__(self):
        self.theme_registry = UniversalThemePackRegistry()

    def create_plan(
        self,
        *,
        title: str,
        quiz_type: str,
        total_questions: int,
        creative_plan: dict[str, Any],
        override: CreativeOverride | None = None,
    ) -> ProductionPlan:
        override = override or CreativeOverride()
        total = max(int(total_questions), 1)
        seed = self._seed(f"{title}|{quiz_type}|{total}")

        theme_pack = self._resolve_theme(
            title=title,
            quiz_type=quiz_type,
            creative_plan=creative_plan,
            override=override,
        )

        energy = self._energy_level(
            quiz_type=quiz_type,
            total=total,
            seed=seed,
        )

        pacing = self._pacing_mode(
            total=total,
            quiz_type=quiz_type,
        )

        theme_pack = dict(theme_pack)

        if override.background_activity is not None:
            theme_pack["background_activity"] = float(
                override.background_activity
            )

        if override.motion_intensity is not None:
            theme_pack["motion_intensity"] = float(
                override.motion_intensity
            )

        if override.camera_style is not None:
            theme_pack["camera_style"] = str(
                override.camera_style
            )

        opening_duration = (
            float(override.opening_duration)
            if override.opening_duration is not None
            else self._opening_duration(energy, quiz_type)
        )

        outro_duration = (
            float(override.outro_duration)
            if override.outro_duration is not None
            else 5.0
        )

        pattern_enabled = (
            bool(override.enable_pattern_breaks)
            if override.enable_pattern_breaks is not None
            else total >= 6
        )

        audio_enabled = (
            bool(override.enable_audio_sync)
            if override.enable_audio_sync is not None
            else True
        )

        mascot_intensity = (
            float(override.mascot_intensity)
            if override.mascot_intensity is not None
            else self._mascot_intensity(quiz_type, energy)
        )

        interval = 3 if total <= 10 else 4 if total <= 24 else 5

        return ProductionPlan(
            title=str(title),
            quiz_type=str(quiz_type),
            total_questions=total,
            audience="infantil e família",
            energy_level=energy,
            pacing_mode=pacing,
            theme_pack=theme_pack,
            opening={
                "enabled": True,
                "duration": opening_duration,
                "hook_mode": (
                    "choice_challenge"
                    if quiz_type == "preferencia"
                    else "guess_challenge"
                ),
                "first_question_deadline": round(
                    opening_duration + 0.9,
                    2,
                ),
            },
            question_flow={
                "entry_duration": self._entry_duration(pacing),
                "countdown_mode": "stable",
                "reveal_duration": self._reveal_duration(pacing),
                "visual_variation": "adaptive",
                "avoid_identical_consecutive_scenes": True,
            },
            pattern_breaks={
                "enabled": pattern_enabled,
                "interval": interval,
                "max_without_visual_change": interval,
                "intensity": round(
                    min(0.70 + energy * 0.18, 0.92),
                    2,
                ),
            },
            mascot={
                "enabled": True,
                "intensity": round(mascot_intensity, 2),
                "position_policy": "opposite_primary_focus",
                "never_cover_primary": True,
                "behavior_policy": "automatic_by_scene",
            },
            audio={
                "sync_enabled": audio_enabled,
                "duck_music_on_voice": True,
                "tick_countdown": True,
                "reveal_impact": True,
                "pattern_break_whoosh": pattern_enabled,
            },
            outro={
                "enabled": True,
                "duration": outro_duration,
                "goal": "next_video_and_subscribe",
                "youtube_end_screen_safe": True,
            },
            quality={
                "profile": "balanced",
                "final_profile": "aaa",
                "anti_aliasing": True,
                "stable_text_priority": True,
            },
            automation={
                "mode": "automatic_with_optional_overrides",
                "automatic_decisions": True,
                "manual_override_used": self._override_used(override),
            },
            metadata={
                "seed": seed,
                "director_version": "1.0",
                "extra_overrides": dict(override.extra),
            },
        )

    def _resolve_theme(
        self,
        *,
        title,
        quiz_type,
        creative_plan,
        override,
    ):
        if override.theme_pack:
            return self.theme_registry.get(
                override.theme_pack
            ).to_dict()

        current = creative_plan.get("theme_pack")

        if isinstance(current, dict):
            return dict(current)

        return self.theme_registry.select(
            title=title,
            quiz_type=quiz_type,
        ).to_dict()

    def _energy_level(self, quiz_type, total, seed):
        base = {
            "preferencia": 0.78,
            "conhecimento": 0.64,
        }.get(str(quiz_type), 0.68)

        if total >= 20:
            base -= 0.05
        elif total <= 8:
            base += 0.04

        return round(
            min(max(base + (seed % 9) / 100, 0.55), 0.88),
            2,
        )

    def _pacing_mode(self, total, quiz_type):
        if total >= 25:
            return "long_form_balanced"
        if total <= 8:
            return "fast_compact"
        if quiz_type == "preferencia":
            return "playful_dynamic"
        return "steady_game"

    def _opening_duration(self, energy, quiz_type):
        base = 4.0 if quiz_type == "preferencia" else 4.2
        return round(
            min(max(base - (energy - 0.65) * 0.7, 3.7), 4.6),
            2,
        )

    def _entry_duration(self, pacing):
        return {
            "fast_compact": 0.78,
            "playful_dynamic": 0.86,
            "steady_game": 0.92,
            "long_form_balanced": 0.84,
        }.get(pacing, 0.90)

    def _reveal_duration(self, pacing):
        return {
            "fast_compact": 1.65,
            "playful_dynamic": 1.85,
            "steady_game": 2.00,
            "long_form_balanced": 1.75,
        }.get(pacing, 1.90)

    def _mascot_intensity(self, quiz_type, energy):
        multiplier = 1.0 if quiz_type == "preferencia" else 0.86
        return min(energy * 1.18 * multiplier, 1.0)

    def _override_used(self, override):
        return any(
            value is not None
            for value in (
                override.theme_pack,
                override.camera_style,
                override.mascot_intensity,
                override.background_activity,
                override.motion_intensity,
                override.opening_duration,
                override.outro_duration,
                override.enable_pattern_breaks,
                override.enable_audio_sync,
            )
        ) or bool(override.extra)

    def _seed(self, value):
        digest = hashlib.sha256(
            str(value).encode("utf-8")
        ).hexdigest()
        return int(digest[:8], 16)
