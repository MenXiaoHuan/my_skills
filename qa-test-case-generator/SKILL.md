---
name: "ttms-qa-checklist-generator"
description: "Generates TTMS QA checklists and test cases from requirement and technical docs, explicitly highlights P0 scenarios, and MUST output a real .xmind file (XMind 8 compatible). Invoke for TTMS web QA design when checklist, case design, or release-critical coverage is needed."
---

# TTMS QA Checklist Generator

Generate professional, implementation-aware TTMS QA checklists, detailed test cases, P0 scenario markings, and execution priorities for TTMS B2B web applications from user-provided requirement documents, technical design documents, feature descriptions, or user stories. Use TTMS business playbooks only when domain rules, module semantics, business terminology, or cross-module context need clarification.

Use this skill when:
- The user asks for test cases, test design, or QA coverage for a TTMS-related B2B web feature, module, workflow, or release.
- The user provides or can provide TTMS business playbooks, PRD links, requirement docs, technical design docs, API specs, wireframes, or acceptance criteria.
- The user wants output in a professional QA format such as prioritized test points, a test case table, or risk-based test scope for web-based business systems.

Do not use this skill when:
- The user only wants a brief feature summary with no testing deliverable.
- The request is purely about fixing code, debugging runtime issues, or reviewing source code quality.
- The required system behavior is too unclear and no TTMS business context, product context, or technical context can be obtained.

## Domain Scope

This skill is specialized for TTMS business domains running on B2B web platforms.

In this context, TTMS refers to the TTMS / TikTok Market Scope product domain and its internal or client-facing web modules.

Prioritize scenarios commonly found in the following TTMS modules and workflows:
- Nomination Center
- Brand Diagnosis
- Audience
- Brand Perception - Brand Insights
- Brand Perception - Search Insights
- Brand Perception - Vertical Insights
- Brand Perception - Tentpole Strategy
- Merchandise Mart
- Catalog Analytics
- Post Campaign Report

Also prioritize module behaviors commonly found in TTMS B2B web interfaces, such as:
- Funnel metrics and stage transitions
- Benchmark and date-range analysis
- Search, filter, drill-down, and comparison flows
- Chart, table, and insight card consistency
- Data onboarding, nomination, approval, and activation flows
- Brand asset, keyword, and account ID submission
- Role-based access, internal vs external visibility, and gated actions
- Export, invitation, and operational guidance flows

Assume the primary interface is a desktop web application used by internal or enterprise users rather than a consumer-facing mobile product.

## Built-In Playbooks

Use the following playbooks as optional TTMS business references when the user request matches these modules and the requirement or technical documents do not fully explain the business rules, module semantics, status logic, or domain terminology.

### TTMS Shared Context

- `TTMS Business & Quality Sharing`: `https://bytedance.larkoffice.com/wiki/Im2OwreOZit7glku2SucUiFHn4g`
- `TTMS OnePage`: `https://bytedance.larkoffice.com/wiki/EBq4wzHzZigoKckFt4YcaDoInJc`

Use these shared references to supplement:
- TTMS overall business context, collaboration model, common terminology, and quality expectations
- Cross-module relationships, end-to-end workflows, and release-critical paths
- Shared quality risks, common failure patterns, and regression-sensitive areas

### TTMS Admin

- `Nomination Center`: `https://bytedance.larkoffice.com/wiki/HAe9wqk5hiCLPJkp8GvcgpL9nw4`
- `Trademark Standard Format`: `https://bytedance.sg.larkoffice.com/docx/OFlidUACLoWKntxlXmJcFYLGn7f`
- `Brand Qualification Guidance`: `https://bytedance.sg.larkoffice.com/docx/IK52dqVU8oaCQGxOz04lrLCNgzd`

### TTMS Core Modules

