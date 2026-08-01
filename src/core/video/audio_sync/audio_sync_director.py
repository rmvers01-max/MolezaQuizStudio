from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from moviepy import AudioFileClip


@dataclass(frozen=True, slots=True)
class AudioCue:
    cue_type: str
    start: float
    volume: float
    path: Path


class AudioSyncDirector:
    """
    Sincroniza efeitos sonoros opcionais às ações visuais.

    O módulo é tolerante a arquivos ausentes. Caso o usuário ainda
    não possua os efeitos, o vídeo é gerado sem interrupção.
    """

    CANDIDATES = {
        "question_in": (
            "assets/sfx/question_in.wav",
            "assets/sfx/question_in.mp3",
            "assets/sfx/card_in.wav",
            "assets/sfx/card_in.mp3",
            "assets/sounds/question_in.wav",
        ),
        "tick": (
            "assets/sfx/tick.wav",
            "assets/sfx/tick.mp3",
            "assets/sounds/tick.wav",
        ),
        "reveal": (
            "assets/sfx/reveal.wav",
            "assets/sfx/reveal.mp3",
            "assets/sfx/correct.wav",
            "assets/sfx/correct.mp3",
            "assets/sounds/reveal.wav",
        ),
        "pattern_break": (
            "assets/sfx/pattern_break.wav",
            "assets/sfx/pattern_break.mp3",
            "assets/sfx/whoosh.wav",
            "assets/sfx/whoosh.mp3",
        ),
    }

    def build_question_cues(
        self,
        *,
        project_root,
        question_number: int,
        total_questions: int,
        question_start: float,
        question_duration: float,
        response_time: int,
        reveal_duration: float,
    ) -> list[AudioCue]:
        root = Path(project_root)

        cues = []

        question_path = self._find(
            root,
            "question_in",
        )

        if question_path is not None:
            cues.append(
                AudioCue(
                    cue_type="question_in",
                    start=float(
                        question_start
                    ),
                    volume=0.36,
                    path=question_path,
                )
            )

        interval = (
            3
            if total_questions <= 10
            else 4
            if total_questions <= 24
            else 5
        )

        is_pattern_break = (
            question_number > 1
            and question_number
            % interval == 0
        )

        if is_pattern_break:
            pattern_path = self._find(
                root,
                "pattern_break",
            )

            if pattern_path is not None:
                cues.append(
                    AudioCue(
                        cue_type="pattern_break",
                        start=float(
                            question_start
                            + 0.08
                        ),
                        volume=0.32,
                        path=pattern_path,
                    )
                )

        tick_path = self._find(
            root,
            "tick",
        )

        if tick_path is not None:
            countdown_start = (
                question_start
                + question_duration
            )

            for offset in range(
                max(
                    int(response_time),
                    0
                )
            ):
                cues.append(
                    AudioCue(
                        cue_type="tick",
                        start=float(
                            countdown_start
                            + offset
                        ),
                        volume=0.20,
                        path=tick_path,
                    )
                )

        reveal_path = self._find(
            root,
            "reveal",
        )

        if reveal_path is not None:
            reveal_start = (
                question_start
                + question_duration
                + response_time
            )

            cues.append(
                AudioCue(
                    cue_type="reveal",
                    start=float(
                        reveal_start
                    ),
                    volume=0.38,
                    path=reveal_path,
                )
            )

        return cues

    def create_clips(
        self,
        cues: list[AudioCue],
    ):
        clips = []

        for cue in cues:
            try:
                clip = (
                    AudioFileClip(
                        str(cue.path)
                    )
                    .with_volume_scaled(
                        cue.volume
                    )
                    .with_start(
                        cue.start
                    )
                )
            except Exception:
                continue

            clips.append(clip)

        return clips

    def _find(
        self,
        project_root: Path,
        cue_type: str,
    ) -> Path | None:
        for relative in self.CANDIDATES.get(
            cue_type,
            ()
        ):
            candidates = (
                Path(relative),
                project_root / relative,
            )

            for candidate in candidates:
                if candidate.exists():
                    return candidate

        return None
