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


class PreferenceQuizAdapter(BaseQuizAdapter):
    quiz_type = "preferencia"
    adapter_name = "PreferenceQuizAdapter"

    def build_plan(
        self,
        title: str,
        questions: list[dict[str, Any]],
        response_time: float,
    ) -> UniversalQuizPlan:
        scenes: list[QuizScene] = []

        scenes.append(
            QuizScene(
                scene_id="opening",
                scene_type=QuizSceneType.OPENING,
                quiz_type=self.quiz_type,
                question_number=None,
                duration_hint=4.2,
                layout_id="opening_retention",
                elements=(
                    SceneElement(
                        element_id="channel_brand",
                        role="brand",
                        content_type="text",
                        content="Moleza Quiz",
                        focus_role=FocusRole.SECONDARY,
                    ),
                    SceneElement(
                        element_id="video_title",
                        role="title",
                        content_type="text",
                        content=title,
                        focus_role=FocusRole.PRIMARY,
                    ),
                ),
            )
        )

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

            option_a = (
                alternatives[0]
                if alternatives
                else ""
            )

            option_b = (
                alternatives[1]
                if len(alternatives) > 1
                else ""
            )

            common_elements = (
                SceneElement(
                    element_id=f"q{index}_title",
                    role="question",
                    content_type="text",
                    content=question.get(
                        "pergunta",
                        ""
                    ),
                    focus_role=FocusRole.PRIMARY,
                ),
                SceneElement(
                    element_id=f"q{index}_option_a",
                    role="option_a",
                    content_type="choice",
                    content={
                        "text": option_a,
                        "image": question.get(
                            "imagem_a"
                        ),
                    },
                    focus_role=FocusRole.PRIMARY,
                ),
                SceneElement(
                    element_id=f"q{index}_or",
                    role="separator",
                    content_type="badge",
                    content="OU",
                    focus_role=FocusRole.SECONDARY,
                ),
                SceneElement(
                    element_id=f"q{index}_option_b",
                    role="option_b",
                    content_type="choice",
                    content={
                        "text": option_b,
                        "image": question.get(
                            "imagem_b"
                        ),
                    },
                    focus_role=FocusRole.PRIMARY,
                ),
            )

            scenes.append(
                QuizScene(
                    scene_id=f"question_{index:03d}",
                    scene_type=QuizSceneType.QUESTION,
                    quiz_type=self.quiz_type,
                    question_number=index,
                    duration_hint=0.9,
                    layout_id="preference_dual_cards",
                    elements=common_elements,
                    metadata={
                        "answer_mode": "viewer_choice",
                        "has_correct_answer": False,
                    },
                )
            )

            scenes.append(
                QuizScene(
                    scene_id=f"countdown_{index:03d}",
                    scene_type=QuizSceneType.COUNTDOWN,
                    quiz_type=self.quiz_type,
                    question_number=index,
                    duration_hint=float(
                        response_time
                    ),
                    layout_id="preference_dual_cards",
                    elements=common_elements
                    + (
                        SceneElement(
                            element_id=f"q{index}_timer",
                            role="timer",
                            content_type="countdown",
                            content=int(
                                response_time
                            ),
                            focus_role=FocusRole.SECONDARY,
                        ),
                    ),
                    metadata={
                        "answer_mode": "viewer_choice",
                    },
                )
            )

            scenes.append(
                QuizScene(
                    scene_id=f"reveal_{index:03d}",
                    scene_type=QuizSceneType.REVEAL,
                    quiz_type=self.quiz_type,
                    question_number=index,
                    duration_hint=1.9,
                    layout_id="preference_result",
                    elements=(
                        SceneElement(
                            element_id=f"q{index}_result_title",
                            role="result_title",
                            content_type="text",
                            content="QUAL VOCÊ ESCOLHEU?",
                            focus_role=FocusRole.PRIMARY,
                        ),
                        SceneElement(
                            element_id=f"q{index}_mascot",
                            role="mascot",
                            content_type="character",
                            content="celebrate",
                            focus_role=FocusRole.SECONDARY,
                        ),
                    ),
                    metadata={
                        "correct_answer": None,
                        "comment_prompt": True,
                    },
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
                    SceneElement(
                        element_id="subscribe",
                        role="subscribe",
                        content_type="youtube_end_screen_slot",
                        focus_role=FocusRole.SECONDARY,
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
                "render_mode": "existing_renderer",
                "migration_stage": "contracts_only",
            },
        )
