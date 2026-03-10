---
name: commit-convention
description: Applies the project's commit message convention. Use when writing commit messages, making git commits, or summarizing changes.
disable-model-invocation: false
argument-hint: "[change description]"
---

# Commit Message Convention

## Project-Specific Convention

If `.commitconventionrc` exists in the project root, read it and apply its `types`, `scopes`, and `rules` as the commit convention for this project. The file is JSON and takes precedence over the defaults below.

## Default Convention

Used when no `.commitconventionrc` is found.

### Format

```
<type>(<scope>): <subject>

<body>
```

### Type Categories

| Type | Description |
|---|---|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation changes |
| `style` | Code formatting (no functional changes) |
| `refactor` | Refactoring (no functional changes) |
| `test` | Add/modify tests |
| `chore` | Build, config, and other tasks |

### Rules

1. **subject**: under 72 characters, imperative mood, lowercase start, no period
2. **body**: optional, wrap at 100 characters, explain "why" the change was made
3. **scope**: optional, indicates the area of change

## Workflow

When generating a commit message:
1. Check for `.commitconventionrc` in the project root — if found, use its config
2. Analyze changes with `git diff --staged` (or `git diff` if nothing staged)
3. Determine appropriate type and scope from the convention
4. Generate a commit message following the convention rules
