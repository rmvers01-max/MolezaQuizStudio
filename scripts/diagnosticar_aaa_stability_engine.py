from __future__ import annotations

from pathlib import Path

from core.video import VideoGenerator


generator = VideoGenerator()

stability = (
    generator.core_engine.resolve(
        "stability_engine"
    )
)

report = stability.validate(
    video_generator=generator
)

print("AAA STABILITY ENGINE")
print("healthy:", report.healthy)
print("score:", report.score)

print("\nFFMPEG:")
print(
    report.metadata.get(
        "ffmpeg_path"
    )
)

print("\nCHECKS:")
for name, value in sorted(
    report.checks.items()
):
    print(
        f"{name}:",
        value,
    )

print("\nFINDINGS:")
for finding in report.findings:
    print(
        finding.severity,
        finding.component,
        finding.message,
    )

assert report.healthy is True
assert report.checks["ffmpeg"] is True
assert (
    report.checks[
        "preference_scene_isolation"
    ]
    is True
)
assert (
    report.checks[
        "audio_engine_present"
    ]
    is True
)

print("\nAAA STABILITY ENGINE OK")
