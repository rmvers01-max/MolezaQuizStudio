from __future__ import annotations

from typing import Any

from core.brand import BrandDirector
from core.retention import RetentionDirector
from core.video.theme_packs import ThemePackDirector

from .contracts import (
    FocusRole,
    QuizScene,
    QuizSceneType,
    SceneElement,
    UniversalQuizPlan,
)


class UniversalCreativeDirector:
    """
    Conecta o Universal Quiz Engine aos diretores já existentes.

    Nesta etapa, ele não substitui os renderizadores.
    Ele cria uma direção criativa universal que poderá ser
    consumida por qualquer formato de quiz nas próximas fases.
    """

    def __init__(
        self,
        brand_code: str = "moleza_quiz",
    ):
        self.brand_director = BrandDirector(
            brand_code
        )

        self.retention_director = (
            RetentionDirector()
        )

        self.theme_pack_director = (
            ThemePackDirector()
        )

    def direct(
        self,
        plan: UniversalQuizPlan,
    ) -> dict[str, Any]:
        brand_direction = (
            self.brand_director
            .criar_direcao_video(
                titulo_quiz=plan.title,
                total_perguntas=(
                    plan.total_questions
                ),
            )
        )

        retention_plan = (
            self.retention_director
            .criar_plano_video(
                titulo=plan.title,
                total_perguntas=(
                    plan.total_questions
                ),
                brand_direction=(
                    brand_direction
                ),
            )
        )

        theme_pack = (
            self.theme_pack_director
            .direct(
                title=plan.title,
                quiz_type=plan.quiz_type,
            )
        )

        directed_scenes = [
            self._direct_scene(
                scene=scene,
                retention_plan=(
                    retention_plan
                ),
                theme_pack=theme_pack,
            )
            for scene in plan.scenes
        ]

        return {
            "quiz_type": plan.quiz_type,
            "title": plan.title,
            "total_questions": (
                plan.total_questions
            ),
            "adapter_name": (
                plan.adapter_name
            ),
            "brand_direction": (
                brand_direction
            ),
            "retention_plan": (
                retention_plan
            ),
            "theme_pack": dict(
                theme_pack
            ),
            "scenes": directed_scenes,
            "metadata": {
                **dict(plan.metadata),
                "creative_direction_stage": (
                    "universal_36_2"
                ),
                "renderers_unchanged": True,
            },
        }

    def _direct_scene(
        self,
        scene: QuizScene,
        retention_plan: dict,
        theme_pack,
    ) -> dict[str, Any]:
        question_decision = {}

        if scene.question_number:
            question_decision = (
                self.retention_director
                .decisao_pergunta(
                    retention_plan,
                    scene.question_number,
                )
            )

        focus_map = self._build_focus_map(
            scene.elements
        )

        density = self._content_density(
            scene.elements
        )

        motion_profile = (
            self._motion_profile(
                scene=scene,
                density=density,
                question_decision=(
                    question_decision
                ),
            )
        )

        mascot_direction = (
            self._mascot_direction(
                scene=scene,
                focus_map=focus_map,
                question_decision=(
                    question_decision
                ),
            )
        )

        return {
            **scene.to_dict(),
            "creative_direction": {
                "focus_map": focus_map,
                "content_density": density,
                "motion_profile": (
                    motion_profile
                ),
                "mascot_direction": (
                    mascot_direction
                ),
                "theme_code": theme_pack["code"],
                "theme_name": theme_pack["name"],
                "retention_decision": (
                    question_decision
                ),
            },
        }

    def _build_focus_map(
        self,
        elements: tuple[
            SceneElement,
            ...
        ],
    ) -> dict[str, list[str]]:
        result = {
            "primary": [],
            "secondary": [],
            "support": [],
            "decorative": [],
        }

        for element in elements:
            key = (
                element.focus_role.value
            )

            result[key].append(
                element.element_id
            )

        return result

    def _content_density(
        self,
        elements: tuple[
            SceneElement,
            ...
        ],
    ) -> float:
        score = 0.0

        weights = {
            "text": 0.11,
            "choice": 0.18,
            "image": 0.22,
            "badge": 0.06,
            "countdown": 0.08,
            "character": 0.10,
            "youtube_end_screen_slot": 0.16,
        }

        for element in elements:
            score += weights.get(
                element.content_type,
                0.08,
            )

        return round(
            min(score, 1.0),
            2,
        )

    def _motion_profile(
        self,
        scene: QuizScene,
        density: float,
        question_decision: dict,
    ) -> dict[str, Any]:
        pattern_break = bool(
            question_decision.get(
                "pattern_break",
                False
            )
        )

        base_intensity = float(
            question_decision.get(
                "intensidade_fx",
                0.55
            )
        )

        if density >= 0.75:
            background_intensity = (
                base_intensity * 0.45
            )

        elif density >= 0.50:
            background_intensity = (
                base_intensity * 0.65
            )

        else:
            background_intensity = (
                base_intensity * 0.82
            )

        camera_modes = {
            QuizSceneType.OPENING: (
                "impact_push"
            ),
            QuizSceneType.QUESTION: (
                "micro_breath"
            ),
            QuizSceneType.COUNTDOWN: (
                "stable_focus"
            ),
            QuizSceneType.REVEAL: (
                "celebration_push"
            ),
            QuizSceneType.CTA: (
                "attention_shift"
            ),
            QuizSceneType.OUTRO: (
                "end_screen_hold"
            ),
        }

        return {
            "camera_mode": (
                camera_modes.get(
                    scene.scene_type,
                    "micro_breath",
                )
            ),
            "background_intensity": round(
                min(
                    background_intensity
                    + (
                        0.08
                        if pattern_break
                        else 0.0
                    ),
                    1.0,
                ),
                3,
            ),
            "pattern_break": pattern_break,
            "visual_change_required": (
                pattern_break
                or scene.scene_type
                in {
                    QuizSceneType.OPENING,
                    QuizSceneType.REVEAL,
                    QuizSceneType.OUTRO,
                }
            ),
            "motion_priority": (
                "focus"
                if density >= 0.65
                else "atmosphere"
            ),
        }

    def _mascot_direction(
        self,
        scene: QuizScene,
        focus_map: dict[str, list[str]],
        question_decision: dict,
    ) -> dict[str, Any]:
        primary = focus_map.get(
            "primary",
            []
        )

        pose = question_decision.get(
            "mascote_pose_entrada",
            "idle",
        )

        target = (
            primary[0]
            if primary
            else None
        )

        if scene.scene_type == (
            QuizSceneType.OPENING
        ):
            pose = "wave"

        elif scene.scene_type == (
            QuizSceneType.COUNTDOWN
        ):
            pose = "thinking"

        elif scene.scene_type == (
            QuizSceneType.REVEAL
        ):
            pose = "celebrate"

        elif scene.scene_type == (
            QuizSceneType.OUTRO
        ):
            pose = "point_left"

        return {
            "pose": pose,
            "look_target": target,
            "never_cover_primary": True,
            "screen_position": (
                "bottom_right"
            ),
        }
