# Skill Format Reference (Common Baseline)

## 1) 최소 공통 포맷

모든 호환 클라이언트에서 안전하게 동작시키려면 아래를 기본으로 사용한다.

```markdown
---
name: your-skill-name
description: Use this skill when users need <core capability> in <contexts>.
---

# Skill Title
...
```

## 2) Frontmatter 제약

필수 키:

- `name`
- `description`

`name` 규칙:

- 1~64자
- 소문자/숫자/하이픈 사용
- 시작/끝 하이픈 금지
- 연속 하이픈(`--`) 금지
- 폴더명과 동일

`description` 규칙:

- 1~1024자
- 무엇을 하는지 + 언제 쓰는지 모두 포함
- 권장 문형: `Use this skill when ...`

선택 키:

- `license`
- `compatibility` (1~500자)
- `metadata`
- `allowed-tools` (experimental)

참고: `skills-ref` 검증기 호환을 위해 frontmatter는 가능한 스펙 키만 사용한다.

## 3) 디렉터리 규칙

```text
your-skill-name/
├── SKILL.md                # Required
├── scripts/                # Optional executable logic
├── references/             # Optional on-demand docs
└── assets/                 # Optional output resources
```

핵심 원칙:

- `SKILL.md`는 핵심 절차 중심, 500줄/5000토큰 내 권장
- 큰 문서/세부 규격은 `references/`로 분리
- 출력 템플릿/정적 리소스는 `assets/`로 분리

## 4) Progressive Disclosure

1. 항상 로드: `name`, `description`
2. 트리거 시 로드: `SKILL.md` 본문
3. 필요 시 로드: `scripts/`, `references/`, `assets/`

따라서 `description` 품질이 스킬 트리거의 핵심이다.

## 5) 경로 참조 규칙

- `SKILL.md`에서 파일 참조는 **스킬 루트 기준 상대경로**로 쓴다.
- 과도한 중첩 참조를 피하고(원 레벨 권장), `SKILL.md`에서 언제 읽을지 명시한다.

예:

```markdown
Read `references/errors.md` if API status is non-200.
Run `python3 scripts/validate.py --input "$INPUT"` before final output.
```

## 6) 링크

- 스펙: `https://agentskills.io/specification`
- 개념: `https://agentskills.io/what-are-skills`
- 레포: `https://github.com/agentskills/agentskills`
