# Multi-Candidate Rules

Read this file when dual-candidate mode is triggered or when adjudicating multiple candidate case trees.

## Mandatory Trigger

Dual-candidate mode is mandatory when any of the following is true:

- the request is both cross-module and high-risk
- the request touches 4 or more stable modules or workflows
- the request includes 2 or more of: permissions, state transitions, export, external dependency failure, data correctness, multi-view switching, multi-role switching
- the same or similar prompt has already shown unstable grouping, coverage, or priority behavior across runs

When one mandatory condition is met:

- do not use single-pass mode
- do not explain away the complexity and proceed with one draft anyway
- always produce Candidate A and Candidate B before adjudication
- do not treat “thinking from two perspectives” as dual-candidate mode
- each candidate must have its own explicit candidate summary and normalized case-tree draft before adjudication starts

## Execution Gate

Before finalizing, check these gates:

- Candidate A exists as a separate draft
- Candidate B exists as a separate draft
- Candidate A and Candidate B have different roles and tradeoffs
- a coverage ledger exists for the target module set
- a per-module case budget exists before leaf cases are finalized
- an adjudication table exists
- final decision notes identify the structural base, coverage additions, rejected candidate-only cases, and grouping fixes
- the final tree records which candidate supplied kept unique cases
- weak, duplicate, or over-broad cases were explicitly dropped
- budget variance notes exist for any module outside its planned range
- raw candidate drafts and adjudication notes are hidden from the user-facing response unless the user explicitly asks for debugging output

If any gate is missing, dual-candidate mode was not completed. Return to candidate generation or mark the run as single-pass internally; do not claim dual-candidate compliance.

## Candidate Split

Candidate A: `coverage-first`

- broader workflow decomposition
- stronger exception and dependency-failure expansion
- more explicit permission, state-transition, and rollback coverage
- catches likely omissions even if some cases later need pruning

Candidate B: `quality-first`

- tighter one-intent-per-case discipline
- stronger expectation quality and setup clarity
- stricter rejection of weak boundary cases
- cleaner group lineage and lower duplication

## Required Internal Artifacts

Dual-candidate mode requires three internal artifacts:

1. Candidate A draft
2. Candidate B draft
3. Coverage ledger, adjudication table, and final normalized case tree

Each candidate draft must include:

- candidate role: `coverage-first` or `quality-first`
- module tree outline
- retained assumptions
- recommended cases
- known weaknesses or overreach risks

The adjudication table must include:

- shared high-value cases
- candidate-only cases worth keeping
- duplicates or weak cases to drop
- priority conflicts to resolve
- grouping or lineage fixes
- final decision notes

The final decision notes must explicitly say:

- which candidate provided the structural base
- which candidate provided coverage additions
- which candidate-only cases were rejected and why
- whether the top-level module tree remained compact
- whether residual checks were filed under `其他` or backfilled into owning modules
- whether each target module stayed inside its planned case budget or needed a variance note

If `Agent` or `Task` is available, actually spawn Candidate A and Candidate B as independent analysis tracks. If no subagent mechanism is available, produce two separate internal drafts serially with the same candidate schema; do not collapse them into one blended draft.

## Stability Convergence

For prompts that previously produced unstable output, adjudication must converge the final tree before writing cases:

- choose a compact target top-level module set before expanding leaf cases
- create a coverage ledger and per-module case budget for that module set
- rename near-synonym modules to the target names instead of allowing run-to-run wording drift
- keep child pages, detail pages, drawers, and drill-downs under the parent module
- backfill audit-style coverage into owning modules before creating new top-level groups
- use at most one `其他` bucket for residual checks that are real but do not belong to a stable module
- compare final top-level groups against the target module set and explain any intentional deviation in internal notes
- compare final per-module case counts against budget and explain any variance

Do not use dual-candidate mode to inflate case count. Its purpose is to combine high-value coverage with a stable, reviewable final structure.

## Adjudication Rubric

When merging candidate outputs, compare them against these dimensions:

- **structure quality:** follows stable product modules and real navigation rather than scattered audit buckets
- **core coverage:** covers the main workflow, key roles, and major state transitions
- **exception coverage:** expands failure, timeout, fallback, rejection, empty-state, partial-data, and dependency-error paths where plausible
- **boundary judgment:** scans real boundaries and includes standalone boundary cases only when justified
- **case quality:** one clear intent with concrete, observable expectations
- **lineage and grouping:** child pages, drill-downs, drawers, and modal flows stay under the correct parent module
- **priority alignment:** priorities reflect impact consistently
- **deduplication:** overlapping or near-duplicate cases are merged or pruned

## Merge Rules

- choose the cleaner module tree as the structural base when one candidate is clearly easier to read and maintain
- map both candidates into the same coverage ledger before deciding which leaf cases to keep
- keep cases that both candidates surfaced unless they duplicate the same intent
- keep unique cases from only one candidate when they close a meaningful coverage gap or materially improve correctness
- backfill high-value permissions, exceptions, consistency checks, and dependency-failure cases into the relevant module rather than creating a new top-level bucket by default
- collapse residual page-interaction, parameter-validation, and generic exception cases into `其他` when doing so improves structural stability without hiding ownership
- drop cases that are thin, redundant, vague, or only inflate the count without adding signal
- resolve priority conflicts by re-grading against `references/priority-rubric.md`, not by averaging candidate opinions
- avoid leaving several small audit buckets at the top level when one `其他` bucket would better match the reference structure and maintenance style
- produce one final normalized case tree for XMind generation; do not keep candidate provenance in the user-facing artifact

## Common Failure

Invalid dual-candidate behavior:

```text
“I considered coverage-first and quality-first while drafting the final case tree.”
```

This is not dual-candidate mode because there are no independent drafts and no adjudication artifact.

Valid dual-candidate behavior:

```text
Candidate A draft -> Candidate B draft -> adjudication table -> final normalized case tree
```
