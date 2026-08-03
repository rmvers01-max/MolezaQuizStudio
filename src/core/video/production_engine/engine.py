from __future__ import annotations
import json
from pathlib import Path
from typing import Any
from .audience_simulator import AudienceSimulator
from .data_intelligence import DataIntelligenceEngine
from .models import IntelligentProductionPlan

class IntelligentProductionEngine:
    def __init__(self):
        self.data = DataIntelligenceEngine()
        self.simulator = AudienceSimulator()

    def create_plan(self, *, title, quiz_type, questions, production_plan, question_plan, story_plan):
        profile = self.data.analyze(title=title, quiz_type=quiz_type, questions=questions)
        total = max(len(questions),1)

        if total <= 8:
            mode = "compact_high_energy"
        elif total >= 25:
            mode = "long_form_retention"
        elif quiz_type == "preferencia":
            mode = "playful_choice_show"
        elif profile.category == "flags_geography":
            mode = "visual_guess_challenge"
        else:
            mode = "balanced_family_quiz"

        curve = (
            ("curiosity","fun","challenge","victory")
            if total <= 8
            else ("curiosity","confidence","fun","challenge","suspense","relief","victory")
            if total >= 25
            else ("curiosity","fun","challenge","suspense","victory")
        )

        risks = self.simulator.simulate(
            questions=questions,
            question_plan=question_plan,
            story_plan=story_plan,
        )
        readiness = max(min(96-len(risks)*5,98),45)

        return IntelligentProductionPlan(
            title=str(title),
            quiz_type=str(quiz_type),
            total_questions=len(questions),
            content_profile=profile,
            production_mode=mode,
            pacing_strategy="adaptive" if total < 25 else "steady_with_frequent_refresh",
            emotional_curve=tuple(curve),
            retention_strategy={
                "first_question_priority":"high",
                "maximum_static_questions":3 if total <= 12 else 4,
                "risk_count":len(risks),
                "pattern_break_policy":"risk_aware",
            },
            mascot_strategy={
                "presence":"selective",
                "difficulty_reaction":"thinking",
                "surprise_reaction":"celebrate",
                "cta_reaction":"point",
            },
            audio_strategy={
                "music_energy":"high" if total <= 8 else "medium",
                "duck_on_voice":True,
                "risk_aware_whoosh":True,
            },
            visual_strategy={
                "theme_family":profile.theme_family,
                "density_mode":profile.visual_density,
                "camera_policy":"story_and_question_driven",
                "scene_graph_required":True,
                "quality_preflight_required":True,
            },
            audience_risks=risks,
            publish_readiness_score=int(readiness),
            metadata={
                "engine_version":"1.0",
                "automatic_application":False,
                "note":"Simulação editorial interna; não prevê retenção real do YouTube.",
                "source_pacing":production_plan.get("pacing_mode"),
            },
        )

    def save(self, plan, path):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(plan.to_dict(),ensure_ascii=False,indent=2),encoding="utf-8")
        return path
