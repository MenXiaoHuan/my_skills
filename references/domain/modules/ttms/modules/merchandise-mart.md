# TTMS Module: Merchandise Mart

Use this file only when the change touches merchandise-level insight browsing, merchandise collection selection, merchandise detail inspection, or exports derived from the currently chosen merchandise set.

## Use This Module For

- merchandise and assortment browsing where the primary question is "which items are in the current merchandise pool" rather than "how did a campaign perform"
- consistency between merchandise collection surfaces such as list, card, and item detail
- filter, sort, and segmentation behavior that determines which merchandise items enter, leave, or stay visible in the current merchandise set
- validating that item-level exports mirror the same merchandise pool, visible attributes, and selection context shown on screen
- checking empty, partial-data, and stale-data behavior for merchandise browsing and selection surfaces

## Business Semantics

### Core Workflow
- open a merchandise pool or assortment browsing surface such as a list, grid, or similar collection view
- apply filters, sorting, segmentation, or attribute constraints to define which merchandise items are currently in scope
- inspect a single item for deeper attributes or performance signals without losing the collection context it came from
- move between collection browsing and merchandise detail while preserving the same merchandise membership logic and ordering expectations
- export the current merchandise set or selected item details for downstream selection, review, or operational follow-up

### Important Branches
- merchandise pool overview vs single-item detail inspection
- manually narrowed merchandise set vs default or broader merchandise pool
- on-screen visible merchandise attributes vs exported merchandise columns or records
- browsing many candidate items vs validating one specific item while keeping its place in the surrounding assortment

### Status and Visibility Rules
- active filters, sorting, and segmentation should define a stable merchandise pool across list, card, and detail surfaces
- opening an item detail should retain the current merchandise membership context instead of jumping to an unrelated default item or a different assortment
- visibility badges, counts, or item-level status hints should explain why an item is present, absent, or not exportable under the current selection logic
- empty-state and partial-data messaging should distinguish between "no items match this scope" and "item data is incomplete or still loading"

## Testing Prompts

Prioritize:
- merchandise pool formation and refinement behavior
- consistency between list or card views and single-item detail
- filter, sort, and segmentation effects on item membership, order, and visible attributes
- export correctness for the currently selected merchandise set and selected item details
- empty, partial-data, stale-data, and visibility-state messaging for merchandise browsing

High-risk failure patterns:
- an item detail page is reachable even though that item is no longer part of the currently filtered merchandise pool
- list counts, card counts, and exported rows are derived from different merchandise membership rules
- sorting or filtering changes the visible collection, but the exported file or next-item navigation still uses the old merchandise set

Typical P0 candidates:
- users cannot reliably inspect or hand off the intended merchandise pool end to end
- exported merchandise output includes the wrong items or omits the items that the current assortment review depended on

## Source Links

- `Merchandise Mart`: `https://bytedance.sg.larkoffice.com/docx/Rr4AdFQN9o6rKxxj9JSlLCSrg5f`

## Notes For Agent Usage

- Prefer explicit requirement and technical docs first.
- Use this file only to fill TTMS-specific semantic gaps.
- Read this module as merchandise-pool and item-selection semantics, not as a generic reporting template.
- Favor questions about item membership, collection continuity, and item-detail handoff over generic chart/table wording.
- If this file materially shaped the answer, mention it explicitly.
