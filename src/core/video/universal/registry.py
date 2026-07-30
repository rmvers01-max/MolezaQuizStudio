from __future__ import annotations

from .adapters.base import BaseQuizAdapter
from .adapters.knowledge import KnowledgeQuizAdapter
from .adapters.preference import PreferenceQuizAdapter


class UniversalQuizAdapterRegistry:
    def __init__(self):
        self._adapters: dict[
            str,
            BaseQuizAdapter
        ] = {
            "preferencia": (
                PreferenceQuizAdapter()
            ),
            "conhecimento": (
                KnowledgeQuizAdapter()
            ),
        }

    def get(
        self,
        quiz_type: str,
    ) -> BaseQuizAdapter:
        return self._adapters.get(
            str(
                quiz_type
            ).strip().lower(),
            self._adapters[
                "conhecimento"
            ],
        )

    def registered_types(
        self,
    ) -> tuple[str, ...]:
        return tuple(
            self._adapters.keys()
        )
