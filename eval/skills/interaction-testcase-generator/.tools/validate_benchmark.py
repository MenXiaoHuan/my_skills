#!/usr/bin/env python3
import argparse
import importlib.util
import json
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parent.parent
BASELINE_PATH = ROOT / "baseline.json"
CASES_DIR = ROOT / "cases"
IR_DIR = ROOT / "ir"
QUALITY_CHECKER_PATH = Path(__file__).resolve().parent / "check_case_tree_quality.py"
REPO_ROOT = Path(__file__).resolve().parents[4]
XMIND_BUILD_PATH = (
    REPO_ROOT
    / "skills"
    / "interaction-testcase-generator"
    / "scripts"
    / "xmind_build.py"
)
XMIND_MEMBERS = {
    "content.xml",
    "meta.xml",
    "styles.xml",
    "META-INF/manifest.xml",
}
XMIND_NS = {"x": "urn:xmind:xmap:xmlns:content:2.0"}
STRUCTURE_QUALITY_FIELDS = {
    "id",
    "input_json",
    "ir_json",
    "selected_case_ids",
    "max_top_level_groups",
    "required_top_level_groups",
    "forbidden_top_level_groups",
    "requires_other_group",
    "max_weak_expectations",
    "max_empty_expected",
    "max_missing_preconditions",
    "min_schema_complete_rate",
    "max_duplicate_titles",
    "min_average_steps_per_case",
    "max_trailing_chinese_periods",
    "min_business_goal_coverage_rate",
    "min_high_risk_goal_path_coverage_rate",
    "max_precondition_action_leaks",
    "max_unobservable_expectations",
    "min_required_atom_coverage_rate",
    "max_schema_errors",
    "max_invalid_priorities",
    "max_priority_prefix_mismatches",
    "max_normalized_duplicate_titles",
    "max_fingerprint_duplicate_clusters",
    "max_api_without_source",
    "max_data_without_invariant",
    "min_api_coverage_rate",
    "min_data_invariant_coverage_rate",
}
ARTIFACT_FIELDS = {"id", "input_json"}

QUALITY_SPEC = importlib.util.spec_from_file_location(
    "check_case_tree_quality",
    QUALITY_CHECKER_PATH,
)
QUALITY_MODULE = importlib.util.module_from_spec(QUALITY_SPEC)
assert QUALITY_SPEC.loader is not None
QUALITY_SPEC.loader.exec_module(QUALITY_MODULE)

XMIND_SPEC = importlib.util.spec_from_file_location(
    "xmind_build",
    XMIND_BUILD_PATH,
)
XMIND_MODULE = importlib.util.module_from_spec(XMIND_SPEC)
assert XMIND_SPEC.loader is not None
XMIND_SPEC.loader.exec_module(XMIND_MODULE)


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def resolve_fixture_path(relative_path: str, field_name: str) -> Path:
    require(
        relative_path.startswith(("cases/", "ir/")),
        f"{field_name} must reference cases/*.json or ir/*.json",
    )
    require(relative_path.endswith(".json"), f"{field_name} must reference JSON")
    path = ROOT / relative_path
    require(path.exists() and path.is_file(), f"missing fixture: {path}")
    return path


def validate_suite_shape(benchmark: dict) -> None:
    require(
        benchmark.get("skill_name") == "interaction-testcase-generator",
        "baseline skill_name must be interaction-testcase-generator",
    )
    for suite_name in ("structure_quality_suite", "artifact_suite"):
        require(
            isinstance(benchmark.get(suite_name), list),
            f"{suite_name} must be a list",
        )
        require(benchmark[suite_name], f"{suite_name} must not be empty")
    require(
        "coverage_ledger_suite" not in benchmark,
        "self-reported coverage_ledger_suite is forbidden",
    )


def validate_structure_quality_config(case: dict) -> None:
    case_id = case["id"]
    unknown_fields = sorted(set(case) - STRUCTURE_QUALITY_FIELDS)
    require(
        not unknown_fields,
        f"{case_id} has unknown fields: {', '.join(unknown_fields)}",
    )
    maximum_keys = (
        "max_top_level_groups",
        "max_weak_expectations",
        "max_empty_expected",
        "max_trailing_chinese_periods",
        "max_duplicate_titles",
        "max_precondition_action_leaks",
        "max_unobservable_expectations",
        "max_schema_errors",
        "max_invalid_priorities",
        "max_priority_prefix_mismatches",
        "max_normalized_duplicate_titles",
        "max_fingerprint_duplicate_clusters",
        "max_api_without_source",
        "max_data_without_invariant",
    )
    for key in maximum_keys:
        value = case.get(key)
        if value is not None:
            require(
                isinstance(value, int) and value >= 0,
                f"{case_id} {key} must be a non-negative integer",
            )

    minimum_rate_keys = (
        "min_schema_complete_rate",
        "min_business_goal_coverage_rate",
        "min_high_risk_goal_path_coverage_rate",
        "min_required_atom_coverage_rate",
        "min_api_coverage_rate",
        "min_data_invariant_coverage_rate",
    )
    for key in minimum_rate_keys:
        value = case.get(key)
        if value is not None:
            require(
                isinstance(value, (int, float)) and 0 <= value <= 1,
                f"{case_id} {key} must be between 0 and 1",
            )


