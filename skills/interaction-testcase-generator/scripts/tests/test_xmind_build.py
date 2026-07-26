import importlib.util
import unittest
from pathlib import Path
from xml.etree import ElementTree as ET


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "xmind_build.py"
SPEC = importlib.util.spec_from_file_location("xmind_build", SCRIPT_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)
NS = {"x": MODULE.NS_CONTENT}


def case(title, priority="P1", **extra):
    return {
        "title": f"[{priority}] {title}",
        "priority": priority,
        "preconditions": extra.pop("preconditions", "用户已登录"),
        "steps": extra.pop(
            "steps",
            [{"action": "执行操作", "expected": "展示可观察结果"}],
        ),
        **extra,
    }


def tree(groups, **extra):
    return {"root_title": "用例集", "groups": groups, **extra}


def all_titles(root):
    return [title.text for title in root.findall(".//x:title", NS)]


def child_titles(node):
    return [
        child.find("x:title", NS).text
        for child in node.findall("./x:children/x:topics/x:topic", NS)
    ]


class XMindBuildTests(unittest.TestCase):
    def test_auto_merges_shared_non_generic_parent(self):
        data = tree(
            [
                {"title": "订单 - 列表", "cases": [case("列表展示")]},
                {"title": "订单 - 详情", "cases": [case("详情展示")]},
            ]
        )
        root = ET.fromstring(MODULE.build_content_xml(data))
        root_topic = root.find("./x:sheet/x:topic", NS)
        self.assertEqual(child_titles(root_topic), ["订单"])
        parent = root_topic.find("./x:children/x:topics/x:topic", NS)
        self.assertEqual(child_titles(parent), ["列表", "详情"])

    def test_keeps_generic_parent_groups_separate(self):
        data = tree(
            [
                {"title": "页面 - 列表", "cases": [case("列表展示")]},
                {"title": "页面 - 详情", "cases": [case("详情展示")]},
            ]
        )
        root = ET.fromstring(MODULE.build_content_xml(data))
        root_topic = root.find("./x:sheet/x:topic", NS)
        self.assertEqual(child_titles(root_topic), ["页面 - 列表", "页面 - 详情"])

    def test_renders_priority_notes_and_strips_only_trailing_chinese_periods(self):
        data = tree(
            [
                {
                    "title": "订单",
                    "note": "分组说明。",
                    "cases": [
                        case(
                            "创建订单。",
                            "P0",
                            note="用例说明。",
                            preconditions="用户已登录。。 ",
                            steps=[
                                {
                                    "action": "提交订单。确认状态。。 ",
                                    "expected": "订单。状态为已创建。",
                                    "note": "步骤说明。",
                                },
                                {
                                    "action": "调用 API v2.",
                                    "expected": "返回 HTTP 200.",
                                },
                            ],
                        )
                    ],
                }
            ],
            note="根说明。",
        )
        root = ET.fromstring(MODULE.build_content_xml(data))
        titles = all_titles(root)
        self.assertIn("[P0] 创建订单。", titles)
        self.assertIn("用户已登录", titles)
        self.assertIn("步骤 1: 提交订单。确认状态", titles)
        self.assertIn("预期 1: 订单。状态为已创建", titles)
        self.assertIn("步骤 2: 调用 API v2.", titles)
        self.assertIn("预期 2: 返回 HTTP 200.", titles)
        notes = [note.text for note in root.findall(".//x:notes/x:plain", NS)]
        self.assertEqual(notes, ["根说明。", "分组说明。", "用例说明。", "步骤说明。"])
        marker = root.find(".//x:marker-ref", NS)
        self.assertEqual(marker.attrib["marker-id"], "priority-1")

    def test_rejects_case_without_required_fields(self):
        with self.assertRaisesRegex(
            MODULE.ValidationError,
            r"groups\[0\]\.cases\[0\]\.preconditions",
        ):
            MODULE.build_content_xml(
                tree(
                    [
                        {
                            "title": "订单",
                            "cases": [
                                {
                                    "title": "[P1] 创建订单",
                                    "priority": "P1",
                                    "steps": [{"action": "提交", "expected": "成功"}],
                                }
                            ],
                        }
                    ]
                )
            )


if __name__ == "__main__":
    unittest.main()
