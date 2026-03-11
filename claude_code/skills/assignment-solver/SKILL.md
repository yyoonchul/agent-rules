---
name: assignment-solver
description: Solve one assignment problem file and save an answer artifact next to the problem file. Use when a user provides a problem file and asks for a full solution with explanation, with optional reference files/folders. If references are missing or insufficient, use web research plus general knowledge. Do not use for batch multi-problem solving.
argument-hint: "[problem_path] [reference_paths(optional; comma-separated)] [output_format(optional; default=md)]"
disable-model-invocation: true
user-invocable: true
---

# Goal

Create a solution file for exactly one assignment problem file.

- Default output: Markdown
- Alternative output: only when explicitly requested by the user (for example, `py`, `js`, `java`, `txt`)

# Inputs

- Primary input: `$ARGUMENTS`
- Optional positional inputs:
  - `$0`: `problem_path` (required)
  - `$1`: `reference_paths` (optional; comma-separated files/folders)
  - `$2`: `output_format` (optional; defaults to `md`)

If arguments are not fully structured, extract equivalent values from the user's message and mentioned paths.

# Workflow

1. Validate input scope.
- Accept exactly one problem file.
- Confirm the problem path exists and is a file.

2. Collect local context when references are provided.
- Read explicitly mentioned files.
- If a folder is provided, recursively scan and select relevant files.
- Prioritize text-like content and include PDF when extractable.

3. Resolve missing context.
- If references are absent or insufficient, run web research.
- Use general knowledge and explicit reasoning to bridge gaps.

4. Draft the solution.
- Detect problem language and match output language.
- Provide final answer first, then detailed step-by-step explanation.
- If data is incomplete, proceed with clearly labeled assumptions and uncertainty.

5. Save artifact.
- Compute `stem` from problem filename (without extension).
- Compute `ext` from requested output format; fallback to `md` if invalid or missing.
- Save in the same directory as the problem file using:
  - `<stem> sol.<ext>`
  - if collision, `<stem> sol (2).<ext>`, then `(3)`, etc.

6. Enforce output format policy.
- For `md`, use the required section order below.
- For non-`md`, return only requested format and embed concise explanation/assumptions in a format-appropriate way (comments for code).

# Required Markdown Structure

1. `## 과제 개요`
2. `## 최종 답안`
3. `## 상세 풀이`
4. `## 참고 근거 (로컬 파일/섹션)`
5. `## 출처 링크` (only when web research was used)
6. `## 가정 및 불확실성`

# Output Format

- Summary: what was solved and what sources were used
- Changes: exact saved file path and selected extension
- Validation: whether collision numbering was applied
- Next actions: optional only when useful

# Guardrails

- One problem file per invocation only.
- Do not fabricate references or web sources.
- Keep assumptions explicit when evidence is incomplete.
- Do not switch away from Markdown unless explicitly requested.
