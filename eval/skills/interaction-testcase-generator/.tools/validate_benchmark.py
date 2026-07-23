#!/usr/bin/env python3
import argparse
import importlib.util
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
BASELINE_PATH = ROOT / "baseline.json"
CASES_DIR = ROOT / "cases"
QUALITY_CHECKER_PATH = Path(__file__).resolve().parent / "check_case_tree_quality.py"
CASE_FILE_RE = re.compile(r"^case_(\d{3})_[a-z0-9_]+\.json$")


QUALITY_SPEC = importlib.util.spec_from_file_location("check_case_tree_quality", QUALITY_CHECKER_PATH)
QUALITY_MODULE = importlib.util.module_from_spec(QUALITY_SPEC)
assert QUALITY_SPEC.loader is not None
QUALITY_SPEC.loader.exec_module(QUALITY_MODULE)


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def validate_coverage_ledger_case(case: dict) -> None:
    case_id = case["id"]
    artifact_path = resolve_case_path(case["artifact_json"], f"{case_id}.artifact_json")
    require(artifact_path.exists(), f"missing coverage ledger artifact: {artifact_path}")
    artifact = load_json(artifact_path)

    target_modules = case.get("target_modules", [])
    required_dimensions = set(case.get("required_dimensions", []))
    require(target_modules, f"{case_id} must define target modules")
    require(required_dimensions, f"{case_id} must define required dimensions")

    ledger = artifact.get("coverage_ledger", [])
    require(ledger, f"{case_id} artifact must include coverage_ledger")
    ledger_by_module = {str(item.get("module") or ""): item for item in ledger}
    require(
        set(target_modules).issubset(set(ledger_by_module.keys())),
        f"{case_id} coverage_ledger must cover every target module",
    )

    budgets = artifact.get("per_module_case_budget", {})
    final_counts = artifact.get("final_case_counts", {})
    variance_notes = artifact.get("budget_variance_notes", {})
    require(budgets, f"{case_id} artifact must include per_module_case_budget")
    require(final_counts, f"{case_id} artifact must include final_case_counts")

    for module_name in target_modules:
        item = ledger_by_module[module_name]
        covered = set(item.get("covered_dimensions", []))
        skipped = item.get("intentionally_skipped_dimensions", {})
        missing = required_dimensions - covered - set(skipped.keys())
        require(not missing, f"{case_id} {module_name} missing coverage dimensions: {sorted(missing)}")

        for skipped_dimension, reason in skipped.items():
            require(str(reason).strip(), f"{case_id} {module_name} skipped {skipped_dimension} without reason")

        budget = budgets.get(module_name)
        require(
            isinstance(budget, list) and len(budget) == 2,
            f"{case_id} budget for {module_name} must be [min, max]",
        )
        min_count, max_count = int(budget[0]), int(budget[1])
        require(0 <= min_count <= max_count, f"{case_id} budget for {module_name} must have min <= max")

        count = int(final_counts.get(module_name, -1))
        if not (min_count <= count <= max_count):
            require(
                str(variance_notes.get(module_name, "")).strip(),
                f"{case_id} {module_name} count outside budget without variance note",
            )


def non_hidden_case_paths() -> list[Path]:
    require(CASES_DIR.exists(), f"missing cases directory: {CASES_DIR}")
    return sorted(path for path in CASES_DIR.iterdir() if not path.name.startswith("."))


def validate_flat_cases() -> None:
    case_paths = non_hidden_case_paths()
    require(case_paths, "cases directory must contain at least one JSON case file")

    for index, path in enumerate(case_paths, start=1):
        require(path.is_file(), f"case entry must be a flat file, not a directory: {path}")
        match = CASE_FILE_RE.match(path.name)
        require(bool(match), f"case file must match case_001_descriptive_name.json: {path.name}")
        require(int(match.group(1)) == index, f"case file numbering must be continuous: expected case_{index:03d}, got {path.name}")
        payload = load_json(path)
        require(isinstance(payload, dict), f"case file must contain a JSON object: {path}")


