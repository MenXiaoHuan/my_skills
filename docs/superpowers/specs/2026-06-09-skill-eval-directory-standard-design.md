# Skill Eval Directory Standard Design

## Goal

Define a repository-level standard for storing, documenting, and evolving skill evaluation assets so that evals are managed consistently across skills instead of being embedded ad hoc inside each skill directory.

## Background

The current repository has one skill-local eval file at `skills/test-case-generator/evals/evals.json`.

That format is workable for a single skill, but it couples runtime skill assets and evaluation assets in one place. As more skills are added, this layout makes it harder to:

- batch-run evals across skills
- apply one shared eval convention
- evolve case structure consistently
- review regressions per skill
- separate "skill runtime assets" from "skill verification assets"

The desired direction is to standardize eval storage at the repository level while keeping each skill's eval pack independently maintainable.

## Design Summary

Adopt a repository-level eval root:

```text
eval/
  skills/
    <skill-name>/
      README.md
      baseline.json
      cases/
        case_001.json
        case_002.json
        route_should_trigger_001.json
        route_should_not_trigger_001.json
```

Keep runtime skill assets in:

```text
skills/<skill-name>/
```

This design establishes a clear responsibility split:

- `skills/<skill-name>/` stores runtime assets used when the skill is invoked
- `eval/skills/<skill-name>/` stores evaluation assets used to verify the skill's behavior

## Design Decisions

### 1. Centralize evals under `eval/skills/`

All skill evals will live under:

```text
eval/skills/
```

Each skill gets its own directory:

```text
eval/skills/<skill-name>/
```

This enables:

- repository-level discoverability
- future batch execution across skills
- consistent review structure
- easier scaling beyond one skill

### 2. Keep eval packs per skill

Each skill's eval assets remain self-contained inside its own eval pack.

Example:

```text
eval/skills/test-case-generator/
```

This keeps ownership and maintenance local to each skill while preserving global consistency.

### 3. Separate examples from eval cases

Do not migrate `examples/` into the eval tree.

Examples and evals serve different purposes:

- `examples/` are few-shot or pattern references for skill behavior
- `eval/cases/` are regression-oriented, pass-fail-oriented evaluation inputs

This separation should remain explicit.

### 4. Use one file per eval case

Do not keep all eval cases in one monolithic JSON file.

Each case should be a standalone JSON file under:

```text
eval/skills/<skill-name>/cases/
```

This improves:

- diff readability
- independent case maintenance
- targeted regression additions
- future filtering by tag or type

### 5. Keep shared rules in `baseline.json`

Shared evaluation rules for one skill should live in:

```text
eval/skills/<skill-name>/baseline.json
```

`baseline.json` is for skill-wide defaults only. It must not become a dumping ground for case-specific expectations.

### 6. Keep human-oriented guidance in `README.md`

Each eval pack should include:

```text
eval/skills/<skill-name>/README.md
```

This file explains:

- what the eval pack is validating
- what is in scope
- what is out of scope
- what counts as pass or fail
- how the pack should be maintained

## Standard File Definitions

### `README.md`

Purpose:

- explain the eval pack
- define scope and pass criteria
- guide future maintainers

Recommended sections:

- `Purpose`
- `Scope`
- `Pass Criteria`
- `Files`
- `Maintenance Rules`

### `baseline.json`

Purpose:

- define shared evaluation defaults for the skill

Recommended contents:

- `skill_name`
- `version`
- `default_language`
- `output_contract`
- `global_expectations`
- `forbidden_behaviors`
- `scoring`

Recommended example:

