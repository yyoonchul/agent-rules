---
name: commit-convention
description: Applies the project's commit message convention. Use when writing commit messages, making git commits, or summarizing changes.
disable-model-invocation: false
argument-hint: "[change description]"
---

# Commit Message Convention

## Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

## Type Categories

| Type | Description | Example |
|---|---|---|
| `feat` | New feature | Add login feature |
| `fix` | Bug fix | Fix signup validation error |
| `docs` | Documentation changes | Update API documentation |
| `style` | Code formatting (no functional changes) | Fix indentation |
| `refactor` | Refactoring (no functional changes) | Improve auth module structure |
| `test` | Add/modify tests | Add login unit tests |
| `chore` | Build, config, and other tasks | Update packages |

## Rules

1. **subject** should be under 50 characters, written in imperative mood (e.g., "Add" not "Added")
2. **body** should wrap at 72 characters, explain "why" the change was made
3. **scope** is optional, indicates the area of change (e.g., `auth`, `api`, `ui`)
4. If there's a breaking change, specify `BREAKING CHANGE:` in the footer

## Example

```
feat(auth): Add social login feature

Supports Google and GitHub OAuth2 authentication.
Can be used alongside existing email login.

Closes #42
```

## Workflow

When $ARGUMENTS is provided:
1. Check changes with `git diff --staged` or `git diff`
2. Analyze the changes to determine appropriate type and scope
3. Generate a commit message following the convention above
4. Execute commit after user confirmation
