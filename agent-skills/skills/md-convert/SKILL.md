---
name: md-convert
description: Convert a non-Markdown source file — PDF, DOCX, PPTX, XLSX, HTML, EPUB, CSV, JSON, XML, ZIP, image, audio, or YouTube URL — into Markdown via Microsoft's markitdown library. PROACTIVELY invoke this skill whenever you or another skill needs to read, quote, summarize, extract, analyze, or otherwise process the textual contents of a non-Markdown file — do not wait for the user to say "markdown" or "convert". Implicit triggers include requests like "read this PDF", "extract this slide deck", "summarize this document", "what does this file say", "이 파일 분석해줘", "이 PDF 내용 정리해줘", as well as any upstream skill (lecture-material-digest, exam-cram-sheet, assignment-solver for non-bundled formats, etc.) whose input is a non-Markdown file that must be text-analyzed. Treat this skill as the default preprocessing step for any non-Markdown source before downstream reasoning. Skip only when the source is already Markdown/plain-text, or when the upstream skill has its own bundled extractor for that specific format.
---

# md-convert

## Goal

입력 파일 하나를 `markitdown`으로 Markdown으로 변환하여 `.md`로 저장한다. 이 스킬은 다른 스킬이 전처리 단계로 호출하는 것을 주 용도로 한다.

## Input Contract

- **필수:** 입력 경로 또는 URL (`<input>`)
- **선택:** 출력 경로 (`--output <path>`). 미지정 시 입력과 같은 폴더에 동일 파일명 + `.md`로 저장
- **선택:** `--stdout` — 파일 저장 대신 stdout으로 Markdown 문자열 반환

## Procedure

1. 의존성 확인: `markitdown`이 설치돼 있지 않으면 스크립트가 exit code 3으로 종료하며 설치 명령을 안내한다. 사용자에게 `pip install 'markitdown[all]'` 실행을 요청하라.
2. 변환 실행:
   ```bash
   python3 scripts/convert.py <input> [--output <path>] [--stdout]
   ```
3. 성공 시 stdout에 출력 파일 경로가 출력된다. 이 경로를 호출자 스킬로 반환하거나 다음 단계에서 사용한다.
4. 실패 시 exit code로 원인을 구분한다(아래 참조).

## Output Contract

- 파일 저장 모드(기본): stdout에 `.md` 파일 경로 한 줄.
- `--stdout` 모드: stdout에 변환된 Markdown 전문.
- 에러: stderr에 한 줄 진단 메시지, 아래 exit code 중 하나.

## Exit Codes

| Code | 의미 |
|---|---|
| 0 | 성공 |
| 2 | 사용법 오류 (`--stdout`와 `--output` 동시 지정 등) |
| 3 | `markitdown` 미설치 |
| 4 | 입력 파일 없음 |
| 5 | 변환 실패 |

## Usage from Other Skills

다른 스킬이 이 스킬에 위임할 때의 호출 예시:

```bash
# PDF → same-folder .md
python3 agent-skills/skills/md-convert/scripts/convert.py /path/to/slide.pdf

# PPTX → specific output path
python3 agent-skills/skills/md-convert/scripts/convert.py \
    /path/to/deck.pptx --output /tmp/deck.md

# HTML → stdout (for in-memory use)
python3 agent-skills/skills/md-convert/scripts/convert.py \
    /path/to/page.html --stdout
```

호출자 스킬은 stdout에 출력된 경로 또는 Markdown 텍스트를 그대로 다음 단계 입력으로 사용한다.

## Guardrails

- 이 스킬은 "파일 → Markdown" 변환에만 책임을 진다. 요약/재구성/번역 같은 콘텐츠 가공은 하지 않는다.
- 기존 출력 파일이 있으면 덮어쓴다. 호출자가 보존이 필요하면 `--output`으로 다른 경로를 명시하라.
- 암호화 PDF, 빈 오디오, 잘못된 ZIP 등은 exit code 5로 실패한다. 그 경우 원인을 그대로 호출자에 전달하고 자체 재시도/복구를 하지 않는다.
- `markitdown`이 내부적으로 LLM/Azure Document Intelligence를 호출하도록 구성하는 옵션은 이 스킬에서 노출하지 않는다(단순 로컬 변환 범위로 한정).

## Troubleshooting

실행 중 아래 증상 중 하나라도 나타나면 `references/gotchas.md`를 읽고 해당 항목의 대응을 적용한다:

- exit code 3 (`markitdown` 미설치) 또는 `pip install`이 PEP 668 / `externally-managed-environment` 에러로 실패
- `pip install` 중 `youtube-transcript-api` 같은 의존성 resolver 실패, 또는 `markitdown 0.0.2`만 설치되는 현상 (Python 3.14 환경)
- stderr에 `Couldn't find ffmpeg or avconv` RuntimeWarning 출력 (오디오 변환이 아니면 무시 가능하나 사용자가 우려하면 대응)

`references/gotchas.md`는 호출자 스킬이 참고할 수 있는 "exit code → 원인 → 수정 절차" 카탈로그로 관리한다. 새로운 재현 가능한 실패 유형을 만나면 즉시 이 문서에 추가한다.
