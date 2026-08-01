# Contributing

## Development setup

```powershell
python -m venv .venv
.venv\Scripts\activate
python -X utf8 -m pip install -e ".[dev]"
```

## Before submitting changes

```powershell
python -X utf8 -m pytest
python -X utf8 -m ruff check .
```

Keep target-repository audits read-only unless a future reviewed apply mode explicitly authorizes
changes.
