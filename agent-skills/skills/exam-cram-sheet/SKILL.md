---
name: exam-cram-sheet
description: Reverse-engineer past exams, quizzes, homework, and example problems in a given exam-prep folder to produce one Markdown "필수 암기 정리" study document saved in that folder. The output is a self-contained study artifact — deep enough to begin studying from scratch, not a bullet-list cheatsheet. Use when the user asks to create a 시험 필수암기 정리 / exam must-memorize summary from a midterm/final folder that bundles lecture digests, past quizzes, HW, and example problems.
---

# Exam Cram Sheet

## Goal

Produce one Markdown study document that is **both** (a) a reverse-engineered forecast of what the exam will ask and (b) a **self-contained explanation deep enough to start studying from zero**. This is not a bullet-list cheatsheet. For every concept kept in scope, the reader should finish the section understanding *what it is, why it exists, how it works, and where the common pitfalls live* — without opening the source digest.

The reverse-engineering layer decides **what to include**; the explanation layer decides **how much detail each item gets**. Both layers are required.

- Output filename: `시험_필수암기_정리.md` (one file per invocation)
- Output location: the same folder that was passed in as the target
- Content policy: keep technical terms, model/formula names, flags, and function signatures in English; write explanations in Korean
- Math policy: use KaTeX-compatible blocks — inline `$...$`, block `$$\n...\n$$`

## Inputs

- Target folder (required): one folder (for example `.../과목명/midterm/`) that gathers all exam-scope materials
- Optional scope hints (optional): user-provided emphasis such as specific chapters, scope restrictions, or 과목 이름

If the user does not specify a folder, ask them to confirm the path before proceeding.

## Procedure

1. Validate scope and folder.
- Confirm the target path exists and is a directory.
- List its contents (one level; descend into subfolders only when clearly part of the exam scope, e.g. `hw1/`, `예상문제_이미지/`).
- If `시험_필수암기_정리.md` already exists, confirm whether to overwrite or save as a collision-numbered filename.

2. Classify source artifacts.
- **Lecture materials** (chapter slides/PDFs, `lecture-notes/`, and any `*_ digest.md` that happens to exist): the concept universe. Treat as ground truth for definitions/formulas. Digests are optional — do **not** assume they exist and do **not** ask the user to create them before proceeding.
- **Past quizzes / sample midterms / final exams** (`Quiz*`, `sample_midterm*`, `*_Answer*`, `기출*`): the primary reverse-engineering source — defines what is actually asked.
- **Homework / 과제** (`HW*`, `hw*`): secondary reverse-engineering source — reveals computation patterns and numeric-answer formats.
- **Example / 예제 / 예상 problems** (`예제문제*`, `예상문제*`, `연습문제*`): tertiary source — reveals likely problem archetypes even when no past exam exists.
- For any non-Markdown source (`pdf` / `pptx` / `ppt` / `docx` / `xlsx` / `html` / image / etc.), **default to delegating extraction to the sibling `md-convert` skill** — this is the primary path because digest markdown is typically absent:
  ```bash
  python3 agent-skills/skills/md-convert/scripts/convert.py "<source>" --stdout
  ```
  Use the returned Markdown as the concept/problem source. Only when a sibling `*_ digest.md` already exists next to the source (rare), you may use it as-is and skip conversion for that specific file. If `md-convert` fails, see `agent-skills/skills/md-convert/references/gotchas.md`; if recovery isn't possible, report the specific source that failed and continue with the remaining extractable materials — do not silently skip non-Markdown sources.

3. Reverse-engineer the exam pattern.
- Enumerate every problem found in quizzes, sample exams, HW, and example sets. For each, record: topic/chapter, problem type (T/F, fill-in, trace, derivation, 서술형, design), keywords, difficulty.
- Collapse repeats into **problem archetypes** and rank by frequency.
- Identify **repeated traps** (same misconception punished twice across quizzes/HW → near-certain exam trap).
- Identify **must-derive proofs / flows** (anything a past exam or sample exam asked to derive end-to-end).

4. Apply the cram-sheet template and work instructions.
- Follow `references/work-instructions.md`.
- Format output with `references/cram-sheet-template.md`.

