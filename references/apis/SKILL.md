---
name: "api-reference-retriever"
description: "Find and summarize maintained API reference knowledge when requirements or technical designs do not fully explain contracts, field semantics, auth rules, error models, idempotency, pagination, callbacks, or integration constraints."
---

# API Reference Retriever

Use this skill to locate and summarize API-specific reference knowledge from maintained documents under `modules/`.

This skill supplements requirement docs, API specs, and technical designs. It does not replace them.

## Use This Skill When

- A task is blocked by unclear API contracts, field meanings, auth rules, headers, error codes, idempotency, pagination, or callback semantics.
- Another skill needs stable API reference context before generating tests, integration checks, or review comments.

## Do Not Use This Skill When

- The user already provided a complete and current API spec.
- The question is mainly about business semantics or product workflow meaning. Use `domain-reference-retriever` for that.
- The question is mainly about system topology, component boundaries, or data flow. Use `architecture-reference-retriever` for that.

## Progressive Disclosure

Read only the matching module under `modules/`.

Current maintained modules:

- `modules/api-reference-catalog.md`

## Default Workflow

1. Identify the API domain, endpoint family, or integration concern that needs clarification.
2. Read only the matching module and relevant sections.
3. Return a concise summary focused on the current task.
4. Separate confirmed reference-backed knowledge from missing or assumed details.
5. Cite the exact module that informed the answer.

## Failure Handling

If no maintained API reference exists, say that directly and ask for the missing source instead of inventing contract details.
