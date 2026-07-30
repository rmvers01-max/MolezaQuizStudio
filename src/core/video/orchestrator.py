from typing import Any
from pathlib import Path
import json
from datetime import datetime

from .legacy_generator import LegacyVideoGenerator
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

        if not str(texto_encerramento or "").strip():
            texto_encerramento = (
                template.texto_encerramento_padrao()
            )

        renderer = (
            self.preference_renderer
            if tipo_quiz == "preferencia"
            else self.renderer
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
