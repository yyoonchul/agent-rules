# Skill Writing Playbook

## 1) 요청을 스킬로 바꾸는 절차

1. 사용자 요청에서 반복 작업/실패 비용/도메인 특수성을 찾는다.
2. 스킬 경계를 정한다. (한 스킬 = 한 응집된 작업 단위)
3. 이름/description을 먼저 확정한다.
4. 본문 절차를 작성한다. (기본 경로 + 예외 분기)
5. 리소스를 분리한다.
   - 코드 반복이면 `scripts/`
   - 상세 지식이면 `references/`
   - 출력 재료면 `assets/`
6. 검증 루프를 넣는다. (실행 → 검증 → 수정 → 재검증)

추가 체크:

- `description`은 사용자 의도 기반 트리거 문장으로 작성 (`Use this skill when ...`)
- `SKILL.md` 본문은 절차 중심으로 작성하고 불필요한 일반론은 제거
- 큰 설명은 `references/`로 이동하고 `SKILL.md`에서 읽는 조건을 명시

## 2) 본문 작성 원칙

- 선언보다 절차: “무엇을 출력하라”보다 “어떻게 접근하라”
- 메뉴보다 기본값: 기본 도구/방법 1개를 먼저 제시
- 일반론 제거: 모델이 이미 아는 배경 설명 최소화
- gotchas 명시: 반복적으로 틀리는 환경 특이사항을 축적

## 3) 설명(`description`) 최적화 루프

1. should-trigger / should-not-trigger 프롬프트를 각각 준비한다.
2. 실제 실행에서 트리거 여부를 확인한다.
3. 실패 패턴을 분리한다.
   - 미트리거: description이 너무 좁은 경우
   - 오트리거: description이 너무 넓은 경우
4. description을 수정하고 재평가한다.

권장 운영:

- 쿼리 수: 총 16~20개
- 비율: should-trigger 8~10, should-not-trigger 8~10
- 반복: 동일 쿼리 최소 3회 실행
- 판단: trigger rate 기준으로 통과 여부 판단
- 과적합 방지: train/validation 분리(예: 60/40)

프롬프트 설계 팁:

- 문체/길이/오탈자/맥락 밀도를 다양화
- 키워드 유사하지만 다른 작업(near-miss) 포함

## 4) 스크립트 포함 기준

`scripts/`를 쓰는 경우:

- 같은 코드가 반복 생성됨
- 실행 실패 비용이 높음
- 순서/파라미터가 엄격함

스크립트 설계 규칙:

- 비대화형(non-interactive) 인터페이스
- `--help` 제공
- 명확한 에러 메시지
- 재실행 가능한 입력/출력 계약
- stdout은 구조화 데이터, stderr는 진단 정보
- 파괴적 작업은 `--dry-run`/`--confirm` 패턴 권장

## 5) references 구성 기준

- 파일 하나당 한 주제
- 큰 파일에는 목차 제공
- `SKILL.md`에서 “언제 읽을지”를 명시

예: “API가 4xx/5xx를 반환하면 `references/api-errors.md`를 읽어라.”

## 6) 반복 개선

- 실제 사용 로그에서 실패 지점을 수집
- 지시가 모호하면 절차를 더 구체화
- 과도하면 축소하고 핵심 절차만 남김
- 새 실수 유형은 gotchas로 즉시 반영

## 7) 출력 품질 평가(권장)

트리거 최적화와 별개로, 산출물 품질도 분리해서 평가한다.

권장 방식:

1. `evals/evals.json`에 테스트 케이스 작성
2. 같은 케이스를 `with_skill`/`without_skill`(또는 이전 버전)로 실행
3. assertion 기반 `grading.json`으로 PASS/FAIL 근거 기록
4. `benchmark.json`에서 pass-rate/time/tokens 비교
5. 사람 리뷰 피드백을 함께 반영하여 다음 iteration 수행

## 8) 생성 직후 1회 검증(필수 게이트)

새 스킬 작성이 끝나면 아래 명령을 한 번 실행한다.

```bash
python3 scripts/validate_skills.py --skill <skill-name>
```

실패 시에는 frontmatter/이름 규칙/필수 필드를 먼저 고친 뒤 다시 실행한다.
