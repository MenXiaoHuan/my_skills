#!/usr/bin/env python3
import argparse
import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
BASELINE_PATH = ROOT / "baseline.json"
LOCK_PATH = ROOT / ".meta" / "benchmark-lock.json"
RESULTS_PATH = ROOT / ".meta" / "results-2026-06-16.json"
COMPARATIVE_EVAL_PATH = ROOT / ".meta" / "comparative-eval-2026-06-16.md"


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


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
