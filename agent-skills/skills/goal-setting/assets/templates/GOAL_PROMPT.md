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

Pause and report if:
- The same failure class occurs 3 times.
- A destructive action, external permission, secret, deployment, billing, or product decision is required.
- The requested change would violate the scope or non-goals in @PLAN.md.
```
