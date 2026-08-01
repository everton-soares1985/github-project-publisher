"""Central configuration for the publication protocol."""

# ================= CONFIGURAÇÕES =================
# Keep protocol weights explicit: all scored checks add up to 100 points.

import re
from pathlib import Path

PREFERRED_BRANCHES = ("main",)
README_MINIMUM_CHARACTERS = 160
MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024

REQUIRED_DOCUMENTS = (
    ("README.md", 10, "error"),
    ("LICENSE", 8, "error"),
    ("CHANGELOG.md", 4, "warning"),
    ("CONTRIBUTING.md", 4, "warning"),
    ("SECURITY.md", 8, "error"),
    ("AGENTS.md", 3, "warning"),
)

EXCLUDED_DIRECTORY_NAMES = {
    ".git",
    ".venv",
    "venv",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    "build",
    "dist",
}
NOISE_DIRECTORY_NAMES = {"__pycache__", ".pytest_cache", ".ruff_cache", "node_modules"}
NOISE_FILE_NAMES = {".coverage"}
NOISE_SUFFIXES = {".pyc"}
TEXT_SUFFIXES = {
    ".bat",
    ".cfg",
    ".env",
    ".ini",
    ".json",
    ".md",
    ".ps1",
    ".py",
    ".sh",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
}
SENSITIVE_FILE_SUFFIXES = {".key", ".pem", ".p12", ".pfx"}
SENSITIVE_FILE_NAMES = {"id_rsa", "id_dsa", "id_ecdsa", "id_ed25519"}

SECRET_CONTENT_PATTERNS = (
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----", re.IGNORECASE),
    re.compile(
        r"(?im)^\s*(?:api[_-]?key|secret|token|password|access[_-]?key)\s*[:=]\s*['\"]?[^\s'\"]{8,}"
    ),
)


def is_allowed_env_example(path: Path) -> bool:
    """Return whether a dotenv file is an intentionally safe example."""

    return path.name in {".env.example", ".env.sample", ".env.template"}
