# Coverage Ledger Rules

Read this file when a broad prompt has shown leaf-case count drift, or when dual-candidate mode is active for a multi-module requirement.

## Purpose

A coverage ledger stabilizes the final case tree before detailed cases are written. It is not user-facing by default.

Use it to lock three things:

- target top-level modules
- required coverage dimensions per module
- expected case budget per module

The goal is stable, high-value coverage, not an exact global case count.

## Required Ledger

Before expanding leaf cases, create an internal table with:

- module name
- required dimensions: `core`, `data_correctness`, `exception`, `empty_state`
- conditional dimensions: `permission`, `export`, `state_transition`, `dependency_failure`, `boundary`, `multi_view`
- planned case budget: `[min, max]`
- notes for dimensions intentionally skipped

For BP3.0 Market Competitive Landscape style prompts, start from this module set unless the source material clearly differs:

- `全局筛选器`
- `Market Landscape`
- `Trend Analysis`
- `Audience Persona`
- `Competitive Landscape`
- `Creative Insights`
- `Creators Insights`
- `其他`

## Budget Rules

- Use a range, not a fixed number. A range allows valid consolidation without hiding large drift.
- Keep final module case counts inside the planned range unless the source material introduces a concrete new workflow.
- If the final count is outside budget, record a budget variance note before finalizing.
- Do not add thin cases just to hit the upper bound.
- Do not drop meaningful exception, data correctness, or empty-state coverage just to hit the lower bound.

## Merge Rules

When adjudicating candidates:

- map both candidates into the same ledger before comparing leaf cases
- compare missing dimensions first, then compare duplicate or thin cases
- keep candidate-only cases when they fill a ledger gap
- drop candidate-only cases when their dimension is already covered by a stronger case
- reject module-name drift before comparing leaf counts

## Final Sweep

Before writing `.xmind`, check:

- every target module has a final case count within budget or a variance note
- every required dimension is covered or intentionally skipped with a reason
- `其他` contains only residual checks and does not hide major module behavior
- total leaf count drift is explainable by budgeted module decisions, not random split/merge behavior
