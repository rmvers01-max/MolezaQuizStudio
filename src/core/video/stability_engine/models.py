from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class StabilityFinding:
    code: str
    severity: str
    message: str
    component: str
    details: dict[str, Any] = field(
        default_factory=dict
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "code": self.code,
            "severity": self.severity,
            "message": self.message,
            "component": self.component,
            "details": dict(self.details),
        }


@dataclass(frozen=True, slots=True)
class StabilityReport:
    healthy: bool
    score: int
    findings: tuple[StabilityFinding, ...]
    checks: dict[str, bool]
    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "healthy": self.healthy,
            "score": self.score,
            "findings": [
                finding.to_dict()
                for finding in self.findings
            ],
            "checks": dict(self.checks),
            "metadata": dict(self.metadata),
        }
