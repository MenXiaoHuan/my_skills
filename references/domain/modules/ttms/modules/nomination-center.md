# TTMS Module: Nomination Center

Use this file only when the feature involves nomination onboarding, qualification gating, invite activation, or related status-driven actions.

## Use This Module For

- nomination creation and submission flows
- qualification upload and validation
- trademark owner vs authorized representative branches
- invite-link visibility and activation constraints
- internal vs external visibility differences

## Business Semantics

### Core Workflow
- nomination creation
- qualification submission
- processing and review progression
- invite availability and activation

### Important Branches
- trademark owner vs authorized representative
- brand-exclusive vs brand-mixed

### Status and Visibility Rules
- processing status transitions gate downstream actions
- qualification review status gates invite-link visibility
- account ID rules may affect onboarding completion

## Testing Prompts

Prioritize:
- nomination creation and submission flows
- qualification branch validation
- invite activation constraints
- status-driven action visibility
- account ID field rules

High-risk failure patterns:
- invite link shown before upstream statuses are ready
- qualification branch logic diverges by owner type
- status-driven actions appear for the wrong role
- onboarding blockers caused by hidden validation rules

Typical P0 candidates:
- merchant cannot complete onboarding due to broken nomination or invite gating
- critical action becomes invisible to the right user at the right status

## Source Links

- `Nomination Center`: `https://bytedance.larkoffice.com/wiki/HAe9wqk5hiCLPJkp8GvcgpL9nw4`
- `Trademark Standard Format`: `https://bytedance.sg.larkoffice.com/docx/OFlidUACLoWKntxlXmJcFYLGn7f`
- `Brand Qualification Guidance`: `https://bytedance.sg.larkoffice.com/docx/IK52dqVU8oaCQGxOz04lrLCNgzd`

## Notes For Agent Usage

- Prefer explicit requirement and technical docs first.
- Use this file only to fill TTMS-specific semantic gaps.
- If this file materially shaped the answer, mention it explicitly.
