#!/usr/bin/env python3
import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
PRODUCTION_SCRIPTS = REPO_ROOT / "skills" / "interaction-testcase-generator" / "scripts"
sys.path.insert(0, str(PRODUCTION_SCRIPTS))
from quality_report import (
    build_quality_report,
    normalize_case_title,
    verification_fingerprint,
)
from validate_case_tree import ValidationError, validate_case_tree


WEAK_EXPECTATION_PATTERNS = [
    "展示正常",
    "显示正常",
    "返回正确",
    "结果正确",
    "数据正确",
    "正常展示",
    "正常显示",
]
TRAILING_CHINESE_PERIOD_RE = re.compile(r"。+\s*$")
PRECONDITION_ACTION_PATTERNS = ["点击", "输入", "选择", "提交", "调用", "校验", "打开"]
UNOBSERVABLE_EXPECTATION_PATTERNS = WEAK_EXPECTATION_PATTERNS + ["处理成功", "操作成功", "符合预期"]


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def iter_groups(groups: list[dict]):
    for group in groups or []:
        yield group
        yield from iter_groups(group.get("groups") or [])


def iter_cases(groups: list[dict]):
    for group in groups or []:
        for case in group.get("cases") or []:
            yield case
        yield from iter_cases(group.get("groups") or [])


def case_steps(case: dict) -> list[dict]:
    steps = case.get("steps") or []
    return [step for step in steps if isinstance(step, dict)] if isinstance(steps, list) else []


def has_preconditions(case: dict) -> bool:
    preconditions = case.get("preconditions")
    if isinstance(preconditions, str):
        return bool(preconditions.strip())
    if isinstance(preconditions, list):
        return any(str(item).strip() for item in preconditions)
    return False


