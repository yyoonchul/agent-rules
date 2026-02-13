# Core Beliefs

> This document defines the invariant principles that agents must follow when working on this project.

## Code Quality

1. **Test First**: All feature changes must be accompanied by tests.
2. **Incremental Changes**: Prefer small, reviewable changes over large ones.
3. **Explicit > Implicit**: Prefer clear code over "magic".

## Architecture

4. **Dependency Direction**: High-level layers depend on low-level layers. No circular dependencies.
5. **Boundary Maintenance**: Domain logic should not know about infrastructure details.

## Process

6. **Design First**: For tasks taking more than 2 days, write a design document first.
7. **Doc Synchronization**: Update relevant documentation when code changes.

## Agent Operation

8. **Autonomy Scope**: Agents perform changes following existing patterns independently.
9. **Escalation**: Confirm with a human before introducing new patterns, adding dependencies, or changing schemas.
10. **Plan Recording**: For complex tasks, create a plan and track progress.