5. Write the content — prose-depth in Section 2, terse in the summary sections.
- Section 1 · 시험 출제 패턴 — table of observed problem types with evidence pointers (e.g. "Q1-4", "Sample P2", "HW1 P5"), plus 2–5 inferred patterns and an exam-day "말할 수 있어야 하는 것" checklist.
- **Section 2 · 챕터별 필수 암기 (이 문서의 본체, 전체 분량의 약 70%)** — for each chapter inside scope, write a **self-teaching explanation**, not a list. Structure:
  - `#### 큰 그림` — 3~6 문장. "이 챕터가 왜 존재하는가, 어떤 도구 세트를 주는가, 이전/이후 챕터와 어떻게 이어지는가."
  - `#### 핵심 개념` — 개념마다 **(n) 제목** 아래 다음 요소를 **모두** 포함:
    - **정의**: 용어를 처음 보는 사람도 읽을 수 있는 한국어 정의 (1~3문장).
    - **핵심 수식 / 공식 / 시그니처**: KaTeX 블록. 수식 뒤에는 **기호 풀이**를 반드시 — 각 기호가 무엇이고, 단위/차원/기본값/제약이 무엇인지.
    - **왜 그런가 (motivation / derivation sketch)**: "왜 이 공식이 이 형태인가", "왜 마이너스인가", "왜 $2\theta$인가" 같은 **질문을 스스로 제기하고 답한다**. 짧은 유도 스케치 또는 직관적 설명 포함.
    - **예시 / 비유**: 이해를 돕는 짧은 예시 또는 비유 (있으면 digest에서 가져오거나 직접 생성).
    - **헷갈리기 쉬운 포인트**: sign convention, 차원, 범위 등 시험에서 함정으로 쓰기 좋은 것.
    - **연결 개념**: 관련 English terms + 어느 개념과 이어지는지 한 줄.
    - **시험 근거**: 이 개념이 실제 등장한 past-exam/HW/example id — 없으면 생략 가능하지만 개념 자체는 과거 자료와 연결되어 있어야 포함.
  - `#### 암기 포인트` — 위 설명의 **압축 요약**만 체크박스로. 본문을 대체하지 말고, 본문을 이미 읽은 사람이 시험 직전에 스캔하는 용도.
  - 개념이 어려울수록 설명을 **더 길게** 쓴다. digest에서 한 줄이었더라도 시험 출제 가능성이 높다면 여기서는 문단으로 풀어 쓴다. 반대로 과거 자료가 전혀 다루지 않은 개념은 이 섹션에서 제외한다 (depth over breadth).
- Section 3 · 반드시 유도할 줄 알아야 할 수식 / 증명 — 유도형 과목에서만. 각 항목 3~6줄의 유도 흐름(전체 풀이가 아닌 **단계 + 핵심 변환 식**).
- Section 4 · 함정 포인트 TOP — ≥10. 표 행 하나하나가 "오해 진술 vs 올바른 답 vs 근거". 섹션 2에서 다룬 개념과 연동.
- Section 5 · 시험 직전 치트시트 — ≥15. 한 줄 공식/플래그/커맨드. Section 2의 본문 설명을 **압축**한 최후 스캔용. 여기서 새로운 개념을 처음 던지지 말 것.
- Section 6 · 시험장 전략 메모 (선택) — 서술형/유도형/T-F 답변 구조 팁.
- Section 7 · 시험 직전 체크리스트 (선택) — `반드시 암기 / 설명 연습 / 계산·트레이스 / 코드 빈칸 / 버그 이름` 등 과목 성격에 맞는 것만.

**분량 감각**: 섹션 2 한 챕터는 digest의 핵심 개념 분량과 비슷하거나 살짝 더 짧지만 **밀도는 같거나 더 높게**. 전체 문서가 과거 자료 없이도 시험 대비 1-shot 학습본으로 기능해야 한다.

6. Save artifact.
- Save to `<target-folder>/시험_필수암기_정리.md`.
- If a file with that name already exists and the user did not opt to overwrite, save as `시험_필수암기_정리 (2).md`, then `(3)`, etc.

## Output Contract

- Summary: which sources (digests, quizzes, HWs, examples) were actually used, and the dominant problem archetypes
- Artifact: exact saved file path
- Validation: whether filename collision numbering was used; whether any section was intentionally omitted (e.g. derivation section for a non-derivation course)
- Follow-up: only if critical extraction failed (e.g. a past exam PDF had no text layer and no sibling digest), so the user can supply it

## Resource Routing

- Work instructions: `references/work-instructions.md`
- Output template: `references/cram-sheet-template.md`

## Guardrails

- Produce exactly one cram sheet per invocation.
- Only claim "출제 가능성 높음" when backed by evidence in the folder — cite the exhibit (quiz number, HW problem, example number) inline.
- Do not translate or paraphrase source technical terms, formula names, function signatures, or flag constants away from English.
- Do not invent past exam problems or trap lists that are not traceable to folder contents; mark inferred items with `⚠️` and explain the inference.
- Do not modify any source file; write only the study document output.
- **Do not degenerate Section 2 into a bullet list.** Every kept concept needs prose-depth explanation (정의 + 기호 풀이 + 왜 그런가 + 함정). If a concept only deserves a bullet, remove it from Section 2 and push it to the Section 5 치트시트 instead.
- Do not merely paraphrase the digest; integrate the digest's explanation with the past-exam evidence so the reader sees both "무엇인가" and "시험에서 어떻게 물리는가".
- Tables, formulas, and checkboxes are tools for Sections 1/4/5/7; Section 2 is prose + formula + evidence.
