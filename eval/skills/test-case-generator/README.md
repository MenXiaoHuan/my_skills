# Eval Pack: test-case-generator

## Purpose

Evaluate whether `test-case-generator` produces structured, implementation-aware test design outputs from requirement or technical materials, with correct prioritization, assumptions handling, and real `.xmind` deliverables when required.

## Scope

This eval pack covers:
- trigger fit
- coverage completeness
- P0 labeling quality
- assumptions and draft behavior
- output contract compliance
- XMind deliverable expectations

This eval pack does not cover:
- implementation correctness of product code
- UI rendering quality of the generated XMind viewer
- external system availability

## Pass Criteria

A case passes only when:
- the skill is correctly triggered
- the response follows the expected output contract
- required scope is covered
- forbidden behavior is not present
- draft or assumptions behavior is correct when applicable

## Files

- `baseline.json`: shared evaluation defaults for this skill
- `cases/`: independent eval cases

## Maintenance Rules

- keep one intent per case
- prefer small, composable cases over mega-cases
- add a new case when a bug, regression, or prompt failure is discovered
- update `baseline.json` only for truly shared rules
