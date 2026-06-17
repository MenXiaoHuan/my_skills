#!/usr/bin/env python3
import argparse
import hashlib
import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
BASELINE_PATH = ROOT / "baseline.json"
LOCK_PATH = ROOT / ".meta" / "benchmark-lock.json"
RESULTS_PATH = ROOT / ".meta" / "results-2026-06-16.json"
COMPARATIVE_EVAL_PATH = ROOT / ".meta" / "comparative-eval-2026-06-16.md"
QUALITY_CHECKER_PATH = Path(__file__).resolve().parent / "check_case_tree_quality.py"


QUALITY_SPEC = importlib.util.spec_from_file_location("check_case_tree_quality", QUALITY_CHECKER_PATH)
QUALITY_MODULE = importlib.util.module_from_spec(QUALITY_SPEC)
assert QUALITY_SPEC.loader is not None
QUALITY_SPEC.loader.exec_module(QUALITY_MODULE)


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def top_level_group_titles(case_tree: dict) -> list[str]:
    return [str(group.get("title") or "") for group in case_tree.get("groups", [])]


def validate_coverage_ledger_case(case: dict) -> None:
    case_id = case["id"]
    artifact_path = ROOT / case["artifact_json"]
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


def validate() -> None:
    benchmark = load_json(BASELINE_PATH)
    lock = load_json(LOCK_PATH)
    results = load_json(RESULTS_PATH)

    current_sha = sha256(BASELINE_PATH)
    require(
        current_sha == lock["benchmark_sha256"],
        "baseline.json sha256 does not match .meta/benchmark-lock.json; update the lock intentionally before changing the baseline",
    )

    for suite_name, expected_size in lock["expected_suite_sizes"].items():
        actual_size = len(benchmark.get(suite_name, []))
        require(
            actual_size == expected_size,
            f"{suite_name} size mismatch: expected {expected_size}, got {actual_size}",
        )

    result_total_map = {
        "trigger_accuracy": results["trigger_accuracy"]["total"],
        "near_boundary_accuracy": results["near_boundary_accuracy"]["total"],
        "comparative_eval": results["comparative_eval"]["total"],
        "multi_turn_stability": results["multi_turn_stability"]["total"],
        "output_quality": results["output_quality"]["total"],
        "coverage": results["coverage"]["total"],
    }
    for result_name, expected_total in lock["expected_result_summaries"].items():
        actual_total = result_total_map[result_name]
        require(
            actual_total == expected_total,
            f"{result_name} total mismatch: expected {expected_total}, got {actual_total}",
        )

    require(
        len(results.get("trigger_results", [])) == lock["expected_suite_sizes"]["trigger_suite"],
        "trigger_results length does not match trigger_suite size",
    )
    require(
        len(results.get("near_boundary_results", [])) == lock["expected_suite_sizes"]["near_boundary_suite"],
        "near_boundary_results length does not match near_boundary_suite size",
    )
    require(
        len(results.get("comparative_results", [])) == lock["expected_suite_sizes"]["comparative_suite"],
        "comparative_results length does not match comparative_suite size",
    )
    require(
        len(results.get("multi_turn_results", [])) == lock["expected_suite_sizes"]["multi_turn_suite"],
        "multi_turn_results length does not match multi_turn_suite size",
    )
    require(
        len(results.get("artifact_results", [])) == lock["expected_suite_sizes"]["artifact_suite"],
        "artifact_results length does not match artifact_suite size",
    )

    for artifact in benchmark.get("artifact_suite", []):
        input_json = ROOT / artifact["input_json"]
        output_xmind = ROOT / artifact["output_xmind"]
        require(input_json.exists(), f"missing artifact input: {input_json}")
        require(output_xmind.exists(), f"missing artifact output: {output_xmind}")
        require(output_xmind.stat().st_size > 0, f"empty artifact output: {output_xmind}")

    require(
        len(benchmark.get("coverage_ledger_suite", [])) >= 1,
        "coverage_ledger_suite must contain positive coverage-ledger examples",
    )

    for case in benchmark.get("dual_candidate_suite", []):
        require(case.get("expected_mode") == "dual-candidate", f"{case['id']} must expect dual-candidate mode")
        required_artifacts = set(case.get("required_internal_artifacts", []))
        required_dual_candidate_artifacts = {
            "candidate_a_draft",
            "candidate_b_draft",
            "adjudication_table",
            "execution_gate",
            "candidate_roles_different",
            "final_merge_decision_notes",
            "dropped_case_log",
            "coverage_ledger",
            "per_module_case_budget",
            "budget_variance_notes",
            "candidate_artifacts_hidden_from_user",
        }
        require(
            required_dual_candidate_artifacts.issubset(required_artifacts),
            f"{case['id']} must require auditable dual-candidate execution artifacts",
        )

    for case in benchmark.get("structure_quality_suite", []):
        input_json = ROOT / case["input_json"]
        require(input_json.exists(), f"missing structure input: {input_json}")
        case_tree = load_json(input_json)
        metrics = QUALITY_MODULE.compute_metrics(case_tree)
        QUALITY_MODULE.validate_against_config(metrics, case, case["id"])

    for case in benchmark.get("coverage_ledger_suite", []):
        validate_coverage_ledger_case(case)

    for case in benchmark.get("stability_suite", []):
        require(case.get("runs", 0) >= 3, f"{case['id']} must require at least 3 runs")
        require(case.get("metrics"), f"{case['id']} must define stability metrics")
        acceptance = case.get("acceptance") or {}
        require(
            "max_top_level_group_delta" in acceptance,
            f"{case['id']} must define max_top_level_group_delta",
        )
        require(
            "forbidden_top_level_groups" in acceptance,
            f"{case['id']} must define forbidden_top_level_groups",
        )
        target_top_level_groups = acceptance.get("target_top_level_groups", [])
        require(
            len(target_top_level_groups) >= 3,
            f"{case['id']} must define a compact target top-level module set",
        )
        require(
            len(target_top_level_groups) == len(set(target_top_level_groups)),
            f"{case['id']} target top-level module set must not contain duplicates",
        )
        for forbidden_title in acceptance.get("forbidden_top_level_groups", []):
            require(
                forbidden_title not in target_top_level_groups,
                f"{case['id']} target top-level module set contains forbidden group: {forbidden_title}",
            )
        require(
            "max_leaf_count_delta" in acceptance,
            f"{case['id']} must define max_leaf_count_delta",
        )
        require(
            acceptance["max_leaf_count_delta"] <= 10,
            f"{case['id']} max_leaf_count_delta must be <= 10 after residual drift hardening",
        )
        per_module_case_budget = acceptance.get("per_module_case_budget", {})
        require(
            per_module_case_budget,
            f"{case['id']} must define per-module case budgets",
        )
        require(
            set(target_top_level_groups).issubset(set(per_module_case_budget.keys())),
            f"{case['id']} per-module case budgets must cover every target top-level group",
        )
        for module_name, budget in per_module_case_budget.items():
            require(
                isinstance(budget, list) and len(budget) == 2,
                f"{case['id']} budget for {module_name} must be [min, max]",
            )
            require(
                0 <= int(budget[0]) <= int(budget[1]),
                f"{case['id']} budget for {module_name} must have min <= max",
            )
        required_coverage_dimensions = acceptance.get("required_coverage_dimensions", [])
        require(
            {"core", "data_correctness", "exception", "empty_state"}.issubset(set(required_coverage_dimensions)),
            f"{case['id']} must define required coverage dimensions for ledger checks",
        )
        if "reference_leaf_count" in acceptance or "min_reference_coverage_ratio" in acceptance:
            reference_leaf_count = int(acceptance.get("reference_leaf_count", 0))
            min_reference_ratio = float(acceptance.get("min_reference_coverage_ratio", 0))
            require(reference_leaf_count > 0, f"{case['id']} must define a positive reference_leaf_count")
            require(
                0.5 <= min_reference_ratio <= 1.0,
                f"{case['id']} min_reference_coverage_ratio must be between 0.5 and 1.0",
            )
            min_leaf_count_floor = int(reference_leaf_count * min_reference_ratio)
            require(
                min_leaf_count_floor > acceptance["max_leaf_count_delta"],
                f"{case['id']} reference coverage floor must be stronger than drift tolerance",
            )
        observed_failures = case.get("observed_failure_examples", [])
        if observed_failures:
            require(len(observed_failures) >= 3, f"{case['id']} must record at least 3 observed failure examples")
            leaf_counts = [int(item["leaf_count"]) for item in observed_failures]
            top_counts = [int(item["top_level_group_count"]) for item in observed_failures]
            observed_titles = [
                str(title)
                for item in observed_failures
                for title in item.get("top_level_groups", [])
            ]
            require(
                max(leaf_counts) - min(leaf_counts) > acceptance["max_leaf_count_delta"],
                f"{case['id']} observed failure examples must demonstrate leaf-count drift",
            )
            require(
                max(top_counts) - min(top_counts) > 0,
                f"{case['id']} observed failure examples must demonstrate top-level structure drift",
            )
            require(
                any(title not in target_top_level_groups for title in observed_titles),
                f"{case['id']} observed failure examples must demonstrate module-name drift",
            )
            require(
                any(title in acceptance["forbidden_top_level_groups"] for title in observed_titles),
                f"{case['id']} observed failure examples must include a forbidden top-level group",
            )
        residual_drift_examples = case.get("residual_drift_examples", [])
        if residual_drift_examples:
            require(
                len(residual_drift_examples) >= 3,
                f"{case['id']} must record at least 3 residual drift examples",
            )
            residual_leaf_counts = [int(item["leaf_count"]) for item in residual_drift_examples]
            require(
                max(residual_leaf_counts) - min(residual_leaf_counts) > acceptance["max_leaf_count_delta"],
                f"{case['id']} residual drift examples must exceed the hardened leaf-count threshold",
            )
        undercoverage_examples = case.get("undercoverage_examples", [])
        if undercoverage_examples:
            reference_leaf_count = int(acceptance.get("reference_leaf_count", 0))
            min_reference_ratio = float(acceptance.get("min_reference_coverage_ratio", 0))
            require(reference_leaf_count > 0, f"{case['id']} undercoverage checks require reference_leaf_count")
            require(min_reference_ratio > 0, f"{case['id']} undercoverage checks require min_reference_coverage_ratio")
            min_leaf_count_floor = int(reference_leaf_count * min_reference_ratio)
            require(
                any(int(item["leaf_count"]) < min_leaf_count_floor for item in undercoverage_examples),
                f"{case['id']} undercoverage examples must fall below the reference coverage floor",
            )

    require(COMPARATIVE_EVAL_PATH.exists(), f"missing comparative eval document: {COMPARATIVE_EVAL_PATH}")

    print("baseline validation passed")
    print(f"baseline sha256: {current_sha}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--print-sha256", action="store_true")
    args = parser.parse_args()

    if args.print_sha256:
        print(sha256(BASELINE_PATH))
        return 0

    validate()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
