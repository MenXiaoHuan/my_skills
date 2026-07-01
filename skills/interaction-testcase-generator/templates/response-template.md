### Delivery Note
- Hand off the generated `.xmind` file as the primary deliverable
- Do not show a local or workspace absolute path in the final user-facing response
- If multiple internal candidates were generated, expose only the adjudicated final result unless the user explicitly requests debug artifacts

### Output Status
- `final` or `draft`

### P0 Scenario Summary
- `本次范围未识别出 P0 场景`

### Full Case Coverage Summary
- core workflow cases
- validation and negative cases
- permission and role cases
- boundary and data cases
- integration and regression cases

### Source Summary
- requirement document or user-provided feature description
- technical design or API spec
- supplementary domain knowledge reference if used

### Assumptions
- List assumptions only when needed

### Risks and Open Questions
- List unresolved conflicts, missing rules, or setup gaps only when needed

### Internal Only
- Candidate A/B comparison notes, merge scratchpads, and rubric scoring are internal workflow artifacts and should not appear in the normal user-facing response
- For dual-candidate mode, use `templates/multi_candidate_adjudication.template.md` internally before building the final `.xmind`