def validate_fixture_references(benchmark: dict) -> None:
    referenced_cases = set()
    referenced_ir = set()
    for case in benchmark["structure_quality_suite"]:
        case_path = resolve_fixture_path(
            case["input_json"],
            f"{case['id']}.input_json",
        )
        ir_path = resolve_fixture_path(case["ir_json"], f"{case['id']}.ir_json")
        referenced_cases.add(case_path.name)
        referenced_ir.add(ir_path.name)
    for case in benchmark["artifact_suite"]:
        case_path = resolve_fixture_path(
            case["input_json"],
            f"{case['id']}.input_json",
        )
        referenced_cases.add(case_path.name)

    case_names = {path.name for path in CASES_DIR.glob("*.json")}
    ir_names = {path.name for path in IR_DIR.glob("*.json")}
    require(
        case_names == referenced_cases,
        f"case fixture references mismatch: missing={sorted(case_names - referenced_cases)}, unknown={sorted(referenced_cases - case_names)}",
    )
    require(
        ir_names == referenced_ir,
        f"IR fixture references mismatch: missing={sorted(ir_names - referenced_ir)}, unknown={sorted(referenced_ir - ir_names)}",
    )


def validate_structure_suite(benchmark: dict) -> None:
    for case in benchmark["structure_quality_suite"]:
        validate_structure_quality_config(case)
        case_tree = load_json(ROOT / case["input_json"])
        ir = load_json(ROOT / case["ir_json"])
        selected_case_ids = case.get("selected_case_ids")
        require(
            isinstance(selected_case_ids, list) and selected_case_ids,
            f"{case['id']} selected_case_ids must be non-empty",
        )
        metrics = QUALITY_MODULE.compute_metrics(
            case_tree,
            ir,
            selected_case_ids,
        )
        QUALITY_MODULE.validate_against_config(metrics, case, case["id"])


def _topic_title(topic) -> str:
    title = topic.find("x:title", XMIND_NS)
    return title.text or "" if title is not None else ""


def _child_topics(topic):
    return topic.findall("./x:children/x:topics/x:topic", XMIND_NS)


def _topic_semantics(topic):
    note = topic.find("./x:notes/x:plain", XMIND_NS)
    marker = topic.find("./x:markers/x:marker-ref", XMIND_NS)
    return {
        "title": _topic_title(topic),
        "note": note.text if note is not None else None,
        "marker": marker.attrib.get("marker-id") if marker is not None else None,
        "children": [
            _topic_semantics(child)
            for child in _child_topics(topic)
        ],
    }


def _expected_case_semantics(case: dict) -> dict:
    preconditions = XMIND_MODULE._strip_trailing_chinese_periods(
        case["preconditions"]
    )
    step_children = []
    for index, step in enumerate(case["steps"], start=1):
        action = XMIND_MODULE._strip_trailing_chinese_periods(step["action"])
        expected = XMIND_MODULE._strip_trailing_chinese_periods(step["expected"])
        step_children.append(
            {
                "title": f"步骤 {index}: {action}",
                "note": step.get("note") or None,
                "marker": None,
                "children": [
                    {
                        "title": f"预期 {index}: {expected}",
                        "note": None,
                        "marker": None,
                        "children": [],
                    }
                ],
            }
        )
    return {
        "title": XMIND_MODULE._case_title(case["title"], case["priority"]),
        "note": case.get("note") or None,
        "marker": XMIND_MODULE._priority_marker(case["priority"]),
        "children": [
            {
                "title": "前置条件",
                "note": None,
                "marker": None,
                "children": [
                    {
                        "title": preconditions,
                        "note": None,
                        "marker": None,
                        "children": [],
                    }
                ],
            },
            {
                "title": "步骤",
                "note": None,
                "marker": None,
                "children": step_children,
            },
        ],
    }


def _expected_group_semantics(group: dict) -> dict:
    return {
        "title": XMIND_MODULE._sanitize_title(group["title"]),
        "note": group.get("note") or None,
        "marker": None,
        "children": [
            *[
                _expected_group_semantics(child)
                for child in group.get("groups") or []
            ],
            *[
                _expected_case_semantics(case)
                for case in group.get("cases") or []
            ],
        ],
    }


