from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

@dataclass(frozen=True, slots=True)
class ContentProfile:
    category: str
    confidence: float
    signals: tuple[str, ...]
    visual_density: str
    theme_family: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self):
        return {
            "category": self.category,
            "confidence": self.confidence,
            "signals": list(self.signals),
            "visual_density": self.visual_density,
            "theme_family": self.theme_family,
            "metadata": dict(self.metadata),
        }

@dataclass(frozen=True, slots=True)
class AudienceRisk:
    start_question: int
    end_question: int
    score: float
    risk_type: str
    explanation: str
    proposed_action: dict[str, Any]

    def to_dict(self):
        return {
            "start_question": self.start_question,
            "end_question": self.end_question,
            "score": self.score,
            "risk_type": self.risk_type,
            "explanation": self.explanation,
            "proposed_action": dict(self.proposed_action),
        }

@dataclass(frozen=True, slots=True)
class IntelligentProductionPlan:
    title: str
    quiz_type: str
    total_questions: int
    content_profile: ContentProfile
    production_mode: str
    pacing_strategy: str
    emotional_curve: tuple[str, ...]
    retention_strategy: dict[str, Any]
    mascot_strategy: dict[str, Any]
    audio_strategy: dict[str, Any]
    visual_strategy: dict[str, Any]
    audience_risks: tuple[AudienceRisk, ...]
    publish_readiness_score: int
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self):
        return {
            "title": self.title,
            "quiz_type": self.quiz_type,
            "total_questions": self.total_questions,
            "content_profile": self.content_profile.to_dict(),
            "production_mode": self.production_mode,
            "pacing_strategy": self.pacing_strategy,
            "emotional_curve": list(self.emotional_curve),
            "retention_strategy": dict(self.retention_strategy),
            "mascot_strategy": dict(self.mascot_strategy),
            "audio_strategy": dict(self.audio_strategy),
            "visual_strategy": dict(self.visual_strategy),
            "audience_risks": [r.to_dict() for r in self.audience_risks],
            "publish_readiness_score": self.publish_readiness_score,
            "metadata": dict(self.metadata),
        }
