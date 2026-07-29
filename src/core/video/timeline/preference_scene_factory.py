from __future__ import annotations

from .builder import (
    TimelineSceneBuilder,
    animacao,
)
from .models import LayerType
from ..animations import CameraProfileRegistry


class PreferenceTimelineFactory:
    """
    Monta a descrição em camadas de uma cena
    "O que você prefere?".

    Esta representação será usada nas próximas etapas
    pelo novo compositor de timeline.
    """

    def __init__(self):
        self.camera_profiles = CameraProfileRegistry()


    def criar_pergunta(
        self,
        pergunta,
        numero,
        duracao,
        layout,
        preset,
        caminho_frame=None,
        premium_theme=None,
    ):
        builder = TimelineSceneBuilder(
            nome=f"pergunta_{numero:03d}",
            duracao=duracao,
        )

        builder.adicionar(
            nome="fundo",
            tipo=LayerType.BACKGROUND,
            z_index=0,
            inicio=0,
            duracao=duracao,
            origem=caminho_frame,
            propriedades={
                "preset": preset.nome,
                "cor_inicio": preset.cor_fundo_inicio,
                "cor_fim": preset.cor_fundo_fim,
                "cor_painel": preset.cor_painel,
            },
            animacoes=[
                animacao(
                    "camera_zoom",
                    duracao=duracao,
                    zoom_final=preset.zoom_cena,
                )
            ],
        )

        builder.adicionar(
            nome="particulas",
            tipo=LayerType.PARTICLES,
            z_index=10,
            inicio=0,
            duracao=duracao,
            propriedades={
                "intensidade": (
                    preset
                    .intensidade_particulas
                )
            },
        )

        builder.adicionar(
            nome="cartao_a",
            tipo=LayerType.CARD,
            z_index=20,
            inicio=0,
            duracao=duracao,
            propriedades={
                "caixa": layout.caixa_a,
                "cor": preset.paletas_perguntas[0]["a"],
            },
            animacoes=[
                animacao(
                    "slide_left",
                    duracao=0.7,
                ),
                animacao(
                    "float",
                    inicio=0.7,
                    duracao=max(
                        duracao - 0.7,
                        0.1
                    ),
                    amplitude=3,
                ),
            ],
        )

        builder.adicionar(
            nome="imagem_a",
            tipo=LayerType.IMAGE,
            z_index=30,
            inicio=0.1,
            duracao=max(
                duracao - 0.1,
                0.1
            ),
            origem=pergunta.get(
                "imagem_a"
            ),
            animacoes=[
                animacao(
                    "breath",
                    duracao=duracao,
                    intensidade=0.018,
                )
            ],
        )

        builder.adicionar(
            nome="texto_a",
            tipo=LayerType.TEXT,
            z_index=35,
            inicio=0,
            duracao=duracao,
            propriedades={
                "texto": (
                    pergunta.get("alternativas", ["A"])[0]
                    if pergunta.get("alternativas")
                    else "A"
                ),
                "caixa": layout.caixa_a,
            },
        )

        builder.adicionar(
            nome="cartao_b",
            tipo=LayerType.CARD,
            z_index=20,
            inicio=0.12,
            duracao=max(
                duracao - 0.12,
                0.1
            ),
            propriedades={
                "caixa": layout.caixa_b,
                "cor": preset.paletas_perguntas[0]["b"],
            },
            animacoes=[
                animacao(
                    "slide_right",
                    duracao=0.7,
                ),
                animacao(
                    "float",
                    inicio=0.7,
                    duracao=max(
                        duracao - 0.7,
                        0.1
                    ),
                    amplitude=-3,
                ),
            ],
        )

        builder.adicionar(
            nome="imagem_b",
            tipo=LayerType.IMAGE,
            z_index=30,
            inicio=0.2,
            duracao=max(
                duracao - 0.2,
                0.1
            ),
            origem=pergunta.get(
                "imagem_b"
            ),
            animacoes=[
                animacao(
                    "breath",
                    duracao=duracao,
                    intensidade=0.018,
                    fase=3.14159,
                )
            ],
        )

        builder.adicionar(
            nome="texto_b",
            tipo=LayerType.TEXT,
            z_index=35,
            inicio=0,
            duracao=duracao,
            propriedades={
                "texto": (
                    pergunta.get("alternativas", ["A", "B"])[1]
                    if len(pergunta.get("alternativas", [])) > 1
                    else "B"
                ),
                "caixa": layout.caixa_b,
            },
        )

        builder.adicionar(
            nome="ou",
            tipo=LayerType.BADGE,
            z_index=40,
            inicio=0.42,
            duracao=max(
                duracao - 0.42,
                0.1
            ),
            origem="assets/ui/ou.png",
            propriedades={
                "caixa": layout.caixa_ou,
            },
            animacoes=[
                animacao(
                    "pop",
                    duracao=0.5,
                )
            ],
        )

        builder.adicionar(
            nome="titulo",
            tipo=LayerType.TEXT,
            z_index=50,
            inicio=0,
            duracao=duracao,
            propriedades={
                "texto": pergunta.get(
                    "pergunta",
                    ""
                )
            },
        )

        builder.adicionar(
            nome="mascote",
            tipo=LayerType.MASCOT,
            z_index=100,
            inicio=0,
            duracao=duracao,
            propriedades={
                "pose": "idle",
                "comportamento": "idle",
                "intensidade": 1.0,
                "posicao": "inferior_direita",
            },
            animacoes=[
                animacao(
                    "breath",
                    duracao=duracao,
                    intensidade=0.025,
                )
            ],
        )

        builder.scene.metadados.update({
            "numero": numero,
            "tipo_quiz": "preferencia",
            "layout": layout.nome,
            "preset": preset.nome,
            "intensidade_fx": (
                preset.intensidade_particulas
            ),
            "premium_theme": {
                "nome": (
                    premium_theme.nome
                    if premium_theme
                    else "Moleza Vibrante"
                ),
                "codigo": (
                    premium_theme.codigo
                    if premium_theme
                    else "moleza_vibrante"
                ),
                "familia_fonte": (
                    premium_theme.familia_fonte
                    if premium_theme
                    else "rounded"
                ),
                "titulo_tamanho": (
                    premium_theme.titulo_tamanho
                    if premium_theme
                    else 43
                ),
                "alternativa_tamanho": (
                    premium_theme.alternativa_tamanho
                    if premium_theme
                    else 28
                ),
                "arredondamento_cartao": (
                    premium_theme.arredondamento_cartao
                    if premium_theme
                    else 34
                ),
                "particulas": (
                    premium_theme.particulas
                    if premium_theme
                    else "sparkles"
                ),
                "efeito_ambiente": (
                    premium_theme.efeito_ambiente
                    if premium_theme
                    else "mixed_glow"
                ),
                "estilo_camera": (
                    premium_theme.estilo_camera
                    if premium_theme
                    else "equilibrada"
                ),
                "intensidade_fx": (
                    premium_theme.intensidade_fx
                    if premium_theme
                    else 0.55
                ),
                "intensidade_glow": (
                    premium_theme.intensidade_glow
                    if premium_theme
                    else 0.36
                ),
                "cor_texto": (
                    premium_theme.cor_texto
                    if premium_theme
                    else (255, 255, 255)
                ),
                "cor_secundaria": (
                    premium_theme.cor_secundaria
                    if premium_theme
                    else (240, 235, 255)
                ),
            },
            "camera": {
                "nome": self.camera_profiles.obter(numero).nome,
                "zoom_inicial": self.camera_profiles.obter(numero).zoom_inicial,
                "zoom_final": self.camera_profiles.obter(numero).zoom_final,
                "pan_x": self.camera_profiles.obter(numero).pan_x,
                "pan_y": self.camera_profiles.obter(numero).pan_y,
                "rotacao": self.camera_profiles.obter(numero).rotacao,
                "pulso_brilho": self.camera_profiles.obter(numero).pulso_brilho,
            },
        })

        return builder.construir()


    def criar_contagem(
        self,
        pergunta,
        numero,
        contador,
        layout,
        preset,
        duracao=1.0,
        premium_theme=None,
    ):
        builder = TimelineSceneBuilder(
            nome=f"pergunta_{numero:03d}_contador_{contador}",
            duracao=duracao,
        )

        builder.adicionar(
            "fundo",
            LayerType.BACKGROUND,
            0,
            0,
            duracao,
            propriedades={
                "preset": preset.nome,
                "cor_inicio": preset.cor_fundo_inicio,
                "cor_fim": preset.cor_fundo_fim,
                "cor_painel": preset.cor_painel,
            },
        )

        alternativas = pergunta.get("alternativas", [])

        for lado, indice, caixa, cor in (
            ("a", 0, layout.caixa_a, preset.paletas_perguntas[0]["a"]),
            ("b", 1, layout.caixa_b, preset.paletas_perguntas[0]["b"]),
        ):
            builder.adicionar(
                f"cartao_{lado}",
                LayerType.CARD,
                20,
                0,
                duracao,
                propriedades={
                    "caixa": caixa,
                    "cor": cor,
                },
            )

            builder.adicionar(
                f"imagem_{lado}",
                LayerType.IMAGE,
                30,
                0,
                duracao,
                origem=pergunta.get(f"imagem_{lado}"),
            )

            builder.adicionar(
                f"texto_{lado}",
                LayerType.TEXT,
                35,
                0,
                duracao,
                propriedades={
                    "texto": (
                        alternativas[indice]
                        if indice < len(alternativas)
                        else lado.upper()
                    ),
                    "caixa": caixa,
                },
            )

        builder.adicionar(
            "ou",
            LayerType.BADGE,
            40,
            0,
            duracao,
            origem="assets/ui/ou.png",
            propriedades={"caixa": layout.caixa_ou},
        )

        builder.adicionar(
            "titulo",
            LayerType.TEXT,
            50,
            0,
            duracao,
            propriedades={
                "texto": pergunta.get("pergunta", "")
            },
        )

        builder.adicionar(
            "contador",
            LayerType.TIMER,
            80,
            0,
            duracao,
            propriedades={
                "valor": int(contador),
                "centro": (640, 590),
                "raio": 54,
                "cor_destaque": (
                    preset.paletas_perguntas[0]["destaque"]
                ),
            },
        )

        builder.adicionar(
            "mascote",
            LayerType.MASCOT,
            100,
            0,
            duracao,
            propriedades={
                "pose": "thinking",
                "comportamento": "thinking",
                "intensidade": 1.1,
                "posicao": "inferior_direita",
            },
        )

        builder.scene.metadados.update({
            "numero": numero,
            "contador": contador,
            "etapa": "contagem",
            "tipo_quiz": "preferencia",
            "layout": layout.nome,
            "preset": preset.nome,
            "intensidade_fx": (
                preset.intensidade_particulas
            ),
            "premium_theme": {
                "nome": (
                    premium_theme.nome
                    if premium_theme
                    else "Moleza Vibrante"
                ),
                "codigo": (
                    premium_theme.codigo
                    if premium_theme
                    else "moleza_vibrante"
                ),
                "familia_fonte": (
                    premium_theme.familia_fonte
                    if premium_theme
                    else "rounded"
                ),
                "titulo_tamanho": (
                    premium_theme.titulo_tamanho
                    if premium_theme
                    else 43
                ),
                "alternativa_tamanho": (
                    premium_theme.alternativa_tamanho
                    if premium_theme
                    else 28
                ),
                "arredondamento_cartao": (
                    premium_theme.arredondamento_cartao
                    if premium_theme
                    else 34
                ),
                "particulas": (
                    premium_theme.particulas
                    if premium_theme
                    else "sparkles"
                ),
                "efeito_ambiente": (
                    premium_theme.efeito_ambiente
                    if premium_theme
                    else "mixed_glow"
                ),
                "estilo_camera": (
                    premium_theme.estilo_camera
                    if premium_theme
                    else "equilibrada"
                ),
                "intensidade_fx": (
                    premium_theme.intensidade_fx
                    if premium_theme
                    else 0.55
                ),
                "intensidade_glow": (
                    premium_theme.intensidade_glow
                    if premium_theme
                    else 0.36
                ),
                "cor_texto": (
                    premium_theme.cor_texto
                    if premium_theme
                    else (255, 255, 255)
                ),
                "cor_secundaria": (
                    premium_theme.cor_secundaria
                    if premium_theme
                    else (240, 235, 255)
                ),
            },
            "camera": {
                "nome": self.camera_profiles.obter(numero).nome,
                "zoom_inicial": self.camera_profiles.obter(numero).zoom_inicial,
                "zoom_final": self.camera_profiles.obter(numero).zoom_final,
                "pan_x": self.camera_profiles.obter(numero).pan_x,
                "pan_y": self.camera_profiles.obter(numero).pan_y,
                "rotacao": self.camera_profiles.obter(numero).rotacao,
                "pulso_brilho": self.camera_profiles.obter(numero).pulso_brilho,
            },
        })

        return builder.construir()


    def criar_resultado(
        self,
        pergunta,
        numero,
        layout,
        preset,
        duracao=2.2,
        premium_theme=None,
    ):
        builder = TimelineSceneBuilder(
            nome=f"pergunta_{numero:03d}_resultado",
            duracao=duracao,
        )

        builder.adicionar(
            "fundo",
            LayerType.BACKGROUND,
            0,
            0,
            duracao,
            propriedades={
                "preset": preset.nome,
                "cor_inicio": preset.cor_fundo_inicio,
                "cor_fim": preset.cor_fundo_fim,
                "cor_painel": preset.cor_painel,
            },
        )

        builder.adicionar(
            "painel_resultado",
            LayerType.CARD,
            20,
            0,
            duracao,
            propriedades={
                "caixa": (120, 195, 1160, 545),
                "cor": (113, 68, 200),
                "raio": 45,
                "resultado": True,
            },
            animacoes=[
                animacao(
                    "pop",
                    duracao=0.55,
                )
            ],
        )

        builder.adicionar(
            "titulo_resultado",
            LayerType.TEXT,
            40,
            0,
            duracao,
            propriedades={
                "texto": "TEMPO ESGOTADO!",
                "tipo_texto": "resultado_titulo",
                "y": 270,
                "cor": preset.paletas_perguntas[0]["destaque"],
            },
        )

        builder.adicionar(
            "subtitulo_resultado",
            LayerType.TEXT,
            40,
            0,
            duracao,
            propriedades={
                "texto": "QUAL VOCÊ ESCOLHEU?",
                "tipo_texto": "resultado_subtitulo",
                "y": 370,
                "cor": (255, 255, 255),
            },
        )

        builder.adicionar(
            "comentario_resultado",
            LayerType.TEXT,
            40,
            0,
            duracao,
            propriedades={
                "texto": "CONTE NOS COMENTÁRIOS!",
                "tipo_texto": "resultado_comentario",
                "y": 470,
                "cor": (235, 225, 255),
            },
        )

        builder.adicionar(
            "rodape_resultado",
            LayerType.TEXT,
            45,
            0,
            duracao,
            propriedades={
                "texto": "A ESCOLHA É TODA SUA!",
                "tipo_texto": "resultado_rodape",
                "y": 584,
                "cor": (74, 45, 145),
            },
        )

        builder.adicionar(
            "confetes",
            LayerType.EFFECT,
            80,
            0,
            min(duracao, 1.2),
            propriedades={
                "efeito": "confetti",
                "quantidade": preset.quantidade_confetes,
            },
        )

        builder.adicionar(
            "mascote",
            LayerType.MASCOT,
            100,
            0,
            duracao,
            propriedades={
                "pose": "celebrate",
                "comportamento": "celebrate",
                "intensidade": 1.15,
                "posicao": "inferior_direita",
            },
        )

        builder.scene.metadados.update({
            "numero": numero,
            "etapa": "resultado",
            "tipo_quiz": "preferencia",
            "layout": layout.nome,
            "preset": preset.nome,
            "intensidade_fx": (
                preset.intensidade_particulas
            ),
            "premium_theme": {
                "nome": (
                    premium_theme.nome
                    if premium_theme
                    else "Moleza Vibrante"
                ),
                "codigo": (
                    premium_theme.codigo
                    if premium_theme
                    else "moleza_vibrante"
                ),
                "familia_fonte": (
                    premium_theme.familia_fonte
                    if premium_theme
                    else "rounded"
                ),
                "titulo_tamanho": (
                    premium_theme.titulo_tamanho
                    if premium_theme
                    else 43
                ),
                "alternativa_tamanho": (
                    premium_theme.alternativa_tamanho
                    if premium_theme
                    else 28
                ),
                "arredondamento_cartao": (
                    premium_theme.arredondamento_cartao
                    if premium_theme
                    else 34
                ),
                "particulas": (
                    premium_theme.particulas
                    if premium_theme
                    else "sparkles"
                ),
                "efeito_ambiente": (
                    premium_theme.efeito_ambiente
                    if premium_theme
                    else "mixed_glow"
                ),
                "estilo_camera": (
                    premium_theme.estilo_camera
                    if premium_theme
                    else "equilibrada"
                ),
                "intensidade_fx": (
                    premium_theme.intensidade_fx
                    if premium_theme
                    else 0.55
                ),
                "intensidade_glow": (
                    premium_theme.intensidade_glow
                    if premium_theme
                    else 0.36
                ),
                "cor_texto": (
                    premium_theme.cor_texto
                    if premium_theme
                    else (255, 255, 255)
                ),
                "cor_secundaria": (
                    premium_theme.cor_secundaria
                    if premium_theme
                    else (240, 235, 255)
                ),
            },
            "camera": {
                "nome": self.camera_profiles.obter(numero).nome,
                "zoom_inicial": self.camera_profiles.obter(numero).zoom_inicial,
                "zoom_final": self.camera_profiles.obter(numero).zoom_final,
                "pan_x": self.camera_profiles.obter(numero).pan_x,
                "pan_y": self.camera_profiles.obter(numero).pan_y,
                "rotacao": self.camera_profiles.obter(numero).rotacao,
                "pulso_brilho": self.camera_profiles.obter(numero).pulso_brilho,
            },
        })

        return builder.construir()


    def criar_entrada(
        self,
        pergunta,
        numero,
        layout,
        preset,
        duracao=1.1,
        premium_theme=None,
    ):
        builder = TimelineSceneBuilder(
            nome=f"pergunta_{numero:03d}_entrada",
            duracao=duracao,
        )

        builder.adicionar(
            "fundo",
            LayerType.BACKGROUND,
            0,
            0,
            duracao,
            propriedades={
                "preset": preset.nome,
                "cor_inicio": preset.cor_fundo_inicio,
                "cor_fim": preset.cor_fundo_fim,
                "cor_painel": preset.cor_painel,
            },
        )

        alternativas = pergunta.get(
            "alternativas",
            []
        )

        # Cartão A entra primeiro pela esquerda.
        builder.adicionar(
            "cartao_a",
            LayerType.CARD,
            20,
            0.0,
            duracao,
            propriedades={
                "caixa": layout.caixa_a,
                "cor": preset.paletas_perguntas[0]["a"],
                "entrada": "esquerda",
                "duracao_entrada": 0.72,
                "easing_entrada": "ease_out_back",
                "overshoot": 1.45,
            },
        )

        builder.adicionar(
            "imagem_a",
            LayerType.IMAGE,
            30,
            0.05,
            max(duracao - 0.05, 0.1),
            origem=pergunta.get("imagem_a"),
            propriedades={
                "entrada": "esquerda",
                "duracao_entrada": 0.72,
                "easing_entrada": "ease_out_back",
                "overshoot": 1.45,
            },
        )

        builder.adicionar(
            "texto_a",
            LayerType.TEXT,
            35,
            0.05,
            max(duracao - 0.05, 0.1),
            propriedades={
                "texto": (
                    alternativas[0]
                    if alternativas
                    else "A"
                ),
                "caixa": layout.caixa_a,
                "entrada": "esquerda",
                "duracao_entrada": 0.72,
                "easing_entrada": "ease_out_back",
                "overshoot": 1.45,
            },
        )

        # Cartão B entra com pequeno atraso pela direita.
        builder.adicionar(
            "cartao_b",
            LayerType.CARD,
            20,
            0.12,
            max(duracao - 0.12, 0.1),
            propriedades={
                "caixa": layout.caixa_b,
                "cor": preset.paletas_perguntas[0]["b"],
                "entrada": "direita",
                "duracao_entrada": 0.72,
                "easing_entrada": "ease_out_elastic",
            },
        )

        builder.adicionar(
            "imagem_b",
            LayerType.IMAGE,
            30,
            0.17,
            max(duracao - 0.17, 0.1),
            origem=pergunta.get("imagem_b"),
            propriedades={
                "entrada": "direita",
                "duracao_entrada": 0.72,
                "easing_entrada": "ease_out_elastic",
            },
        )

        builder.adicionar(
            "texto_b",
            LayerType.TEXT,
            35,
            0.17,
            max(duracao - 0.17, 0.1),
            propriedades={
                "texto": (
                    alternativas[1]
                    if len(alternativas) > 1
                    else "B"
                ),
                "caixa": layout.caixa_b,
                "entrada": "direita",
                "duracao_entrada": 0.72,
                "easing_entrada": "ease_out_elastic",
            },
        )

        builder.adicionar(
            "ou",
            LayerType.BADGE,
            40,
            0.42,
            max(duracao - 0.42, 0.1),
            origem="assets/ui/ou.png",
            propriedades={
                "caixa": layout.caixa_ou,
                "entrada": "pop",
                "duracao_entrada": 0.5,
                "easing_entrada": "ease_out_bounce",
            },
        )

        builder.adicionar(
            "titulo",
            LayerType.TEXT,
            50,
            0,
            duracao,
            propriedades={
                "texto": pergunta.get(
                    "pergunta",
                    ""
                ),
            },
        )

        builder.adicionar(
            "mascote",
            LayerType.MASCOT,
            100,
            0,
            duracao,
            propriedades={
                "pose": (
                    "point_left"
                    if numero % 2 == 1
                    else "point_right"
                ),
                "comportamento": (
                    "point_left"
                    if numero % 2 == 1
                    else "point_right"
                ),
                "intensidade": 1.0,
                "posicao": "inferior_direita",
            },
        )

        builder.scene.metadados.update({
            "numero": numero,
            "etapa": "entrada",
            "tipo_quiz": "preferencia",
            "layout": layout.nome,
            "preset": preset.nome,
        })

        return builder.construir()
