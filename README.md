# Agent Skills Hub

Claude Code와 Codex가 공통으로 사용하는 스킬 저장소입니다.
현재 단일 소스는 `agent-skills/skills`이며, 전역 `~/.claude/skills`, `~/.codex/skills`는 이 경로를 바라보도록 연결합니다.

## 구조

```text
agent-rules/
├── agent-skills/
│   ├── SKILL_SYSTEM_GUIDE.md
│   └── skills/
│       ├── SKILLS.md
│       ├── assignment-solver/
│       ├── commit-convention/
│       ├── docs/
│       ├── lecture-material-digest/
│       ├── lecture-note/
│       ├── openai-docs/
│       ├── skill-creator/
│       └── skill-installer/
├── claude_code/   # (legacy) 과거 개별 관리 경로
└── codex/         # (legacy) 과거 개별 관리 경로
```

## 빠른 시작

1. 스킬 목록 갱신

```bash
python3 agent-skills/skills/skill-creator/scripts/update_skills_list.py
```

2. 스킬 검증

```bash
# 단일 스킬
python3 agent-skills/skills/skill-creator/scripts/validate_skills.py --skill <skill-name>

# 전체 스킬
python3 agent-skills/skills/skill-creator/scripts/validate_skills.py
```

3. 전역 심링크 설정(필요 시)

```bash
mkdir -p ~/.claude ~/.codex
ln -sfn /Users/yoonchul/dev/agent-rules/agent-skills/skills ~/.claude/skills
ln -sfn /Users/yoonchul/dev/agent-rules/agent-skills/skills ~/.codex/skills
```

## 운영 원칙

- 새 스킬 생성/수정 후 `SKILLS.md`를 항상 갱신합니다.
- 그다음 `validate_skills.py`로 형식 검증을 통과해야 합니다.
- 상세 규칙은 `agent-skills/SKILL_SYSTEM_GUIDE.md`를 따릅니다.

## 참고

- Agent Skills spec: `https://agentskills.io/specification`
- Agent Skills repo: `https://github.com/agentskills/agentskills`
