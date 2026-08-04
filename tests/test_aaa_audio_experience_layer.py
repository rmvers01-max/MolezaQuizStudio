from pathlib import Path
from core.video.audio_sync import AudioExperienceDirector, AudioSyncDirector, ProceduralSfxSynthesizer


def test_victory_reveal_selection():
    result=AudioExperienceDirector().choose(scene_kind='reveal',difficulty=80,surprise=True,pattern_break=False,emotional_tone='victory',final_zone=True)
    assert result['experience_code']=='victory_01'
    assert result['cue_type']=='victory_hit'


def test_procedural_sfx_is_created(tmp_path):
    path=ProceduralSfxSynthesizer().ensure(tmp_path,'competition_whoosh')
    assert path is not None and path.exists() and path.stat().st_size>1000


def test_question_cues_include_countdown_and_reveal(tmp_path):
    cues=AudioSyncDirector().build_question_cues(project_root=tmp_path,question_number=4,total_questions=10,question_start=0,question_duration=1,response_time=3,reveal_duration=2,difficulty=78,surprise=True,emotional_tone='suspense',force_pattern_break=True)
    kinds=[c.cue_type for c in cues]
    assert kinds.count('suspense_tick')==3
    assert 'victory_hit' in kinds
