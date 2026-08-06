from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

from .ffmpeg import FFmpegResolver
from .models import StabilityFinding


class DependencyChecker:
    REQUIRED_MODULES = (
        "PIL",
        "moviepy",
        "numpy",
        "pandas",
        "openpyxl",
        "customtkinter",
        "imageio",
        "imageio_ffmpeg",
    )

    OPTIONAL_MODULES = (
        "pytest",
    )

    def __init__(
        self,
        project_root: str | Path,
    ):
        self.project_root = Path(
            project_root
        )

    def run(self):
        findings = []
        checks = {}

        for module_name in (
            self.REQUIRED_MODULES
        ):
            available = (
                importlib.util.find_spec(
                    module_name
                )
                is not None
            )

            checks[
                f"module:{module_name}"
            ] = available

            if not available:
                findings.append(
                    StabilityFinding(
                        code="missing_python_module",
                        severity="error",
                        message=(
                            "Dependência Python obrigatória ausente."
                        ),
                        component=module_name,
                        details={
                            "python": sys.executable,
                        },
                    )
                )

        for module_name in (
            self.OPTIONAL_MODULES
        ):
            available = (
                importlib.util.find_spec(
                    module_name
                )
                is not None
            )

            checks[
                f"optional:{module_name}"
            ] = available

            if not available:
                findings.append(
                    StabilityFinding(
                        code="missing_optional_module",
                        severity="warning",
                        message=(
                            "Dependência opcional ausente."
                        ),
                        component=module_name,
                    )
                )

        resolver = FFmpegResolver(
            self.project_root
        )

        ffmpeg_path = (
            resolver.configure_environment()
        )

        checks[
            "ffmpeg"
        ] = ffmpeg_path is not None

        if ffmpeg_path is None:
            findings.append(
                StabilityFinding(
                    code="ffmpeg_not_found",
                    severity="error",
                    message=(
                        "FFmpeg não foi localizado."
                    ),
                    component="ffmpeg",
                    details={
                        "searched_project_root": (
                            str(
                                self.project_root
                            )
                        ),
                    },
                )
            )

        return checks, findings, ffmpeg_path
