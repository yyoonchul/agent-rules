---
name: skill-creator
description: Create or update Agent Skills for Claude Code, Codex, and other Agent Skills-compatible clients. Use when users ask to design a new skill, revise an existing skill, write SKILL.md, optimize skill triggering descriptions, or decide scripts/references/assets and folder structure from a prompt.
---

# Skill Creator

## Goal

사용자 프롬프트를 재사용 가능한 스킬로 변환한다.

- 공통 기준은 Agent Skills 스펙을 따르되, 기본은 최대 호환(`name`, `description`)으로 설계한다.
- 스킬은 즉시 실행 가능한 형태(폴더 구조 + `SKILL.md` + 필요한 리소스)로 만든다.

## Input Contract

최소 입력:

- 사용자 요청(무엇을 자동화/전문화하고 싶은지)

있으면 좋은 입력:

- 대상 클라이언트(Claude Code, Codex, VS Code Copilot 등)
- 사용 환경 제약(네트워크, 설치 가능 여부, OS)
- 샘플 프롬프트(트리거되어야 하는/되면 안 되는 예시)

## Procedure

1. 요청에서 **문제 범위**를 추출한다.
2. 한 스킬이 맡을 **책임 경계**를 정한다.
3. 스킬 이름을 규칙에 맞게 정한다.
4. `description`을 트리거 중심으로 작성한다.
   - 권장 문형: `Use this skill when ...`
   - 1024자 제한 내에서 사용자 의도/문맥 키워드를 포함한다.
5. 리소스 구조를 결정한다.
   - `scripts/`: 반복 코드/결정론적 실행이 필요할 때
   - `references/`: 상세 지식/정책/스키마가 필요할 때
   - `assets/`: 출력 산출물 템플릿/정적 리소스가 필요할 때
6. `SKILL.md` 본문을 절차 중심으로 작성한다.
   - 기본 경로(default)와 예외 분기만 남기고 메뉴식 나열을 피한다.
   - `SKILL.md`가 커지면 `references/`로 분리하고 읽는 조건을 명시한다.
7. 사용자 프롬프트에 대응 가능한지 점검한다.
   - should-trigger / should-not-trigger 관점으로 확인
8. 스킬 목록 문서를 최신화한다.
   - 항상 실행: `python3 scripts/update_skills_list.py`
9. 스펙 검증을 실행한다.
   - 새 스킬을 다 만든 뒤 한 번에 검증:
     - 단일 스킬: `python3 scripts/validate_skills.py --skill <skill-name>`
     - 전체 스킬: `python3 scripts/validate_skills.py`
10. 결과를 파일 단위로 정리해 제시한다.

## Resource Routing

- 공통 포맷/호환 규칙: `references/skill-format.md`
- 작성/개선 플레이북: `references/skill-writing-playbook.md`
- 트리거/품질 평가 기준: `references/evaluation.md`
- 재사용 템플릿 모음: `references/templates.md`

## Available Scripts

- `scripts/update_skills_list.py` — `skills/SKILLS.md`를 현재 스킬 목록 기준으로 갱신한다.
- `scripts/validate_skills.py` — `skills/` 하위 스킬을 일괄/선택 검증한다.
- `scripts/init_skill.py` — 새 스킬 폴더 템플릿을 생성한다.
- `scripts/quick_validate.py` — 단일 스킬의 기본 형식을 빠르게 검증한다.
- `scripts/generate_openai_yaml.py` — `agents/openai.yaml` UI 메타데이터를 생성/갱신한다.

## Output Contract

결과에는 다음을 포함한다.

- 생성/수정된 파일 목록
- 스킬 이름과 `description` 근거
- 선택한 구조(`scripts/`, `references/`, `assets/`) 근거
- 갱신된 스킬 목록 파일 경로(`skills/SKILLS.md`)
- 검증 관점(트리거 정확도, 실행 절차, 실패 시 보정 루프)
- 검증 실행 결과(`skills-ref` 가능 시 결과 포함)

## Guardrails

- 스킬은 하나의 응집된 작업 단위를 다루게 한다.
- `SKILL.md`에 불필요한 일반 지식 설명을 넣지 않는다.
- 선택지를 과도하게 나열하지 말고 기본 경로를 먼저 제시한다.
- 인터랙티브 프롬프트 의존 스크립트는 피한다.
- 스킬을 생성/수정한 경우 `scripts/update_skills_list.py` 실행을 생략하지 않는다.
- 스크립트는 `--help`, 명확한 에러, 구조화 출력(stdout)/진단(stderr) 분리를 지향한다.
- 과적합을 피하기 위해 description 개선 시 다양한 프롬프트 패턴을 사용한다.
