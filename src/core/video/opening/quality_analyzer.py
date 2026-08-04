from __future__ import annotations


class OpeningQualityAnalyzer:
    def analyze(
        self,
        direction: dict,
    ) -> dict:
        score = 100
        findings = []

        duration = float(
            direction.get(
                "duracao",
                4.2,
            )
        )

        hook = str(
            direction.get(
                "hook_texto",
                "",
            )
        ).strip()

        challenge = str(
            direction.get(
                "desafio_texto",
                "",
            )
        ).strip()

        teasers = list(
            direction.get(
                "teaser_items",
                [],
            )
        )

        if duration > 5.2:
            score -= 18
            findings.append(
                "Abertura longa demais."
            )

        if duration < 3.2:
            score -= 12
            findings.append(
                "Abertura curta demais para explicar o desafio."
            )

        if not hook:
            score -= 30
            findings.append(
                "Gancho ausente."
            )

        if len(hook) > 62:
            score -= 10
            findings.append(
                "Gancho longo para o primeiro quadro."
            )

        if not challenge:
            score -= 20
            findings.append(
                "Convite para participar ausente."
            )

        if not teasers:
            score -= 10
            findings.append(
                "Tema não possui teaser visual."
            )

        if not direction.get(
            "usar_mascote",
            True,
        ):
            score -= 4
            findings.append(
                "Mascote não participa da abertura."
            )

        score = max(
            min(score, 100),
            0,
        )

        return {
            "score": score,
            "status": (
                "aaa_ready"
                if score >= 92
                else "approved"
                if score >= 80
                else "needs_revision"
            ),
            "findings": findings,
            "criteria": {
                "challenge_clear": bool(hook),
                "participation_clear": bool(
                    challenge
                ),
                "theme_visible": bool(teasers),
                "mascot_present": bool(
                    direction.get(
                        "usar_mascote",
                        True,
                    )
                ),
                "duration_safe": (
                    3.2 <= duration <= 5.2
                ),
            },
        }
