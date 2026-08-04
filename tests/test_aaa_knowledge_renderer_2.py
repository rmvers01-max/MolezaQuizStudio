from core.video.knowledge_experience import (
    AAAKnowledgeVisualDirector,
    KnowledgeRevealPlanner,
)

def test_flags_use_geography_preset():
    profile = AAAKnowledgeVisualDirector().choose(
        question={
            "pergunta": "Qual é esta bandeira?",
            "alternativas": ["Brasil", "Portugal", "França", "Itália"],
            "imagem": "brasil.png",
        },
        question_number=2,
        total_questions=10,
        category="flags_geography",
        curiosity_selected=False,
    )
    assert profile.image_mode == "hero_flag"
    assert profile.countdown_style == "radial_compass"
    assert profile.metadata["correct_answer_required"] is True

def test_reveal_does_not_use_red_cross():
    profile = AAAKnowledgeVisualDirector().choose(
        question={"alternativas": ["A", "B", "C", "D"]},
        question_number=4,
        total_questions=10,
        category="general_knowledge",
        curiosity_selected=False,
    )
    reveal = KnowledgeRevealPlanner().create(
        question={
            "resposta_correta_indice": 0,
            "resposta_correta": "Brasília",
            "explicacao": "Brasília é a capital federal.",
        },
        profile=profile,
    )
    assert reveal["highlight_correct"] is True
    assert reveal["show_red_cross"] is False
    assert reveal["show_explanation"] is True

def test_final_questions_receive_more_energy():
    director = AAAKnowledgeVisualDirector()
    normal = director.choose(
        question={"alternativas": ["A", "B", "C", "D"]},
        question_number=2,
        total_questions=10,
        category="general_knowledge",
        curiosity_selected=False,
    )
    final = director.choose(
        question={"alternativas": ["A", "B", "C", "D"]},
        question_number=9,
        total_questions=10,
        category="general_knowledge",
        curiosity_selected=False,
    )
    assert final.particle_intensity > normal.particle_intensity
