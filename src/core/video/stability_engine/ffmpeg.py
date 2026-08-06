from __future__ import annotations

import os
import shutil
from pathlib import Path


class FFmpegResolver:
    """
    Resolve o FFmpeg priorizando o executável local do projeto.

    Ordem:
    1. pasta local do projeto;
    2. IMAGEIO_FFMPEG_EXE;
    3. FFMPEG_BINARY;
    4. PATH do Windows;
    5. imageio-ffmpeg.
    """

    def __init__(
        self,
        project_root: str | Path | None = None,
    ):
        self.project_root = (
            Path(project_root)
            if project_root is not None
            else Path.cwd()
        )

    def resolve(self) -> Path | None:
        candidates = [
            self.project_root
            / "ffmpeg"
            / "ffmpeg.exe",

            self.project_root
            / "tools"
            / "ffmpeg"
            / "ffmpeg.exe",

            self.project_root
            / "bin"
            / "ffmpeg.exe",
        ]

        for env_name in (
            "IMAGEIO_FFMPEG_EXE",
            "FFMPEG_BINARY",
        ):
            value = os.environ.get(
                env_name
            )

            if value:
                candidates.append(
                    Path(value)
                )

        system_path = shutil.which(
            "ffmpeg"
        )

        if system_path:
            candidates.append(
                Path(system_path)
            )

        try:
            import imageio_ffmpeg

            candidates.append(
                Path(
                    imageio_ffmpeg
                    .get_ffmpeg_exe()
                )
            )
        except Exception:
            pass

        for candidate in candidates:
            try:
                if (
                    candidate
                    and candidate.exists()
                    and candidate.is_file()
                ):
                    return candidate.resolve()
            except OSError:
                continue

        return None

    def configure_environment(
        self,
    ) -> Path | None:
        resolved = self.resolve()

        if resolved is None:
            return None

        path = str(resolved)

        os.environ[
            "IMAGEIO_FFMPEG_EXE"
        ] = path

        os.environ[
            "FFMPEG_BINARY"
        ] = path

        return resolved
