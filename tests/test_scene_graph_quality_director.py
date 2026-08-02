from core.video.scene_graph import (
    Rect,
    SceneGraph,
    SceneGraphQualityDirector,
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
            Rect(100, 70, 1080, 120),
            safe_area=True,
            tags={"content"},
        )
    )

    root.add(
        SceneNode(
            "progress",
            Rect(990, 20, 190, 50),
            safe_area=True,
            tags={"content"},
        )
    )

    return SceneGraph(
        1280,
        720,
        root,
    )


def test_valid_question_is_renderable():
    report = SceneGraphQualityDirector().preflight(
        graph=build_graph(),
        scene_kind="question",
        question_text="Qual é esta bandeira?",
        alternatives=[],
        has_image=False,
        image_path=None,
        theme_pack={
            "text_color": (30, 40, 70),
            "panel_color": (245, 245, 250),
        },
    )

    assert report.can_render is True


def test_empty_question_blocks_scene():
    report = SceneGraphQualityDirector().preflight(
        graph=build_graph(),
        scene_kind="question",
        question_text="",
        alternatives=[],
        has_image=False,
        image_path=None,
        theme_pack={},
    )

    assert report.can_render is False
    assert report.status == "blocked"


def test_orphan_effect_is_hidden():
    graph = build_graph()

    effect = graph.root.add(
        SceneNode(
            "orphan_glow",
            Rect(100, 100, 100, 100),
            tags={"effect"},
            metadata={
                "scope": "target",
                "target_node_id": "missing_card",
            },
        )
    )

    report = SceneGraphQualityDirector().preflight(
        graph=graph,
        scene_kind="question",
        question_text="Pergunta válida",
        alternatives=[],
        has_image=False,
        image_path=None,
        theme_pack={},
    )

    assert effect.visible is False
    assert report.auto_fixes >= 1
