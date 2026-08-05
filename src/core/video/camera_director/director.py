from __future__ import annotations

from .library import AAACameraMoveLibrary
from .models import CameraPlan


class AAACameraDirector:
    def __init__(self):
        self.library = AAACameraMoveLibrary()

    def create_plan(
        self,
        *,
        scene_kind: str,
        category: str,
        question_number: int,
        difficulty: float,
        emotional_tone: str,
        pattern_break: bool,
        surprise: bool,
        focus_x: float,
        focus_y: float,
    ) -> CameraPlan:
        tone = str(emotional_tone or "").lower()
        category = str(category or "general_knowledge")

        if scene_kind == "reveal" and surprise:
            primary = self.library.hero_reveal()
        elif scene_kind == "reveal" and tone in {"victory", "celebration"}:
            primary = self.library.hero_reveal()
        elif scene_kind == "countdown" or float(difficulty) >= 72:
            primary = self.library.suspense_focus()
        elif pattern_break or tone in {"challenge", "competition"}:
            primary = self.library.competition_push()
        elif category == "preference":
            primary = self.library.choice_balance()
        elif tone in {"relief", "calm"}:
            primary = self.library.calm_drift()
        else:
            primary = self.library.discovery_push()

        return CameraPlan(
            scene_kind=str(scene_kind),
            category=category,
            question_number=max(int(question_number), 0),
            primary_move=primary,
            fallback_move=self.library.static_safe(),
            target_x=max(min(float(focus_x), 1.0), 0.0),
            target_y=max(min(float(focus_y), 1.0), 0.0),
            safe_motion_limit=0.92,
            metadata={
                "camera_director_version": "2.0",
                "difficulty": float(difficulty),
                "emotional_tone": tone,
                "pattern_break": bool(pattern_break),
                "surprise": bool(surprise),
            },
        )
