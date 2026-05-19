---
name: goal-setting
description: Use this skill when a user wants to prepare a Codex or Claude /goal run by collaboratively defining the objective, scope, plan, test conditions, validation evidence, stop rules, and the final inline /goal prompt. Use it before long-running coding, migration, evaluation, testing, or polishing work where durable files like PLAN.md and PROGRESS.md should guide the goal loop.
---

# Goal Setting

## Purpose

Prepare a reliable `/goal` run. This skill turns a vague long-running task into durable planning and verification artifacts, then returns a ready-to-run inline `/goal` prompt that mentions those files and tells the goal loop how to use them.

Base the workflow on the repository guide `codex-goal-loop-guide.html` when present. Its core rule is: a good goal is not just an objective; it includes context, scope, checkpoints, validation commands, failure handling, stop rules, and final evidence.

## Default Output Files

Create these files in the target work area. Prefer the user's requested location; otherwise use the project root if the files do not exist, or `goal/<task-slug>/` if root files would overwrite existing plans.

- `PLAN.md`: objective, context, scope, milestones, task table, and done criteria.
- `VALIDATION.md`: test conditions, commands, evidence expectations, semantic checks, and human approval gates.
- `PROGRESS.md`: checkpoint log template for the goal loop to update while running.
- `implementation-notes.html`: living implementation dashboard for decisions not covered by the spec, required changes, tradeoffs, validation state, and anything the user should know.
- `GOAL_PROMPT.md`: the final prompt as a saved artifact, while also returning the prompt inline in the final response.

If the task is UI, data, security, deployment, evaluation, or migration heavy, create one extra focused file only when useful:

- `ACCESSIBILITY.md` for UI keyboard/contrast/screen checks.
- `EVAL_CASES.md` for prompt/model/eval improvement tasks.
- `ROLLBACK.md` for deployment, data migration, or risky operational changes.
- `STEERING.md` when mid-flight decisions are expected.

Use `assets/templates/` as the starting point for standard files.

## Artifact Cleanup

The generated planning files are temporary goal-loop scaffolding. The final
`/goal` prompt must tell the goal loop to delete its own goal artifacts after
the done criteria are satisfied and final evidence has been summarized to the
user.

Default cleanup targets are:

- `PLAN.md`
- `VALIDATION.md`
- `PROGRESS.md`
- `implementation-notes.html`
- `GOAL_PROMPT.md`
- Extra focused files created only for the goal run, such as `ACCESSIBILITY.md`,
  `EVAL_CASES.md`, `ROLLBACK.md`, or `STEERING.md`

Do not delete user-provided source/context files, implementation files,
deliverables requested by the user, or any artifact the user explicitly asks to
keep. If cleanup would require deleting files outside the generated goal
artifact set, pause and ask first.

## Conversation Workflow

1. Identify whether the user's request is already concrete enough.
2. If key fields are missing or ambiguous, gather information through conversation before creating files. Ask concise, grouped questions, then follow up on answers that still leave scope, objective, validation, or product decisions unclear.
3. Required fields:
   - Objective: one outcome, not a backlog bundle.
   - Context to read: files, issues, logs, docs, failing tests, screenshots, or examples.
   - Scope: paths that may change and boundaries that must not change.
   - Plan: milestones small enough for one checkpoint at a time.
   - Test conditions: deterministic commands first, semantic checks second, human gates last.
   - Done criteria: verifiable end state with commands, exit codes, and evidence files.
   - Stop rules: repeated failure, missing permissions, unclear product decision, destructive action, time/token budget, or external dependency.
4. Do not silently resolve unclear product, scope, validation, or safety decisions. Ask the user first; if the user explicitly cannot provide a field after that conversation, infer a conservative default from the repo and mark it as an assumption or open question in `PLAN.md`.
5. Before editing, briefly tell the user which files will be created or updated.

## Artifact Requirements

### `PLAN.md`

Must include:

- Goal statement.
- Non-goals and forbidden changes.
- Context inventory with `@file`-style references where possible.
- Scope table: allowed paths, restricted paths, owner approval needed.
- Milestone table with ID, task, expected output, validation, and status.
- Done criteria that can be evaluated from files, command results, or explicit user approval.
- Assumptions and open questions.
- Explicitly unresolved questions that the goal loop must pause on before making product, scope, validation, or safety decisions.

