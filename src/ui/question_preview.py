from pathlib import Path

from core.video.legacy_generator import LegacyVideoGenerator
from core.video.templates.preference_renderer import (
    ProfessionalPreferenceRenderer,
)
from core.video.templates.registry import VideoTemplateRegistry


class QuestionPreviewGenerator:
    """Gera uma imagem de prévia usando o mesmo renderer do vídeo."""

    def __init__(self):
        self.registry = VideoTemplateRegistry()
        self.renderer_preferencia = (
            ProfessionalPreferenceRenderer()
        )
        self.renderer_conhecimento = (
            LegacyVideoGenerator()
        )

    def gerar(
        self,
        pasta_projeto,
        pergunta,
        numero=1,
        etapa="pergunta",
        contador=5,
    ) -> Path:
        pasta_projeto = Path(
            pasta_projeto
        )

        pasta_previews = (
            pasta_projeto
            / "videos"
            / "previews"
        )

        pasta_previews.mkdir(
            parents=True,
            exist_ok=True
        )

        pergunta_preparada = dict(
            pergunta
        )

        tipo = self.registry.identificar_tipo(
            perguntas=[pergunta_preparada],
            titulo_quiz=str(
                pergunta_preparada.get(
                    "pergunta",
                    ""
                )
            ),
        )

        pergunta_preparada["tipo_quiz"] = tipo

        renderer = (
            self.renderer_preferencia
            if tipo == "preferencia"
            else self.renderer_conhecimento
        )

        nome_arquivo = (
            f"pergunta_{int(numero):03d}_"
            f"{etapa}.png"
        )

        caminho = (
            pasta_previews
            / nome_arquivo
        )

        if etapa == "contagem":
            renderer._criar_frame_contagem(
                caminho=caminho,
                numero=numero,
                pergunta=pergunta_preparada,
                contador=max(
                    int(contador),
                    1
                )
            )

        elif etapa == "resultado":
            if tipo == "preferencia":
                renderer._criar_frame_escolha(
                    caminho=caminho,
                    numero=numero,
                    pergunta=pergunta_preparada
                )
            else:
                renderer._criar_frame_resposta(
                    caminho=caminho,
                    numero=numero,
                    pergunta=pergunta_preparada
                )

        else:
            renderer._criar_frame_pergunta(
                caminho=caminho,
                numero=numero,
                pergunta=pergunta_preparada
            )

        return caminho
