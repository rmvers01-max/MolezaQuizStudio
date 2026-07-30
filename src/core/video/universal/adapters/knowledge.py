from __future__ import annotations

from typing import Any

from .base import BaseQuizAdapter
from ..contracts import (
    FocusRole,
    QuizScene,
    QuizSceneType,
    SceneElement,
    UniversalQuizPlan,
)


class KnowledgeQuizAdapter(BaseQuizAdapter):
    quiz_type = "conhecimento"
    adapter_name = "KnowledgeQuizAdapter"

    def build_plan(
        self,
        title: str,
        questions: list[dict[str, Any]],
        response_time: float,
    ) -> UniversalQuizPlan:
        scenes: list[QuizScene] = [
            QuizScene(
                scene_id="opening",
                scene_type=QuizSceneType.OPENING,
                quiz_type=self.quiz_type,
                question_number=None,
                duration_hint=4.2,
                layout_id="opening_retention",
                elements=(
                    SceneElement(
                        element_id="video_title",
                        role="title",
                        content_type="text",
                        content=title,
                        focus_role=FocusRole.PRIMARY,
                    ),
                ),
            )
        ]

        for index, question in enumerate(
            questions,
            start=1,
        ):
            alternatives = list(
                question.get(
                    "alternativas",
                    []
                )
            )

            elements = [
                SceneElement(
                    element_id=f"q{index}_question",
                    role="question",
                    content_type="text",
                    content=question.get(
                        "pergunta",
                        ""
                    ),
                    focus_role=FocusRole.PRIMARY,
                ),
            ]

            image_path = question.get(
                "imagem"
            )

            if image_path:
                elements.append(
                    SceneElement(
                        element_id=f"q{index}_image",
                        role="main_image",
                        content_type="image",
                        content=image_path,
                        focus_role=FocusRole.PRIMARY,
                    )
                )

            for alt_index, alternative in enumerate(
                alternatives,
                start=1,
            ):
                elements.append(
                    SceneElement(
                        element_id=(
                            f"q{index}_option_"
                            f"{alt_index}"
                        ),
                        role="option",
                        content_type="choice",
                        content={
                            "index": alt_index,
                            "text": alternative,
                        },
                        focus_role=FocusRole.SECONDARY,
                    )
                )

            scenes.append(
                QuizScene(
                    scene_id=f"question_{index:03d}",
                    scene_type=QuizSceneType.QUESTION,
                    quiz_type=self.quiz_type,
                    question_number=index,
                    duration_hint=float(
                        response_time
                    ),
                    layout_id=(
                        "knowledge_image_choices"
                        if image_path
                        else "knowledge_choices"
                    ),
                    elements=tuple(elements),
                    metadata={
                        "correct_answer": (
                            question.get(
                                "resposta"
                            )
                        ),
                    },
                )
            )

            scenes.append(
                QuizScene(
                    scene_id=f"reveal_{index:03d}",
                    scene_type=QuizSceneType.REVEAL,
                    quiz_type=self.quiz_type,
                    question_number=index,
                    duration_hint=2.0,
                    layout_id="knowledge_reveal",
                    elements=(
                        SceneElement(
                            element_id=f"q{index}_answer",
                            role="correct_answer",
                            content_type="text",
                            content=question.get(
                                "resposta",
                                ""
                            ),
                            focus_role=FocusRole.PRIMARY,
                        ),
                    ),
                )
            )

        scenes.append(
            QuizScene(
                scene_id="outro",
                scene_type=QuizSceneType.OUTRO,
                quiz_type=self.quiz_type,
                question_number=None,
                duration_hint=5.0,
                layout_id="youtube_end_screen",
                elements=(
                    SceneElement(
                        element_id="next_video",
                        role="recommended_video",
                        content_type="youtube_end_screen_slot",
                        focus_role=FocusRole.PRIMARY,
                    ),
                ),
            )
        )

        return UniversalQuizPlan(
            quiz_type=self.quiz_type,
            title=title,
            total_questions=len(
                questions
            ),
            adapter_name=self.adapter_name,
            scenes=tuple(scenes),
            metadata={
                "render_mode": "legacy_renderer",
                "migration_stage": "contracts_only",
            },
        )
