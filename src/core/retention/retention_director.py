from __future__ import annotations

import hashlib
import json
from pathlib import Path

from .retention_analyzer import RetentionAnalyzer
from .retention_profile import RetentionProfile


class RetentionDirector:
    """
    Controla ritmo, variedade e pontos de surpresa do vídeo.

    Não depende de chamadas externas. As decisões são reproduzíveis
    para que o mesmo projeto gere sempre o mesmo plano.
    """

    def __init__(self):
        self.profile = RetentionProfile(
            nome="Moleza Retention",
            abertura_maxima=4.5,
            entrada_minima=0.78,
            entrada_maxima=1.02,
            resultado_minimo=1.75,
            resultado_maximo=2.20,
            mudanca_visual_maxima=4.0,
            intervalo_pattern_break=4,
            limite_texto_pergunta=86,
            limite_texto_alternativa=28,
            intensidade_base=0.72,
            usar_cta_intermediario=True,
            usar_cta_final=True,
        )

        self.analyzer = RetentionAnalyzer()

    def criar_plano_video(
        self,
        titulo: str,
        total_perguntas: int,
        brand_direction: dict | None = None,
    ) -> dict:
        total = max(
            int(total_perguntas),
            1
        )

        semente = self._semente(
            titulo
        )

        intervalo = (
            3
            if total >= 25
            else 4
            if total >= 12
            else 3
        )

        pontos_cta = []

        if (
            self.profile.usar_cta_intermediario
            and total >= 10
        ):
            pontos_cta.append(
                max(
                    int(total * 0.38),
                    4
                )
            )

        if total >= 24:
            pontos_cta.append(
                max(
                    int(total * 0.74),
                    10
                )
            )

        plano = {
            "titulo": str(titulo),
            "total_perguntas": total,
            "abertura_maxima": (
                self.profile.abertura_maxima
            ),
            "primeira_pergunta_rapida": True,
            "intervalo_pattern_break": intervalo,
            "mudanca_visual_maxima": (
                self.profile
                .mudanca_visual_maxima
            ),
            "cta_intermediarios": pontos_cta,
            "cta_final": (
                self.profile.usar_cta_final
            ),
            "semente_criativa": semente,
            "energia_base": float(
                (
                    brand_direction
                    or {}
                ).get(
                    "energia_video",
                    self.profile.intensidade_base
                )
            ),
        }

        plano["auditoria"] = (
            self.analyzer.analisar(
                plano
            )
        )

        return plano

    def decisao_pergunta(
        self,
        plano: dict,
        numero: int,
    ) -> dict:
        numero = max(
            int(numero),
            1
        )

        intervalo = max(
            int(
                plano.get(
                    "intervalo_pattern_break",
                    4
                )
            ),
            2
        )

        pattern_break = (
            numero > 1
            and numero % intervalo == 0
        )

        variacao = (
            int(
                plano.get(
                    "semente_criativa",
                    0
                )
            )
            + numero
        ) % 6

        duracoes_entrada = (
            0.82,
            0.90,
            0.86,
            0.96,
            0.84,
            0.92,
        )

        duracoes_resultado = (
            1.80,
            1.95,
            1.85,
            2.10,
            1.90,
            2.00,
        )

        poses = (
            "point_left",
            "point_right",
            "idle",
            "happy",
            "wave",
            "idle",
        )

        intensidade = float(
            plano.get(
                "energia_base",
                0.72
            )
        )

        if pattern_break:
            intensidade = min(
                intensidade + 0.12,
                0.95
            )

        return {
            "numero": numero,
            "pattern_break": pattern_break,
            "variacao": variacao,
            "duracao_entrada": (
                duracoes_entrada[
                    variacao
                ]
            ),
            "duracao_resultado": (
                duracoes_resultado[
                    variacao
                ]
            ),
            "mascote_pose_entrada": (
                poses[variacao]
            ),
            "intensidade_fx": intensidade,
            "camera_bonus": (
                0.006
                if pattern_break
                else 0.0
            ),
            "cta_curto": (
                numero
                in plano.get(
                    "cta_intermediarios",
                    []
                )
            ),
        }

    def salvar_relatorio(
        self,
        plano: dict,
        caminho,
    ) -> Path:
        caminho = Path(
            caminho
        )

        caminho.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        caminho.write_text(
            json.dumps(
                plano,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return caminho

    def _semente(
        self,
        texto: str,
    ) -> int:
        digest = hashlib.sha256(
            str(texto).encode(
                "utf-8"
            )
        ).hexdigest()

        return int(
            digest[:8],
            16
        )
