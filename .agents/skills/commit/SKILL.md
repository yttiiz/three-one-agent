---
name: commit
description: Commit staged changes grouped by logical change. Use when committing multiple independent changes separately, when you need to create atomic commits per logical unit of work, or after making a mix of changes across the codebase. Analyzes git status and creates properly formatted commits following commitlint conventions.
---

# Commit Per Change

Create separate commits for each logical change, following the project's commitlint conventions. A "logical change" is a coherent unit of work — one feature, one fix, one refactor — regardless of how many files or modules it touches.

## Core Principle

**Group by intent, not by location.** A single feature that spans multiple modules is one commit. Two unrelated fixes in the same module are two commits.

## Workflow

1. **Survey all changes**
   - Run `git status --porcelain` to list modified files
   - Run `git diff` (and `git diff --staged`) to understand what actually changed
   - Read the diffs — don't rely on file paths alone to infer intent

2. **Group files by logical change**
   - Identify coherent units: each feature, fix, refactor, or concern is its own group
   - A single group may span multiple modules (e.g., a feature touching `memory` + `models`)
   - A single module may contribute to multiple groups (split it across commits)
   - Unrelated changes must go in separate commits, even if they sit in the same file — use `git add -p` for hunk-level staging when needed

3. **For each logical change**
   - Stage only the files (or hunks) belonging to that change
   - Choose the best-fitting `type` and `scope` based on the change itself
   - Commit with proper format: `type(scope): Subject`
   - If the commit fails because the pre-commit hook's `bun lint` (`biome check .`) reports issues, run `bun lint:fix` (`biome check --write .`) to auto-fix them, re-stage the affected files, and retry the commit
   - Repeat until the working tree is clean (or only unrelated work remains)

## Commit Message Format

```
type(scope): subject line
```

### Valid Types

- `feat`: New feature
- `fix`: Bug fix
- `refactor`: Code restructuring (no new feature, no bug fix)
- `test`: Adding/updating tests
- `chore`: Maintenance tasks (dependencies, configs)
- `docs`: Documentation changes
- `style`: Code style changes (formatting, whitespace)
- `perf`: Performance improvements
- `build`: Build system changes
- `ci`: CI configuration changes
- `revert`: Revert a previous commit

### Valid Scopes

Scopes are defined by the project's commitlint config:

- `agent`: Root-level files (pyproject.toml, uv.lock, .python-version, ...)
- `models`: Backend (`src/models/`)
- `config`: Frontend PWA (`src/config/`)
- `tools`: Frontend PWA (`src/tools/`)
- `memory`: Frontend PWA (`src/memory/`)

When a logical change spans multiple scopes, pick the scope that best represents the **primary** intent of the change. If truly split, prefer separate commits.

### Subject Rules

- Use only lowercase letters
- No period at the end
- Maximum 100 characters for entire header
- Use imperative mood ("add feature" not "added feature")

## Choosing Commit Type

Let the nature of the change — not the file type — decide:

| Change Pattern                        | Type       |
| ------------------------------------- | ---------- |
| New user-facing capability            | `feat`     |
| Corrects broken behavior              | `fix`      |
| Restructure without behavior change   | `refactor` |
| Only test files changed               | `test`     |
| Only documentation (`*.md`)           | `docs`     |
| Dependencies, lockfiles               | `chore`    |
| Build tooling (Vite, bundler configs) | `build`    |
| CI/CD workflows                       | `ci`       |
| Formatting, whitespace only           | `style`    |
| Measurable performance work           | `perf`     |

If a change mixes types, pick the one that reflects the primary intent and mention the rest in the subject or split the commit.
