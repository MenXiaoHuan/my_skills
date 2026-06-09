# TTMS Domain Reference Restructure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Restructure TTMS domain reference content from one flat file into a progressively loadable directory under `references/domain/modules/ttms/` and update the domain retriever to use the new entry point.

**Architecture:** Keep the TTMS reference tree shallow and responsibility-driven: one index, one module map, one shared-context file, and one file per TTMS module. Migrate content out of the legacy flat TTMS file, preserve source attribution in both navigation and module files, then remove that legacy entry after the retriever skill points to the new path.

**Tech Stack:** Markdown, repository reference skills under `references/domain/`, git, shell verification with `rg`, `find`, and `git diff`

---

## File Structure

### Create

- `references/domain/modules/ttms/index.md`
- `references/domain/modules/ttms/module-map.md`
- `references/domain/modules/ttms/shared-context.md`
- `references/domain/modules/ttms/modules/nomination-center.md`
- `references/domain/modules/ttms/modules/brand-diagnosis.md`
- `references/domain/modules/ttms/modules/audience.md`
- `references/domain/modules/ttms/modules/brand-perception.md`
- `references/domain/modules/ttms/modules/merchandise-mart.md`
- `references/domain/modules/ttms/modules/catalog-analytics.md`
- `references/domain/modules/ttms/modules/post-campaign-report.md`

### Modify

- `references/domain/SKILL.md`

### Delete

- the legacy single-file TTMS reference

## Task 1: Create TTMS Entry Files

**Files:**
- Create: `references/domain/modules/ttms/index.md`
- Create: `references/domain/modules/ttms/module-map.md`
- Create: `references/domain/modules/ttms/shared-context.md`

- [ ] **Step 1: Create the TTMS directory tree**

Run: `mkdir -p references/domain/modules/ttms/modules`
Expected: command exits `0`

- [ ] **Step 2: Write `references/domain/modules/ttms/index.md`**

```md
# TTMS Domain Index

Read this directory only when requirement or technical materials do not fully explain TTMS-specific business semantics.

Do not treat TTMS domain references as the primary source of truth when formal requirement or technical documents exist.

## Loading Order

1. Read this file first.
2. If the question is about TTMS-wide terminology, roles, or cross-module context, read `shared-context.md`.
3. If the question is module-specific, locate the matching module in `module-map.md`.
4. Read only the matching file under `modules/`.
5. In the final output, state clearly when TTMS references were used to fill gaps.

## Use This Reference For

- TTMS terminology
- role definitions
- status and visibility semantics
- module-specific workflow meaning
- metric interpretation
- release-critical business paths
- cross-module consistency checks

## Do Not Use This Reference For

- replacing explicit requirement or technical design
- inventing product truth when no source exists
- loading all TTMS modules by default

## Attribution Rule

If TTMS references materially influenced the answer, say so explicitly.
```

- [ ] **Step 3: Verify the loading order text exists**

Run: `rg -n "Loading Order|module-map.md|shared-context.md|Read only the matching file under \`modules/\`" references/domain/modules/ttms/index.md`
Expected: 4 matching lines from `references/domain/modules/ttms/index.md`

- [ ] **Step 4: Write `references/domain/modules/ttms/module-map.md`**

```md
# TTMS Module Map

Use this file to locate the correct TTMS module reference. Do not use it as the final business source when a deeper module file exists.

| Module | Use When | File | Primary Sources |
| --- | --- | --- | --- |
| Nomination Center | nomination onboarding, qualification gating, invite activation | `modules/nomination-center.md` | `https://bytedance.larkoffice.com/wiki/HAe9wqk5hiCLPJkp8GvcgpL9nw4` |
| Brand Diagnosis | funnel metrics, benchmark logic, reporting consistency | `modules/brand-diagnosis.md` | `https://bytedance.sg.larkoffice.com/docx/TEFzdBzFYofX7hxRakxlE4Qvgzf` |
| Audience | ACC journeys, transition analysis, model-specific behavior | `modules/audience.md` | `https://bytedance.sg.larkoffice.com/docx/K5azdNO98oWMqYxTuHLlHLrkgbf` |
| Brand Perception | insight browsing, filter logic, data sync | `modules/brand-perception.md` | `https://bytedance.sg.larkoffice.com/docx/L6O0drMbmo6d1vxFcAKcS4SPn1c`, `https://bytedance.sg.larkoffice.com/docx/OLRKdWFEzoeYtAxWeuZlwEGygVe`, `https://bytedance.sg.larkoffice.com/docx/Nm6kdyVjboyC6yxS1VvlEEejgG7`, `https://bytedance.sg.larkoffice.com/docx/CUUednSAPo4Vyaxne7dlmbCbgZe` |
| Merchandise Mart | merchandise insight and reporting behavior | `modules/merchandise-mart.md` | `https://bytedance.sg.larkoffice.com/docx/Rr4AdFQN9o6rKxxj9JSlLCSrg5f` |
| Catalog Analytics | catalog reporting and export consistency | `modules/catalog-analytics.md` | `https://bytedance.larkoffice.com/wiki/BwruwhM4Yif2W1kaYTEcHaREn6f` |
| Post Campaign Report | reporting output, export, freshness, consistency | `modules/post-campaign-report.md` | `https://bytedance.sg.larkoffice.com/docx/RhHIdMos0oe8I5xxSXOlMn99gTc` |

