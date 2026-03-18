# Agent Skills 공통 운영 가이드 (Claude Code + Codex)

## 1) 목표

이 디렉터리는 에이전트별 스킬을 따로 관리하지 않고, **하나의 공통 스킬 본체**를 운영하기 위한 기준이다.

- 루트: `agent-skills/`
- 공통 스킬 본체: `agent-skills/skills/`
- 이 경로를 각 클라이언트 스킬 경로에 심볼릭 링크로 연결해 재사용한다.

## 2) 기본 구조

```text
agent-skills/
├── SKILL_SYSTEM_GUIDE.md        # 이 문서 (운영 지침)
└── skills/                      # 공통 스킬 본체
    └── <skill-name>/
        ├── SKILL.md             # 필수
        ├── scripts/             # 선택: 실행 코드
        ├── references/          # 선택: 지연 로딩 문서
        └── assets/              # 선택: 출력 리소스/템플릿
```

## 3) 설치/연결 규칙 (상호운용 우선)

Agent Skills 생태계 기준으로는 `.agents/skills/`가 가장 상호운용성이 높다.

- 우선 경로: `.agents/skills/`
- 호환 경로: `.claude/skills/`, 각 클라이언트 전용 경로

예시(프로젝트 루트에서 실행):

```bash
mkdir -p .agents
ln -sfn ../agent-skills/skills .agents/skills

mkdir -p .claude
ln -sfn ../agent-skills/skills .claude/skills
```

## 4) 공통 스펙 (필수/제약)

모든 스킬은 `SKILL.md`를 포함하고, YAML frontmatter + Markdown 본문으로 구성한다.

필수 frontmatter:

- `name`
- `description`

핵심 제약:

- `name`
  - 1~64자
  - 소문자/숫자/하이픈 권장 (크로스클라이언트 안전 규칙)
  - 하이픈으로 시작/종료 금지
  - 연속 하이픈(`--`) 금지
  - 스킬 폴더명과 일치
- `description`
  - 1~1024자
  - 무엇을 하는지 + 언제 쓰는지(트리거 조건) 포함
  - 권장 문형: `Use this skill when ...`

선택 frontmatter:

- `license`
- `compatibility` (최대 500자)
- `metadata`
- `allowed-tools` (experimental)

## 5) 작성 원칙 (원본 문서 반영)

- **Real expertise 우선**: 실제 작업/수정 이력에서 스킬을 추출한다.
- **Progressive disclosure**: `SKILL.md`는 핵심만, 상세는 `references/`로 분리한다.
- **Default-first**: 다중 옵션 나열보다 기본 경로 + 예외 분기로 쓴다.
- **Procedure-first**: 선언형 결과 지시보다 재사용 가능한 절차를 쓴다.
- **Gotchas 축적**: 반복 실수를 명시적으로 기록해 재발을 줄인다.
- **Validation loop**: 실행 → 검증 → 수정 → 재검증 루프를 명시한다.

권장 크기 가이드:

- `SKILL.md` 본문 500줄 이하 / 5000토큰 내 권장

## 6) 스크립트 설계 규칙

`scripts/`를 포함할 때는 다음을 기본 준수한다.

- 비대화형(non-interactive) 실행만 허용 (`TTY prompt` 금지)
- `--help` 제공 (입력/옵션/예시)
- 에러 메시지에 원인 + 수정 방법 포함
- stdout은 구조화 데이터(JSON/CSV 등), stderr는 진단 정보
- 재시도 가능하도록 idempotent 설계
- 파괴적 작업은 `--dry-run`, `--confirm/--force` 고려

## 7) 검증 운영 계획

1. **요청 분류**: 사용자 프롬프트에서 범위/산출물/제약 추출
2. **스킬 경계 정의**: in-scope / out-of-scope 정의
3. **description 설계**: 트리거 문구 초안 작성
4. **리소스 설계**: `scripts/`, `references/`, `assets/` 필요성 판단
5. **SKILL.md 작성**: 절차/체크리스트/검증 루프 중심 작성
6. **트리거 평가**: should-trigger / should-not-trigger 세트로 측정
7. **출력 평가**: with-skill vs without-skill(또는 이전 버전) 비교
8. **반복 개선**: 실패 패턴을 gotchas/절차/스크립트에 반영

검증 도구:

```bash
skills-ref validate ./agent-skills/skills/<skill-name>
```

`skill-creator` 사용 시 권장 단일 명령:

```bash
python3 agent-skills/skills/skill-creator/scripts/validate_skills.py --skill <skill-name>
```

## 8) 운영 시 주의사항

- 프로젝트 스킬은 신뢰된 저장소에서만 자동 로드하는 정책을 권장한다.
- 충돌 시 우선순위는 프로젝트 레벨 > 사용자 레벨을 기본으로 둔다.
- 동일 이름 충돌이 있으면 경고를 남긴다.

## 9) 업데이트 대응 루틴

다음 소스를 정기 확인해 규격/모범사례 변화를 반영한다.

- 공식 레포: `https://github.com/agentskills/agentskills`
- 공식 홈: `https://agentskills.io/home#why-agent-skills`
- 개념: `https://agentskills.io/what-are-skills`
- 스펙: `https://agentskills.io/specification`
- 클라이언트 구현: `https://agentskills.io/client-implementation/adding-skills-support`
- 제작/평가 가이드:
  - `https://agentskills.io/skill-creation/quickstart`
  - `https://agentskills.io/skill-creation/best-practices`
  - `https://agentskills.io/skill-creation/optimizing-descriptions`
  - `https://agentskills.io/skill-creation/evaluating-skills`
  - `https://agentskills.io/skill-creation/using-scripts`

권장 주기: 월 1회 또는 주요 에이전트 릴리스 직후.
