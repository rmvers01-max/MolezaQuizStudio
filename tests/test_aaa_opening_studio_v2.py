from core.video.opening import (
    OpeningDirector,
    OpeningQualityAnalyzer,
)


def test_flag_opening_uses_flag_teasers():
    direction = OpeningDirector().escolher(
        titulo="Adivinhe a Bandeira",
        total_perguntas=20,
        quiz_type="conhecimento",
        production_plan={
            "content_profile": {
                "category": "flags_geography",
            },
            "production_mode": (
                "visual_guess_challenge"
            ),
        },
    )

    assert (
        direction["categoria"]
        == "flags_geography"
    )

    assert "🇧🇷" in direction[
        "teaser_items"
    ]

    assert direction[
        "quality"
    ]["score"] >= 90


def test_preference_opening_uses_choice_camera():
    direction = OpeningDirector().escolher(
        titulo="O que você prefere?",
        total_perguntas=15,
        quiz_type="preferencia",
        production_plan={
            "content_profile": {
                "category": "preference",
            },
        },
    )

    assert (
        direction["camera_style"]
        == "competition_push"
    )

    assert direction[
        "transition_style"
    ] == "split_choice"


def test_quality_analyzer_blocks_missing_hook():
    report = OpeningQualityAnalyzer().analyze(
        {
            "duracao": 4.2,
            "hook_texto": "",
            "desafio_texto": "",
            "teaser_items": [],
            "usar_mascote": False,
        }
    )

    assert report["score"] < 80
