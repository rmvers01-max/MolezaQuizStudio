from __future__ import annotations

import unicodedata

from .models import UniversalThemePack


class UniversalThemePackRegistry:
    PACKS = (
        UniversalThemePack(
            code="geography_flags",
            name="Geografia e Bandeiras",
            keywords=(
                "bandeira",
                "bandeiras",
                "pais",
                "paises",
                "capital",
                "capitais",
                "geografia",
                "mundo",
                "continente",
                "europa",
                "america",
                "asia",
                "africa",
            ),
            background_top=(20, 75, 150),
            background_bottom=(10, 28, 78),
            panel_color=(235, 245, 255),
            primary_color=(35, 115, 220),
            secondary_color=(50, 180, 155),
            accent_color=(255, 215, 65),
            text_color=(20, 38, 72),
            particle_style="map_stars",
            camera_style="center_focus",
            reveal_style="gold_flash",
            mascot_style="curious",
            background_activity=0.48,
            glow_intensity=0.34,
            motion_intensity=0.42,
        ),
        UniversalThemePack(
            code="food_fun",
            name="Comidas Divertidas",
            keywords=(
                "comida",
                "comidas",
                "pizza",
                "hamburguer",
                "lanche",
                "fast food",
                "fruta",
                "frutas",
                "restaurante",
                "salgado",
            ),
            background_top=(235, 92, 70),
            background_bottom=(120, 40, 75),
            panel_color=(255, 247, 225),
            primary_color=(240, 95, 65),
            secondary_color=(255, 170, 65),
            accent_color=(255, 225, 75),
            text_color=(72, 35, 30),
            particle_style="food_sparkles",
            camera_style="playful",
            reveal_style="warm_pop",
            mascot_style="happy",
            background_activity=0.58,
            glow_intensity=0.40,
            motion_intensity=0.55,
        ),
        UniversalThemePack(
            code="candy_party",
            name="Festa de Doces",
            keywords=(
                "doce",
                "doces",
                "chocolate",
                "sorvete",
                "bolo",
                "bala",
                "sobremesa",
            ),
            background_top=(205, 70, 184),
            background_bottom=(75, 40, 145),
            panel_color=(255, 238, 250),
            primary_color=(255, 95, 155),
            secondary_color=(125, 110, 245),
            accent_color=(255, 225, 75),
            text_color=(70, 35, 105),
            particle_style="candy_sparkles",
            camera_style="playful",
            reveal_style="confetti_pop",
            mascot_style="celebrate",
            background_activity=0.64,
            glow_intensity=0.46,
            motion_intensity=0.60,
        ),
        UniversalThemePack(
            code="gift_surprise",
            name="Presentes e Surpresas",
            keywords=(
                "presente",
                "presentes",
                "surpresa",
                "surpresas",
                "caixa",
                "escolha seu presente",
            ),
            background_top=(120, 60, 190),
            background_bottom=(45, 30, 105),
            panel_color=(250, 240, 255),
            primary_color=(145, 75, 220),
            secondary_color=(255, 95, 140),
            accent_color=(255, 220, 70),
            text_color=(58, 32, 95),
            particle_style="ribbons",
            camera_style="mystery_push",
            reveal_style="gift_burst",
            mascot_style="curious",
            background_activity=0.62,
            glow_intensity=0.48,
            motion_intensity=0.58,
        ),
        UniversalThemePack(
            code="hero_arena",
            name="Arena de Heróis",
            keywords=(
                "heroi",
                "herois",
                "super-heroi",
                "super heroi",
                "poder",
                "vingadores",
                "marvel",
                "dc",
                "personagem",
            ),
            background_top=(35, 65, 165),
            background_bottom=(18, 20, 65),
            panel_color=(235, 242, 255),
            primary_color=(55, 105, 230),
            secondary_color=(235, 55, 80),
            accent_color=(255, 215, 55),
            text_color=(22, 35, 80),
            particle_style="energy",
            camera_style="dynamic",
            reveal_style="energy_flash",
            mascot_style="brave",
            background_activity=0.70,
            glow_intensity=0.60,
            motion_intensity=0.68,
        ),
        UniversalThemePack(
            code="princess_dream",
            name="Sonho de Princesas",
            keywords=(
                "princesa",
                "princesas",
                "castelo",
                "fada",
                "magia",
                "unicornio",
                "encanto",
            ),
            background_top=(185, 85, 178),
            background_bottom=(72, 42, 122),
            panel_color=(255, 240, 252),
            primary_color=(225, 105, 195),
            secondary_color=(155, 115, 245),
            accent_color=(255, 225, 105),
            text_color=(75, 38, 100),
            particle_style="stars",
            camera_style="elegant",
            reveal_style="magic_glow",
            mascot_style="gentle",
            background_activity=0.54,
            glow_intensity=0.52,
            motion_intensity=0.48,
        ),
        UniversalThemePack(
            code="jungle_animals",
            name="Selva e Animais",
            keywords=(
                "animal",
                "animais",
                "selva",
                "floresta",
                "natureza",
                "fazenda",
                "dinossauro",
                "oceano",
            ),
            background_top=(38, 120, 82),
            background_bottom=(18, 52, 50),
            panel_color=(238, 250, 230),
            primary_color=(75, 155, 85),
            secondary_color=(70, 145, 185),
            accent_color=(255, 215, 75),
            text_color=(30, 70, 45),
            particle_style="leaves",
            camera_style="gentle",
            reveal_style="nature_glow",
            mascot_style="curious",
            background_activity=0.46,
            glow_intensity=0.32,
            motion_intensity=0.42,
        ),
        UniversalThemePack(
            code="moleza_vibrant",
            name="Moleza Vibrante",
            keywords=(),
            background_top=(90, 55, 180),
            background_bottom=(35, 28, 92),
            panel_color=(245, 240, 255),
            primary_color=(115, 70, 205),
            secondary_color=(255, 95, 135),
            accent_color=(255, 215, 65),
            text_color=(55, 35, 95),
            particle_style="sparkles",
            camera_style="balanced",
            reveal_style="celebration",
            mascot_style="friendly",
            background_activity=0.55,
            glow_intensity=0.38,
            motion_intensity=0.50,
        ),
    )

    def select(
        self,
        title: str,
        quiz_type: str = "",
    ) -> UniversalThemePack:
        normalized = self._normalize(
            f"{title} {quiz_type}"
        )

        best = self.PACKS[-1]
        best_score = 0

        for pack in self.PACKS:
            score = sum(
                1
                for keyword in pack.keywords
                if self._normalize(keyword)
                in normalized
            )

            if score > best_score:
                best = pack
                best_score = score

        return best

    def get(
        self,
        code: str,
    ) -> UniversalThemePack:
        normalized = self._normalize(
            code
        )

        for pack in self.PACKS:
            if self._normalize(
                pack.code
            ) == normalized:
                return pack

        return self.PACKS[-1]

    def _normalize(
        self,
        value: str,
    ) -> str:
        decomposed = unicodedata.normalize(
            "NFKD",
            str(value).lower(),
        )

        return "".join(
            char
            for char in decomposed
            if not unicodedata.combining(
                char
            )
        )
