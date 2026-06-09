# TTMS Domain Reference Structure Design

## Background

The current TTMS business-domain reference lives in a single file:

- the legacy single-file TTMS reference

That file currently mixes multiple responsibilities:

- entry and usage rules
- TTMS-wide shared context
- module discovery and source mapping
- module-specific business knowledge
- cross-cutting coverage heuristics
- attribution guidance

This shape is workable for a small seed document, but it does not fit the intended long-term usage pattern for Agent-driven knowledge lookup. The target usage model is progressive loading: the Agent should read the smallest amount of TTMS reference material needed for the current task.

## Goal

Restructure TTMS domain knowledge under `references/domain/modules/ttms/` so the content becomes structured reference material for Agents, optimized for progressive disclosure and selective loading.

## Non-Goals

- Turning TTMS references into a human-oriented comprehensive handbook
- Replacing requirement or technical design documents as the source of truth
- Introducing deep per-module subtrees before the knowledge volume justifies it
- Changing the substance of TTMS business knowledge beyond necessary normalization

## Design Principles

### Requirement and Technical Materials Stay Primary

TTMS domain references remain supplementary. If requirement or technical documents exist, they stay higher priority than any maintained domain reference.

### Progressive Loading First

The expected read path is:

1. `index.md`
2. `module-map.md`
3. `shared-context.md` only if TTMS-wide context is needed
4. one matching file under `modules/`

The structure must discourage loading all TTMS knowledge by default.

### One File, One Responsibility

Each file should own one layer of knowledge:

- index and loading rules
- module discovery and source mapping
- TTMS-wide shared context
- single-module business knowledge

### Source Traceability

Every module file must retain its own source links. Source links should not live only in one central file, because that makes module-level attribution weaker and harder to maintain.

## Proposed Structure

```text
references/domain/modules/
└── ttms/
    ├── index.md
    ├── module-map.md
    ├── shared-context.md
    └── modules/
        ├── nomination-center.md
        ├── brand-diagnosis.md
        ├── audience.md
        ├── brand-perception.md
        ├── merchandise-mart.md
        ├── catalog-analytics.md
        └── post-campaign-report.md
```

## File Responsibilities

### `index.md`

Purpose:

- define when TTMS references should be used
- define the loading order
- explain what TTMS references can and cannot answer
- define attribution rules

Must not contain:

- long-form module knowledge
- module-specific heuristics
- source tables for every module in detail

### `module-map.md`

Purpose:

- map business modules to file paths
- state when each module file should be used
- provide a concise pointer to the primary source links

Must not contain:

- deep business explanations
- detailed workflow semantics

### `shared-context.md`

Purpose:

- hold TTMS-wide shared concepts
- describe cross-module concerns
- store truly shared heuristics that apply across multiple TTMS modules

Must not contain:

- module-specific behavior that belongs in a single module file

### `modules/*.md`

Purpose:

- store one module's business semantics
- define module-specific testing prompts
- capture module-specific risk patterns
- preserve module-level source links

Each module file should be independently readable after the Agent reaches it through `module-map.md`.

## Standard Templates

### Template: `index.md`

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

### Template: `module-map.md`

```md
# TTMS Module Map

Use this file to locate the correct TTMS module reference. Do not use it as the final business source when a deeper module file exists.

| Module | Use When | File | Primary Sources |
| --- | --- | --- | --- |
| Nomination Center | nomination onboarding, qualification gating, invite activation | `modules/nomination-center.md` | `https://...` |
| Brand Diagnosis | funnel metrics, benchmark logic, reporting consistency | `modules/brand-diagnosis.md` | `https://...` |
| Audience | ACC journeys, transition analysis, model-specific behavior | `modules/audience.md` | `https://...` |
| Brand Perception | insight browsing, filter logic, data sync | `modules/brand-perception.md` | `https://...` |
| Merchandise Mart | merchandise insight and reporting behavior | `modules/merchandise-mart.md` | `https://...` |
| Catalog Analytics | catalog reporting and export consistency | `modules/catalog-analytics.md` | `https://...` |
| Post Campaign Report | reporting output, export, freshness, consistency | `modules/post-campaign-report.md` | `https://...` |

## Shared Sources

- `TTMS Business & Quality Sharing`: `https://...`
- `TTMS OnePage`: `https://...`
```

### Template: `shared-context.md`

```md
# TTMS Shared Context

