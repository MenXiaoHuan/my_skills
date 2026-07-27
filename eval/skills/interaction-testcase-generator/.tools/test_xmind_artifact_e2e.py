import importlib.util
import json
import tempfile
import unittest
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


TOOLS_DIR = Path(__file__).resolve().parent
ROOT = TOOLS_DIR.parent
VALIDATOR_PATH = TOOLS_DIR / "validate_benchmark.py"
SPEC = importlib.util.spec_from_file_location("validate_benchmark", VALIDATOR_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)

NS = {"x": "urn:xmind:xmap:xmlns:content:2.0"}
REQUIRED_MEMBERS = {
    "content.xml",
    "meta.xml",
    "styles.xml",
    "META-INF/manifest.xml",
}


def topic_title(topic):
    title = topic.find("x:title", NS)
    return title.text if title is not None else None


def child_topics(topic):
    return topic.findall("./x:children/x:topics/x:topic", NS)


class XMindArtifactE2ETests(unittest.TestCase):
    def test_structure_quality_suite_rejects_unknown_fields(self):
        with self.assertRaisesRegex(
            SystemExit,
            "structure_unknown has unknown fields: unexpected",
        ):
            MODULE.validate_structure_quality_config(
                {
                    "id": "structure_unknown",
                    "input_json": "cases/case_001_app_cart_offline.json",
                    "ir_json": "ir/interaction-cart.json",
                    "selected_case_ids": ["C-CART-ADD"],
                    "unexpected": True,
                }
            )

    def test_artifact_suite_rejects_unknown_fields(self):
        with self.assertRaisesRegex(
            SystemExit,
            "artifact_unknown has unknown fields: unexpected",
        ):
            MODULE.validate_artifact_suite(
                {
                    "artifact_suite": [
                        {
                            "id": "artifact_unknown",
                            "input_json": "cases/case_001_app_cart_offline.json",
                            "unexpected": True,
                        }
                    ]
                }
            )

    def test_module_fixture_uses_its_own_ir_and_selected_case_binding(self):
        baseline = json.loads(
            (ROOT / "baseline.json").read_text(encoding="utf-8")
        )
        module_case = next(
            case
            for case in baseline["structure_quality_suite"]
            if case["id"] == "structure_modules"
        )
        self.assertEqual(module_case["ir_json"], "ir/module-tree.json")
        tree = json.loads(
            (ROOT / module_case["input_json"]).read_text(encoding="utf-8")
        )
        tree_ids = {
            case["case_id"]
            for case in MODULE.QUALITY_MODULE.iter_cases(tree["groups"])
        }
        self.assertEqual(tree_ids, set(module_case["selected_case_ids"]))

    def test_full_artifact_comparison_rejects_wrong_marker(self):
        fixture = json.loads(
            (ROOT / "cases" / "case_001_app_cart_offline.json").read_text(
                encoding="utf-8"
            )
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            input_path = temp_path / "input.json"
            output_path = temp_path / "artifact.xmind"
            input_path.write_text(
                json.dumps(fixture, ensure_ascii=False),
                encoding="utf-8",
            )
            MODULE.run_artifact_regression(input_path, output_path)

            with zipfile.ZipFile(output_path) as archive:
                members = {
                    name: archive.read(name)
                    for name in archive.namelist()
                }
            root = ET.fromstring(members["content.xml"])
            marker = root.find(".//x:marker-ref", NS)
            marker.attrib["marker-id"] = "priority-4"
            members["content.xml"] = ET.tostring(
                root,
                encoding="utf-8",
                xml_declaration=True,
            )
            with zipfile.ZipFile(
                output_path,
                "w",
                compression=zipfile.ZIP_DEFLATED,
            ) as archive:
                for name, content in members.items():
                    archive.writestr(name, content)

            with self.assertRaisesRegex(SystemExit, "artifact mismatch"):
                MODULE.validate_artifact_matches_input(input_path, output_path)

    def test_builds_and_validates_real_xmind_from_standard_fixture(self):
        fixture = json.loads(
            (ROOT / "cases" / "case_001_app_cart_offline.json").read_text(
                encoding="utf-8"
            )
        )
        fixture["note"] = "根节点说明"
        fixture["groups"].extend(
            [
                {
                    "title": "订单 - 列表",
                    "cases": [
                        {
                            "title": "[P1] 订单列表 - 标点与说明。",
                            "priority": "P1",
                            "note": "用例说明。",
                            "preconditions": "用户已登录。。",
                            "steps": [
                                {
                                    "action": "打开订单列表。。",
                                    "expected": "展示订单。状态为已创建。",
                                    "note": "步骤说明。",
                                }
                            ],
                        }
                    ],
                },
                {
                    "title": "订单 - 详情",
                    "cases": [
                        {
                            "title": "[P2] 订单详情 - 展示订单",
                            "priority": "P2",
                            "preconditions": "订单已创建",
                            "steps": [
                                {
                                    "action": "打开订单详情",
                                    "expected": "展示目标订单",
                                }
                            ],
                        }
                    ],
                },
            ]
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            input_path = temp_path / "input.json"
            output_path = temp_path / "artifact.xmind"
            input_path.write_text(
                json.dumps(fixture, ensure_ascii=False),
                encoding="utf-8",
            )
            MODULE.run_artifact_regression(input_path, output_path)

            self.assertTrue(output_path.exists())
            with zipfile.ZipFile(output_path) as archive:
                self.assertTrue(REQUIRED_MEMBERS <= set(archive.namelist()))
                root = ET.fromstring(archive.read("content.xml"))

        root_topic = root.find("./x:sheet/x:topic", NS)
        self.assertEqual(topic_title(root_topic), "用例集")
        top_groups = {topic_title(topic): topic for topic in child_topics(root_topic)}
        self.assertIn("在线加购", top_groups)
        self.assertIn("订单", top_groups)

        online_case = child_topics(top_groups["在线加购"])[0]
        self.assertTrue(topic_title(online_case).startswith("[P0]"))
        marker = online_case.find("./x:markers/x:marker-ref", NS)
        self.assertEqual(marker.attrib["marker-id"], "priority-1")
        online_children = {topic_title(topic): topic for topic in child_topics(online_case)}
        self.assertIn("前置条件", online_children)
        self.assertIn("步骤", online_children)
        first_step = child_topics(online_children["步骤"])[0]
        self.assertTrue(topic_title(first_step).startswith("步骤 1:"))
        self.assertTrue(topic_title(child_topics(first_step)[0]).startswith("预期 1:"))

        order_children = {topic_title(topic): topic for topic in child_topics(top_groups["订单"])}
        self.assertEqual(set(order_children), {"列表", "详情"})
        punctuation_case = child_topics(order_children["列表"])[0]
        titles = [title.text for title in punctuation_case.findall(".//x:title", NS)]
        self.assertIn("用户已登录", titles)
        self.assertIn("步骤 1: 打开订单列表", titles)
        self.assertIn("预期 1: 展示订单。状态为已创建", titles)
        notes = [note.text for note in punctuation_case.findall(".//x:notes/x:plain", NS)]
        self.assertEqual(notes, ["用例说明。", "步骤说明。"])


if __name__ == "__main__":
    unittest.main()
