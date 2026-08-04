from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

@dataclass(frozen=True, slots=True)
class ChannelDNA:
    channel_code: str
    channel_name: str
    personality: tuple[str, ...]
    accent_color: tuple[int,int,int]
    text_color: tuple[int,int,int]
    maximum_motion: float
    maximum_vignette: float
    maximum_particles: float
    metadata: dict[str,Any]=field(default_factory=dict)
    def to_dict(self):
        return {
            "channel_code":self.channel_code,"channel_name":self.channel_name,
            "personality":list(self.personality),"accent_color":list(self.accent_color),
            "text_color":list(self.text_color),"maximum_motion":self.maximum_motion,
            "maximum_vignette":self.maximum_vignette,
            "maximum_particles":self.maximum_particles,"metadata":dict(self.metadata),
        }

@dataclass(frozen=True, slots=True)
class IdentityPlan:
    channel_dna: ChannelDNA
    category: str
    corrected_theme_pack: dict[str,Any]
    rules: dict[str,Any]
    score: int
    findings: tuple[str,...]=()
    metadata: dict[str,Any]=field(default_factory=dict)
    def to_dict(self):
        return {
            "channel_dna":self.channel_dna.to_dict(),"category":self.category,
            "corrected_theme_pack":dict(self.corrected_theme_pack),
            "rules":dict(self.rules),"score":self.score,
            "findings":list(self.findings),"metadata":dict(self.metadata),
        }
