from __future__ import annotations

import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps
from moviepy import ImageSequenceClip

from .models import LayerType


class TimelineCompositor:
    def __init__(self, fps=18):
        self.fps = max(int(fps), 10)

    def renderizar(self, cena):
        cena.validar()
        total = max(int(round(cena.duracao * self.fps)), 2)
        quadros = []

        for indice in range(total):
            t = indice / self.fps
            imagem = self._fundo(cena, t)

            for camada in sorted(cena.camadas, key=lambda c: c.z_index):
                if not (camada.inicio <= t <= camada.fim):
                    continue

                progresso = (
                    (t - camada.inicio)
                    / max(camada.duracao, 0.001)
                )

                if camada.tipo == LayerType.CARD:
                    self._cartao(imagem, camada, progresso)
                elif camada.tipo == LayerType.IMAGE:
                    self._imagem(imagem, camada, progresso, cena)
                elif camada.tipo == LayerType.TEXT:
                    self._texto(
                        imagem,
                        camada,
                        progresso
                    )
                elif camada.tipo == LayerType.BADGE:
                    self._badge(imagem, camada, progresso)
                elif camada.tipo == LayerType.TIMER:
                    self._contador(imagem, camada, progresso)

                elif camada.tipo == LayerType.EFFECT:
                    self._efeito(
                        imagem,
                        camada,
                        progresso
                    )

                elif camada.tipo == LayerType.MASCOT:
                    self._mascote(imagem, camada, progresso)

            quadros.append(np.asarray(imagem.convert("RGB")))

        return ImageSequenceClip(
            quadros,
            fps=self.fps,
        ).with_duration(cena.duracao)

    def _fundo(self, cena, t):
        fundo = next(
            (c for c in cena.camadas if c.tipo == LayerType.BACKGROUND),
            None,
        )
        props = fundo.propriedades if fundo else {}
        inicio = tuple(props.get("cor_inicio", (88, 40, 170)))
        fim = tuple(props.get("cor_fim", (25, 18, 70)))
        painel = tuple(props.get("cor_painel", (35, 28, 78)))

        imagem = Image.new(
            "RGBA",
            (cena.largura, cena.altura),
            (0, 0, 0, 255),
        )
        desenho = ImageDraw.Draw(imagem)

        for y in range(cena.altura):
            p = y / max(cena.altura - 1, 1)
            cor = tuple(
                int(inicio[i] + (fim[i] - inicio[i]) * p)
                for i in range(3)
            )
            desenho.line((0, y, cena.largura, y), fill=cor)

        deslocamento = int(20 * math.sin(t * 0.8))
        desenho.ellipse(
            (-120 + deslocamento, -80, 280 + deslocamento, 320),
            fill=(130, 90, 220, 160),
        )
        desenho.ellipse(
            (1010 - deslocamento, -100, 1390 - deslocamento, 280),
            fill=(70, 120, 230, 160),
        )
        desenho.rounded_rectangle(
            (34, 28, 1246, 692),
            radius=42,
            fill=(255, 255, 255, 255),
        )
        desenho.rounded_rectangle(
            (50, 44, 1230, 676),
            radius=34,
            fill=(*painel, 255),
        )
        desenho.rounded_rectangle(
            (80, 62, 1200, 132),
            radius=24,
            fill=(255, 255, 255, 255),
        )
        desenho.text(
            (110, 79),
            "MOLEZA QUIZ",
            font=self._fonte(34, True),
            fill=(83, 45, 165, 255),
        )
        return imagem

    def _deslocamento_entrada(
        self,
        camada,
        progresso
    ):
        direcao = str(
            camada.propriedades.get(
                "entrada",
                ""
            )
        ).strip().lower()

        if direcao not in {
            "esquerda",
            "direita"
        }:
            return 0

        duracao_entrada = max(
            float(
                camada.propriedades.get(
                    "duracao_entrada",
                    0.72
                )
            ),
            0.01
        )

        # progresso é relativo à duração inteira da camada.
        tempo_relativo = (
            progresso
            * camada.duracao
        )

        p = min(
            max(
                tempo_relativo
                / duracao_entrada,
                0.0
            ),
            1.0
        )

        suavizado = (
            1.0
            - pow(
                1.0 - p,
                3
            )
        )

        distancia = 620

        if direcao == "esquerda":
            return int(
                -distancia
                * (
                    1.0
                    - suavizado
                )
            )

        return int(
            distancia
            * (
                1.0
                - suavizado
            )
        )

    def _cartao(self, imagem, camada, progresso):
        x1, y1, x2, y2 = map(int, camada.propriedades["caixa"])
        deslocamento_entrada = self._deslocamento_entrada(
            camada,
            progresso
        )

        x1 += deslocamento_entrada
        x2 += deslocamento_entrada

        cor = tuple(camada.propriedades.get("cor", (255, 85, 115)))
        resultado = bool(
            camada.propriedades.get("resultado", False)
        )

        if resultado:
            escala = min(
                max(progresso / 0.22, 0.15),
                1.0,
            )

            centro_x = (x1 + x2) / 2
            centro_y = (y1 + y2) / 2

            largura = (x2 - x1) * escala
            altura = (y2 - y1) * escala

            x1 = int(centro_x - largura / 2)
            x2 = int(centro_x + largura / 2)
            y1 = int(centro_y - altura / 2)
            y2 = int(centro_y + altura / 2)
            dy = 0

        else:
            onda = math.sin(progresso * math.pi * 2)
            dy = int(3 * onda)

            if camada.nome.endswith("_b"):
                dy *= -1

        raio = int(
            camada.propriedades.get(
                "raio",
                34
            )
        )

        desenho = ImageDraw.Draw(imagem)
        desenho.rounded_rectangle(
            (x1 + 10, y1 + 14 + dy, x2 + 10, y2 + 14 + dy),
            radius=raio,
            fill=(0, 0, 0, 75),
        )
        desenho.rounded_rectangle(
            (x1, y1 + dy, x2, y2 + dy),
            radius=raio,
            fill=(*cor, 255),
            outline=(255, 255, 255, 255),
            width=5,
        )

    def _imagem(self, imagem, camada, progresso, cena):
        if not camada.origem:
            return
        caminho = Path(camada.origem)
        if not caminho.exists():
            return

        nome_cartao = "cartao_a" if camada.nome.endswith("_a") else "cartao_b"
        card = next((c for c in cena.camadas if c.nome == nome_cartao), None)
        if card is None:
            return

        x1, y1, x2, y2 = map(int, card.propriedades["caixa"])

        try:
            item = Image.open(caminho).convert("RGBA")
        except OSError:
            return

        fase = math.pi if camada.nome.endswith("_b") else 0
        escala = 1 + 0.018 * math.sin(progresso * math.pi * 2 + fase)

        item = ImageOps.contain(
            item,
            (
                int((x2 - x1 - 90) * escala),
                int((y2 - y1 - 115) * escala),
            ),
            method=Image.Resampling.LANCZOS,
        )

        deslocamento_entrada = self._deslocamento_entrada(
            camada,
            progresso
        )

        x = (
            (x1 + x2) // 2
            - item.width // 2
            + deslocamento_entrada
        )

        y = (
            y1
            + 58
            + int(
                4
                * math.sin(
                    progresso
                    * math.pi
                    * 2
                    + fase
                )
            )
        )
        imagem.alpha_composite(item, (x, y))

    def _texto(
        self,
        imagem,
        camada,
        progresso
    ):
        texto = str(camada.propriedades.get("texto", "")).strip()
        if not texto:
            return

        desenho = ImageDraw.Draw(imagem)

        tipo_texto = str(
            camada.propriedades.get(
                "tipo_texto",
                ""
            )
        ).strip()

        if tipo_texto:
            tamanhos = {
                "resultado_titulo": 60,
                "resultado_subtitulo": 42,
                "resultado_comentario": 28,
                "resultado_rodape": 25,
            }

            fonte = self._fonte(
                tamanhos.get(
                    tipo_texto,
                    32
                ),
                True
            )

            cor = tuple(
                camada.propriedades.get(
                    "cor",
                    (255, 255, 255)
                )
            )

            y = int(
                camada.propriedades.get(
                    "y",
                    300
                )
            )

            caixa = desenho.textbbox(
                (0, 0),
                texto,
                font=fonte
            )

            largura = caixa[2] - caixa[0]
            altura = caixa[3] - caixa[1]

            if tipo_texto == "resultado_rodape":
                desenho.rounded_rectangle(
                    (
                        imagem.width / 2
                        - largura / 2
                        - 28,
                        y - 8,
                        imagem.width / 2
                        + largura / 2
                        + 28,
                        y + altura + 12
                    ),
                    radius=18,
                    fill=(255, 255, 255, 255)
                )

            desenho.text(
                (
                    (imagem.width - largura) / 2,
                    y
                ),
                texto,
                font=fonte,
                fill=(*cor, 255)
            )

            return

        if camada.nome == "titulo":
            fonte = self._fonte(42, True)
            linhas = self._quebrar(texto, 42)[:2]
            y = 154
            for linha in linhas:
                caixa = desenho.textbbox((0, 0), linha, font=fonte)
                largura = caixa[2] - caixa[0]
                desenho.text(
                    ((imagem.width - largura) / 2, y),
                    linha,
                    font=fonte,
                    fill=(255, 255, 255, 255),
                )
                y += 50
            return

        caixa = camada.propriedades.get("caixa")
        if not caixa:
            return

        x1, y1, x2, y2 = map(int, caixa)
        fonte = self._fonte(28, True)
        linhas = self._quebrar(texto, 20)[:2]
        y = y2 - 72

        for linha in linhas:
            box = desenho.textbbox((0, 0), linha, font=fonte)
            largura = box[2] - box[0]
            deslocamento_entrada = self._deslocamento_entrada(
                camada,
                progresso
            )

            desenho.text(
                (
                    (x1 + x2) / 2
                    - largura / 2
                    + deslocamento_entrada,
                    y
                ),
                linha,
                font=fonte,
                fill=(255, 255, 255, 255),
            )
            y += 32

    def _badge(self, imagem, camada, progresso):
        if not camada.origem:
            return
        caminho = Path(camada.origem)
        if not caminho.exists():
            return
        caixa = camada.propriedades.get("caixa")
        if not caixa:
            return

        try:
            badge = Image.open(caminho).convert("RGBA")
        except OSError:
            return

        x1, y1, x2, y2 = map(int, caixa)
        escala = min(max(progresso / 0.35, 0.15), 1.0)
        badge.thumbnail(
            (
                max(int((x2 - x1) * escala), 1),
                max(int((y2 - y1) * escala), 1),
            ),
            Image.Resampling.LANCZOS,
        )
        x = (x1 + x2) // 2 - badge.width // 2
        y = (y1 + y2) // 2 - badge.height // 2
        imagem.alpha_composite(badge, (x, y))

    def _mascote(self, imagem, camada, progresso):
        pose = str(
            camada.propriedades.get("pose", "idle")
        ).strip().lower()

        candidatos = [
            Path(f"assets/mascots/{pose}.png"),
            Path("assets/mascots/idle.png"),
            Path("assets/mascots/moleza.png"),
            Path("assets/mascots/mascote.png"),
            Path("assets/moleza.png"),
        ]
        caminho = next((p for p in candidatos if p.exists()), None)
        if caminho is None:
            return

        try:
            mascote = Image.open(caminho).convert("RGBA")
        except OSError:
            return

        escala = 1 + 0.025 * math.sin(progresso * math.pi * 2)
        mascote.thumbnail(
            (int(185 * escala), int(185 * escala)),
            Image.Resampling.LANCZOS,
        )
        x = imagem.width - mascote.width - 28
        y = (
            imagem.height
            - mascote.height
            - 18
            + int(5 * math.sin(progresso * math.pi * 2))
        )
        imagem.alpha_composite(mascote, (x, y))


    def _efeito(
        self,
        imagem,
        camada,
        progresso
    ):
        efeito = str(
            camada.propriedades.get(
                "efeito",
                ""
            )
        ).strip().lower()

        if efeito != "confetti":
            return

        import random

        quantidade = int(
            camada.propriedades.get(
                "quantidade",
                70
            )
        )

        random.seed(42)

        cores = [
            (255, 214, 75),
            (255, 90, 120),
            (75, 170, 255),
            (105, 220, 170),
            (190, 105, 255),
            (255, 255, 255),
        ]

        desenho = ImageDraw.Draw(
            imagem
        )

        for indice in range(
            max(quantidade, 20)
        ):
            x_base = (
                indice * 97
                + 31
            ) % imagem.width

            y_inicio = -220 - (
                indice * 37
            ) % 180

            velocidade = (
                360
                + (
                    indice % 7
                )
                * 22
            )

            x = (
                x_base
                + 30
                * math.sin(
                    progresso
                    * math.pi
                    * 4
                    + indice
                )
            )

            y = (
                y_inicio
                + velocidade
                * progresso
            )

            tamanho = 5 + (
                indice % 8
            )

            desenho.rounded_rectangle(
                (
                    x,
                    y,
                    x + tamanho,
                    y + tamanho * 1.6,
                ),
                radius=2,
                fill=(
                    *cores[
                        indice
                        % len(cores)
                    ],
                    255
                )
            )

    def _contador(self, imagem, camada, progresso):
        valor = str(camada.propriedades.get("valor", ""))
        centro_x, centro_y = camada.propriedades.get(
            "centro",
            (640, 590),
        )
        raio_base = int(
            camada.propriedades.get("raio", 54)
        )
        cor = tuple(
            camada.propriedades.get(
                "cor_destaque",
                (255, 214, 75),
            )
        )

        pulso = 1.0 + 0.08 * math.sin(progresso * math.pi)
        raio = max(int(raio_base * pulso), 1)

        desenho = ImageDraw.Draw(imagem)
        desenho.ellipse(
            (
                centro_x - raio - 6,
                centro_y - raio - 6,
                centro_x + raio + 6,
                centro_y + raio + 6,
            ),
            fill=(*cor, 255),
        )
        desenho.ellipse(
            (
                centro_x - raio,
                centro_y - raio,
                centro_x + raio,
                centro_y + raio,
            ),
            fill=(255, 255, 255, 255),
        )

        fonte = self._fonte(46, True)
        caixa = desenho.textbbox((0, 0), valor, font=fonte)
        largura = caixa[2] - caixa[0]
        altura = caixa[3] - caixa[1]

        desenho.text(
            (
                centro_x - largura / 2,
                centro_y - altura / 2 - 5,
            ),
            valor,
            font=fonte,
            fill=(67, 43, 120, 255),
        )

    def _fonte(self, tamanho, negrito=False):
        nomes = (
            ["arialbd.ttf", "calibrib.ttf"]
            if negrito
            else ["arial.ttf", "calibri.ttf"]
        )
        for nome in nomes:
            caminho = Path("C:/Windows/Fonts") / nome
            if caminho.exists():
                return ImageFont.truetype(str(caminho), tamanho)
        return ImageFont.load_default()

    def _quebrar(self, texto, largura):
        palavras = str(texto).split()
        linhas = []
        atual = []

        for palavra in palavras:
            teste = " ".join(atual + [palavra])
            if len(teste) <= largura:
                atual.append(palavra)
            else:
                if atual:
                    linhas.append(" ".join(atual))
                atual = [palavra]

        if atual:
            linhas.append(" ".join(atual))
        return linhas
