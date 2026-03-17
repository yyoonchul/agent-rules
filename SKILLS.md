# 스킬 목록

이 문서는 이 저장소의 `codex`와 `claude_code` 기준 스킬 보유 현황을 정리합니다.

| 사용 가능 범위 | 스킬 이름 | 역할 요약 | Codex 경로 | Claude 경로 |
| --- | --- | --- | --- | --- |
| 둘 다 | `commit-convention` | 프로젝트 커밋 메시지 규칙을 적용해 커밋 작성/변경 요약을 돕습니다. | `codex/skills/commit-convention/SKILL.md` | `claude_code/skills/commit-convention/SKILL.md` |
| 둘 다 | `docs` | 프로젝트 문서 구조를 초기화하고 관리합니다 (`AGENTS.md`는 맵, `docs/`는 상세 문서 저장소). | `codex/skills/docs/SKILL.md` | `claude_code/skills/docs/SKILL.md` |
| 둘 다 | `assignment-solver` | 문제 파일 1개를 기준으로 정답과 상세 풀이 파일을 생성하며, 참고자료가 없으면 웹 검색/상식을 활용합니다. | `codex/skills/assignment-solver/SKILL.md` | `claude_code/skills/assignment-solver/SKILL.md` |
| 둘 다 | `lecture-note` | 전사본 Markdown 1개를 느슨하게 정제해 템플릿 기반 강의노트를 만들고, 정리본+전사본을 한 파일로 저장합니다. | `codex/skills/lecture-note/SKILL.md` | `claude_code/skills/lecture-note/SKILL.md` |
| 둘 다 | `lecture-material-digest` | 강의자료 파일 1개를 읽어 `<같은 제목> digest.md`를 생성하고, 용어는 English로 유지한 채 한국어 설명 중심의 시험 대비 다이제스트를 만듭니다. | `codex/skills/lecture-material-digest/SKILL.md` | `claude_code/skills/lecture-material-digest/SKILL.md` |
| codex 전용 | `skill-creator` | 새 스킬 생성 또는 기존 스킬 개선을 구조화된 가이드/리소스로 지원합니다. | `codex/skills/.system/skill-creator/SKILL.md` | \- |
| codex 전용 | `skill-installer` | 큐레이션 목록 또는 GitHub 경로(비공개 포함)에서 스킬 설치를 지원합니다. | `codex/skills/.system/skill-installer/SKILL.md` | \- |

## 참고

- 사용 가능 범위는 각 플랫폼의 `skills/` 디렉터리 아래 현재 `SKILL.md` 파일을 기준으로 판단했습니다.
- `codex/skills/.system/` 아래의 숨김 시스템 스킬도 포함했습니다.
