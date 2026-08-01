"""Publication-protocol checks. Every function here is intentionally read-only."""

from __future__ import annotations

from pathlib import Path

from project_publisher.configuration import (
    MAX_FILE_SIZE_BYTES,
    NOISE_FILE_NAMES,
    NOISE_SUFFIXES,
    PREFERRED_BRANCHES,
    README_MINIMUM_CHARACTERS,
    REQUIRED_DOCUMENTS,
    SECRET_CONTENT_PATTERNS,
    SENSITIVE_FILE_NAMES,
    SENSITIVE_FILE_SUFFIXES,
    TEXT_SUFFIXES,
    is_allowed_env_example,
)
from project_publisher.models import Finding
from project_publisher.project_scanner import (
    current_branch,
    find_noise_directories,
    is_ignored_by_git,
    is_git_repository,
    iter_project_files,
    worktree_changes,
)


def collect_findings(target: Path) -> list[Finding]:
    """Run the v0.1 protocol and return all findings, never stopping at first error."""

    findings: list[Finding] = []
    findings.extend(_git_findings(target))
    findings.extend(_documentation_findings(target))
    findings.extend(_repository_hygiene_findings(target))
    return findings


def _git_findings(target: Path) -> list[Finding]:
    if not is_git_repository(target):
        return [
            Finding(
                "git-repository",
                "Git repository",
                "error",
                "This directory is not a Git worktree.",
                0,
                8,
            ),
            Finding(
                "git-branch",
                "Publication branch",
                "warning",
                "Branch could not be checked because Git is unavailable for this directory.",
                0,
                5,
            ),
            Finding(
                "git-worktree",
                "Clean Git worktree",
                "warning",
                "Git is unavailable, so the worktree state could not be checked.",
                0,
                8,
            ),
        ]

    branch = current_branch(target)
    branch_finding = Finding(
        "git-branch",
        "Publication branch",
        "pass" if branch in PREFERRED_BRANCHES else "warning",
        f"Current branch is '{branch}'."
        if branch in PREFERRED_BRANCHES
        else f"Current branch is '{branch or 'detached HEAD'}'; preferred branch is 'main'.",
        5 if branch in PREFERRED_BRANCHES else 0,
        5,
    )
    changes = worktree_changes(target) or []
    worktree_finding = Finding(
        "git-worktree",
        "Clean Git worktree",
        "pass" if not changes else "warning",
        "No uncommitted files detected."
        if not changes
        else f"{len(changes)} uncommitted Git change(s) detected.",
        8 if not changes else 0,
        8,
    )
    return [
        Finding("git-repository", "Git repository", "pass", "Git worktree detected.", 8, 8),
        branch_finding,
        worktree_finding,
    ]


def _documentation_findings(target: Path) -> list[Finding]:
    findings: list[Finding] = []
    for document_name, points, severity in REQUIRED_DOCUMENTS:
        exists = (target / document_name).is_file()
        findings.append(
            Finding(
                f"required-{document_name.lower().replace('.', '-')}",
                f"Required file: {document_name}",
                "pass" if exists else severity,
                f"{document_name} found." if exists else f"{document_name} is missing.",
                points if exists else 0,
                points,
            )
        )

    readme = target / "README.md"
    readme_is_substantive = (
        readme.is_file() and len(_read_text(readme)) >= README_MINIMUM_CHARACTERS
    )
    findings.append(
        Finding(
            "readme-substance",
            "Substantive README",
            "pass" if readme_is_substantive else "error",
            "README has enough content for a first public explanation."
            if readme_is_substantive
            else f"README needs at least {README_MINIMUM_CHARACTERS} readable characters.",
            5 if readme_is_substantive else 0,
            5,
        )
    )

    gitignore = target / ".gitignore"
    safe_gitignore = gitignore.is_file() and ".env" in _read_text(gitignore)
    findings.append(
        Finding(
            "gitignore-secrets",
            "Secrets protected by .gitignore",
            "pass" if safe_gitignore else "error",
            ".gitignore includes .env."
            if safe_gitignore
            else "Add a .gitignore entry for .env before publication.",
            5 if safe_gitignore else 0,
            5,
        )
    )

    docs_directory = target / "docs"
    findings.append(
        Finding(
            "docs-directory",
            "Documentation directory",
            "pass" if docs_directory.is_dir() else "warning",
            "docs/ directory found." if docs_directory.is_dir() else "docs/ directory is missing.",
            3 if docs_directory.is_dir() else 0,
            3,
        )
    )
    screenshots_directory = target / "screenshots"
    findings.append(
        Finding(
            "screenshots-directory",
            "Screenshots directory",
            "pass" if screenshots_directory.is_dir() else "warning",
            "screenshots/ directory found."
            if screenshots_directory.is_dir()
            else "screenshots/ directory is missing.",
            2 if screenshots_directory.is_dir() else 0,
            2,
        )
    )
    portuguese_digest = target / "README.pt-BR.md"
    findings.append(
        Finding(
            "portuguese-digest",
            "Portuguese project digest",
            "pass" if portuguese_digest.is_file() else "info",
            "Optional README.pt-BR.md found."
            if portuguese_digest.is_file()
            else "Optional: add README.pt-BR.md for a concise Portuguese overview.",
        )
    )
    return findings


