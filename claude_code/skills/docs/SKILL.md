name: docs
description: Initializes and manages the project's documentation structure. Follows the "in‑repository knowledge store" pattern, using AGENTS.md as the map and docs/ as the system of record. Use for project docs initialization, design docs, product specs, and syncing docs with code changes.
argument-hint: "[init | add-design-doc | add-spec | sync [branch|commit-range]]"
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

### `sync` — Analyze code changes and update documentation

Detects code changes, updates affected documentation, and verifies overall consistency.
Accepts an optional argument: a branch name, commit range, or change description.

#### Step 1: Determine Change Set

Focus only on **code changes** (exclude `*.md`):

```bash
# If argument is a branch name
git diff main..<branch> --name-only -- ':!*.md'

# If argument is a commit range
git diff <range> --name-only -- ':!*.md'

# If no argument, use working tree + recent commits
git diff --name-only HEAD -- ':!*.md'
git diff --name-only --cached -- ':!*.md'
git ls-files --others --exclude-standard -- ':!*.md'

# Fallback: last commit
git diff --name-only HEAD~1 HEAD -- ':!*.md'
```

If there are no changed code files, report:
> "No changed code detected. Commit your work or specify a branch/range before running sync."

#### Step 2: Classify Changes and Find Impacted Docs

From the changed file paths and diffs, classify the changes:

| Change Type | Heuristic | Potentially Affected Docs |
|---|---|---|
| Directory structure | New/moved/deleted directories | `AGENTS.md`, `ARCHITECTURE.md` |
| New module/package | New directory + entry file | `ARCHITECTURE.md` |
| Dependency changes | `package.json`, `go.mod`, `pyproject.toml`, etc. | `AGENTS.md` (tech stack), `ARCHITECTURE.md` |
| DB schema changes | Schema files, migrations | DB-related design docs |
| API changes | Router/controller files | Feature design docs, product specs |
| Config changes | Lint, build, CI config files | `docs/design-docs/core-beliefs.md` |
| Security changes | Auth, encryption, env handling | `docs/SECURITY.md` |
| New TODO/FIXME | Diff lines containing TODO/FIXME/HACK | `docs/exec-plans/tech-debt-tracker.md` |
| File deletions | Deleted files referenced in docs | Any doc linking to those files |

Then search for impacted documents:

```bash
for changed_file in <CHANGED_FILES>; do
  dir=$(dirname "$changed_file")
  base=$(basename "$changed_file")
  grep -rl "$base\|$dir" docs/ AGENTS.md ARCHITECTURE.md 2>/dev/null
done
```

#### Step 3: Review Core Documents

The following documents **must** be checked if related to the changed area:

| Document | Update Condition |
|---|---|
| `AGENTS.md` | Project structure, commands, key files, or tech stack changed |
| `ARCHITECTURE.md` | System architecture, domains, or data flow changed |
| `docs/FRONTEND.md` | Coding conventions, patterns, or folder structure changed |
| `docs/DESIGN.md` | UI components, design tokens, or styling rules changed |
| `docs/design-docs/*` | Implementation diverged from design |
| `docs/product-specs/*` | Spec behavior or status changed |

If a feature was changed but has no documentation, create `docs/features/<feature-name>.md`.

#### Step 4: Read Updated Code (Not Only the Diff)

For each impacted code file:

- Read the **full current file**, not just the diff
- Inspect key imports/exports to understand dependency changes
- For new modules, read all public APIs and entry points

Never update documentation based only on diff snippets; always use the **final code state** as the source of truth.

#### Step 5: Apply Targeted Updates

For each impacted document:

1. Read the current content
2. Locate sections that describe behavior affected by the code changes
3. Update **only those sections** to reflect the new behavior/structure
4. Leave unrelated sections untouched

**Update scope:**
- **Add**: When new features, files, or patterns are created
- **Modify**: When existing descriptions don't match the code
- **Delete**: When documentation for removed features remains
- **No change**: Don't touch if unrelated

**Style rules:**
- Maintain the existing document's tone and format
- Verify code examples match the actual code
- Write file paths relative to project root
- All documentation must be in **English**

**Per-document guidelines:**

| Document | Rules |
|---|---|
| `AGENTS.md` | Keep as a map, not a full spec. Update tech stack, directory structure, or core rules only when truly changed. |
| `ARCHITECTURE.md` | Add new domain sections for new modules, update dependency directions, adjust diagrams. |
| `docs/design-docs/*` | If implementation diverged from design, add "Current Implementation" / "Changes" notes or mark as `superseded`. |
| `docs/product-specs/*` | Adjust status and behavior descriptions when the implementation changed. |
| `docs/FRONTEND.md` | Update routing, component structure, and state management sections when FE architecture changes. |

**Don't:**
- Don't refactor documents unrelated to the changes
- Don't write documentation based on assumptions (only what's confirmed in code)
- Don't generate CHANGELOG entries (use commit convention)

#### Step 6: Verify Consistency

After all updates, perform a full consistency check:

1. Check that all links in `AGENTS.md` point to real files
2. Ensure `docs/design-docs/index.md` lists all existing design docs
3. Ensure `docs/product-specs/index.md` lists all existing product specs
4. Detect broken links across all documentation files
5. Sync TODO/FIXME with tech-debt tracker (if it exists):

```bash
grep -rn 'TODO\|FIXME\|HACK\|XXX\|WORKAROUND' \
  --include='*.ts' --include='*.tsx' --include='*.js' --include='*.jsx' \
  --include='*.py' --include='*.go' --include='*.rs' --include='*.java' \
  --include='*.rb' --include='*.ex' --include='*.exs' \
  . 2>/dev/null | grep -v node_modules | grep -v .git | head -50
```

Compare against `docs/exec-plans/tech-debt-tracker.md` (if it exists):
- Newly detected items → add to **Active Debt**
- Items that disappeared from code → move to **Resolved Debt**

#### Step 7: Report Results

After completion, produce a summary in this format:

```
## Sync Results

Changed code files: N
Detected change types: <high-level categories>

### Updated Documents
- `ARCHITECTURE.md` — updated "payments" domain dependencies
- `docs/FRONTEND.md` — updated IPC patterns section

### Reviewed but No Changes Needed
- `AGENTS.md` — structure and tech stack unchanged

### Newly Created
- `docs/features/xxx.md` — new feature documentation

### Consistency Issues
- (broken links, missing index entries, etc.)

### Needs Human Review
- `docs/product-specs/checkout.md` — verify that description matches new implementation
```

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
