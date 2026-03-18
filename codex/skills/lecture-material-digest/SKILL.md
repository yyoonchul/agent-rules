---
name: lecture-material-digest
description: Read one or more lecture material files (for example PDF/PPT/PPTX) and generate one Markdown digest file per source in the same folder using the source title + "_ digest" filename pattern. Use when the user asks for understanding-focused concept explanations from lecture materials, including sequential processing across multiple files.
---

# Lecture Material Digest

## Goal

Create understanding-focused digest Markdown files from lecture material files.

- Output filename: source title + `_ digest.md` (one file per source)
- Content policy: keep all technical terms exactly in English, and write explanations in clear Korean with enough detail for understanding
- Coverage policy: thoroughly include the lecture's major concepts and explain what they are, why they matter, and how they connect

## Inputs

- Lecture material file(s) (required): one or more mentioned files such as `pdf`, `ppt`, `pptx`
- Optional focus hints (optional): user-provided emphasis (for example, "기초부터", "수식 위주", "직관 중심")

If multiple files are mentioned, process them sequentially in the user-mentioned order unless the user specifies a different order.

## Procedure

1. Validate scope and file path.
- Accept one or more lecture material files.
- Confirm each path exists and is a file.

2. Extract readable content from each source.
- Read text directly when possible.
- For slide/PDF formats, extract text from the file content available in the environment.
- If extraction quality is low, continue with explicit uncertainty notes instead of fabricating details.

3. Apply digest instructions and template.
- Follow `references/work-instructions.md`.
- Format output with `references/digest-template.md`.

4. Build concept-complete digest per source.
- Enumerate all major concepts from each material.
- Preserve key terms exactly as written in English.
- Explain each concept in detail so the reader can understand without re-reading the slide.
- For each major concept, include at least: definition, importance/background, mechanism or flow, and an intuitive example or analogy.
- Explicitly connect related concepts and call out common confusion points.

5. Save artifacts.
- For each source, save in the same directory as that source file.
- Let `title` be each source basename without extension.
- Base output: `<title>_ digest.md`.
- If collision exists, use `<title>_ digest (2).md`, then `(3)`, etc.

## Output Contract

- Summary: what was explained and learning-focused strategy
- Artifact: exact saved file path(s)
- Validation: whether filename collision numbering was used for any artifact
- Follow-up: only if extraction uncertainty for any source materially affects digest quality

## Resource Routing

- Work instructions: `references/work-instructions.md`
- Digest template: `references/digest-template.md`

## Guardrails

- Process one or more lecture material files sequentially; create a separate digest per source.
- Do not translate or paraphrase source technical terms away from English.
- Prioritize reader understanding over brevity; avoid shallow summary-only output.
- Do not invent slide content that cannot be extracted from source.
