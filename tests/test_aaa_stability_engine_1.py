from pathlib import Path

from core.video.stability_engine import (
    FFmpegResolver,
    StabilityFinding,
    StabilityReport,
)


def test_stability_report_serializes():
    report = StabilityReport(
        healthy=True,
        score=100,
        findings=(),
        checks={
            "ffmpeg": True,
        },
        metadata={
            "version": "1.0",
        },
    )

    data = report.to_dict()

    assert data["healthy"] is True
    assert data["score"] == 100
    assert data["checks"]["ffmpeg"] is True


def test_ffmpeg_resolver_accepts_project_binary(
    tmp_path,
):
    ffmpeg_dir = (
        tmp_path
        / "ffmpeg"
    )
    ffmpeg_dir.mkdir()

    binary = (
        ffmpeg_dir
        / "ffmpeg.exe"
    )
    binary.write_bytes(
        b"fake"
    )

    resolver = FFmpegResolver(
        tmp_path
    )

    assert resolver.resolve() == (
        binary.resolve()
    )


def test_finding_serializes():
    finding = StabilityFinding(
        code="test",
        severity="warning",
        message="Aviso",
        component="component",
    )

    data = finding.to_dict()

    assert data["severity"] == "warning"
    assert data["component"] == "component"
