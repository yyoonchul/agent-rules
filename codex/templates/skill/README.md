# Codex Skill Template

이 폴더는 Codex 공식 스킬 형식에 맞춰 새 스킬을 만들기 위한 템플릿입니다.

## 1) 새 스킬 생성 절차

1. `SKILL.md.template`를 복사해 `<skill-name>/SKILL.md`를 만듭니다.
2. 필요하면 `agents/openai.yaml.template`를 복사해 `agents/openai.yaml`을 추가합니다.
3. `SKILL_REQUEST_TEMPLATE.md`에 요구사항을 먼저 정리한 뒤 지시문을 채웁니다.
4. 필요 시 `scripts/`, `references/`, `assets/`를 추가합니다.

## 2) Codex 공식 형식 핵심

- 필수 파일: `SKILL.md`
- 필수 frontmatter: `name`, `description`
- 선택 메타데이터: `agents/openai.yaml`
- 호출 방식:
  - 명시적 호출: `/skills` 또는 `$skill-name`
  - 암시적 호출: `description`과 사용자 요청이 매칭될 때

## 3) 권장 디렉토리 구조

```text
<skill-name>/
├── SKILL.md
├── scripts/
├── references/
├── assets/
└── agents/
    └── openai.yaml
```

## 4) `agents/openai.yaml` 주요 옵션

- `interface.display_name`: UI 표시 이름
- `interface.short_description`: UI 설명
- `interface.icon_small` / `icon_large`: 아이콘 경로
- `interface.brand_color`: 브랜드 색상
- `interface.default_prompt`: 기본 프롬프트
- `policy.allow_implicit_invocation`: `false`면 암시적 호출 비활성
- `dependencies.tools`: MCP 등 도구 의존성 선언

## 5) 설치/활성 관련 참고

- 스킬 비활성화: `~/.codex/config.toml`의 `[[skills.config]]`에서 `enabled = false`
- 동일 이름 스킬은 병합되지 않으며, 셀렉터에 함께 나타날 수 있음
- 스킬 폴더 심볼릭 링크도 스캔 대상

## 6) 주의사항

- `description`은 트리거 품질을 좌우하므로 범위/제외 조건을 함께 작성합니다.
- 스크립트는 결정적 동작이 필요할 때만 추가하고, 기본은 instruction-only를 권장합니다.