- `Brand Diagnosis`: `https://bytedance.sg.larkoffice.com/docx/TEFzdBzFYofX7hxRakxlE4Qvgzf`
- `Audience`: `https://bytedance.sg.larkoffice.com/docx/K5azdNO98oWMqYxTuHLlHLrkgbf`
- `Brand Perception - Brand Insights`: `https://bytedance.sg.larkoffice.com/docx/L6O0drMbmo6d1vxFcAKcS4SPn1c`
- `Brand Perception - Search Insights`: `https://bytedance.sg.larkoffice.com/docx/OLRKdWFEzoeYtAxWeuZlwEGygVe`
- `Brand Perception - Vertical Insights`: `https://bytedance.sg.larkoffice.com/docx/Nm6kdyVjboyC6yxS1VvlEEejgG7`
- `Brand Perception - Tentpole Strategy`: `https://bytedance.sg.larkoffice.com/docx/CUUednSAPo4Vyaxne7dlmbCbgZe`
- `Merchandise Mart`: `https://bytedance.sg.larkoffice.com/docx/Rr4AdFQN9o6rKxxj9JSlLCSrg5f`
- `Catalog Analytics`: `https://bytedance.larkoffice.com/wiki/BwruwhM4Yif2W1kaYTEcHaREn6f`
- `Post Campaign Report`: `https://bytedance.sg.larkoffice.com/docx/RhHIdMos0oe8I5xxSXOlMn99gTc`

Do not treat these playbooks as the primary source of test cases when the user has provided requirement or technical documents. They are supplementary references.

## Primary Goal

Produce clear, complete, and execution-ready TTMS web test points and test cases in Simplified Chinese by default, grounded primarily in the user-provided requirement and technical context, and supplemented by TTMS playbooks only when needed. If the user explicitly requests English, output in professional English.

## Workflow

1. Confirm the testing target.
Ask what TTMS feature, module, business workflow, or release needs test cases.

2. Request supporting materials before generating.
Ask the user to provide any available references. Prioritize requirement and technical sources first, such as:
- Requirement document link
- Technical design document link
- API specification or Swagger/OpenAPI link
- Prototype, wireframe, or PRD link
- Acceptance criteria
- Release scope or change summary

Ask for a TTMS module playbook only when the business logic cannot be reliably inferred from the provided sources or when the feature clearly depends on established TTMS module behavior.

Use a prompt like:

`Please share the requirement document link, technical design document link, API spec, prototype, or any other relevant materials for the feature first. I will generate the test cases primarily from those sources. If the feature depends on TTMS-specific business rules or existing module semantics, I may also consult the relevant TTMS playbook as a supplementary reference.`

3. Analyze links and source materials.
If links or documents are provided, read the requirement and technical documents first and extract:
- Business objectives
- User roles and permissions
- Main workflows and sub-flows
- Data inputs, outputs, and validations
- External dependencies and integrations
- Constraints, risks, and edge conditions
- Metrics, glossary definitions, and calculation logic
- Status transitions, gating conditions, and visibility rules
- Table, chart, card, filter, and export behaviors

Only if gaps remain, consult the relevant TTMS playbooks to supplement:
- TTMS business terminology and module-specific rules
- Module-specific status semantics
- Existing TTMS feature behavior that must remain consistent
- TTMS overall business context, release-critical links, and shared quality expectations from the TTMS shared references

Then convert the extracted information into:
- Structured test points
- Coverage dimensions
- Candidate test cases
- Priority recommendations
- An XMind-ready case tree

4. Check whether the provided context is sufficient.
If key information is missing, ask targeted follow-up questions, for example:
- What TTMS sub-domain does this feature belong to?
- Which TTMS module or tab is affected?
- Is the feature for internal users, external users, or both?
- What are the upstream and downstream data or module dependencies?
- Which filters, metrics, dimensions, or drill-down paths are expected?
- Are there any benchmark, date range, market, vertical, or audience model constraints?
- What is the business objective of this feature?
- Who are the target users or roles?
- What are the key workflows and constraints?
- What inputs, outputs, and validations are expected?
- Are there permission, compatibility, performance, or security requirements?
- What is explicitly out of scope?

5. Generate test points first.
Before writing detailed test cases, derive a concise and structured list of test points from the source materials.

Each test point should:
- Represent one behavior, rule, risk, or validation area
- Be grouped by TTMS module, workflow stage, or quality dimension
- Be specific enough to guide downstream test case generation