def resolve_case_path(relative_path: str, field_name: str) -> Path:
    require(relative_path.startswith("cases/"), f"{field_name} must reference cases/*.json: {relative_path}")
    require("/input.json" not in relative_path, f"{field_name} must not reference nested input.json: {relative_path}")
    require(relative_path.endswith(".json"), f"{field_name} must reference a JSON case file: {relative_path}")
    case_path = ROOT / relative_path
    require(CASE_FILE_RE.match(case_path.name) is not None, f"{field_name} must use case_001_descriptive_name.json: {relative_path}")
    require(case_path.exists(), f"missing referenced case file: {case_path}")
    return case_path


def iter_case_reference_fields(benchmark: dict):
    for suite_name in ("structure_quality_suite", "artifact_suite"):
        for case in benchmark.get(suite_name, []):
            if "input_json" in case:
                yield suite_name, case["id"], "input_json", case["input_json"]
    for case in benchmark.get("coverage_ledger_suite", []):
        if "artifact_json" in case:
            yield "coverage_ledger_suite", case["id"], "artifact_json", case["artifact_json"]


def validate_case_references(benchmark: dict) -> None:
    referenced = set()
    for suite_name, case_id, field_name, relative_path in iter_case_reference_fields(benchmark):
        case_path = resolve_case_path(relative_path, f"{suite_name}.{case_id}.{field_name}")
        referenced.add(case_path.name)

    case_names = {path.name for path in non_hidden_case_paths()}
    missing_from_baseline = sorted(case_names - referenced)
    require(not missing_from_baseline, f"case files are not referenced by baseline.json: {missing_from_baseline}")


def validate_suite_shape(benchmark: dict) -> None:
    require(benchmark.get("skill_name") == "interaction-testcase-generator", "baseline skill_name must be interaction-testcase-generator")

    suite_names = [
        "structure_quality_suite",
        "coverage_ledger_suite",
        "artifact_suite",
    ]
    for suite_name in suite_names:
        require(isinstance(benchmark.get(suite_name), list), f"{suite_name} must be a list")


def validate_structure_quality_config(case: dict) -> None:
    case_id = case["id"]
    for key in (
        "max_trailing_chinese_periods",
        "max_precondition_action_leaks",
        "max_unobservable_expectations",
    ):
        value = case.get(key)
        if value is not None:
            require(isinstance(value, int) and value >= 0, f"{case_id} {key} must be a non-negative integer")

    for key in (
        "min_business_goal_coverage_rate",
        "min_high_risk_goal_path_coverage_rate",
    ):
        value = case.get(key)
        if value is not None:
            require(isinstance(value, (int, float)) and 0 <= value <= 1, f"{case_id} {key} must be between 0 and 1")


def validate_artifact_suite(benchmark: dict) -> None:
    for artifact in benchmark.get("artifact_suite", []):
        artifact_id = artifact["id"]
        require("output_xmind" not in artifact, f"{artifact_id} should not reference checked-in expected.xmind")
        input_json = resolve_case_path(artifact["input_json"], f"{artifact_id}.input_json")
        content = input_json.read_text(encoding="utf-8")
        for required_string in artifact.get("required_strings", []):
            require(required_string in content, f"{artifact_id} missing required string in JSON case: {required_string}")


def validate() -> None:
    benchmark = load_json(BASELINE_PATH)
    validate_flat_cases()
    validate_suite_shape(benchmark)
    validate_case_references(benchmark)
    validate_artifact_suite(benchmark)

    require(
        len(benchmark.get("coverage_ledger_suite", [])) >= 1,
        "coverage_ledger_suite must contain positive coverage-ledger examples",
    )

    for case in benchmark.get("structure_quality_suite", []):
        validate_structure_quality_config(case)
        input_json = resolve_case_path(case["input_json"], f"{case['id']}.input_json")
        require(input_json.exists(), f"missing structure input: {input_json}")
        case_tree = load_json(input_json)
        metrics = QUALITY_MODULE.compute_metrics(case_tree)
        QUALITY_MODULE.validate_against_config(metrics, case, case["id"])

    for case in benchmark.get("coverage_ledger_suite", []):
        validate_coverage_ledger_case(case)

    print("lightweight baseline validation passed")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--list-cases", action="store_true")
    args = parser.parse_args()

    if args.list_cases:
        for path in non_hidden_case_paths():
            print(path.name)
        return 0

    validate()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
