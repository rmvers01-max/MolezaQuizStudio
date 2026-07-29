import math


def clamp(valor: float, minimo: float = 0.0, maximo: float = 1.0) -> float:
    return max(minimo, min(maximo, float(valor)))


def ease_out_cubic(t: float) -> float:
    t = clamp(t)
    return 1.0 - pow(1.0 - t, 3)


def ease_out_back(t: float) -> float:
    t = clamp(t)
    constante_1 = 1.70158
    constante_3 = constante_1 + 1.0

    return (
        1.0
        + constante_3 * pow(t - 1.0, 3)
        + constante_1 * pow(t - 1.0, 2)
    )


def ease_in_out_sine(t: float) -> float:
    t = clamp(t)
    return -(math.cos(math.pi * t) - 1.0) / 2.0


def pulse(t: float, ciclos: float = 1.0) -> float:
    t = clamp(t)
    return math.sin(t * math.pi * 2.0 * ciclos)
