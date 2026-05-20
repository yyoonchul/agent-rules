---
name: commit-manager
description: Analyze changed files, split work into intentional commit groups, create convention-based commits, and push too when the user includes push intent in the request.
---

# Commit Manager

Use this skill when asked to inspect changes, prepare commits, write commit
messages, create commits, or push committed work.

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

When preparing commits:

1. Check for `.commitconventionrc` in the project root. If found, use its config.
2. Inspect the full working tree before staging anything:
   - `git status --short`
   - `git diff --staged`
   - `git diff`
   - untracked files that may need to be read directly
3. Group changed files by independent intent. Each group should represent one
   coherent change that can stand alone in history.
4. Stage only the files needed for the current group.
5. If one file contains multiple unrelated intents, use patch staging for the
   relevant hunks. If the intents cannot be separated cleanly, say so before
   committing and explain the smallest safe commit boundary.
6. Before each commit, re-check `git diff --staged` and confirm that the staged
   contents match only the intended group.
7. Determine the appropriate type and scope from the convention.
8. Generate and use a commit message following the convention rules.
9. Repeat until every intended group is committed.
10. After all commits, run `git status --short` and report any remaining files.
11. If the user's original request includes push intent, such as "commit and
    push", "commit then push", "commit with push", "커밋하고 push", or
    "커밋 뒤에 push", treat that as push confirmation for the newly created
    commit(s).
12. If push intent was not included in the original request, ask the user
    whether they want to push the newly created commit(s).
13. If the user declines or does not explicitly confirm, stop after reporting
    the commit(s), current branch, upstream status, and the exact push command
    they can run later.
14. If pushing is confirmed, identify the target remote and branch from the
    current repository state, ask the user to confirm that target only if there
    is ambiguity, then run `git push` as part of this skill's workflow.
15. After pushing, report the pushed branch and final `git status --short`
    result.

## Safety Rules

- Never revert user changes unless the user explicitly asks for that revert.
- Do not mix unrelated changes into a commit.
- Do not stage files just because they are present in the working tree.
- Preserve existing staged user work unless the user asks you to reorganize it.
- If unrelated changes remain after the requested commits, leave them unstaged
  and report them.
