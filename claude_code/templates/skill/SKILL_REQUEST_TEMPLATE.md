# Claude Skill Request Template

아래 항목을 채우면 Claude 스킬을 정확한 형식으로 설계/생성하기 쉽습니다.

## 1) 스킬 기본 정보

- Skill name (kebab-case):
- 한 줄 설명:
- 이 스킬이 해결할 핵심 문제:

## 2) 트리거 조건

- 자동 호출되어야 하는 상황:
- 자동 호출되면 안 되는 상황:
- 수동 호출 명령(`/skill-name`) 필요 여부:
- 예상 인수 형식(`argument-hint`):

## 3) 실행 정책

- `disable-model-invocation`: `true` / `false`
- `user-invocable`: `true` / `false`
- 필요 도구(`allowed-tools`):
- subagent 실행 필요 여부(`context: fork`):
- subagent 타입(`agent`):

## 4) 작업 절차

- 입력값 정의 (`$ARGUMENTS`, `$0`, `$1` 등):
- 단계별 workflow (번호 목록으로):
- 성공 조건(완료 정의):

## 5) 출력 형식

- 최종 응답에 반드시 포함할 섹션:
- 파일/코드 변경 시 보고 형식:
- 테스트/검증 결과 보고 방식:

## 6) 지원 파일

- `references/`에 둘 규칙/레퍼런스:
- `examples/`에 둘 예시:
- `scripts/`에 둘 실행 스크립트:

## 7) 제약/가드레일

- 금지 행동:
- 보안/개인정보 제한:
- 승인 필요한 작업:
