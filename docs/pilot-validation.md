# Pilot Validation Record

## Scope

This repository is the first project evaluated with the GitHub Project Publisher protocol.
The goal of this pilot is to verify that the tool can assess its own Git, documentation,
security, testing, and repository-hygiene requirements without mutating the target.

## Validation command

```powershell
project-publisher check .
```

## Expected result

- The command exits with code `0`.
- The readiness score is 100% in a clean working tree.
- The audit finds no likely secrets or unignored generated artifacts.
- The protocol files, test suite, lint configuration, and GitHub Actions workflow are present.

## Safety note

`audit` and `check` are read-only for the repository being inspected. Report files are only
written when the caller explicitly supplies `--json-output`.
