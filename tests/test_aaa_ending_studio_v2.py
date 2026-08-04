from core.video.outro import AAAEndingDirector, EndingQualityAnalyzer

def test_preference_has_no_score():
    d=AAAEndingDirector().choose(category='preference',quiz_type='preferencia')
    assert d.show_score_prompt is False
    assert d.show_comment_prompt is True
    assert 'ESCOLHAS' in d.headline
    assert EndingQualityAnalyzer().analyze(d)['score'] >= 92

def test_knowledge_invites_score_without_inventing_it():
    d=AAAEndingDirector().choose(category='flags_geography',quiz_type='conhecimento')
    assert d.show_score_prompt is True
    assert 'PONTUAÇÃO' in d.primary_cta
    assert '17/20' not in d.supporting_text
