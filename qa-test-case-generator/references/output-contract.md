# Output Contract

Read this file only when you need stricter formatting rules, explicit priority wording, or XMind structure details beyond the default workflow in `SKILL.md`.

## Default Deliverable

Default output is a real `.xmind` file generated on disk.

Rules:
- Return the absolute file path first.
- Keep supporting narration short unless the user asks for more detail.
- Treat the `.xmind` file as the primary deliverable, not an optional attachment.
- If generation fails, explain the exact failure and provide a fallback outline only as a failure mode.

Default response order:
1. XMind file path
2. P0 Scenario Summary
3. Source Summary
4. Full Case Coverage Summary
5. Risks and Open Questions
6. Optional outline preview or tables only if requested

## Language Rules

Default output language is Simplified Chinese.

Use professional English only when the user explicitly asks for English.

Do not translate implementation-stable identifiers such as:
- API fields
- enum values
- error codes
- URLs
- metric IDs
- feature flags
- log keywords

## Required Output Behavior

Always do the following:
- Generate a complete in-scope case set, not only `P0`
- Mark `P0` cases explicitly when justified
- State assumptions when source material is incomplete
- Call out document conflicts instead of silently merging contradictions
- Prefer concise, executable wording over requirement paraphrasing

Do not do the following:
- Return only a prose summary when the user expects test cases
- Invent TTMS business rules without a clear source or an explicit assumption label
- Use `P0` as a filter that suppresses `P1/P2/P3`
- Inflate output with tables when the user only wants the XMind file

## Test Point Standard

Use this section when the user asks for explicit test points or when you need a stable intermediate structure before expanding to cases.

Each test point should:
- represent one independently testable behavior, rule, risk, or validation focus
- be grouped by module, workflow stage, or quality dimension
- include a priority and a short rationale
- be specific enough to expand into one or more concrete test cases

Recommended naming pattern:

`[Module] - [Business Rule or Verification Focus]`

Examples:
- `Nomination Center - Invite link is gated by Data Ready and qualification review status`
- `Audience - Transition tile drill-down respects selected ACC journey and date range`
- `Brand Diagnosis - Metrics stay consistent across card, chart, and glossary`

Default test point table:

| Test Point ID | Module/Feature | Test Point | Source Basis | Priority | Rationale |
| --- | --- | --- | --- | --- | --- |

## Test Case Standard

Each detailed test case should:
- validate one primary scenario
- state preconditions when permissions, data, or environment matter
- use sequential, executable web steps
- describe observable expected results
- align priority with the linked test point
- use a controlled test type when tabular output is requested

Recommended scenario naming pattern:

`[Module] - [Action] - [Condition or Expected Behavior]`

Examples:
- `Nomination Center - Show invite link only after processing status becomes Data Ready`
- `Audience - Display New Consideration transition results for the selected 30-day window`
- `Brand Diagnosis - Calculate Awareness penetration consistently with benchmark rules`

Default detailed case table:

| Test Case ID | Module/Feature | Test Scenario | Preconditions | Test Steps | Test Data | Expected Result | Priority | Test Type |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

Suggested controlled vocabulary for `Test Type`:
- `Functional`
- `Negative`
- `Boundary`
- `Permission`
- `Integration`
- `Regression`
- `UI`

## Priority Model

Use the following interpretation unless the user defines another model.

- `P0`: Release-critical path, launch blocker, or severe failure on a core TTMS workflow
- `P1`: High-value or high-risk behavior with strong business or operational impact
- `P2`: Important but non-blocking scenario with moderate impact or fallback
- `P3`: Low-risk, low-frequency, cosmetic, or optional coverage

Use `P0` conservatively. Typical `P0` candidates include:
- launch-blocking end-to-end paths
- permission or visibility failures on critical workflows
- status-gating errors that block onboarding or reporting
- severe metric or export correctness issues
- upstream or downstream failures that break workflow continuity

If no case truly qualifies, explicitly state:

`本次范围未识别出 P0 场景`

## Coverage Expectations

Unless the user narrows scope, coverage should be balanced across the relevant dimensions:
- core functional flow
- negative and validation scenarios
- permissions and role-based access
- boundary and data conditions
- integration dependencies
- regression-sensitive paths
- empty, partial-data, and no-data behavior

Keep coverage complete for the agreed scope. Do not repeat trivial wording variants.

## XMind Contract

Use this section when the skill needs to produce the `.xmind` file.

The output file must be XMind 8 compatible and openable as a zip container with `content.xml`.

Preferred hierarchy:
- Root topic: `用例集`
- Group node: `+分组 N` or a short module/workflow label
- Test case node: one topic per case
- Detail node under case: `前置条件` preferred, `文本描述` allowed when setup is not needed
- Step nodes under detail branch
- Expected result node under each step

### Grouping Rules

Group cases by one of the following:
- module
- page
- feature area
- workflow stage