```json
{
  "skill_name": "test-case-generator",
  "version": 1,
  "default_language": "zh-CN",
  "output_contract": {
    "primary_artifact": "xmind",
    "return_absolute_path_first": true,
    "require_real_xmind_file": true
  },
  "global_expectations": [
    "keep full in-scope coverage instead of outputting only P0 cases",
    "mark P0 only when justified",
    "state no P0 explicitly when none qualifies",
    "separate confirmed information from assumptions when assumptions are used",
    "label output as draft when critical source material is missing or conflicting"
  ],
  "forbidden_behaviors": [
    "returning only prose when a real xmind deliverable is required",
    "treating P0 as a coverage filter",
    "silently inventing critical workflow semantics",
    "using markdown bullet prefixes in xmind group or case titles"
  ],
  "scoring": {
    "mode": "rule-based",
    "pass_threshold": 1.0
  }
}
```

### `cases/*.json`

Purpose:

- define one independent evaluation case per file

Recommended minimal schema:

```json
{
  "id": "case_001",
  "title": "Web login with MFA and lockout",
  "type": "core",
  "tags": ["web", "auth", "mfa", "lockout", "p0"],
  "prompt": "请基于以下 Web 登录需求设计测试用例，并默认输出真实 .xmind 文件。需求：...",
  "inputs": {
    "files": []
  },
  "expect": {
    "must": [
      "generate a real .xmind file",
      "return the absolute path first",
      "cover login success flow",
      "cover MFA flow",
      "cover account lockout behavior",
      "cover boundary and negative scenarios"
    ],
    "should": [
      "identify at least one justified P0 scenario"
    ],
    "must_not": [
      "output only P0 cases",
      "omit lockout-with-correct-password behavior"
    ]
  },
  "notes": "Core regression case for auth flow."
}
```

Recommended semantics:

- `id`: stable unique identifier
- `title`: human-readable title
- `type`: case class such as `core`, `trigger`, `negative`, `draft`, or `regression`
- `tags`: filter and grouping metadata
- `prompt`: eval prompt or user request
- `inputs.files`: supporting file list when needed
- `expect.must`: hard requirements
- `expect.should`: soft expectations
- `expect.must_not`: forbidden outcomes
- `notes`: optional maintenance note

## Naming Rules

Support two naming styles:

- `case_001.json`
- `route_should_trigger_001.json`

Recommended usage:

- use `case_001.json` for general functional evals
- use `route_should_trigger_001.json` or `route_should_not_trigger_001.json` for trigger-routing evals

Do not mix multiple intents into one case file merely to reduce file count.

## Migration Rules

Migrate existing skill-local eval files into the new repository-level structure.

For the current skill:

```text
skills/test-case-generator/evals/evals.json
```

target:

```text
eval/skills/test-case-generator/
  README.md
  baseline.json
  cases/
    case_001.json
    case_002.json
    case_003.json
```

Migration steps:

1. Extract shared expectations from the old monolithic file into `baseline.json`.
2. Convert each eval entry into one file under `cases/`.
3. Move old `files` arrays into `inputs.files`.
4. Split old `expected_output` strings into `expect.must`, `expect.should`, and `expect.must_not`.
5. Add an eval-pack `README.md` describing purpose, scope, and pass criteria.
6. Delete the old `skills/<skill-name>/evals/evals.json` after the new structure is complete.

## First Skill Rollout

Use `test-case-generator` as the first migration target.

Initial target cases:

- `case_001.json`: Web login with MFA and lockout
- `case_002.json`: App cart with inventory and offline retry
- `case_003.json`: Order API idempotency with draft behavior

This provides:

- one core auth/workflow case
- one app/offline consistency case
- one sparse-material draft case

These three cases are enough to validate the first version of the structure without over-designing the system.

## Non-Goals

This design does not define:

- a global eval runner
- a repository-wide eval registry
- a scoring engine beyond simple rule-based expectations
- cross-skill orchestration rules

Those can be designed later if the repository grows beyond the current scale.

## Recommended Next Step

After this spec is approved, create an implementation plan to:

1. add the new `eval/skills/test-case-generator/` structure
2. migrate the current `evals.json` contents into `README.md`, `baseline.json`, and `cases/*.json`
3. remove the legacy `skills/test-case-generator/evals/evals.json`
4. verify the migrated pack is complete and readable
