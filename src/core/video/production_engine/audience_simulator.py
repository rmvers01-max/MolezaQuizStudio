from __future__ import annotations
from typing import Any
from .models import AudienceRisk

class AudienceSimulator:
    def simulate(self, *, questions: list[dict[str, Any]], question_plan: dict[str, Any], story_plan: dict[str, Any]):
        directions = {int(x.get("question_number",0)):x for x in question_plan.get("questions",[])}
        beats = {int(x.get("question_number",0)):x for x in story_plan.get("beats",[])}
        risks, previous, streak = [], None, 0

        for number, q in enumerate(questions, start=1):
            signature = (
                len(str(q.get("pergunta","")))//20,
                len(q.get("alternativas",[])),
                bool(q.get("imagem") or q.get("imagem_a") or q.get("imagem_b")),
            )
            streak = streak + 1 if signature == previous else 1
            previous = signature
            direction = directions.get(number,{})
            surprise = bool(direction.get("surprise_moment",False))
            reading = float(direction.get("reading_score",0))

            if streak >= 4 and not surprise:
                risks.append(AudienceRisk(
                    max(number-3,1), number, 78.0, "visual_repetition",
                    "Quatro perguntas consecutivas possuem estrutura visual semelhante.",
                    {"force_pattern_break":True,"camera_variant":"lateral_push","mascot_reaction":"wave"},
                ))
                streak = 0

            if reading >= 78 and number <= 3:
                risks.append(AudienceRisk(
                    number, number, 74.0, "early_cognitive_load",
                    "Uma das primeiras perguntas exige muita leitura.",
                    {"move_question_later":True,"entry_duration_delta":0.15},
                ))

            chapter = str(beats.get(number,{}).get("chapter",""))
            camera = float(direction.get("camera_intensity",.5))
            if number >= 5 and camera < .48 and chapter not in {"climax","grand_finale"}:
                risks.append(AudienceRisk(
                    number, number, 62.0, "low_motion_point",
                    "A pergunta possui baixa variação visual em um ponto intermediário.",
                    {"motion_boost":0.08},
                ))

        return tuple(risks)
