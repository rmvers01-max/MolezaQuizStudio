from moviepy import concatenate_videoclips


class ProfessionalSceneEngine:
    """
    Orquestrador da Animation Engine 2.0.

    Cada módulo continua independente:
    - câmera;
    - cartões;
    - reflexo;
    - futuras camadas.
    """

    def __init__(
        self,
        camera_factory,
        card_factory,
        light_factory,
    ):
        self.camera_factory = (
            camera_factory
        )

        self.card_factory = (
            card_factory
        )

        self.light_factory = (
            light_factory
        )

    def criar_cena_pergunta(
        self,
        caminho_frame,
        duracao,
        zoom_final=1.02,
    ):
        duracao = max(
            float(duracao),
            0.2,
        )

        duracao_reflexo = min(
            0.8,
            duracao,
        )

        duracao_cartoes = (
            duracao
            - duracao_reflexo
        )

        clips = []

        if duracao_cartoes > 0.05:
            clips.append(
                self.card_factory.aplicar(
                    caminho_frame=caminho_frame,
                    duracao=duracao_cartoes,
                    amplitude_vertical=3,
                    amplitude_horizontal=2,
                )
            )

        clips.append(
            self.light_factory.aplicar(
                caminho_frame=caminho_frame,
                duracao=duracao_reflexo,
                intensidade=0.18,
            )
        )

        return concatenate_videoclips(
            clips,
            method="compose",
        )

    def criar_cena_contagem(
        self,
        caminho_frame,
        duracao=1.0,
        zoom_final=1.01,
    ):
        return self.camera_factory.aplicar(
            caminho_frame=caminho_frame,
            duracao=duracao,
            zoom_final=zoom_final,
            pan_horizontal=3,
            pulso_brilho=0.025,
        )
