from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class CuriosityDecision:
    enabled: bool
    reason: str
    forced: bool
    score: float
    metadata: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "enabled": self.enabled,
            "reason": self.reason,
            "forced": self.forced,
            "score": self.score,
            "metadata": dict(self.metadata),
        }


class CuriosityDistributionDirector:
    """
    Distribui curiosidades como recompensas e Pattern Breaks.

    Regras:
    - normalmente 20% a 30% das perguntas;
    - nunca duas consecutivas;
    - respeita usar_curiosidade=True/False;
    - só mostra quando há conteúdo factual fornecido;
    - evita a primeira pergunta;
    - prioriza pontos intermediários e próximos ao final.
    """

    def __init__(self):
        self._last_selected = 0
        self._selected: list[int] = []

    def reset(self) -> None:
        self._last_selected = 0
        self._selected.clear()

    def decide(
        self,
        *,
        question: dict[str, Any],
        question_number: int,
        total_questions: int,
        quiz_type: str,
        has_pattern_break: bool = False,
        reading_load: float = 0.0,
    ) -> CuriosityDecision:
        number = max(int(question_number), 1)
        total = max(int(total_questions), 1)

        override = question.get("usar_curiosidade")
        has_content = self._has_curiosity_content(
            question=question,
            quiz_type=quiz_type,
        )

        if override is False:
            return self._decision(
                False, "disabled_by_question", True, 0.0,
                number, total, has_content
            )

        if not has_content:
            return self._decision(
                False, "no_curiosity_content", bool(override), 0.0,
                number, total, has_content
            )

        if override is True:
            self._mark(number)
            return self._decision(
                True, "forced_by_question", True, 100.0,
                number, total, has_content
            )

        if number == 1:
            return self._decision(
                False, "avoid_first_question", False, 10.0,
                number, total, has_content
            )

        if number - self._last_selected <= 1:
            return self._decision(
                False, "avoid_consecutive_curiosity", False, 15.0,
                number, total, has_content
            )

        if has_pattern_break:
            return self._decision(
                False, "avoid_after_strong_pattern_break", False, 20.0,
                number, total, has_content
            )

        if float(reading_load) >= 78:
            return self._decision(
                False, "avoid_high_reading_load", False, 25.0,
                number, total, has_content
            )

        target = self._target_count(total)
        remaining_slots = total - number + 1
        remaining_needed = max(target - len(self._selected), 0)

        score = self._position_score(number, total)

        # Distribuição determinística: pontos intermediários e finais.
        interval = max(round(total / max(target, 1)), 3)
        scheduled = (
            number >= 3
            and (
                number % interval == 0
                or number in self._preferred_positions(total)
            )
        )

        # Garante que a meta ainda possa ser alcançada no fim.
        must_select = (
            remaining_needed > 0
            and remaining_slots <= remaining_needed * 2
        )

        enabled = (
            len(self._selected) < target
            and (scheduled or must_select)
        )

        if enabled:
            self._mark(number)

        return self._decision(
            enabled,
            "scheduled_pattern_refresh" if enabled else "not_selected",
            False,
            score,
            number,
            total,
            has_content,
            target=target,
        )

    def _target_count(self, total: int) -> int:
        if total <= 4:
            return 1
        if total <= 8:
            return min(2, max(1, round(total * 0.22)))
        if total <= 15:
            return max(3, round(total * 0.24))
        if total <= 25:
            return max(4, round(total * 0.22))
        if total <= 40:
            return max(6, round(total * 0.20))
        return max(8, round(total * 0.20))

    def _preferred_positions(self, total: int) -> set[int]:
        return {
            max(round(total * 0.28), 3),
            max(round(total * 0.55), 4),
            max(round(total * 0.82), 5),
        }

    def _position_score(self, number: int, total: int) -> float:
        progress = number / max(total, 1)
        middle_bonus = 35.0 if 0.25 <= progress <= 0.85 else 15.0
        final_bonus = 20.0 if progress >= 0.75 else 0.0
        spacing_bonus = min(max(number - self._last_selected, 0) * 8.0, 32.0)
        return round(min(30.0 + middle_bonus + final_bonus + spacing_bonus, 100.0), 2)

    def _has_curiosity_content(
        self,
        *,
        question: dict[str, Any],
        quiz_type: str,
    ) -> bool:
        if quiz_type == "preferencia":
            fields = (
                "curiosidade_a",
                "curiosidade_b",
                "curiosidade",
            )
        else:
            fields = (
                "curiosidade",
                "explicacao",
            )

        return any(
            str(question.get(field, "")).strip()
            for field in fields
        )

    def _mark(self, number: int) -> None:
        self._last_selected = number
        if number not in self._selected:
            self._selected.append(number)

    def _decision(
        self,
        enabled: bool,
        reason: str,
        forced: bool,
        score: float,
        number: int,
        total: int,
        has_content: bool,
        target: int | None = None,
    ) -> CuriosityDecision:
        return CuriosityDecision(
            enabled=enabled,
            reason=reason,
            forced=forced,
            score=score,
            metadata={
                "question_number": number,
                "total_questions": total,
                "has_content": has_content,
                "selected_questions": list(self._selected),
                "target_count": (
                    target
                    if target is not None
                    else self._target_count(total)
                ),
                "distribution_version": "1.0",
            },
        )
