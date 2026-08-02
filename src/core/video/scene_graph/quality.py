from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .geometry import Rect
from .nodes import SceneGraph


@dataclass(frozen=True, slots=True)
class QualityFinding:
    severity: str
    code: str
    message: str
    node_ids: tuple[str, ...] = ()
    auto_fixed: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "severity": self.severity,
            "code": self.code,
            "message": self.message,
            "node_ids": list(self.node_ids),
            "auto_fixed": self.auto_fixed,
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True, slots=True)
class QualityPreflightReport:
    score: int
    status: str
    can_render: bool
    findings: tuple[QualityFinding, ...]
    auto_fixes: int
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "score": self.score,
            "status": self.status,
            "can_render": self.can_render,
            "findings": [
                finding.to_dict()
                for finding in self.findings
            ],
            "auto_fixes": self.auto_fixes,
            "metadata": dict(self.metadata),
        }


class SceneGraphQualityDirector:
    ESSENTIAL_BY_SCENE = {
        "question": ("question", "progress"),
        "countdown": ("question", "progress", "timer"),
        "reveal": ("question", "progress", "answer"),
    }

    def preflight(
        self,
        *,
        graph: SceneGraph,
        scene_kind: str,
        question_text: str,
        alternatives: list[str],
        has_image: bool,
        image_path: str | None,
        theme_pack: dict[str, Any],
    ) -> QualityPreflightReport:
        findings: list[QualityFinding] = []

        self._normalize_nodes(graph, findings)
        self._check_essential_nodes(
            graph,
            scene_kind,
            findings,
        )
        self._check_content(
            graph,
            question_text,
            alternatives,
            has_image,
            image_path,
            findings,
        )
        self._check_effect_bindings(
            graph,
            findings,
        )
        self._protect_safe_content(
            graph,
            findings,
        )
        self._check_theme_contrast(
            theme_pack,
            findings,
        )

        errors = sum(
            1
            for finding in findings
            if (
                finding.severity == "error"
                and not finding.auto_fixed
            )
        )
        warnings = sum(
            1
            for finding in findings
            if (
                finding.severity == "warning"
                and not finding.auto_fixed
            )
        )
        auto_fixes = sum(
            1
            for finding in findings
            if finding.auto_fixed
        )

        score = max(
            100
            - errors * 25
            - warnings * 8
            - auto_fixes * 2,
            0,
        )
        can_render = errors == 0

        status = (
            "approved"
            if can_render and score >= 92
            else "approved_with_fixes"
            if can_render
            else "blocked"
        )

        graph.metadata["quality_preflight"] = {
            "score": score,
            "status": status,
            "can_render": can_render,
            "auto_fixes": auto_fixes,
        }

        return QualityPreflightReport(
            score=score,
            status=status,
            can_render=can_render,
            findings=tuple(findings),
            auto_fixes=auto_fixes,
            metadata={
                "director_version": "1.0",
                "scene_kind": scene_kind,
            },
        )

    def _normalize_nodes(
        self,
        graph,
        findings,
    ):
        viewport = Rect(
            0,
            0,
            graph.width,
            graph.height,
        )

        for node in graph.nodes():
            if not 0.0 <= float(node.opacity) <= 1.0:
                before = node.opacity
                node.opacity = min(
                    max(float(node.opacity), 0.0),
                    1.0,
                )
                findings.append(
                    QualityFinding(
                        "warning",
                        "opacity_normalized",
                        (
                            f"A opacidade de {node.node_id} "
                            "foi normalizada."
                        ),
                        (node.node_id,),
                        True,
                        {
                            "before": before,
                            "after": node.opacity,
                        },
                    )
                )

            if (
                node.bounds.width <= 0
                or node.bounds.height <= 0
            ):
                if "effect" in node.tags:
                    node.visible = False
                    findings.append(
                        QualityFinding(
                            "warning",
                            "invalid_effect_hidden",
                            (
                                f"O efeito {node.node_id} "
                                "foi ocultado por ter tamanho inválido."
                            ),
                            (node.node_id,),
                            True,
                        )
                    )
                else:
                    findings.append(
                        QualityFinding(
                            "error",
                            "invalid_content_bounds",
                            (
                                f"O elemento {node.node_id} "
                                "possui dimensões inválidas."
                            ),
                            (node.node_id,),
                        )
                    )
                continue

            clamped = node.bounds.clamp_inside(
                viewport
            )
            if clamped != node.bounds:
                before = node.bounds
                node.bounds = clamped
                findings.append(
                    QualityFinding(
                        "warning",
                        "node_clamped_to_viewport",
                        (
                            f"{node.node_id} foi mantido "
                            "dentro do vídeo."
                        ),
                        (node.node_id,),
                        True,
                        {
                            "before": before.as_tuple(),
                            "after": clamped.as_tuple(),
                        },
                    )
                )

    def _check_essential_nodes(
        self,
        graph,
        scene_kind,
        findings,
    ):
        for node_id in self.ESSENTIAL_BY_SCENE.get(
            scene_kind,
            (),
        ):
            node = graph.find(node_id)
            if node is None or not node.visible:
                findings.append(
                    QualityFinding(
                        "error",
                        "essential_node_missing",
                        (
                            f"O nó obrigatório {node_id} "
                            f"não existe na cena {scene_kind}."
                        ),
                        (node_id,),
                    )
                )

    def _check_content(
        self,
        graph,
        question_text,
        alternatives,
        has_image,
        image_path,
        findings,
    ):
        if not str(question_text).strip():
            findings.append(
                QualityFinding(
                    "error",
                    "empty_question",
                    "A pergunta está vazia.",
                    ("question",),
                )
            )

        if len(str(question_text)) > 180:
            findings.append(
                QualityFinding(
                    "warning",
                    "question_too_long",
                    (
                        "A pergunta possui texto demais "
                        "para uma única cena."
                    ),
                    ("question",),
                    metadata={
                        "length": len(
                            str(question_text)
                        ),
                    },
                )
            )

        visible_choices = [
            node
            for node in graph.nodes()
            if (
                node.visible
                and "choice" in node.tags
                and "sheen" not in node.tags
            )
        ]

        if alternatives and not visible_choices:
            findings.append(
                QualityFinding(
                    "error",
                    "choices_not_rendered",
                    (
                        "Existem alternativas, mas nenhum "
                        "cartão de resposta está visível."
                    ),
                )
            )

        if len(alternatives) > 6:
            findings.append(
                QualityFinding(
                    "warning",
                    "too_many_choices",
                    (
                        "Mais de seis alternativas podem "
                        "prejudicar a leitura."
                    ),
                    metadata={
                        "alternative_count": len(
                            alternatives
                        ),
                    },
                )
            )

        if has_image:
            image_node = graph.find("main_image")
            if image_node is None or not image_node.visible:
                findings.append(
                    QualityFinding(
                        "error",
                        "image_node_missing",
                        (
                            "A pergunta possui imagem, mas "
                            "main_image não está disponível."
                        ),
                        ("main_image",),
                    )
                )
            if not image_path:
                findings.append(
                    QualityFinding(
                        "error",
                        "image_path_missing",
                        (
                            "A pergunta exige imagem, mas "
                            "o caminho não foi informado."
                        ),
                        ("main_image",),
                    )
                )

    def _check_effect_bindings(
        self,
        graph,
        findings,
    ):
        for node in graph.nodes():
            if "effect" not in node.tags:
                continue

            target_id = node.metadata.get(
                "target_node_id"
            )
            scope = node.metadata.get("scope")

            if (
                scope == "target"
                and target_id
                and graph.find(str(target_id)) is None
            ):
                node.visible = False
                findings.append(
                    QualityFinding(
                        "warning",
                        "orphan_effect_hidden",
                        (
                            f"O efeito {node.node_id} perdeu "
                            f"o alvo {target_id} e foi ocultado."
                        ),
                        (
                            node.node_id,
                            str(target_id),
                        ),
                        True,
                    )
                )

            if (
                node.parent_id
                and graph.find(node.parent_id) is None
            ):
                node.visible = False
                findings.append(
                    QualityFinding(
                        "warning",
                        "orphan_child_hidden",
                        (
                            f"O nó {node.node_id} não possui "
                            "pai válido e foi ocultado."
                        ),
                        (node.node_id,),
                        True,
                    )
                )

    def _protect_safe_content(
        self,
        graph,
        findings,
    ):
        for node in graph.nodes():
            if (
                node.safe_area
                and node.visible
                and node.opacity < 0.65
            ):
                before = node.opacity
                node.opacity = 0.65
                findings.append(
                    QualityFinding(
                        "warning",
                        "safe_content_opacity_raised",
                        (
                            f"A opacidade de {node.node_id} "
                            "foi aumentada para preservar leitura."
                        ),
                        (node.node_id,),
                        True,
                        {
                            "before": before,
                            "after": node.opacity,
                        },
                    )
                )

    def _check_theme_contrast(
        self,
        theme_pack,
        findings,
    ):
        text = tuple(
            theme_pack.get(
                "text_color",
                (30, 45, 70),
            )
        )
        panel = tuple(
            theme_pack.get(
                "panel_color",
                (245, 240, 255),
            )
        )
        ratio = self._contrast_ratio(
            text,
            panel,
        )

        if ratio < 3.0:
            findings.append(
                QualityFinding(
                    "warning",
                    "low_text_contrast",
                    (
                        "O contraste entre texto e painel "
                        "está abaixo do nível recomendado."
                    ),
                    metadata={
                        "contrast_ratio": round(
                            ratio,
                            3,
                        ),
                    },
                )
            )

    def _contrast_ratio(
        self,
        foreground,
        background,
    ):
        first = self._luminance(
            foreground
        )
        second = self._luminance(
            background
        )

        lighter = max(first, second)
        darker = min(first, second)

        return (
            lighter + 0.05
        ) / (
            darker + 0.05
        )

    def _luminance(
        self,
        color,
    ):
        channels = []

        for raw in color[:3]:
            value = float(raw) / 255.0
            channels.append(
                value / 12.92
                if value <= 0.03928
                else (
                    (
                        value + 0.055
                    )
                    / 1.055
                ) ** 2.4
            )

        return (
            0.2126 * channels[0]
            + 0.7152 * channels[1]
            + 0.0722 * channels[2]
        )
