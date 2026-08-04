from __future__ import annotations
from .models import MascotBeat, MascotPerformance

class MascotPerformanceDirector:
    def create_performance(self, *, scene_kind: str, question_number: int,
                           duration: float, difficulty: float = 50.0,
                           surprise: bool = False, correct_reveal: bool = False,
                           focus_side: str = "center", production_mode: str = ""):
        d=max(float(duration), .8)
        difficulty=max(0., min(float(difficulty),100.))
        side="right" if focus_side=="left" else "left"
        if scene_kind=="question":
            beats=(
                MascotBeat(0, min(.75,d*.25), "wave", "greet", "viewer", .78, "slide_bounce"),
                MascotBeat(min(.45,d*.18), max(min(d*.72,d-.18),.55),
                           "thinking" if difficulty>=55 else "happy",
                           "observe", "question", .88 if difficulty>=70 else .68),
                MascotBeat(max(d*.67,.58), d,
                           "point_left" if side=="left" else "point_right",
                           "guide", "choices", .84, "soft_pop", "soft_exit"),
            )
        elif scene_kind=="countdown":
            beats=(
                MascotBeat(0,d*.58,"thinking","anticipate","timer",.84),
                MascotBeat(d*.48,d,"point_left" if side=="left" else "point_right",
                           "encourage","choices",.94,"soft_pop"),
            )
        elif scene_kind=="reveal":
            beats=(
                MascotBeat(0,min(d*.3,.55),"thinking","suspense","answer",.72),
                MascotBeat(min(d*.22,.42),d,
                           "celebrate" if (correct_reveal or surprise) else "happy",
                           "celebrate" if (correct_reveal or surprise) else "approve",
                           "answer",1.0 if surprise else .9,"impact_pop","bounce_out"),
            )
        else:
            beats=(MascotBeat(0,d,"idle","breathe","viewer",.55),)
        return MascotPerformance(scene_kind, max(int(question_number),0), beats, side,
                                 round(min(.58+difficulty/100*.22+(.14 if surprise else 0),1),3),
                                 {"version":"1.0","production_mode":production_mode})
