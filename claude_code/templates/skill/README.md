# Claude Skill Template

이 폴더는 Claude Code 공식 스킬 형식에 맞춰 새 스킬을 만들기 위한 템플릿입니다.

## 1) 새 스킬 생성 절차

1. `SKILL.md.template`를 복사해 `<skill-name>/SKILL.md`를 만듭니다.
2. `SKILL_REQUEST_TEMPLATE.md`에 원하는 기능을 먼저 정리합니다.
3. 요청서 내용을 기반으로 `SKILL.md`의 frontmatter와 지시문을 채웁니다.
4. 필요하면 `references/`, `examples/`, `scripts/`를 추가합니다.

## 2) Claude 공식 형식 핵심

- 필수 파일: `SKILL.md`
- 형식: YAML frontmatter + markdown 본문
- 호출 방식:
  - 자동 호출: `description`과 요청이 매칭될 때
  - 수동 호출: `/skill-name`
- 지원 파일: 같은 스킬 디렉토리 안의 참조 문서/예제/스크립트

## 3) 권장 디렉토리 구조

```text
<skill-name>/
├── SKILL.md
├── references/
│   └── reference.md
├── examples/
│   └── example.md
└── scripts/
    └── helper.sh
```

## 4) Frontmatter 필드(Claude)

아래 필드는 공식 문서 기준이며 모두 선택 사항입니다(단 `description` 권장).

- `name`: 스킬 이름 (`/name`으로 호출)
- `description`: 언제 이 스킬을 써야 하는지
- `argument-hint`: 자동완성에서 보일 인수 힌트
- `disable-model-invocation`: `true`면 자동 호출 비활성화(수동만)
- `user-invocable`: `false`면 `/` 메뉴에서 숨김(배경지식용)
- `allowed-tools`: 스킬 활성화 중 허용 도구 목록
- `context`: `fork` 설정 시 subagent 컨텍스트에서 실행
- `agent`: `context: fork`일 때 사용할 subagent 타입
- `hooks`: 스킬 라이프사이클 훅 설정

## 5) 문자열 치환(Claude)

- `$ARGUMENTS`: 전달된 전체 인수
- `$ARGUMENTS[N]` 또는 `$N`: 위치별 인수(0-based)
- `${CLAUDE_SESSION_ID}`: 현재 세션 ID

## 6) 주의사항

- 사이드 이펙트(배포/메시지 전송/커밋 등)가 있으면 `disable-model-invocation: true`를 권장합니다.
- 설명(`description`)은 트리거 정확도에 직접 영향을 주므로, 해야 할 일/하지 말아야 할 일을 함께 적습니다.
