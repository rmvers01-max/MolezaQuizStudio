from datetime import datetime
from pathlib import Path
import math
import textwrap

from PIL import Image, ImageDraw, ImageFont

from moviepy import (
    AudioFileClip,
    ImageClip,
    concatenate_audioclips,
    concatenate_videoclips
)


class VideoGenerator:

    def __init__(self):
        self.largura = 1280
        self.altura = 720
        self.fps = 30

    def gerar_video(
        self,
        pasta_projeto,
        perguntas,
        tempo_resposta=5,
        limite_perguntas=None,
        caminho_musica=None,
        volume_musica=0.15,
        titulo_quiz="Moleza Quiz",
        texto_encerramento=(
            "Comente quantos pontos você fez!"
        ),
        incluir_abertura=True,
        incluir_encerramento=True,
        callback_progresso=None
    ):
        pasta_projeto = Path(
            pasta_projeto
        )

        pasta_frames = (
            pasta_projeto
            / "videos"
            / "frames"
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

        clips_video = []

        video_final = None
        video_com_audio = None
        audio_original = None
        audio_repetido = None
        audio_final = None

        try:

            # =====================================
            # ABERTURA
            # =====================================

            if incluir_abertura:
                self._informar_progresso(
                    callback_progresso,
                    0,
                    total_perguntas,
                    "Criando a tela de abertura..."
                )

                caminho_abertura = (
                    pasta_frames
                    / "abertura.png"
                )

                self._criar_frame_abertura(
                    caminho=caminho_abertura,
                    titulo=titulo_quiz,
                    quantidade=total_perguntas
                )

                clip_abertura = ImageClip(
                    str(caminho_abertura)
                ).with_duration(3)

                clips_video.append(
                    clip_abertura
                )

            # =====================================
            # PERGUNTAS
            # =====================================

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

                clips_da_pergunta = (
                    self._criar_clips_da_pergunta(
                        pasta_frames=pasta_frames,
                        numero=numero,
                        pergunta=pergunta,
                        tempo_resposta=(
                            tempo_resposta
                        )
                    )
                )

                clips_video.extend(
                    clips_da_pergunta
                )

            # =====================================
            # ENCERRAMENTO
            # =====================================

            if incluir_encerramento:
                self._informar_progresso(
                    callback_progresso,
                    total_perguntas,
                    total_perguntas,
                    "Criando a tela de encerramento..."
                )

                caminho_encerramento = (
                    pasta_frames
                    / "encerramento.png"
                )

                self._criar_frame_encerramento(
                    caminho=caminho_encerramento,
                    texto=texto_encerramento
                )

                clip_encerramento = ImageClip(
                    str(caminho_encerramento)
                ).with_duration(4)

                clips_video.append(
                    clip_encerramento
                )

            # =====================================
            # MONTAGEM
            # =====================================

            self._informar_progresso(
                callback_progresso,
                total_perguntas,
                total_perguntas,
                "Montando o vídeo final..."
            )

            video_final = (
                concatenate_videoclips(
                    clips_video,
                    method="compose"
                )
            )

            video_para_exportar = video_final

            # =====================================
            # MÚSICA
            # =====================================

            if caminho_musica:
                self._informar_progresso(
                    callback_progresso,
                    total_perguntas,
                    total_perguntas,
                    "Adicionando música de fundo..."
                )

                caminho_musica = Path(
                    caminho_musica
                )

                if not caminho_musica.exists():
                    raise FileNotFoundError(
                        "O arquivo de música "
                        "não foi encontrado."
                    )

                audio_original = AudioFileClip(
                    str(caminho_musica)
                )

                audio_repetido = (
                    self._preparar_musica(
                        audio_original=(
                            audio_original
                        ),
                        duracao_video=(
                            video_final.duration
                        )
                    )
                )

                audio_final = (
                    audio_repetido
                    .with_volume_scaled(
                        volume_musica
                    )
                )

                video_com_audio = (
                    video_final.with_audio(
                        audio_final
                    )
                )

                video_para_exportar = (
                    video_com_audio
                )

            # =====================================
            # EXPORTAÇÃO
            # =====================================

            data_hora = (
                datetime.now().strftime(
                    "%Y%m%d_%H%M%S"
                )
            )

            caminho_saida = (
                pasta_exportado
                / (
                    f"moleza_quiz_"
                    f"{data_hora}.mp4"
                )
            )

            self._informar_progresso(
                callback_progresso,
                total_perguntas,
                total_perguntas,
                "Renderizando o arquivo MP4..."
            )

            video_para_exportar.write_videofile(
                str(caminho_saida),
                fps=self.fps,
                codec="libx264",
                audio_codec="aac",
                audio=bool(caminho_musica),
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

            if audio_final is not None:
                audio_final.close()

            if audio_repetido is not None:
                audio_repetido.close()

            if audio_original is not None:
                audio_original.close()

            if video_final is not None:
                video_final.close()

            for clip in clips_video:
                clip.close()

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

        if (
            audio_original.duration
            >= duracao_video
        ):
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

    def _criar_clips_da_pergunta(
        self,
        pasta_frames,
        numero,
        pergunta,
        tempo_resposta
    ):
        clips = []

        caminho_pergunta = (
            pasta_frames
            / f"pergunta_{numero:03d}.png"
        )

        self._criar_frame_pergunta(
            caminho=caminho_pergunta,
            numero=numero,
            pergunta=pergunta
        )

        clips.append(
            ImageClip(
                str(caminho_pergunta)
            ).with_duration(1)
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

            clips.append(
                ImageClip(
                    str(caminho_contagem)
                ).with_duration(1)
            )

        caminho_resposta = (
            pasta_frames
            / (
                f"pergunta_{numero:03d}"
                f"_resposta.png"
            )
        )

        self._criar_frame_resposta(
            caminho=caminho_resposta,
            numero=numero,
            pergunta=pergunta
        )

        clips.append(
            ImageClip(
                str(caminho_resposta)
            ).with_duration(2)
        )

        return clips

    def _criar_frame_abertura(
        self,
        caminho,
        titulo,
        quantidade
    ):
        imagem = Image.new(
            mode="RGB",
            size=(
                self.largura,
                self.altura
            ),
            color=(24, 66, 42)
        )

        desenho = ImageDraw.Draw(
            imagem
        )

        desenho.rounded_rectangle(
            (90, 70, 1190, 650),
            radius=45,
            fill=(240, 245, 236)
        )

        fonte_logo = self._carregar_fonte(
            42
        )

        fonte_titulo = self._carregar_fonte(
            60
        )

        fonte_subtitulo = (
            self._carregar_fonte(31)
        )

        desenho.text(
            (150, 120),
            "🦥 MOLEZA QUIZ",
            font=fonte_logo,
            fill=(35, 100, 60)
        )

        linhas_titulo = textwrap.wrap(
            titulo,
            width=28
        )

        y = 250

        for linha in linhas_titulo:
            caixa = desenho.textbbox(
                (0, 0),
                linha,
                font=fonte_titulo
            )

            largura = (
                caixa[2] - caixa[0]
            )

            x = (
                self.largura
                - largura
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

        caixa_quantidade = desenho.textbbox(
            (0, 0),
            texto_quantidade,
            font=fonte_subtitulo
        )

        largura_quantidade = (
            caixa_quantidade[2]
            - caixa_quantidade[0]
        )

        x_quantidade = (
            self.largura
            - largura_quantidade
        ) / 2

        desenho.text(
            (x_quantidade, 500),
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
            mode="RGB",
            size=(
                self.largura,
                self.altura
            ),
            color=(24, 66, 42)
        )

        desenho = ImageDraw.Draw(
            imagem
        )

        desenho.rounded_rectangle(
            (90, 70, 1190, 650),
            radius=45,
            fill=(240, 245, 236)
        )

        fonte_titulo = self._carregar_fonte(
            58
        )

        fonte_texto = self._carregar_fonte(
            36
        )

        fonte_botao = self._carregar_fonte(
            30
        )

        desenho.text(
            (350, 150),
            "FIM DO QUIZ!",
            font=fonte_titulo,
            fill=(35, 100, 60)
        )

        linhas = textwrap.wrap(
            texto,
            width=38
        )

        y = 290

        for linha in linhas:
            caixa = desenho.textbbox(
                (0, 0),
                linha,
                font=fonte_texto
            )

            largura = (
                caixa[2] - caixa[0]
            )

            x = (
                self.largura
                - largura
            ) / 2

            desenho.text(
                (x, y),
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

    def _criar_frame_pergunta(
        self,
        caminho,
        numero,
        pergunta
    ):
        imagem, desenho = (
            self._criar_base()
        )

        self._desenhar_cabecalho(
            desenho,
            numero
        )

        self._desenhar_pergunta_e_alternativas(
            desenho,
            pergunta
        )

        desenho.text(
            (100, 625),
            (
                "Prepare-se! "
                "A contagem vai começar."
            ),
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
        imagem, desenho = (
            self._criar_base()
        )

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

        fonte_contador = (
            self._carregar_fonte(55)
        )

        texto = str(contador)

        caixa_texto = desenho.textbbox(
            (0, 0),
            texto,
            font=fonte_contador
        )

        largura_texto = (
            caixa_texto[2]
            - caixa_texto[0]
        )

        altura_texto = (
            caixa_texto[3]
            - caixa_texto[1]
        )

        x = 1135 - (
            largura_texto / 2
        )

        y = 600 - (
            altura_texto / 2
        ) - 8

        desenho.text(
            (x, y),
            texto,
            font=fonte_contador,
            fill=(255, 255, 255)
        )

        desenho.text(
            (100, 625),
            (
                "Responda antes que "
                "o tempo acabe!"
            ),
            font=self._carregar_fonte(24),
            fill=(65, 90, 70)
        )

        imagem.save(caminho)

    def _criar_frame_resposta(
        self,
        caminho,
        numero,
        pergunta
    ):
        imagem, desenho = (
            self._criar_base()
        )

        self._desenhar_cabecalho(
            desenho,
            numero
        )

        texto_pergunta = pergunta.get(
            "pergunta",
            "Pergunta sem texto"
        )

        fonte_pergunta = (
            self._carregar_fonte(40)
        )

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
        imagem = Image.new(
            mode="RGB",
            size=(
                self.largura,
                self.altura
            ),
            color=(25, 45, 35)
        )

        desenho = ImageDraw.Draw(
            imagem
        )

        desenho.rounded_rectangle(
            (60, 45, 1220, 675),
            radius=35,
            fill=(242, 244, 238)
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
            fill=(35, 85, 55)
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

        fonte_pergunta = (
            self._carregar_fonte(38)
        )

        fonte_alternativa = (
            self._carregar_fonte(28)
        )

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

            if 1 <= indice <= len(
                alternativas
            ):
                indice -= 1

            if 0 <= indice < len(
                alternativas
            ):
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

                if indice < len(
                    alternativas
                ):
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
            Path(
                "C:/Windows/Fonts/arial.ttf"
            ),
            Path(
                "C:/Windows/Fonts/calibri.ttf"
            ),
            Path(
                "C:/Windows/Fonts/segoeui.ttf"
            )
        ]

        for caminho_fonte in fontes_possiveis:
            if caminho_fonte.exists():
                return ImageFont.truetype(
                    str(caminho_fonte),
                    tamanho
                )

        return ImageFont.load_default()
