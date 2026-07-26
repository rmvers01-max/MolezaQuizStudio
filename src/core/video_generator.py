from pathlib import Path
import textwrap

from PIL import Image, ImageDraw, ImageFont
from moviepy import ImageClip, concatenate_videoclips


class VideoGenerator:

    def __init__(self):
        self.largura = 1280
        self.altura = 720
        self.fps = 30

    def gerar_video_teste(
        self,
        pasta_projeto,
        perguntas,
        tempo_resposta=5
    ):
        pasta_projeto = Path(pasta_projeto)

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

        clips = []

        # Nesta fase, o teste usa apenas 3 perguntas.
        perguntas_teste = perguntas[:3]

        for numero, pergunta in enumerate(
            perguntas_teste,
            start=1
        ):
            # Tela inicial da pergunta.
            caminho_pergunta = (
                pasta_frames
                / f"pergunta_{numero:03d}.png"
            )

            self._criar_frame_pergunta(
                caminho=caminho_pergunta,
                numero=numero,
                pergunta=pergunta
            )

            clip_pergunta = ImageClip(
                str(caminho_pergunta)
            ).with_duration(1)

            clips.append(clip_pergunta)

            # Contagem regressiva.
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

                clip_contagem = ImageClip(
                    str(caminho_contagem)
                ).with_duration(1)

                clips.append(clip_contagem)

            # Revelação da resposta.
            caminho_resposta = (
                pasta_frames
                / f"pergunta_{numero:03d}_resposta.png"
            )

            self._criar_frame_resposta(
                caminho=caminho_resposta,
                numero=numero,
                pergunta=pergunta
            )

            clip_resposta = ImageClip(
                str(caminho_resposta)
            ).with_duration(2)

            clips.append(clip_resposta)

        video_final = concatenate_videoclips(
            clips,
            method="compose"
        )

        caminho_saida = (
            pasta_exportado
            / "video_teste.mp4"
        )

        try:
            video_final.write_videofile(
                str(caminho_saida),
                fps=self.fps,
                codec="libx264",
                audio=False,
                preset="medium",
                threads=4
            )

        finally:
            video_final.close()

            for clip in clips:
                clip.close()

        return caminho_saida

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

        desenho.text(
            (100, 625),
            "Prepare-se! A contagem vai começar.",
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

        largura_texto = caixa[2] - caixa[0]
        altura_texto = caixa[3] - caixa[1]

        x = 1135 - (largura_texto / 2)
        y = 600 - (altura_texto / 2) - 8

        desenho.text(
            (x, y),
            texto,
            font=fonte_contador,
            fill=(255, 255, 255)
        )

        desenho.text(
            (100, 625),
            "Responda antes que o tempo acabe!",
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

        linhas_resposta = textwrap.wrap(
            resposta,
            width=42
        )

        y_resposta = 455

        for linha in linhas_resposta:
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

        desenho = ImageDraw.Draw(imagem)

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
            f"MOLEZA QUIZ — PERGUNTA {numero}",
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

        fonte_pergunta = self._carregar_fonte(38)
        fonte_alternativa = self._carregar_fonte(28)

        linhas_pergunta = textwrap.wrap(
            texto_pergunta,
            width=50
        )

        y = 170

        for linha in linhas_pergunta:
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

            texto_alternativa = (
                f"{letra}) {alternativa}"
            )

            desenho.text(
                (125, y + 10),
                texto_alternativa,
                font=fonte_alternativa,
                fill=(30, 30, 30)
            )

            y += 66

    def _formatar_resposta(self, pergunta):
        resposta = pergunta.get(
            "resposta",
            "Resposta não informada"
        )

        alternativas = pergunta.get(
            "alternativas",
            []
        )

        # Caso a resposta seja um índice numérico.
        if isinstance(resposta, int):
            indice = resposta

            # Aceita tanto 0–3 quanto 1–4.
            if 1 <= indice <= len(alternativas):
                indice -= 1

            if 0 <= indice < len(alternativas):
                letra = chr(65 + indice)

                return (
                    f"{letra}) "
                    f"{alternativas[indice]}"
                )

        resposta_texto = str(resposta).strip()

        # Caso a resposta seja somente uma letra.
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

    def _carregar_fonte(self, tamanho):
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
