from __future__ import annotations

from .models import ChoiceVisualProfile


class AAAChoiceVisualDirector:
    """Escolhe uma variação vibrante sem alterar a lógica de preferência."""

    PALETTES = (
        ((255, 74, 122), (65, 145, 255), (255, 218, 70)),
        ((255, 102, 76), (115, 79, 225), (255, 226, 72)),
        ((233, 77, 168), (47, 172, 214), (255, 214, 65)),
        ((248, 91, 76), (67, 179, 137), (255, 224, 82)),
    )

    def choose(
        self,
        *,
        question_number: int,
        total_questions: int,
        has_images: bool,
        curiosity_selected: bool,
    ) -> ChoiceVisualProfile:
        index = (max(int(question_number), 1) - 1) % len(self.PALETTES)
        color_a, color_b, accent = self.PALETTES[index]

        final_zone = (
            total_questions > 0
            and question_number >= max(total_questions - 2, 1)
        )

        return ChoiceVisualProfile(
            code=f"choice_v2_{index + 1}",
            color_a=color_a,
            color_b=color_b,
            accent=accent,
            card_glow=0.78 if has_images else 0.62,
            image_scale=1.10 if has_images else 1.0,
            or_scale=1.12 if final_zone else 1.0,
            countdown_energy=0.92 if final_zone else 0.78,
            background_mode=(
                "celebration_gradient"
                if final_zone
                else "dual_neon_gradient"
            ),
            transition_style=(
                "curiosity_bridge"
                if curiosity_selected
                else "choice_flash"
            ),
            metadata={
                "renderer_version": "2.0",
                "question_number": question_number,
                "curiosity_selected": curiosity_selected,
                "no_correct_answer": True,
            },
        )
