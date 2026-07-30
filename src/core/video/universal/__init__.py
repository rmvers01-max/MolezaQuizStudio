"""
Universal Quiz Engine.

Este inicializador usa carregamento preguiçoso para evitar ciclos entre:
- LegacyVideoGenerator;
- ProfessionalPreferenceRenderer;
- UniversalCreativeDirector;
- UniversalSceneRenderer.
"""

from __future__ import annotations

from importlib import import_module


_EXPORTS = {
    "FocusRole": (
        ".contracts",
        "FocusRole",
    ),
    "QuizScene": (
        ".contracts",
        "QuizScene",
    ),
    "QuizSceneType": (
        ".contracts",
        "QuizSceneType",
    ),
    "SceneElement": (
        ".contracts",
        "SceneElement",
    ),
    "UniversalQuizPlan": (
        ".contracts",
        "UniversalQuizPlan",
    ),
    "UniversalLegacyMotionRenderer": (
        ".legacy_motion",
        "UniversalLegacyMotionRenderer",
    ),
    "UniversalSceneRenderer": (
        ".scene_renderer",
        "UniversalSceneRenderer",
    ),
    "UniversalCreativeDirector": (
        ".creative_director",
        "UniversalCreativeDirector",
    ),
    "UniversalCreativePlanWriter": (
        ".creative_plan_writer",
        "UniversalCreativePlanWriter",
    ),
    "UniversalPlanWriter": (
        ".plan_writer",
        "UniversalPlanWriter",
    ),
    "UniversalQuizAdapterRegistry": (
        ".registry",
        "UniversalQuizAdapterRegistry",
    ),
}


__all__ = list(
    _EXPORTS.keys()
)


def __getattr__(name):
    target = _EXPORTS.get(
        name
    )

    if target is None:
        raise AttributeError(
            f"module {__name__!r} "
            f"has no attribute {name!r}"
        )

    module_name, attribute_name = target

    module = import_module(
        module_name,
        __name__,
    )

    value = getattr(
        module,
        attribute_name,
    )

    globals()[name] = value

    return value


def __dir__():
    return sorted(
        set(
            globals()
        )
        | set(
            __all__
        )
    )
