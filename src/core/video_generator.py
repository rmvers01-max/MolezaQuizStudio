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
        tempo_pergunta=3
    ):
        pasta_projeto = Path(pasta_projeto)

        pasta_frames = pasta_projeto / "videos" / "frames"
        pasta_exportado = pasta_projeto / "exportado"

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

        # Nesta primeira versão, limitamos o teste a 3 perguntas
        perguntas_teste = perguntas[:3]

        for numero, pergunta in enumerate(
            perguntas_teste,
            start=1
        ):
            caminho_frame = (
                pasta_frames / f"pergunta_{numero:03d}.png"
            )

            self._criar_frame(
                caminho=caminho_frame,
                numero=numero,
                pergunta=pergunta
            )

            clip = ImageClip(
                str(caminho_frame)
            ).with_duration(
                tempo_pergunta
            )

            clips.append(clip)

        video_final = concatenate_videoclips(
            clips,
            method="compose"
        )

        caminho_saida = (
            pasta_exportado / "video_teste.mp4"
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

    def _criar_frame(
        self,
        caminho,
        numero,
        pergunta
    ):
        imagem = Image.new(
            mode="RGB",
            size=(self.largura, self.altura),
            color=(25, 45, 35)
        )

        desenho = ImageDraw.Draw(imagem)

        fonte_titulo = self._carregar_fonte(48)
        fonte_pergunta = self._carregar_fonte(42)
        fonte_alternativa = self._carregar_fonte(31)
        fonte_rodape = self._carregar_fonte(24)

        texto_pergunta = pergunta.get(
            "pergunta",
            "Pergunta sem texto"
        )

        alternativas = pergunta.get(
            "alternativas",
            []
        )

        desenho.rounded_rectangle(
            (60, 45, 1220, 675),
            radius=35,
            fill=(242, 244, 238)
        )

        desenho.text(
            (100, 85),
            f"MOLEZA QUIZ — PERGUNTA {numero}",
            font=fonte_titulo,
            fill=(35, 85, 55)
        )

        linhas_pergunta = textwrap.wrap(
            texto_pergunta,
            width=46
        )

        y = 180

        for linha in linhas_pergunta:
            desenho.text(
                (100, y),
                linha,
                font=fonte_pergunta,
                fill=(25, 25, 25)
            )

            y += 54

        y += 30

        for indice, alternativa in enumerate(
            alternativas[:4]
        ):
            letra = chr(65 + indice)

            desenho.rounded_rectangle(
                (100, y, 1180, y + 58),
                radius=16,
                fill=(220, 230, 220)
            )

            desenho.text(
                (125, y + 10),
                f"{letra}) {alternativa}",
                font=fonte_alternativa,
                fill=(30, 30, 30)
            )

            y += 72

        desenho.text(
            (100, 625),
            "Responda antes que o tempo acabe!",
            font=fonte_rodape,
            fill=(65, 90, 70)
        )

        imagem.save(caminho)

    def _carregar_fonte(self, tamanho):
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
