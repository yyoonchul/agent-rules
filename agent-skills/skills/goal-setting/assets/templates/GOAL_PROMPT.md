# GOAL PROMPT

```text
/goal Complete <objective> without stopping until <verifiable end state>.

Read first:
- @PLAN.md
- @VALIDATION.md
- @PROGRESS.md
- @implementation-notes.html

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
