# Claude Skill Generation Prompt Template

아래 프롬프트에 `SKILL_REQUEST_TEMPLATE.md` 내용을 붙여 Claude용 `SKILL.md`를 생성하세요.

```text
당신은 Claude Code skill author입니다.
아래 요구사항을 바탕으로 Claude 공식 스펙에 맞는 스킬을 생성하세요.

요구사항:
{{여기에 SKILL_REQUEST_TEMPLATE.md 작성 결과를 붙여넣기}}

출력 규칙:
1) 최종 출력은 완성된 `SKILL.md` 본문만 출력한다.
2) YAML frontmatter를 반드시 포함한다.
3) frontmatter는 다음 키를 필요 시 사용한다:
   - name
   - description
   - argument-hint
   - disable-model-invocation
   - user-invocable
   - allowed-tools
   - context
   - agent
4) 본문에는 Goal, Inputs, Workflow, Output Format, Guardrails를 포함한다.
5) 인수 사용이 필요하면 `$ARGUMENTS`, `$0`, `$1` 형식을 사용한다.
6) 부작용 있는 작업이면 `disable-model-invocation: true`로 설정한다.
```
