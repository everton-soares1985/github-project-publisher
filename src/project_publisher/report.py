"""Terminal and JSON presentation for audit results."""

from __future__ import annotations

import json
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from project_publisher.models import AuditReport

STATUS_LABELS = {
    "pass": "[green]OK[/green]",
    "warning": "[yellow]WARNING[/yellow]",
    "error": "[red]ERROR[/red]",
    "info": "[cyan]INFO[/cyan]",
}


def render_terminal_report(report: AuditReport, console: Console) -> None:
    """Render a concise human-readable report."""

    readiness = "READY" if report.ready else "NOT READY"
    color = "green" if report.ready else "yellow" if not report.errors else "red"
    console.print(
        Panel.fit(
            f"[{color}]{readiness}[/{color}] for publication\n"
            f"Score: [bold]{report.score}%[/bold] | "
            f"Errors: {len(report.errors)} | Warnings: {len(report.warnings)}\n"
            f"Target: {report.target}",
            title="GitHub Project Publisher",
        )
    )
    table = Table(show_header=True, header_style="bold")
    table.add_column("Status", no_wrap=True)
    table.add_column("Check")
    table.add_column("Result")
    table.add_column("Points", justify="right", no_wrap=True)
    for finding in report.findings:
        table.add_row(
            STATUS_LABELS[finding.status],
            finding.title,
            finding.message,
            f"{finding.points}/{finding.max_points}" if finding.max_points else "—",
        )
    console.print(table)


def write_json_report(report: AuditReport, destination: Path) -> Path:
    """Write a JSON report only when explicitly requested by the caller."""

    resolved_destination = destination.resolve()
    resolved_destination.parent.mkdir(parents=True, exist_ok=True)
    resolved_destination.write_text(
        json.dumps(report.to_dict(), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return resolved_destination
