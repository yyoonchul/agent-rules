---
name: lecture-material-digest
description: Read one lecture material file (for example PDF/PPT/PPTX) and create one Markdown digest in the same folder using the source title + " digest" filename pattern. Use when the user asks for exam-focused concept digestion from lecture slides/materials. Do not use for multi-file batch processing.
argument-hint: "[lecture_material_path] [focus(optional)]"
disable-model-invocation: true
user-invocable: true
---

# Goal

Generate one exam-focused digest Markdown file from exactly one lecture material file.

- Filename rule: source title + ` digest.md`
- Language rule: keep terms in English exactly as in source, write explanations only in concise Korean
- Coverage rule: include all major concepts and highlight likely exam concepts

# Inputs

- Primary input: `$ARGUMENTS`
- Optional positional inputs:
  - `$0`: `lecture_material_path` (required)
  - `$1`: `focus` (optional; exam/midterm/final/problem-solving emphasis)

If argument shape is unclear, resolve the source file from user-mentioned paths and context.

# Workflow

1. Validate input scope.
- Accept exactly one lecture material file.
- Confirm the path exists and is a file.

2. Extract readable source content.
- Read text directly when available.
- For `pdf`/`ppt`/`pptx`, extract text that can be obtained in the current environment.
- If extraction is partial, proceed with explicit uncertainty notes instead of hallucinating content.

3. Load separated references.
- Apply `references/work-instructions.md`.
- Format with `references/digest-template.md`.

4. Build digest content.
- Capture the full set of major concepts from the material.
- Keep key terms in original English form.
- Explain each concept briefly in Korean.
- Add exam priority (`High`/`Medium`/`Low`) with concise Korean rationale.

5. Save output file.
- Save in the source file directory.
- Let `title` be the source basename without extension.
- Base filename: `<title> digest.md`.
- On collision: `<title> digest (2).md`, then `(3)`, etc.

# Output Format

- Summary: what was digested and exam-focus strategy
- Changes: exact output file path
- Validation: whether collision numbering was used
- Next actions: only when extraction uncertainty materially impacts quality

# Additional Resources

- Work instructions: `references/work-instructions.md`
- Digest template: `references/digest-template.md`

# Guardrails

- Process one lecture material file per invocation only.
- Never translate core technical terms away from English.
- Keep explanations concise and exam-relevant in Korean.
- Do not invent unavailable source details.