## Shared Sources

- `TTMS Business & Quality Sharing`: `https://bytedance.larkoffice.com/wiki/Im2OwreOZit7glku2SucUiFHn4g`
- `TTMS OnePage`: `https://bytedance.larkoffice.com/wiki/EBq4wzHzZigoKckFt4YcaDoInJc`
```

- [ ] **Step 5: Write `references/domain/modules/ttms/shared-context.md`**

```md
# TTMS Shared Context

Use this file only when TTMS-wide understanding is needed across modules.

## Typical Use Cases

- clarify TTMS-wide terms or collaboration models
- understand cross-module relationships
- identify release-critical end-to-end paths
- supplement shared quality expectations

## Shared Concepts

### Roles
- internal users
- external users
- operational roles
- approval roles

### Cross-Module Concerns
- upstream and downstream continuity across TTMS flows
- status-driven visibility
- permission-gated actions
- shared reporting consistency
- invitation and onboarding dependencies

## Shared Validation Heuristics

Use only when relevant:
- required vs optional fields
- valid vs invalid inputs
- minimum, maximum, and boundary values
- empty, null, duplicate, and malformed data
- file upload validation
- state transitions
- status gating
- branch conditions
- retry and dependency failure handling
- role-based action visibility
- search, filter, sort, and pagination
- table, card, chart, and drill-down consistency
- export, invitation, and onboarding flows
- empty, loading, and partial-data states
- metric definitions and glossary consistency
- benchmark behavior
- date-range logic and aggregation consistency

## Shared Sources

- `TTMS Business & Quality Sharing`: `https://bytedance.larkoffice.com/wiki/Im2OwreOZit7glku2SucUiFHn4g`
- `TTMS OnePage`: `https://bytedance.larkoffice.com/wiki/EBq4wzHzZigoKckFt4YcaDoInJc`
```

- [ ] **Step 6: Verify the entry files exist and are non-empty**

Run: `find references/domain/modules/ttms -maxdepth 1 -type f | sort`
Expected:

```text
references/domain/modules/ttms/index.md
references/domain/modules/ttms/module-map.md
references/domain/modules/ttms/shared-context.md
```

- [ ] **Step 7: Commit the entry-file creation**

```bash
git add references/domain/modules/ttms/index.md \
  references/domain/modules/ttms/module-map.md \
  references/domain/modules/ttms/shared-context.md
git commit -m "docs(domain): add TTMS progressive entry files"
```

## Task 2: Split Nomination Center, Brand Diagnosis, and Audience

**Files:**
- Create: `references/domain/modules/ttms/modules/nomination-center.md`
- Create: `references/domain/modules/ttms/modules/brand-diagnosis.md`
- Create: `references/domain/modules/ttms/modules/audience.md`

- [ ] **Step 1: Write `references/domain/modules/ttms/modules/nomination-center.md`**

```md
# TTMS Module: Nomination Center

Use this file only when the feature involves nomination onboarding, qualification gating, invite activation, or related status-driven actions.

## Use This Module For

- nomination creation and submission flows
- qualification upload and validation
- trademark owner vs authorized representative branches
- invite-link visibility and activation constraints
- internal vs external visibility differences

## Business Semantics

### Core Workflow
- nomination creation
- qualification submission
- processing and review progression
- invite availability and activation

### Important Branches
- trademark owner vs authorized representative
- brand-exclusive vs brand-mixed

### Status and Visibility Rules
- processing status transitions gate downstream actions
- qualification review status gates invite-link visibility
- account ID rules may affect onboarding completion

## Testing Prompts

