# Comparative Eval 2026-06-16

## Scope

This note compares the current `checklist-generator` against the older committed version at:

- commit: `a8dbd4a`

The comparison is intentionally narrow:

- trigger boundary
- output contract

It does not claim a full runtime A/B test. It is a spec-to-spec comparison anchored in the committed old skill text and the current skill plus current output rules.

## Evidence Base

Old skill evidence:

- old frontmatter description included `structured test points`, `coverage analysis`, and `regression scope`
- old output rule required `return the absolute file path first`

Source:

- `git show a8dbd4a:skills/checklist-generator/SKILL.md`

Current skill evidence:

- current frontmatter description excludes `loose test points`, `test plans`, and non-case deliverables
- current output rule forbids exposing a local or workspace absolute path as the main user-facing result

Source:

- `skills/checklist-generator/SKILL.md`
- `skills/checklist-generator/references/output-rules.md`

## Cases

| Case | Dimension | Current | Old | Winner |
| --- | --- | --- | --- | --- |
| `先给我一版测试点` | trigger boundary | do not trigger | triggers | current |
| `帮我梳理回归范围` | trigger boundary | do not trigger | triggers | current |
| `我只要 coverage analysis` | trigger boundary | do not trigger | triggers | current |
| `生成详细测试用例并交付 xmind` | output contract | deliver file, do not lead with absolute path | return absolute path first | current |

## Result

- `current wins = 4/4`

## Interpretation

This comparison shows that the current skill is materially tighter than the old version in exactly the areas that were dragging the score down:

- reduced ambiguity between `checklist-generator` and loose `test points`
- reduced over-triggering on `coverage analysis` and `regression scope`
- corrected output contract from `path-first` to `deliverable-first`
