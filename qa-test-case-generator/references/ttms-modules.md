# TTMS Modules Reference

Read this file only when the primary requirement or technical materials do not fully explain TTMS-specific business semantics, module behavior, role definitions, metric meanings, or cross-module context.

Do not treat this file as the primary source of truth when the user has provided requirement documents or technical design documents. Use it as a supplementary business reference.

## How To Use This Reference

Use the primary requirement or technical sources first. Then read only the relevant sections below when you need help with:
- TTMS terminology
- module-specific workflow semantics
- status or visibility rules
- metric interpretation
- release-critical business paths
- cross-module consistency checks

If this reference fills an information gap, make that explicit in the final output.

Example:

`Primary cases were derived from the requirement and technical documents. TTMS-specific status gating and invite-link semantics were supplemented by the Nomination Center playbook.`

## Shared TTMS Context

Use shared context when you need TTMS-wide business understanding, common terminology, or cross-module release risk.

- `TTMS Business & Quality Sharing`: `https://bytedance.larkoffice.com/wiki/Im2OwreOZit7glku2SucUiFHn4g`
- `TTMS OnePage`: `https://bytedance.larkoffice.com/wiki/EBq4wzHzZigoKckFt4YcaDoInJc`

Typical use cases:
- clarify TTMS-wide terms or collaboration models
- understand cross-module relationships
- identify release-critical end-to-end paths
- supplement shared quality expectations

## Built-In Playbooks

Read only the matching playbook for the module in scope. Do not load all of them by default.

### TTMS Admin

- `Nomination Center`: `https://bytedance.larkoffice.com/wiki/HAe9wqk5hiCLPJkp8GvcgpL9nw4`
- `Trademark Standard Format`: `https://bytedance.sg.larkoffice.com/docx/OFlidUACLoWKntxlXmJcFYLGn7f`
- `Brand Qualification Guidance`: `https://bytedance.sg.larkoffice.com/docx/IK52dqVU8oaCQGxOz04lrLCNgzd`

### TTMS Core Modules

- `Brand Diagnosis`: `https://bytedance.sg.larkoffice.com/docx/TEFzdBzFYofX7hxRakxlE4Qvgzf`
- `Audience`: `https://bytedance.sg.larkoffice.com/docx/K5azdNO98oWMqYxTuHLlHLrkgbf`
- `Brand Perception - Brand Insights`: `https://bytedance.sg.larkoffice.com/docx/L6O0drMbmo6d1vxFcAKcS4SPn1c`
- `Brand Perception - Search Insights`: `https://bytedance.sg.larkoffice.com/docx/OLRKdWFEzoeYtAxWeuZlwEGygVe`
- `Brand Perception - Vertical Insights`: `https://bytedance.sg.larkoffice.com/docx/Nm6kdyVjboyC6yxS1VvlEEejgG7`
- `Brand Perception - Tentpole Strategy`: `https://bytedance.sg.larkoffice.com/docx/CUUednSAPo4Vyaxne7dlmbCbgZe`
- `Merchandise Mart`: `https://bytedance.sg.larkoffice.com/docx/Rr4AdFQN9o6rKxxj9JSlLCSrg5f`
- `Catalog Analytics`: `https://bytedance.larkoffice.com/wiki/BwruwhM4Yif2W1kaYTEcHaREn6f`
- `Post Campaign Report`: `https://bytedance.sg.larkoffice.com/docx/RhHIdMos0oe8I5xxSXOlMn99gTc`

## Module-Specific Guidance

Use the following sections as testing prompts, not as immutable product truth. Prefer source-backed cases over broad domain assumptions.

### Nomination Center

Relevant when the feature involves nomination onboarding, qualification gating, or invite activation.

Prioritize:
- nomination creation and submission flows
- brand qualification upload and validation
- trademark owner vs authorized representative branches
- processing status transitions and qualification review status gating
- invite link visibility and activation constraints
- account ID field rules
- brand-exclusive vs brand-mixed definitions when relevant
- internal vs external visibility differences

High-risk failure patterns:
- invite link shown before upstream statuses are ready
- qualification branch logic diverges by owner type
- status-driven actions appear for the wrong role
- onboarding blockers caused by hidden validation rules

Typical `P0` candidates:
- merchant cannot complete onboarding due to broken nomination or invite gating
- critical action becomes invisible to the right user at the right status

