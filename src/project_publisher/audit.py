"""Public service for auditing a repository."""

from pathlib import Path

from project_publisher.checks import collect_findings
from project_publisher.models import AuditReport


def audit_project(target: Path) -> AuditReport:
    """Inspect ``target`` without changing its files, Git state, or configuration."""

    resolved_target = target.resolve()
    return AuditReport(target=resolved_target, findings=collect_findings(resolved_target))
