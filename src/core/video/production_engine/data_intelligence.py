from __future__ import annotations
from collections import Counter
from typing import Any
from .models import ContentProfile

class DataIntelligenceEngine:
    SIGNALS = {
        "flags_geography": ("bandeira","país","pais","capital","continente","brasil","europa","🇧🇷","🇺🇸","🇫🇷"),
        "animals": ("animal","cachorro","gato","leão","tigre","elefante","🐶","🐱"),
        "food": ("comida","doce","pizza","hambúrguer","chocolate","sorvete","🍕","🍔"),
        "sports": ("futebol","esporte","time","jogador","gol","⚽","🏀"),
        "characters": ("personagem","filme","desenho","princesa","herói","pokemon","pokémon"),
        "preference": ("você prefere","o que você prefere","escolha","qual você escolheria"),
        "general_knowledge": ("qual","quem","onde","quando","adivinhe","descubra"),
    }
    THEMES = {
        "flags_geography":"geography","animals":"nature","food":"food_fun",
        "sports":"sports_energy","characters":"characters_pop",
        "preference":"choice_playful","general_knowledge":"knowledge_default",
    }

    def analyze(self, *, title: str, quiz_type: str, questions: list[dict[str, Any]]) -> ContentProfile:
        parts = [str(title)]
        image_count = alt_count = text_total = 0
        for q in questions:
            text = str(q.get("pergunta",""))
            parts.append(text); text_total += len(text)
            alts = q.get("alternativas", [])
            alt_count += len(alts)
            parts.extend(str(v) for v in alts)
            if q.get("imagem") or q.get("imagem_a") or q.get("imagem_b"):
                image_count += 1

        corpus = " ".join(parts).lower()
        scores, matched = Counter(), []
        for category, signals in self.SIGNALS.items():
            for signal in signals:
                count = corpus.count(signal)
                if count:
                    scores[category] += count
                    matched.append(signal)
        if quiz_type == "preferencia":
            scores["preference"] += 8

        category = scores.most_common(1)[0][0] if scores else "general_knowledge"
        confidence = round(min(max(scores.get(category,0)/max(sum(scores.values()),1),.35),.98),3)
        total = max(len(questions),1)
        density_value = (text_total/total)/45 + (alt_count/total)/4 + image_count/total
        density = "high" if density_value >= 2.4 else "medium" if density_value >= 1.45 else "low"

        return ContentProfile(
            category=category,
            confidence=confidence,
            signals=tuple(sorted(set(matched))[:20]),
            visual_density=density,
            theme_family=self.THEMES.get(category,"knowledge_default"),
            metadata={
                "image_ratio": round(image_count/total,3),
                "average_alternatives": round(alt_count/total,3),
                "average_question_text_length": round(text_total/total,3),
                "engine_version":"1.0",
            },
        )
