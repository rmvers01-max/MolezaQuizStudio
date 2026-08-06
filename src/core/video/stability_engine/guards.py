from __future__ import annotations

from .models import StabilityFinding


class RegressionGuard:
    """
    Verifica invariantes que já causaram regressões no projeto.
    """

    def run(
        self,
        *,
        video_generator=None,
    ):
        checks = {}
        findings = []

        if video_generator is None:
            return checks, findings

        renderer = getattr(
            video_generator,
            "renderer",
            None,
        )

        preference_renderer = getattr(
            video_generator,
            "preference_renderer",
            None,
        )

        checks[
            "renderer_present"
        ] = renderer is not None

        checks[
            "preference_renderer_present"
        ] = (
            preference_renderer
            is not None
        )

        if renderer is None:
            findings.append(
                StabilityFinding(
                    code="renderer_missing",
                    severity="error",
                    message=(
                        "Renderer principal ausente."
                    ),
                    component="legacy_renderer",
                )
            )

        if preference_renderer is None:
            findings.append(
                StabilityFinding(
                    code="preference_renderer_missing",
                    severity="error",
                    message=(
                        "Renderer de preferência ausente."
                    ),
                    component="preference_renderer",
                )
            )

        if preference_renderer is not None:
            safe_scene = hasattr(
                preference_renderer,
                "_preparar_cena_timeline_segura",
            )

            checks[
                "preference_scene_isolation"
            ] = safe_scene

            if not safe_scene:
                findings.append(
                    StabilityFinding(
                        code="scene_isolation_missing",
                        severity="error",
                        message=(
                            "Proteção contra frames congelados ausente."
                        ),
                        component="preference_renderer",
                    )
                )

        if renderer is not None:
            audio_engine = getattr(
                renderer,
                "aaa_audio_engine",
                None,
            )

            checks[
                "audio_engine_present"
            ] = (
                audio_engine is not None
            )

            if audio_engine is None:
                findings.append(
                    StabilityFinding(
                        code="audio_engine_missing",
                        severity="error",
                        message=(
                            "AAA Audio Engine ausente."
                        ),
                        component="audio_engine",
                    )
                )

            performance_engine = getattr(
                renderer,
                "performance_engine",
                None,
            )

            checks[
                "performance_engine_present"
            ] = (
                performance_engine is not None
            )

            if performance_engine is None:
                findings.append(
                    StabilityFinding(
                        code="performance_engine_missing",
                        severity="error",
                        message=(
                            "AAA Performance Engine ausente."
                        ),
                        component="performance_engine",
                    )
                )

        return checks, findings
