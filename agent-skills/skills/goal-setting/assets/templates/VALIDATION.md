# VALIDATION

## Deterministic Checks

Run the narrowest relevant checks after each milestone, then broad checks before final completion.

| Stage | Command or Check | When To Run | Expected Result |
| --- | --- | --- | --- |
| Narrow | <!-- command --> | <!-- after milestone --> | exits 0 |
| Broad | <!-- command --> | before final summary | exits 0 |

## Semantic Checks

- <!-- Review rubric, visual check, eval threshold, accessibility check, or data-quality check -->

## Human Gates

Pause before:

- Deployment or release.
- Destructive file/data changes.
- Billing, payments, or external service changes.
- Secrets, credentials, or data export.
- Security policy weakening.
- Product behavior decisions not specified in PLAN.md.

## Failure Classes

| Class | Examples | Retry Rule |
| --- | --- | --- |
| Test failure | assertion, snapshot, type error | one focused repair per checkpoint |
| Environment/dependency | missing service, network, install issue | report required access |
| Ambiguous requirement | unclear UX/product/security behavior | pause for user decision |
| Permission required | sandbox, external dir, destructive action | request approval or pause |
| Flaky check | nondeterministic failure | rerun once, then classify |

## Evidence Format

Every validation entry in `PROGRESS.md` must include:

- Command or check.
- Exit code or pass/fail result.
- Short output summary.
- Changed files relevant to the check.
- Residual risk.
