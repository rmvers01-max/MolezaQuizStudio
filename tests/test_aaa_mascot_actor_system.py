from core.video.mascot_actor import MascotPerformanceDirector

def test_question_has_three_beats():
    p=MascotPerformanceDirector().create_performance(scene_kind='question',question_number=1,duration=4,difficulty=70,focus_side='left')
    assert len(p.beats)==3 and p.preferred_side=='right' and p.beats[1].pose=='thinking'

def test_reveal_celebrates():
    p=MascotPerformanceDirector().create_performance(scene_kind='reveal',question_number=5,duration=2.2,difficulty=80,surprise=True,correct_reveal=True)
    assert p.beats[-1].pose=='celebrate'
