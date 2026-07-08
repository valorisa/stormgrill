# Contributing / Contribuer

*English below / Anglais plus bas.*

## FR

1. Créer une branche nommée depuis `dev` : `git checkout -b feat/nom-de-la-fonctionnalite`
2. Commits au format [Conventional Commits](https://www.conventionalcommits.org/) (`feat:`, `fix:`, `docs:`, `ci:`, ...)
3. Ouvrir une PR vers `dev` : `gh pr create`
4. Attendre les checks CI : `gh pr checks --watch`
5. Squash-merge : `gh pr merge --squash --delete-branch`
6. `main` et `backup` sont synchronisés en fast-forward depuis `dev`

Lint markdown : `markdownlint-cli2 "**/*.md"` (config dans `.markdownlint.json`, 120 caractères/ligne).

Lint & tests Python : `ruff check src/ tests/ && pytest`

## EN

1. Create a named branch from `dev`: `git checkout -b feat/feature-name`
2. Commits follow [Conventional Commits](https://www.conventionalcommits.org/) (`feat:`, `fix:`, `docs:`, `ci:`, ...)
3. Open a PR against `dev`: `gh pr create`
4. Wait for CI checks: `gh pr checks --watch`
5. Squash-merge: `gh pr merge --squash --delete-branch`
6. `main` and `backup` are fast-forwarded from `dev`

Markdown lint: `markdownlint-cli2 "**/*.md"` (config in `.markdownlint.json`, 120 chars/line).

Python lint & tests: `ruff check src/ tests/ && pytest`