Prioritize:
- nomination creation and submission flows
- qualification branch validation
- invite activation constraints
- status-driven action visibility
- account ID field rules

High-risk failure patterns:
- invite link shown before upstream statuses are ready
- qualification branch logic diverges by owner type
- status-driven actions appear for the wrong role
- onboarding blockers caused by hidden validation rules

Typical P0 candidates:
- merchant cannot complete onboarding due to broken nomination or invite gating
- critical action becomes invisible to the right user at the right status

## Source Links

- `Nomination Center`: `https://bytedance.larkoffice.com/wiki/HAe9wqk5hiCLPJkp8GvcgpL9nw4`
- `Trademark Standard Format`: `https://bytedance.sg.larkoffice.com/docx/OFlidUACLoWKntxlXmJcFYLGn7f`
- `Brand Qualification Guidance`: `https://bytedance.sg.larkoffice.com/docx/IK52dqVU8oaCQGxOz04lrLCNgzd`

## Notes For Agent Usage

- Prefer explicit requirement and technical docs first.
- Use this file only to fill TTMS-specific semantic gaps.
- If this file materially shaped the answer, mention it explicitly.
```

- [ ] **Step 2: Write `references/domain/modules/ttms/modules/brand-diagnosis.md`**

```md
# TTMS Module: Brand Diagnosis

Use this file only when the feature affects funnel metrics, benchmark logic, or reporting consistency.

## Use This Module For

- funnel grouping semantics
- metric glossary correctness
- campaign mapping logic
- benchmark-dependent behavior
- cross-view reporting consistency

## Business Semantics

### Core Workflow
- interpret premium reach, massive reach, consideration, and conversion
- apply benchmark-dependent metric logic
- compare summary and detail reporting views

### Important Branches
- with benchmark vs without benchmark
- summary cards vs detail tables and charts

### Status and Visibility Rules
- glossary and displayed metric values must stay aligned
- benchmark changes must not silently alter downstream meaning

## Testing Prompts

Prioritize:
- funnel grouping correctness
- glossary and tooltip consistency
- campaign mapping classification
- benchmark-dependent metric behavior
- cross-card, chart, and glossary consistency

High-risk failure patterns:
- metric definitions differ across views
- benchmark changes silently alter downstream values
- glossary text and displayed calculations drift apart

Typical P0 candidates:
- core reporting metrics become materially incorrect for decision-making
- summary and detail views disagree on key business numbers

## Source Links

- `Brand Diagnosis`: `https://bytedance.sg.larkoffice.com/docx/TEFzdBzFYofX7hxRakxlE4Qvgzf`

## Notes For Agent Usage

- Prefer explicit requirement and technical docs first.
- Use this file only to fill TTMS-specific semantic gaps.
- If this file materially shaped the answer, mention it explicitly.
```

- [ ] **Step 3: Write `references/domain/modules/ttms/modules/audience.md`**

```md
# TTMS Module: Audience

Use this file only when the feature affects ACC journeys, transition analysis, or model-driven audience behavior.

## Use This Module For

- ACC stage definitions and transitions
- diagram and table toggle semantics
- drill-down flows
- touchpoint, creator, and video insight sections
- model-specific audience analysis

## Business Semantics

### Core Workflow
- select an ACC model
- inspect journey and transition stages
- switch between visual and tabular views
- drill into downstream audience details

### Important Branches
- Web Payment
- Web Payment and Registration
- App Payment
- Ticketing
- past 7, 15, and 30 day windows

### Status and Visibility Rules
- selected stage or journey must propagate to downstream views
- selected model and time window must stay consistent across related components

## Testing Prompts

Prioritize:
- ACC stage definitions and transition logic
- transition tiles and diagram or table toggle behavior
- drill-down flows
- touchpoint, creator, and video insight sections
- time-window and model-specific behavior

High-risk failure patterns:
- selected stage or journey does not propagate to downstream views
- time-window switching causes inconsistent metrics or segmentation
- drill-down results do not match summary tiles

Typical P0 candidates:
- core transition analysis cannot be completed end to end
- selected model or time window produces materially wrong audience results

## Source Links

- `Audience`: `https://bytedance.sg.larkoffice.com/docx/K5azdNO98oWMqYxTuHLlHLrkgbf`

## Notes For Agent Usage

