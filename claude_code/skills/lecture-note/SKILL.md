---
name: lecture-note
description: Transform one mentioned transcript markdown file into one merged lecture-note markdown file in the same folder. Use when the user asks to create structured lecture notes from a prepared transcript. Keep transcript cleanup loose and preserve the original text as much as possible.
argument-hint: "[transcript_path]"
disable-model-invocation: true
user-invocable: true
---

# Goal

Generate one merged Markdown artifact from exactly one transcript Markdown file:

- Top: structured lecture note
- Divider: `---`
- Bottom: lightly cleaned transcript

# Inputs

- Primary input: `$ARGUMENTS`
- Optional positional inputs:
  - `$0`: `transcript_path` (required)

If argument shape is unclear, resolve the transcript path from mentioned files and user context.

# Workflow

1. Validate input scope.
- Accept exactly one transcript file.
- Confirm the path exists and is a Markdown file.

2. Load separated references.
- Apply instructions from `references/work-instructions.md`.
- Format the note with `references/lecture-note-template.md`.

3. Build cleaned transcript (loose cleanup).
- Remove obvious STT noise (`inaudible`-like artifacts, repeated filler bursts, repeated characters).
- Preserve original meaning and wording order whenever possible.

4. Build structured lecture note.
- Fill all template sections from transcript context.
- Keep emphasized professor points explicit.

5. Save merged output.
- Compose:
  - structured note
  - `---`
  - cleaned transcript
- Save in transcript's folder.
- Filename: local KST date `YYMMDD.md`.
- If exists, save as `YYMMDD (2).md`, then `(3)`, etc.

# Output Format

- Summary: what was cleaned and organized
- Changes: exact output path
- Validation: whether collision numbering was used
- Next actions: only if unresolved transcript ambiguity materially affects note quality

# Additional Resources

- Work instructions: `references/work-instructions.md`
- Note template: `references/lecture-note-template.md`

# Guardrails

- Process one transcript file per invocation only.
- Avoid heavy rewriting; apply minimal cleanup.
- Keep unresolved ambiguities visible in the note.
- Always output one merged Markdown file.
