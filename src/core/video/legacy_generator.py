from datetime import datetime
from pathlib import Path
import math
import textwrap

from PIL import Image, ImageDraw, ImageFont

from .audio_sync import AudioSyncDirector
from .execution import ExecutionSettings
from .attention import (
    PatternBreakDirector,
    ViewerAttentionAnalyzer,
)
from .opening import OpeningDirector, OpeningStudio
from .outro import OutroStudio
from .universal.legacy_motion import (
    UniversalLegacyMotionRenderer,
)
from .universal.scene_renderer import (
    UniversalSceneRenderer,
)

from moviepy import (
    AudioFileClip,
    CompositeAudioClip,
    ImageClip,
    concatenate_audioclips,
    concatenate_videoclips
)


class LegacyVideoGenerator:

    def __init__(self):
        self.largura = 1280
        self.altura = 720
        self.fps = 30

        self.universal_visual_context = {
            "theme_pack": {
                "code": "moleza_vibrant",
                "name": "Moleza Vibrante",
                "background_top": [90, 55, 180],
                "background_bottom": [35, 28, 92],
                "panel_color": [245, 240, 255],
                "primary_color": [115, 70, 205],
                "secondary_color": [255, 95, 135],
                "accent_color": [255, 215, 65],
                "text_color": [55, 35, 95],
                "particle_style": "sparkles",
                "background_activity": 0.55,
                "motion_intensity": 0.50,
            }
        }

        self.legacy_motion = (
            UniversalLegacyMotionRenderer(
                largura=self.largura,
                altura=self.altura,
                fps=18,
            )
        )

        self.universal_scene_renderer = (
            UniversalSceneRenderer(
                width=self.largura,
                height=self.altura,
                fps=18,
            )
        )

        self.total_perguntas_contexto = 1

        self.opening_director = OpeningDirector()
        self.opening_studio = OpeningStudio(
            largura=self.largura,
            altura=self.altura,
            fps=18,
        )

        self.outro_studio = OutroStudio(
            width=self.largura,
            height=self.altura,
            fps=18,
        )

        self.audio_sync = AudioSyncDirector()
        self.pattern_break_director = (
            PatternBreakDirector()
        )
        self.viewer_attention = (
            ViewerAttentionAnalyzer()
        )

        self.execution_settings = ExecutionSettings(
            theme_pack=dict(
                self.universal_visual_context[
                    "theme_pack"
                ]
            ),
            opening_enabled=True,
            opening_duration=4.2,
            question_entry_duration=0.90,
            reveal_duration=1.90,
            pattern_breaks_enabled=True,
            pattern_break_interval=4,
            pattern_break_intensity=0.82,
            mascot_enabled=True,
            mascot_intensity=0.80,
            audio_sync_enabled=True,
            outro_enabled=True,
            outro_duration=5.0,
            quality_profile="balanced",
        )

    def configurar_plano_producao(
        self,
        settings,
    ):
        self.execution_settings = settings

        self.universal_visual_context[
            "theme_pack"
        ] = dict(
            settings.theme_pack
        )

        self.universal_scene_renderer.configure_execution(
            settings
        )

    def configurar_direcao_universal(
        self,
        creative_plan,
    ):
        self.universal_visual_context = dict(
            creative_plan or {}
        )

    def _theme_pack(self):
        execution_pack = getattr(
            self.execution_settings,
            "theme_pack",
            {}
        )

        if execution_pack:
            return dict(
                execution_pack
            )

        return dict(
            self.universal_visual_context.get(
                "theme_pack",
                {}
            )
        )

    def _criar_clip_abertura_profissional(
        self,
        titulo,
        quantidade,
        pasta_frames,
    ):
        retention_plan = dict(
            self.universal_visual_context.get(
                "retention_plan",
                {}
            )
        )

        direction = (
            self.opening_director
            .escolher(
                titulo=titulo,
                total_perguntas=quantidade,
                retention_plan=retention_plan,
            )
        )

        pack = self._theme_pack()

        class ThemeProxy:
            codigo = pack.get(
                "code",
                "moleza_vibrante"
            )

        clip = self.opening_studio.criar_clip(
            titulo=titulo,
            direcao=direction,
            brand_direction=dict(
                self.universal_visual_context.get(
                    "brand_direction",
                    {}
                )
            ),
            premium_theme=ThemeProxy(),
        )

        target_duration = float(
            self.execution_settings
            .opening_duration
        )

        clip = clip.with_duration(
            target_duration
        )

        return {
            "clip": clip,
            "duracao": target_duration,
        }

    def _clip_frame_animado(
        self,
        caminho,
        duracao,
        tipo_cena,
        numero=0,
    ):
        self.legacy_motion.largura = (
            self.largura
        )
        self.legacy_motion.altura = (
            self.altura
        )

        return self.legacy_motion.create_clip(
            image_path=caminho,
            duration=duracao,
            scene_kind=tipo_cena,
            theme_pack=self._theme_pack(),
            question_number=numero,
        )

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
        texto_encerramento=(
            "Comente quantos pontos você fez!"
        ),
        incluir_abertura=True,
        incluir_encerramento=True,
        callback_progresso=None
    ):
        pasta_projeto = Path(pasta_projeto)

        pasta_frames = (
            pasta_projeto
            / "videos"
            / "frames"
        )

        pasta_audios = (
            pasta_projeto
            / "audios"
        )

        pasta_exportado = (
            pasta_projeto
            / "exportado"
        )

        pasta_frames.mkdir(
            parents=True,
            exist_ok=True
        )

        pasta_exportado.mkdir(
            parents=True,
            exist_ok=True
        )

        if not perguntas:
            raise ValueError(
                "O projeto não possui perguntas."
            )

        if limite_perguntas is None:
            perguntas_selecionadas = perguntas
        else:
            perguntas_selecionadas = perguntas[
                :limite_perguntas
            ]

        total_perguntas = len(
            perguntas_selecionadas
        )

        self.total_perguntas_contexto = max(
            total_perguntas,
            1
        )

        pattern_break_questions = [
            number
            for number in range(
                1,
                self.total_perguntas_contexto + 1
            )
            if (
                self.pattern_break_director
                .decide(
                    question_number=number,
                    total_questions=(
                        self.total_perguntas_contexto
                    ),
                    scene_kind="question",
                    interval_override=(
                        self.execution_settings
                        .pattern_break_interval
                    ),
                    enabled=(
                        self.execution_settings
                        .pattern_breaks_enabled
                    ),
                    intensity_override=(
                        self.execution_settings
                        .pattern_break_intensity
                    ),
                )
                .active
            )
        ]

        attention_report = (
            self.viewer_attention
            .analyze(
                total_questions=(
                    self.total_perguntas_contexto
                ),
                pattern_break_questions=(
                    pattern_break_questions
                ),
                theme_pack=self._theme_pack(),
            )
        )

        self.viewer_attention.save(
            attention_report,
            (
                pasta_projeto
                / "videos"
                / "relatorios"
                / "viewer_attention_report.json"
            ),
        )

        clips_video = []
        clips_narracao = []

        video_final = None
        video_com_audio = None

        audio_musica_original = None
        audio_musica_repetido = None
        audio_musica_final = None
        audio_composto = None

        tempo_atual = 0.0

        try:

            # ==================================
            # ABERTURA
            # ==================================

            if (
                incluir_abertura
                and self.execution_settings.opening_enabled
            ):
                self._informar_progresso(
                    callback_progresso,
                    0,
                    total_perguntas,
                    "Criando tela de abertura..."
                )

                if hasattr(
                    self,
                    "_criar_clip_abertura_profissional"
                ):
                    resultado_abertura = (
                        self
                        ._criar_clip_abertura_profissional(
                            titulo=titulo_quiz,
                            quantidade=total_perguntas,
                            pasta_frames=pasta_frames
                        )
                    )

                    clips_video.append(
                        resultado_abertura[
                            "clip"
                        ]
                    )

                    duracao_abertura = float(
                        resultado_abertura[
                            "duracao"
                        ]
                    )

                else:
                    caminho_abertura = (
                        pasta_frames
                        / "abertura.png"
                    )

                    self._criar_frame_abertura(
                        caminho=caminho_abertura,
                        titulo=titulo_quiz,
                        quantidade=total_perguntas
                    )

                    duracao_abertura = 3

                    clips_video.append(
                        ImageClip(
                            str(caminho_abertura)
                        ).with_duration(
                            duracao_abertura
                        )
                    )

                tempo_atual += duracao_abertura

            # ==================================
            # PERGUNTAS
            # ==================================

            for numero, pergunta in enumerate(
                perguntas_selecionadas,
                start=1
            ):
                self._informar_progresso(
                    callback_progresso,
                    numero - 1,
                    total_perguntas,
                    (
                        f"Criando pergunta "
                        f"{numero} de "
                        f"{total_perguntas}..."
                    )
                )

                resultado = (
                    self._criar_clips_da_pergunta(
                        pasta_frames=pasta_frames,
                        pasta_audios=pasta_audios,
                        numero=numero,
                        pergunta=pergunta,
                        tempo_resposta=tempo_resposta,
                        tempo_inicio=tempo_atual,
                        usar_narracao=usar_narracao,
                        volume_narracao=volume_narracao,
                        pasta_projeto=pasta_projeto
                    )
                )

                clips_video.extend(
                    resultado["clips_video"]
                )

                clips_narracao.extend(
                    resultado["clips_audio"]
                )

                tempo_atual += resultado[
                    "duracao_total"
                ]

            # ==================================
            # ENCERRAMENTO
            # ==================================

            if (
                incluir_encerramento
                and self.execution_settings.outro_enabled
            ):
                self._informar_progresso(
                    callback_progresso,
                    total_perguntas,
                    total_perguntas,
                    "Criando tela de encerramento..."
                )

                duracao_encerramento = float(
                    self.execution_settings
                    .outro_duration
                )

                clips_video.append(
                    self.outro_studio.create_clip(
                        text=texto_encerramento,
                        duration=duracao_encerramento,
                        theme_pack=self._theme_pack(),
                    )
                )

                tempo_atual += duracao_encerramento

            # ==================================
            # MONTAGEM DO VÍDEO
            # ==================================

            self._informar_progresso(
                callback_progresso,
                total_perguntas,
                total_perguntas,
                "Montando o vídeo final..."
            )

            video_final = concatenate_videoclips(
                clips_video,
                method="compose"
            )

            fontes_audio = []

            # ==================================
            # MÚSICA DE FUNDO
            # ==================================

            if caminho_musica:
                self._informar_progresso(
                    callback_progresso,
                    total_perguntas,
                    total_perguntas,
                    "Preparando música de fundo..."
                )

                caminho_musica = Path(
                    caminho_musica
                )

                if not caminho_musica.exists():
                    raise FileNotFoundError(
                        "O arquivo de música "
                        "não foi encontrado."
                    )

                audio_musica_original = (
                    AudioFileClip(
                        str(caminho_musica)
                    )
                )

                audio_musica_repetido = (
                    self._preparar_musica(
                        audio_original=(
                            audio_musica_original
                        ),
                        duracao_video=(
                            video_final.duration
                        )
                    )
                )

                audio_musica_final = (
                    audio_musica_repetido
                    .with_volume_scaled(
                        volume_musica
                    )
                )

                fontes_audio.append(
                    audio_musica_final
                )

            # ==================================
            # NARRAÇÕES
            # ==================================

            fontes_audio.extend(
                clips_narracao
            )

            if fontes_audio:
                self._informar_progresso(
                    callback_progresso,
                    total_perguntas,
                    total_perguntas,
                    "Misturando música e narração..."
                )

                audio_composto = CompositeAudioClip(
                    fontes_audio
                ).with_duration(
                    video_final.duration
                )

                video_com_audio = (
                    video_final.with_audio(
                        audio_composto
                    )
                )

                video_para_exportar = (
                    video_com_audio
                )

            else:
                video_para_exportar = (
                    video_final
                )

            # ==================================
            # EXPORTAÇÃO
            # ==================================

            data_hora = datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )

            caminho_saida = (
                pasta_exportado
                / (
                    "moleza_quiz_"
                    f"{data_hora}.mp4"
                )
            )

            self._informar_progresso(
                callback_progresso,
                total_perguntas,
                total_perguntas,
                "Renderizando arquivo MP4..."
            )

            video_para_exportar.write_videofile(
                str(caminho_saida),
                fps=self.fps,
                codec="libx264",
                audio_codec="aac",
                audio=bool(fontes_audio),
                preset="medium",
                threads=4,
                logger=None
            )

            self._informar_progresso(
                callback_progresso,
                total_perguntas,
                total_perguntas,
                "Vídeo concluído."
            )

            return caminho_saida

        finally:
            if video_com_audio is not None:
                video_com_audio.close()

            if audio_composto is not None:
                audio_composto.close()

            for clip_audio in clips_narracao:
                clip_audio.close()

            if audio_musica_final is not None:
                audio_musica_final.close()

            if audio_musica_repetido is not None:
                audio_musica_repetido.close()

            if audio_musica_original is not None:
                audio_musica_original.close()

            if video_final is not None:
                video_final.close()

            for clip_video in clips_video:
                clip_video.close()

    def _criar_clips_da_pergunta(
        self,
        pasta_frames,
        pasta_audios,
        numero,
        pergunta,
        tempo_resposta,
        tempo_inicio,
        usar_narracao,
        volume_narracao,
        pasta_projeto
    ):
        clips_video = []
        clips_audio = []

        caminho_audio_pergunta = (
            pasta_audios
            / f"pergunta_{numero:03d}.mp3"
        )

        caminho_audio_resposta = (
            pasta_audios
            / f"resposta_{numero:03d}.mp3"
        )

        caminho_audio_escolha = (
            pasta_audios
            / f"escolha_{numero:03d}.mp3"
        )

        audio_pergunta = None
        audio_resposta = None
        audio_escolha = None

        # O plano define o ritmo mínimo, mas nunca corta a narração.
        duracao_pergunta = max(
            float(
                self.execution_settings
                .question_entry_duration
            ),
            0.65
        )

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
                float(
                    self.execution_settings
                    .question_entry_duration
                )
            )

            clips_audio.append(
                audio_pergunta.with_start(
                    tempo_inicio
                )
            )

        clips_video.append(
            self.universal_scene_renderer
            .create_knowledge_clip(
                question=pergunta,
                question_number=numero,
                total_questions=(
                    self.total_perguntas_contexto
                ),
                duration=duracao_pergunta,
                scene_kind="question",
                theme_pack=self._theme_pack(),
            )
        )

        tempo_depois_pergunta = (
            tempo_inicio + duracao_pergunta
        )

        # Contagem regressiva.
        for contador in range(
            tempo_resposta,
            0,
            -1
        ):
            clips_video.append(
                self.universal_scene_renderer
                .create_knowledge_clip(
                    question=pergunta,
                    question_number=numero,
                    total_questions=(
                        self.total_perguntas_contexto
                    ),
                    duration=1.0,
                    scene_kind="countdown",
                    theme_pack=self._theme_pack(),
                    countdown_value=contador,
                    countdown_maximum=tempo_resposta,
                )
            )

        tempo_inicio_resposta = (
            tempo_depois_pergunta
            + tempo_resposta
        )

        quiz_preferencia = self._eh_quiz_preferencia(
            pergunta
        )

        if quiz_preferencia:
            duracao_resposta = float(
                self.execution_settings
                .reveal_duration
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

                duracao_resposta = max(
                    audio_escolha.duration + 0.5,
                    float(
                        self.execution_settings
                        .reveal_duration
                    )
                )

                clips_audio.append(
                    audio_escolha.with_start(
                        tempo_inicio_resposta
                    )
                )

            caminho_frame_resposta = (
                pasta_frames
                / (
                    f"pergunta_{numero:03d}"
                    "_escolha.png"
                )
            )

            self._criar_frame_escolha(
                caminho=caminho_frame_resposta,
                numero=numero,
                pergunta=pergunta
            )

            clips_video.append(
                self._clip_frame_animado(
                    caminho=caminho_frame_resposta,
                    duracao=duracao_resposta,
                    tipo_cena="reveal",
                    numero=numero,
                )
            )

        else:
            # A resposta segue o plano, sem cortar a narração.
            duracao_resposta = float(
                self.execution_settings
                .reveal_duration
            )

            if (
                usar_narracao
                and caminho_audio_resposta.exists()
            ):
                audio_resposta = AudioFileClip(
                    str(caminho_audio_resposta)
                ).with_volume_scaled(
                    volume_narracao
                )

                duracao_resposta = max(
                    audio_resposta.duration + 0.5,
                    float(
                        self.execution_settings
                        .reveal_duration
                    )
                )

                clips_audio.append(
                    audio_resposta.with_start(
                        tempo_inicio_resposta
                    )
                )

            clips_video.append(
                self.universal_scene_renderer
                .create_knowledge_clip(
                    question=pergunta,
                    question_number=numero,
                    total_questions=(
                        self.total_perguntas_contexto
                    ),
                    duration=duracao_resposta,
                    scene_kind="reveal",
                    theme_pack=self._theme_pack(),
                )
            )

        if self.execution_settings.audio_sync_enabled:
            audio_cues = (
                self.audio_sync
                .build_question_cues(
                    project_root=pasta_projeto,
                    question_number=numero,
                    total_questions=(
                        self.total_perguntas_contexto
                    ),
                    question_start=tempo_inicio,
                    question_duration=duracao_pergunta,
                    response_time=tempo_resposta,
                    reveal_duration=duracao_resposta,
                )
            )

            clips_audio.extend(
                self.audio_sync.create_clips(
                    audio_cues
                )
            )

        duracao_total = (
            duracao_pergunta
            + tempo_resposta
            + duracao_resposta
        )

        return {
            "clips_video": clips_video,
            "clips_audio": clips_audio,
            "duracao_total": duracao_total
        }

    def _preparar_musica(
        self,
        audio_original,
        duracao_video
    ):
        if not audio_original.duration:
            raise ValueError(
                "Não foi possível identificar "
                "a duração da música."
            )

        if audio_original.duration >= duracao_video:
            return audio_original.subclipped(
                0,
                duracao_video
            )

        quantidade_repeticoes = math.ceil(
            duracao_video
            / audio_original.duration
        )

        repeticoes = [
            audio_original
            for _ in range(
                quantidade_repeticoes
            )
        ]

        audio_repetido = (
            concatenate_audioclips(
                repeticoes
            )
        )

        return audio_repetido.subclipped(
            0,
            duracao_video
        )

    def _informar_progresso(
        self,
        callback,
        atual,
        total,
        mensagem
    ):
        if callback is not None:
            callback(
                atual,
                total,
                mensagem
            )

    def _criar_frame_abertura(
        self,
        caminho,
        titulo,
        quantidade
    ):
        imagem = Image.new(
            "RGB",
            (self.largura, self.altura),
            (24, 66, 42)
        )

        desenho = ImageDraw.Draw(imagem)

        desenho.rounded_rectangle(
            (90, 70, 1190, 650),
            radius=45,
            fill=(240, 245, 236)
        )

        fonte_logo = self._carregar_fonte(42)
        fonte_titulo = self._carregar_fonte(60)
        fonte_subtitulo = self._carregar_fonte(31)

        desenho.text(
            (150, 120),
            "MOLEZA QUIZ",
            font=fonte_logo,
            fill=(35, 100, 60)
        )

        y = 250

        for linha in textwrap.wrap(
            titulo,
            width=28
        ):
            caixa = desenho.textbbox(
                (0, 0),
                linha,
                font=fonte_titulo
            )

            largura = caixa[2] - caixa[0]

            x = (
                self.largura - largura
            ) / 2

            desenho.text(
                (x, y),
                linha,
                font=fonte_titulo,
                fill=(30, 45, 35)
            )

            y += 75

        texto_quantidade = (
            f"{quantidade} perguntas"
        )

        caixa = desenho.textbbox(
            (0, 0),
            texto_quantidade,
            font=fonte_subtitulo
        )

        largura = caixa[2] - caixa[0]

        desenho.text(
            (
                (self.largura - largura) / 2,
                500
            ),
            texto_quantidade,
            font=fonte_subtitulo,
            fill=(70, 90, 75)
        )

        desenho.text(
            (360, 570),
            "Prepare-se e boa sorte!",
            font=fonte_subtitulo,
            fill=(35, 100, 60)
        )

        imagem.save(caminho)

    def _criar_frame_encerramento(
        self,
        caminho,
        texto
    ):
        imagem = Image.new(
            "RGB",
            (self.largura, self.altura),
            (24, 66, 42)
        )

        desenho = ImageDraw.Draw(imagem)

        desenho.rounded_rectangle(
            (90, 70, 1190, 650),
            radius=45,
            fill=(240, 245, 236)
        )

        fonte_titulo = self._carregar_fonte(58)
        fonte_texto = self._carregar_fonte(36)
        fonte_botao = self._carregar_fonte(30)

        desenho.text(
            (350, 150),
            "FIM DO QUIZ!",
            font=fonte_titulo,
            fill=(35, 100, 60)
        )

        y = 290

        for linha in textwrap.wrap(
            texto,
            width=38
        ):
            caixa = desenho.textbbox(
                (0, 0),
                linha,
                font=fonte_texto
            )

            largura = caixa[2] - caixa[0]

            desenho.text(
                (
                    (self.largura - largura) / 2,
                    y
                ),
                linha,
                font=fonte_texto,
                fill=(35, 45, 38)
            )

            y += 50

        desenho.rounded_rectangle(
            (390, 470, 890, 555),
            radius=20,
            fill=(45, 135, 75)
        )

        desenho.text(
            (455, 490),
            "INSCREVA-SE NO CANAL",
            font=fonte_botao,
            fill=(255, 255, 255)
        )

        desenho.text(
            (355, 590),
            "Até o próximo desafio!",
            font=fonte_texto,
            fill=(35, 100, 60)
        )

        imagem.save(caminho)

    def _criar_frame_pergunta(
        self,
        caminho,
        numero,
        pergunta
    ):
        imagem, desenho = self._criar_base()

        self._desenhar_cabecalho(
            desenho,
            numero
        )

        self._desenhar_pergunta_e_alternativas(
            desenho,
            pergunta
        )

        texto_rodape = (
            "Escolha a opção que você mais prefere!"
            if self._eh_quiz_preferencia(pergunta)
            else "Ouça a pergunta e prepare sua resposta!"
        )

        desenho.text(
            (100, 625),
            texto_rodape,
            font=self._carregar_fonte(24),
            fill=(65, 90, 70)
        )

        imagem.save(caminho)

    def _criar_frame_contagem(
        self,
        caminho,
        numero,
        pergunta,
        contador
    ):
        imagem, desenho = self._criar_base()

        self._desenhar_cabecalho(
            desenho,
            numero
        )

        self._desenhar_pergunta_e_alternativas(
            desenho,
            pergunta
        )

        desenho.ellipse(
            (1080, 545, 1190, 655),
            fill=(35, 110, 65)
        )

        fonte_contador = self._carregar_fonte(55)
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
                1135 - (largura / 2),
                600 - (altura / 2) - 8
            ),
            texto,
            font=fonte_contador,
            fill=(255, 255, 255)
        )

        texto_rodape = (
            "Faça sua escolha antes que o tempo acabe!"
            if self._eh_quiz_preferencia(pergunta)
            else "Responda antes que o tempo acabe!"
        )

        desenho.text(
            (100, 625),
            texto_rodape,
            font=self._carregar_fonte(24),
            fill=(65, 90, 70)
        )

        imagem.save(caminho)

    def _criar_frame_escolha(
        self,
        caminho,
        numero,
        pergunta
    ):
        imagem, desenho = self._criar_base()

        self._desenhar_cabecalho(
            desenho,
            numero
        )

        texto_pergunta = pergunta.get(
            "pergunta",
            "Pergunta sem texto"
        )

        fonte_pergunta = self._carregar_fonte(
            38
        )

        y = 165

        for linha in textwrap.wrap(
            texto_pergunta,
            width=48
        ):
            desenho.text(
                (100, y),
                linha,
                font=fonte_pergunta,
                fill=(25, 25, 25)
            )

            y += 48

        desenho.rounded_rectangle(
            (100, 360, 1180, 545),
            radius=30,
            fill=(113, 68, 200)
        )

        titulo = "TEMPO ESGOTADO!"

        caixa = desenho.textbbox(
            (0, 0),
            titulo,
            font=self._carregar_fonte(48)
        )

        largura = caixa[2] - caixa[0]

        desenho.text(
            (
                (self.largura - largura) / 2,
                395
            ),
            titulo,
            font=self._carregar_fonte(48),
            fill=(255, 255, 255)
        )

        subtitulo = "QUAL VOCÊ ESCOLHEU?"

        caixa = desenho.textbbox(
            (0, 0),
            subtitulo,
            font=self._carregar_fonte(28)
        )

        largura = caixa[2] - caixa[0]

        desenho.text(
            (
                (self.largura - largura) / 2,
                475
            ),
            subtitulo,
            font=self._carregar_fonte(28),
            fill=(238, 229, 255)
        )

        desenho.text(
            (100, 625),
            "Conte sua escolha nos comentários!",
            font=self._carregar_fonte(25),
            fill=(65, 90, 70)
        )

        imagem.save(
            caminho
        )

    def _criar_frame_resposta(
        self,
        caminho,
        numero,
        pergunta
    ):
        imagem, desenho = self._criar_base()

        self._desenhar_cabecalho(
            desenho,
            numero
        )

        texto_pergunta = pergunta.get(
            "pergunta",
            "Pergunta sem texto"
        )

        fonte_pergunta = self._carregar_fonte(40)

        y = 175

        for linha in textwrap.wrap(
            texto_pergunta,
            width=48
        ):
            desenho.text(
                (100, y),
                linha,
                font=fonte_pergunta,
                fill=(25, 25, 25)
            )

            y += 50

        resposta = self._formatar_resposta(
            pergunta
        )

        desenho.rounded_rectangle(
            (100, 380, 1180, 535),
            radius=25,
            fill=(45, 135, 75)
        )

        desenho.text(
            (140, 405),
            "RESPOSTA CORRETA:",
            font=self._carregar_fonte(31),
            fill=(225, 245, 230)
        )

        y_resposta = 455

        for linha in textwrap.wrap(
            resposta,
            width=42
        ):
            desenho.text(
                (140, y_resposta),
                linha,
                font=self._carregar_fonte(38),
                fill=(255, 255, 255)
            )

            y_resposta += 45

        desenho.text(
            (100, 625),
            "Você acertou? Some um ponto!",
            font=self._carregar_fonte(25),
            fill=(65, 90, 70)
        )

        imagem.save(caminho)

    def _criar_base(self):
        pack = self._theme_pack()

        background_top = tuple(
            pack.get(
                "background_top",
                (90, 55, 180)
            )
        )

        background_bottom = tuple(
            pack.get(
                "background_bottom",
                (35, 28, 92)
            )
        )

        panel_color = tuple(
            pack.get(
                "panel_color",
                (245, 240, 255)
            )
        )

        imagem = Image.new(
            "RGB",
            (self.largura, self.altura),
            background_bottom
        )

        desenho = ImageDraw.Draw(imagem)

        for y in range(self.altura):
            progress = y / max(
                self.altura - 1,
                1
            )

            color = tuple(
                int(
                    background_top[index]
                    + (
                        background_bottom[index]
                        - background_top[index]
                    )
                    * progress
                )
                for index in range(3)
            )

            desenho.line(
                (0, y, self.largura, y),
                fill=color
            )

        desenho.rounded_rectangle(
            (60, 45, 1220, 675),
            radius=35,
            fill=panel_color
        )

        return imagem, desenho

    def _desenhar_cabecalho(
        self,
        desenho,
        numero
    ):
        desenho.text(
            (100, 85),
            (
                "MOLEZA QUIZ — "
                f"PERGUNTA {numero}"
            ),
            font=self._carregar_fonte(45),
            fill=tuple(
                self._theme_pack().get(
                    "primary_color",
                    (35, 85, 55)
                )
            )
        )

    def _desenhar_pergunta_e_alternativas(
        self,
        desenho,
        pergunta
    ):
        texto_pergunta = pergunta.get(
            "pergunta",
            "Pergunta sem texto"
        )

        alternativas = pergunta.get(
            "alternativas",
            []
        )

        fonte_pergunta = self._carregar_fonte(38)
        fonte_alternativa = self._carregar_fonte(28)

        y = 170

        for linha in textwrap.wrap(
            texto_pergunta,
            width=50
        ):
            desenho.text(
                (100, y),
                linha,
                font=fonte_pergunta,
                fill=(25, 25, 25)
            )

            y += 48

        y += 20

        for indice, alternativa in enumerate(
            alternativas[:4]
        ):
            letra = chr(65 + indice)

            desenho.rounded_rectangle(
                (100, y, 1020, y + 55),
                radius=15,
                fill=(220, 230, 220)
            )

            desenho.text(
                (125, y + 10),
                f"{letra}) {alternativa}",
                font=fonte_alternativa,
                fill=(30, 30, 30)
            )

            y += 66

    def _eh_quiz_preferencia(
        self,
        pergunta
    ) -> bool:
        tipo = str(
            pergunta.get(
                "tipo_quiz",
                ""
            )
        ).strip().lower()

        if tipo == "preferencia":
            return True

        resposta = pergunta.get(
            "resposta",
            ""
        )

        return not str(
            resposta
        ).strip()

    def _formatar_resposta(
        self,
        pergunta
    ):
        resposta = pergunta.get(
            "resposta",
            "Resposta não informada"
        )

        alternativas = pergunta.get(
            "alternativas",
            []
        )

        if isinstance(resposta, int):
            indice = resposta

            if 1 <= indice <= len(alternativas):
                indice -= 1

            if 0 <= indice < len(alternativas):
                letra = chr(65 + indice)

                return (
                    f"{letra}) "
                    f"{alternativas[indice]}"
                )

        resposta_texto = str(
            resposta
        ).strip()

        if len(resposta_texto) == 1:
            letra = resposta_texto.upper()

            if letra in "ABCD":
                indice = ord(letra) - 65

                if indice < len(alternativas):
                    return (
                        f"{letra}) "
                        f"{alternativas[indice]}"
                    )

        return resposta_texto

    def _carregar_fonte(
        self,
        tamanho
    ):
        fontes_possiveis = [
            Path("C:/Windows/Fonts/arial.ttf"),
            Path("C:/Windows/Fonts/calibri.ttf"),
            Path("C:/Windows/Fonts/segoeui.ttf")
        ]

        for caminho_fonte in fontes_possiveis:
            if caminho_fonte.exists():
                return ImageFont.truetype(
                    str(caminho_fonte),
                    tamanho
                )

        return ImageFont.load_default()
