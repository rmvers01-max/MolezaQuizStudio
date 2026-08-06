from __future__ import annotations

import json
from pathlib import Path

from .dependencies import DependencyChecker
from .guards import RegressionGuard
from .models import StabilityReport


class AAAStabilityEngine:
    def __init__(
        self,
        project_root: str | Path,
    ):
        self.project_root = Path(
            project_root
        )

        self.dependency_checker = (
            DependencyChecker(
                self.project_root
            )
        )

        self.regression_guard = (
            RegressionGuard()
        )

        self.last_report = None
        self.ffmpeg_path = None

    def validate(
        self,
        *,
        video_generator=None,
    ) -> StabilityReport:
        dependency_checks, dependency_findings, ffmpeg_path = (
            self.dependency_checker.run()
        )

        guard_checks, guard_findings = (
            self.regression_guard.run(
                video_generator=(
                    video_generator
                )
            )
        )

        findings = (
            list(
                dependency_findings
            )
            + list(
                guard_findings
            )
        )

        checks = {
            **dependency_checks,
            **guard_checks,
        }

        score = 100

        for finding in findings:
            score -= (
                20
                if finding.severity
                == "error"
                else 5
            )

        report = StabilityReport(
            healthy=not any(
                finding.severity
                == "error"
                for finding in findings
            ),
            score=max(
                score,
                0,
            ),
            findings=tuple(
                findings
            ),
            checks=checks,
            metadata={
                "stability_engine_version": "1.0",
                "project_root": str(
                    self.project_root
                ),
                "ffmpeg_path": (
                    str(ffmpeg_path)
                    if ffmpeg_path
                    is not None
                    else None
                ),
            },
        )

        self.last_report = report
        self.ffmpeg_path = ffmpeg_path

        return report

    def ensure_healthy(
        self,
        *,
        video_generator=None,
    ) -> StabilityReport:
        report = self.validate(
            video_generator=(
                video_generator
            )
        )

        if not report.healthy:
            errors = [
                finding
                for finding
                in report.findings
                if finding.severity
                == "error"
            ]

            message = "; ".join(
                (
                    f"{finding.component}: "
                    f"{finding.message}"
                )
                for finding in errors
            )

            raise RuntimeError(
                "AAA Stability Engine bloqueou "
                "a geração: "
                + message
            )

        return report

    def save_report(
        self,
        path,
    ):
        if self.last_report is None:
            return None

        path = Path(path)
        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        path.write_text(
            json.dumps(
                self.last_report.to_dict(),
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return path
