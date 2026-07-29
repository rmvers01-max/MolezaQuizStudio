from .easing import (
    clamp,
    ease_in_out_sine,
    ease_out_back,
    ease_out_cubic,
    pulse,
)
from .scene_clips import SceneClipFactory
from .layered_scene import LayeredSceneAnimator

__all__ = [
    "CameraMotionFactory",
    "CardMotionFactory",
    "ProfessionalSceneEngine",
    "MascotAnimationFactory",
    "TransitionFactory",
    "AnimatedBackgroundFactory",
    "SceneClipFactory",
    "LayeredSceneAnimator",
    "clamp",
    "ease_in_out_sine",
    "ease_out_back",
    "ease_out_cubic",
    "pulse",
]

from .transitions import TransitionFactory
from .animated_background import AnimatedBackgroundFactory

from .mascot_animation import MascotAnimationFactory

from .camera_motion import CameraMotionFactory
from .card_motion import CardMotionFactory
from .scene_engine import ProfessionalSceneEngine
