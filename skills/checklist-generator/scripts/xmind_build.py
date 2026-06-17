import json
import os
import re
import sys
import uuid
import zipfile
from datetime import datetime, timezone
from xml.etree.ElementTree import Element, SubElement, tostring


NS_CONTENT = "urn:xmind:xmap:xmlns:content:2.0"
NS_MANIFEST = "urn:xmind:xmap:xmlns:manifest:1.0"
NS_META = "urn:xmind:xmap:xmlns:meta:2.0"
NS_STYLE = "urn:xmind:xmap:xmlns:style:2.0"


def _u():
    return str(uuid.uuid4())


def _iso_now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _sanitize_title(title):
    text = str(title or "").strip()
    while True:
        updated = re.sub(r"^(?:(?:[+*\-]\s*)|(?:\d+[.)]\s+))+", "", text, flags=re.IGNORECASE)
        if updated == text:
            return text
        text = updated.strip()


def _topic(parent, title, note=None, marker=None):
    topic = SubElement(parent, f"{{{NS_CONTENT}}}topic", {"id": _u()})
    SubElement(topic, f"{{{NS_CONTENT}}}title").text = _sanitize_title(title)

    if note:
        notes = SubElement(topic, f"{{{NS_CONTENT}}}notes")
        SubElement(notes, f"{{{NS_CONTENT}}}plain").text = note

    if marker:
        markers = SubElement(topic, f"{{{NS_CONTENT}}}markers")
        SubElement(markers, f"{{{NS_CONTENT}}}marker-ref", {"marker-id": marker})

    return topic


def _attach_children(topic):
    children = SubElement(topic, f"{{{NS_CONTENT}}}children")
    return SubElement(children, f"{{{NS_CONTENT}}}topics", {"type": "attached"})


def _priority_marker(priority):
    mapping = {
        "P0": "priority-1",
        "P1": "priority-2",
        "P2": "priority-3",
        "P3": "priority-4",
        "P4": "priority-5",
    }
    if not priority:
        return None
    return mapping.get(str(priority).strip())


def _case_title(title, priority):
    clean_title = _sanitize_title(title)
    normalized_priority = str(priority or "").strip().upper()
    if not normalized_priority:
        return clean_title

    expected_prefix = f"[{normalized_priority}] "
    if re.match(r"^\[(?:P[0-9]+)\]\s*", clean_title, flags=re.IGNORECASE):
        return re.sub(r"^\[(?:P[0-9]+)\]\s*", expected_prefix, clean_title, count=1, flags=re.IGNORECASE)
    return f"{expected_prefix}{clean_title}"


def build_content_xml(data):
    xmap = Element(f"{{{NS_CONTENT}}}xmap-content", {"version": "2.0"})

    sheet = SubElement(xmap, f"{{{NS_CONTENT}}}sheet", {"id": _u()})
    SubElement(sheet, f"{{{NS_CONTENT}}}title").text = "Sheet 1"

    root_title = data.get("root_title") or "用例集"
    root = _topic(sheet, root_title, note=data.get("note"))
    root_attached = _attach_children(root)

    for group in data.get("groups") or []:
        group_topic = _topic(
            root_attached,
            group.get("title") or "分组",
            note=group.get("note"),
        )
        group_attached = _attach_children(group_topic)

        for case in group.get("cases") or []:
            case_topic = _topic(
                group_attached,
                _case_title(case.get("title") or "用例标题", case.get("priority")),
                note=case.get("note"),
                marker=_priority_marker(case.get("priority")),
            )
            case_attached = _attach_children(case_topic)

            preconditions = (case.get("preconditions") or "").strip()
            description = (case.get("description") or "").strip()
            if preconditions:
                preconditions_topic = _topic(case_attached, "前置条件")
                preconditions_attached = _attach_children(preconditions_topic)
                _topic(preconditions_attached, preconditions)
            elif description:
                description_topic = _topic(case_attached, "文本描述")
                description_attached = _attach_children(description_topic)
                _topic(description_attached, description)

            steps_topic = _topic(case_attached, "步骤")
            steps_attached = _attach_children(steps_topic)

            steps = case.get("steps") or []
            if not steps:
                _topic(steps_attached, "步骤 1")
                continue

            for index, step in enumerate(steps, start=1):
                action = (step.get("action") or "").strip()
                expected = (step.get("expected") or "").strip()
                step_title = f"步骤 {index}: {action}" if action else f"步骤 {index}"
                step_topic = _topic(steps_attached, step_title, note=step.get("note"))
                step_attached = _attach_children(step_topic)
                if expected:
                    _topic(step_attached, f"预期 {index}: {expected}")

    return tostring(xmap, encoding="utf-8", xml_declaration=True)


def build_manifest_xml():
    manifest = Element(f"{{{NS_MANIFEST}}}manifest")
    SubElement(
        manifest,
        f"{{{NS_MANIFEST}}}file-entry",
        {"full-path": "content.xml", "media-type": "text/xml"},
    )
    SubElement(
        manifest,
        f"{{{NS_MANIFEST}}}file-entry",
        {"full-path": "meta.xml", "media-type": "text/xml"},
    )
    SubElement(
        manifest,
        f"{{{NS_MANIFEST}}}file-entry",
        {"full-path": "styles.xml", "media-type": "text/xml"},
    )
    return tostring(manifest, encoding="utf-8", xml_declaration=True)


def build_meta_xml():
    meta = Element(f"{{{NS_META}}}meta", {"version": "2.0"})
    SubElement(meta, f"{{{NS_META}}}CreateTime").text = _iso_now()
    return tostring(meta, encoding="utf-8", xml_declaration=True)


def build_styles_xml():
    styles = Element(f"{{{NS_STYLE}}}xmap-styles", {"version": "2.0"})
    return tostring(styles, encoding="utf-8", xml_declaration=True)


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 scripts/xmind_build.py <input.json> <output.xmind>", file=sys.stderr)
        return 2

    input_path = sys.argv[1]
    output_path = os.path.abspath(sys.argv[2])

    with open(input_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    output_dir = os.path.dirname(output_path) or "."
    os.makedirs(output_dir, exist_ok=True)

    with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("content.xml", build_content_xml(data))
        archive.writestr("meta.xml", build_meta_xml())
        archive.writestr("styles.xml", build_styles_xml())
        archive.writestr("META-INF/manifest.xml", build_manifest_xml())

    if not os.path.exists(output_path) or os.path.getsize(output_path) <= 0:
        raise RuntimeError("Failed to write output .xmind")

    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
