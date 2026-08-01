from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class VideoMetrics:
    video_id: str
    title: str
    quiz_type: str
    theme_pack: str
    published_at: str | None = None
    impressions: int | None = None
    views: int | None = None
    watch_time_hours: float | None = None
    average_view_duration_seconds: float | None = None
    average_percentage_viewed: float | None = None
    ctr_percent: float | None = None
    likes: int | None = None
    comments: int | None = None
    subscribers_gained: int | None = None
    first_30_seconds_retention: float | None = None
    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "video_id": self.video_id,
            "title": self.title,
            "quiz_type": self.quiz_type,
            "theme_pack": self.theme_pack,
            "published_at": self.published_at,
            "impressions": self.impressions,
            "views": self.views,
            "watch_time_hours": self.watch_time_hours,
            "average_view_duration_seconds": (
                self.average_view_duration_seconds
            ),
            "average_percentage_viewed": (
                self.average_percentage_viewed
            ),
            "ctr_percent": self.ctr_percent,
            "likes": self.likes,
            "comments": self.comments,
            "subscribers_gained": (
                self.subscribers_gained
            ),
            "first_30_seconds_retention": (
                self.first_30_seconds_retention
            ),
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True, slots=True)
class ProductionFingerprint:
    production_id: str
    title: str
    quiz_type: str
    total_questions: int
    theme_pack: str
    energy_level: float
    pacing_mode: str
    opening_duration: float
    reveal_duration: float
    pattern_break_interval: int
    mascot_intensity: float
    outro_duration: float
    story_chapters: tuple[str, ...]
    created_at: str
    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "production_id": self.production_id,
            "title": self.title,
            "quiz_type": self.quiz_type,
            "total_questions": self.total_questions,
            "theme_pack": self.theme_pack,
            "energy_level": self.energy_level,
            "pacing_mode": self.pacing_mode,
            "opening_duration": self.opening_duration,
            "reveal_duration": self.reveal_duration,
            "pattern_break_interval": (
                self.pattern_break_interval
            ),
            "mascot_intensity": self.mascot_intensity,
            "outro_duration": self.outro_duration,
            "story_chapters": list(
                self.story_chapters
            ),
            "created_at": self.created_at,
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True, slots=True)
class IntelligenceRecommendation:
    code: str
    priority: str
    title: str
    explanation: str
    proposed_change: dict[str, Any]
    evidence: dict[str, Any] = field(
        default_factory=dict
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "code": self.code,
            "priority": self.priority,
            "title": self.title,
            "explanation": self.explanation,
            "proposed_change": dict(
                self.proposed_change
            ),
            "evidence": dict(self.evidence),
        }
