# Agent Guidance

## Non-negotiable rules

- Keep `audit` and `check` read-only for target repositories.
- Do not hardcode API keys or create a requirement for an API key.
- Do not weaken tests to pass a gate.
- Do not add automatic mutation features before an explicit apply-mode design is approved.
- Run `python -X utf8 -m pytest` and `python -X utf8 -m ruff check .` after code changes.

## Language policy

- English is the canonical language for public documentation.
- `README.pt-BR.md` is an optional Portuguese summary, not a duplicate full manual.
