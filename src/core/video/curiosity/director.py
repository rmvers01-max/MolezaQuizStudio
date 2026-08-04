from __future__ import annotations
from pathlib import Path
from typing import Any
from .models import CuriosityItem, CuriosityPlan

class CuriosityExperienceDirector:
    """Cria curiosidades somente a partir de conteúdo fornecido no projeto.

    O motor não inventa fatos. Quando não há curiosidade cadastrada, a tela
    factual é omitida e o fluxo segue para a próxima pergunta.
    """

    CATEGORY_STYLE = {
        "flags_geography": "geography_glow",
        "animals": "nature_discovery",
        "food": "food_pop",
        "sports": "energy_fact",
        "characters": "mystery_card",
        "preference": "dual_choice_fact",
        "general_knowledge": "knowledge_card",
    }

    def create_plan(self, *, question: dict[str, Any], quiz_type: str, category: str, default_duration: float = 3.2) -> CuriosityPlan:
        items=[]
        alternatives=[str(v).strip() for v in question.get("alternativas", [])]

        if quiz_type == "preferencia":
            pairs = [
                ("curiosidade_a", "imagem_curiosidade_a", alternatives[0] if len(alternatives)>0 else "Opção A"),
                ("curiosidade_b", "imagem_curiosidade_b", alternatives[1] if len(alternatives)>1 else "Opção B"),
            ]
            for key, image_key, subject in pairs:
                text=str(question.get(key, "")).strip()
                if text:
                    items.append(CuriosityItem(
                        title="CURIOSIDADE!",
                        text=text,
                        subject=subject,
                        image_path=self._path(question.get(image_key)),
                        icon="💡",
                        metadata={"field": key, "choice_side": "a" if key.endswith("_a") else "b"},
                    ))
            general=str(question.get("curiosidade", "")).strip()
            if general and not items:
                items.append(CuriosityItem(
                    title="CURIOSIDADE!", text=general,
                    subject="Sobre as escolhas",
                    image_path=self._path(question.get("imagem_curiosidade")),
                    icon="💡", metadata={"field":"curiosidade"},
                ))
        else:
            text=str(question.get("curiosidade", question.get("explicacao", ""))).strip()
            if text:
                items.append(CuriosityItem(
                    title="VOCÊ SABIA?",
                    text=text,
                    subject=str(question.get("resposta_texto", question.get("resposta", ""))).strip(),
                    image_path=self._path(question.get("imagem_curiosidade", question.get("imagem"))),
                    icon="💡",
                    metadata={"field":"curiosidade_or_explicacao"},
                ))

        duration=max(float(question.get("duracao_curiosidade", default_duration)), 1.8) if items else 0.0
        return CuriosityPlan(
            enabled=bool(items), quiz_type=quiz_type, category=category,
            items=tuple(items), duration=duration,
            transition_text="PREPARE-SE PARA A PRÓXIMA PERGUNTA!",
            mascot_pose="point_left" if items else "happy",
            visual_style=self.CATEGORY_STYLE.get(category, "knowledge_card"),
            metadata={"director_version":"1.0", "factual_content_source":"project_fields_only"},
        )

    def _path(self, value):
        if value in (None, ""): return None
        return str(Path(value))
