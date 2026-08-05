from __future__ import annotations
import math

class MotionEasing:
    @staticmethod
    def clamp(value: float) -> float:
        return max(min(float(value), 1.0), 0.0)

    @classmethod
    def ease_out_cubic(cls, value: float) -> float:
        t = cls.clamp(value)
        return 1.0 - (1.0 - t) ** 3

    @classmethod
    def ease_in_out_cubic(cls, value: float) -> float:
        t = cls.clamp(value)
        return 4*t**3 if t < .5 else 1 - ((-2*t+2)**3)/2

    @classmethod
    def ease_out_back(cls, value: float, overshoot: float=1.70158) -> float:
        t = cls.clamp(value)
        c1, c3 = overshoot, overshoot + 1
        return 1 + c3*(t-1)**3 + c1*(t-1)**2

    @classmethod
    def ease_out_bounce(cls, value: float) -> float:
        t, n1, d1 = cls.clamp(value), 7.5625, 2.75
        if t < 1/d1:
            return n1*t*t
        if t < 2/d1:
            t -= 1.5/d1
            return n1*t*t + .75
        if t < 2.5/d1:
            t -= 2.25/d1
            return n1*t*t + .9375
        t -= 2.625/d1
        return n1*t*t + .984375

    @classmethod
    def spring(cls, value: float) -> float:
        t = cls.clamp(value)
        return 1 - math.cos(t*math.pi*4.5)*math.exp(-t*6)

    @classmethod
    def pulse(cls, value: float) -> float:
        return math.sin(cls.clamp(value)*math.pi)
