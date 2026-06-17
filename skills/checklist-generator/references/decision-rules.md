# Decision Rules

Read this file only when you need to decide whether to ask follow-up questions, proceed with assumptions, or produce a draft instead of a final detailed test case set.

## Ask Vs Assume

Ask follow-up questions when:
- the feature under test is unclear
- the main workflow or expected outcome is unclear
- the target user, role boundary, or permission model is unclear
- the release scope or systems affected are unclear
- conflicting source materials would materially change test coverage or priority
- missing information would change whether a case is `P0`, in scope, or out of scope

Continue with explicit assumptions when:
- only secondary limits, examples, or non-critical defaults are missing
- missing detail does not change the core workflow or release risk classification
- the user explicitly wants a fast first-pass version
- the missing information can be safely isolated as an assumption without distorting the main test structure

Do not silently assume:
- core workflow semantics
- approval or status transitions
- role permissions
- API contract behavior
- metric definitions that affect expected outcomes
- architecture dependencies that change test scope

## Draft Vs Final

Produce a final detailed test case set when:
- the main workflow is understandable
- the affected systems and roles are sufficiently clear
- critical expectations are backed by source material or clearly bounded assumptions
- no major source conflict remains unresolved

Produce a draft when:
- source material is thin and the user still wants a usable first version
- critical definitions are missing for workflow, status, role, contract, or dependency behavior
- available materials conflict in ways that materially affect coverage
- the result depends on assumptions that could substantially change the final test case set

When producing a draft:
- label it clearly as `draft`
- state the key assumptions explicitly
- separate confirmed knowledge from assumptions
- highlight what must be clarified before execution-grade testing

## Thin Or Conflicting Sources

If source materials are thin, decide in this order:
1. use a relevant supplementary reference skill if the gap is about business, API, or architecture semantics
2. ask follow-up questions if the remaining gap still affects scope, workflow meaning, role behavior, expected outcomes, or release risk
3. continue with explicit assumptions only when the missing detail is secondary
4. produce a draft when critical uncertainty remains

If source materials conflict:
- identify the conflict explicitly
- do not silently merge contradictory expectations
- downgrade to `draft` when the conflict materially affects the final test case set
