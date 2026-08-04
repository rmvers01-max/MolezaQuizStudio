from __future__ import annotations
from typing import Any

class KnowledgeRevealPlanner:
    def create(self, *, question: dict[str, Any], profile):
        explanation = str(question.get("explicacao", "")).strip()
        return {
            "correct_index": question.get(
                "resposta_correta_indice",
                question.get("indice_resposta_correta", question.get("correta")),
            ),
            "answer_text": str(question.get(
                "resposta", question.get("resposta_correta", "")
            )).strip(),
            "explanation": explanation,
            "reveal_style": profile.reveal_style,
            "highlight_correct": True,
            "dim_incorrect": True,
            "show_red_cross": False,
            "correct_glow": "golden_soft",
            "incorrect_opacity": 0.58,
            "answer_badge": "RESPOSTA",
            "show_explanation": bool(explanation),
        }
