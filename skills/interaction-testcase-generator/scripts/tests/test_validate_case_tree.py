import importlib.util
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "validate_case_tree.py"
SPEC = importlib.util.spec_from_file_location("validate_case_tree", SCRIPT_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


def valid_tree():
    return {
        "root_title": "用例集",
        "groups": [
            {
                "title": "订单",
                "groups": [],
                "cases": [
                    {
                        "title": "[P1] 创建订单",
                        "priority": "P1",
                        "preconditions": "用户已登录",
                        "steps": [{"action": "提交订单", "expected": "创建成功"}],
                    }
                ],
            }
        ],
    }


INVALID_CASES = [
    {"title": "", "priority": "P1", "preconditions": "无特殊前置条件", "steps": []},
    {
        "title": "[P1] 示例",
        "priority": "P4",
        "preconditions": "无特殊前置条件",
        "steps": [{"action": "执行", "expected": "成功"}],
    },
    {
        "title": "[P2] 示例",
        "priority": "P1",
        "preconditions": "无特殊前置条件",
        "steps": [{"action": "执行", "expected": "成功"}],
    },
    {
        "title": "[P1] 示例",
        "priority": "P1",
        "preconditions": [],
        "steps": [{"action": "执行", "expected": "成功"}],
    },
    {
        "title": "[P1] 示例",
        "priority": "P1",
        "preconditions": "无特殊前置条件",
        "steps": [{"action": "", "expected": "成功"}],
    },
    {
        "title": "[P1] 示例",
        "priority": "P1",
        "preconditions": "无特殊前置条件",
        "steps": [{"action": "执行", "expected": ""}],
    },
]


class ValidateCaseTreeTests(unittest.TestCase):
    def test_valid_tree_is_returned_unchanged(self):
        tree = valid_tree()
        self.assertIs(MODULE.validate_case_tree(tree), tree)

    def test_rejects_invalid_cases_with_json_path(self):
        for invalid_case in INVALID_CASES:
            with self.subTest(case=invalid_case):
                tree = valid_tree()
                tree["groups"][0]["cases"] = [invalid_case]
                with self.assertRaisesRegex(
                    MODULE.ValidationError,
                    r"groups\[0\]\.cases\[0\]",
                ):
                    MODULE.validate_case_tree(tree)

    def test_rejects_invalid_top_level_and_group_shapes(self):
        invalid_inputs = [
            ([], r"\$"),
            ({"groups": []}, r"groups"),
            ({"groups": [{"title": "", "groups": [], "cases": []}]}, r"groups\[0\]\.title"),
            ({"groups": [{"title": "订单", "groups": {}, "cases": []}]}, r"groups\[0\]\.groups"),
            ({"groups": [{"title": "订单", "groups": [], "cases": {}}]}, r"groups\[0\]\.cases"),
        ]
        for data, path in invalid_inputs:
            with self.subTest(data=data):
                with self.assertRaisesRegex(MODULE.ValidationError, path):
                    MODULE.validate_case_tree(data)


if __name__ == "__main__":
    unittest.main()
