# Codex Skill Generation Prompt Template

아래 프롬프트에 `SKILL_REQUEST_TEMPLATE.md` 내용을 붙여 Codex용 `SKILL.md`(+선택 `agents/openai.yaml`)를 생성하세요.

```text
당신은 Codex skill author입니다.
아래 요구사항을 바탕으로 Codex 공식 스펙에 맞는 스킬 파일을 생성하세요.

요구사항:
{{여기에 SKILL_REQUEST_TEMPLATE.md 작성 결과를 붙여넣기}}

출력 규칙:
1) 먼저 완성된 `SKILL.md`를 출력한다.
2) `SKILL.md`는 YAML frontmatter를 포함하고, `name`과 `description`은 필수다.
3) 본문에는 Goal, Inputs, Procedure, Output Contract, Guardrails를 포함한다.
4) 요구사항에 암시적 호출 제한이 있으면 `agents/openai.yaml`도 함께 출력하고
   `policy.allow_implicit_invocation`을 요구사항대로 설정한다.
5) 도구 의존성이 있으면 `dependencies.tools`를 선언한다.
6) 코드 블록 외의 장황한 설명 없이 바로 파일 내용을 출력한다.
```
