from __future__ import annotations

import hashlib


class OpeningHookLibrary:
    HOOKS = {
        "flags_geography": (
            "VOCÊ RECONHECE ESTAS BANDEIRAS?",
            "QUANTOS PAÍSES VOCÊ CONSEGUE ACERTAR?",
            "ESSA ÚLTIMA BANDEIRA COSTUMA ENGANAR!",
            "SERÁ QUE VOCÊ FAZ MAIS PONTOS QUE SEUS AMIGOS?",
            "PREPARE-SE PARA O DESAFIO DAS BANDEIRAS!",
        ),
        "preference": (
            "QUAL SERIA A SUA ESCOLHA?",
            "VOCÊ CONSEGUIRIA DECIDIR?",
            "SERÁ QUE FARÍAMOS AS MESMAS ESCOLHAS?",
            "ESCOLHA RÁPIDO E SEM ARREPENDIMENTO!",
            "ALGUMAS ESCOLHAS VÃO SER DIFÍCEIS!",
        ),
        "animals": (
            "VOCÊ RECONHECE TODOS ESTES ANIMAIS?",
            "QUE ANIMAL ESTÁ ESCONDIDO AQUI?",
            "SÓ OS MAIS ATENTOS ACERTAM TODOS!",
            "VAMOS DESCOBRIR QUANTOS VOCÊ CONHECE!",
        ),
        "food": (
            "VOCÊ CONSEGUE ESCOLHER ENTRE ESTAS DELÍCIAS?",
            "QUAL COMIDA VOCÊ ESCOLHERIA?",
            "ESSE DESAFIO VAI DAR FOME!",
            "PREPARE-SE PARA ESCOLHAS DELICIOSAS!",
        ),
        "sports": (
            "VOCÊ ESTÁ PRONTO PARA ESTE DESAFIO?",
            "QUANTOS PONTOS VOCÊ CONSEGUE FAZER?",
            "SÓ QUEM ENTENDE DE ESPORTE ACERTA TODAS!",
        ),
        "characters": (
            "VOCÊ SABE QUEM É ESTE PERSONAGEM?",
            "QUANTOS PERSONAGENS VOCÊ RECONHECE?",
            "A ÚLTIMA PISTA VAI SURPREENDER VOCÊ!",
        ),
        "general_knowledge": (
            "VOCÊ CONSEGUE ACERTAR TODAS?",
            "QUANTOS PONTOS VOCÊ VAI FAZER?",
            "PREPARE-SE PARA TESTAR SEUS CONHECIMENTOS!",
            "A ÚLTIMA PERGUNTA PODE SURPREENDER!",
        ),
    }

    CTA = {
        "flags_geography": (
            "MARQUE UM PONTO PARA CADA BANDEIRA!",
            "VEJA QUANTOS PAÍSES VOCÊ ACERTA!",
        ),
        "preference": (
            "ESCOLHA UMA OPÇÃO ANTES DO TEMPO ACABAR!",
            "CONTE QUANTAS ESCOLHAS FORAM IGUAIS ÀS SUAS!",
        ),
        "animals": (
            "MARQUE UM PONTO PARA CADA ANIMAL!",
            "VEJA QUANTOS VOCÊ RECONHECE!",
        ),
        "food": (
            "FAÇA SUA ESCOLHA ANTES DO TEMPO ACABAR!",
            "CONTE QUANTAS DELÍCIAS VOCÊ ESCOLHEU!",
        ),
        "sports": (
            "MARQUE UM PONTO PARA CADA ACERTO!",
        ),
        "characters": (
            "VEJA QUANTOS PERSONAGENS VOCÊ DESCOBRE!",
        ),
        "general_knowledge": (
            "MARQUE UM PONTO PARA CADA ACERTO!",
            "VEJA QUANTAS VOCÊ CONSEGUE ACERTAR!",
        ),
    }

    TEASERS = {
        "flags_geography": ("🇧🇷", "🇯🇵", "🇫🇷", "?"),
        "preference": ("🍕", "OU", "🍔"),
        "animals": ("🐶", "🐯", "🦁", "?"),
        "food": ("🍕", "🍫", "🍦", "?"),
        "sports": ("⚽", "🏀", "🏆", "?"),
        "characters": ("?", "★", "?", "★"),
        "general_knowledge": ("A", "B", "C", "?"),
    }

    def choose(
        self,
        *,
        category: str,
        title: str,
        total_questions: int,
    ) -> dict:
        category = (
            category
            if category in self.HOOKS
            else "general_knowledge"
        )

        seed = self._seed(
            f"{title}|{total_questions}|{category}"
        )

        hooks = self.HOOKS[category]
        ctas = self.CTA.get(
            category,
            self.CTA["general_knowledge"],
        )

        return {
            "hook": hooks[
                seed % len(hooks)
            ],
            "cta": ctas[
                (seed // 7) % len(ctas)
            ],
            "teasers": self.TEASERS.get(
                category,
                self.TEASERS[
                    "general_knowledge"
                ],
            ),
            "hook_index": (
                seed % len(hooks)
            ),
        }

    def _seed(self, value: str) -> int:
        digest = hashlib.sha256(
            value.encode("utf-8")
        ).hexdigest()

        return int(
            digest[:8],
            16,
        )