- Prefer explicit requirement and technical docs first.
- Use this file only to fill TTMS-specific semantic gaps.
- If this file materially shaped the answer, mention it explicitly.
```

- [ ] **Step 4: Verify the three module files contain `Testing Prompts` and `Source Links`**

Run: `rg -n "## Testing Prompts|## Source Links" references/domain/modules/ttms/modules/{nomination-center,brand-diagnosis,audience}.md`
Expected: 6 matching lines across 3 files

- [ ] **Step 5: Commit the first module split**

```bash
git add references/domain/modules/ttms/modules/nomination-center.md \
  references/domain/modules/ttms/modules/brand-diagnosis.md \
  references/domain/modules/ttms/modules/audience.md
git commit -m "docs(domain): split core TTMS module references"
```

## Task 3: Split Brand Perception, Merchandise Mart, Catalog Analytics, and Post Campaign Report

**Files:**
- Create: `references/domain/modules/ttms/modules/brand-perception.md`
- Create: `references/domain/modules/ttms/modules/merchandise-mart.md`
- Create: `references/domain/modules/ttms/modules/catalog-analytics.md`
- Create: `references/domain/modules/ttms/modules/post-campaign-report.md`

- [ ] **Step 1: Write `references/domain/modules/ttms/modules/brand-perception.md`**

```md
# TTMS Module: Brand Perception

Use this file only when the change touches insight browsing, reporting, export, or content synchronization across Brand Perception views.

## Use This Module For

- filter combinations and segmentation dimensions
- table and chart synchronization
- metric explanation correctness
- data freshness and partial-data behavior
- export workflow correctness

## Business Semantics

### Core Workflow
- select a perception sub-view such as Brand Insights, Search Insights, Vertical Insights, or Tentpole Strategy
- apply filters and segmentation dimensions
- compare synchronized table and chart output
- export or report selected insight results

### Important Branches
- Brand Insights
- Search Insights
- Vertical Insights
- Tentpole Strategy

### Status and Visibility Rules
- filters must affect all linked components consistently
- freshness messaging must reflect real data completeness

## Testing Prompts

Prioritize:
- filter combinations and segmentation dimensions
- table and chart synchronization
- metric explanation correctness
- data freshness and partial-data behavior
- export workflow correctness

High-risk failure patterns:
- filters affect one component but not another
- export output does not match on-screen selection
- data freshness messaging is absent or misleading

Typical P0 candidates:
- exported or externally delivered report is materially wrong
- a release breaks the main customer-facing insight workflow

## Source Links

- `Brand Insights`: `https://bytedance.sg.larkoffice.com/docx/L6O0drMbmo6d1vxFcAKcS4SPn1c`
- `Search Insights`: `https://bytedance.sg.larkoffice.com/docx/OLRKdWFEzoeYtAxWeuZlwEGygVe`
- `Vertical Insights`: `https://bytedance.sg.larkoffice.com/docx/Nm6kdyVjboyC6yxS1VvlEEejgG7`
- `Tentpole Strategy`: `https://bytedance.sg.larkoffice.com/docx/CUUednSAPo4Vyaxne7dlmbCbgZe`

## Notes For Agent Usage

- Prefer explicit requirement and technical docs first.
- Use this file only to fill TTMS-specific semantic gaps.
- If this file materially shaped the answer, mention it explicitly.
```

- [ ] **Step 2: Write the remaining three module files with the same template shape**

```md
# TTMS Module: Merchandise Mart

Use this file only when the change touches merchandise insight browsing, reporting, export, or content synchronization across Merchandise Mart views.

## Use This Module For

- merchandise insight browsing
- filter and segmentation behavior
- table and chart synchronization
- data freshness messaging
- export and reporting correctness

## Business Semantics

### Core Workflow
- open merchandise insight views
- apply filters and segmentation dimensions
- compare synchronized table and chart output
- export or report selected merchandise insight results

### Important Branches
- filter combinations
- segmented vs unsegmented views
- on-screen browsing vs exported output

### Status and Visibility Rules
- filters must affect all linked components consistently
- freshness and empty-state messaging must reflect real data completeness

## Testing Prompts

Prioritize:
- merchandise insight browsing
- filter and segmentation behavior
- table and chart synchronization
- data freshness messaging
- export and reporting correctness

High-risk failure patterns:
- filters affect one component but not another
- export output does not match on-screen selection
- data freshness messaging is absent or misleading

Typical P0 candidates:
- exported or externally delivered report is materially wrong
- the main merchandise insight workflow is broken for customer-facing usage

## Source Links

- `Merchandise Mart`: `https://bytedance.sg.larkoffice.com/docx/Rr4AdFQN9o6rKxxj9JSlLCSrg5f`

## Notes For Agent Usage

