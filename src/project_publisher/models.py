"""Data models returned by the audit engine."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

FindingStatus = Literal["pass", "warning", "error", "info"]


@dataclass(frozen=True)
class Finding:
    """One transparent, independently verifiable protocol check."""

    identifier: str
    title: str
    status: FindingStatus
    message: str
    points: int = 0
    max_points: int = 0

    def to_dict(self) -> dict[str, object]:
        return {
            "id": self.identifier,
            "title": self.title,
            "status": self.status,
            "message": self.message,
            "points": self.points,
            "max_points": self.max_points,
        }


@dataclass
class AuditReport:
    """Aggregate result for a repository publication audit."""

    target: Path
    findings: list[Finding] = field(default_factory=list)

    @property
    def score(self) -> int:
        maximum = sum(finding.max_points for finding in self.findings)
        earned = sum(finding.points for finding in self.findings)
        return round((earned / maximum) * 100) if maximum else 0

    @property
    def errors(self) -> list[Finding]:
        return [finding for finding in self.findings if finding.status == "error"]

    @property
    def warnings(self) -> list[Finding]:
        return [finding for finding in self.findings if finding.status == "warning"]

    @property
    def ready(self) -> bool:
        return not self.errors and self.score >= 80

    def to_dict(self) -> dict[str, object]:
        return {
            "target": str(self.target),
            "score": self.score,
            "ready": self.ready,
            "summary": {
                "errors": len(self.errors),
                "warnings": len(self.warnings),
                "findings": len(self.findings),
            },
            "findings": [finding.to_dict() for finding in self.findings],
        }
