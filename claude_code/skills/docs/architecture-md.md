# Architecture Overview

> Last Updated: {{Date}}

## System Overview

{{2-3 sentences describing what the system does}}

## Architecture Diagram

```
{{ASCII or Mermaid diagram}}
```

## Domains

### {{Domain 1}}

- **Responsibility**: {{1-2 sentences}}
- **Location**: `src/{{path}}/`
- **Dependencies**: {{other domains it depends on}}

### {{Domain 2}}

- **Responsibility**: {{1-2 sentences}}
- **Location**: `src/{{path}}/`
- **Dependencies**: {{other domains it depends on}}

## Package Hierarchy

Dependencies flow only from top to bottom:

```
Presentation (API / UI)
    ↓
Application (Use Cases)
    ↓
Domain (Business Logic)
    ↓
Infrastructure (DB, External APIs)
```

## Data Flow

{{Description of key data flows}}

## Key Technical Decisions

| Decision | Rationale | Alternatives | Date |
|----------|-----------|--------------|------|
| {{Decision}} | {{Rationale}} | {{Alternatives considered}} | {{Date}} |
