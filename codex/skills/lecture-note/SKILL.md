---
name: lecture-note
description: Transform one mentioned lecture transcript markdown file into a structured lecture note and save a merged output file in the same folder. Use when the user asks to create lecture notes from an existing transcript file. Keep transcript cleanup loose and preserve original wording as much as possible.
---

# Lecture Note

## Goal

Generate one merged Markdown artifact from one transcript Markdown file:

- Top: structured lecture note
- Divider: `---`
- Bottom: lightly cleaned transcript

## Inputs

- Transcript file (required): one mentioned Markdown transcript file

Optional values inferred from user request:
- Output date naming preference (default fixed by this skill)
- Extra focus points for the note (exam, assignment, etc.)

## Procedure

1. Validate scope and input.
- Accept exactly one transcript file.
- Confirm the path exists and is a Markdown file.

2. Load separated references.
- Read `references/work-instructions.md` and follow it for cleanup behavior.
- Read `references/lecture-note-template.md` and use it as the note output template.

3. Create a lightly cleaned transcript.
- Remove or normalize obvious STT noise such as `inaudible`-type fragments, repeated filler bursts, and accidental repeated characters.
- Keep edits loose and minimal; preserve wording/order whenever possible.

4. Create the structured lecture note from the cleaned transcript.
- Fill all template sections.
- Keep core terminology and emphasized points explicit.

5. Build merged output and save.
- Compose one Markdown file as:
  - Structured note
  - `---`
  - Cleaned transcript
- Save in the same directory as the transcript.
- Filename must use local KST date: `YYMMDD.md`.
- If filename exists, use `YYMMDD (2).md`, then `(3)`, etc.

## Output Contract

- Summary: what was cleaned and how the note was structured
- Artifact: exact saved file path
- Validation: whether collision numbering was used
- Follow-up: only if a specific ambiguous section needs user confirmation

## Resource Routing

- Work instructions: `references/work-instructions.md`
- Note template: `references/lecture-note-template.md`

## Guardrails

- Process one transcript file per invocation only.
- Do not over-edit transcript content; prefer minimal correction.
- Do not omit explicit uncertainty; keep unclear parts visible in note sections.
- Always output a single merged Markdown file.
