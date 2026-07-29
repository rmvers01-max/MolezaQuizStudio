from __future__ import annotations

import math


class SmartEasing:
    """Curvas profissionais de animação usadas pela timeline."""

    @staticmethod
    def clamp(valor):
        return max(
            0.0,
            min(
                float(valor),
                1.0
            )
        )

    @classmethod
    def linear(cls, t):
        return cls.clamp(t)

    @classmethod
    def ease_out_cubic(cls, t):
        t = cls.clamp(t)
        return 1.0 - pow(
            1.0 - t,
            3
        )

    @classmethod
    def ease_out_back(
        cls,
        t,
        overshoot=1.70158
    ):
        t = cls.clamp(t)
        c1 = float(overshoot)
        c3 = c1 + 1.0

        return (
            1.0
            + c3
            * pow(
                t - 1.0,
                3
            )
            + c1
            * pow(
                t - 1.0,
                2
            )
        )

    @classmethod
    def ease_out_elastic(cls, t):
        t = cls.clamp(t)

        if t == 0.0:
            return 0.0

        if t == 1.0:
            return 1.0

        constante = (
            2.0
            * math.pi
            / 3.0
        )

        return (
            pow(
                2.0,
                -10.0 * t
            )
            * math.sin(
                (
                    t * 10.0
                    - 0.75
                )
                * constante
            )
            + 1.0
        )

    @classmethod
    def ease_out_bounce(cls, t):
        t = cls.clamp(t)
        n1 = 7.5625
        d1 = 2.75

        if t < 1.0 / d1:
            return n1 * t * t

        if t < 2.0 / d1:
            t -= 1.5 / d1
            return n1 * t * t + 0.75

        if t < 2.5 / d1:
            t -= 2.25 / d1
            return n1 * t * t + 0.9375

        t -= 2.625 / d1
        return n1 * t * t + 0.984375

    @classmethod
    def spring(
        cls,
        t,
        damping=7.5,
        frequency=10.0
    ):
        t = cls.clamp(t)

        if t >= 1.0:
            return 1.0

        return (
            1.0
            - math.exp(
                -float(damping)
                * t
            )
            * math.cos(
                float(frequency)
                * t
            )
        )

    @classmethod
    def aplicar(
        cls,
        nome,
        t,
        **parametros
    ):
        chave = str(
            nome or "linear"
        ).strip().lower()

        if chave == "ease_out_cubic":
            return cls.ease_out_cubic(t)

        if chave == "ease_out_back":
            return cls.ease_out_back(
                t,
                overshoot=parametros.get(
                    "overshoot",
                    1.70158
                )
            )

        if chave == "ease_out_elastic":
            return cls.ease_out_elastic(t)

        if chave == "ease_out_bounce":
            return cls.ease_out_bounce(t)

        if chave == "spring":
            return cls.spring(
                t,
                damping=parametros.get(
                    "damping",
                    7.5
                ),
                frequency=parametros.get(
                    "frequency",
                    10.0
                )
            )

        return cls.linear(t)
