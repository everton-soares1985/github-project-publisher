# GitHub Project Publisher

> [Português — resumo do projeto](README.pt-BR.md)

Prepare repositories for publication with repeatable checks for documentation, Git hygiene,
security risks, project structure, and release readiness.

## Why it exists

Good projects are often published with missing documentation, uncommitted changes, accidental
secrets, or unclear setup instructions. GitHub Project Publisher provides a deterministic local
preflight before a repository is shared.

## MVP scope

Version `0.1.0` is intentionally read-only for target repositories:

- `audit`: reports documentation, Git, security, and structure findings;
- `check`: applies the publication gate and exits non-zero when the project is not ready;
- terminal and JSON reports with a readiness score;
- tests that prove the audit does not alter the target repository.

Automatic changes through `apply` are a future phase and will require an explicit review flow.

## Quickstart

```powershell
python -m venv .venv
.venv\Scripts\activate
python -X utf8 -m pip install -e ".[dev]"
project-publisher audit C:\path\to\repository
project-publisher check C:\path\to\repository
```

## Current checks

| Area | Examples |
| --- | --- |
| Git | repository, preferred branch, uncommitted changes |
| Documentation | README, license, changelog, contribution and security files |
| Security | `.env`, private keys, likely credentials |
| Quality | tests, oversized files, tracked runtime artifacts |
| Presentation | `docs/`, screenshots folder, optional Portuguese summary |

## Language policy

Public projects use English as their primary language. A project may optionally provide a concise
`README.pt-BR.md` for Portuguese-speaking readers without duplicating the complete technical
documentation.

## Safety

`audit` and `check` never modify the target repository unless the user explicitly supplies a
JSON report destination. Findings are evidence-based and are intended to be reviewed before any
future apply mode exists.

## Development

```powershell
.venv\Scripts\activate
python -X utf8 -m pytest
python -X utf8 -m ruff check .
```

## License

MIT. See [LICENSE](LICENSE).
