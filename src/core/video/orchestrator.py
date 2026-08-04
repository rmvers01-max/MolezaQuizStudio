from typing import Any
from pathlib import Path
import json
from datetime import datetime

from .identity_engine import AAAIdentityEngine
from .legacy_generator import LegacyVideoGenerator
from .execution import ProductionPlanExecutor
from .quiz_director import IntelligentQuizDirector
from .story_engine import CinematicStoryDirector
from .production_engine import (
    IPEExecutionLayer,
    IntelligentProductionEngine,
)
from .intelligence import (
    ABTestPlanner,
    MolezaIntelligenceManager,
    RecommendationOverrideBuilder,
)
from .ai_director import (
    AICreativeDirector,
    CreativeOverrideLoader,
    ProductionPlanWriter,
)
from .templates.preference_renderer import ProfessionalPreferenceRenderer
from .templates.registry import VideoTemplateRegistry
from .universal import (
    UniversalCreativeDirector,
    UniversalCreativePlanWriter,
    UniversalPlanWriter,
    UniversalQuizAdapterRegistry,
)


class VideoGenerator:
    """Orquestra templates e preserva a interface pública anterior."""

    def __init__(self):
        self.registry = VideoTemplateRegistry()
        self.renderer = LegacyVideoGenerator()
        self.preference_renderer = (
            ProfessionalPreferenceRenderer()
        )

        self.universal_registry = (
            UniversalQuizAdapterRegistry()
        )

        self.universal_plan_writer = (
            UniversalPlanWriter()
        )

        self.universal_creative_director = (
            UniversalCreativeDirector()
        )

        self.universal_creative_writer = (
            UniversalCreativePlanWriter()
        )

        self.ai_creative_director = AICreativeDirector()
        self.creative_override_loader = (
            CreativeOverrideLoader()
        )
        self.production_plan_writer = (
            ProductionPlanWriter()
        )

        self.production_plan_executor = (
            ProductionPlanExecutor()
        )

        self.intelligent_quiz_director = (
            IntelligentQuizDirector()
        )

        self.cinematic_story_director = (
            CinematicStoryDirector()
        )

        self.intelligence_manager = None
        self.ab_test_planner = ABTestPlanner()
        self.recommendation_override_builder = (
            RecommendationOverrideBuilder()
        )

        self.intelligent_production_engine = (
            IntelligentProductionEngine()
        )
        self.ipe_execution_layer = IPEExecutionLayer()
        self.identity_engine = AAAIdentityEngine()

    @property
    def largura(self):
        return self.renderer.largura

    @largura.setter
    def largura(self, valor):
        self.renderer.largura = valor
        self.preference_renderer.largura = valor

    @property
    def altura(self):
        return self.renderer.altura

    @altura.setter
    def altura(self, valor):
        self.renderer.altura = valor
        self.preference_renderer.altura = valor

    @property
    def fps(self):
        return self.renderer.fps

    @fps.setter
    def fps(self, valor):
        self.renderer.fps = valor
        self.preference_renderer.fps = valor

    def gerar_video(
        self,
        pasta_projeto,
        perguntas,
        tempo_resposta=5,
        limite_perguntas=None,
        caminho_musica=None,
        volume_musica=0.15,
        volume_narracao=1.0,
        usar_narracao=True,
        titulo_quiz="Moleza Quiz",
        texto_encerramento=None,
        incluir_abertura=True,
        incluir_encerramento=True,
        callback_progresso=None,
        perfil_renderizacao="balanced",
    ):
        perguntas_validas = [
            dict(pergunta)
            for pergunta in perguntas
            if isinstance(pergunta, dict)
        ]

        tipo_quiz, perguntas_preparadas = (
            self.registry.preparar_perguntas(
                perguntas=perguntas_validas,
                titulo_quiz=titulo_quiz,
            )
        )

        template = self.registry.obter(tipo_quiz)

        universal_adapter = (
            self.universal_registry
            .get(tipo_quiz)
        )

        universal_plan = (
            universal_adapter
            .build_plan(
                title=titulo_quiz,
                questions=perguntas_preparadas,
                response_time=tempo_resposta,
            )
        )

        self.universal_plan_writer.save(
            universal_plan,
            (
                Path(pasta_projeto)
                / "videos"
                / "relatorios"
                / "universal_quiz_plan.json"
            )
        )

        universal_creative_plan = (
            self.universal_creative_director
            .direct(
                universal_plan
            )
        )

        self.universal_creative_writer.save(
            universal_creative_plan,
            (
                Path(pasta_projeto)
                / "videos"
                / "relatorios"
                / "universal_creative_plan.json"
            )
        )

        creative_override = (
            self.creative_override_loader.load(
                Path(pasta_projeto)
                / "config"
                / "creative_overrides.json"
            )
        )

        production_plan = (
            self.ai_creative_director.create_plan(
                title=titulo_quiz,
                quiz_type=tipo_quiz,
                total_questions=len(
                    perguntas_preparadas
                ),
                creative_plan=universal_creative_plan,
                override=creative_override,
            )
        )

        self.production_plan_writer.save(
            production_plan,
            (
                Path(pasta_projeto)
                / "videos"
                / "relatorios"
                / "ai_production_plan.json"
            )
        )

        universal_creative_plan[
            "ai_production_plan"
        ] = production_plan.to_dict()

        execution_settings = (
            self.production_plan_executor
            .build_settings(
                production_plan.to_dict()
            )
        )

        self.production_plan_executor.save_report(
            execution_settings,
            (
                Path(pasta_projeto)
                / "videos"
                / "relatorios"
                / "production_execution_report.json"
            )
        )

        quiz_direction_plan = (
            self.intelligent_quiz_director
            .create_plan(
                title=titulo_quiz,
                quiz_type=tipo_quiz,
                questions=perguntas_preparadas,
                base_response_time=tempo_resposta,
                production_plan=(
                    production_plan.to_dict()
                ),
            )
        )

        self.intelligent_quiz_director.save(
            quiz_direction_plan,
            (
                Path(pasta_projeto)
                / "videos"
                / "relatorios"
                / "question_director_report.json"
            )
        )

        story_arc_plan = (
            self.cinematic_story_director
            .create_plan(
                title=titulo_quiz,
                quiz_type=tipo_quiz,
                total_questions=len(
                    perguntas_preparadas
                ),
                question_plan=(
                    quiz_direction_plan.to_dict()
                ),
            )
        )

        self.cinematic_story_director.save(
            story_arc_plan,
            (
                Path(pasta_projeto)
                / "videos"
                / "relatorios"
                / "cinematic_story_plan.json"
            )
        )

        intelligent_production_plan = (
            self.intelligent_production_engine.create_plan(
                title=titulo_quiz,
                quiz_type=tipo_quiz,
                questions=perguntas_preparadas,
                production_plan=production_plan.to_dict(),
                question_plan=quiz_direction_plan.to_dict(),
                story_plan=story_arc_plan.to_dict(),
            )
        )

        self.intelligent_production_engine.save(
            intelligent_production_plan,
            (
                Path(pasta_projeto)
                / "videos"
                / "relatorios"
                / "intelligent_production_plan.json"
            )
        )

        universal_creative_plan[
            "intelligent_production_plan"
        ] = intelligent_production_plan.to_dict()

        identity_plan = self.identity_engine.create_plan(
            category=intelligent_production_plan.content_profile.category,
            theme_pack=production_plan.to_dict().get(
                "theme_pack",
                universal_creative_plan.get("theme_pack", {}),
            ),
            production_mode=intelligent_production_plan.production_mode,
        )
        self.identity_engine.save(
            identity_plan,
            Path(pasta_projeto) / "videos" / "relatorios" / "identity_engine_report.json",
        )
        universal_creative_plan["identity_plan"] = identity_plan.to_dict()
        universal_creative_plan["theme_pack"] = dict(identity_plan.corrected_theme_pack)

        ipe_execution_plan = (
            self.ipe_execution_layer.build(
                intelligent_production_plan.to_dict()
            )
        )
        self.ipe_execution_layer.save(
            ipe_execution_plan,
            Path(pasta_projeto) / "videos" / "relatorios" / "ipe_execution_report.json",
        )

        self.intelligence_manager = (
            MolezaIntelligenceManager(
                Path(pasta_projeto)
                / "intelligence"
            )
        )

        production_fingerprint = (
            self.intelligence_manager
            .register_production(
                title=titulo_quiz,
                quiz_type=tipo_quiz,
                total_questions=len(
                    perguntas_preparadas
                ),
                production_plan=(
                    production_plan.to_dict()
                ),
                story_plan=(
                    story_arc_plan.to_dict()
                ),
            )
        )

        intelligence_report = (
            self.intelligence_manager
            .build_intelligence_report()
        )

        recommendations = list(
            intelligence_report.get(
                "recommendations",
                []
            )
        )

        ab_test_plan = (
            self.ab_test_planner
            .create_plan(
                title=titulo_quiz,
                quiz_type=tipo_quiz,
                production_plan=(
                    production_plan.to_dict()
                ),
                recommendations=recommendations,
            )
        )

        self.ab_test_planner.save(
            ab_test_plan,
            (
                Path(pasta_projeto)
                / "intelligence"
                / "experiments"
                / f"{ab_test_plan.experiment_id}.json"
            )
        )

        self.ab_test_planner.save(
            ab_test_plan,
            (
                Path(pasta_projeto)
                / "videos"
                / "relatorios"
                / "ab_test_plan.json"
            )
        )

        suggested_overrides = (
            self.recommendation_override_builder
            .build(
                production_plan=(
                    production_plan.to_dict()
                ),
                recommendations=recommendations,
            )
        )

        self.recommendation_override_builder.save(
            suggested_overrides,
            (
                Path(pasta_projeto)
                / "intelligence"
                / "suggested_creative_overrides.json"
            )
        )

        (
            Path(pasta_projeto)
            / "videos"
            / "relatorios"
            / "intelligence_report.json"
        ).write_text(
            json.dumps(
                {
                    "production_fingerprint": (
                        production_fingerprint
                        .to_dict()
                    ),
                    **intelligence_report,
                    "ab_test_plan": (
                        ab_test_plan.to_dict()
                    ),
                    "suggested_overrides": (
                        suggested_overrides
                    ),
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        self.renderer.configurar_plano_producao(
            execution_settings
        )

        self.renderer.configurar_direcao_perguntas(
            quiz_direction_plan
        )

        self.renderer.configurar_historia_cinematica(
            story_arc_plan
        )
        self.renderer.configurar_execucao_ipe(
            ipe_execution_plan
        )

        if hasattr(
            self.preference_renderer,
            "configurar_plano_producao"
        ):
            self.preference_renderer.configurar_plano_producao(
                execution_settings
            )

        if not str(texto_encerramento or "").strip():
            texto_encerramento = (
                template.texto_encerramento_padrao()
            )

        renderer = (
            self.preference_renderer
            if tipo_quiz == "preferencia"
            else self.renderer
        )

        if tipo_quiz != "preferencia":
            self.renderer.configurar_direcao_universal(
                universal_creative_plan
            )

        if tipo_quiz == "preferencia":
            renderer.total_perguntas_contexto = len(
                perguntas_preparadas
            )

            renderer.definir_preset_automatico(
                titulo_quiz
            )

            renderer.definir_perfil_renderizacao(
                perfil_renderizacao
            )

        resultado_video = renderer.gerar_video(
            pasta_projeto=pasta_projeto,
            perguntas=perguntas_preparadas,
            tempo_resposta=tempo_resposta,
            limite_perguntas=limite_perguntas,
            caminho_musica=caminho_musica,
            volume_musica=volume_musica,
            volume_narracao=volume_narracao,
            usar_narracao=usar_narracao,
            titulo_quiz=titulo_quiz,
            texto_encerramento=texto_encerramento,
            incluir_abertura=incluir_abertura,
            incluir_encerramento=incluir_encerramento,
            callback_progresso=callback_progresso,
        )

        if tipo_quiz != "preferencia":
            scene_graph_report = (
                self.renderer
                .obter_relatorio_scene_graph()
            )

            if scene_graph_report is not None:
                report_path = (
                    Path(pasta_projeto)
                    / "videos"
                    / "relatorios"
                    / "scene_graph_report.json"
                )
                report_path.parent.mkdir(
                    parents=True,
                    exist_ok=True,
                )
                report_path.write_text(
                    json.dumps(
                        scene_graph_report,
                        ensure_ascii=False,
                        indent=2,
                        default=str,
                    ),
                    encoding="utf-8",
                )

        if tipo_quiz == "preferencia":
            self._salvar_relatorio_render(
                pasta_projeto=pasta_projeto,
                renderer=renderer,
                titulo_quiz=titulo_quiz,
                total_perguntas=len(
                    perguntas_preparadas
                )
            )

        return resultado_video

    def _salvar_relatorio_render(
        self,
        pasta_projeto,
        renderer,
        titulo_quiz,
        total_perguntas
    ):
        pasta_projeto = Path(
            pasta_projeto
        )

        pasta_relatorios = (
            pasta_projeto
            / "videos"
            / "relatorios"
        )

        pasta_relatorios.mkdir(
            parents=True,
            exist_ok=True
        )

        compositor = (
            renderer.timeline_compositor
        )

        perfil = (
            compositor.render_profile
        )

        diagnostico = (
            compositor.render_diagnostics
            .resumo()
        )

        dados = {
            "gerado_em": datetime.now().isoformat(
                timespec="seconds"
            ),
            "titulo_quiz": titulo_quiz,
            "total_perguntas": int(
                total_perguntas
            ),
            "perfil": {
                "codigo": (
                    renderer
                    .perfil_renderizacao
                ),
                "nome": perfil.nome,
                "fps_timeline": (
                    perfil.fps_timeline
                ),
                "escala_interna": (
                    perfil.escala_interna
                ),
                "anti_aliasing": (
                    perfil.anti_aliasing
                ),
                "cinematic_fx": (
                    perfil.cinematic_fx
                ),
                "visual_fx": (
                    perfil.visual_fx
                ),
                "motion_blur": (
                    perfil.motion_blur
                ),
                "camera_engine": (
                    perfil.camera_engine
                ),
            },
            "diagnostico": diagnostico,
        }

        caminho = (
            pasta_relatorios
            / "ultimo_render.json"
        )

        caminho.write_text(
            json.dumps(
                dados,
                ensure_ascii=False,
                indent=2
            ),
            encoding="utf-8"
        )

        return caminho

    def identificar_tipo_quiz(
        self,
        perguntas: list[dict[str, Any]],
        titulo_quiz: str = "",
    ) -> str:
        return self.registry.identificar_tipo(
            perguntas=perguntas,
            titulo_quiz=titulo_quiz,
        )

    def __getattr__(self, nome):
        return getattr(self.renderer, nome)
