from __future__ import annotations

from .models import ThemeExperienceProfile


class ThemeSpecificExperienceDirector:
    PRESETS = {
        "preference": {
            "engine_code": "choice_world_01",
            "background_mode": "dual_world",
            "motif_style": "choice_shapes",
            "transition_style": "split_flash",
            "countdown_style": "dual_ring",
            "density": 0.74,
            "speed": 0.90,
            "icons": ("★", "♥", "?", "OU"),
            "accent": (255, 215, 65),
            "secondary": (62, 145, 255),
        },
        "flags_geography": {
            "engine_code": "geography_world_01",
            "background_mode": "world_map",
            "motif_style": "map_compass",
            "transition_style": "flag_wipe",
            "countdown_style": "radial_compass",
            "density": 0.56,
            "speed": 0.48,
            "icons": ("✦", "⌖", "N", "S"),
            "accent": (255, 215, 65),
            "secondary": (65, 138, 225),
        },
        "animals": {
            "engine_code": "animal_nature_01",
            "background_mode": "forest_depth",
            "motif_style": "leaves_paws",
            "transition_style": "leaf_wipe",
            "countdown_style": "paw_ring",
            "density": 0.62,
            "speed": 0.52,
            "icons": ("●", "❧", "✦", "☘"),
            "accent": (255, 224, 90),
            "secondary": (62, 172, 118),
        },
        "food": {
            "engine_code": "food_fun_01",
            "background_mode": "kitchen_pop",
            "motif_style": "food_shapes",
            "transition_style": "color_pop",
            "countdown_style": "plate_ring",
            "density": 0.68,
            "speed": 0.70,
            "icons": ("●", "✦", "♡", "○"),
            "accent": (255, 220, 78),
            "secondary": (244, 102, 86),
        },
        "sports": {
            "engine_code": "sports_arena_01",
            "background_mode": "arena_lines",
            "motif_style": "field_score",
            "transition_style": "speed_wipe",
            "countdown_style": "scoreboard_ring",
            "density": 0.58,
            "speed": 0.96,
            "icons": ("◇", "✦", "GO", "★"),
            "accent": (255, 224, 68),
            "secondary": (55, 150, 230),
        },
        "characters": {
            "engine_code": "character_mystery_01",
            "background_mode": "mystery_stage",
            "motif_style": "stars_silhouettes",
            "transition_style": "mystery_flash",
            "countdown_style": "mystery_ring",
            "density": 0.60,
            "speed": 0.55,
            "icons": ("★", "?", "✦", "◆"),
            "accent": (255, 205, 86),
            "secondary": (158, 80, 218),
        },
        "general_knowledge": {
            "engine_code": "knowledge_lab_01",
            "background_mode": "knowledge_lab",
            "motif_style": "ideas_shapes",
            "transition_style": "light_wipe",
            "countdown_style": "neon_ring",
            "density": 0.50,
            "speed": 0.58,
            "icons": ("?", "!", "✦", "A"),
            "accent": (255, 215, 65),
            "secondary": (101, 61, 185),
        },
    }

    def choose(
        self,
        *,
        category: str,
        question_number: int = 1,
        scene_kind: str = "question",
    ) -> ThemeExperienceProfile:
        normalized = (
            category
            if category in self.PRESETS
            else "general_knowledge"
        )

        preset = self.PRESETS[normalized]

        density = float(preset["density"])
        speed = float(preset["speed"])

        if scene_kind == "countdown":
            density *= 0.78
            speed *= 1.08
        elif scene_kind == "reveal":
            density *= 1.08
            speed *= 0.92

        return ThemeExperienceProfile(
            category=normalized,
            engine_code=preset["engine_code"],
            background_mode=preset["background_mode"],
            motif_style=preset["motif_style"],
            transition_style=preset["transition_style"],
            countdown_style=preset["countdown_style"],
            decorative_density=min(density, 0.82),
            motion_speed=min(speed, 1.0),
            icon_set=tuple(preset["icons"]),
            accent_color=tuple(preset["accent"]),
            secondary_color=tuple(preset["secondary"]),
            metadata={
                "theme_engine_version": "1.0",
                "question_number": int(question_number),
                "scene_kind": str(scene_kind),
            },
        )