def _repository_hygiene_findings(target: Path) -> list[Finding]:
    files = list(iter_project_files(target))
    relative_files = [file_path.relative_to(target) for file_path in files]
    findings: list[Finding] = []

    secret_files = _find_secret_files(target, files)
    findings.append(
        Finding(
            "secret-exposure",
            "Potential secret exposure",
            "pass" if not secret_files else "error",
            "No likely secret files or values detected."
            if not secret_files
            else f"Review or remove: {_format_paths(secret_files)}.",
            15 if not secret_files else 0,
            15,
        )
    )

    large_files = [
        relative
        for file_path, relative in zip(files, relative_files, strict=True)
        if _safe_file_size(file_path) > MAX_FILE_SIZE_BYTES
    ]
    findings.append(
        Finding(
            "large-files",
            "Large repository files",
            "pass" if not large_files else "warning",
            "No files above 10 MB detected."
            if not large_files
            else f"Files above 10 MB: {_format_paths(large_files)}.",
            4 if not large_files else 0,
            4,
        )
    )

    candidate_noise_paths = find_noise_directories(target) + [
        target / relative
        for relative in relative_files
        if relative.name in NOISE_FILE_NAMES or relative.suffix in NOISE_SUFFIXES
    ]
    noise_paths = [
        path for path in candidate_noise_paths if not is_ignored_by_git(target, path)
    ]
    findings.append(
        Finding(
            "generated-noise",
            "Generated files and folders",
            "pass" if not noise_paths else "warning",
            "No common generated artifacts detected."
            if not noise_paths
            else "Consider removing or ignoring: "
            f"{_format_paths([path.relative_to(target) for path in noise_paths])}.",
            3 if not noise_paths else 0,
            3,
        )
    )

    has_tests = any(
        relative.name.startswith("test_") and relative.suffix == ".py" and "tests" in relative.parts
        for relative in relative_files
    )
    findings.append(
        Finding(
            "tests-present",
            "Automated tests",
            "pass" if has_tests else "warning",
            "Test files detected." if has_tests else "No Python test files found under tests/.",
            5 if has_tests else 0,
            5,
        )
    )
    return findings


def _find_secret_files(target: Path, files: list[Path]) -> list[Path]:
    suspicious: list[Path] = []
    for file_path in files:
        if file_path.name == ".env" or (
            file_path.name.startswith(".env") and not is_allowed_env_example(file_path)
        ):
            suspicious.append(file_path)
            continue
        if (
            file_path.name in SENSITIVE_FILE_NAMES
            or file_path.suffix.lower() in SENSITIVE_FILE_SUFFIXES
        ):
            suspicious.append(file_path)
            continue
        if file_path.suffix.lower() not in TEXT_SUFFIXES or _safe_file_size(file_path) > 1_000_000:
            continue
        content = _read_text(file_path)
        if any(pattern.search(content) for pattern in SECRET_CONTENT_PATTERNS):
            suspicious.append(file_path)
    return [path.relative_to(target) for path in suspicious]


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def _safe_file_size(path: Path) -> int:
    try:
        return path.stat().st_size
    except OSError:
        return 0


def _format_paths(paths: list[Path], limit: int = 5) -> str:
    rendered = [path.as_posix() for path in paths[:limit]]
    if len(paths) > limit:
        rendered.append(f"and {len(paths) - limit} more")
    return ", ".join(rendered)
