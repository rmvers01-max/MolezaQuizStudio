from __future__ import annotations

from .registry import UniversalThemePackRegistry


class ThemePackDirector:
    def __init__(self):
        self.registry = (
            UniversalThemePackRegistry()
        )

    def direct(
        self,
        title: str,
        quiz_type: str,
    ) -> dict:
        pack = self.registry.select(
            title=title,
            quiz_type=quiz_type,
        )

        result = pack.to_dict()

        result["selection_reason"] = {
            "title": str(title),
            "quiz_type": str(quiz_type),
            "automatic": True,
        }

        return result
