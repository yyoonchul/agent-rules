---
name: lecture-material-digest
description: Read one lecture material file (for example PDF/PPT/PPTX) and generate one Markdown digest file in the same folder using the source title + " digest" filename pattern. Use when the user asks for an exam-focused concept digest from lecture materials. Do not use for multi-file batch processing.
---

# Lecture Material Digest

## Goal

Create one exam-focused digest Markdown file from exactly one lecture material file.

- Output filename: source title + ` digest.md`
- Content policy: keep all technical terms exactly in English, and write only explanations in concise Korean
- Coverage policy: thoroughly include the lecture's major concepts and likely exam concepts

## Inputs

- Lecture material file (required): one mentioned file such as `pdf`, `ppt`, `pptx`
- Optional focus hints (optional): user-provided emphasis (for example, "midterm", "calculation-heavy")

If multiple files are mentioned, ask the user to select one file for this invocation.

## Procedure

1. Validate scope and file path.
- Accept exactly one lecture material file.
- Confirm the path exists and is a file.

2. Extract readable content from the source.
- Read text directly when possible.
- For slide/PDF formats, extract text from the file content available in the environment.
- If extraction quality is low, continue with explicit uncertainty notes instead of fabricating details.

3. Apply digest instructions and template.
- Follow `references/work-instructions.md`.
- Format output with `references/digest-template.md`.

4. Build concept-complete digest.
- Enumerate all major concepts from the material.
- Preserve key terms exactly as written in English.
- Explain each concept briefly in Korean.
- Mark likely exam points with priority (`High`, `Medium`, `Low`) and rationale in concise Korean.

5. Save artifact.
- Save in the same directory as the source file.
- Let `title` be the source basename without extension.
- Base output: `<title> digest.md`.
- If collision exists, use `<title> digest (2).md`, then `(3)`, etc.

## Output Contract

- Summary: what was digested and exam-focus strategy
- Artifact: exact saved file path
- Validation: whether filename collision numbering was used
- Follow-up: only if source extraction uncertainty materially affects digest quality

## Resource Routing

- Work instructions: `references/work-instructions.md`
- Digest template: `references/digest-template.md`

## Guardrails

- Process one lecture material file per invocation only.
- Do not translate or paraphrase source technical terms away from English.
- Keep Korean explanations concise and exam-relevant.
- Do not invent slide content that cannot be extracted from source.