- Prefer explicit requirement and technical docs first.
- Use this file only to fill TTMS-specific semantic gaps.
- If this file materially shaped the answer, mention it explicitly.
```

```md
# TTMS Module: Catalog Analytics

Use this file only when the change touches catalog reporting, export, or content synchronization across Catalog Analytics views.

## Use This Module For

- catalog reporting workflows
- export consistency
- metric explanation correctness
- data freshness and partial-data behavior
- filter-driven cross-view consistency

## Business Semantics

### Core Workflow
- open catalog reporting views
- apply filters and dimensions
- compare synchronized table and chart output
- export or report selected catalog metrics

### Important Branches
- filtered vs unfiltered reporting
- on-screen analysis vs exported output
- full-data vs partial-data scenarios

### Status and Visibility Rules
- filters must affect all linked reporting components consistently
- freshness messaging must reflect partial-data and stale-data states honestly

## Testing Prompts

Prioritize:
- catalog reporting workflows
- export consistency
- metric explanation correctness
- data freshness and partial-data behavior
- filter-driven cross-view consistency

High-risk failure patterns:
- filters affect one component but not another
- export output does not match on-screen selection
- data freshness messaging is absent or misleading

Typical P0 candidates:
- exported or externally delivered catalog report is materially wrong
- a release breaks the main catalog analysis workflow

## Source Links

- `Catalog Analytics`: `https://bytedance.larkoffice.com/wiki/BwruwhM4Yif2W1kaYTEcHaREn6f`

## Notes For Agent Usage

- Prefer explicit requirement and technical docs first.
- Use this file only to fill TTMS-specific semantic gaps.
- If this file materially shaped the answer, mention it explicitly.
```

```md
# TTMS Module: Post Campaign Report

Use this file only when the change touches post-campaign reporting, export, or delivered-report consistency.

## Use This Module For

- post-campaign reporting workflows
- reporting output and export correctness
- data freshness semantics
- filter and date-range consistency
- externally delivered report validation

## Business Semantics

### Core Workflow
- open post-campaign reporting views
- apply filters and date ranges
- compare on-screen report sections and summary components
- export or deliver the final report

### Important Branches
- filtered vs unfiltered reporting
- on-screen report vs exported or delivered report
- full-data vs partial-data reporting

### Status and Visibility Rules
- filters and date ranges must stay consistent across report sections
- freshness messaging must reflect delivery readiness and data completeness

## Testing Prompts

Prioritize:
- post-campaign reporting workflows
- reporting output and export correctness
- data freshness semantics
- filter and date-range consistency
- externally delivered report validation

High-risk failure patterns:
- filters affect one component but not another
- delivered report does not match on-screen selection
- freshness messaging is absent or misleading

Typical P0 candidates:
- exported or externally delivered report is materially wrong
- a release breaks the main post-campaign reporting workflow

## Source Links

- `Post Campaign Report`: `https://bytedance.sg.larkoffice.com/docx/RhHIdMos0oe8I5xxSXOlMn99gTc`

## Notes For Agent Usage

- Prefer explicit requirement and technical docs first.
- Use this file only to fill TTMS-specific semantic gaps.
- If this file materially shaped the answer, mention it explicitly.
```

Use these exact section headings in all three files:

```md
## Use This Module For
## Business Semantics
### Core Workflow
### Important Branches
### Status and Visibility Rules
## Testing Prompts
## Source Links
## Notes For Agent Usage
```

- [ ] **Step 3: Verify the remaining three module files use the required section headings**

Run: `rg -n "## Use This Module For|## Business Semantics|### Core Workflow|### Important Branches|### Status and Visibility Rules|## Testing Prompts|## Source Links|## Notes For Agent Usage" references/domain/modules/ttms/modules/{merchandise-mart,catalog-analytics,post-campaign-report}.md`
Expected: 24 matching lines across the 3 files

- [ ] **Step 4: Verify all seven module files exist**

Run: `find references/domain/modules/ttms/modules -maxdepth 1 -type f | sort`
Expected:

```text
references/domain/modules/ttms/modules/audience.md
references/domain/modules/ttms/modules/brand-diagnosis.md
references/domain/modules/ttms/modules/brand-perception.md
references/domain/modules/ttms/modules/catalog-analytics.md
references/domain/modules/ttms/modules/merchandise-mart.md
references/domain/modules/ttms/modules/nomination-center.md
references/domain/modules/ttms/modules/post-campaign-report.md
```

- [ ] **Step 5: Commit the remaining module split**

```bash
git add references/domain/modules/ttms/modules/brand-perception.md \
  references/domain/modules/ttms/modules/merchandise-mart.md \
  references/domain/modules/ttms/modules/catalog-analytics.md \
  references/domain/modules/ttms/modules/post-campaign-report.md
