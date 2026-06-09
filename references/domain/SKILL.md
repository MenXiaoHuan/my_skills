---
name: "domain-reference-retriever"
description: "Find and summarize maintained business-domain reference knowledge when requirements or technical materials do not fully explain terms, workflows, role definitions, metrics, status logic, or module context."
---

# Domain Reference Retriever

Use this skill to locate and summarize domain-specific knowledge from maintained documents under `modules/`.

This skill is for knowledge lookup. It supplements requirement and technical materials when domain semantics are missing or ambiguous.

## Use This Skill When

- A task is blocked by missing business terms, workflow semantics, role definitions, metric meanings, status logic, or module context.
- The user asks what a module, business concept, state, or metric means.
- Another skill needs supplementary domain context before generating tests, analysis, or design output.

## Do Not Use This Skill When

- The user already provided complete and current requirement or technical materials.
- The question is mainly about API contract behavior. Use `api-reference-retriever`.
- The question is mainly about system topology or cross-service architecture. Use `architecture-reference-retriever`.

## Progressive Disclosure

Read only the matching module under `modules/`.

Current maintained modules:

- `modules/ttms/index.md`

For TTMS:
- read `modules/ttms/index.md` first
- read `modules/ttms/shared-context.md` only when TTMS-wide context is needed
- use `modules/ttms/module-map.md` to locate the correct module file
- read only the matching file under `modules/ttms/modules/`

As this repository grows, add more domain modules under `modules/` and read only the relevant one.

## Default Workflow

1. Identify the domain, module, term, workflow, metric, or business question that needs clarification.
2. Read only the matching module and relevant sections.
3. Return a concise summary of the knowledge needed for the current task.
4. Separate confirmed reference-backed knowledge from missing information or assumptions.
5. Cite the exact module that informed the answer.

## Failure Handling

If no relevant knowledge source exists, say that directly and ask for the missing source instead of inventing business semantics.

If a maintained reference conflicts with explicit requirement or technical documents, treat the requirement or technical document as higher priority and call out the conflict explicitly.
