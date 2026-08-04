from __future__ import annotations
from typing import Any
from .models import KnowledgeVisualProfile

class AAAKnowledgeVisualDirector:
    CATEGORY_PRESETS = {
        "flags_geography": ("visual_identity","hero_flag","radial_compass","country_reveal",(255,215,65),(68,138,225),"world_gradient"),
        "animals": ("discovery","hero_animal","paw_countdown","nature_reveal",(255,225,92),(69,173,122),"nature_gradient"),
        "food": ("playful","hero_food","plate_countdown","flavor_reveal",(255,220,80),(244,104,89),"food_gradient"),
        "sports": ("competition","hero_sport","scoreboard_countdown","score_reveal",(255,224,70),(58,150,230),"arena_gradient"),
        "characters": ("mystery","hero_character","mystery_countdown","character_reveal",(255,205,86),(164,82,220),"mystery_gradient"),
        "general_knowledge": ("clean_challenge","adaptive","neon_ring","answer_spotlight",(255,215,65),(101,61,185),"moleza_gradient"),
    }

    def choose(self, *, question: dict[str, Any], question_number: int,
               total_questions: int, category: str,
               curiosity_selected: bool, pattern_break: bool=False):
        preset = self.CATEGORY_PRESETS.get(
            category, self.CATEGORY_PRESETS["general_knowledge"]
        )
        question_style, image_mode, countdown_style, reveal_style, accent, secondary, background = preset
        alternatives = list(question.get("alternativas", []))
        layout = "two_by_two" if len(alternatives) <= 4 else "stacked"
        has_image = bool(question.get("imagem") or question.get("imagem_principal"))
        final_zone = total_questions > 0 and question_number >= max(total_questions - 2, 1)
        try:
            difficulty = float(question.get("dificuldade_score", question.get("dificuldade", 50)) or 50)
        except (TypeError, ValueError):
            difficulty = 50.0
        motion = 0.68 + (0.08 if difficulty >= 70 else 0) + (0.08 if pattern_break else 0) + (0.06 if final_zone else 0)
        explanation = str(question.get("explicacao", "")).strip()

        return KnowledgeVisualProfile(
            code=f"knowledge_v2_{category}",
            category=category,
            question_style=question_style,
            options_layout=layout,
            image_mode=image_mode if has_image else "none",
            countdown_style=countdown_style,
            reveal_style=reveal_style,
            accent_color=accent,
            secondary_color=secondary,
            background_mode=background,
            motion_intensity=min(motion, 0.92),
            particle_intensity=0.62 if final_zone else 0.34,
            show_explanation=bool(explanation),
            curiosity_selected=bool(curiosity_selected),
            metadata={
                "renderer_version": "2.0",
                "question_number": question_number,
                "total_questions": total_questions,
                "difficulty": difficulty,
                "final_zone": final_zone,
                "pattern_break": bool(pattern_break),
                "has_image": has_image,
                "correct_answer_required": True,
            },
        )
