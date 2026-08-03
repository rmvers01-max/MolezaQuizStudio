from core.video.production_engine import IPEExecutionLayer

def test_risk_becomes_runtime_directive():
    plan = IPEExecutionLayer().build({
        "production_mode":"visual_guess_challenge",
        "audience_risks":[{
            "start_question":2,"end_question":5,"risk_type":"visual_repetition",
            "proposed_action":{"force_pattern_break":True},
        }],
    })
    directive=plan.question(5)
    assert directive is not None
    assert directive.force_pattern_break is True
    assert directive.motion_boost > 0

def test_safety_limits_are_respected():
    plan=IPEExecutionLayer().build({
        "production_mode":"balanced_family_quiz",
        "audience_risks":[{
            "start_question":1,"end_question":1,"risk_type":"early_cognitive_load",
            "proposed_action":{"entry_duration_delta":99},
        }],
    })
    assert plan.question(1).entry_duration_delta <= .25