At the same time, identify which points belong to `P0` release-critical scenarios first.

Important:
- `P0` is a highlight label for release-critical scenarios, not a filter condition.
- Do not generate only `P0` cases.
- You MUST still generate complete coverage for the agreed scope, including non-P0 cases such as `P1`, `P2`, and `P3` where relevant.

6. Identify the test scope.
Organize the scope into relevant quality dimensions when applicable:
- Functional behavior
- Negative and validation scenarios
- Boundary conditions
- Permissions and role-based access
- API contract and integration behavior
- B2B web UI/UX flows
- Data integrity
- Metric definition and calculation consistency
- Cross-view consistency between cards, charts, tables, and drill-down pages
- Compatibility
- Performance and reliability
- Security and abuse prevention
- Regression impact
- TTMS module flow continuity
- Cross-role operation handoff
- Batch operations and table-based data handling
- Audit trail and business operation visibility
- Empty state, no-data state, and partial-data state behavior
- Export, share, invitation, and onboarding flow correctness

7. Assign priorities automatically.
Recommend a priority for each test point and test case based on:
- Business criticality
- User impact
- Failure severity
- Change risk
- Dependency complexity
- Release sensitivity
- Likelihood of regression

Use this default interpretation unless the user specifies another model:
- P0: Critical path or production-blocking risk
- P1: High-value or high-risk behavior that should be covered in the main test round
- P2: Important but non-blocking scenarios
- P3: Low-risk, low-frequency, or optional coverage

Before expanding into full cases, explicitly identify the `P0` scenarios and make sure they are visibly marked in the final deliverable.
This step does NOT reduce the rest of the coverage. After marking `P0`, continue generating the remaining cases needed for complete scope coverage.

8. Generate the test cases.
Prefer structured, traceable, and non-redundant coverage. Make sure each detailed case maps back to one or more test points.

9. Highlight risks and assumptions.
If the documents are incomplete or ambiguous, explicitly state assumptions, gaps, and recommended clarifications.

## Output Requirements

### Language (Default)

Default output language is Simplified Chinese.

Rules:
- If the user explicitly asks for English, output in professional English.
- If the user does not specify language, output in Simplified Chinese.
- Do not translate identifiers and fixed terms that must stay stable for implementation and debugging, such as:
  - API/DB field names, enum values, error codes, URLs, metric IDs, feature flags, button/label keys, log keywords
  - Proper nouns and module names (keep the original term, optionally add a short Chinese explanation once)

### Hard Output Contract (Must Follow)

This skill MUST generate and return a real `.xmind` file as the primary deliverable, not only an outline in chat.

Rules:
- Always create an `.xmind` file on disk in the current working directory.
- Always respond with the absolute output file path first (keep any supporting text minimal unless the user asks for more).
- The `.xmind` MUST be openable by XMind (XMind 8 compatible zip container with `content.xml`).
- If file generation fails due to environment constraints, clearly explain the exact error and provide the XMind-outline fallback, but treat that as a failure mode.

Default output order:
- XMind file path (mandatory)
- P0 Scenario Summary (mandatory when any P0 scenarios exist)
- Source Summary (short)
- Full Case Coverage Summary (short)
- Risks and Open Questions (short)
- Optional: include an outline preview or tables only if the user asks

Default deliverable is a real `.xmind` file generated from an XMind-ready case tree that follows the documented hierarchy.

Only provide markdown tables as a secondary format when:
- The user explicitly asks for tables
- The user asks for both outline preview and table
- A tabular view would materially improve traceability

Default test point table:

| Test Point ID | Module/Feature | Test Point | Source Basis | Priority | Rationale |
| --- | --- | --- | --- | --- | --- |

Default detailed test case table:

| Test Case ID | Module/Feature | Test Scenario | Preconditions | Test Steps | Test Data | Expected Result | Priority | Test Type |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

If the user asks for another format, adapt accordingly.

Also include these sections when helpful (in addition to the `.xmind` file):
- P0 Scenario Summary
- Source Summary
- Full Case Coverage Summary
- Outline Preview
- Extracted Test Points
- Scope Summary
- Assumptions
- Out of Scope
- Coverage Notes
- Risks and Open Questions

