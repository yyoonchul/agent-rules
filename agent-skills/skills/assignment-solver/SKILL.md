---
name: assignment-solver
description: Solve one assignment problem file using a single endpoint with two logical tracks: (A) Math/Physics PDF problem solving (lecture slides/lecture notes as ground truth) and (B) code artifact generation. Save a final answer with detailed explanation next to the problem file.
---

# Assignment Solver

## Goal

Produce a high-quality solution artifact for exactly one assignment problem file, using a single endpoint with track-specific instructions:

- Track A (Math/Physics PDF Solver): strict ground-truth-based solving with lecture slides/lecture notes.
- Track B (Code Results Generator): generate code artifacts and companion explanations.

- Required outcome: final answer + detailed explanation
- Default output: Markdown file
- Optional output: a non-Markdown format only when the user explicitly requests it
- If the requested output is code (or a folder containing code), also generate a companion Markdown document summarizing assignment overview, evidence, concepts used, and sources from lecture slides/assignment materials

## Inputs

- Problem file (required): one file containing the assignment question
- Reference paths (optional): zero or more files/folders (lecture slides, textbook notes, course folders, etc.)
- Output format (optional): file extension such as `md`, `py`, `js`, `java`, `txt`

If output format is not explicitly requested, use `md`.

## Track Selection (Single Endpoint)
After extracting the problem text, the skill must choose exactly one track:

1. Use Track A (Math/Physics PDF Solver) when:
   - The problem file is a `.pdf`, AND
   - The extracted problem content indicates a math/physics question or concept (e.g., equations, variables, units, derivations, “Problem/Exercise” style statement), AND
   - The user intent is to solve/explain/derive (e.g., “풀이”, “해설”, “계산”, “유도”).
2. Use Track B (Code Results Generator) when:
   - The user explicitly requests code/scripts (e.g., “write code”, “implement”, “generate script”, or the requested output format is a code file extension), OR
   - The extracted problem is primarily about software/tooling/code output rather than a math/physics derivation.
3. Ambiguity handling:
   - Prefer Track A when the extracted problem text contains clear equations/units/derivation structure.
   - Otherwise prefer Track B.

## Procedure

1. Validate inputs.
- Ensure exactly one problem file is selected.
- Ensure the problem path exists and is a file.

2. Extract the problem file text and gather context from local references when provided.
- Extract the problem file text.
  - If the problem file is `.pdf`, `.pptx`, or `.ppt`, use the bundled extractor at `scripts/extract_reference_text.py` resolved relative to this `SKILL.md`.
  - For other problem file types, read the text directly.
- Read directly mentioned reference files.
- For referenced folders, recursively scan and prioritize relevant text-like files first.
- When a lecture or reference file is `.pdf`, `.pptx`, or `.ppt`, use the bundled extractor at `scripts/extract_reference_text.py` resolved relative to this `SKILL.md`.
- The bundled extractor already includes the required runtime modules under `vendor/`; do not install packages in the assignment/project folder at execution time.
- Format routing is fixed:
  - `.pdf` -> bundled `pypdf`
  - `.pptx` -> bundled extractor's standard-library ZIP/XML parser
  - `.ppt` -> bundled `olefile` + binary PowerPoint text-record parser
- Include PDF/PPTX/PPT sources when extractable.
- Prefer relevance over volume: select files by filename/path keywords and problem-topic matching.

3. Decide track and fill knowledge gaps (track-specific).
- First, apply the track decision rules in `## Track Selection (Single Endpoint)`.
- Track A (Math/Physics PDF Solver):
  - Ground truth priority: treat the project files’ lecture slides and lecture notes/transcripts as the primary ground truth for any concept/formula/definition used in the answer.
  - In `## 상세 풀이`, always explain the most relevant chapter's core concepts and formulas first, then substitute/apply them to the specific given problem, with a detailed step-by-step 풀이.
  - Professional terms/concepts mentioned in the lecture slides/assignment must be kept in English exactly as written; explain them only in Korean.
  - If the needed ground-truth chapter/material is not found locally, clearly state what is missing and either ask for additional reference files or use web research only as a clearly labeled fallback with explicit uncertainty.
  - If web research is used, reflect it in `## 출처 링크` and clearly separate it from local ground truth in `## 참고 근거 (로컬 파일/섹션)`.
