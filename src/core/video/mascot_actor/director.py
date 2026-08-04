from __future__ import annotations
from .models import MascotBeat, MascotPerformance


class MascotPerformanceDirector:
    """Converte o estado narrativo da cena em uma atuação curta do mascote."""

    def create_performance(
        self,
        *,
        scene_kind: str,
        question_number: int,
        duration: float,
        difficulty: float = 50.0,
        surprise: bool = False,
        correct_reveal: bool = False,
        focus_side: str = "center",
        production_mode: str = "",
        emotional_tone: str = "",
        mascot_boost: float = 0.0,
    ) -> MascotPerformance:
        duration=max(float(duration),.8)
        difficulty=max(0.,min(float(difficulty),100.))
        mascot_boost=max(0.,min(float(mascot_boost),.25))
        side="right" if focus_side=="left" else "left"
        tone=str(emotional_tone or '').lower()

        if scene_kind=='question':
            middle_pose='thinking' if difficulty>=55 or tone in {'suspense','challenge'} else 'happy'
            beats=(
                MascotBeat(0.0,min(.72,duration*.24),'wave','greet','viewer',min(.78+mascot_boost,1.0),'slide_bounce'),
                MascotBeat(min(.42,duration*.17),max(min(duration*.72,duration-.18),.55),middle_pose,'observe','question',min((.88 if difficulty>=70 else .68)+mascot_boost,1.0),'hold'),
                MascotBeat(max(duration*.67,.58),duration,'point_left' if side=='left' else 'point_right','guide','choices',min(.84+mascot_boost,1.0),'soft_pop','soft_exit'),
            )
        elif scene_kind=='countdown':
            beats=(
                MascotBeat(0.0,duration*.58,'thinking','anticipate','timer',min(.84+mascot_boost,1.0),'hold'),
                MascotBeat(duration*.48,duration,'point_left' if side=='left' else 'point_right','encourage','choices',min(.94+mascot_boost,1.0),'soft_pop'),
            )
        elif scene_kind=='reveal':
            victory=bool(correct_reveal or surprise or tone=='victory')
            beats=(
                MascotBeat(0.0,min(duration*.30,.55),'thinking','suspense','answer',min(.72+mascot_boost,1.0),'hold'),
                MascotBeat(min(duration*.22,.42),duration,'celebrate' if victory else 'happy','celebrate' if victory else 'approve','answer',min((1.0 if surprise else .90)+mascot_boost,1.0),'impact_pop','bounce_out'),
            )
        else:
            beats=(MascotBeat(0.0,duration,'idle','breathe','viewer',min(.55+mascot_boost,1.0)),)

        return MascotPerformance(
            scene_kind=str(scene_kind),
            question_number=max(int(question_number),0),
            beats=beats,
            preferred_side=side,
            energy=round(min(.58+difficulty/100*.22+(.14 if surprise else 0)+mascot_boost,1.0),3),
            metadata={
                'version':'2.0',
                'production_mode':production_mode,
                'emotional_tone':tone,
                'surprise':bool(surprise),
                'difficulty':difficulty,
                'mascot_boost':mascot_boost,
            },
        )
