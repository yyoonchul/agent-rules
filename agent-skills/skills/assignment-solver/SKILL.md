---
name: assignment-solver
description: Solve one assignment problem file and save a final answer with detailed explanation next to the problem file. Use when the user asks to generate a solution artifact from a mentioned problem file, optionally with reference files/folders. If references are missing or insufficient, use web research plus general knowledge. Do not use for multi-problem batch processing.
---

# Assignment Solver

## Goal

Produce a high-quality solution artifact for exactly one assignment problem file.

- Required outcome: final answer + detailed explanation
- Default output: Markdown file
- Optional output: a non-Markdown format only when the user explicitly requests it
- If the requested output is code (or a folder containing code), also generate a companion Markdown document summarizing assignment overview, evidence, concepts used, and sources from lecture slides/assignment materials

## Inputs

- Problem file (required): one file containing the assignment question
- Reference paths (optional): zero or more files/folders (lecture slides, textbook notes, course folders, etc.)
- Output format (optional): file extension such as `md`, `py`, `js`, `java`, `txt`

If output format is not explicitly requested, use `md`.

## Procedure

1. Validate inputs.
- Ensure exactly one problem file is selected.
- Ensure the problem path exists and is a file.

2. Gather context from local references when provided.
- Read directly mentioned reference files.
- For referenced folders, recursively scan and prioritize relevant text-like files first.
- Include PDF sources when extractable.
- Prefer relevance over volume: select files by filename/path keywords and problem-topic matching.

3. Fill knowledge gaps.
- If references are absent or insufficient, perform web research.
- Combine web findings with generally known domain knowledge and explicit reasoning.

4. Build the solution content.
- Detect and follow the language of the problem file.
- Provide the final answer first, then step-by-step explanation.
- If information is incomplete, continue with explicit assumptions and uncertainty notes.

5. Decide output filename and save.
- Let `stem` be the problem file basename without extension.
- Let `ext` be requested format; if missing or invalid, fall back to `md`.
- Base filename: `<stem> sol.<ext>` in the same folder as the problem file.
- Collision handling: if file exists, create `<stem> sol (2).<ext>`, then `(3)`, etc.

6. Enforce output structure.
- For `md`, use the required Markdown structure below.
- For non-`md`, generate the requested format artifact.
- If the requested format is code or a code-containing folder, also generate a companion Markdown file next to the output (base name: `<stem> sol notes.md`, with the same collision handling rule).
- The companion Markdown must organize references and sources specifically from lecture slides and assignment materials.

## Required Markdown Structure

When output format is `md`, include sections in this order:

1. `## 과제 개요`
2. `## 최종 답안`
3. `## 상세 풀이`
4. `## 참고 근거 (로컬 파일/섹션)`
5. `## 출처 링크` (only if web research was used)
6. `## 가정 및 불확실성`

## Companion Markdown for Code/Folder Outputs

When the output is code (for example `py`, `js`, `java`, etc.) or a folder containing code, create an additional Markdown file with these sections in order:

1. `## 과제 개요`
2. `## 참고 근거 (강의 슬라이드/과제 자료)`
3. `## 사용된 개념 설명`
4. `## 출처 (강의 슬라이드/과제 자료)`

Rules:

- Prefer local lecture slides and assignment handouts/materials as primary evidence.
- If a referenced source was not used directly, do not list it.
- Keep mappings explicit: concept -> which slide/material supports it.

## Output Contract

- Summary: what was solved and which strategy was used (local references, web, or mixed)
- Artifact: exact saved file path(s) (include companion Markdown path when created)
- Validation: note whether filename collision handling was applied
- Follow-up: suggest additional checks only when materially helpful

## Guardrails

- Process exactly one problem file per invocation.
- Do not silently skip uncertainty; state assumptions and confidence limits.
- Do not fabricate local citations; only cite files/sections actually used.
- Do not change output format unless explicitly requested by the user.
