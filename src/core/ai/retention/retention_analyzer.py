from __future__ import annotations


class RetentionAnalyzer:
    """Auditoria simples e determinística do plano do vídeo."""

    def analisar(
        self,
        plano: dict,
    ) -> dict:
        alertas = []
        pontuacao = 100

        abertura = float(
            plano.get(
                "abertura_maxima",
                5.0
            )
        )

        if abertura > 5.0:
            alertas.append(
                "A abertura ultrapassa 5 segundos."
            )
            pontuacao -= 12

        intervalo = int(
            plano.get(
                "intervalo_pattern_break",
                4
            )
        )

        if intervalo > 5:
            alertas.append(
                "Há pouca variação visual entre perguntas."
            )
            pontuacao -= 10

        if not plano.get(
            "cta_final",
            True
        ):
            alertas.append(
                "O vídeo não possui CTA final."
            )
            pontuacao -= 8

        if not plano.get(
            "primeira_pergunta_rapida",
            True
        ):
            alertas.append(
                "A primeira pergunta demora a começar."
            )
            pontuacao -= 15

        pontuacao = max(
            min(pontuacao, 100),
            0
        )

        return {
            "pontuacao_retencao": pontuacao,
            "classificacao": (
                "excelente"
                if pontuacao >= 90
                else "boa"
                if pontuacao >= 80
                else "precisa_de_ajustes"
            ),
            "alertas": alertas,
        }
