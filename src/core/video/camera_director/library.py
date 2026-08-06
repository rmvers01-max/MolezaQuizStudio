from __future__ import annotations

from .models import CameraMove


class AAACameraMoveLibrary:
    def discovery_push(self) -> CameraMove:
        return CameraMove(
            code="discovery_push_01",
            move_type="push",
            zoom_from=1.00,
            zoom_to=1.05,
            pan_x=0.0,
            pan_y=-0.01,
            rotation=0.0,
            shake=0.0,
            focus_strength=0.48,
            depth_strength=0.20,
            duration=3.8,
            easing="ease_in_out_cubic",
        )

    def suspense_focus(self) -> CameraMove:
        return CameraMove(
            code="suspense_focus_01",
            move_type="slow_push",
            zoom_from=1.00,
            zoom_to=1.09,
            pan_x=0.0,
            pan_y=0.0,
            rotation=0.0,
            shake=0.01,
            focus_strength=0.78,
            depth_strength=0.34,
            duration=4.2,
            easing="ease_in_out_cubic",
        )

    def competition_push(self) -> CameraMove:
        return CameraMove(
            code="competition_push_01",
            move_type="dynamic_push",
            zoom_from=1.00,
            zoom_to=1.12,
            pan_x=0.02,
            pan_y=0.0,
            rotation=0.0,
            shake=0.025,
            focus_strength=0.62,
            depth_strength=0.22,
            duration=3.0,
            easing="ease_out_cubic",
        )

    def hero_reveal(self) -> CameraMove:
        return CameraMove(
            code="hero_reveal_01",
            move_type="hero_zoom",
            zoom_from=0.98,
            zoom_to=1.14,
            pan_x=0.0,
            pan_y=-0.02,
            rotation=0.0,
            shake=0.018,
            focus_strength=0.90,
            depth_strength=0.28,
            duration=2.4,
            easing="ease_out_back",
        )

    def choice_balance(self) -> CameraMove:
        return CameraMove(
            code="choice_safe_static_02",
            move_type="static_safe",
            zoom_from=1.00,
            zoom_to=1.00,
            pan_x=0.0,
            pan_y=0.0,
            rotation=0.0,
            shake=0.0,
            focus_strength=0.35,
            depth_strength=0.0,
            duration=4.0,
            easing="linear",
        )

    def calm_drift(self) -> CameraMove:
        return CameraMove(
            code="calm_drift_01",
            move_type="drift",
            zoom_from=1.00,
            zoom_to=1.02,
            pan_x=-0.01,
            pan_y=0.01,
            rotation=0.0,
            shake=0.0,
            focus_strength=0.35,
            depth_strength=0.12,
            duration=4.4,
            easing="ease_in_out_cubic",
        )

    def static_safe(self) -> CameraMove:
        return CameraMove(
            code="static_safe_01",
            move_type="static",
            zoom_from=1.00,
            zoom_to=1.00,
            pan_x=0.0,
            pan_y=0.0,
            rotation=0.0,
            shake=0.0,
            focus_strength=0.20,
            depth_strength=0.0,
            duration=4.0,
            easing="linear",
        )
