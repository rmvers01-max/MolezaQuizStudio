from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from ..contracts import UniversalQuizPlan


class BaseQuizAdapter(ABC):
    quiz_type = "conhecimento"
    adapter_name = "BaseQuizAdapter"

    @abstractmethod
    def build_plan(
        self,
        title: str,
        questions: list[dict[str, Any]],
        response_time: float,
    ) -> UniversalQuizPlan:
        raise NotImplementedError
