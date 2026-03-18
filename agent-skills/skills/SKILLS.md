# 통합 스킬 목록

이 문서는 `agent-skills/skills` 기준 스킬 목록입니다.
`skill-creator/scripts/update_skills_list.py`로 자동 생성/갱신됩니다.

| 스킬 이름 | 역할 요약 | 경로 |
| --- | --- | --- |
| `assignment-solver` | Solve one assignment problem file and save a final answer with detailed explanation next to the problem file. Use when the user asks to generate a solution artifact from a mention… | `agent-skills/skills/assignment-solver/SKILL.md` |
| `commit-convention` | Applies the project's commit message convention. Use when writing commit messages, making git commits, or summarizing changes. | `agent-skills/skills/commit-convention/SKILL.md` |
| `docs` | Initializes and manages the project's documentation structure. Follows the "in‑repository knowledge store" pattern, using AGENTS.md as the map and docs/ as the system of record. U… | `agent-skills/skills/docs/SKILL.md` |
| `lecture-material-digest` | Read one or more lecture material files (for example PDF/PPT/PPTX) and generate one Markdown digest file per source in the same folder using the source title + "_ digest" filename… | `agent-skills/skills/lecture-material-digest/SKILL.md` |
| `lecture-note` | Transform one mentioned lecture transcript markdown file into a structured lecture note and save a merged output file in the same folder. Use when the user asks to create lecture… | `agent-skills/skills/lecture-note/SKILL.md` |
| `openai-docs` | Use when the user asks how to build with OpenAI products or APIs and needs up-to-date official documentation with citations, help choosing the latest model for a use case, or expl… | `agent-skills/skills/openai-docs/SKILL.md` |
| `skill-creator` | Create or update Agent Skills for Claude Code, Codex, and other Agent Skills-compatible clients. Use when users ask to design a new skill, revise an existing skill, write SKILL.md… | `agent-skills/skills/skill-creator/SKILL.md` |
| `skill-installer` | Install Codex skills into $CODEX_HOME/skills from a curated list or a GitHub repo path. Use when a user asks to list installable skills, install a curated skill, or install a skil… | `agent-skills/skills/skill-installer/SKILL.md` |

## 갱신 명령

```bash
python3 agent-skills/skills/skill-creator/scripts/update_skills_list.py
```
