"""CLI behavior tests."""

from __future__ import annotations

import subprocess
from pathlib import Path

from typer.testing import CliRunner

from project_publisher.cli import app


def _create_repository(tmp_path: Path) -> Path:
    repository = tmp_path / "project"
    repository.mkdir()
    (repository / "README.md").write_text("# Ready Project\n\n" + "Useful project context. " * 12)
    for document in ("LICENSE", "CHANGELOG.md", "CONTRIBUTING.md", "SECURITY.md", "AGENTS.md"):
        (repository / document).write_text(f"# {document}\n")
    (repository / ".gitignore").write_text(".env\n")
    (repository / "docs").mkdir()
    (repository / "screenshots").mkdir()
    (repository / "tests").mkdir()
    (repository / "tests" / "test_example.py").write_text("def test_example():\n    assert True\n")
    for arguments in (
        ("init", "-b", "main"),
        ("config", "user.name", "Test User"),
        ("config", "user.email", "test@example.com"),
        ("add", "."),
        ("commit", "-m", "Initial commit"),
    ):
        subprocess.run(
            ["git", "-C", str(repository), *arguments],
            check=True,
            capture_output=True,
            text=True,
        )
    return repository


def test_check_returns_zero_for_ready_project(tmp_path: Path) -> None:
    result = CliRunner().invoke(app, ["check", str(_create_repository(tmp_path))])

    assert result.exit_code == 0
    assert "PRONTO" in result.output


def test_check_returns_one_for_project_with_secret(tmp_path: Path) -> None:
    repository = _create_repository(tmp_path)
    (repository / ".env").write_text("TOKEN=not-a-real-secret\n")

    result = CliRunner().invoke(app, ["check", str(repository)])

    assert result.exit_code == 1
    assert "ERRO" in result.output


def test_audit_writes_json_only_when_requested(tmp_path: Path) -> None:
    repository = _create_repository(tmp_path)
    destination = tmp_path / "reports" / "audit.json"

    result = CliRunner().invoke(
        app,
        ["audit", str(repository), "--json-output", str(destination)],
    )

    assert result.exit_code == 0
    assert destination.is_file()
    assert '"ready": true' in destination.read_text(encoding="utf-8")
