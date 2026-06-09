# TTMS Module: Catalog Analytics

Use this file only when the change touches catalog-level aggregation, grouped rollups, drill-down from catalog summaries, or exports that should mirror the current aggregated scope.

## Use This Module For

- catalog-entity analysis where the primary object is a catalog bucket, grouped segment, or rolled-up entity set rather than a single merchandise item
- aggregation semantics such as totals, grouped rows, summary metrics, and entity counts that depend on a defined catalog grain
- grouping, hierarchy, or dimension changes that alter how catalog entities are bucketed and compared
- consistency between top-level catalog summaries, drill-down views, and exported outputs derived from the same aggregate definition
- reasoning about partial data, late-arriving data, and freshness when the user is reading rolled-up catalog results instead of raw item rows

## Business Semantics

### Core Workflow
- open a catalog analysis view that starts from aggregated catalog entities rather than item-by-item inspection
- choose filters, grouping dimensions, hierarchy levels, or other dimension selections that define the current rollup grain
- inspect summary cards, charts, grouped tables, or entity counts that represent that exact aggregate scope
- drill down from one aggregate bucket into a narrower slice while preserving the parent filters, dimension definitions, and catalog membership logic
- export the current aggregate view or drilled subset with the same entity grain and grouping semantics shown on screen

### Important Branches
- top-level catalog rollup vs drill-down into one grouped slice or one hierarchy branch
- one dimension definition or hierarchy level vs another dimensioning of the same catalog entities
- aggregate metric view vs constituent entity list or narrower grouped breakdown
- complete catalog aggregation vs partial, delayed, or still-refreshing aggregate data

### Status and Visibility Rules
- filters, grouping selections, hierarchy choices, and catalog-grain definitions must propagate consistently to all catalog totals, charts, tables, and drill-down targets
- drill-down should inherit the parent aggregate scope and entity-membership rule rather than resetting to an unrelated default grouping
- when regrouping changes the dimension context, every dependent summary should recompute from the same catalog universe instead of mixing old and new buckets
- freshness and partial-data messaging should clarify whether the aggregate result is complete enough for decision-making or export, especially when some catalog entities have not fully arrived

## Testing Prompts

Prioritize:
- catalog-level aggregation and rollup correctness at the intended catalog entity grain
- grouping, hierarchy, and dimension-switch behavior
- consistency between aggregate summaries, grouped rows, entity counts, and drill-down targets
- export correctness for the current aggregate scope and dimension definition
- freshness and partial-data behavior for rolled-up catalog results

High-risk failure patterns:
- totals, grouped rows, entity counts, and drill-down results are calculated from different catalog universes or different entity grains
- regrouping changes the bucket definition in one component but leaves another component on the prior dimension context
- export output flattens or re-buckets data differently from the on-screen aggregate view, so the same catalog slice cannot be reconciled

Typical P0 candidates:
- catalog totals, grouped results, or entity counts become materially wrong at the analysis layer
- users cannot trust catalog drill-down or exported aggregates because the dimension definition changes between surfaces

## Source Links

- `Catalog Analytics`: `https://bytedance.larkoffice.com/wiki/BwruwhM4Yif2W1kaYTEcHaREn6f`

## Notes For Agent Usage

- Prefer explicit requirement and technical docs first.
- Use this file only to fill TTMS-specific semantic gaps.
- Read this module as catalog-entity aggregation semantics, not as a generic report page description.
- Focus on catalog grain, bucket definition, and cross-surface dimension consistency before discussing generic charts or exports.
- If this file materially shaped the answer, mention it explicitly.