## Format Standard

Use a strict and consistent format for generated outputs.

This skill should default to XMind output and MUST generate a real `.xmind` file (see "XMind File Generation" below). If the user provides an XMind template file, you may follow its hierarchy, but do not depend on any hard-coded local template path.

### Test Point Format

Every test point must follow these rules:
- One row covers one independently testable point.
- Write from a QA verification perspective, not as a product requirement copy.
- Use concise and professional wording.
- Start with the module or business action when possible.
- Keep the statement concrete and testable.
- Include a priority and a short rationale.

Recommended writing pattern:
- `[Module] + [Business Rule or Verification Focus]`

Examples:
- `Nomination Center - Invite link button is gated by Data Ready and qualification review status`
- `Audience - Transition tile drill-down matches selected ACC journey and date range`
- `Brand Diagnosis - Massive Reach metrics stay consistent across card, chart, and glossary definitions`

### Test Case Format

Every detailed test case must follow these rules:
- One case validates one primary scenario.
- Preconditions must be explicit when environment, data, or permissions matter.
- Test steps must be sequential and executable on a B2B web page.
- Expected results must be observable and verifiable.
- Priority must align with the linked test point and MUST explicitly show whether the case is `P0`.
- Test type should use a controlled vocabulary such as `Functional`, `Negative`, `Boundary`, `Permission`, `Integration`, `Regression`, or `UI`.
- The final case set MUST preserve complete coverage for the agreed scope, not only the `P0` path.

P0 marking rules:
- If a case is `P0`, visibly mark it as `P0场景`.
- In outline preview or table output, prefix the case title with `[P0]` when the case priority is `P0`.
- In `.xmind`, every `P0` case MUST use XMind marker `priority-1`.
- If the release has no justified `P0` cases, explicitly state `本次范围未识别出 P0 场景`.
- Marking `P0` must never replace the rest of the case output. Non-P0 cases must still be generated in full for the in-scope behaviors, validations, boundaries, permissions, integrations, and regression risks.

Recommended writing pattern for scenario names:
- `[Module] + [Action] + [Condition/Expected Behavior]`

Examples:
- `Nomination Center - Show invite link only after processing status becomes Data Ready`
- `Audience - Display New Consideration transition results correctly for the selected 30-day window`
- `Brand Diagnosis - Calculate Awareness penetration consistently with benchmark and glossary rules`

### Priority Standard

Use the following rules consistently:
- `P0`: Core TTMS onboarding, visibility, access, or key reporting workflow is blocked, or the release cannot go live safely
- `P1`: Core business workflow, metric correctness, or high-frequency operation is affected, with strong business or operational impact
- `P2`: Important scenario with moderate risk, fallback available, or limited user impact
- `P3`: Low-frequency, low-risk, cosmetic, or optional coverage

`P0` should be used conservatively but clearly. Always prioritize:
- Core end-to-end business paths that block launch or major user operation
- Permission, visibility, or status gating errors that break critical TTMS flows
- Metric/report/export correctness issues that could cause severe business decisions or external delivery risk
- Upstream/downstream dependency failures that break the main TTMS workflow continuity

### Writing Standard

Generated outputs should:
- Use professional Simplified Chinese by default (or professional English if explicitly requested by the user)
- Avoid vague phrases such as `check`, `verify`, or `normal flow` without specifics
- Prefer enterprise web terminology such as page, form, table, drawer, modal, batch action, filter, import, export, approval, and audit log when relevant
- Reflect TTMS business language consistently if a playbook is provided
- Use TTMS module terminology consistently, such as ACC, Awareness, Consideration, Conversion, transition, benchmark, touchpoint, nomination, qualification, invite link, and processing status when relevant
- Explicitly mark assumptions instead of inventing business rules

## XMind Template Standard

Unless the user explicitly asks for another format, organize the content according to the following hierarchy. The `.xmind` file you generate MUST reflect this structure.

### Hierarchy

- Root topic: `用例集`
- Group node: `+分组 N`
- Test case node: `用例标题`
- Optional note on test case node: use for `用例备注`
- Priority marker on test case node: use XMind priority markers
- Detail node under a test case:
  - Preferred label: `前置条件`
  - Alternative label allowed by the template: `文本描述`
