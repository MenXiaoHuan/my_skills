import importlib.util
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parent / "check_case_tree_quality.py"
SPEC = importlib.util.spec_from_file_location("check_case_tree_quality", SCRIPT_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)

VALIDATOR_PATH = Path(__file__).resolve().parent / "validate_benchmark.py"
VALIDATOR_SPEC = importlib.util.spec_from_file_location("validate_benchmark", VALIDATOR_PATH)
VALIDATOR_MODULE = importlib.util.module_from_spec(VALIDATOR_SPEC)
assert VALIDATOR_SPEC.loader is not None
VALIDATOR_SPEC.loader.exec_module(VALIDATOR_MODULE)


def _case_tree():
    return {
        "groups": [
            {
                "title": "支付",
                "cases": [
                    {
                        "title": "支付成功",
                        "priority": "P1",
                        "preconditions": "点击进入支付页。",
                        "steps": [
                            {
                                "action": "提交支付。",
                                "expected": "订单状态变为已支付。",
                            }
                        ],
                    },
                    {
                        "title": "重复支付",
                        "priority": "P2",
                        "preconditions": "订单已支付",
                        "steps": [
                            {
                                "action": "再次提交支付",
                                "expected": "处理成功",
                            }
                        ],
                    },
                ],
            }
        ],
        "_evaluation": {
            "business_goals": [
                {
                    "id": "G1",
                    "risk": "high",
                    "required_paths": ["positive", "critical_failure"],
                },
                {
                    "id": "G2",
                    "risk": "medium",
                    "required_paths": ["positive"],
                },
            ],
            "case_traceability": {
                "支付成功": {"goals": ["G1"], "path": "positive"},
                "重复支付": {"goals": ["G1"], "path": "critical_failure"},
                "不存在的用例": {"goals": ["G2"], "path": "positive"},
            },
        },
    }


class CaseTreeQualityTests(unittest.TestCase):
    def test_compute_metrics_includes_format_business_and_priority_metrics(self):
        metrics = MODULE.compute_metrics(_case_tree())

        self.assertEqual(metrics["trailing_chinese_period_count"], 3)
        self.assertEqual(metrics["business_goal_coverage_rate"], 0.5)
        self.assertEqual(metrics["high_risk_goal_path_coverage_rate"], 1.0)
        self.assertEqual(metrics["precondition_action_leak_count"], 1)
        self.assertEqual(metrics["unobservable_expectation_count"], 1)
        self.assertEqual(
            metrics["priority_distribution"],
            {"P0": 0, "P1": 1, "P2": 1, "P3": 0},
        )

    def test_goal_coverage_metrics_are_none_without_evaluation_metadata(self):
        case_tree = _case_tree()
        case_tree.pop("_evaluation")

        metrics = MODULE.compute_metrics(case_tree)

        self.assertIsNone(metrics["business_goal_coverage_rate"])
        self.assertIsNone(metrics["high_risk_goal_path_coverage_rate"])

    def test_validate_against_config_rejects_new_metric_threshold_violations(self):
        metrics = MODULE.compute_metrics(_case_tree())
        invalid_configs = [
            {"max_trailing_chinese_periods": 2},
            {"max_precondition_action_leaks": 0},
            {"max_unobservable_expectations": 0},
            {"min_business_goal_coverage_rate": 0.6},
            {"min_high_risk_goal_path_coverage_rate": 1.1},
        ]

        for config in invalid_configs:
            with self.subTest(config=config):
                with self.assertRaises(SystemExit):
                    MODULE.validate_against_config(metrics, config, "case")

    def test_validate_against_config_requires_metadata_for_coverage_thresholds(self):
        case_tree = _case_tree()
        case_tree.pop("_evaluation")
        metrics = MODULE.compute_metrics(case_tree)

        for key in (
            "min_business_goal_coverage_rate",
            "min_high_risk_goal_path_coverage_rate",
        ):
            with self.subTest(key=key):
                with self.assertRaises(SystemExit):
                    MODULE.validate_against_config(metrics, {key: 1.0}, "case")

    def test_validate_benchmark_checks_new_quality_config_ranges(self):
        valid_config = {
            "id": "case",
            "max_trailing_chinese_periods": 0,
            "max_precondition_action_leaks": 1,
            "max_unobservable_expectations": 2,
            "min_business_goal_coverage_rate": 1.0,
            "min_high_risk_goal_path_coverage_rate": 0.5,
        }
        VALIDATOR_MODULE.validate_structure_quality_config(valid_config)

        invalid_configs = [
            {"id": "case", "max_trailing_chinese_periods": -1},
            {"id": "case", "max_precondition_action_leaks": -1},
            {"id": "case", "max_unobservable_expectations": -1},
            {"id": "case", "min_business_goal_coverage_rate": 1.1},
            {"id": "case", "min_high_risk_goal_path_coverage_rate": -0.1},
        ]
        for config in invalid_configs:
            with self.subTest(config=config):
                with self.assertRaises(SystemExit):
                    VALIDATOR_MODULE.validate_structure_quality_config(config)


if __name__ == "__main__":
    unittest.main()
