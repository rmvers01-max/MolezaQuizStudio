from core.video.production_engine import DataIntelligenceEngine, IntelligentProductionEngine

def test_detects_flags():
    profile = DataIntelligenceEngine().analyze(
        title="Adivinhe a Bandeira",
        quiz_type="conhecimento",
        questions=[{"pergunta":"Qual país possui esta bandeira?","alternativas":["Brasil","Portugal"],"imagem":"x.png"}],
    )
    assert profile.category == "flags_geography"

def test_creates_plan():
    plan = IntelligentProductionEngine().create_plan(
        title="Adivinhe a Bandeira",
        quiz_type="conhecimento",
        questions=[{"pergunta":"Qual país possui esta bandeira?","alternativas":["Brasil","Portugal"],"imagem":"x.png"}],
        production_plan={"pacing_mode":"steady_game"},
        question_plan={"questions":[{"question_number":1,"camera_intensity":.65,"reading_score":30,"surprise_moment":False}]},
        story_plan={"beats":[{"question_number":1,"chapter":"warm_up"}]},
    )
    assert plan.production_mode
    assert plan.publish_readiness_score >= 45
