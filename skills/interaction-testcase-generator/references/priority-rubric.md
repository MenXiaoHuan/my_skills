# Priority Rubric

Read this file when the main difficulty is deciding whether a case should be marked `P0`, `P1`, `P2`, or `P3`.

Use this rubric to improve consistency. Treat it as a decision aid, not a substitute for reading the source requirements.

## Core Definitions

- `P0`: Release blocker or critical correctness failure on a core workflow
- `P1`: High-risk or high-value behavior with strong business, operational, or downstream impact
- `P2`: Important but recoverable issue with bounded scope or a practical workaround
- `P3`: Low-risk, low-frequency, cosmetic, or optional coverage

## Decision Order

1. Ask whether the release should stop if this case fails.
2. Ask whether the failure breaks a core user journey, core operator workflow, core metric, or externally visible truth.
3. Ask whether the failure leaks permissions, corrupts data, misroutes workflow state, or spreads to downstream systems.
4. Ask whether the issue is recoverable, scoped, and supported by a clear workaround.
5. Pick the highest justified priority, then downgrade only when the blast radius is clearly limited.

## Fast Heuristics

Use `P0` when the failure:
- blocks launch or forces rollback
- breaks payment, order creation, login, publishing, approval, or another primary workflow
- creates severe permission leakage or data loss
- causes critical report or export results to become materially wrong
- makes a cross-system workflow land in the wrong state without a safe recovery path

Use `P1` when the failure:
- does not block launch, but materially harms a high-value workflow
- breaks a major operator path, operational efficiency, or important downstream correctness
- causes incorrect notifications, exports, or synchronization with meaningful business impact
- affects a core module but still has containment or partial fallback

Use `P2` when the failure:
- is important but recoverable
- is limited to specific roles, data ranges, or edge states
- has a reasonable workaround
- affects secondary correctness, partial fallback behavior, or non-default workflow branches

Use `P3` when the failure:
- is cosmetic, low-frequency, or optional
- affects convenience behavior rather than critical execution
- has little business or operational impact

## Cross-Checks

Before finalizing a priority, check these dimensions:

- workflow criticality: core path or secondary path
- role criticality: core role or secondary role
- blast radius: single view, single role, or multiple systems
- recoverability: no recovery, partial recovery, or easy workaround
- correctness impact: cosmetic, local correctness, or external/business truth

## Typical Examples

### P0 Examples

- `[P0] Authentication - Locked account still blocks login during the lock window`
- `[P0] Order API - Same idempotency key with different payload returns conflict instead of creating a second order`
- `[P0] Permissioned Report - Export timeout still creates the correct download-center task for the current filtered scope`

### P1 Examples

- `[P1] Permissioned Report - Operator cannot enter the full report page`
- `[P1] Trend Analysis - Switching driverTag updates the chart to the correct scoped data`
- `[P1] Notification Workflow - Approval success sends the correct message to downstream stakeholders`

### P2 Examples

- `[P2] Trend Analysis - Fun Facts cards remain consistent with the selected filter scope`
- `[P2] Export Center - Retry after a transient failure preserves the user's current filter context`
- `[P2] Login - Expired MFA code shows a clear retry path`

### P3 Examples

- `[P3] Report Page - Empty-state illustration style is consistent with design guidance`
- `[P3] Search Filter - Optional tooltip text is shown with the expected wording`

## Guardrails

- Do not mark too many cases as `P0`; `P0` is a highlight, not the default.
- Do not downgrade a case only because a workaround exists if the failure still breaks a core business truth or release-critical path.
- Do not upgrade a case only because it is visible; visibility without strong impact is not enough.
- If no case truly qualifies, explicitly state `本次范围未识别出 P0 场景`.
