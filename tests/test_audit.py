"""Tests for the read-only publication audit."""

from __future__ import annotations

import subprocess
from pathlib import Path

from project_publisher.audit import audit_project


def _run_git(repository: Path, *arguments: str) -> None:
    subprocess.run(
        ["git", "-C", str(repository), *arguments],
        check=True,
        capture_output=True,
        text=True,
    )


def _create_ready_repository(tmp_path: Path) -> Path:
    repository = tmp_path / "ready-project"
    repository.mkdir()
    (repository / "README.md").write_text("# Ready Project\n\n" + "Useful project context. " * 12)
    (repository / "LICENSE").write_text("MIT License\n")
    (repository / "CHANGELOG.md").write_text("# Changelog\n")
    (repository / "CONTRIBUTING.md").write_text("# Contributing\n")
    (repository / "SECURITY.md").write_text("# Security\n")
    (repository / "AGENTS.md").write_text("# Agent instructions\n")
    (repository / ".gitignore").write_text(".env\n.venv/\n")
    (repository / "docs").mkdir()
    (repository / "docs" / "overview.md").write_text("# Documentation\n")
    (repository / "screenshots").mkdir()
    (repository / "screenshots" / ".gitkeep").write_text("")
    (repository / "tests").mkdir()
    (repository / "tests" / "test_example.py").write_text("def test_example():\n    assert True\n")
    _run_git(repository, "init", "-b", "main")
    _run_git(repository, "config", "user.name", "Test User")
    _run_git(repository, "config", "user.email", "test@example.com")
    _run_git(repository, "add", ".")
    _run_git(repository, "commit", "-m", "Initial commit")
    return repository


def test_ready_repository_scores_one_hundred_without_changes(tmp_path: Path) -> None:
    repository = _create_ready_repository(tmp_path)
    before_status = subprocess.run(
        ["git", "-C", str(repository), "status", "--porcelain"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout

    report = audit_project(repository)

    after_status = subprocess.run(
        ["git", "-C", str(repository), "status", "--porcelain"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    assert report.ready
    assert report.score == 100
    assert before_status == after_status == ""


def test_dotenv_file_blocks_publication(tmp_path: Path) -> None:
    repository = _create_ready_repository(tmp_path)
    (repository / ".env").write_text("API_KEY=not-a-real-secret\n")

    report = audit_project(repository)

    secret_finding = next(
        finding for finding in report.findings if finding.identifier == "secret-exposure"
    )
    assert not report.ready
    assert secret_finding.status == "error"
    assert ".env" in secret_finding.message


def test_env_example_is_allowed(tmp_path: Path) -> None:
    repository = _create_ready_repository(tmp_path)
    (repository / ".env.example").write_text("API_KEY=replace-me\n")

    report = audit_project(repository)

    secret_finding = next(
        finding for finding in report.findings if finding.identifier == "secret-exposure"
    )
    assert secret_finding.status == "pass"
