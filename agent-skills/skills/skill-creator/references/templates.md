# Reusable Templates for Skill Creation

## 1) Minimal `SKILL.md`

```markdown
---
name: your-skill-name
description: Use this skill when users ask for <trigger A>, <trigger B>, or tasks involving <context C>. It handles <core capability>.
---

# Your Skill Title

## Goal
- ...

## Procedure
1. ...
2. ...

## Guardrails
- ...
```

## 2) Extended `SKILL.md` skeleton

```markdown
---
name: your-skill-name
description: Use this skill when <user intent + trigger contexts>. It provides <capability>.
---

# <Skill Title>

## Goal
- Define what this skill must accomplish.

## Input Contract
- Required inputs
- Optional context

## Procedure
1. Analyze request intent.
2. Select default workflow.
3. Execute.
4. Validate.
5. Repair and re-validate if needed.

## Resource Routing
- `references/...` for domain details
- `scripts/...` for deterministic execution
- `assets/...` for output templates

## Output Contract
- Expected artifact format/path
- Required summary fields

## Guardrails
- Safety, scope, and non-goals
```

## 3) Skill folder scaffold

```text
<skill-name>/
├── SKILL.md
├── scripts/
│   └── <script files>
├── references/
│   └── <domain docs>
└── assets/
    └── <templates/resources>
```

## 4) Trigger eval query template

```json
[
  { "query": "<should trigger example 1>", "should_trigger": true },
  { "query": "<should trigger example 2>", "should_trigger": true },
  { "query": "<near-miss example 1>", "should_trigger": false },
  { "query": "<near-miss example 2>", "should_trigger": false }
]
```

## 5) Output eval template (`evals/evals.json`)

```json
{
  "skill_name": "<skill-name>",
  "evals": [
    {
      "id": 1,
      "prompt": "<realistic user prompt>",
      "expected_output": "<human-readable success criteria>",
      "files": ["evals/files/<input-file>"],
      "assertions": [
        "<verifiable assertion 1>",
        "<verifiable assertion 2>"
      ]
    }
  ]
}
```

## 6) Prompt-to-skill extraction template

```markdown
### Request Summary
- User goal:
- Constraints:
- Environment:

### Skill Design
- Skill name:
- Trigger description draft:
- Scope in:
- Scope out:

### Resource Plan
- scripts:
- references:
- assets:

### Validation Plan
- should-trigger prompts:
- should-not-trigger prompts:
- trigger success criteria:
- output success criteria:
```

## 7) Script usage template in `SKILL.md`

```markdown
## Available scripts
- `scripts/validate.py` — Validate intermediate outputs
- `scripts/run.py` — Execute main workflow

## Execution
1. Validate input:
   ```bash
   python3 scripts/validate.py --input "$INPUT"
   ```
2. Run main process:
   ```bash
   python3 scripts/run.py --input "$INPUT" --output "$OUTPUT"
   ```
3. Re-run validation on output and fix if needed.
```

## 8) Optional frontmatter template

```yaml
---
name: your-skill-name
description: Use this skill when <trigger>. It handles <capability>.
license: Apache-2.0
compatibility: Requires python3 and uv; network access may be needed for dependency install.
metadata:
  owner: your-team
  version: "0.1.0"
---
```

## 9) Post-create validation command

```bash
# Refresh unified skill list (always)
python3 scripts/update_skills_list.py

# Validate one new skill
python3 scripts/validate_skills.py --skill <skill-name>

# Validate all skills
python3 scripts/validate_skills.py
```
