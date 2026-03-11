# Codex Skill Request Template

아래 항목을 채우면 Codex 스킬을 공식 스펙 형식으로 구현하기 쉽습니다.

## 1) 기본 정보

- Skill name (kebab-case):
- 한 줄 설명 (`description` 초안):
- 해결하려는 문제:

## 2) 호출 정책

- 명시적 호출 키워드(예: `$skill-name`):
- 암시적 호출되어야 하는 상황:
- 암시적 호출되면 안 되는 상황:
- `policy.allow_implicit_invocation`: `true` / `false`

## 3) 입력/출력 정의

- 입력 형식:
- 반드시 생성해야 하는 결과물:
- 최종 응답 형식:
- 성공 조건(완료 정의):

## 4) 절차 정의

- 단계별 workflow (번호 목록):
- 실패 시 처리 방식:
- 검증 방법(테스트/체크):

## 5) 도구 및 의존성

- 필요한 도구(기본 도구/MCP):
- `agents/openai.yaml` 의존성 선언 필요 여부:
- 외부 리소스/인증 요구사항:

## 6) 지원 파일

- `references/`에 둘 문서:
- `scripts/`에 둘 스크립트:
- `assets/`에 둘 템플릿/정적 파일:

## 7) 제약 조건

- 금지 행동:
- 보안/개인정보 제한:
- 사용자 승인 필요 조건:
