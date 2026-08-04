from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

@dataclass(frozen=True, slots=True)
class EndingDirection:
    category: str
    quiz_type: str
    duration: float
    headline: str
    supporting_text: str
    primary_cta: str
    secondary_cta: str
    mascot_sequence: tuple[str, ...]
    celebration_style: str
    transition_style: str
    show_score_prompt: bool
    show_comment_prompt: bool
    show_next_video_slot: bool
    show_subscribe_slot: bool
    curiosity_closer: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            'category': self.category,
            'quiz_type': self.quiz_type,
            'duration': self.duration,
            'headline': self.headline,
            'supporting_text': self.supporting_text,
            'primary_cta': self.primary_cta,
            'secondary_cta': self.secondary_cta,
            'mascot_sequence': list(self.mascot_sequence),
            'celebration_style': self.celebration_style,
            'transition_style': self.transition_style,
            'show_score_prompt': self.show_score_prompt,
            'show_comment_prompt': self.show_comment_prompt,
            'show_next_video_slot': self.show_next_video_slot,
            'show_subscribe_slot': self.show_subscribe_slot,
            'curiosity_closer': self.curiosity_closer,
            'metadata': dict(self.metadata),
        }