def text_values(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        yield from (str(item) for item in value)


def compute_goal_coverage(case_tree: dict, case_titles: set[str]) -> tuple[float | None, float | None]:
    return None, None


def compute_metrics(case_tree: dict) -> dict:
    groups = case_tree.get("groups") or []
    cases = list(iter_cases(groups))
    titles = [str(case.get("title") or "") for case in cases]
    duplicate_titles = sorted(title for title, count in Counter(titles).items() if title and count > 1)

    weak_expectations = []
    empty_expected_count = 0
    missing_preconditions_count = 0
    missing_expected_count = 0
    empty_steps_count = 0
    schema_complete_count = 0
    total_steps = 0
    trailing_chinese_period_count = 0
    precondition_action_leak_count = 0
    unobservable_expectation_count = 0
    priority_distribution = {priority: 0 for priority in ("P0", "P1", "P2", "P3")}

    for case in cases:
        steps = case_steps(case)
        case_has_preconditions = has_preconditions(case)
        case_has_steps = bool(steps)
        case_has_all_expected = True

        if not case_has_preconditions:
            missing_preconditions_count += 1
        if not case_has_steps:
            empty_steps_count += 1

        precondition_values = list(text_values(case.get("preconditions")))
        trailing_chinese_period_count += sum(
            bool(TRAILING_CHINESE_PERIOD_RE.search(value)) for value in precondition_values
        )
        if any(pattern in value for value in precondition_values for pattern in PRECONDITION_ACTION_PATTERNS):
            precondition_action_leak_count += 1

        priority = str(case.get("priority") or "").upper()
        if priority in priority_distribution:
            priority_distribution[priority] += 1

        for step in steps:
            total_steps += 1
            action = str(step.get("action") or "")
            expected = str(step.get("expected") or "").strip()
            trailing_chinese_period_count += bool(TRAILING_CHINESE_PERIOD_RE.search(action))
            trailing_chinese_period_count += bool(TRAILING_CHINESE_PERIOD_RE.search(expected))
            if not expected:
                empty_expected_count += 1
                missing_expected_count += 1
                case_has_all_expected = False
                continue
            if any(pattern in expected for pattern in WEAK_EXPECTATION_PATTERNS):
                weak_expectations.append(
                    {
                        "case_title": case.get("title"),
                        "expected": expected,
                    }
                )
            if any(pattern in expected for pattern in UNOBSERVABLE_EXPECTATION_PATTERNS):
                unobservable_expectation_count += 1
        if case_has_preconditions and case_has_steps and case_has_all_expected:
            schema_complete_count += 1

    top_level_titles = [str(group.get("title") or "") for group in groups]
    business_goal_coverage_rate, high_risk_goal_path_coverage_rate = compute_goal_coverage(
        case_tree,
        set(titles),
    )
    return {
        "top_level_group_count": len(top_level_titles),
        "top_level_group_titles": top_level_titles,
        "case_count": len(cases),
        "step_count": total_steps,
        "average_steps_per_case": round(total_steps / len(cases), 3) if cases else 0,
        "empty_expected_count": empty_expected_count,
        "missing_preconditions_count": missing_preconditions_count,
        "missing_expected_count": missing_expected_count,
        "empty_steps_count": empty_steps_count,
        "schema_complete_count": schema_complete_count,
        "schema_complete_rate": round(schema_complete_count / len(cases), 4) if cases else 0,
        "weak_expectation_count": len(weak_expectations),
        "weak_expectations": weak_expectations,
        "duplicate_title_count": len(duplicate_titles),
        "duplicate_titles": duplicate_titles,
        "trailing_chinese_period_count": trailing_chinese_period_count,
        "business_goal_coverage_rate": business_goal_coverage_rate,
        "high_risk_goal_path_coverage_rate": high_risk_goal_path_coverage_rate,
        "precondition_action_leak_count": precondition_action_leak_count,
        "unobservable_expectation_count": unobservable_expectation_count,
        "priority_distribution": priority_distribution,
    }


_compute_legacy_metrics = compute_metrics


def compute_metrics(
    case_tree: dict,
    ir: dict | None = None,
    selected_case_ids: list[str] | None = None,
) -> dict:
    metrics = _compute_legacy_metrics(case_tree)
    cases = list(iter_cases(case_tree.get("groups") or []))
    allowed_priorities = {"P0", "P1", "P2", "P3"}
    invalid_priority_count = 0
    priority_prefix_mismatch_count = 0
    schema_complete_count = 0
    schema_errors = []

    try:
        validate_case_tree(case_tree)
    except ValidationError as error:
        schema_errors.append(str(error))

    normalized_titles = []
    for case in cases:
        title = str(case.get("title") or "").strip()
        priority = str(case.get("priority") or "").strip().upper()
        if priority not in allowed_priorities:
            invalid_priority_count += 1
        prefix = re.match(r"^\[(P[0-9]+)\]\s+", title, re.IGNORECASE)
        if prefix is None or prefix.group(1).upper() != priority:
            priority_prefix_mismatch_count += 1

        preconditions = case.get("preconditions")
        steps = case.get("steps")
        complete = (
            bool(title)
            and priority in allowed_priorities
            and prefix is not None
            and prefix.group(1).upper() == priority
            and isinstance(preconditions, str)
            and bool(preconditions.strip())
            and isinstance(steps, list)
            and bool(steps)
            and all(
                isinstance(step, dict)
                and isinstance(step.get("action"), str)
                and bool(step["action"].strip())
                and isinstance(step.get("expected"), str)
                and bool(step["expected"].strip())
                for step in (steps or [])
            )
        )
        schema_complete_count += int(complete)
        normalized_titles.append(normalize_case_title(title))

    normalized_duplicates = {
        title
        for title, count in Counter(normalized_titles).items()
        if title and count > 1
    }
    metrics.update(
        {
            "schema_complete_count": schema_complete_count,
            "schema_complete_rate": (
                round(schema_complete_count / len(cases), 4) if cases else 0
            ),
            "schema_error_count": 0 if schema_complete_count == len(cases) and not schema_errors else max(1, len(cases) - schema_complete_count),
            "schema_errors": schema_errors,
            "invalid_priority_count": invalid_priority_count,
            "priority_prefix_mismatch_count": priority_prefix_mismatch_count,
            "normalized_duplicate_title_count": len(normalized_duplicates),
            "normalized_duplicate_titles": sorted(normalized_duplicates),
        }
    )

    if ir is not None:
        report = build_quality_report(ir, selected_case_ids)
        selected_ids = [str(case_id) for case_id in report["selected_case_ids"]]
        tree_case_ids = [
            case.get("case_id")
            for case in cases
            if isinstance(case.get("case_id"), str)
            and case["case_id"].strip()
        ]
        tree_ir_binding_passed = (
            len(tree_case_ids) == len(cases)
            and len(tree_case_ids) == len(set(tree_case_ids))
            and set(tree_case_ids) == set(selected_ids)
        )
        selected = [
            case
            for case in ir.get("candidate_cases", [])
            if str(case.get("id")) in set(selected_ids)
        ]
        fingerprint_counts = Counter(
            verification_fingerprint(case) for case in selected
        )
        blocking = report["quality_gates"]["blocking"]
        metrics.update(
            {
                "required_atom_coverage_rate": report["required_atom_coverage"]["rate"],
                "business_goal_coverage_rate": report["goal_coverage"]["rate"],
                "api_coverage_rate": report["api_coverage"]["rate"],
                "data_invariant_coverage_rate": report["data_invariant_coverage"]["rate"],
                "high_risk_goal_path_coverage_rate": report["risk_coverage"]["high_risk_path_rate"],
                "api_without_source_count": len(blocking["api_without_source"]),
                "data_without_invariant_count": len(blocking["data_without_invariant"]),
                "fingerprint_duplicate_cluster_count": sum(
                    count > 1 for count in fingerprint_counts.values()
                ),
                "tree_ir_binding_passed": tree_ir_binding_passed,
                "quality_gate_passed": (
                    report["quality_gates"]["passed"]
                    and tree_ir_binding_passed
                ),
            }
        )
    else:
        metrics.update(
            {
                "required_atom_coverage_rate": None,
                "api_coverage_rate": None,
                "data_invariant_coverage_rate": None,
                "api_without_source_count": 0,
                "data_without_invariant_count": 0,
                "fingerprint_duplicate_cluster_count": 0,
                "tree_ir_binding_passed": None,
                "quality_gate_passed": None,
            }
        )
    return metrics


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def validate_against_config(metrics: dict, config: dict, case_id: str) -> None:
    if metrics.get("quality_gate_passed") is not None:
        require(
            metrics["quality_gate_passed"] is True,
            f"{case_id} quality gate failed",
        )

    max_top_level_groups = config.get("max_top_level_groups")
    if max_top_level_groups is not None:
        require(
            metrics["top_level_group_count"] <= max_top_level_groups,
            f"{case_id} top-level group count exceeded: expected <= {max_top_level_groups}, got {metrics['top_level_group_count']}",
        )

    for title in config.get("required_top_level_groups", []):
        require(title in metrics["top_level_group_titles"], f"{case_id} missing required top-level group: {title}")

    for title in config.get("forbidden_top_level_groups", []):
        require(title not in metrics["top_level_group_titles"], f"{case_id} contains forbidden top-level group: {title}")

    requires_other = config.get("requires_other_group")
    if requires_other is not None:
        has_other = "其他" in metrics["top_level_group_titles"]
        require(
            has_other == bool(requires_other),
            f"{case_id} requires_other_group mismatch: expected {requires_other}, got {has_other}",
        )

    max_weak_expectations = config.get("max_weak_expectations")
    if max_weak_expectations is not None:
        require(
            metrics["weak_expectation_count"] <= max_weak_expectations,
            f"{case_id} weak expectation count exceeded: expected <= {max_weak_expectations}, got {metrics['weak_expectation_count']}",
        )

    max_empty_expected = config.get("max_empty_expected")
    if max_empty_expected is not None:
        require(
            metrics["empty_expected_count"] <= max_empty_expected,
            f"{case_id} empty expected count exceeded: expected <= {max_empty_expected}, got {metrics['empty_expected_count']}",
        )

    max_missing_preconditions = config.get("max_missing_preconditions")
    if max_missing_preconditions is not None:
        require(
            metrics["missing_preconditions_count"] <= max_missing_preconditions,
            f"{case_id} missing preconditions count exceeded: expected <= {max_missing_preconditions}, got {metrics['missing_preconditions_count']}",
        )

    min_schema_complete_rate = config.get("min_schema_complete_rate")
    if min_schema_complete_rate is not None:
        require(
            metrics["schema_complete_rate"] >= min_schema_complete_rate,
            f"{case_id} schema complete rate too low: expected >= {min_schema_complete_rate}, got {metrics['schema_complete_rate']}",
        )

    max_duplicate_titles = config.get("max_duplicate_titles")
    if max_duplicate_titles is not None:
        require(
            metrics["duplicate_title_count"] <= max_duplicate_titles,
            f"{case_id} duplicate title count exceeded: expected <= {max_duplicate_titles}, got {metrics['duplicate_title_count']}",
        )

    min_average_steps = config.get("min_average_steps_per_case")
    if min_average_steps is not None:
        require(
            metrics["average_steps_per_case"] >= min_average_steps,
            f"{case_id} average steps per case too low: expected >= {min_average_steps}, got {metrics['average_steps_per_case']}",
        )

    maximum_metrics = {
        "max_trailing_chinese_periods": "trailing_chinese_period_count",
        "max_precondition_action_leaks": "precondition_action_leak_count",
        "max_unobservable_expectations": "unobservable_expectation_count",
    }
    for config_key, metric_key in maximum_metrics.items():
        maximum = config.get(config_key)
        if maximum is not None:
            require(
                metrics[metric_key] <= maximum,
                f"{case_id} {metric_key} exceeded: expected <= {maximum}, got {metrics[metric_key]}",
            )

    minimum_metrics = {
        "min_business_goal_coverage_rate": "business_goal_coverage_rate",
        "min_high_risk_goal_path_coverage_rate": "high_risk_goal_path_coverage_rate",
        "min_required_atom_coverage_rate": "required_atom_coverage_rate",
        "min_api_coverage_rate": "api_coverage_rate",
        "min_data_invariant_coverage_rate": "data_invariant_coverage_rate",
    }
    for config_key, metric_key in minimum_metrics.items():
        minimum = config.get(config_key)
        if minimum is not None:
            actual = metrics[metric_key]
            require(actual is not None, f"{case_id} {metric_key} requires an IR fixture")
            require(
                actual >= minimum,
                f"{case_id} {metric_key} too low: expected >= {minimum}, got {actual}",
            )

    regression_maximum_metrics = {
        "max_schema_errors": "schema_error_count",
        "max_invalid_priorities": "invalid_priority_count",
        "max_priority_prefix_mismatches": "priority_prefix_mismatch_count",
        "max_normalized_duplicate_titles": "normalized_duplicate_title_count",
        "max_fingerprint_duplicate_clusters": "fingerprint_duplicate_cluster_count",
        "max_api_without_source": "api_without_source_count",
        "max_data_without_invariant": "data_without_invariant_count",
    }
    for config_key, metric_key in regression_maximum_metrics.items():
        maximum = config.get(config_key)
        if maximum is not None:
            require(
                metrics[metric_key] <= maximum,
                f"{case_id} {metric_key} exceeded: expected <= {maximum}, got {metrics[metric_key]}",
            )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_json")
    parser.add_argument("--print-metrics", action="store_true")
    args = parser.parse_args()

    metrics = compute_metrics(load_json(Path(args.input_json)))
    if args.print_metrics:
        print(json.dumps(metrics, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
