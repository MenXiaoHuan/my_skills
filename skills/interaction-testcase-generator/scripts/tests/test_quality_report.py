import importlib.util
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "quality_report.py"
SPEC = importlib.util.spec_from_file_location("quality_report", SCRIPT_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


def minimal_ir():
    return {
        "version": "1.0",
        "sources": [{"id": "SRC-1", "type": "api"}],
        "business_goals": [
            {
                "id": "G-1",
                "risk": "high",
                "required_paths": ["positive", "critical_failure"],
            }
        ],
        "api_contracts": [{"id": "API-1", "source_refs": ["SRC-1"]}],
        "data_invariants": [{"id": "INV-1", "source_refs": ["SRC-1"]}],
        "states": [],
        "coverage_atoms": [
            {
                "id": "A-1",
                "kind": "api_contract",
                "target_ref": "API-1",
                "required": True,
                "risk_weight": 5,
            },
            {
                "id": "A-2",
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
                "goal_refs": ["G-1"],
                "path_type": "positive",
                "coverage_atoms": ["A-1"],
                "source_refs": ["SRC-1"],
                "execution_cost": 1,
            },
            {
                "id": "C-2",
                "title": "重复请求",
                "goal_refs": ["G-1"],
                "path_type": "critical_failure",
                "coverage_atoms": ["A-1"],
                "source_refs": ["SRC-1"],
                "execution_cost": 1,
            },
            {
                "id": "C-3",
                "title": "订单数据一致",
                "goal_refs": ["G-1"],
                "path_type": "positive",
                "coverage_atoms": ["A-2"],
                "invariant_refs": ["INV-1"],
                "execution_cost": 1,
            },
        ],
        "assumptions": [],
        "conflicts": [],
    }


class QualityReportTests(unittest.TestCase):
    def test_computes_coverage_and_preserves_different_paths_for_adjudication(self):
        report = MODULE.build_quality_report(minimal_ir(), ["C-1", "C-2", "C-3"])
        self.assertEqual(report["required_atom_coverage"]["rate"], 1.0)
        self.assertEqual(report["api_coverage"]["rate"], 1.0)
        self.assertEqual(report["data_invariant_coverage"]["rate"], 1.0)
        self.assertEqual(report["risk_coverage"]["high_risk_path_rate"], 1.0)
        self.assertEqual(report["duplicate_clusters"][0]["case_ids"], ["C-1", "C-2"])
        self.assertEqual(report["duplicate_clusters"][0]["decision"], "keep_separate")

    def test_blocks_api_case_without_source_evidence(self):
        ir = minimal_ir()
        ir["candidate_cases"][0]["source_refs"] = []
        report = MODULE.build_quality_report(ir, ["C-1", "C-2", "C-3"])
        self.assertFalse(report["quality_gates"]["passed"])
        self.assertIn("C-1", report["quality_gates"]["blocking"]["api_without_source"])

    def test_blocks_data_case_without_invariant_reference(self):
        ir = minimal_ir()
        ir["candidate_cases"][2]["invariant_refs"] = []
        report = MODULE.build_quality_report(ir, ["C-1", "C-2", "C-3"])
        self.assertIn(
            "C-3",
            report["quality_gates"]["blocking"]["data_without_invariant"],
        )

    def test_normalizes_title_and_builds_deterministic_fingerprint(self):
        self.assertEqual(MODULE.normalize_case_title("[P1]  创建 订单。"), "创建订单")
        first = {
            "module_ref": "M-1",
            "business_object": "订单",
            "pre_state": "草稿",
            "trigger": "提交",
            "condition": "库存充足",
            "assertion_target": "订单状态",
            "post_state": "已创建",
        }
        second = dict(first, title="任意标题")
        self.assertEqual(
            MODULE.verification_fingerprint(first),
            MODULE.verification_fingerprint(second),
        )

    def test_selects_stable_minimum_sufficient_set(self):
        self.assertEqual(
            MODULE.select_minimum_sufficient_cases(minimal_ir()),
            ["C-1", "C-3", "C-2"],
        )


if __name__ == "__main__":
    unittest.main()