git commit -m "docs(domain): add remaining TTMS module references"
```

## Task 4: Update The Domain Retriever And Remove The Legacy Flat File

**Files:**
- Modify: `references/domain/SKILL.md`
- Delete: the legacy single-file TTMS reference

- [ ] **Step 1: Update the progressive disclosure section in `references/domain/SKILL.md`**

Replace:

```md
Current maintained modules:

- the previous flat TTMS entry
```

With:

```md
Current maintained modules:

- `modules/ttms/index.md`

For TTMS:
- read `modules/ttms/index.md` first
- read `modules/ttms/shared-context.md` only when TTMS-wide context is needed
- use `modules/ttms/module-map.md` to locate the correct module file
- read only the matching file under `modules/ttms/modules/`
```

- [ ] **Step 2: Keep the workflow focused on the new TTMS entry path**

Ensure `references/domain/SKILL.md` still contains this workflow shape:

```md
1. Identify the domain, module, term, workflow, metric, or business question that needs clarification.
2. Read only the matching module and relevant sections.
3. Return a concise summary of the knowledge needed for the current task.
4. Separate confirmed reference-backed knowledge from missing information or assumptions.
5. Cite the exact module that informed the answer.
```

- [ ] **Step 3: Delete the legacy flat TTMS file**

Run: remove the legacy flat TTMS file from the domain modules directory
Expected: command exits `0`

- [ ] **Step 4: Verify no repository references still point to the old flat file**

Run: `rg -n "modules/ttms\.md" references docs`
Expected: no matches

- [ ] **Step 5: Verify the new entry path is referenced by the retriever**

Run: `rg -n "modules/ttms/index.md|modules/ttms/module-map.md|modules/ttms/modules/" references/domain/SKILL.md`
Expected: 3 matching lines in `references/domain/SKILL.md`

- [ ] **Step 6: Commit the retriever update and legacy removal**

```bash
git add references/domain/SKILL.md
git rm <legacy-flat-ttms-reference>
git commit -m "refactor(domain): switch TTMS reference to progressive structure"
```

## Task 5: Final Verification

**Files:**
- Verify: `references/domain/SKILL.md`
- Verify: `references/domain/modules/ttms/`

- [ ] **Step 1: Verify the TTMS file tree**

Run: `find references/domain/modules/ttms -maxdepth 2 -type f | sort`
Expected:

```text
references/domain/modules/ttms/index.md
references/domain/modules/ttms/module-map.md
references/domain/modules/ttms/modules/audience.md
references/domain/modules/ttms/modules/brand-diagnosis.md
references/domain/modules/ttms/modules/brand-perception.md
references/domain/modules/ttms/modules/catalog-analytics.md
references/domain/modules/ttms/modules/merchandise-mart.md
references/domain/modules/ttms/modules/nomination-center.md
references/domain/modules/ttms/modules/post-campaign-report.md
references/domain/modules/ttms/shared-context.md
```

- [ ] **Step 2: Verify shared loading rules and module notes are present**

Run: `rg -n "Read this directory only when|Use this file only when|If this file materially shaped the answer" references/domain/modules/ttms references/domain/modules/ttms/modules`
Expected: matches in `index.md` and all module files

- [ ] **Step 3: Verify git diff shape**

Run: `git diff --stat HEAD~4..HEAD`
Expected: shows creation of the TTMS directory tree, modification of `references/domain/SKILL.md`, and deletion of the legacy flat TTMS file

- [ ] **Step 4: Verify working tree is clean after the final commit**

Run: `git status --short`
Expected: no output

- [ ] **Step 5: Record the implementation result**

```bash
git log --oneline -n 4
```

Expected: the latest 4 commits should reflect:

- entry-file creation
- first module split
- remaining module split
- retriever update and legacy removal

## Self-Review Checklist

- Spec coverage:
  - progressive structure covered by Tasks 1-4
  - module split covered by Tasks 2-3
  - retriever update and legacy removal covered by Task 4
  - verification and cleanliness covered by Task 5
- Placeholder scan:
  - no `TODO` or `TBD`
  - all paths are explicit
  - all verification commands are concrete
- Consistency:
  - single entry path is `references/domain/modules/ttms/index.md`
  - all module files live under `references/domain/modules/ttms/modules/`
