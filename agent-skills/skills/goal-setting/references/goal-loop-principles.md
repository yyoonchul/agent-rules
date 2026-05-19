# Goal Loop Principles

This reference summarizes the local `codex-goal-loop-guide.html` for the `goal-setting` skill.

## Stable Goal Elements

A long-running `/goal` prompt should include:

1. Single objective.
2. Context to read first.
3. Scope and forbidden changes.
4. Validation commands ordered from narrow to broad.
5. Checkpoints and durable progress logging.
6. Failure classification.
7. Stop rules.
8. Final evidence requirements.

When any of these elements are unclear, the setup phase should gather missing
information through conversation before writing the goal artifacts. Conservative
repo-derived assumptions are acceptable only after asking, and they must be
recorded as assumptions or open questions.

## Recommended Files

- `PLAN.md`: source of truth for objective, scope, milestones, and done criteria.
- `PROGRESS.md`: append-style checkpoint log and validation evidence.
- `VALIDATION.md`: deterministic checks, semantic checks, human gates, and failure classes.
- `implementation-notes.html`: running dashboard for decisions outside the spec, required changes, tradeoffs, validation state, and user handoff notes.
- `GOAL_PROMPT.md`: the ready-to-run `/goal` command.

These files are temporary scaffolding for the goal run. After the goal completes
and final evidence is summarized to the user, delete the generated goal
artifacts unless the user explicitly asks to keep them. Never delete
user-provided context, implementation files, or requested deliverables as part
of cleanup.

## Validation Layers

- Deterministic: typecheck, lint, unit tests, integration tests, snapshots, schema validation, link checks.
- Semantic: review model, rubric, screenshots, accessibility check, eval thresholds, data-quality inspection.
- Human gate: deployment, billing, deletion, data export, security policy changes, secrets, product decisions.

## Stop Rules

Pause when:

- The same failure class occurs 3 times.
- A product, scope, validation, or safety decision is unclear and cannot be answered from the plan, validation notes, or referenced context.
- A destructive action or external permission is required.
- Cleanup would delete user-provided context, implementation files, requested deliverables, or files outside the generated goal artifact set.
- The task needs a product/security/legal decision.
- Validation cannot run because of missing dependencies or environment access.
- The task would exceed the declared scope.

## Evidence Requirements

Final evidence should include:

- Commands run.
- Exit codes.
- Changed files.
- Final `implementation-notes.html` dashboard state.
- Test or check summaries.
- Known residual risks.
- Human gates that remain unresolved.
