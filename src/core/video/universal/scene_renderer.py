from __future__ import annotations

import math
import random
from pathlib import Path

import numpy as np
from PIL import (
    Image,
    ImageDraw,
    ImageFilter,
)
from moviepy import ImageSequenceClip

from ..attention import (
    CinematicSceneDirector,
    EyeFocusDirector,
    MascotLifeEngine,
    PatternBreakDirector,
)

from .components import (
    AnswerComponent,
    ChoiceComponent,
    ComponentContext,
    MainImageComponent,
    ProgressComponent,
    QuestionComponent,
    TimerComponent,
)
from .layouts import UniversalLayoutEngine


class UniversalSceneRenderer:
    """
    Primeiro renderizador universal real do projeto.

    Nesta Sprint ele renderiza quizzes de conhecimento.
    Preferências continuam no renderizador profissional existente.
    """

    def __init__(
        self,
        width=1280,
        height=720,
        fps=18,
    ):
        self.width = int(width)
        self.height = int(height)
        self.fps = max(
            int(fps),
            12
        )

        self.layout_engine = (
            UniversalLayoutEngine(
                width=self.width,
                height=self.height,
            )
        )

        self.eye_focus = EyeFocusDirector()
        self.cinematic_scene = (
            CinematicSceneDirector()
        )
        self.mascot_life = (
            MascotLifeEngine()
        )

        self.pattern_break = (
            PatternBreakDirector()
        )

    def create_knowledge_clip(
        self,
        question: dict,
        question_number: int,
        total_questions: int,
        duration: float,
        scene_kind: str,
        theme_pack: dict,
        countdown_value: int | None = None,
        countdown_maximum: int | None = None,
    ):
        duration = max(
            float(duration),
            0.1
        )

        total_frames = max(
            int(
                round(
                    duration * self.fps
                )
            ),
            2,
        )

        frames = []

        for index in range(
            total_frames
        ):
            time = index / self.fps
            progress = min(
                time / duration,
                1.0
            )

            frame = self.render_knowledge_frame(
                question=question,
                question_number=question_number,
                total_questions=total_questions,
                scene_kind=scene_kind,
                theme_pack=theme_pack,
                progress=progress,
                time=time,
                countdown_value=countdown_value,
                countdown_maximum=countdown_maximum,
            )

            frames.append(
                np.asarray(
                    frame.convert("RGB")
                )
            )

        return ImageSequenceClip(
            frames,
            fps=self.fps,
        ).with_duration(
            duration
        )

    def render_knowledge_frame(
        self,
        question: dict,
        question_number: int,
        total_questions: int,
        scene_kind: str,
        theme_pack: dict,
        progress: float,
        time: float,
        countdown_value: int | None = None,
        countdown_maximum: int | None = None,
    ) -> Image.Image:
        alternatives = list(
            question.get(
                "alternativas",
                []
            )
        )

        image_path = question.get(
            "imagem"
        )

        has_image = bool(
            image_path
            and Path(image_path).exists()
        )

        layout = self.layout_engine.knowledge(
            choice_count=len(
                alternatives
            ),
            has_image=has_image,
        )

        pattern_decision = (
            self.pattern_break
            .decide(
                question_number=question_number,
                total_questions=total_questions,
                scene_kind=scene_kind,
            )
        )

        image = self._background(
            theme_pack=theme_pack,
            time=time,
            scene_kind=scene_kind,
        )

        context = ComponentContext(
            width=self.width,
            height=self.height,
            theme_pack=theme_pack,
            scene_kind=scene_kind,
            question_number=question_number,
            total_questions=total_questions,
            progress=progress,
            time=time,
        )

        QuestionComponent(
            question.get(
                "pergunta",
                ""
            )
        ).render(
            image,
            layout.question,
            context,
        )

        ProgressComponent(
            current=question_number,
            total=total_questions,
        ).render(
            image,
            layout.progress,
            context,
        )

        if (
            has_image
            and layout.main_image
            is not None
        ):
            MainImageComponent(
                image_path
            ).render(
                image,
                layout.main_image,
                context,
            )

        correct_answer = str(
            question.get(
                "resposta",
                ""
            )
        ).strip()

        for index, alternative in enumerate(
            alternatives,
            start=1,
        ):
            if index > len(
                layout.choices
            ):
                break

            highlighted = (
                scene_kind == "reveal"
                and self._matches_answer(
                    alternative,
                    index,
                    correct_answer,
                )
            )

            ChoiceComponent(
                text=alternative,
                index=index,
                highlighted=highlighted,
            ).render(
                image,
                layout.choices[
                    index - 1
                ],
                context,
            )

        if (
            scene_kind == "countdown"
            and countdown_value
            is not None
        ):
            TimerComponent(
                value=countdown_value,
                maximum=max(
                    int(
                        countdown_maximum
                        or countdown_value
                    ),
                    1,
                ),
            ).render(
                image,
                layout.timer,
                context,
            )

        if scene_kind == "reveal":
            AnswerComponent(
                correct_answer
            ).render(
                image,
                layout.answer,
                context,
            )

            self._reveal_effect(
                image=image,
                progress=progress,
                theme_pack=theme_pack,
            )

        image = (
            self.pattern_break
            .apply_accent(
                image=image,
                decision=pattern_decision,
                accent_color=tuple(
                    theme_pack.get(
                        "accent_color",
                        (255, 215, 65),
                    )
                ),
                progress=progress,
            )
        )

        focus_target = (
            self.eye_focus
            .resolve_knowledge_target(
                scene_kind=scene_kind,
                has_image=has_image,
                width=self.width,
                height=self.height,
            )
        )

        image = self.eye_focus.apply(
            image,
            focus_target,
            accent_color=tuple(
                theme_pack.get(
                    "accent_color",
                    (255, 215, 65),
                )
            ),
        )

        image = self.mascot_life.render(
            image,
            scene_kind=scene_kind,
            progress=progress,
            focus=focus_target,
            intensity=(
                (
                    0.72
                    if scene_kind == "countdown"
                    else 1.0
                )
                + pattern_decision.mascot_boost
            ),
        )

        image = (
            self.cinematic_scene
            .apply_camera(
                image,
                target=focus_target,
                time=time,
                progress=progress,
                scene_kind=scene_kind,
                motion_intensity=min(
                    float(
                        theme_pack.get(
                            "motion_intensity",
                            0.50,
                        )
                    )
                    + pattern_decision.camera_boost,
                    1.0,
                ),
            )
        )

        return image

    def _background(
        self,
        theme_pack: dict,
        time: float,
        scene_kind: str,
    ) -> Image.Image:
        top = tuple(
            theme_pack.get(
                "background_top",
                (90, 55, 180),
            )
        )

        bottom = tuple(
            theme_pack.get(
                "background_bottom",
                (35, 28, 92),
            )
        )

        panel = tuple(
            theme_pack.get(
                "panel_color",
                (245, 240, 255),
            )
        )

        image = Image.new(
            "RGBA",
            (self.width, self.height),
            (*bottom, 255),
        )

        draw = ImageDraw.Draw(image)

        for y in range(self.height):
            p = y / max(
                self.height - 1,
                1
            )

            color = tuple(
                int(
                    top[i]
                    + (
                        bottom[i]
                        - top[i]
                    )
                    * p
                )
                for i in range(3)
            )

            draw.line(
                (0, y, self.width, y),
                fill=(*color, 255),
            )

        activity = float(
            theme_pack.get(
                "background_activity",
                0.5
            )
        )

        if scene_kind == "countdown":
            activity *= 0.48

        lights = Image.new(
            "RGBA",
            image.size,
            (0, 0, 0, 0),
        )

        light_draw = ImageDraw.Draw(
            lights
        )

        primary = tuple(
            theme_pack.get(
                "primary_color",
                (70, 120, 220),
            )
        )

        secondary = tuple(
            theme_pack.get(
                "secondary_color",
                (255, 95, 135),
            )
        )

        dx = int(
            50
            * math.sin(
                time * 0.35
            )
        )

        light_draw.ellipse(
            (
                -240 + dx,
                -200,
                540 + dx,
                560,
            ),
            fill=(
                *primary,
                int(45 * activity),
            ),
        )

        light_draw.ellipse(
            (
                760 - dx,
                -190,
                1500 - dx,
                550,
            ),
            fill=(
                *secondary,
                int(40 * activity),
            ),
        )

        lights = lights.filter(
            ImageFilter.GaussianBlur(
                radius=110
            )
        )

        image.alpha_composite(lights)

        draw = ImageDraw.Draw(image)

        draw.rounded_rectangle(
            (
                42,
                38,
                self.width - 42,
                self.height - 38,
            ),
            radius=38,
            fill=(*panel, 242),
            outline=(255, 255, 255, 210),
            width=4,
        )

        self._particles(
            image=image,
            time=time,
            style=theme_pack.get(
                "particle_style",
                "sparkles",
            ),
            intensity=activity,
        )

        return image

    def _particles(
        self,
        image,
        time,
        style,
        intensity,
    ):
        random.seed(4601)

        layer = Image.new(
            "RGBA",
            image.size,
            (0, 0, 0, 0),
        )

        draw = ImageDraw.Draw(layer)

        count = max(
            int(13 * intensity),
            4,
        )

        for index in range(count):
            x = (
                index * 117
                + 31
                + int(
                    12
                    * math.sin(
                        time * 0.27
                        + index
                    )
                )
            ) % self.width

            y = (
                index * 73
                + 29
                + int(
                    9
                    * math.cos(
                        time * 0.24
                        + index
                    )
                )
            ) % self.height

            alpha = int(
                50 * intensity
            )

            if style == "map_stars":
                draw.arc(
                    (
                        x - 7,
                        y - 4,
                        x + 7,
                        y + 4,
                    ),
                    start=0,
                    end=310,
                    fill=(190, 225, 255, alpha),
                    width=1,
                )
            else:
                draw.ellipse(
                    (
                        x - 3,
                        y - 3,
                        x + 3,
                        y + 3,
                    ),
                    fill=(255, 255, 255, alpha),
                )

        image.alpha_composite(layer)

    def _reveal_effect(
        self,
        image,
        progress,
        theme_pack,
    ):
        pulse = math.sin(
            min(
                max(progress, 0.0),
                1.0
            )
            * math.pi
        )

        if pulse <= 0:
            return

        accent = tuple(
            theme_pack.get(
                "accent_color",
                (255, 215, 65),
            )
        )

        layer = Image.new(
            "RGBA",
            image.size,
            (0, 0, 0, 0),
        )

        draw = ImageDraw.Draw(layer)

        draw.rounded_rectangle(
            (
                55,
                50,
                self.width - 55,
                self.height - 50,
            ),
            radius=42,
            outline=(
                *accent,
                int(105 * pulse),
            ),
            width=9,
        )

        layer = layer.filter(
            ImageFilter.GaussianBlur(
                radius=9
            )
        )

        image.alpha_composite(layer)

    def _matches_answer(
        self,
        alternative,
        index,
        answer,
    ) -> bool:
        normalized_answer = str(
            answer
        ).strip().lower()

        normalized_option = str(
            alternative
        ).strip().lower()

        return (
            normalized_answer
            == normalized_option
            or normalized_answer
            == str(index)
            or normalized_answer
            == chr(
                64 + index
            ).lower()
        )
