from __future__ import annotations

import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageEnhance
from moviepy import ImageSequenceClip

from .models import LayerType
from ..animations import (
    CharacterAnimationEngine,
    SmartEasing,
)
from ..effects import (
    CardMaterialEngine,
    CinematicFXEngine,
    ImageDepthFactory,
    MotionBlurEngine,
    VisualFXEngine,
)


class TimelineCompositor:
    def __init__(self, fps=18):
        self.fps = max(int(fps), 10)
        self.visual_fx = VisualFXEngine()
        self.motion_blur = MotionBlurEngine()
        self.image_depth = ImageDepthFactory()
        self.character_engine = CharacterAnimationEngine()
        self.cinematic_fx = CinematicFXEngine()
        self.card_material = CardMaterialEngine()

    def renderizar(self, cena):
        cena.validar()

        self.visual_fx.largura = cena.largura
        self.visual_fx.altura = cena.altura

        self.cinematic_fx.largura = cena.largura
        self.cinematic_fx.altura = cena.altura

        self.card_material.largura = cena.largura
        self.card_material.altura = cena.altura

        total = max(int(round(cena.duracao * self.fps)), 2)
        quadros = []

        for indice in range(total):
            t = indice / self.fps
            self._tema_atual = dict(
                cena.metadados.get(
                    "premium_theme",
                    {}
                )
            )
            imagem = self._fundo(cena, t)

            intensidade_fx = float(
                self._tema_atual.get(
                    "intensidade_fx",
                    cena.metadados.get(
                        "intensidade_fx",
                        0.55
                    )
                )
            )

            self.visual_fx.aplicar_ambiente(
                imagem,
                tempo=t,
                intensidade=intensidade_fx
            )

            self.visual_fx.aplicar_particulas(
                imagem,
                tempo=t,
                quantidade=30,
                intensidade=intensidade_fx
            )

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

            self.visual_fx.aplicar_vinheta(
                imagem,
                intensidade=0.12
            )

            imagem = self._aplicar_camera(
                imagem,
                cena,
                t
            )

            intensidade_cinematica = float(
                self._tema_atual.get(
                    "intensidade_glow",
                    0.36
                )
            )

            imagem = self.cinematic_fx.aplicar(
                imagem,
                tempo=t,
                intensidade=intensidade_cinematica,
                estilo=self._tema_atual.get(
                    "efeito_ambiente",
                    "mixed_glow"
                )
            )

            quadros.append(
                np.asarray(
                    imagem.convert("RGB")
                )
            )

        return ImageSequenceClip(
            quadros,
            fps=self.fps,
        ).with_duration(cena.duracao)

    def _aplicar_camera(
        self,
        imagem,
        cena,
        tempo
    ):
        perfil = dict(
            cena.metadados.get(
                "camera",
                {}
            )
        )

        if not perfil:
            return imagem

        duracao = max(
            float(cena.duracao),
            0.001
        )

        progresso = min(
            max(
                tempo / duracao,
                0.0
            ),
            1.0
        )

        zoom_inicial = float(
            perfil.get(
                "zoom_inicial",
                1.0
            )
        )

        zoom_final = float(
            perfil.get(
                "zoom_final",
                1.02
            )
        )

        zoom = (
            zoom_inicial
            + (
                zoom_final
                - zoom_inicial
            )
            * progresso
        )

        pan_x_total = int(
            perfil.get(
                "pan_x",
                0
            )
        )

        pan_y_total = int(
            perfil.get(
                "pan_y",
                0
            )
        )

        pan_x = int(
            pan_x_total
            * progresso
        )

        pan_y = int(
            pan_y_total
            * progresso
        )

        rotacao_total = float(
            perfil.get(
                "rotacao",
                0.0
            )
        )

        rotacao = (
            rotacao_total
            * math.sin(
                progresso
                * math.pi
            )
        )

        pulso_brilho = float(
            perfil.get(
                "pulso_brilho",
                0.0
            )
        )

        largura = max(
            int(
                round(
                    cena.largura
                    * zoom
                )
            ),
            cena.largura
        )

        altura = max(
            int(
                round(
                    cena.altura
                    * zoom
                )
            ),
            cena.altura
        )

        camera = imagem.resize(
            (largura, altura),
            Image.Resampling.LANCZOS
        )

        x = (
            largura
            - cena.largura
        ) // 2 + pan_x

        y = (
            altura
            - cena.altura
        ) // 2 + pan_y

        x = max(
            0,
            min(
                largura - cena.largura,
                x
            )
        )

        y = max(
            0,
            min(
                altura - cena.altura,
                y
            )
        )

        camera = camera.crop(
            (
                x,
                y,
                x + cena.largura,
                y + cena.altura
            )
        )

        if abs(rotacao) > 0.001:
            camera = camera.rotate(
                rotacao,
                resample=Image.Resampling.BICUBIC,
                expand=False
            )

        if pulso_brilho > 0:
            brilho = (
                1.0
                + pulso_brilho
                * math.sin(
                    progresso
                    * math.pi
                    * 2
                )
            )

            camera = ImageEnhance.Brightness(
                camera
            ).enhance(
                brilho
            )

        return camera

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

        easing_nome = str(
            camada.propriedades.get(
                "easing_entrada",
                "ease_out_cubic"
            )
        )

        suavizado = SmartEasing.aplicar(
            easing_nome,
            p,
            overshoot=camada.propriedades.get(
                "overshoot",
                1.70158
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

    def _cartao(
        self,
        imagem,
        camada,
        progresso
    ):
        x1, y1, x2, y2 = map(
            int,
            camada.propriedades[
                "caixa"
            ]
        )

        deslocamento_entrada = (
            self._deslocamento_entrada(
                camada,
                progresso
            )
        )

        x1 += deslocamento_entrada
        x2 += deslocamento_entrada

        cor = tuple(
            camada.propriedades.get(
                "cor",
                (255, 85, 115)
            )
        )

        resultado = bool(
            camada.propriedades.get(
                "resultado",
                False
            )
        )

        if resultado:
            escala = min(
                max(
                    progresso / 0.22,
                    0.15
                ),
                1.0
            )

            centro_x = (
                x1 + x2
            ) / 2

            centro_y = (
                y1 + y2
            ) / 2

            largura = (
                x2 - x1
            ) * escala

            altura = (
                y2 - y1
            ) * escala

            x1 = int(
                centro_x
                - largura / 2
            )

            x2 = int(
                centro_x
                + largura / 2
            )

            y1 = int(
                centro_y
                - altura / 2
            )

            y2 = int(
                centro_y
                + altura / 2
            )

            dy = 0

        else:
            amplitude_idle = float(
                camada.propriedades.get(
                    "idle_amplitude",
                    3.0
                )
            )

            fase_idle = float(
                camada.propriedades.get(
                    "idle_fase",
                    (
                        math.pi
                        if camada.nome.endswith(
                            "_b"
                        )
                        else 0.0
                    )
                )
            )

            onda = math.sin(
                progresso
                * math.pi
                * 2
                + fase_idle
            )

            dy = int(
                amplitude_idle
                * onda
            )

        tema = dict(
            getattr(
                self,
                "_tema_atual",
                {}
            )
        )

        raio = int(
            camada.propriedades.get(
                "raio",
                tema.get(
                    "arredondamento_cartao",
                    34
                )
            )
        )

        intensidade_glow = float(
            tema.get(
                "intensidade_glow",
                0.36
            )
        )

        camada_cartao = Image.new(
            "RGBA",
            imagem.size,
            (0, 0, 0, 0)
        )

        self.card_material.renderizar(
            imagem_base=camada_cartao,
            caixa=(
                x1,
                y1 + dy,
                x2,
                y2 + dy
            ),
            cor=cor,
            progresso=progresso,
            raio=raio,
            glow=min(
                intensidade_glow,
                0.65
            ),
            intensidade_reflexo=(
                0.0
                if resultado
                else 0.22
            ),
            resultado=resultado
        )

        intensidade = (
            self.motion_blur
            .intensidade_entrada(
                progresso,
                limite=0.72
            )
            if deslocamento_entrada
            else 0.0
        )

        if intensidade > 0.01:
            camada_cartao = (
                self.motion_blur
                .aplicar_horizontal(
                    camada_cartao,
                    intensidade=intensidade,
                    direcao=(
                        -1
                        if camada.nome.endswith(
                            "_a"
                        )
                        else 1
                    )
                )
            )

        imagem.alpha_composite(
            camada_cartao
        )


    def _imagem(
        self,
        imagem,
        camada,
        progresso,
        cena
    ):
        if not camada.origem:
            return

        caminho = Path(
            camada.origem
        )

        if not caminho.exists():
            return

        nome_cartao = (
            "cartao_a"
            if camada.nome.endswith(
                "_a"
            )
            else "cartao_b"
        )

        card = next(
            (
                item
                for item in cena.camadas
                if item.nome
                == nome_cartao
            ),
            None
        )

        if card is None:
            return

        x1, y1, x2, y2 = map(
            int,
            card.propriedades[
                "caixa"
            ]
        )

        try:
            item = Image.open(
                caminho
            ).convert(
                "RGBA"
            )

        except OSError:
            return

        fase = float(
            camada.propriedades.get(
                "idle_fase",
                (
                    math.pi
                    if camada.nome.endswith(
                        "_b"
                    )
                    else 0.0
                )
            )
        )

        intensidade_respiracao = float(
            camada.propriedades.get(
                "breath_intensidade",
                0.018
            )
        )

        escala = (
            1.0
            + intensidade_respiracao
            * math.sin(
                progresso
                * math.pi
                * 2
                + fase
            )
        )

        item = ImageOps.contain(
            item,
            (
                max(
                    int(
                        (
                            x2 - x1 - 110
                        )
                        * escala
                    ),
                    20
                ),
                max(
                    int(
                        (
                            y2 - y1 - 135
                        )
                        * escala
                    ),
                    20
                )
            ),
            method=Image.Resampling.LANCZOS
        )

        item = (
            self.image_depth
            .preparar(
                item,
                padding=10,
                raio=18
            )
        )

        deslocamento_entrada = (
            self._deslocamento_entrada(
                camada,
                progresso
            )
        )

        intensidade = (
            self.motion_blur
            .intensidade_entrada(
                progresso,
                limite=0.72
            )
            if deslocamento_entrada
            else 0.0
        )

        if intensidade > 0.01:
            item = (
                self.motion_blur
                .aplicar_horizontal(
                    item,
                    intensidade=intensidade,
                    direcao=(
                        -1
                        if camada.nome.endswith(
                            "_a"
                        )
                        else 1
                    )
                )
            )

        x = (
            (
                x1 + x2
            ) // 2
            - item.width // 2
            + deslocamento_entrada
        )

        amplitude_idle = float(
            camada.propriedades.get(
                "idle_amplitude",
                4.0
            )
        )

        y = (
            y1
            + 46
            + int(
                amplitude_idle
                * math.sin(
                    progresso
                    * math.pi
                    * 2
                    + fase
                )
            )
        )

        imagem.alpha_composite(
            item,
            (x, y)
        )

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
            fonte = self._fonte(
                int(
                    self._tema_atual.get(
                        "titulo_tamanho",
                        42
                    )
                ),
                True,
                familia=self._tema_atual.get(
                    "familia_fonte",
                    "rounded"
                )
            )
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
        fonte = self._fonte(
            int(
                self._tema_atual.get(
                    "alternativa_tamanho",
                    28
                )
            ),
            True,
            familia=self._tema_atual.get(
                "familia_fonte",
                "rounded"
            )
        )
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
        easing_nome = str(
            camada.propriedades.get(
                "easing_entrada",
                "ease_out_bounce"
            )
        )

        escala = max(
            SmartEasing.aplicar(
                easing_nome,
                min(
                    max(
                        progresso / 0.35,
                        0.0
                    ),
                    1.0
                )
            ),
            0.15
        )
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

    def _mascote(
        self,
        imagem,
        camada,
        progresso
    ):
        pose = str(
            camada.propriedades.get(
                "pose",
                "idle"
            )
        ).strip().lower()

        comportamento = str(
            camada.propriedades.get(
                "comportamento",
                "auto"
            )
        ).strip().lower()

        intensidade = float(
            camada.propriedades.get(
                "intensidade",
                1.0
            )
        )

        (
            mascote,
            deslocamento_x,
            deslocamento_y
        ) = self.character_engine.renderizar(
            pose=pose,
            progresso=progresso,
            tamanho_base=(185, 185),
            comportamento=comportamento,
            intensidade=intensidade
        )

        if mascote is None:
            return

        x = (
            imagem.width
            - mascote.width
            - 28
            + deslocamento_x
        )

        y = (
            imagem.height
            - mascote.height
            - 18
            + deslocamento_y
        )

        imagem.alpha_composite(
            mascote,
            (x, y)
        )


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

    def _fonte(
        self,
        tamanho,
        negrito=False,
        familia="rounded"
    ):
        familias = {
            "rounded": (
                ["arialbd.ttf", "calibrib.ttf"]
                if negrito
                else ["arial.ttf", "calibri.ttf"]
            ),
            "tech": (
                ["segoeuib.ttf", "arialbd.ttf"]
                if negrito
                else ["segoeui.ttf", "arial.ttf"]
            ),
            "display": (
                ["impact.ttf", "arialbd.ttf"]
                if negrito
                else ["arial.ttf", "calibri.ttf"]
            ),
            "elegant": (
                ["georgiab.ttf", "timesbd.ttf"]
                if negrito
                else ["georgia.ttf", "times.ttf"]
            ),
        }

        nomes = familias.get(
            str(familia).lower(),
            familias["rounded"]
        )

        for nome in nomes:
            caminho = (
                Path("C:/Windows/Fonts")
                / nome
            )

            if caminho.exists():
                return ImageFont.truetype(
                    str(caminho),
                    tamanho
                )

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
