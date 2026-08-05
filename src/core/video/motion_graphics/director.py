from __future__ import annotations
from .models import MotionGraphicsPlan
from .presets import MotionPresetLibrary

class AAAMotionGraphicsDirector:
    TRANSITIONS = {
        "preference":"split_flash","flags_geography":"flag_wipe",
        "animals":"leaf_wipe","food":"food_pop","sports":"speed_wipe",
        "characters":"mystery_flash","general_knowledge":"light_wipe",
    }
    def __init__(self):
        self.library = MotionPresetLibrary()

    def create_plan(self, *, category, scene_kind, question_number, fps=24):
        category = category if category in self.TRANSITIONS else "general_knowledge"
        return MotionGraphicsPlan(
            scene_kind=str(scene_kind), category=category,
            question_number=max(int(question_number),0),
            title_preset=self.library.title(category),
            card_preset=self.library.card(category),
            counter_preset=self.library.counter(category),
            reveal_preset=self.library.reveal(category),
            badge_preset=self.library.badge(category),
            progress_preset=self.library.progress(category),
            transition_style=self.TRANSITIONS[category],
            fps=max(int(fps),18),
            metadata={"motion_graphics_version":"1.0","theme_aware":True},
        )
