"""Read-only filesystem and Git inspection helpers."""

from __future__ import annotations

import os
import subprocess
from collections.abc import Iterator
from pathlib import Path

from project_publisher.configuration import EXCLUDED_DIRECTORY_NAMES


def run_git(target: Path, *arguments: str) -> str | None:
    """Run a read-only Git command and return stripped stdout when successful."""

    completed = subprocess.run(
        ["git", "-C", str(target), *arguments],
        capture_output=True,
        check=False,
        encoding="utf-8",
        errors="replace",
        text=True,
    )
    if completed.returncode != 0:
        return None
    return completed.stdout.strip()


def is_git_repository(target: Path) -> bool:
    return run_git(target, "rev-parse", "--is-inside-work-tree") == "true"


def current_branch(target: Path) -> str | None:
    branch = run_git(target, "branch", "--show-current")
    return branch or None


def worktree_changes(target: Path) -> list[str] | None:
    output = run_git(target, "status", "--porcelain")
    if output is None:
        return None
    return output.splitlines() if output else []


def is_ignored_by_git(target: Path, path: Path) -> bool:
    """Return whether a path is already excluded by the repository's Git rules."""

    relative_path = path.relative_to(target)
    completed = subprocess.run(
        ["git", "-C", str(target), "check-ignore", "-q", "--", str(relative_path)],
        capture_output=True,
        check=False,
        encoding="utf-8",
        errors="replace",
        text=True,
    )
    return completed.returncode == 0


def iter_project_files(target: Path) -> Iterator[Path]:
    """Yield relevant project files without descending into generated directories."""

    for directory, directory_names, file_names in os.walk(target):
        directory_names[:] = [
            name for name in directory_names if name not in EXCLUDED_DIRECTORY_NAMES
        ]
        root = Path(directory)
        for file_name in file_names:
            yield root / file_name


def find_noise_directories(target: Path) -> list[Path]:
    """Find generated directories while avoiding descent into them."""

    found: list[Path] = []
    for directory, directory_names, _ in os.walk(target):
        root = Path(directory)
        for name in list(directory_names):
            if name in EXCLUDED_DIRECTORY_NAMES:
                if name in {"__pycache__", ".pytest_cache", ".ruff_cache", "node_modules"}:
                    found.append(root / name)
                directory_names.remove(name)
    return found