### Brand Diagnosis

Relevant when the feature affects funnel metrics, benchmark logic, or reporting consistency.

Prioritize:
- funnel grouping such as Premium Reach, Massive Reach, Consideration, and Conversion
- metric glossary correctness and tooltip consistency
- campaign mapping logic and classification correctness
- benchmark-dependent metric behavior
- cross-card, chart, and glossary consistency

High-risk failure patterns:
- metric definitions differ across views
- benchmark changes silently alter downstream values
- glossary text and displayed calculations drift apart

Typical `P0` candidates:
- core reporting metrics become materially incorrect for decision-making
- summary and detail views disagree on key business numbers

### Audience

Relevant when the feature affects ACC journeys, transitions, or model-driven audience analysis.

Prioritize:
- ACC stage definitions and transition logic
- transition tiles and diagram/table toggle behavior
- drill-down flows
- touchpoint, creator, and video insight sections
- time window logic such as past 7, 15, and 30 days
- model-specific behavior such as Web Payment, Web Payment and Registration, App Payment, and Ticketing

High-risk failure patterns:
- selected stage or journey does not propagate to downstream views
- time-window switching causes inconsistent metrics or segmentation
- drill-down results do not match summary tiles

Typical `P0` candidates:
- core transition analysis cannot be completed end to end
- selected model or time window produces materially wrong audience results

### Brand Perception, Merchandise Mart, Catalog Analytics, Post Campaign Report

Use this section when the change touches insight browsing, reporting, export, or content synchronization across visual components.

Prioritize:
- filter combinations and segmentation dimensions
- table and chart synchronization
- metric explanation correctness
- data freshness and partial-data behavior
- no-data and empty-state handling
- export or reporting workflow correctness

High-risk failure patterns:
- filters affect one component but not another
- export output does not match on-screen selection
- data freshness messaging is absent or misleading

Typical `P0` candidates:
- exported or externally delivered report is materially wrong
- a release breaks the main customer-facing insight workflow

## Cross-Cutting Coverage Heuristics

Use these only when relevant to the in-scope feature.

### Data and Validation

Check where applicable:
- required vs optional fields
- valid vs invalid inputs
- minimum, maximum, and boundary values
- empty, null, duplicate, and malformed data
- file upload validation
- keyword, asset, and account ID format rules

### Workflow and State

Check where applicable:
- state transitions
- status gating
- branch conditions
- approval operations
- retry and dependency failure handling
- upstream/downstream continuity across TTMS flows

### Permissions and Visibility

Check where applicable:
- internal vs external users
- role-based action visibility
- gated actions by status and permission
- handoff behavior between operational roles

### Web B2B Interaction Patterns

Check where applicable:
- search, filter, sort, and pagination
- table, card, chart, and drill-down consistency
- bulk actions
- modal and drawer behavior
- export, invitation, and onboarding flows
- empty, loading, and partial-data states

### Metrics and Reporting

Check where applicable:
- metric definitions
- glossary consistency
- benchmark behavior
- date-range logic
- time-window selection
- cross-view aggregation consistency

## Link-Based Usage Rules

When the user provides links:
- treat requirement and technical documents as the primary source
- use a matching TTMS playbook only when the documents leave TTMS-specific gaps
- use shared TTMS references only when wider business context is needed
- extract testable statements, workflows, constraints, and edge cases
- merge duplicate requirements across links
- call out conflicting requirements explicitly

When the user does not provide requirement or technical materials:
- you may produce a draft using this reference as supplementary business context
- clearly label the result as a draft
- state assumptions and missing confirmations

## Clarification Prompts

Ask concise follow-up questions when important information is missing. Good examples:
- Which TTMS module or tab is affected?
- Is this for internal users, external users, or both?
- What upstream or downstream modules depend on this behavior?
- Which metrics, filters, dimensions, or date ranges are expected?
- What statuses or permission gates control the main action?
- What is explicitly out of scope for this release?

## Source Attribution Guidance

When this reference materially shapes the final output, summarize that honestly. Example:

`Primary cases were generated from the requirement and technical documents. TTMS module semantics and status-gating expectations were supplemented by the Nomination Center playbook and TTMS OnePage.`

If the final result relies mainly on this reference because no formal spec was provided, say so directly instead of implying stronger certainty than you have.
