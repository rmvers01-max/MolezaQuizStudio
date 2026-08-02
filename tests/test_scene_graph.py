from core.video.scene_graph import (
    Rect,
    SafeAreaResolver,
    SceneGraph,
    SceneGraphValidator,
    SceneNode,
)


def test_rect_overlap():
    assert Rect(0, 0, 100, 100).intersects(Rect(50, 50, 100, 100))
    assert not Rect(0, 0, 20, 20).intersects(Rect(30, 30, 20, 20))


def test_validator_detects_safe_overlap():
    root = SceneNode("root", Rect(0, 0, 1280, 720), allow_overlap=True)
    root.add(SceneNode("question", Rect(100, 100, 500, 200), safe_area=True, priority=100))
    root.add(SceneNode("mascot", Rect(400, 150, 220, 220), priority=40))
    graph = SceneGraph(1280, 720, root)
    issues = SceneGraphValidator().validate(graph)
    assert any(issue.code in {"visual_overlap", "safe_area_blocked"} for issue in issues)


def test_resolver_moves_movable_node():
    root = SceneNode("root", Rect(0, 0, 1280, 720), allow_overlap=True)
    safe = root.add(SceneNode("content", Rect(850, 430, 350, 250), safe_area=True, priority=100))
    mascot = root.add(SceneNode("mascot", Rect(900, 480, 200, 200), priority=40, metadata={"movable": True}))
    graph = SafeAreaResolver().resolve(SceneGraph(1280, 720, root))
    assert graph.find("mascot").bounds.overlap_ratio(safe.bounds) < 0.12
