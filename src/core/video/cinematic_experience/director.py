from __future__ import annotations

from .library import CinematicExperienceLibrary


class CinematicExperienceDirector:
    def __init__(self):
        self.library = CinematicExperienceLibrary()

    def choose(
        self,
        *,
        scene_kind: str,
        emotional_tone: str,
        difficulty: float,
        surprise: bool,
        pattern_break: bool,
        question_number: int,
        total_questions: int,
    ):
        tone = str(
            emotional_tone or ""
        ).lower()

        final_zone = (
            total_questions > 0
            and question_number
            >= max(total_questions - 1, 1)
        )

        if (
            scene_kind == "reveal"
            and (
                surprise
                or final_zone
                or tone == "victory"
            )
        ):
            return self.library.victory()

        if (
            scene_kind == "countdown"
            or difficulty >= 72
            or tone == "suspense"
        ):
            return self.library.suspense()

        if (
            pattern_break
            or tone in {
                "challenge",
                "competition",
            }
        ):
            return self.library.competition()

        if tone in {
            "relief",
            "calm",
        }:
            return self.library.calm()

        return self.library.discovery()
