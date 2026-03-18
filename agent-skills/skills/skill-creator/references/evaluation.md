# Evaluation Reference (Trigger + Output)

## 1) Trigger 평가

목표: 스킬이 필요한 요청에서 안정적으로 트리거되고, 불필요한 요청에서는 트리거되지 않게 한다.

권장 절차:

1. `should_trigger=true/false` 쿼리 세트 작성
2. 각 쿼리를 여러 번 실행해 trigger rate 측정
3. train/validation 분리로 과적합 방지
4. `description` 수정 후 반복

핵심 지표:

- should-trigger 쿼리의 trigger rate
- should-not-trigger 쿼리의 비트리거율

## 2) Output 품질 평가

목표: 트리거 이후 실제 산출물이 baseline 대비 개선되는지 확인한다.

권장 절차:

1. `evals/evals.json` 작성 (prompt, expected_output, assertions)
2. `with_skill` / `without_skill`(또는 이전 버전) 각각 실행
3. `grading.json`에서 assertion별 PASS/FAIL + evidence 기록
4. `benchmark.json`으로 pass-rate / time / tokens 비교
5. 인간 리뷰 피드백으로 최종 보정

## 3) Assertion 작성 규칙

- 검증 가능하고 관측 가능한 문장으로 작성
- 지나치게 취약한 문자열 일치 조건은 피함
- 정량화 가능한 조건을 우선

좋은 예:

- "출력 디렉터리에 차트 이미지 파일이 존재한다"
- "정확히 3개 항목이 표에 포함된다"

나쁜 예:

- "결과가 좋아 보인다"
- "문장 A를 정확히 포함한다"

## 4) 반복 개선 루프

1. 실패 assertion + 실행 trace + 사람 피드백 수집
2. 절차 모호성/과도성/누락 지점 분리
3. `SKILL.md`와 리소스(`scripts/`, `references/`) 보정
4. 새 iteration 디렉터리에서 재평가

## 5) 참고 링크

- `https://agentskills.io/skill-creation/optimizing-descriptions`
- `https://agentskills.io/skill-creation/evaluating-skills`