Use this file only when TTMS-wide understanding is needed across modules.

## Typical Use Cases

- clarify TTMS-wide terms
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
- upstream and downstream continuity
- status-driven visibility
- permission-gated actions
- shared reporting consistency
- invitation and onboarding dependencies

## Shared Validation Heuristics

Use only when relevant:
- required vs optional fields
- state transitions
- approval and retry behavior
- empty, loading, and partial-data states
- table, card, chart, and drill-down consistency
- date-range and aggregation consistency

## Shared Sources

- `TTMS Business & Quality Sharing`: `https://...`
- `TTMS OnePage`: `https://...`
```

### Template: module file

The angle-bracket placeholders below are intentional template markers for future module authors. They are not unresolved items in this design.

```md
# TTMS Module: <Module Name>

Use this file only when the feature involves <module scope>.

## Use This Module For

- <scenario>
- <scenario>
- <scenario>

## Business Semantics

### Core Workflow
- <step or state>
- <step or state>

### Important Branches
- <branch>
- <branch>

### Status and Visibility Rules
- <rule>
- <rule>

## Testing Prompts

Prioritize:
- <focus area>
- <focus area>

High-risk failure patterns:
- <risk>
- <risk>

Typical P0 candidates:
- <P0 scenario>
- <P0 scenario>

## Source Links

- `<source name>`: `https://...`

## Notes For Agent Usage

- Prefer explicit requirement and technical docs first.
- Use this file only to fill TTMS-specific semantic gaps.
- If this file materially shaped the answer, mention it explicitly.
```

## Migration Mapping From The Current File

Current source file:

- the legacy single-file TTMS reference

Recommended extraction mapping:

- lines 1-22 -> `ttms/index.md`
- lines 23-35 -> `ttms/shared-context.md`
- lines 36-56 -> `ttms/module-map.md` plus per-module source sections
- lines 62-84 -> `ttms/modules/nomination-center.md`
- lines 86-104 -> `ttms/modules/brand-diagnosis.md`
- lines 106-125 -> `ttms/modules/audience.md`
- lines 127-146 -> split into:
  - `ttms/modules/brand-perception.md`
  - `ttms/modules/merchandise-mart.md`
  - `ttms/modules/catalog-analytics.md`
  - `ttms/modules/post-campaign-report.md`
- lines 148-198 -> `ttms/shared-context.md`
- lines 200-231 -> `ttms/index.md` and each module file's usage notes

## Migration Steps

1. Create `references/domain/modules/ttms/` and `references/domain/modules/ttms/modules/`.
2. Create `index.md`, `module-map.md`, and `shared-context.md` using the standardized templates.
3. Split module-specific guidance from the current `ttms.md` into individual files under `modules/`.
4. Copy module-specific source links into each corresponding module file.
5. Move only truly cross-module heuristics into `shared-context.md`.
6. Update `references/domain/SKILL.md` so progressive disclosure points to `modules/ttms/index.md` instead of the previous flat TTMS entry.
7. Replace the legacy single-file TTMS reference with one of the following:
   - preferred: remove it entirely
   - fallback: keep a short compatibility shim that points to `modules/ttms/index.md`

## Compatibility Decision

Recommended choice: remove the legacy `ttms.md` after the retriever skill has been updated.

Reason:

- keeping two entry points increases the chance that Agents continue reading the old flat file
- the new structure is intended to become the single authoritative TTMS domain entry

Use a compatibility shim only if another maintained tool still hardcodes the old path.

## Risks And Mitigations

### Risk: Over-splitting the content

If files become too granular, the Agent may need too many reads for a single question.

Mitigation:

- keep one file per module, not one file per subsection
- keep shared concepts in one TTMS-wide file

### Risk: Source drift between map and module files

If source links are updated in only one location, the reference becomes inconsistent.

Mitigation:

- use `module-map.md` for concise discovery
- treat each module file as the authoritative local source list for that module

### Risk: Shared heuristics swallowing module semantics

If shared-context grows too much, it becomes another monolithic file.

Mitigation:

- move any module-specific rule back into the corresponding module file
- keep `shared-context.md` limited to TTMS-wide concepts only

## Success Criteria

The design is successful when:

- an Agent can find the correct TTMS module without loading unrelated content
- the loading order is explicit and stable
- source attribution remains possible at module level
- requirement and technical documents remain clearly higher priority than TTMS references
- the new structure is simpler to extend than the current single-file layout