- Track B (Code Results Generator):
  - Use local references first; if absent or insufficient, web research is allowed.
  - Combine gathered evidence with generally known domain knowledge and explicit reasoning.

### Bundled Lecture Material Extraction

Use the following command pattern for bundled lecture material extraction:

```bash
python3 "<skill-dir>/scripts/extract_reference_text.py" "<reference-file>"
```

Rules:

- Resolve `<skill-dir>` as the directory containing this `SKILL.md`.
- Supported bundled formats are only `.pdf`, `.pptx`, and `.ppt`.
- Treat `.ppt` extraction as text-focused best effort. If the extracted text is sparse or noisy, say so in the final artifact and compensate with other references or web research.
- If a file in one of these formats fails extraction, report the failure explicitly instead of silently skipping it.

### Optional PDF page OCR (agent judgment)

When **bundled text extraction** (`scripts/extract_reference_text.py`) is insufficient for a `.pdf`, the agent may run **page-level OCR** using the separate tool below. Do **not** run OCR by default; use it only when justified.

**When to consider OCR**

- Extraction raises `no extractable text found in PDF`, or
- Per-page extracted text is clearly too sparse for the visible content (e.g. scan/image-only slides, figures with critical labels), or
- The problem statement clearly depends on content that is unlikely to be text-layered.

**Command pattern**

```bash
python3 "<skill-dir>/scripts/extract_pdf_page_ocr.py" --page N "<path-to.pdf>"
# or multiple pages / ranges (1-based):
python3 "<skill-dir>/scripts/extract_pdf_page_ocr.py" --pages "1,3-5" "<path-to.pdf>"
# optional: tesseract language(s), default is eng+kor
python3 "<skill-dir>/scripts/extract_pdf_page_ocr.py" --page N --lang eng "<path-to.pdf>"
```

**Rules**

- Resolve `<skill-dir>` as the directory containing this `SKILL.md`.
- OCR output is **less reliable** than native PDF text; treat it as approximate.
- In the solution artifact, label OCR-derived content explicitly (e.g. in `## 참고 근거 (로컬 파일/섹션)` or `## 가정 및 불확실성`): note **OCR**, **page number(s)**, and **uncertainty** (misread symbols, equations, diagrams).
- If OCR cannot run (missing `tesseract`, renderer, or languages), report the error message to the user and fall back to asking for alternate materials or other allowed strategies—do not invent PDF content.

**Runtime prerequisites** (not bundled; see `vendor/README.md`): `tesseract` on PATH; plus **either** Poppler (`pdftoppm`) **or** an importable **PyMuPDF** (`fitz`) in the Python environment used to run the script.

4. Build the solution content.
- Detect and follow the language of the problem file.
- Provide the final answer first, then step-by-step explanation.
- If information is incomplete, continue with explicit assumptions and uncertainty notes.
- Track A (Math/Physics PDF Solver) writing rules:
  - In `## 상세 풀이`, use the explicit flow: `핵심 개념` -> `핵심 공식/Equations` -> `대입/적용` -> detailed step-by-step 풀이.
  - When writing equations in Track A, use LaTeX math blocks in the requested formats: `$...$` (single-line/inline) or `$$` + newline + equation + newline + `$$` (multi-line block).
  - Keep lecture-assigned professional terms/concepts in English exactly as written; explain them only in Korean.
  - Prefer local evidence for each concept/formula; when showing a formula, briefly indicate the source ground-truth evidence in `## 참고 근거 (로컬 파일/섹션)` (no fabricated citations).
- Track B (Code Results Generator) writing rules:
  - If the output is code, include the code blocks and a brief run/use note when applicable.

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

Track A (Math/Physics PDF Solver) additional requirement:
- In `## 상세 풀이`, start with the relevant chapter's key concepts and formulas first, then apply/substitute them to the specific given problem, and include detailed step-by-step derivation. Professional terms/concepts must keep their English wording exactly as in the lecture slides.

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