Pick the grouping that best reduces ambiguity. Do not mix unrelated grouping strategies in the same output unless the source material clearly spans multiple structures.

### Case Node Rules

For each case node:
- Put exactly one case title on the topic node
- Use the note field for compact remarks when needed
- Keep the title short enough for mind-map reading
- Add the appropriate XMind priority marker
- Prefix the title with `[P0]` when the case priority is `P0`

### Detail and Step Rules

- Prefer `前置条件` as the first detail node when setup matters
- Use `文本描述` only when explicit setup is unnecessary
- Keep one executable action per step node
- Put the expected result under the corresponding step
- Avoid merging unrelated expectations into one step unless they are inseparable

### Priority Mapping

Map priorities to XMind markers as follows:
- `P0` -> `priority-1`
- `P1` -> `priority-2`
- `P2` -> `priority-3`
- `P3` -> `priority-4`
- optional or informational coverage -> `priority-5`

Apply both of the following to `P0` cases:
- title prefix `[P0]`
- marker `priority-1`

### Naming Guidance

Use short, stable names:

- Group name:
  - `+Nomination`
  - `+Audience Transition`
  - `+Brand Diagnosis`
- Precondition node:
  - one compact sentence describing setup, role, or data state
- Step node:
  - start with an action verb such as `Open`, `Select`, `Click`, `Input`, `Upload`, `Switch`, `Filter`, `Export`
- Expected node:
  - describe the observable result, status, visibility, calculation, or navigation outcome

## Structured Input for the Builder

When preparing data for `scripts/xmind_build.py`, use a normalized case tree before generating the file.

If you only need a starter artifact instead of writing the JSON from scratch, begin from `templates/xmind_input.template.json` and replace the placeholder group, cases, priorities, and steps with scenario-specific content.

Recommended JSON shape:

```json
{
  "root_title": "用例集",
  "groups": [
    {
      "title": "+Nomination",
      "cases": [
        {
          "title": "[P0] Nomination Center - Show invite link after Data Ready",
          "priority": "P0",
          "note": "Optional note",
          "preconditions": "Merchant has passed qualification review",
          "description": "",
          "steps": [
            {
              "action": "Open nomination detail page",
              "expected": "Invite link entry is visible"
            }
          ]
        }
      ]
    }
  ]
}
```

Normalization rules:
- Use `root_title = 用例集` unless the user requests a different root
- Keep `groups` and `cases` non-empty for final output
- Prefer `preconditions`; use `description` only if setup is unnecessary
- Preserve user-facing wording in titles, but keep identifiers stable when needed

## Examples

Use the following examples as structure references, not as fixed domain content.

### Example Response Shape

```md
XMind file: /absolute/path/to/output.xmind

### P0 Scenario Summary
- [P0] Nomination Center - Invite link becomes visible only after Data Ready

### Full Case Coverage Summary
- nomination creation and submission
- qualification validation
- status gating and role visibility
- negative and boundary scenarios

### Source Summary
- requirement draft from user
- supplementary Nomination Center playbook

### Risks and Open Questions
- exact brand-mixed rule needs confirmation
```

### Example Minimal XMind JSON

```json
{
  "root_title": "用例集",
  "groups": [
    {
      "title": "+Nomination",
      "cases": [
        {
          "title": "[P0] Nomination Center - Invite link visible after Data Ready",
          "priority": "P0",
          "preconditions": "Merchant passed qualification review",
          "steps": [
            {
              "action": "Open nomination detail page",
              "expected": "Invite link entry is visible"
            }
          ]
        }
      ]
    }
  ]
}
```

## Response Template

Use this default structure unless the user asks for another format.

If you need a compact response scaffold, start from `templates/response-template.md` and then trim or expand sections based on the user request.

### XMind File (Mandatory)

`XMind file: /absolute/path/to/output.xmind`

### P0 Scenario Summary

List all identified `P0场景` first. If none exist, say:

`本次范围未识别出 P0 场景`

### Full Case Coverage Summary

Summarize the non-P0 coverage briefly, for example:
- core workflow cases
- validation and negative cases
- permission and role cases
- boundary and data cases
- integration and regression cases

### Source Summary

List the primary requirement or technical documents used, plus any supplementary TTMS references.

### Outline Preview (Optional)

Provide only when requested or when a quick structure check is materially helpful.

### Assumptions

List assumptions caused by missing or ambiguous information.

### Risks and Open Questions

List conflicts, unclear rules, missing dependencies, or data/setup gaps that should be confirmed.

## Failure Handling

If `.xmind` generation fails:
- explain the exact failure
- provide the fallback outline only as a temporary substitute
- do not pretend the main deliverable succeeded

If the source materials conflict:
- identify the conflict explicitly
- keep affected cases marked as assumptions or open questions

If the source material is thin:
- produce a draft if the user still wants one
- label assumptions clearly
- avoid overstating confidence
