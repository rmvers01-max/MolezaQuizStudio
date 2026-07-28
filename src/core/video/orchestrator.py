from typing import Any

from .legacy_generator import LegacyVideoGenerator
from .templates.preference_renderer import ProfessionalPreferenceRenderer
from .templates.registry import VideoTemplateRegistry


class VideoGenerator:
    """Orquestra templates e preserva a interface pública anterior."""

    def __init__(self):
        self.registry = VideoTemplateRegistry()
        self.renderer = LegacyVideoGenerator()
        self.preference_renderer = (
            ProfessionalPreferenceRenderer()
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

        if not str(texto_encerramento or "").strip():
            texto_encerramento = (
                template.texto_encerramento_padrao()
            )

        renderer = (
            self.preference_renderer
            if tipo_quiz == "preferencia"
            else self.renderer
        )

        return renderer.gerar_video(
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
