<p align="center">
  <img src="assets/banner.svg" alt="GitHub Project Publisher — ship with confidence" width="100%">
</p>

<p align="center">
  <a href="https://github.com/everton-soares1985/github-project-publisher/actions/workflows/ci.yml"><img src="https://github.com/everton-soares1985/github-project-publisher/actions/workflows/ci.yml/badge.svg" alt="CI status"></a>
  <img src="https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white" alt="Python 3.12">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-0E7490" alt="MIT license"></a>
  <img src="https://img.shields.io/badge/Protocol-v0.1.0-1E293B" alt="Protocol version 0.1.0">
</p>

<p align="center">
  <strong>Audit and validate repositories before publishing them on GitHub.</strong><br>
  A deterministic local preflight for documentation, Git hygiene, security, and release readiness.
</p>

<p align="center">
  <a href="#quickstart">Quickstart</a> ·
  <a href="#how-it-works">How it works</a> ·
  <a href="#what-it-checks">Checks</a> ·
  <a href="README.pt-BR.md">Português</a>
</p>

---

## Ship with evidence, not assumptions

Good projects are often published with missing documentation, uncommitted changes, accidental
secrets, or unclear setup instructions. GitHub Project Publisher gives you a transparent
publication gate before a repository is shared.

Version `0.1.0` is deliberately **read-only** for target repositories. It reports what needs
attention; it never changes the inspected project.

| Command | Purpose | Result |
| --- | --- | --- |
| `project-publisher audit <path>` | Inspect a repository | Full report for review |
| `project-publisher check <path>` | Run the publication gate | Exit code `0` only when ready |

## How it works

```mermaid
flowchart LR
    A[Repository] --> B[Audit]
    B --> C{Findings}
    C -->|Errors or warnings| D[Review and improve]
    D --> B
    C -->|Ready| E[Check]
    E --> F[Publish with confidence]

    classDef action fill:#0f766e,color:#ffffff,stroke:#0f766e;
    classDef gate fill:#1e293b,color:#ffffff,stroke:#1e293b;
    class B,E action;
    class C gate;
```

<p align="center">
  <img src="assets/self-validation.svg" alt="Self-validation result: 100 percent ready, zero errors and zero warnings" width="760">
</p>

<p align="center"><sub>Real self-validation result on <code>main</code>. See <a href="docs/pilot-validation.md">the pilot record</a>.</sub></p>

## Quickstart

```powershell
python -m venv .venv
.venv\Scripts\activate
python -X utf8 -m pip install -e ".[dev]"

project-publisher audit C:\path\to\repository
project-publisher check C:\path\to\repository
```

Use `--json-output report.json` when a machine-readable report is needed.

## What it checks

| Area | Evidence collected |
| --- | --- |
| Git hygiene | Git repository, preferred branch, uncommitted changes |
| Documentation | README, license, changelog, contribution and security files |
| Security | `.env`, private keys, and likely credentials without exposing values |
| Quality | Python tests, oversized files, and unignored generated artifacts |
| Presentation | `docs/`, screenshots folder, and optional Portuguese project digest |

## Safety by design

`audit` and `check` do not modify the target repository. A JSON file is written only when you
explicitly provide `--json-output`. Any future `apply` mode must be designed around a separate
review-and-approval step.

## Language policy

English is the canonical language for public documentation. Projects may include a concise
[Portuguese digest](README.pt-BR.md) without duplicating the complete technical documentation.

## Development

```powershell
.venv\Scripts\activate
python -X utf8 -m pytest
python -X utf8 -m ruff check .
```

## License

MIT. See [LICENSE](LICENSE).
