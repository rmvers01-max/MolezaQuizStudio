from PIL import Image

from core.video.scene_graph import KnowledgeSceneGraphFactory, SceneGraphFocusResolver
from core.video.universal.layouts import UniversalLayoutEngine


def test_effect_nodes_and_focus():
    layout = UniversalLayoutEngine(1280, 720).knowledge(4, True)
    graph = KnowledgeSceneGraphFactory(1280, 720).build(
        layout=layout,
        renderers={},
        alternative_count=4,
        has_image=True,
        scene_kind="question",
    )
    assert graph.find("mascot") is not None
    assert graph.find("focus_effect") is not None
    assert graph.find("reveal_effect") is not None
    target = SceneGraphFocusResolver().resolve(graph, "question")
    assert target.node_id == "main_image"
