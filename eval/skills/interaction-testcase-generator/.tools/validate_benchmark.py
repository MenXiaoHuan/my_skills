#!/usr/bin/env python3
import argparse
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
BASELINE_PATH = ROOT / "baseline.json"
CASES_DIR = ROOT / "cases"
IR_DIR = ROOT / "ir"
QUALITY_CHECKER_PATH = Path(__file__).resolve().parent / "check_case_tree_quality.py"

QUALITY_SPEC = importlib.util.spec_from_file_location(
    "check_case_tree_quality",
    QUALITY_CHECKER_PATH,
)
QUALITY_MODULE = importlib.util.module_from_spec(QUALITY_SPEC)
assert QUALITY_SPEC.loader is not None
QUALITY_SPEC.loader.exec_module(QUALITY_MODULE)


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


def validate_artifact_suite(benchmark: dict) -> None:
    for artifact in benchmark["artifact_suite"]:
        require(
            "output_xmind" not in artifact,
            f"{artifact['id']} must not reference a checked-in XMind",
        )
        case_tree = load_json(ROOT / artifact["input_json"])
        metrics = QUALITY_MODULE.compute_metrics(case_tree)
        require(
            metrics["schema_complete_rate"] == 1.0,
            f"{artifact['id']} artifact input must satisfy strict schema",
        )


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
