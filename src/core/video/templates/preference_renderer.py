from pathlib import Path
import math
import textwrap

from PIL import Image, ImageDraw, ImageFont, ImageOps
from moviepy import AudioFileClip, ImageClip

from ..animations import (
    AnimatedBackgroundFactory,
    CameraMotionFactory,
    CardMotionFactory,
    MascotAnimationFactory,
    ProfessionalSceneEngine,
    LayeredSceneAnimator,
    SceneClipFactory,
    TransitionFactory,
)
from ..effects import (
    ConfettiFactory,
    SoundEffectFactory,
    SparklesFactory,
    LightSweepFactory,
)
from ..widgets import MascotWidget
from .visual_presets import VisualPresetRegistry

from ..legacy_generator import LegacyVideoGenerator


class ProfessionalPreferenceRenderer(LegacyVideoGenerator):
    """
    Primeiro renderer visual profissional para quizzes de preferência.

    Reaproveita toda a lógica de áudio, montagem e exportação do gerador
    legado, alterando somente a identidade visual dos frames.
    """

    COR_A = (255, 85, 115)
    COR_B = (66, 145, 255)
    COR_DESTAQUE = (255, 214, 75)
    COR_TEXTO = (255, 255, 255)
    COR_ESCURO = (24, 24, 45)

    def __init__(self):
        super().__init__()

        self.scene_factory = SceneClipFactory(
            largura=self.largura,
            altura=self.altura,
            fps_animacao=15
        )

        self.layered_animator = LayeredSceneAnimator(
            largura=self.largura,
            altura=self.altura,
            fps=20
        )

        self.sound_factory = SoundEffectFactory()
        self.transition_factory = TransitionFactory(
            largura=self.largura,
            altura=self.altura,
            fps=20
        )
        self.background_factory = AnimatedBackgroundFactory(
            largura=self.largura,
            altura=self.altura,
            fps=15
        )
        self.mascot_widget = MascotWidget()

        self.mascot_animation = MascotAnimationFactory(
            largura=self.largura,
            altura=self.altura,
            fps=20
        )

        self.confetti_factory = ConfettiFactory(
            largura=self.largura,
            altura=self.altura,
            fps=20,
            quantidade=70
        )

        self.sparkles_factory = SparklesFactory(
            largura=self.largura,
            altura=self.altura,
            fps=15,
            quantidade=28
        )

        self.total_perguntas_contexto = 1

        self.camera_factory = CameraMotionFactory(
            largura=self.largura,
            altura=self.altura,
            fps=18
        )

        self.card_motion_factory = CardMotionFactory(
            largura=self.largura,
            altura=self.altura,
            fps=18
        )

        self.light_sweep_factory = LightSweepFactory(
            largura=self.largura,
            altura=self.altura,
            fps=18
        )

        self.professional_scene_engine = (
            ProfessionalSceneEngine(
                camera_factory=self.camera_factory,
                card_factory=self.card_motion_factory,
                light_factory=self.light_sweep_factory
            )
        )
        self.preset_registry = VisualPresetRegistry()
        self.preset_visual = (
            self.preset_registry
            .obter(
                "vibrante"
            )
        )

    def _sincronizar_scene_factory(self):
        self.scene_factory.largura = self.largura
        self.scene_factory.altura = self.altura

        self.layered_animator.largura = self.largura
        self.layered_animator.altura = self.altura

        self.transition_factory.largura = self.largura
        self.transition_factory.altura = self.altura

        self.background_factory.largura = self.largura
        self.background_factory.altura = self.altura

        self.mascot_animation.largura = self.largura
        self.mascot_animation.altura = self.altura

        self.confetti_factory.largura = self.largura
        self.confetti_factory.altura = self.altura

        self.sparkles_factory.largura = self.largura
        self.sparkles_factory.altura = self.altura

        self.camera_factory.largura = self.largura
        self.camera_factory.altura = self.altura

        self.card_motion_factory.largura = self.largura
        self.card_motion_factory.altura = self.altura

        self.light_sweep_factory.largura = self.largura
        self.light_sweep_factory.altura = self.altura

    def _criar_clips_da_pergunta(
        self,
        pasta_frames,
        pasta_audios,
        numero,
        pergunta,
        tempo_resposta,
        tempo_inicio,
        usar_narracao,
        volume_narracao
    ):
        self._sincronizar_scene_factory()

        if not hasattr(
            self,
            "total_perguntas_contexto"
        ):
            self.total_perguntas_contexto = numero

        clips_video = []
        clips_audio = []

        pasta_projeto = (
            pasta_frames
            .parent
            .parent
        )

        efeitos = (
            self.sound_factory
            .preparar_pacote(
                pasta_projeto
            )
        )

        caminho_audio_pergunta = (
            pasta_audios
            / f"pergunta_{numero:03d}.mp3"
        )

        caminho_audio_escolha = (
            pasta_audios
            / f"escolha_{numero:03d}.mp3"
        )

        duracao_pergunta = 1.5

        if (
            usar_narracao
            and caminho_audio_pergunta.exists()
        ):
            audio_pergunta = AudioFileClip(
                str(caminho_audio_pergunta)
            ).with_volume_scaled(
                volume_narracao
            )

            duracao_pergunta = max(
                audio_pergunta.duration + 0.5,
                1.5
            )

            clips_audio.append(
                audio_pergunta.with_start(
                    tempo_inicio
                )
            )

        caminho_frame_pergunta = (
            pasta_frames
            / f"pergunta_{numero:03d}.png"
        )

        caminho_base_entrada = (
            pasta_frames
            / f"pergunta_{numero:03d}_base.png"
        )

        caminho_cartao_a = (
            pasta_frames
            / f"pergunta_{numero:03d}_cartao_a.png"
        )

        caminho_cartao_b = (
            pasta_frames
            / f"pergunta_{numero:03d}_cartao_b.png"
        )

        caminho_selo_ou = (
            pasta_frames
            / f"pergunta_{numero:03d}_ou.png"
        )

        self._criar_frame_pergunta(
            caminho=caminho_frame_pergunta,
            numero=numero,
            pergunta=pergunta
        )

        self._criar_camadas_entrada(
            caminho_base=caminho_base_entrada,
            caminho_cartao_a=caminho_cartao_a,
            caminho_cartao_b=caminho_cartao_b,
            caminho_selo_ou=caminho_selo_ou,
            numero=numero,
            pergunta=pergunta
        )

        duracao_entrada = min(
            1.1,
            duracao_pergunta
        )

        mascote_idle = (
            self.mascot_widget
            .preparar_pose(
                pose="idle",
                tamanho=(185, 185)
            )
        )

        clips_video.append(
            self.layered_animator.criar_entrada_opcoes(
                caminho_base=caminho_base_entrada,
                caminho_cartao_a=caminho_cartao_a,
                caminho_cartao_b=caminho_cartao_b,
                caminho_ou=caminho_selo_ou,
                duracao=duracao_entrada,
                mascote=mascote_idle
            )
        )

        clips_audio.extend([
            AudioFileClip(
                str(efeitos["entrada_a"])
            ).with_volume_scaled(
                0.32
            ).with_start(
                tempo_inicio
            ),
            AudioFileClip(
                str(efeitos["entrada_b"])
            ).with_volume_scaled(
                0.32
            ).with_start(
                tempo_inicio + 0.14
            ),
            AudioFileClip(
                str(efeitos["ou"])
            ).with_volume_scaled(
                0.38
            ).with_start(
                tempo_inicio + 0.50
            ),
        ])

        restante_pergunta = (
            duracao_pergunta
            - duracao_entrada
        )

        if restante_pergunta > 0.01:
            clips_video.append(
                self.professional_scene_engine.criar_cena_pergunta(
                    caminho_frame=caminho_frame_pergunta,
                    duracao=restante_pergunta,
                    zoom_final=(
                        self.preset_visual
                        .zoom_cena
                    )
                )
            )

        tempo_depois_pergunta = (
            tempo_inicio
            + duracao_pergunta
        )

        for contador in range(
            tempo_resposta,
            0,
            -1
        ):
            caminho_contagem = (
                pasta_frames
                / (
                    f"pergunta_{numero:03d}"
                    f"_contador_{contador}.png"
                )
            )

            self._criar_frame_contagem(
                caminho=caminho_contagem,
                numero=numero,
                pergunta=pergunta,
                contador=contador
            )

            mascote_pensando = (
                self.mascot_widget
                .preparar_pose(
                    pose="thinking",
                    tamanho=(185, 185)
                )
            )

            clips_video.append(
                self.professional_scene_engine.criar_cena_contagem(
                    caminho_frame=caminho_contagem,
                    duracao=1.0,
                    zoom_final=1.01
                )
            )

            clips_audio.append(
                AudioFileClip(
                    str(efeitos["tick"])
                ).with_volume_scaled(
                    0.28
                ).with_start(
                    tempo_depois_pergunta
                    + (
                        tempo_resposta
                        - contador
                    )
                )
            )

        tempo_inicio_escolha = (
            tempo_depois_pergunta
            + tempo_resposta
        )

        duracao_escolha = 2.2

        clips_audio.append(
            AudioFileClip(
                str(
                    efeitos[
                        "tempo_esgotado"
                    ]
                )
            ).with_volume_scaled(
                0.40
            ).with_start(
                tempo_inicio_escolha
            )
        )

        if (
            usar_narracao
            and caminho_audio_escolha.exists()
        ):
            audio_escolha = AudioFileClip(
                str(caminho_audio_escolha)
            ).with_volume_scaled(
                volume_narracao
            )

            duracao_escolha = max(
                audio_escolha.duration + 0.5,
                2.2
            )

            clips_audio.append(
                audio_escolha.with_start(
                    tempo_inicio_escolha
                )
            )

        caminho_frame_escolha = (
            pasta_frames
            / (
                f"pergunta_{numero:03d}"
                "_escolha.png"
            )
        )

        self._criar_frame_escolha(
            caminho=caminho_frame_escolha,
            numero=numero,
            pergunta=pergunta
        )

        duracao_confete = min(
            1.2,
            duracao_escolha
        )

        mascote_celebrando = (
            self.mascot_widget
            .preparar_pose(
                pose="celebrate",
                tamanho=(185, 185)
            )
        )

        clips_video.append(
            self.confetti_factory.aplicar(
                caminho_frame=caminho_frame_escolha,
                duracao=duracao_confete,
                mascote=mascote_celebrando
            )
        )

        restante_escolha = (
            duracao_escolha
            - duracao_confete
        )

        if restante_escolha > 0.01:
            if mascote_celebrando is not None:
                clips_video.append(
                    self.mascot_animation.animar_sobre_frame(
                        caminho_frame=caminho_frame_escolha,
                        mascote=mascote_celebrando,
                        duracao=restante_escolha,
                        intensidade_balanco=7,
                        intensidade_respiracao=0.035
                    )
                )
            else:
                clips_video.append(
                    ImageClip(
                        str(caminho_frame_escolha)
                    ).with_duration(
                        restante_escolha
                    )
                )

        clips_video.append(
            self.transition_factory.criar_flash(
                caminho_imagem=caminho_frame_escolha,
                duracao=0.28
            )
        )

        return {
            "clips_video": clips_video,
            "clips_audio": clips_audio,
            "duracao_total": (
                duracao_pergunta
                + tempo_resposta
                + duracao_escolha
                + 0.28
            )
        }

    def _criar_camadas_entrada(
        self,
        caminho_base,
        caminho_cartao_a,
        caminho_cartao_b,
        caminho_selo_ou,
        numero,
        pergunta
    ):
        base, desenho_base = self._criar_base()

        self._desenhar_cabecalho(
            desenho_base,
            numero
        )

        self._desenhar_titulo_pergunta(
            desenho_base,
            pergunta
        )

        self._desenhar_rodape(
            desenho_base,
            "ESCOLHA RÁPIDO!"
        )

        base.save(
            caminho_base
        )

        alternativas = pergunta.get(
            "alternativas",
            []
        )

        alternativa_a = (
            str(alternativas[0]).strip()
            if len(alternativas) >= 1
            else "OPÇÃO A"
        )

        alternativa_b = (
            str(alternativas[1]).strip()
            if len(alternativas) >= 2
            else "OPÇÃO B"
        )

        cartao_a = Image.new(
            "RGBA",
            (480, 260),
            (0, 0, 0, 0)
        )

        desenho_a = ImageDraw.Draw(
            cartao_a
        )

        desenho_a.rounded_rectangle(
            (0, 0, 479, 259),
            radius=34,
            fill=self.COR_A,
            outline=(255, 255, 255),
            width=5
        )

        self._desenhar_opcao(
            imagem_base=cartao_a,
            desenho=desenho_a,
            centro_x=240,
            topo=0,
            letra="A",
            texto=alternativa_a,
            caminho_imagem=self._obter_caminho_imagem(
                pergunta,
                indice=0
            ),
            cor_cartao=self.COR_A
        )

        cartao_a.save(
            caminho_cartao_a
        )

        cartao_b = Image.new(
            "RGBA",
            (480, 260),
            (0, 0, 0, 0)
        )

        desenho_b = ImageDraw.Draw(
            cartao_b
        )

        desenho_b.rounded_rectangle(
            (0, 0, 479, 259),
            radius=34,
            fill=self.COR_B,
            outline=(255, 255, 255),
            width=5
        )

        self._desenhar_opcao(
            imagem_base=cartao_b,
            desenho=desenho_b,
            centro_x=240,
            topo=0,
            letra="B",
            texto=alternativa_b,
            caminho_imagem=self._obter_caminho_imagem(
                pergunta,
                indice=1
            ),
            cor_cartao=self.COR_B
        )

        cartao_b.save(
            caminho_cartao_b
        )

        imagem_ou = self._carregar_imagem_ou(
            tamanho=(130, 100)
        )

        if imagem_ou is not None:
            selo = Image.new(
                "RGBA",
                (130, 100),
                (0, 0, 0, 0)
            )

            x_ou = (
                selo.width
                - imagem_ou.width
            ) // 2

            y_ou = (
                selo.height
                - imagem_ou.height
            ) // 2

            selo.alpha_composite(
                imagem_ou,
                (x_ou, y_ou)
            )

        else:
            selo = Image.new(
                "RGBA",
                (100, 100),
                (0, 0, 0, 0)
            )

            desenho_selo = ImageDraw.Draw(
                selo
            )

            desenho_selo.ellipse(
                (0, 0, 99, 99),
                fill=self.COR_DESTAQUE,
                outline=(255, 255, 255),
                width=5
            )

            fonte_ou = self._carregar_fonte_negrito(
                34
            )

            caixa = desenho_selo.textbbox(
                (0, 0),
                "OU",
                font=fonte_ou
            )

            largura = caixa[2] - caixa[0]
            altura = caixa[3] - caixa[1]

            desenho_selo.text(
                (
                    50 - largura / 2,
                    50 - altura / 2 - 4
                ),
                "OU",
                font=fonte_ou,
                fill=(45, 34, 72)
            )

        selo.save(
            caminho_selo_ou
        )

    def _carregar_imagem_ou(
        self,
        tamanho=(120, 90)
    ):
        candidatos = [
            Path("assets/ui/ou.png"),
            Path("assets/ou.png"),
            Path("assets/OU.png"),
        ]

        for caminho in candidatos:
            if not caminho.exists():
                continue

            try:
                imagem_ou = Image.open(
                    caminho
                ).convert("RGBA")

                imagem_ou.thumbnail(
                    tamanho,
                    Image.Resampling.LANCZOS
                )

                return imagem_ou

            except OSError:
                continue

        return None

    def _desenhar_ou_personalizado(
        self,
        imagem_base,
        desenho,
        caixa_destino
    ):
        imagem_ou = self._carregar_imagem_ou(
            tamanho=(
                caixa_destino[2]
                - caixa_destino[0],
                caixa_destino[3]
                - caixa_destino[1]
            )
        )

        if imagem_ou is not None:
            centro_x = (
                caixa_destino[0]
                + caixa_destino[2]
            ) // 2

            centro_y = (
                caixa_destino[1]
                + caixa_destino[3]
            ) // 2

            x = int(
                centro_x
                - imagem_ou.width / 2
            )

            y = int(
                centro_y
                - imagem_ou.height / 2
            )

            imagem_base.paste(
                imagem_ou,
                (x, y),
                imagem_ou
            )

            return

        desenho.ellipse(
            caixa_destino,
            fill=self.COR_DESTAQUE,
            outline=(255, 255, 255),
            width=5
        )

        fonte_ou = self._carregar_fonte_negrito(
            34
        )

        caixa = desenho.textbbox(
            (0, 0),
            "OU",
            font=fonte_ou
        )

        largura = caixa[2] - caixa[0]
        altura = caixa[3] - caixa[1]

        centro_x = (
            caixa_destino[0]
            + caixa_destino[2]
        ) / 2

        centro_y = (
            caixa_destino[1]
            + caixa_destino[3]
        ) / 2

        desenho.text(
            (
                centro_x - largura / 2,
                centro_y - altura / 2 - 4
            ),
            "OU",
            font=fonte_ou,
            fill=(45, 34, 72)
        )

    def _desenhar_titulo_pergunta(
        self,
        desenho,
        pergunta
    ):
        texto_pergunta = str(
            pergunta.get(
                "pergunta",
                "O que você prefere?"
            )
        ).strip()

        fonte_pergunta = self._carregar_fonte_negrito(
            42
        )

        y = 154

        for linha in textwrap.wrap(
            texto_pergunta,
            width=42
        )[:2]:
            caixa = desenho.textbbox(
                (0, 0),
                linha,
                font=fonte_pergunta
            )

            largura = caixa[2] - caixa[0]

            desenho.text(
                (
                    (self.largura - largura) / 2,
                    y
                ),
                linha,
                font=fonte_pergunta,
                fill=self.COR_TEXTO
            )

            y += 50

    def definir_preset_automatico(
        self,
        tema
    ):
        self.preset_visual = (
            self.preset_registry
            .selecionar_por_tema(
                tema
            )
        )

        self.confetti_factory.quantidade = (
            self.preset_visual
            .quantidade_confetes
        )

    def definir_preset(
        self,
        nome
    ):
        self.preset_visual = (
            self.preset_registry
            .obter(
                nome
            )
        )

        self.confetti_factory.quantidade = (
            self.preset_visual
            .quantidade_confetes
        )

    @property
    def nome_preset_atual(
        self
    ):
        return self.preset_visual.nome

    def _cores_da_pergunta(
        self,
        numero
    ):
        paletas = (
            self.preset_visual
            .paletas_perguntas
        )

        indice = (
            max(int(numero), 1)
            - 1
        ) % len(paletas)

        return paletas[indice]

    def _aplicar_paleta(
        self,
        numero
    ):
        paleta = self._cores_da_pergunta(
            numero
        )

        self.COR_A = paleta["a"]
        self.COR_B = paleta["b"]
        self.COR_DESTAQUE = (
            paleta["destaque"]
        )

    def _desenhar_progresso(
        self,
        desenho,
        numero
    ):
        """
        Mostra apenas o progresso textual da rodada.

        A barra fixa grande foi removida para evitar conflito visual
        com a barra da contagem regressiva.
        """
        total = max(
            int(
                getattr(
                    self,
                    "total_perguntas_contexto",
                    numero
                )
            ),
            1
        )

        texto = f"{numero}/{total}"
        fonte = self._carregar_fonte_negrito(
            20
        )

        caixa = desenho.textbbox(
            (0, 0),
            texto,
            font=fonte
        )

        largura = caixa[2] - caixa[0]
        altura = caixa[3] - caixa[1]

        # Canto superior esquerdo do rodapé, longe do mascote.
        x = 92
        y = 616

        desenho.rounded_rectangle(
            (
                x - 12,
                y - 7,
                x + largura + 12,
                y + altura + 9
            ),
            radius=12,
            fill=(255, 255, 255)
        )

        desenho.text(
            (x, y),
            texto,
            font=fonte,
            fill=(74, 45, 145)
        )

    def _aplicar_mascote_frente(
        self,
        imagem,
        pose="idle"
    ):
        """
        Cola o mascote por último, sempre à frente de todos os elementos.
        """

        mascote = self.mascot_widget.preparar_pose(
            pose=pose,
            tamanho=(185, 185)
        )

        if mascote is None:
            return imagem

        margem_direita = 28
        margem_inferior = 18

        x = (
            self.largura
            - mascote.width
            - margem_direita
        )

        y = (
            self.altura
            - mascote.height
            - margem_inferior
        )

        imagem.paste(
            mascote,
            (x, y),
            mascote
        )

        return imagem

    def _criar_base(self):
        imagem = Image.new(
            "RGB",
            (self.largura, self.altura),
            self.COR_ESCURO
        )

        desenho = ImageDraw.Draw(imagem)

        cor_inicio = (
            self.preset_visual
            .cor_fundo_inicio
        )

        cor_fim = (
            self.preset_visual
            .cor_fundo_fim
        )

        for y in range(self.altura):
            proporcao = y / max(self.altura - 1, 1)

            cor = tuple(
                int(
                    cor_inicio[indice]
                    + (
                        cor_fim[indice]
                        - cor_inicio[indice]
                    )
                    * proporcao
                )
                for indice in range(3)
            )

            desenho.line(
                (0, y, self.largura, y),
                fill=cor
            )

        # Bolhas decorativas.
        for caixa, cor in [
            ((-120, -80, 280, 320), (130, 90, 220)),
            ((1010, -100, 1390, 280), (70, 120, 230)),
            ((980, 500, 1360, 850), (180, 60, 170)),
            ((-150, 510, 240, 880), (80, 180, 190)),
        ]:
            desenho.ellipse(
                caixa,
                fill=cor
            )

        desenho.rounded_rectangle(
            (34, 28, 1246, 692),
            radius=42,
            fill=(255, 255, 255),
            outline=(255, 255, 255),
            width=3
        )

        desenho.rounded_rectangle(
            (50, 44, 1230, 676),
            radius=34,
            fill=(
                self.preset_visual
                .cor_painel
            )
        )

        return imagem, desenho

    def _desenhar_cabecalho(
        self,
        desenho,
        numero
    ):
        desenho.rounded_rectangle(
            (80, 62, 1200, 132),
            radius=24,
            fill=(255, 255, 255)
        )

        fonte_logo = self._carregar_fonte_negrito(34)
        fonte_numero = self._carregar_fonte_negrito(28)

        desenho.text(
            (110, 79),
            "MOLEZA QUIZ",
            font=fonte_logo,
            fill=(83, 45, 165)
        )

        texto_numero = f"PERGUNTA {numero}"

        caixa = desenho.textbbox(
            (0, 0),
            texto_numero,
            font=fonte_numero
        )

        largura = caixa[2] - caixa[0]

        desenho.rounded_rectangle(
            (
                1160 - largura - 44,
                76,
                1170,
                119
            ),
            radius=18,
            fill=(255, 214, 75)
        )

        desenho.text(
            (
                1148 - largura,
                82
            ),
            texto_numero,
            font=fonte_numero,
            fill=(47, 33, 75)
        )

    def _desenhar_pergunta_e_alternativas(
        self,
        imagem,
        desenho,
        pergunta
    ):
        texto_pergunta = str(
            pergunta.get(
                "pergunta",
                "O que você prefere?"
            )
        ).strip()

        alternativas = pergunta.get(
            "alternativas",
            []
        )

        alternativa_a = (
            str(alternativas[0]).strip()
            if len(alternativas) >= 1
            else "OPÇÃO A"
        )

        alternativa_b = (
            str(alternativas[1]).strip()
            if len(alternativas) >= 2
            else "OPÇÃO B"
        )

        fonte_pergunta = self._carregar_fonte_negrito(42)
        y = 154

        linhas = textwrap.wrap(
            texto_pergunta,
            width=42
        )[:2]

        for linha in linhas:
            caixa = desenho.textbbox(
                (0, 0),
                linha,
                font=fonte_pergunta
            )
            largura = caixa[2] - caixa[0]

            desenho.text(
                (
                    (self.largura - largura) / 2,
                    y
                ),
                linha,
                font=fonte_pergunta,
                fill=self.COR_TEXTO
            )

            y += 50

        topo_cartao = 275
        base_cartao = 535

        desenho.rounded_rectangle(
            (90, topo_cartao, 570, base_cartao),
            radius=34,
            fill=self.COR_A,
            outline=(255, 255, 255),
            width=5
        )

        desenho.rounded_rectangle(
            (710, topo_cartao, 1190, base_cartao),
            radius=34,
            fill=self.COR_B,
            outline=(255, 255, 255),
            width=5
        )

        caminho_imagem_a = self._obter_caminho_imagem(
            pergunta,
            indice=0
        )

        caminho_imagem_b = self._obter_caminho_imagem(
            pergunta,
            indice=1
        )

        self._desenhar_opcao(
            imagem_base=imagem,
            desenho=desenho,
            centro_x=330,
            topo=topo_cartao,
            letra="A",
            texto=alternativa_a,
            caminho_imagem=caminho_imagem_a,
            cor_cartao=self.COR_A
        )

        self._desenhar_opcao(
            imagem_base=imagem,
            desenho=desenho,
            centro_x=950,
            topo=topo_cartao,
            letra="B",
            texto=alternativa_b,
            caminho_imagem=caminho_imagem_b,
            cor_cartao=self.COR_B
        )

        self._desenhar_ou_personalizado(
            imagem_base=imagem,
            desenho=desenho,
            caixa_destino=(
                575,
                325,
                705,
                455
            )
        )

    def _desenhar_opcao(
        self,
        imagem_base,
        desenho,
        centro_x,
        topo,
        letra,
        texto,
        caminho_imagem,
        cor_cartao
    ):
        desenho.ellipse(
            (
                centro_x - 34,
                topo + 18,
                centro_x + 34,
                topo + 86
            ),
            fill=(255, 255, 255)
        )

        fonte_letra = self._carregar_fonte_negrito(34)

        caixa = desenho.textbbox(
            (0, 0),
            letra,
            font=fonte_letra
        )

        largura = caixa[2] - caixa[0]
        altura = caixa[3] - caixa[1]

        desenho.text(
            (
                centro_x - largura / 2,
                topo + 52 - altura / 2 - 4
            ),
            letra,
            font=fonte_letra,
            fill=(54, 38, 91)
        )

        imagem_adicionada = self._colar_imagem_opcao(
            imagem_base=imagem_base,
            caminho_imagem=caminho_imagem,
            centro_x=centro_x,
            topo=topo
        )

        fonte_texto = self._carregar_fonte_negrito(
            27 if imagem_adicionada else 31
        )

        linhas = textwrap.wrap(
            texto,
            width=21 if imagem_adicionada else 19
        )[:2 if imagem_adicionada else 3]

        if imagem_adicionada:
            y = topo + 208
        else:
            altura_total = len(linhas) * 40
            y = topo + 145 - altura_total / 2

        for linha in linhas:
            caixa = desenho.textbbox(
                (0, 0),
                linha,
                font=fonte_texto
            )

            largura = caixa[2] - caixa[0]

            desenho.text(
                (
                    centro_x - largura / 2,
                    y
                ),
                linha,
                font=fonte_texto,
                fill=(255, 255, 255)
            )

            y += 34 if imagem_adicionada else 40

    def _colar_imagem_opcao(
        self,
        imagem_base,
        caminho_imagem,
        centro_x,
        topo
    ) -> bool:
        if caminho_imagem is None:
            return False

        caminho = Path(
            caminho_imagem
        )

        if not caminho.exists() or not caminho.is_file():
            return False

        try:
            imagem_opcao = Image.open(
                caminho
            ).convert("RGBA")

            largura_alvo = 330
            altura_alvo = 118

            imagem_opcao = ImageOps.contain(
                imagem_opcao,
                (
                    largura_alvo,
                    altura_alvo
                ),
                method=Image.Resampling.LANCZOS
            )

            fundo = Image.new(
                "RGBA",
                (
                    largura_alvo,
                    altura_alvo
                ),
                (255, 255, 255, 245)
            )

            x = (
                largura_alvo
                - imagem_opcao.width
            ) // 2

            y = (
                altura_alvo
                - imagem_opcao.height
            ) // 2

            fundo.alpha_composite(
                imagem_opcao,
                (x, y)
            )

            mascara = Image.new(
                "L",
                (
                    largura_alvo,
                    altura_alvo
                ),
                0
            )

            desenho_mascara = ImageDraw.Draw(
                mascara
            )

            desenho_mascara.rounded_rectangle(
                (
                    0,
                    0,
                    largura_alvo - 1,
                    altura_alvo - 1
                ),
                radius=22,
                fill=255
            )

            fundo.putalpha(
                mascara
            )

            destino_x = int(
                centro_x
                - largura_alvo / 2
            )

            destino_y = int(
                topo + 82
            )

            imagem_base.paste(
                fundo,
                (
                    destino_x,
                    destino_y
                ),
                fundo
            )

            return True

        except (
            OSError,
            ValueError
        ):
            return False

    def _obter_caminho_imagem(
        self,
        pergunta,
        indice
    ):
        campos_por_indice = {
            0: (
                "imagem_a",
                "imagem_esquerda",
                "imagem_opcao_a",
                "imagem_1"
            ),
            1: (
                "imagem_b",
                "imagem_direita",
                "imagem_opcao_b",
                "imagem_2"
            )
        }

        for campo in campos_por_indice.get(
            indice,
            ()
        ):
            valor = pergunta.get(
                campo
            )

            if valor:
                return valor

        imagens = pergunta.get(
            "imagens",
            []
        )

        if (
            isinstance(imagens, list)
            and indice < len(imagens)
            and imagens[indice]
        ):
            return imagens[indice]

        return None

    def _criar_frame_pergunta(
        self,
        caminho,
        numero,
        pergunta
    ):
        self._aplicar_paleta(
            numero
        )

        imagem, desenho = self._criar_base()

        self._desenhar_cabecalho(
            desenho,
            numero
        )

        self._desenhar_pergunta_e_alternativas(
            imagem,
            desenho,
            pergunta
        )

        self._desenhar_rodape(
            desenho,
            "ESCOLHA RÁPIDO!"
        )

        imagem = self._aplicar_mascote_frente(
            imagem,
            pose="idle"
        )

        self._desenhar_progresso(
            desenho,
            numero
        )

        imagem.save(caminho)

    def _criar_frame_contagem(
        self,
        caminho,
        numero,
        pergunta,
        contador
    ):
        self._aplicar_paleta(
            numero
        )

        imagem, desenho = self._criar_base()

        self._desenhar_cabecalho(
            desenho,
            numero
        )

        self._desenhar_pergunta_e_alternativas(
            imagem,
            desenho,
            pergunta
        )

        centro_x = 640
        centro_y = 600
        raio = 52

        desenho.ellipse(
            (
                centro_x - raio,
                centro_y - raio,
                centro_x + raio,
                centro_y + raio
            ),
            fill=(255, 255, 255),
            outline=self.COR_DESTAQUE,
            width=8
        )

        fonte_contador = self._carregar_fonte_negrito(46)
        texto = str(contador)

        caixa = desenho.textbbox(
            (0, 0),
            texto,
            font=fonte_contador
        )

        largura = caixa[2] - caixa[0]
        altura = caixa[3] - caixa[1]

        desenho.text(
            (
                centro_x - largura / 2,
                centro_y - altura / 2 - 5
            ),
            texto,
            font=fonte_contador,
            fill=(67, 43, 120)
        )

        imagem = self._aplicar_mascote_frente(
            imagem,
            pose="thinking"
        )

        self._desenhar_progresso(
            desenho,
            numero
        )

        imagem.save(caminho)

    def _criar_frame_escolha(
        self,
        caminho,
        numero,
        pergunta
    ):
        self._aplicar_paleta(
            numero
        )

        imagem, desenho = self._criar_base()

        self._desenhar_cabecalho(
            desenho,
            numero
        )

        desenho.rounded_rectangle(
            (120, 195, 1160, 545),
            radius=45,
            fill=(113, 68, 200),
            outline=(255, 255, 255),
            width=5
        )

        fonte_titulo = self._carregar_fonte_negrito(60)
        fonte_subtitulo = self._carregar_fonte_negrito(42)
        fonte_comentario = self._carregar_fonte_negrito(28)

        self._texto_centralizado(
            desenho,
            "TEMPO ESGOTADO!",
            y=270,
            fonte=fonte_titulo,
            cor=self.COR_DESTAQUE
        )

        self._texto_centralizado(
            desenho,
            "QUAL VOCÊ ESCOLHEU?",
            y=370,
            fonte=fonte_subtitulo,
            cor=(255, 255, 255)
        )

        self._texto_centralizado(
            desenho,
            "CONTE NOS COMENTÁRIOS!",
            y=470,
            fonte=fonte_comentario,
            cor=(235, 225, 255)
        )

        self._desenhar_rodape(
            desenho,
            "A ESCOLHA É TODA SUA!"
        )

        # O frame-base do resultado deve ser salvo sem mascote.
        # O mascote celebrate é adicionado depois pela animação,
        # evitando que uma cópia estática apareça por baixo.
        self._desenhar_progresso(
            desenho,
            numero
        )

        imagem.save(caminho)

    def _desenhar_rodape(
        self,
        desenho,
        texto
    ):
        fonte = self._carregar_fonte_negrito(25)

        caixa = desenho.textbbox(
            (0, 0),
            texto,
            font=fonte
        )

        largura = caixa[2] - caixa[0]

        desenho.rounded_rectangle(
            (
                640 - largura / 2 - 28,
                575,
                640 + largura / 2 + 28,
                625
            ),
            radius=18,
            fill=(255, 255, 255)
        )

        desenho.text(
            (
                640 - largura / 2,
                584
            ),
            texto,
            font=fonte,
            fill=(74, 45, 145)
        )

    def _texto_centralizado(
        self,
        desenho,
        texto,
        y,
        fonte,
        cor
    ):
        caixa = desenho.textbbox(
            (0, 0),
            texto,
            font=fonte
        )

        largura = caixa[2] - caixa[0]

        desenho.text(
            (
                (self.largura - largura) / 2,
                y
            ),
            texto,
            font=fonte,
            fill=cor
        )

    def _carregar_fonte_negrito(
        self,
        tamanho
    ):
        fontes = [
            Path("C:/Windows/Fonts/arialbd.ttf"),
            Path("C:/Windows/Fonts/calibrib.ttf"),
            Path("C:/Windows/Fonts/seguisb.ttf"),
        ]

        for caminho in fontes:
            if caminho.exists():
                return ImageFont.truetype(
                    str(caminho),
                    tamanho
                )

        return self._carregar_fonte(
            tamanho
        )
