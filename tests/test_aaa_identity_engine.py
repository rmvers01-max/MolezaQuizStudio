from core.video.cinematic_experience import CinematicExperienceLibrary
from core.video.identity_engine import AAAIdentityEngine

def test_theme_receives_identity():
    plan=AAAIdentityEngine().create_plan(
        category="flags_geography",
        theme_pack={"motion_intensity":1.4,"background_activity":1.2},
        production_mode="visual_guess_challenge",
    )
    assert plan.corrected_theme_pack["identity_code"]=="moleza_quiz"
    assert plan.corrected_theme_pack["motion_intensity"]<=.92
    assert plan.corrected_theme_pack["background_activity"]<=.82

def test_experience_limits():
    corrected=AAAIdentityEngine().enforce_experience(
        CinematicExperienceLibrary().victory()
    )
    assert corrected.vignette<=.20
    assert corrected.particle_intensity<=.76
    assert corrected.metadata["identity_enforced"] is True
