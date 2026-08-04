from core.video.mascot_actor import MascotPerformanceDirector


def test_question_uses_difficulty_and_focus():
    p=MascotPerformanceDirector().create_performance(
        scene_kind='question',question_number=2,duration=4.0,
        difficulty=82,focus_side='left',emotional_tone='challenge'
    )
    assert p.preferred_side=='right'
    assert p.beats[1].pose=='thinking'
    assert p.beats[-1].look_target=='choices'


def test_countdown_targets_timer():
    p=MascotPerformanceDirector().create_performance(
        scene_kind='countdown',question_number=3,duration=5.0,
        difficulty=60
    )
    assert p.beats[0].look_target=='timer'
    assert p.beats[-1].action=='encourage'


def test_reveal_story_tone_celebrates():
    p=MascotPerformanceDirector().create_performance(
        scene_kind='reveal',question_number=8,duration=2.0,
        difficulty=75,emotional_tone='victory',correct_reveal=False
    )
    assert p.beats[-1].pose=='celebrate'
