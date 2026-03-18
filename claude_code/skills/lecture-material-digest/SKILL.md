---
name: lecture-material-digest
description: Read one or more lecture material files (for example PDF/PPT/PPTX) and create one Markdown digest per source in the same folder using the source title + "_ digest" filename pattern. Use when the user asks for understanding-focused concept explanations from lecture slides/materials, including sequential processing across multiple files.
argument-hint: "[lecture_material_path ...] [focus(optional)]"
disable-model-invocation: true
user-invocable: true
---

# Goal

Generate understanding-focused digest Markdown files from lecture material files.

- Filename rule: source title + `_ digest.md` (one file per source)
- Language rule: keep terms in English exactly as in source, and explain in clear Korean with enough detail for understanding
- Coverage rule: include all major concepts and explain what they are, why they matter, and how they connect

# Inputs

- Primary input: `$ARGUMENTS`
- Optional positional inputs:
  - `$0`: `lecture_material_path` (required)
  - `$1`: `focus` (optional; 예: 기초부터, 직관 중심, 수식 위주)

If argument shape is unclear, resolve the source file from user-mentioned paths and context.

# Workflow

1. Validate input scope.
- Accept one or more lecture material files.
- Confirm each path exists and is a file.

If multiple files are provided, process them sequentially in user-mentioned order unless the user requests a different order.

2. Extract readable source content per file.
- Read text directly when available.
- For `pdf`/`ppt`/`pptx`, extract text that can be obtained in the current environment.
- If extraction is partial, proceed with explicit uncertainty notes instead of hallucinating content.

3. Load separated references.
- Apply `references/work-instructions.md`.
- Format with `references/digest-template.md`.

4. Build digest content per file.
- Capture the full set of major concepts from each material.
- Keep key terms in original English form.
- Explain each concept in detail so the reader can understand without re-reading the slide.
- For each major concept, include at least: definition, importance/background, mechanism or flow, and an intuitive example or analogy.
- Explicitly connect related concepts and call out common confusion points.

5. Save output files.
- For each source, save in the source file directory.
- Let `title` be each source basename without extension.
- Base filename: `<title>_ digest.md`.
- On collision: `<title>_ digest (2).md`, then `(3)`, etc.

# Output Format

- Summary: what was explained and learning-focused strategy
- Changes: exact output file path(s)
- Validation: whether collision numbering was used for any output
- Next actions: only when extraction uncertainty in any source materially impacts quality

# Additional Resources

- Work instructions: `references/work-instructions.md`
- Digest template: `references/digest-template.md`

# Guardrails

- Process one or more lecture material files sequentially; create a separate digest per source.
- Never translate core technical terms away from English.
- Prioritize reader understanding over brevity; avoid shallow summary-only output.
- Do not invent unavailable source details.
