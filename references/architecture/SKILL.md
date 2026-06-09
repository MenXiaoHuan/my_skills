---
name: "architecture-reference-retriever"
description: "Find and summarize maintained architecture reference knowledge when requirements or technical designs do not fully explain system boundaries, dependencies, data flow, state ownership, async chains, deployment constraints, or cross-service interaction."
---

# Architecture Reference Retriever

Use this skill to locate and summarize architecture-specific reference knowledge from maintained documents under `modules/`.

This skill supplements requirement docs and technical designs. It should not override a current design document for the feature in scope.

## Use This Skill When

- A task is blocked by missing context about system boundaries, upstream and downstream dependencies, data ownership, async links, or cross-service impact.
- Another skill needs architecture context before generating tests, risk analysis, or implementation review points.

## Do Not Use This Skill When

- The current technical design already explains the relevant architecture clearly.
- The question is mainly about business semantics or product workflow meaning. Use `domain-reference-retriever`.
- The question is mainly about API contract details. Use `api-reference-retriever`.

## Progressive Disclosure

Read only the matching module under `modules/`.

Current maintained modules:

- `modules/architecture-reference-catalog.md`

## Default Workflow

1. Identify the system, component, data flow, or dependency concern that needs clarification.
2. Read only the matching module and relevant sections.
3. Return a concise summary tied to the current task.
4. Separate confirmed reference-backed knowledge from assumptions or missing confirmations.
5. Cite the exact module that informed the answer.

## Failure Handling

If no maintained architecture reference exists, say that directly and request the missing design source.
