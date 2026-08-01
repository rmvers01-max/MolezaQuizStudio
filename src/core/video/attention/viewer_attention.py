from __future__ import annotations

import json
from pathlib import Path


class ViewerAttentionAnalyzer:
    """
    Cria uma auditoria técnica do ritmo planejado.

    Não promete prever o comportamento real do público.
    A pontuação serve para detectar repetição, falta de mudança
    visual e excesso de estímulo antes da exportação.
    """

    def analyze(
        self,
        *,
        total_questions: int,
        pattern_break_questions: list[int],
        theme_pack: dict,
    ) -> dict:
        total = max(
            int(total_questions),
            1,
        )

        breaks = sorted(
            set(
                int(value)
                for value in pattern_break_questions
                if int(value) > 0
            )
        )

        score = 100
        alerts = []

        if total >= 8 and not breaks:
            score -= 18
            alerts.append(
                "Nenhuma quebra de padrão foi planejada."
            )

        maximum_gap = self._maximum_gap(
            total,
            breaks,
        )

        if maximum_gap > 6:
            score -= 12
            alerts.append(
                "Há um intervalo longo sem mudança visual."
            )

        activity = float(
            theme_pack.get(
                "background_activity",
                0.50,
            )
        )

        motion = float(
            theme_pack.get(
                "motion_intensity",
                0.50,
            )
        )

        if activity > 0.78:
            score -= 8
            alerts.append(
                "A atividade do fundo pode competir com a leitura."
            )

        if motion > 0.80:
            score -= 8
            alerts.append(
                "A intensidade da câmera pode estar excessiva."
            )

        score = max(
            min(score, 100),
            0,
        )

        return {
            "score": score,
            "classification": (
                "excelente"
                if score >= 92
                else "boa"
                if score >= 82
                else "revisar"
            ),
            "total_questions": total,
            "pattern_break_questions": breaks,
            "maximum_gap": maximum_gap,
            "alerts": alerts,
            "note": (
                "Pontuação técnica interna; "
                "não representa retenção real do YouTube."
            ),
        }

    def save(
        self,
        report: dict,
        path,
    ) -> Path:
        path = Path(path)

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        path.write_text(
            json.dumps(
                report,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return path

    def _maximum_gap(
        self,
        total: int,
        breaks: list[int],
    ) -> int:
        points = [
            1,
            *breaks,
            total,
        ]

        return max(
            (
                points[index + 1]
                - points[index]
                for index in range(
                    len(points) - 1
                )
            ),
            default=total,
        )
