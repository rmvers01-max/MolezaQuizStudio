from __future__ import annotations

import math
import textwrap
from pathlib import Path

import numpy as np
from PIL import (
    Image,
    ImageDraw,
    ImageFilter,
    ImageFont,
)
from moviepy import ImageSequenceClip

from ..animations import (
    CharacterAnimationEngine,
    SmartEasing,
)


class OpeningStudio:
    """
    Cria uma abertura curta, profissional e orientada à retenção.
    """

    def __init__(
        self,
        largura=1280,
        altura=720,
        fps=18,
    ):
        self.largura = int(
            largura
        )
        self.altura = int(
            altura
        )
        self.fps = max(
            int(fps),
            12
        )
        self.character_engine = (
            CharacterAnimationEngine()
        )

    def criar_clip(
        self,
        titulo: str,
        direcao: dict,
        brand_direction: dict,
        premium_theme,
    ):
        duracao = float(
            direcao.get(
                "duracao",
                4.1
            )
        )

        total_quadros = max(
            int(
                round(
                    duracao
                    * self.fps
                )
            ),
            2
        )

        quadros = []

        for indice in range(
            total_quadros
        ):
            tempo = indice / self.fps
            progresso = min(
                tempo / max(
                    duracao,
                    0.001
                ),
                1.0
            )

            quadro = self._renderizar_frame(
                titulo=titulo,
                direcao=direcao,
                brand_direction=brand_direction,
                premium_theme=premium_theme,
                tempo=tempo,
                progresso=progresso,
            )

            quadros.append(
                np.asarray(
                    quadro.convert(
                        "RGB"
                    )
                )
            )

        return ImageSequenceClip(
            quadros,
            fps=self.fps,
        ).with_duration(
            duracao
        )

    def _renderizar_frame(
        self,
        titulo,
        direcao,
        brand_direction,
        premium_theme,
        tempo,
        progresso,
    ):
        cores = self._cores(
            premium_theme,
            brand_direction
        )

        imagem = self._fundo(
            cores,
            tempo
        )

        desenho = ImageDraw.Draw(
            imagem
        )

        self._desenhar_particulas(
            imagem,
            tempo,
            direcao.get(
                "intensidade",
                0.82
            )
        )

        # Logo entra imediatamente.
        p_logo = self._intervalo(
            tempo,
            0.0,
            0.62
        )

        escala_logo = SmartEasing.ease_out_back(
            p_logo,
            overshoot=1.25
        )

        self._texto_central(
            desenho=desenho,
            texto="MOLEZA QUIZ",
            y=62,
            tamanho=max(
                int(
                    48
                    * escala_logo
                ),
                1
            ),
            cor=(255, 255, 255, 255),
            contorno=(63, 31, 130, 255),
            largura_contorno=4,
        )

        # Hook aparece antes do título.
        p_hook = self._intervalo(
            tempo,
            0.22,
            0.92
        )

        hook_y = int(
            150
            - 26
            * (
                1.0
                - SmartEasing.ease_out_cubic(
                    p_hook
                )
            )
        )

        self._texto_central(
            desenho=desenho,
            texto=str(
                direcao.get(
                    "hook_texto",
                    "VOCÊ CONSEGUE ESCOLHER?"
                )
            ),
            y=hook_y,
            tamanho=31,
            cor=(*cores["destaque"], 255),
            contorno=(50, 25, 90, 255),
            largura_contorno=3,
            opacidade=p_hook,
        )

        # Título principal com entrada curta.
        p_titulo = self._intervalo(
            tempo,
            0.55,
            1.42
        )

        escala_titulo = max(
            SmartEasing.ease_out_back(
                p_titulo,
                overshoot=1.18
            ),
            0.01
        )

        linhas = textwrap.wrap(
            str(titulo),
            width=28
        )[:2]

        y_titulo = 248

        for linha in linhas:
            tamanho = max(
                int(
                    55
                    * escala_titulo
                ),
                1
            )

            self._texto_central(
                desenho=desenho,
                texto=linha.upper(),
                y=y_titulo,
                tamanho=tamanho,
                cor=(255, 255, 255, 255),
                contorno=(45, 22, 88, 255),
                largura_contorno=5,
                opacidade=p_titulo,
            )

            y_titulo += 68

        # Quantidade funciona como promessa de conteúdo.
        p_quantidade = self._intervalo(
            tempo,
            1.20,
            1.85
        )

        if direcao.get(
            "mostrar_quantidade",
            True
        ):
            quantidade = (
                f"{int(direcao.get('total_perguntas', 1))} "
                "ESCOLHAS DIVERTIDAS"
            )

            self._badge_texto(
                imagem=imagem,
                texto=quantidade,
                centro=(
                    self.largura // 2,
                    438
                ),
                progresso=p_quantidade,
                cor=cores["secundaria"],
            )

        # CTA de início muito curto.
        p_desafio = self._intervalo(
            tempo,
            2.10,
            2.78
        )

        self._texto_central(
            desenho=desenho,
            texto=str(
                direcao.get(
                    "desafio_texto",
                    "VAMOS COMEÇAR!"
                )
            ),
            y=512,
            tamanho=38,
            cor=(*cores["destaque"], 255),
            contorno=(60, 30, 100, 255),
            largura_contorno=4,
            opacidade=p_desafio,
        )

        # Mascote aparece na frente sem cobrir título.
        if direcao.get(
            "usar_mascote",
            True
        ):
            p_mascote = self._intervalo(
                tempo,
                0.35,
                1.30
            )

            mascote, dx, dy = (
                self.character_engine
                .renderizar(
                    pose="wave",
                    progresso=max(
                        progresso,
                        p_mascote
                    ),
                    tamanho_base=(205, 205),
                    comportamento="wave",
                    intensidade=1.08,
                )
            )

            if mascote is not None:
                entrada_x = int(
                    210
                    * (
                        1.0
                        - SmartEasing.ease_out_back(
                            p_mascote,
                            overshoot=1.18
                        )
                    )
                )

                x = (
                    self.largura
                    - mascote.width
                    - 26
                    + entrada_x
                    + dx
                )

                y = (
                    self.altura
                    - mascote.height
                    - 10
                    + dy
                )

                imagem.alpha_composite(
                    mascote,
                    (x, y)
                )

        # Transição de saída rápida para a primeira pergunta.
        p_saida = self._intervalo(
            tempo,
            max(
                float(
                    direcao.get(
                        "duracao",
                        4.1
                    )
                )
                - 0.48,
                0.0
            ),
            float(
                direcao.get(
                    "duracao",
                    4.1
                )
            )
        )

        if p_saida > 0:
            camada_saida = Image.new(
                "RGBA",
                imagem.size,
                (
                    255,
                    255,
                    255,
                    int(
                        255
                        * SmartEasing.ease_out_cubic(
                            p_saida
                        )
                    )
                )
            )

            imagem.alpha_composite(
                camada_saida
            )

        return imagem

    def _fundo(
        self,
        cores,
        tempo
    ):
        imagem = Image.new(
            "RGBA",
            (
                self.largura,
                self.altura
            ),
            (0, 0, 0, 255)
        )

        desenho = ImageDraw.Draw(
            imagem
        )

        topo = cores["topo"]
        base = cores["base"]

        for y in range(
            self.altura
        ):
            p = y / max(
                self.altura - 1,
                1
            )

            cor = tuple(
                int(
                    topo[i]
                    + (
                        base[i]
                        - topo[i]
                    )
                    * p
                )
                for i in range(3)
            )

            desenho.line(
                (
                    0,
                    y,
                    self.largura,
                    y
                ),
                fill=cor
            )

        luz = Image.new(
            "RGBA",
            imagem.size,
            (0, 0, 0, 0)
        )

        desenho_luz = ImageDraw.Draw(
            luz
        )

        deslocamento = int(
            75
            * math.sin(
                tempo * 0.8
            )
        )

        desenho_luz.ellipse(
            (
                -180 + deslocamento,
                -130,
                560 + deslocamento,
                610
            ),
            fill=(
                *cores["luz_a"],
                95
            )
        )

        desenho_luz.ellipse(
            (
                720 - deslocamento,
                -150,
                1460 - deslocamento,
                590
            ),
            fill=(
                *cores["luz_b"],
                85
            )
        )

        luz = luz.filter(
            ImageFilter.GaussianBlur(
                radius=95
            )
        )

        imagem.alpha_composite(
            luz
        )

        return imagem

    def _desenhar_particulas(
        self,
        imagem,
        tempo,
        intensidade
    ):
        desenho = ImageDraw.Draw(
            imagem
        )

        quantidade = max(
            int(
                26
                * float(
                    intensidade
                )
            ),
            12
        )

        for indice in range(
            quantidade
        ):
            x = (
                indice * 97
                + 31
                + int(
                    18
                    * math.sin(
                        tempo * 1.6
                        + indice
                    )
                )
            ) % self.largura

            y = (
                indice * 59
                + 23
                + int(
                    12
                    * math.cos(
                        tempo * 1.2
                        + indice
                    )
                )
            ) % self.altura

            raio = 2 + (
                indice % 4
            )

            desenho.ellipse(
                (
                    x - raio,
                    y - raio,
                    x + raio,
                    y + raio
                ),
                fill=(
                    255,
                    255,
                    255,
                    70
                    + (
                        indice % 3
                    )
                    * 25
                )
            )

    def _badge_texto(
        self,
        imagem,
        texto,
        centro,
        progresso,
        cor
    ):
        if progresso <= 0:
            return

        escala = max(
            SmartEasing.ease_out_back(
                progresso,
                overshoot=1.18
            ),
            0.01
        )

        fonte = self._fonte(
            max(
                int(
                    25 * escala
                ),
                1
            ),
            True
        )

        desenho = ImageDraw.Draw(
            imagem
        )

        caixa = desenho.textbbox(
            (0, 0),
            texto,
            font=fonte
        )

        largura = (
            caixa[2]
            - caixa[0]
        )

        altura = (
            caixa[3]
            - caixa[1]
        )

        x1 = int(
            centro[0]
            - largura / 2
            - 28
        )

        y1 = int(
            centro[1]
            - altura / 2
            - 13
        )

        x2 = int(
            centro[0]
            + largura / 2
            + 28
        )

        y2 = int(
            centro[1]
            + altura / 2
            + 15
        )

        desenho.rounded_rectangle(
            (
                x1,
                y1,
                x2,
                y2
            ),
            radius=22,
            fill=(
                *cor,
                int(
                    235
                    * progresso
                )
            ),
            outline=(
                255,
                255,
                255,
                int(
                    230
                    * progresso
                )
            ),
            width=3
        )

        desenho.text(
            (
                centro[0]
                - largura / 2,
                centro[1]
                - altura / 2
                - 2
            ),
            texto,
            font=fonte,
            fill=(
                255,
                255,
                255,
                int(
                    255
                    * progresso
                )
            ),
            stroke_width=2,
            stroke_fill=(
                50,
                25,
                95,
                int(
                    220
                    * progresso
                )
            )
        )

    def _texto_central(
        self,
        desenho,
        texto,
        y,
        tamanho,
        cor,
        contorno,
        largura_contorno,
        opacidade=1.0,
    ):
        if (
            opacidade <= 0
            or tamanho <= 0
        ):
            return

        fonte = self._fonte(
            tamanho,
            True
        )

        caixa = desenho.textbbox(
            (0, 0),
            texto,
            font=fonte,
            stroke_width=largura_contorno
        )

        largura = (
            caixa[2]
            - caixa[0]
        )

        desenho.text(
            (
                (
                    self.largura
                    - largura
                ) / 2,
                y
            ),
            texto,
            font=fonte,
            fill=(
                cor[0],
                cor[1],
                cor[2],
                int(
                    cor[3]
                    * opacidade
                )
            ),
            stroke_width=largura_contorno,
            stroke_fill=(
                contorno[0],
                contorno[1],
                contorno[2],
                int(
                    contorno[3]
                    * opacidade
                )
            )
        )

    def _intervalo(
        self,
        tempo,
        inicio,
        fim
    ):
        if fim <= inicio:
            return 1.0

        return min(
            max(
                (
                    tempo - inicio
                )
                / (
                    fim - inicio
                ),
                0.0
            ),
            1.0
        )

    def _fonte(
        self,
        tamanho,
        negrito=False
    ):
        nomes = (
            [
                "arialbd.ttf",
                "calibrib.ttf"
            ]
            if negrito
            else [
                "arial.ttf",
                "calibri.ttf"
            ]
        )

        for nome in nomes:
            caminho = (
                Path(
                    "C:/Windows/Fonts"
                )
                / nome
            )

            if caminho.exists():
                return ImageFont.truetype(
                    str(caminho),
                    tamanho
                )

        return ImageFont.load_default()

    def _cores(
        self,
        premium_theme,
        brand_direction
    ):
        codigo = str(
            getattr(
                premium_theme,
                "codigo",
                "moleza_vibrante"
            )
        )

        temas = {
            "candy_party": {
                "topo": (205, 70, 184),
                "base": (75, 40, 145),
                "destaque": (255, 225, 80),
                "secundaria": (255, 100, 155),
                "luz_a": (255, 110, 190),
                "luz_b": (95, 170, 255),
            },
            "neon_future": {
                "topo": (25, 35, 105),
                "base": (12, 12, 45),
                "destaque": (80, 255, 225),
                "secundaria": (170, 80, 255),
                "luz_a": (40, 245, 225),
                "luz_b": (185, 75, 255),
            },
            "jungle_adventure": {
                "topo": (38, 120, 82),
                "base": (18, 52, 50),
                "destaque": (255, 220, 75),
                "secundaria": (85, 170, 95),
                "luz_a": (100, 225, 130),
                "luz_b": (255, 205, 65),
            },
            "game_arena": {
                "topo": (40, 72, 175),
                "base": (25, 24, 75),
                "destaque": (255, 215, 55),
                "secundaria": (255, 80, 110),
                "luz_a": (70, 170, 255),
                "luz_b": (255, 70, 150),
            },
            "princess_dream": {
                "topo": (180, 82, 176),
                "base": (72, 42, 122),
                "destaque": (255, 225, 105),
                "secundaria": (235, 110, 205),
                "luz_a": (255, 125, 210),
                "luz_b": (150, 115, 255),
            },
        }

        return temas.get(
            codigo,
            {
                "topo": (90, 55, 180),
                "base": (35, 28, 92),
                "destaque": (255, 215, 65),
                "secundaria": (255, 95, 135),
                "luz_a": (255, 100, 170),
                "luz_b": (80, 155, 255),
            }
        )
