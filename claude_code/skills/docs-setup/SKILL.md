name: docs-setup
description: Initializes and manages the project's documentation structure. Follows the "in‑repository knowledge store" pattern, using AGENTS.md as the map and docs/ as the system of record. Use for project docs initialization, design docs, and product specs.
argument-hint: "[init | add-design-doc | add-spec | sync]"
---

# Project Documentation Structure Management Skill

## Core Principles

This skill follows the principle of **progressive disclosure**:
- `AGENTS.md` acts as a **map**, not an encyclopedia
- It is designed so that agents can discover detailed information themselves
- All detailed content is organized under the `docs/` directory

## Commands

### `init` — Initialize documentation structure

Creates the full documentation structure in the project root.

1. Inspect the existing project structure (package.json, go.mod, Cargo.toml, etc.)
2. Create the following directory tree:

```
AGENTS.md
ARCHITECTURE.md
docs/
├── design-docs/
│   ├── index.md
│   └── core-beliefs.md
├── product-specs/
│   └── index.md
├── references/
├── DESIGN.md
├── FRONTEND.md
├── PLANS.md
```

3. Populate each file with initial content tailored to the project context
4. Use this skill's `templates/` directory as the source of templates

**Important**: Do not overwrite existing files. Only create missing ones.

### `add-design-doc <title>` — Add a design document

1. Create a new design doc under `docs/design-docs/`
2. Convert the title to kebab‑case for the filename (e.g. "User authentication flow" → `user-auth-flow.md`)
3. Add an entry to `docs/design-docs/index.md`
4. Start the status as `draft`
5. Template: [templates/design-doc.md](templates/design-doc.md)

### `add-spec <title>` — Add a product spec

1. Create a new spec under `docs/product-specs/`
2. Add an entry to `docs/product-specs/index.md`
3. Template: [templates/product-spec.md](templates/product-spec.md)

### `sync` — Verify documentation consistency

1. Check that all links in `AGENTS.md` point to real files
2. Ensure `docs/design-docs/index.md` lists all existing design docs
3. Report broken links and inconsistencies

## AGENTS.md authoring guidelines

`AGENTS.md` is the main entry point for agents. Follow these rules:

1. **Keep it short**: Under 500 lines. Link out to details.
2. **Act as a map**: Focus on "what lives where".
3. **Required sections**:
   - Project overview (2–3 sentences)
   - Tech stack
   - Directory structure summary
   - Documentation navigation (links to files under `docs/`)
   - Core rules (≤ 5 invariant rules)
4. **Avoid**: Implementation details, full API references, long code examples

## ARCHITECTURE.md authoring guidelines

1. Describe the system's **domains and package/layer structure**
2. Clearly document dependency directions and boundaries
3. Prefer ASCII diagrams or Mermaid syntax for visuals
4. Summarize each major module's responsibility in 1–2 sentences

## Additional resources

- Templates for each document type: see the [templates/](templates/) directory
- Good examples: see the [examples/](examples/) directory