### `VALIDATION.md`

Must include layered validation:

- Deterministic checks: smallest relevant command after each checkpoint, then full build/test/lint/typecheck.
- Semantic checks: review rubric, screenshot comparison, eval threshold, accessibility review, or data-quality review as applicable.
- Human gates: deployment, destructive changes, billing, secrets, data export, schema breaks, security weakening, or product decisions.
- Failure classification: test failure, dependency/environment problem, ambiguous requirement, permission request, flaky check, or out-of-scope request.
- Evidence format: command, exit code, relevant output summary, changed files, residual risk.

### `PROGRESS.md`

Must be a runtime log template, not a completed report. Include:

- Current state.
- Checkpoint rows.
- Validation evidence rows.
- Failure ledger with retry count.
- Steering decisions.
- Final summary section.

### `implementation-notes.html`

Must be a living dashboard, not a completed report. Include:

- Current implementation status and active milestone.
- Decisions made because the spec was incomplete or ambiguous.
- Required changes discovered during implementation.
- Tradeoffs and alternatives considered.
- Validation status and residual risks.
- User-visible notes the goal loop should preserve for handoff.

### `GOAL_PROMPT.md` and Inline Prompt

The prompt must:

- Start with `/goal`.
- State the objective and verifiable end state.
- Mention every created file with `@` references.
- Explain how to use the files: read first, work checkpoint by checkpoint, update `PROGRESS.md`, keep `implementation-notes.html` current as a dashboard, run validation from `VALIDATION.md`, stop by stop rules.
- Include "Done only when" bullets with commands and evidence requirements.
- Include "Pause and report" bullets for blockers.
- Tell the goal loop to ask the user for clarification when a product, scope, validation, or safety decision is unclear instead of guessing.
- Tell the goal loop to clean up generated goal artifacts after completion, without deleting user-provided context or requested deliverables.

Return the exact same prompt inline in the final answer so the user can run it directly.

## Prompt Shape

Use this shape, adapting the details from the generated files:

```text
/goal Complete <objective> without stopping until <verifiable end state>.

Read first:
- @PLAN.md
- @VALIDATION.md
- @PROGRESS.md
- @implementation-notes.html
- <other @context files>

Scope:
- You may change: <paths>
- Do not change: <paths/contracts>

Loop:
1. Follow @PLAN.md milestone by milestone.
2. Before each checkpoint, update @PROGRESS.md with the current target.
3. After each checkpoint, run the smallest relevant checks from @VALIDATION.md.
4. Record commands, exit codes, changed files, and residual risks in @PROGRESS.md.
5. Keep @implementation-notes.html current as a running dashboard: decisions that were not in the spec, required changes, tradeoffs, validation state, and anything the user should know.
6. Classify failures using @VALIDATION.md and attempt one focused repair.

Done only when:
- <command/check> exits 0 or the documented human gate is satisfied.
- @PROGRESS.md contains final evidence: commands, exit codes, changed files, and remaining risks.
- @implementation-notes.html reflects the final decisions, tradeoffs, changed behavior, validation state, and residual risks.
- All done criteria in @PLAN.md are satisfied.
- Final evidence has been summarized to the user, then generated goal artifacts have been deleted: @PLAN.md, @VALIDATION.md, @PROGRESS.md, @implementation-notes.html, @GOAL_PROMPT.md, and any extra goal-only files created for this run.

Pause and report if:
- The same failure class occurs 3 times.
- A product, scope, validation, or safety decision is unclear and cannot be answered from @PLAN.md, @VALIDATION.md, or the referenced context.
- A destructive action, external permission, secret, deployment, billing, or product decision is required.
- The requested change would violate the scope or non-goals in @PLAN.md.
- Cleanup would delete user-provided context, implementation files, requested deliverables, or files outside the generated goal artifact set.
```

## Quality Check

Before finishing:

- Verify no generated artifact has unresolved placeholders like `<...>` unless explicitly marked as an open question.
- Verify `PLAN.md` and `VALIDATION.md` agree on commands and done criteria.
- Verify the inline prompt references all created files using the actual paths.
- If tests cannot be known from repo context, use a conservative validation discovery step in `VALIDATION.md`, such as "inspect package scripts and identify the narrowest relevant command before editing."
