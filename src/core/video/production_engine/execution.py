from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True, slots=True)
class QuestionRuntimeDirective:
    question_number: int
    force_pattern_break: bool = False
    motion_boost: float = 0.0
    mascot_boost: float = 0.0
    entry_duration_delta: float = 0.0
    thinking_duration_delta: float = 0.0
    reveal_duration_delta: float = 0.0
    audio_whoosh: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self):
        return {
            "question_number": self.question_number,
            "force_pattern_break": self.force_pattern_break,
            "motion_boost": self.motion_boost,
            "mascot_boost": self.mascot_boost,
            "entry_duration_delta": self.entry_duration_delta,
            "thinking_duration_delta": self.thinking_duration_delta,
            "reveal_duration_delta": self.reveal_duration_delta,
            "audio_whoosh": self.audio_whoosh,
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True, slots=True)
class IPEExecutionPlan:
    enabled: bool
    production_mode: str
    global_adjustments: dict[str, Any]
    question_directives: tuple[QuestionRuntimeDirective, ...]
    safety_limits: dict[str, Any]
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self):
        return {
            "enabled": self.enabled,
            "production_mode": self.production_mode,
            "global_adjustments": dict(self.global_adjustments),
            "question_directives": [x.to_dict() for x in self.question_directives],
            "safety_limits": dict(self.safety_limits),
            "metadata": dict(self.metadata),
        }

    def question(self, number: int):
        for item in self.question_directives:
            if item.question_number == int(number):
                return item
        return None


class IPEExecutionLayer:
    """Converte recomendações do IPE em ajustes pequenos e seguros."""

    def build(self, intelligent_plan: dict[str, Any]) -> IPEExecutionPlan:
        mode = str(intelligent_plan.get("production_mode", "balanced_family_quiz"))
        risks = list(intelligent_plan.get("audience_risks", []))

        global_adjustments = {
            "pattern_break_interval_delta": -1 if mode == "long_form_retention" else 0,
            "pattern_break_intensity_delta": 0.06 if mode in {"compact_high_energy","visual_guess_challenge"} else 0.0,
            "mascot_intensity_multiplier": 1.06 if mode in {"playful_choice_show","compact_high_energy"} else 1.0,
            "motion_intensity_multiplier": 1.05 if mode == "compact_high_energy" else 1.0,
            "audio_sync_enabled": True,
        }

        directives: dict[int, dict[str, Any]] = {}
        for risk in risks:
            start=max(int(risk.get("start_question",1)),1)
            end=max(int(risk.get("end_question",start)),start)
            kind=str(risk.get("risk_type",""))
            action=dict(risk.get("proposed_action",{}))
            target=end
            item=directives.setdefault(target, {
                "force_pattern_break":False,"motion_boost":0.0,"mascot_boost":0.0,
                "entry_duration_delta":0.0,"thinking_duration_delta":0.0,
                "reveal_duration_delta":0.0,"audio_whoosh":False,"risk_types":[],
            })
            item["risk_types"].append(kind)
            if kind == "visual_repetition":
                item["force_pattern_break"] = True
                item["motion_boost"] = max(item["motion_boost"], .10)
                item["mascot_boost"] = max(item["mascot_boost"], .10)
                item["audio_whoosh"] = True
            elif kind == "early_cognitive_load":
                item["entry_duration_delta"] = min(max(float(action.get("entry_duration_delta",.15)),0),.25)
                item["thinking_duration_delta"] = .5
            elif kind in {"low_motion_point","low_motion_block"}:
                item["motion_boost"] = min(max(float(action.get("motion_boost",.08)),0),.15)
                item["audio_whoosh"] = True

        question_directives=tuple(
            QuestionRuntimeDirective(
                question_number=n,
                force_pattern_break=v["force_pattern_break"],
                motion_boost=round(min(v["motion_boost"],.18),3),
                mascot_boost=round(min(v["mascot_boost"],.18),3),
                entry_duration_delta=round(min(v["entry_duration_delta"],.25),3),
                thinking_duration_delta=round(min(v["thinking_duration_delta"],1.0),3),
                reveal_duration_delta=round(min(v["reveal_duration_delta"],.35),3),
                audio_whoosh=v["audio_whoosh"],
                metadata={"risk_types":tuple(v["risk_types"])},
            ) for n,v in sorted(directives.items())
        )

        return IPEExecutionPlan(
            enabled=True,
            production_mode=mode,
            global_adjustments=global_adjustments,
            question_directives=question_directives,
            safety_limits={
                "maximum_motion_boost":.18,
                "maximum_mascot_boost":.18,
                "maximum_entry_delta":.25,
                "maximum_thinking_delta":1.0,
                "minimum_pattern_break_interval":2,
            },
            metadata={"execution_version":"1.0","source":"intelligent_production_plan"},
        )

    def save(self, plan: IPEExecutionPlan, path):
        path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(json.dumps(plan.to_dict(),ensure_ascii=False,indent=2),encoding='utf-8')
        return path
