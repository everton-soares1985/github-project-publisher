---
name: growthtech-github-publisher
description: Audit, standardize, maintain, and prepare software repositories for safe GitHub publication using the GrowthTech protocol. Use for first publication, retrofit of an existing repository, README or publication-document improvements, release preparation, and routine pre-commit or pre-push validation. Treat fixes, features, commits, and pushes as incremental maintenance unless the user explicitly requests full standardization.
---

# GrowthTech GitHub Publisher

Use the GitHub Project Publisher repository as the canonical protocol implementation.

## Select one mode first

- **Maintenance (default):** Use for fixes, features, documentation edits, commits, and pushes. Preserve the established visual identity and repository structure. Never regenerate banners, badges, screenshots, diagrams, or the full README unless the user explicitly requests that specific change.
- **Bootstrap:** Use only for a new project's first full publication setup.
- **Retrofit:** Use only when the user explicitly asks to standardize an existing project. Audit first, propose a reversible change set, and apply it only after approval.
- **Release:** Use when preparing an explicit version, tag, or GitHub release. Validate release evidence without redesigning the project.

A request to commit, push, fix, or add a feature does not authorize bootstrap, retrofit, visual regeneration, or unrelated documentation changes. If mode remains uncertain, choose Maintenance.

## Workflow by mode

### Maintenance

1. Inspect repository instructions and the current Git diff.
2. Keep changes within the user's requested scope.
3. Update documentation or `CHANGELOG.md` only when the change affects users, operation, compatibility, security, or release history.
4. Run relevant repository-native tests and lint, then run:

   ```powershell
   project-publisher check <repository-path>
   ```

5. Use a concise Conventional Commit when authorized: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`, `ci:`, `perf:`, `security:`, or `release:`.
6. Never commit or push unless the user requests it.

### Bootstrap or Retrofit

1. Inspect existing instructions and run the read-only baseline:

   ```powershell
   project-publisher audit <repository-path>
   ```

2. Explain findings and propose a minimal, reversible change set.
3. Apply only approved changes; preserve working code and functional structure.
4. Re-run repository-native validation and `project-publisher check <repository-path>`.

### Release

Inspect the diff and release history, run the complete test/lint/build commands available in the repository, finalize only relevant version and changelog material, then run the publication check. Create tags or releases only when explicitly authorized.

## Full publication standard

Apply this complete standard only in Bootstrap or approved Retrofit work:

- Keep `README.md` and main technical documentation in English.
- Offer `README.pt-BR.md` only as a concise Portuguese digest.
- Require `README.md`, `LICENSE`, `CHANGELOG.md`, `CONTRIBUTING.md`, `SECURITY.md`, and `AGENTS.md`.
- Use concise badges, an established banner, real screenshots in `screenshots/`, and Mermaid only when a diagram materially improves understanding.
- Keep detailed material in `docs/` and prefer `main` as the publication branch.

## Safety boundary

- Keep `audit` and `check` read-only for target repositories.
- Stop publication for likely secrets, `.env` files, private keys, or missing critical documents; never expose secret contents.
- Do not rewrite application code, move project folders, install visual-generation dependencies, or alter established assets merely to fit the presentation standard.
- In Maintenance and Release, modify visual assets only when explicitly requested or when the related asset is demonstrably broken by the current change.