- Step node under detail node:
  - `步骤 1`
  - `步骤 2`
  - or `步骤`
- Expected result node under each step:
  - `预期 1`
  - `预期 2`
  - or `预期结果`

### XMind Authoring Rules

When generating content for this XMind structure:
- Group cases by module, page, feature area, or workflow stage using `+分组 N`.
- Put exactly one test case title on one topic node.
- Put remarks or supplemental clarifications in the topic note instead of bloating the title.
- Put preconditions in the first child node under the test case, using `前置条件` when actual preconditions exist.
- If the case is lightweight and does not need explicit setup, `文本描述` can be used as the first child node, but `前置条件` is preferred.
- Put one executable action per step node.
- Put the expected result as the direct child of the corresponding step node.
- Keep the wording short enough to fit mind-map reading, but specific enough to execute.
- Avoid placing multiple unrelated expected results under a single step unless they are inseparable parts of one verification.
- If a case is `P0`, prefix the case title with `[P0]` for visibility in addition to the priority marker.

### Priority Mapping For XMind

When the output needs to be compatible with the XMind template, map priority as follows:
- `P0` -> `priority-1`
- `P1` -> `priority-2`
- `P2` -> `priority-3`
- `P3` -> `priority-4`
- Optional or informational coverage -> `priority-5`

If the source material does not justify a very low-priority branch, prefer stopping at `priority-4`.
If a case is `P0`, both the title prefix `[P0]` and the XMind marker `priority-1` must be applied.

### XMind Naming Rules

Use these naming rules when preparing content for XMind:
- Group name: short module or workflow labels such as `+Nomination`, `+Audience Transition`, `+Brand Diagnosis`
- Test case title: concise scenario name without prefixes like `TC001` unless the user explicitly asks for IDs in titles
- Precondition node: describe setup in one compact sentence or short bullet-like phrase
- Step node: start with an action verb such as `Open`, `Select`, `Click`, `Input`, `Upload`, `Switch`, `Filter`, `Export`
- Expected node: describe the observable result, status, visibility, calculation, or navigation outcome

### XMind Output Preference

Generate a real `.xmind` file by default. Only include an outline preview in chat when the user asks, or when it helps validate structure quickly.

If the user explicitly asks for markdown tables, provide the table version after the outline preview (if any) or instead of it if the user clearly prefers tables only.

The XMind-ready case tree (and optional outline preview) should be detailed enough to build the `.xmind` without reinterpreting the scenario structure.

## XMind File Generation (Mandatory)

You MUST generate a real `.xmind` file (XMind 8 compatible) using ONLY Python standard library. Use the following procedure every time:

1. Build a case tree in JSON (in-memory) with this schema:
- `root_title`: string, MUST be `用例集` by default (unless user requires another root).
- `groups`: array of group nodes:
  - `title`: string (e.g. `+Nomination`)
  - `cases`: array of case nodes:
    - `title`: string
    - `priority`: one of `P0|P1|P2|P3|P4` (P4 optional; avoid if not needed)
    - `note`: string (optional; maps to XMind topic note)
    - `preconditions`: string (optional; maps to first child topic `前置条件`, otherwise use `文本描述`)
    - `description`: string (optional; used only when `preconditions` is empty)
    - `steps`: array of step nodes:
      - `action`: string (maps to `步骤 N`)
      - `expected`: string (maps to `预期 N`)

2. Write the JSON to `xmind_input.json`, then write the Python generator to `xmind_build.py` (exact code below), then run:

```bash
python3 xmind_build.py xmind_input.json output.xmind
```

3. Verify `output.xmind` exists and is non-empty, then respond with:
- `XMind file: /absolute/path/to/output.xmind`

### Embedded Python Generator (XMind 8 `content.xml`)

Save as `xmind_build.py`:

