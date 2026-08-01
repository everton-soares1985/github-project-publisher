"""Command-line interface for the read-only publication protocol."""

from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console

from project_publisher.audit import audit_project
from project_publisher.report import render_terminal_report, write_json_report

app = typer.Typer(
    add_completion=False,
    no_args_is_help=True,
    help="Audit and validate a repository before publishing it on GitHub.",
)
console = Console()
TargetPath = Annotated[
    Path,
    typer.Argument(exists=True, file_okay=False, dir_okay=True, readable=True, resolve_path=True),
]
JsonOutput = Annotated[
    Path | None,
    typer.Option("--json-output", help="Optional location for a machine-readable report."),
]


@app.command()
def audit(path: TargetPath = Path("."), json_output: JsonOutput = None) -> None:
    """Inspect a repository and report issues without changing it."""

    report = audit_project(path)
    render_terminal_report(report, console)
    if json_output is not None:
        destination = write_json_report(report, json_output)
        console.print(f"JSON report written to: {destination}")


@app.command()
def check(path: TargetPath = Path("."), json_output: JsonOutput = None) -> None:
    """Run the publication gate; exit non-zero when the repository is not ready."""

    report = audit_project(path)
    render_terminal_report(report, console)
    if json_output is not None:
        destination = write_json_report(report, json_output)
        console.print(f"JSON report written to: {destination}")
    if not report.ready:
        raise typer.Exit(code=1)
