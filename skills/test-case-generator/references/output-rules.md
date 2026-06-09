# Output Rules

Read this file only when you need stricter formatting rules, explicit priority wording, table structures, or XMind hierarchy details beyond the default workflow in `SKILL.md`.

## Default Deliverable

Default output is a real `.xmind` file generated on disk.

Rules:
- Return the absolute file path first.
- Keep supporting narration short unless the user asks for more detail.
- Treat the `.xmind` file as the primary deliverable.
- Do not expose the intermediate JSON build file unless the user explicitly asks for debugging artifacts.
- If generation fails, explain the exact failure and provide a fallback outline only as a failure mode.

## Required Output Behavior

Always:
- Generate a complete in-scope case set, not only `P0`
- Mark `P0` cases explicitly when justified
- State assumptions when source material is incomplete
- Call out document conflicts instead of silently merging contradictions

Do not:
- Return only a prose summary when the user expects test cases
- Invent domain-specific business rules without a clear source or an explicit assumption label
- Use `P0` as a filter that suppresses `P1/P2/P3`

## Test Point Standard

Recommended naming pattern:

`[Module] - [Business Rule or Verification Focus]`

Example:
- `Authentication - MFA challenge appears after valid password submission`
- `Order API - Duplicate callback is handled idempotently`
- `Sales Dashboard - Chart and export totals stay consistent under the selected filters`

Default test point table:

| Test Point ID | Module/Feature | Test Point | Source Basis | Priority | Rationale |
| --- | --- | --- | --- | --- | --- |

## Test Case Standard

Recommended naming pattern:

`[Module] - [Action] - [Condition or Expected Behavior]`

Example:
- `Authentication - Require MFA after valid password submission`
- `Order API - Return 409 when duplicate create request conflicts with existing state`
- `Sales Dashboard - Keep chart, table, and export totals consistent for the selected date range`

Default detailed case table:

| Test Case ID | Module/Feature | Test Scenario | Preconditions | Test Steps | Test Data | Expected Result | Priority | Test Type |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

## Priority Model

- `P0`: Release-critical path, launch blocker, or severe failure on a core workflow
- `P1`: High-value or high-risk behavior with strong business or operational impact
- `P2`: Important but non-blocking scenario with moderate impact or fallback
- `P3`: Low-risk, low-frequency, cosmetic, or optional coverage

If no case truly qualifies, explicitly state:

`本次范围未识别出 P0 场景`

## XMind Contract

Preferred hierarchy:
- Root topic: `用例集`
- Group node: a short module or workflow label
- Test case node: one topic per case
- Detail node under case: `前置条件` preferred, `文本描述` allowed when setup is not needed
- Step nodes under detail branch
- Expected result node under each step

Priority mapping:
- `P0` -> `priority-1`
- `P1` -> `priority-2`
- `P2` -> `priority-3`
- `P3` -> `priority-4`

## Structured Input for the Builder

Use a normalized case tree before generating the final file.

Write the JSON to an internal build file such as `.test_case_xmind_input.json`.

Recommended JSON shape:

```json
{
  "root_title": "用例集",
  "groups": [
    {
      "title": "Authentication",
      "cases": [
        {
          "title": "[P0] Authentication - Require MFA after valid password submission",
          "priority": "P0",
          "note": "Optional note",
          "preconditions": "Test account has MFA enabled",
          "description": "",
          "steps": [
            {
              "action": "Submit valid username and password",
              "expected": "The MFA challenge is displayed"
            }
          ]
        }
      ]
    }
  ]
}
```

## Response Template

Default response order:

1. XMind file path
2. P0 Scenario Summary
3. Source Summary
4. Full Case Coverage Summary
5. Risks and Open Questions

