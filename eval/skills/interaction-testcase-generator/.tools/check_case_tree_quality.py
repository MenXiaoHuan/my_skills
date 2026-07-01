#!/usr/bin/env python3
import argparse
import json
from collections import Counter
from pathlib import Path


WEAK_EXPECTATION_PATTERNS = [
    "展示正常",
    "显示正常",
    "返回正确",
    "结果正确",
    "数据正确",
    "正常展示",
    "正常显示",
]


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

    for case in cases:
        steps = case_steps(case)
        case_has_preconditions = has_preconditions(case)
        case_has_steps = bool(steps)
        case_has_all_expected = True

        if not case_has_preconditions:
            missing_preconditions_count += 1
        if not case_has_steps:
            empty_steps_count += 1

        for step in steps:
            total_steps += 1
            expected = str(step.get("expected") or "").strip()
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
        if case_has_preconditions and case_has_steps and case_has_all_expected:
            schema_complete_count += 1

    top_level_titles = [str(group.get("title") or "") for group in groups]
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
    }


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def validate_against_config(metrics: dict, config: dict, case_id: str) -> None:
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
