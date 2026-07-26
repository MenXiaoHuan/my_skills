import importlib.util
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parent / "check_case_tree_quality.py"
SPEC = importlib.util.spec_from_file_location("check_case_tree_quality", SCRIPT_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)

def case_tree():
    return {
        "root_title": "用例集",
        "groups": [
            {
                "title": "订单",
                "cases": [
                    {
                        "title": "[P1] 创建订单",
                        "priority": "P1",
                        "preconditions": "用户已登录",
                        "steps": [
                            {
                                "action": "提交订单",
                                "expected": "订单状态为已创建",
                            }
                        ],
                    }
                ],
            }
        ]
    }


def ir():
    return {
        "version": "1.0",
        "sources": [{"id": "SRC-API", "type": "api"}],
        "business_goals": [
            {"id": "G-1", "risk": "high", "required_paths": ["positive"]}
        ],
        "api_contracts": [{"id": "API-1", "source_refs": ["SRC-API"]}],
        "data_invariants": [{"id": "INV-1", "source_refs": ["SRC-API"]}],
        "states": [],
        "coverage_atoms": [
            {
                "id": "A-API",
                "kind": "api_contract",
                "target_ref": "API-1",
                "required": True,
                "risk_weight": 5,
            },
            {
                "id": "A-DATA",
                "kind": "data_consistency",
                "target_ref": "INV-1",
                "required": True,
                "risk_weight": 4,
            },
        ],
        "candidate_cases": [
            {
                "id": "C-1",
                "title": "创建订单",
                "source_refs": ["SRC-API"],
                "goal_refs": ["G-1"],
                "path_type": "positive",
                "coverage_atoms": ["A-API"],
                "module_ref": "M-ORDER",
                "business_object": "订单",
                "pre_state": "草稿",
                "trigger": "提交",
                "condition": "有效请求",
                "assertion_target": "订单状态",
                "post_state": "已创建",
            },
            {
                "id": "C-2",
                "title": "订单数据一致",
                "invariant_refs": ["INV-1"],
                "goal_refs": ["G-1"],
                "path_type": "positive",
                "coverage_atoms": ["A-DATA"],
            },
        ],
        "assumptions": [],
        "conflicts": [],
    }


class CaseTreeQualityTests(unittest.TestCase):
    def test_empty_action_is_not_schema_complete(self):
        tree = case_tree()
        tree["groups"][0]["cases"][0]["steps"][0]["action"] = ""
        metrics = MODULE.compute_metrics(tree)
        self.assertEqual(metrics["schema_complete_rate"], 0)
        self.assertEqual(metrics["schema_error_count"], 1)

    def test_invalid_priority_and_mismatched_prefix_are_reported(self):
        tree = case_tree()
        tree["groups"][0]["cases"][0]["priority"] = "P4"
        metrics = MODULE.compute_metrics(tree)
        self.assertEqual(metrics["invalid_priority_count"], 1)
        tree["groups"][0]["cases"][0]["priority"] = "P2"
        metrics = MODULE.compute_metrics(tree)
        self.assertEqual(metrics["priority_prefix_mismatch_count"], 1)

    def test_normalized_title_and_fingerprint_duplicates_are_reported(self):
        tree = case_tree()
        duplicate = {
            **tree["groups"][0]["cases"][0],
            "title": "[P1] 创建 订单。",
        }
        tree["groups"][0]["cases"].append(duplicate)
        metrics = MODULE.compute_metrics(tree)
        self.assertEqual(metrics["normalized_duplicate_title_count"], 1)

        report_ir = ir()
        report_ir["candidate_cases"].append(
            {**report_ir["candidate_cases"][0], "id": "C-3", "title": "其他标题"}
        )
        metrics = MODULE.compute_metrics(tree, report_ir, ["C-1", "C-2", "C-3"])
        self.assertEqual(metrics["fingerprint_duplicate_cluster_count"], 1)

    def test_api_and_data_traceability_failures_are_reported(self):
        report_ir = ir()
        report_ir["candidate_cases"][0]["source_refs"] = []
        report_ir["candidate_cases"][1]["invariant_refs"] = []
        metrics = MODULE.compute_metrics(case_tree(), report_ir, ["C-1", "C-2"])
        self.assertEqual(metrics["api_without_source_count"], 1)
        self.assertEqual(metrics["data_without_invariant_count"], 1)

    def test_coverage_is_computed_from_ir_and_selected_cases(self):
        metrics = MODULE.compute_metrics(case_tree(), ir(), ["C-1"])
        self.assertEqual(metrics["required_atom_coverage_rate"], 0.5)
        self.assertEqual(metrics["api_coverage_rate"], 1.0)
        self.assertEqual(metrics["data_invariant_coverage_rate"], 0.0)

    def test_threshold_validation_uses_computed_metrics(self):
        metrics = MODULE.compute_metrics(case_tree(), ir(), ["C-1", "C-2"])
        valid = {
            "min_schema_complete_rate": 1.0,
            "max_schema_errors": 0,
            "min_required_atom_coverage_rate": 1.0,
            "max_api_without_source": 0,
            "max_data_without_invariant": 0,
        }
        MODULE.validate_against_config(metrics, valid, "case")
        with self.assertRaises(SystemExit):
            MODULE.validate_against_config(
                metrics,
                {"min_required_atom_coverage_rate": 1.1},
                "case",
            )


if __name__ == "__main__":
    unittest.main()
