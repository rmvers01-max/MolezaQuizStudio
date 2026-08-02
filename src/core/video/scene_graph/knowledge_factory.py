from __future__ import annotations

from PIL import Image

from .context import SceneRenderContext
from .geometry import Rect
from .nodes import SceneGraph, SceneNode


class KnowledgeSceneGraphFactory:
    def __init__(self, width: int, height: int):
        self.width = int(width)
        self.height = int(height)

    def build(
        self,
        *,
        layout,
        renderers: dict,
        alternative_count: int,
        has_image: bool,
        scene_kind: str,
    ) -> SceneGraph:
        root = SceneNode(
            node_id="scene_root",
            bounds=Rect(0, 0, self.width, self.height),
            z_index=0,
            allow_overlap=True,
            renderer=renderers.get("background"),
        )

        root.add(SceneNode(
            "question",
            Rect(layout.question.x, layout.question.y, layout.question.width, layout.question.height),
            z_index=20,
            priority=100,
            safe_area=True,
            tags={"content", "text", "primary"},
            renderer=renderers.get("question"),
        ))

        root.add(SceneNode(
            "progress",
            Rect(layout.progress.x, layout.progress.y, layout.progress.width, layout.progress.height),
            z_index=30,
            priority=80,
            safe_area=True,
            tags={"status"},
            renderer=renderers.get("progress"),
        ))

        if has_image and layout.main_image is not None:
            root.add(SceneNode(
                "main_image",
                Rect(layout.main_image.x, layout.main_image.y, layout.main_image.width, layout.main_image.height),
                z_index=20,
                priority=95,
                safe_area=True,
                tags={"content", "image", "primary"},
                renderer=renderers.get("main_image"),
            ))

        for index, box in enumerate(layout.choices[:alternative_count], start=1):
            root.add(SceneNode(
                f"choice_{index}",
                Rect(box.x, box.y, box.width, box.height),
                z_index=20,
                priority=90,
                safe_area=True,
                tags={"content", "choice"},
                renderer=renderers.get(f"choice_{index}"),
            ))

        if scene_kind == "countdown":
            root.add(SceneNode(
                "timer",
                Rect(layout.timer.x, layout.timer.y, layout.timer.width, layout.timer.height),
                z_index=35,
                priority=85,
                safe_area=True,
                tags={"status", "timer"},
                renderer=renderers.get("timer"),
            ))

        if scene_kind == "reveal":
            root.add(SceneNode(
                "answer",
                Rect(layout.answer.x, layout.answer.y, layout.answer.width, layout.answer.height),
                z_index=40,
                priority=100,
                safe_area=True,
                tags={"content", "answer", "primary"},
                renderer=renderers.get("answer"),
            ))

        root.add(SceneNode(
            "reveal_effect",
            Rect(0, 0, self.width, self.height),
            z_index=48,
            priority=12,
            allow_overlap=True,
            tags={"effect", "reveal"},
            metadata={"scope": "answer"},
            renderer=renderers.get("reveal_effect"),
        ))

        root.add(SceneNode(
            "pattern_accent",
            Rect(0, 0, self.width, self.height),
            z_index=50,
            priority=10,
            allow_overlap=True,
            tags={"effect", "pattern_break"},
            metadata={"scope": "scene"},
            renderer=renderers.get("pattern_accent"),
        ))

        root.add(SceneNode(
            "focus_effect",
            Rect(0, 0, self.width, self.height),
            z_index=55,
            priority=10,
            allow_overlap=True,
            tags={"effect", "focus"},
            metadata={"scope": "focus_target"},
            renderer=renderers.get("focus_effect"),
        ))

        root.add(SceneNode(
            "mascot",
            Rect(self.width - 205, self.height - 205, 190, 190),
            z_index=60,
            priority=45,
            allow_overlap=False,
            tags={"character"},
            metadata={"movable": True, "opposite_focus": True},
            renderer=renderers.get("mascot"),
        ))

        root.add(SceneNode(
            "camera_and_color",
            Rect(0, 0, self.width, self.height),
            z_index=100,
            priority=0,
            allow_overlap=True,
            tags={"post_process"},
            renderer=renderers.get("post_process"),
        ))

        return SceneGraph(
            width=self.width,
            height=self.height,
            root=root,
            metadata={
                "scene_kind": scene_kind,
                "has_image": has_image,
                "alternative_count": alternative_count,
                "graph_version": "1.0",
            },
        )