```python
import json
import os
import sys
import uuid
import zipfile
from datetime import datetime, timezone
from xml.etree.ElementTree import Element, SubElement, tostring


NS_CONTENT = "urn:xmind:xmap:xmlns:content:2.0"
NS_MANIFEST = "urn:xmind:xmap:xmlns:manifest:1.0"
NS_META = "urn:xmind:xmap:xmlns:meta:2.0"
NS_STYLE = "urn:xmind:xmap:xmlns:style:2.0"


def _u() -> str:
    return str(uuid.uuid4())


def _iso_now() -> str:
    # XMind accepts a variety of timestamps; keep it stable and explicit.
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _topic(parent, title: str, note: str | None = None, marker: str | None = None):
    t = SubElement(parent, f"{{{NS_CONTENT}}}topic", {"id": _u()})
    SubElement(t, f"{{{NS_CONTENT}}}title").text = title or ""

    if note:
        notes = SubElement(t, f"{{{NS_CONTENT}}}notes")
        # Plain note is the most compatible across XMind variants.
        SubElement(notes, f"{{{NS_CONTENT}}}plain").text = note

    if marker:
        makers = SubElement(t, f"{{{NS_CONTENT}}}markers")
        SubElement(makers, f"{{{NS_CONTENT}}}marker-ref", {"marker-id": marker})

    return t


def _attach_children(topic):
    children = SubElement(topic, f"{{{NS_CONTENT}}}children")
    attached = SubElement(children, f"{{{NS_CONTENT}}}topics", {"type": "attached"})
    return attached


def _priority_marker(priority: str | None) -> str | None:
    # Priority mapping per spec in this SKILL.
    mapping = {
        "P0": "priority-1",
        "P1": "priority-2",
        "P2": "priority-3",
        "P3": "priority-4",
        "P4": "priority-5",
    }
    return mapping.get((priority or "").strip())


def build_content_xml(data: dict) -> bytes:
    # Root
    xmap = Element(f"{{{NS_CONTENT}}}xmap-content", {"version": "2.0"})

    sheet = SubElement(xmap, f"{{{NS_CONTENT}}}sheet", {"id": _u()})
    SubElement(sheet, f"{{{NS_CONTENT}}}title").text = "Sheet 1"

    root_title = data.get("root_title") or "用例集"
    root = _topic(sheet, root_title)
    root_attached = _attach_children(root)

    for g in data.get("groups") or []:
        g_title = g.get("title") or "+分组"
        g_topic = _topic(root_attached, g_title)
        g_attached = _attach_children(g_topic)

        for c in g.get("cases") or []:
            c_title = c.get("title") or "用例标题"
            c_note = c.get("note")
            c_marker = _priority_marker(c.get("priority"))
            c_topic = _topic(g_attached, c_title, note=c_note, marker=c_marker)
            c_attached = _attach_children(c_topic)

            # Always create exactly one "detail" node under the case, and put steps under it,
            # matching the documented hierarchy (detail -> steps -> expected).
            pre = (c.get("preconditions") or "").strip()
            desc = (c.get("description") or "").strip()
            detail_label = "前置条件" if pre else "文本描述"
            detail_text = pre if pre else desc

            detail_node = _topic(c_attached, detail_label)
            detail_attached = _attach_children(detail_node)
            if detail_text:
                _topic(detail_attached, detail_text)

            steps = c.get("steps") or []
            steps_node = _topic(detail_attached, "步骤")
            steps_attached = _attach_children(steps_node)
            if steps:
                for i, s in enumerate(steps, start=1):
                    action = (s.get("action") or "").strip()
                    expected = (s.get("expected") or "").strip()
                    step_node = _topic(steps_attached, f"步骤 {i}: {action}" if action else f"步骤 {i}")
                    step_attached = _attach_children(step_node)
                    if expected:
                        _topic(step_attached, f"预期 {i}: {expected}")
            else:
                # Keep a placeholder structure to avoid empty branches in some XMind viewers.
                _topic(steps_attached, "步骤 1")

    # XML bytes with UTF-8 encoding; no pretty-print to keep it deterministic.
    xml = tostring(xmap, encoding="utf-8", xml_declaration=True)
    return xml


def build_manifest_xml() -> bytes:
    m = Element(f"{{{NS_MANIFEST}}}manifest")
    SubElement(m, f"{{{NS_MANIFEST}}}file-entry", {"full-path": "content.xml", "media-type": "text/xml"})
    SubElement(m, f"{{{NS_MANIFEST}}}file-entry", {"full-path": "meta.xml", "media-type": "text/xml"})
    SubElement(m, f"{{{NS_MANIFEST}}}file-entry", {"full-path": "styles.xml", "media-type": "text/xml"})
    return tostring(m, encoding="utf-8", xml_declaration=True)


def build_meta_xml() -> bytes:
    meta = Element(f"{{{NS_META}}}meta", {"version": "2.0"})
    SubElement(meta, f"{{{NS_META}}}CreateTime").text = _iso_now()
    return tostring(meta, encoding="utf-8", xml_declaration=True)


def build_styles_xml() -> bytes:
    s = Element(f"{{{NS_STYLE}}}xmap-styles", {"version": "2.0"})
    return tostring(s, encoding="utf-8", xml_declaration=True)


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 xmind_build.py <input.json> <output.xmind>", file=sys.stderr)
        return 2

    in_path = sys.argv[1]
    out_path = sys.argv[2]

    with open(in_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    content_xml = build_content_xml(data)
    manifest_xml = build_manifest_xml()
    meta_xml = build_meta_xml()
    styles_xml = build_styles_xml()

    out_path = os.path.abspath(out_path)
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)

    # XMind 8 format: zip container with at least content.xml and META-INF/manifest.xml
    with zipfile.ZipFile(out_path, "w", compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr("content.xml", content_xml)
        z.writestr("meta.xml", meta_xml)
        z.writestr("styles.xml", styles_xml)
        z.writestr("META-INF/manifest.xml", manifest_xml)

    if not os.path.exists(out_path) or os.path.getsize(out_path) <= 0:
        raise RuntimeError("Failed to write output .xmind")

    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## Quality Standards

Each test case should be:
- Atomic: one clear verification goal per case where possible
- Traceable: tied to a documented behavior, rule, or interface
- Actionable: steps are executable and specific
- Verifiable: expected results are objective and testable
- Prioritized: indicate business or release criticality
- Balanced: include both happy path and edge/failure coverage

Each test point should be:
- Derived from source materials or clearly marked assumptions
- Grouped logically by feature or workflow
- Prioritized with explicit rationale
- Suitable for expansion into detailed test cases
- Written in a format consistent with B2B web QA deliverables

Avoid:
- Vague steps such as "verify it works"
- Expected results without measurable criteria
- Repeating the same scenario with trivial wording changes
- Inventing business rules that were not implied by the source material

## Coverage Heuristics

When relevant, ensure coverage considers:
- Required fields vs optional fields
- Valid inputs vs invalid inputs
- Minimum, maximum, and boundary values
- Empty, null, duplicate, and malformed data
- State transitions and workflow branching
- Different user roles and permission levels
- Network, timeout, retry, and dependency failures
- Error messages and fallback behavior
- Localization, timezone, and formatting differences
- Audit trail, logging, and data persistence expectations
- Search, filter, sort, pagination, and export behavior on web tables
- Bulk actions, modal dialogs, drawer forms, and approval operations
- Multi-role collaboration and upstream/downstream TTMS process continuity
- Date range, time window, and benchmark selection logic
- Metric card, glossary, chart, and table consistency
- Drill-down consistency from summary views into detailed views
- Empty state, loading state, and partial data state handling
- Cross-module consistency where one module references another module's definitions
- ACC stage rules, audience transition rules, and model-specific behavior
- Nomination status gating, qualification review, invite link visibility, and onboarding constraints
- Keyword, asset, account ID, and file upload validation rules
- P0 release-critical path coverage and whether the main TTMS business objective can still be completed end to end

## TTMS-Specific Testing Guidance

Prioritize the following TTMS-specific behaviors whenever they appear in the source materials:

### Nomination Center

- Nomination creation and submission flows
- Brand qualification upload and validation
- Trademark owner vs authorized representative branches
- Processing status and qualification review status gating
- Invite link visibility and activation constraints
- Account ID field rules and brand-exclusive vs brand-mixed definitions
- Internal vs external access visibility

### Brand Diagnosis

- Funnel grouping such as Premium Reach, Massive Reach, Consideration, and Conversion
- Metric glossary correctness and tooltip consistency
- Campaign mapping logic and classification correctness
- Benchmark-dependent metrics and cross-card consistency

### Audience

- ACC stage definitions and transition logic
- Transition tiles, diagram/table toggle, and drill-down flows
- Touchpoint, creator, and video insight sections
- Time window logic such as past 7, 15, and 30 days
- Model-specific behavior such as Web Payment, Web Payment and Registration, App Payment, and Ticketing

### Brand Perception / Merchandise Mart / Catalog Analytics / Post Campaign Report

- Filter combinations, segmentation dimensions, and result consistency
- Table and chart synchronization
- Data freshness, no-data behavior, and metric explanation content
- Export or reporting workflow correctness

## Link-Based Generation Rules

When the user provides links:
- Read and use the requirement and technical documents as the primary source of truth when accessible.
- Use a matching TTMS playbook only as a supplementary business source when the provided documents do not fully explain TTMS-specific terminology, workflow semantics, role definitions, metric meanings, or existing module behavior.
- Use `TTMS Business & Quality Sharing` and `TTMS OnePage` as shared supplementary context when you need TTMS-wide business understanding, quality expectations, release-critical path context, or cross-module relationship clarification.
- Extract testable statements, flows, constraints, field rules, and edge conditions from the linked material.
- Do not merely summarize the document. Convert the source content into test points and then into test cases.
- If multiple links are provided, merge overlapping requirements and remove duplicate coverage.
- If the links conflict, call out the inconsistency and mark the affected test points as needing clarification.

If the user does not provide requirement or technical documents, you may use the built-in TTMS playbooks as a fallback knowledge source, but you must clearly mark the result as a draft based on supplementary business materials rather than primary requirement input.

## Clarification Strategy

If the user provides documents but they are incomplete, ask concise follow-up questions before finalizing.

If the user cannot provide documents, proceed with a draft using the available context and clearly mark:
- Assumptions
- Missing information
- Areas requiring confirmation

## Response Template

Use this structure by default:

### XMind File (Mandatory)

Return the generated file path first:

`XMind file: /absolute/path/to/output.xmind`

### P0 Scenario Summary

List all identified `P0场景` first. If none exist, explicitly say:

`本次范围未识别出 P0 场景`

### Full Case Coverage Summary

Briefly summarize how the final output still covers the full agreed scope beyond `P0`, for example:
- core workflow cases
- non-P0 functional cases
- validation and negative cases
- permission and role cases
- boundary and data cases
- integration and regression cases

### Source Summary (Short)

List the requirement documents, technical documents, and any supplementary TTMS playbooks or text inputs used.

### Outline Preview (Optional)

Only include a small outline preview in chat when the user asks, or when it helps quickly validate grouping and priorities. The preview MUST follow:
- `用例集`
- `分组 N`
- `[P0]用例标题` or `用例标题`
- `前置条件` / `文本描述`
- `步骤`
- `预期结果`

### Extracted Test Points

Provide this section only when the user asks for explicit test points or when traceability needs to be shown separately.

### Scope Summary

Briefly summarize what TTMS web capability is being tested and what materials were used.

### Assumptions

List any assumptions made due to missing or ambiguous information.

### Test Cases

Provide the detailed test case table only when the user asks for table format, dual format, or explicit tabular traceability.

### Risks and Open Questions

List gaps, ambiguities, or recommended follow-up items.

## Example Opening

`Please share the requirement document link, technical design document link, API documentation, prototype, or any other relevant references for the feature first. I will analyze those materials and generate a real .xmind file by default (XMind 8 compatible), with priorities and executable case steps. If the feature depends on TTMS-specific module rules or business semantics that are not fully described in the provided materials, I may also consult the relevant TTMS playbook as a supplementary reference. If formal documentation is incomplete, send me the feature description, user roles, key workflows, field rules, and acceptance criteria, and I will generate a draft while marking assumptions and open questions clearly.`
