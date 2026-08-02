from core.video.scene_graph import (
    Rect,
    SceneGraph,
    SceneLayoutIntelligence,
    SceneNode,
)


def build_graph():
    root = SceneNode(
        "root",
        Rect(0, 0, 1280, 720),
    )

    root.add(
        SceneNode(
            "question",
            Rect(100, 70, 1080, 100),
            priority=100,
            safe_area=True,
            tags={"content"},
        )
    )

    root.add(
        SceneNode(
            "main_image",
            Rect(100, 210, 300, 190),
            priority=95,
            safe_area=True,
            tags={"content"},
        )
    )

    root.add(
        SceneNode(
            "choice_1",
            Rect(450, 220, 290, 70),
            priority=90,
            safe_area=True,
            tags={"content"},
        )
    )

    return SceneGraph(
        1280,
        720,
        root,
    )


def test_long_question_receives_more_height():
    graph = build_graph()

    report = SceneLayoutIntelligence().optimize(
        graph=graph,
        question_text_length=110,
        alternative_lengths=[20],
        has_image=True,
        scene_kind="question",
    )

    assert graph.find(
        "question"
    ).bounds.height > 100

    assert report.adjustments


def test_long_choice_receives_more_width():
    graph = build_graph()

    before = graph.find(
        "choice_1"
    ).bounds.width

    SceneLayoutIntelligence().optimize(
        graph=graph,
        question_text_length=30,
        alternative_lengths=[58],
        has_image=True,
        scene_kind="question",
    )

    assert graph.find(
        "choice_1"
    ).bounds.width > before
