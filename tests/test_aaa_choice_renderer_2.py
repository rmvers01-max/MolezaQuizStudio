from core.video.choice_experience import AAAChoiceVisualDirector
from core.video.curiosity import CuriosityDistributionDirector


def question_with_curiosity():
    return {
        "pergunta": "O que você prefere?",
        "alternativas": ["Pizza", "Sorvete"],
        "curiosidade_a": "Curiosidade da pizza.",
        "curiosidade_b": "Curiosidade do sorvete.",
    }


def test_curiosity_not_selected_for_every_question():
    director = CuriosityDistributionDirector()
    selected = []

    for number in range(1, 11):
        decision = director.decide(
            question=question_with_curiosity(),
            question_number=number,
            total_questions=10,
            quiz_type="preferencia",
        )
        if decision.enabled:
            selected.append(number)

    assert 1 <= len(selected) <= 4
    assert all(
        second - first > 1
        for first, second in zip(
            selected,
            selected[1:],
        )
    )


def test_force_and_disable_override():
    director = CuriosityDistributionDirector()

    forced = director.decide(
        question={
            **question_with_curiosity(),
            "usar_curiosidade": True,
        },
        question_number=2,
        total_questions=10,
        quiz_type="preferencia",
    )

    disabled = director.decide(
        question={
            **question_with_curiosity(),
            "usar_curiosidade": False,
        },
        question_number=5,
        total_questions=10,
        quiz_type="preferencia",
    )

    assert forced.enabled is True
    assert forced.forced is True
    assert disabled.enabled is False


def test_choice_profile_never_uses_correct_answer():
    profile = AAAChoiceVisualDirector().choose(
        question_number=3,
        total_questions=10,
        has_images=True,
        curiosity_selected=True,
    )

    assert profile.metadata[
        "no_correct_answer"
    ] is True
    assert (
        profile.transition_style
        == "curiosity_bridge"
    )
