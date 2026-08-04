from __future__ import annotations

import math
import random
from pathlib import Path

import numpy as np
from PIL import (
    ImageEnhance,
    Image,
    ImageDraw,
    ImageFilter,
)
from moviepy import ImageSequenceClip

from ..identity_engine import AAAIdentityEngine
from ..theme_experience import (
    ThemeSpecificCompositor,
    ThemeSpecificExperienceDirector,
)

from ..cinematic_experience import (
    CinematicExperienceCompositor,
    CinematicExperienceDirector,
)

from ..mascot_actor import (
    MascotActorAnimator,
    MascotPerformanceDirector,
)

from ..scene_graph import (
    KnowledgeSceneGraphFactory,
    SafeAreaResolver,
    SceneGraphDiagnostics,
    SceneGraphFocusResolver,
    SceneGraphValidator,
    SceneRenderContext,
    ScopedMaterialRenderer,
    SceneLayoutIntelligence,
    SceneGraphQualityDirector,
)

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

        self.scene_graph_factory = KnowledgeSceneGraphFactory(
            self.width,
            self.height,
        )
        self.scene_graph_validator = SceneGraphValidator()
        self.scene_graph_resolver = SafeAreaResolver()
        self.scene_graph_diagnostics = SceneGraphDiagnostics()
        self.scene_graph_focus = SceneGraphFocusResolver()
        self.scoped_materials = ScopedMaterialRenderer()
        self.layout_intelligence = SceneLayoutIntelligence()
        self.quality_director = SceneGraphQualityDirector()
        self.last_scene_graph_report = None
        self.last_layout_intelligence_report = None
        self.last_quality_preflight_report = None

        self.eye_focus = EyeFocusDirector()
        self.cinematic_scene = (
            CinematicSceneDirector()
        )
        self.mascot_life = (
            MascotLifeEngine()
        )
        self.mascot_performance_director = MascotPerformanceDirector()
        self.mascot_actor_animator = MascotActorAnimator()
        self.last_mascot_performance = None

        self.cinematic_experience_director = (
            CinematicExperienceDirector()
        )

        self.cinematic_experience_compositor = (
            CinematicExperienceCompositor()
        )

        self.last_cinematic_experience = None
        self.identity_engine = AAAIdentityEngine()
        self.identity_plan = {}
        self.last_identity_evaluation = None
        self.knowledge_profile = {}
        self.knowledge_reveal_plan = {}
        self.theme_experience_director = ThemeSpecificExperienceDirector()
        self.theme_specific_compositor = ThemeSpecificCompositor()
        self.last_theme_experience = None

        self.pattern_break = (
            PatternBreakDirector()
        )

        self.question_direction_plan = None
        self.story_arc_plan = None
        self.ipe_execution_plan = None

        self.execution_settings = {
            "pattern_breaks_enabled": True,
            "pattern_break_interval": 4,
            "pattern_break_intensity": 0.82,
            "mascot_enabled": True,
            "mascot_intensity": 0.80,
        }

    def configure_knowledge_profile(self, profile, reveal_plan):
        self.knowledge_profile = dict(profile or {})
        self.knowledge_reveal_plan = dict(reveal_plan or {})

    def configure_identity(self, plan):
        self.identity_plan = plan.to_dict() if hasattr(plan, "to_dict") else dict(plan or {})

    def configure_ipe_execution(
        self,
        plan,
    ):
        self.ipe_execution_plan = plan
        adjustments = getattr(plan, "global_adjustments", {})
        interval_delta = int(adjustments.get("pattern_break_interval_delta", 0))
        current_interval = int(self.execution_settings.get("pattern_break_interval", 4))
        self.execution_settings["pattern_break_interval"] = max(current_interval + interval_delta, 2)
        self.execution_settings["pattern_break_intensity"] = min(
            float(self.execution_settings.get("pattern_break_intensity", .82))
            + float(adjustments.get("pattern_break_intensity_delta", 0.0)),
            1.0,
        )

    def _ipe_directive(self, number):
        if self.ipe_execution_plan is None:
            return None
        if hasattr(self.ipe_execution_plan, "question"):
            return self.ipe_execution_plan.question(number)
        return None

    def configure_story_arc(
        self,
        plan,
    ):
        self.story_arc_plan = plan

    def _story_beat(
        self,
        question_number,
    ):
        if self.story_arc_plan is None:
            return None

        if hasattr(
            self.story_arc_plan,
            "beat"
        ):
            return self.story_arc_plan.beat(
                question_number
            )

        return None

    def configure_question_direction(
        self,
        plan,
    ):
        self.question_direction_plan = plan

    def _question_direction(
        self,
        question_number,
    ):
        if self.question_direction_plan is None:
            return None

        if hasattr(
            self.question_direction_plan,
            "question"
        ):
            return self.question_direction_plan.question(
                question_number
            )

        return None

    def configure_execution(
        self,
        settings,
    ):
        if hasattr(
            settings,
            "to_dict"
        ):
            data = settings.to_dict()
        else:
            data = dict(
                settings or {}
            )

        self.execution_settings.update(
            data
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
                scene_duration=duration,
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
        scene_duration: float | None = None,
    ) -> Image.Image:
        question_direction = (
            self._question_direction(
                question_number
            )
        )

        story_beat = self._story_beat(
            question_number
        )
        ipe_directive = self._ipe_directive(question_number)

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
                interval_override=(
                    self.execution_settings.get(
                        "pattern_break_interval"
                    )
                ),
                enabled=bool(
                    self.execution_settings.get(
                        "pattern_breaks_enabled",
                        True
                    )
                ),
                intensity_override=(
                    self.execution_settings.get(
                        "pattern_break_intensity"
                    )
                ),
            )
        )

        if (
            ipe_directive is not None
            and ipe_directive.force_pattern_break
            and scene_kind == "question"
        ):
            from dataclasses import replace
            pattern_decision = replace(
                pattern_decision,
                active=True,
                intensity=max(pattern_decision.intensity, .84),
                camera_boost=max(pattern_decision.camera_boost, ipe_directive.motion_boost),
                mascot_boost=max(pattern_decision.mascot_boost, ipe_directive.mascot_boost),
            )

        component_context = ComponentContext(
            width=self.width,
            height=self.height,
            theme_pack=theme_pack,
            scene_kind=scene_kind,
            question_number=question_number,
            total_questions=total_questions,
            progress=progress,
            time=time,
        )

        correct_answer = str(
            question.get(
                "resposta",
                ""
            )
        ).strip()

        def component_renderer(component):
            def render(canvas, bounds, graph_context):
                from .components import ComponentBox
                component.render(
                    canvas,
                    ComponentBox(
                        bounds.x,
                        bounds.y,
                        bounds.width,
                        bounds.height,
                    ),
                    component_context,
                )
                return canvas
            return render

        renderers = {
            "background": lambda canvas, bounds, ctx: self._background(
                theme_pack=theme_pack,
                time=time,
                scene_kind=scene_kind,
            ),
            "question": component_renderer(
                QuestionComponent(question.get("pergunta", ""))
            ),
            "progress": component_renderer(
                ProgressComponent(question_number, total_questions)
            ),
        }

        if has_image and layout.main_image is not None:
            renderers["main_image"] = component_renderer(
                MainImageComponent(image_path)
            )

        for index, alternative in enumerate(alternatives, start=1):
            highlighted = (
                scene_kind == "reveal"
                and self._matches_answer(
                    alternative,
                    index,
                    correct_answer,
                )
            )
            renderers[f"choice_{index}"] = component_renderer(
                ChoiceComponent(
                    alternative,
                    index,
                    highlighted,
                )
            )

            def make_sheen_renderer(
                choice_index,
                is_highlighted,
            ):
                def render_sheen(
                    canvas,
                    bounds,
                    graph_context,
                ):
                    phase = (
                        progress
                        + choice_index * 0.17
                    ) % 1.0

                    intensity = (
                        0.38
                        if is_highlighted
                        else 0.20
                    )

                    return (
                        self.scoped_materials
                        .apply_sheen(
                            canvas=canvas,
                            bounds=bounds,
                            progress=phase,
                            color=(255, 255, 255),
                            intensity=intensity,
                            corner_radius=22,
                        )
                    )

                return render_sheen

            renderers[
                f"choice_{index}_sheen"
            ] = make_sheen_renderer(
                index,
                highlighted,
            )

        if scene_kind == "countdown" and countdown_value is not None:
            renderers["timer"] = component_renderer(
                TimerComponent(
                    countdown_value,
                    max(int(countdown_maximum or countdown_value), 1),
                )
            )

        if scene_kind == "reveal":
            renderers["answer"] = component_renderer(
                AnswerComponent(
                    correct_answer
                )
            )

            def answer_inner_glow_renderer(
                canvas,
                bounds,
                graph_context,
            ):
                reveal_intensity = (
                    float(
                        question_direction
                        .reveal_intensity
                    )
                    if question_direction
                    is not None
                    else 0.72
                )

                if story_beat is not None:
                    reveal_intensity *= (
                        story_beat
                        .reveal_multiplier
                    )

                return (
                    self.scoped_materials
                    .apply_inner_glow(
                        canvas=canvas,
                        bounds=bounds,
                        progress=progress,
                        color=tuple(
                            theme_pack.get(
                                "accent_color",
                                (255, 215, 65),
                            )
                        ),
                        intensity=min(
                            reveal_intensity,
                            1.0,
                        ),
                        corner_radius=28,
                        width=8,
                    )
                )

            renderers[
                "answer_inner_glow"
            ] = answer_inner_glow_renderer


        # O foco agora é resolvido a partir dos nós estruturais.
        graph = self.scene_graph_factory.build(
            layout=layout,
            renderers=renderers,
            alternative_count=len(alternatives),
            has_image=has_image,
            scene_kind=scene_kind,
        )

        self.last_layout_intelligence_report = (
            self.layout_intelligence.optimize(
                graph=graph,
                question_text_length=len(
                    str(
                        question.get(
                            "pergunta",
                            ""
                        )
                    )
                ),
                alternative_lengths=[
                    len(str(value))
                    for value in alternatives
                ],
                has_image=has_image,
                scene_kind=scene_kind,
            )
        )

        graph_focus = self.scene_graph_focus.resolve(
            graph,
            scene_kind,
        )
        from ..attention.eye_focus import FocusTarget
        focus_target = FocusTarget(
            x=graph_focus.x,
            y=graph_focus.y,
            radius=graph_focus.radius,
            intensity=graph_focus.intensity,
        )

        difficulty = float(
            getattr(
                question_direction,
                "difficulty_score",
                getattr(
                    question_direction,
                    "difficulty",
                    50.0,
                ),
            )
            if question_direction is not None
            else 50.0
        )

        surprise = bool(
            getattr(
                question_direction,
                "surprise_moment",
                False,
            )
            if question_direction is not None
            else False
        )

        emotional_tone = str(
            getattr(
                story_beat,
                "emotional_tone",
                "",
            )
            if story_beat is not None
            else ""
        )

        self.last_cinematic_experience = (
            self.cinematic_experience_director
            .choose(
                scene_kind=scene_kind,
                emotional_tone=emotional_tone,
                difficulty=difficulty,
                surprise=surprise,
                pattern_break=bool(
                    pattern_decision.active
                ),
                question_number=question_number,
                total_questions=total_questions,
            )
        )

        self.last_cinematic_experience = (
            self.identity_engine.enforce_experience(
                self.last_cinematic_experience
            )
        )

        def pattern_renderer(canvas, bounds, ctx):
            return self.pattern_break.apply_accent(
                image=canvas,
                decision=pattern_decision,
                accent_color=tuple(theme_pack.get("accent_color", (255, 215, 65))),
                progress=progress,
            )

        def focus_renderer(canvas, bounds, ctx):
            return self.eye_focus.apply(
                canvas,
                focus_target,
                accent_color=tuple(theme_pack.get("accent_color", (255, 215, 65))),
            )


        def mascot_renderer(canvas, bounds, ctx):
            if not bool(self.execution_settings.get("mascot_enabled", True)):
                return canvas

            base=float(
                question_direction.mascot_intensity
                if question_direction is not None
                else self.execution_settings.get("mascot_intensity", .80)
            )
            if story_beat is not None:
                base*=story_beat.mascot_multiplier

            boost=float(pattern_decision.mascot_boost)
            if ipe_directive is not None:
                boost=max(boost,float(getattr(ipe_directive,"mascot_boost",0.0)))

            duration=max(float(scene_duration or 0.0),1.0)
            difficulty=float(
                getattr(question_direction,"difficulty_score",
                    getattr(question_direction,"difficulty",50.0))
                if question_direction is not None else 50.0
            )
            surprise=bool(
                getattr(question_direction,"surprise_moment",False)
                if question_direction is not None else False
            )
            tone=str(getattr(story_beat,"emotional_tone","") if story_beat is not None else "")
            focus_side="left" if focus_target.x<self.width/2 else "right"
            production_mode=str(
                getattr(self,"universal_visual_context",{}).get(
                    "intelligent_production_plan",{}
                ).get("production_mode","")
            )

            performance=self.mascot_performance_director.create_performance(
                scene_kind=scene_kind,
                question_number=question_number,
                duration=duration,
                difficulty=difficulty,
                surprise=surprise,
                correct_reveal=(scene_kind=="reveal"),
                focus_side=focus_side,
                production_mode=production_mode,
                emotional_tone=tone,
                mascot_boost=min(max(boost+max(base-.80,0.0)*.35,0.0),.25),
            )
            self.last_mascot_performance=performance

            asset,x,y=self.mascot_actor_animator.render(
                performance=performance,
                time=time,
                canvas_size=(self.width,self.height),
                base_size=(bounds.width,bounds.height),
                anchor=(bounds.x,bounds.y),
            )
            if asset is not None:
                canvas.alpha_composite(asset,(x,y))
            return canvas
        def post_process_renderer(canvas, bounds, ctx):
            experience = (
                self.last_cinematic_experience
            )

            canvas = (
                self.cinematic_experience_compositor
                .apply_pre_camera(
                    image=canvas,
                    experience=experience,
                    time=time,
                    progress=progress,
                    focus=focus_target,
                    accent_color=tuple(
                        theme_pack.get(
                            "accent_color",
                            (255, 215, 65),
                        )
                    ),
                )
            )

            motion = float(
                question_direction.camera_intensity
                if question_direction is not None
                else theme_pack.get(
                    "motion_intensity",
                    0.50,
                )
            )

            if story_beat is not None:
                motion *= (
                    story_beat.camera_multiplier
                )

            motion *= float(
                experience.camera_multiplier
            )

            canvas = self.cinematic_scene.apply_camera(
                canvas,
                target=focus_target,
                time=time,
                progress=progress,
                scene_kind=scene_kind,
                motion_intensity=min(
                    motion
                    + pattern_decision.camera_boost,
                    1.0,
                ),
            )

            canvas = self._apply_color_script(
                image=canvas,
                story_beat=story_beat,
            )

            return (
                self.cinematic_experience_compositor
                .apply_post_camera(
                    image=canvas,
                    experience=experience,
                    time=time,
                    progress=progress,
                )
            )

        effect_renderers = {
            "pattern_accent": pattern_renderer,
            "focus_effect": focus_renderer,
            "mascot": mascot_renderer,
            "post_process": post_process_renderer,
        }
        for node_id, renderer in effect_renderers.items():
            node = graph.find(node_id if node_id != "post_process" else "camera_and_color")
            if node is not None:
                node.renderer = renderer
                node.visible = True

        # Posiciona o mascote no lado oposto ao foco antes da resolução de colisões.
        mascot_node = graph.find("mascot")
        if mascot_node is not None:
            if focus_target.x >= self.width // 2:
                mascot_node.bounds = mascot_node.bounds.__class__(18, self.height - mascot_node.bounds.height - 8, mascot_node.bounds.width, mascot_node.bounds.height)
            else:
                mascot_node.bounds = mascot_node.bounds.__class__(self.width - mascot_node.bounds.width - 18, self.height - mascot_node.bounds.height - 8, mascot_node.bounds.width, mascot_node.bounds.height)

        graph = self.scene_graph_resolver.resolve(
            graph
        )

        self.last_quality_preflight_report = (
            self.quality_director.preflight(
                graph=graph,
                scene_kind=scene_kind,
                question_text=str(
                    question.get(
                        "pergunta",
                        ""
                    )
                ),
                alternatives=[
                    str(value)
                    for value in alternatives
                ],
                has_image=has_image,
                image_path=(
                    str(image_path)
                    if image_path
                    else None
                ),
                theme_pack=theme_pack,
            )
        )

        graph_issues = self.scene_graph_validator.validate(
            graph
        )
        self.last_identity_evaluation = self.identity_engine.evaluate_scene(
            theme_pack=theme_pack,
            experience=self.last_cinematic_experience,
            mascot_performance=self.last_mascot_performance,
        )

        graph.metadata.update({
            "focus_node_id": graph_focus.node_id,
            "effects_migrated": [
                "scoped_card_sheen",
                "scoped_answer_glow",
                "pattern_break",
                "eye_focus",
                "mascot",
                "camera",
                "color_script",
            ],
            "material_binding": True,
            "mascot_actor": (
                self.last_mascot_performance.to_dict()
                if self.last_mascot_performance is not None
                else None
            ),
            "cinematic_experience": (
                self.last_cinematic_experience.to_dict()
                if self.last_cinematic_experience is not None
                else None
            ),
            "identity_engine": self.last_identity_evaluation,
            "knowledge_renderer": {
                "profile": dict(self.knowledge_profile),
                "reveal_plan": dict(self.knowledge_reveal_plan),
            },
            "theme_experience": (
                self.last_theme_experience.to_dict()
                if self.last_theme_experience is not None
                else None
            ),
            "graph_version": "4.5",
        })
        self.last_scene_graph_report = self.scene_graph_diagnostics.graph_to_dict(
            graph,
            graph_issues,
        )
        self.last_scene_graph_report[
            "quality_preflight"
        ] = (
            self.last_quality_preflight_report
            .to_dict()
            if self.last_quality_preflight_report
            is not None
            else None
        )

        self.last_scene_graph_report[
            "layout_intelligence"
        ] = (
            self.last_layout_intelligence_report
            .to_dict()
            if self.last_layout_intelligence_report
            is not None
            else None
        )

        graph_context = SceneRenderContext(
            width=self.width,
            height=self.height,
            time=time,
            progress=progress,
            scene_kind=scene_kind,
            question_number=question_number,
            total_questions=total_questions,
            theme_pack=theme_pack,
            metadata={
                "question_direction": question_direction,
                "story_beat": story_beat,
                "focus_node_id": graph_focus.node_id,
            },
        )

        base_canvas = Image.new(
            "RGBA",
            (
                self.width,
                self.height,
            ),
            (
                0,
                0,
                0,
                0,
            ),
        )

        if (
            self.last_quality_preflight_report
            is not None
            and not self.last_quality_preflight_report
            .can_render
        ):
            image = self._quality_fallback_frame(
                image=self._background(
                    theme_pack=theme_pack,
                    time=time,
                    scene_kind=scene_kind,
                ),
                question_text=str(
                    question.get(
                        "pergunta",
                        ""
                    )
                ),
            )
        else:
            image = graph.render(
                base_canvas,
                graph_context,
            )

        return image

    def _quality_fallback_frame(
        self,
        *,
        image,
        question_text,
    ):
        draw = ImageDraw.Draw(image)

        draw.rounded_rectangle(
            (
                150,
                220,
                self.width - 150,
                500,
            ),
            radius=34,
            fill=(255, 255, 255, 245),
            outline=(185, 65, 65, 255),
            width=6,
        )

        from .components.utils import (
            centered_x,
            fit_font,
        )

        title = (
            "Não foi possível montar esta pergunta"
        )

        title_font = fit_font(
            draw=draw,
            text=title,
            max_width=self.width - 360,
            start_size=38,
            min_size=24,
            bold=True,
        )

        draw.text(
            (
                centered_x(
                    draw,
                    title,
                    title_font,
                    self.width,
                ),
                265,
            ),
            title,
            font=title_font,
            fill=(120, 35, 35),
        )

        safe_text = (
            question_text[:120]
            if question_text
            else "Pergunta sem conteúdo."
        )

        body_font = fit_font(
            draw=draw,
            text=safe_text,
            max_width=self.width - 420,
            start_size=27,
            min_size=18,
            bold=False,
        )

        draw.text(
            (
                centered_x(
                    draw,
                    safe_text,
                    body_font,
                    self.width,
                ),
                355,
            ),
            safe_text,
            font=body_font,
            fill=(50, 50, 65),
        )

        return image

    def _apply_color_script(
        self,
        *,
        image,
        story_beat,
    ):
        if story_beat is None:
            return image

        contrast = (
            1.0
            + float(
                story_beat.contrast_shift
            )
        )

        saturation = (
            1.0
            + float(
                story_beat.saturation_shift
            )
        )

        result = ImageEnhance.Contrast(
            image.convert("RGB")
        ).enhance(
            contrast
        )

        result = ImageEnhance.Color(
            result
        ).enhance(
            saturation
        )

        rgba = result.convert("RGBA")

        warmth = float(
            story_beat.warmth_shift
        )

        if abs(warmth) > 0.001:
            overlay = Image.new(
                "RGBA",
                rgba.size,
                (
                    255,
                    175,
                    95,
                    int(
                        min(
                            abs(warmth)
                            * 255,
                            28
                        )
                    )
                )
                if warmth > 0
                else (
                    90,
                    150,
                    255,
                    int(
                        min(
                            abs(warmth)
                            * 255,
                            28
                        )
                    )
                ),
            )

            rgba.alpha_composite(
                overlay
            )

        return rgba

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

        category = str(
            self.knowledge_profile.get(
                "category",
                "general_knowledge",
            )
        )

        self.last_theme_experience = (
            self.theme_experience_director.choose(
                category=category,
                question_number=int(
                    self.knowledge_profile
                    .get(
                        "metadata",
                        {},
                    )
                    .get(
                        "question_number",
                        1,
                    )
                ),
                scene_kind=scene_kind,
            )
        )

        image = self.theme_specific_compositor.apply(
            image=image,
            profile=self.last_theme_experience,
            time=time,
            content_box=(
                54,
                50,
                self.width - 54,
                self.height - 50,
            ),
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