def validate_artifact_matches_input(input_path: Path, output_path: Path) -> None:
    data = load_json(input_path)
    expected = {
        "title": XMIND_MODULE._sanitize_title(
            data.get("root_title") or "用例集"
        ),
        "note": data.get("note") or None,
        "marker": None,
        "children": [
            _expected_group_semantics(group)
            for group in XMIND_MODULE._normalize_groups(data["groups"])
        ],
    }
    with zipfile.ZipFile(output_path) as archive:
        root = ET.fromstring(archive.read("content.xml"))
    root_topic = root.find("./x:sheet/x:topic", XMIND_NS)
    require(root_topic is not None, "artifact mismatch: missing root topic")
    actual = _topic_semantics(root_topic)
    require(
        actual == expected,
        "artifact mismatch: input tree, notes, priorities, or markers differ",
    )


def _validate_case_topic(topic) -> None:
    title = _topic_title(topic)
    require(
        title.startswith(("[P0] ", "[P1] ", "[P2] ", "[P3] ")),
        f"case topic has invalid priority prefix: {title}",
    )
    require(
        topic.find("./x:markers/x:marker-ref", XMIND_NS) is not None,
        f"case topic has no priority marker: {title}",
    )
    children = {_topic_title(child): child for child in _child_topics(topic)}
    require("前置条件" in children, f"case has no preconditions branch: {title}")
    require("步骤" in children, f"case has no steps branch: {title}")
    require(
        _child_topics(children["前置条件"]),
        f"case has empty preconditions branch: {title}",
    )
    steps = _child_topics(children["步骤"])
    require(steps, f"case has empty steps branch: {title}")
    for step in steps:
        step_title = _topic_title(step)
        require(
            step_title.startswith("步骤 ") and not step_title.endswith("。"),
            f"invalid step topic: {step_title}",
        )
        expected = _child_topics(step)
        require(expected, f"step has no expected result: {step_title}")
        expected_title = _topic_title(expected[0])
        require(
            expected_title.startswith("预期 ") and not expected_title.endswith("。"),
            f"invalid expected topic: {expected_title}",
        )


def _validate_group_or_case(topic) -> int:
    if _topic_title(topic).startswith(("[P0] ", "[P1] ", "[P2] ", "[P3] ")):
        _validate_case_topic(topic)
        return 1
    return sum(_validate_group_or_case(child) for child in _child_topics(topic))


def run_artifact_regression(input_path: Path, output_path: Path) -> None:
    completed = subprocess.run(
        [sys.executable, str(XMIND_BUILD_PATH), str(input_path), str(output_path)],
        check=False,
        capture_output=True,
        text=True,
    )
    require(
        completed.returncode == 0,
        f"XMind build failed for {input_path}: {completed.stderr.strip()}",
    )
    require(
        output_path.exists() and output_path.stat().st_size > 0,
        f"XMind output is missing or empty: {output_path}",
    )
    with zipfile.ZipFile(output_path) as archive:
        require(
            XMIND_MEMBERS <= set(archive.namelist()),
            f"XMind members are incomplete: {output_path}",
        )
        root = ET.fromstring(archive.read("content.xml"))
    require(root.tag.endswith("xmap-content"), "content.xml root must be xmap-content")
    root_topic = root.find("./x:sheet/x:topic", XMIND_NS)
    require(root_topic is not None, "content.xml must contain a root topic")
    require(bool(_topic_title(root_topic)), "root topic title must not be empty")
    groups = _child_topics(root_topic)
    require(groups, "root topic must contain groups")
    case_count = sum(_validate_group_or_case(group) for group in groups)
    require(case_count > 0, "XMind must contain at least one case")
    validate_artifact_matches_input(input_path, output_path)


def validate_artifact_suite(benchmark: dict) -> None:
    for artifact in benchmark["artifact_suite"]:
        unknown_fields = sorted(set(artifact) - ARTIFACT_FIELDS)
        require(
            not unknown_fields,
            f"{artifact['id']} has unknown fields: {', '.join(unknown_fields)}",
        )
        require(
            "output_xmind" not in artifact,
            f"{artifact['id']} must not reference a checked-in XMind",
        )
        input_path = ROOT / artifact["input_json"]
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / f"{artifact['id']}.xmind"
            run_artifact_regression(input_path, output_path)


def validate() -> None:
    benchmark = load_json(BASELINE_PATH)
    validate_suite_shape(benchmark)
    validate_fixture_references(benchmark)
    validate_structure_suite(benchmark)
    validate_artifact_suite(benchmark)
    print("schema and quality baseline validation passed")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--list-cases", action="store_true")
    args = parser.parse_args()
    if args.list_cases:
        for path in sorted(CASES_DIR.glob("*.json")):
            print(path.name)
        return 0
    validate()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
