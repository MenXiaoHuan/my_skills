import importlib.util
import unittest
from pathlib import Path
from xml.etree import ElementTree as ET


SCRIPT_PATH = Path(__file__).resolve().parent / "xmind_build.py"
SPEC = importlib.util.spec_from_file_location("xmind_build", SCRIPT_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)

NS = {"x": MODULE.NS_CONTENT}


def _titles(node):
    return [child.find("x:title", NS).text for child in node.findall("./x:children/x:topics/x:topic", NS)]


def _count_cases(groups):
    total = 0
    for group in groups or []:
        total += len(group.get("cases") or [])
        total += _count_cases(group.get("groups") or [])
    return total


def _all_titles(node):
    return [title.text for title in node.findall(".//x:title", NS)]


def _all_notes(node):
    return [note.text for note in node.findall(".//x:notes/x:plain", NS)]


class XMindBuildTests(unittest.TestCase):
    def test_auto_merges_groups_with_shared_business_parent(self):
        data = {
            "root_title": "用例集",
            "groups": [
                {
                    "title": "Creative Insights - Top10 Videos",
                    "cases": [{"title": "校验 A", "priority": "P1", "steps": [{"action": "打开", "expected": "成功"}]}],
                },
                {
                    "title": "Creative Insights - Content Execution Label",
                    "cases": [{"title": "校验 B", "priority": "P1", "steps": [{"action": "打开", "expected": "成功"}]}],
                },
            ],
        }

        root = ET.fromstring(MODULE.build_content_xml(data))
        root_topic = root.find("./x:sheet/x:topic", NS)
        self.assertIsNotNone(root_topic)
        top_level_titles = _titles(root_topic)
        self.assertEqual(top_level_titles, ["Creative Insights"])

        shared_group = root_topic.find("./x:children/x:topics/x:topic", NS)
        self.assertIsNotNone(shared_group)
        self.assertEqual(_titles(shared_group), ["Top10 Videos", "Content Execution Label"])

    def test_does_not_merge_generic_parent_titles(self):
        data = {
            "root_title": "用例集",
            "groups": [
                {
                    "title": "页面 - Top10 Videos",
                    "cases": [{"title": "校验 A", "priority": "P1", "steps": [{"action": "打开", "expected": "成功"}]}],
                },
                {
                    "title": "页面 - Content Execution Label",
                    "cases": [{"title": "校验 B", "priority": "P1", "steps": [{"action": "打开", "expected": "成功"}]}],
                },
            ],
        }

        root = ET.fromstring(MODULE.build_content_xml(data))
        root_topic = root.find("./x:sheet/x:topic", NS)
        self.assertIsNotNone(root_topic)
        self.assertEqual(
            _titles(root_topic),
            ["页面 - Top10 Videos", "页面 - Content Execution Label"],
        )

    def test_preserves_explicit_nested_groups(self):
        data = {
            "root_title": "用例集",
            "groups": [
                {
                    "title": "Creative Insights",
                    "groups": [
                        {
                            "title": "Top10 Videos",
                            "cases": [{"title": "校验 A", "priority": "P1", "steps": [{"action": "打开", "expected": "成功"}]}],
                        },
                        {
                            "title": "Content Execution Label",
                            "cases": [{"title": "校验 B", "priority": "P1", "steps": [{"action": "打开", "expected": "成功"}]}],
                        },
                    ],
                }
            ],
        }

        root = ET.fromstring(MODULE.build_content_xml(data))
        root_topic = root.find("./x:sheet/x:topic", NS)
        self.assertIsNotNone(root_topic)
        top_level_titles = _titles(root_topic)
        self.assertEqual(top_level_titles, ["Creative Insights"])

        shared_group = root_topic.find("./x:children/x:topics/x:topic", NS)
        self.assertIsNotNone(shared_group)
        self.assertEqual(_titles(shared_group), ["Top10 Videos", "Content Execution Label"])

    def test_auto_merge_preserves_total_case_count(self):
        groups = [
            {
                "title": "Creative Insights - Top10 Videos",
                "cases": [{"title": "校验 A", "priority": "P1", "steps": [{"action": "打开", "expected": "成功"}]}],
            },
            {
                "title": "Creative Insights - Content Execution Label",
                "cases": [
                    {"title": "校验 B1", "priority": "P1", "steps": [{"action": "打开", "expected": "成功"}]},
                    {"title": "校验 B2", "priority": "P2", "steps": [{"action": "切换", "expected": "成功"}]},
                ],
            },
            {
                "title": "Search",
                "cases": [{"title": "校验 C", "priority": "P1", "steps": [{"action": "搜索", "expected": "成功"}]}],
            },
        ]

        original_case_count = _count_cases(groups)
        normalized = MODULE._normalize_groups(groups)
        normalized_case_count = _count_cases(normalized)

        self.assertEqual(original_case_count, 4)
        self.assertEqual(normalized_case_count, original_case_count)

    def test_auto_merges_parent_module_and_child_view_titles(self):
        data = {
            "root_title": "用例集",
            "groups": [
                {
                    "title": "Top10 Videos - 视频列表",
                    "cases": [{"title": "列表校验", "priority": "P1", "steps": [{"action": "打开列表", "expected": "成功"}]}],
                },
                {
                    "title": "Top10 Videos - 视频详情",
                    "cases": [{"title": "详情校验", "priority": "P1", "steps": [{"action": "进入详情", "expected": "成功"}]}],
                },
            ],
        }

        root = ET.fromstring(MODULE.build_content_xml(data))
        root_topic = root.find("./x:sheet/x:topic", NS)
        self.assertIsNotNone(root_topic)
        self.assertEqual(_titles(root_topic), ["Top10 Videos"])

        parent_group = root_topic.find("./x:children/x:topics/x:topic", NS)
        self.assertIsNotNone(parent_group)
        self.assertEqual(_titles(parent_group), ["视频列表", "视频详情"])

    def test_case_title_priority_prefix_matches_priority_field(self):
        data = {
            "root_title": "用例集",
            "groups": [
                {
                    "title": "Priority",
                    "cases": [
                        {
                            "title": "[P2] 优先级前缀需要被纠正",
                            "priority": "P0",
                            "steps": [{"action": "执行", "expected": "成功"}],
                        }
                    ],
                }
            ],
        }

        root = ET.fromstring(MODULE.build_content_xml(data))
        self.assertIn("[P0] 优先级前缀需要被纠正", _all_titles(root))
        self.assertNotIn("[P2] 优先级前缀需要被纠正", _all_titles(root))

        marker_refs = root.findall(".//x:marker-ref", NS)
        self.assertEqual(len(marker_refs), 1)
        self.assertEqual(marker_refs[0].attrib["marker-id"], "priority-1")

    def test_notes_are_rendered_for_root_group_case_and_step(self):
        data = {
            "root_title": "用例集",
            "note": "根节点说明",
            "groups": [
                {
                    "title": "Notes",
                    "note": "分组说明",
                    "cases": [
                        {
                            "title": "说明校验",
                            "priority": "P1",
                            "note": "用例说明",
                            "steps": [
                                {
                                    "action": "执行步骤",
                                    "expected": "看到预期",
                                    "note": "步骤说明",
                                }
                            ],
                        }
                    ],
                }
            ],
        }

        root = ET.fromstring(MODULE.build_content_xml(data))
        notes = _all_notes(root)
        self.assertIn("根节点说明", notes)
        self.assertIn("分组说明", notes)
        self.assertIn("用例说明", notes)
        self.assertIn("步骤说明", notes)

    def test_strips_trailing_chinese_periods_only_from_case_execution_fields(self):
        data = {
            "root_title": "用例集",
            "groups": [
                {
                    "title": "标点清理",
                    "cases": [
                        {
                            "title": "标题保留。",
                            "priority": "P1",
                            "note": "备注保留。",
                            "preconditions": "用户已登录。。 ",
                            "steps": [
                                {
                                    "action": "打开订单。确认状态。。 ",
                                    "expected": "展示订单。状态为待支付。",
                                    "note": "步骤备注保留。",
                                },
                                {
                                    "action": "调用 API v2.",
                                    "expected": "返回 HTTP 200.",
                                },
                            ],
                        }
                    ],
                }
            ],
        }

        root = ET.fromstring(MODULE.build_content_xml(data))
        titles = _all_titles(root)
        self.assertIn("用户已登录", titles)
        self.assertIn("步骤 1: 打开订单。确认状态", titles)
        self.assertIn("预期 1: 展示订单。状态为待支付", titles)
        self.assertIn("步骤 2: 调用 API v2.", titles)
        self.assertIn("预期 2: 返回 HTTP 200.", titles)
        self.assertIn("[P1] 标题保留。", titles)
        self.assertIn("备注保留。", _all_notes(root))
        self.assertIn("步骤备注保留。", _all_notes(root))


if __name__ == "__main__":
    unittest.main()
