# Agent Skills Hub

This repository manages a shared Agent Skills source for multiple clients (Claude Code and Codex).
The single source of truth is `agent-skills/skills`.

## Repository Layout

```text
agent-rules/
├── agent-skills/
│   ├── SKILL_SYSTEM_GUIDE.md
│   └── skills/
│       ├── SKILLS.md
│       ├── <skill-name>/
│       │   ├── SKILL.md
│       │   ├── scripts/
│       │   ├── references/
│       │   └── assets/
│       └── ...
├── .claude/
│   └── skills -> ../agent-skills/skills
└── .codex/
    └── skills -> ../agent-skills/skills
```

## Quick Commands

```bash
# Refresh skill catalog markdown
python3 agent-skills/skills/skill-creator/scripts/update_skills_list.py

# Validate all skills
python3 agent-skills/skills/skill-creator/scripts/validate_skills.py
```

## Global Symlink Setup (optional)

```bash
mkdir -p ~/.claude ~/.codex
ln -sfn /Users/yoonchul/dev/agent-rules/agent-skills/skills ~/.claude/skills
ln -sfn /Users/yoonchul/dev/agent-rules/agent-skills/skills ~/.codex/skills
```

## References

- Agent Skills specification: `https://agentskills.io/specification`
- Agent Skills repository: `https://github.com/agentskills/agentskills`
