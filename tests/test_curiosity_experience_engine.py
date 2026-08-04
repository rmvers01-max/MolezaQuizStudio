from core.video.curiosity import CuriosityExperienceDirector

def test_preference_uses_two_user_supplied_curiosities():
    plan=CuriosityExperienceDirector().create_plan(
        question={"alternativas":["Pizza","Sorvete"],"curiosidade_a":"A pizza tem longa história.","curiosidade_b":"Existem muitos sabores de sorvete."},
        quiz_type="preferencia",category="preference")
    assert plan.enabled is True
    assert len(plan.items)==2

def test_missing_curiosity_does_not_invent_fact():
    plan=CuriosityExperienceDirector().create_plan(
        question={"alternativas":["A","B"]},quiz_type="preferencia",category="preference")
    assert plan.enabled is False
    assert plan.items == ()

def test_knowledge_accepts_explanation():
    plan=CuriosityExperienceDirector().create_plan(
        question={"explicacao":"Informação fornecida no projeto.","resposta":"Brasil"},quiz_type="conhecimento",category="flags_geography")
    assert plan.enabled
    assert plan.items[0].text.startswith("Informação")
