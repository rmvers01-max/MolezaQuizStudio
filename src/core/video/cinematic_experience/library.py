from __future__ import annotations

from .models import CinematicExperience


class CinematicExperienceLibrary:
    """
    Biblioteca inicial de pacotes cinematográficos coerentes.

    Cada pacote descreve intenção narrativa, e não apenas efeitos
    isolados.
    """

    def discovery(self) -> CinematicExperience:
        return CinematicExperience(
            code="discovery_01",
            emotion="curiosity",
            camera_style="discovery_push",
            camera_multiplier=1.04,
            light_mode="soft_spot",
            light_intensity=0.42,
            particle_mode="floating_sparks",
            particle_intensity=0.30,
            color_temperature=-0.02,
            vignette=0.08,
            pulse=0.05,
            mascot_action="observe",
            audio_cue="soft_rise",
        )

    def suspense(self) -> CinematicExperience:
        return CinematicExperience(
            code="suspense_01",
            emotion="suspense",
            camera_style="slow_focus_push",
            camera_multiplier=1.10,
            light_mode="focused_cool",
            light_intensity=0.54,
            particle_mode="slow_dust",
            particle_intensity=0.22,
            color_temperature=-0.08,
            vignette=0.20,
            pulse=0.11,
            mascot_action="thinking",
            audio_cue="tension_rise",
        )

    def competition(self) -> CinematicExperience:
        return CinematicExperience(
            code="competition_01",
            emotion="challenge",
            camera_style="competition_push",
            camera_multiplier=1.14,
            light_mode="dual_energy",
            light_intensity=0.62,
            particle_mode="speed_streaks",
            particle_intensity=0.44,
            color_temperature=0.01,
            vignette=0.07,
            pulse=0.14,
            mascot_action="encourage",
            audio_cue="fast_whoosh",
        )

    def victory(self) -> CinematicExperience:
        return CinematicExperience(
            code="victory_01",
            emotion="victory",
            camera_style="hero_reveal",
            camera_multiplier=1.18,
            light_mode="golden_burst",
            light_intensity=0.78,
            particle_mode="confetti_sparks",
            particle_intensity=0.72,
            color_temperature=0.08,
            vignette=0.03,
            pulse=0.18,
            mascot_action="celebrate",
            audio_cue="victory_hit",
        )

    def calm(self) -> CinematicExperience:
        return CinematicExperience(
            code="calm_01",
            emotion="relief",
            camera_style="soft_drift",
            camera_multiplier=0.92,
            light_mode="open_soft",
            light_intensity=0.34,
            particle_mode="soft_bokeh",
            particle_intensity=0.16,
            color_temperature=0.04,
            vignette=0.02,
            pulse=0.02,
            mascot_action="happy",
            audio_cue="soft_release",
        )
