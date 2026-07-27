import re


ALLOWED_PRIORITIES = {"P0", "P1", "P2", "P3"}
PRIORITY_PREFIX_RE = re.compile(r"^\[(P[0-9]+)\]\s+")


class ValidationError(ValueError):
    pass


def _fail(path, message):
    raise ValidationError(f"{path}: {message}")


def _require_non_empty_string(value, path):
    if not isinstance(value, str) or not value.strip():
        _fail(path, "must be a non-empty string")


def _validate_optional_note(container, path):
    if "note" in container and not isinstance(container["note"], str):
        _fail(f"{path}.note" if path else "note", "must be a string")


def _validate_case(case, path):
    if not isinstance(case, dict):
        _fail(path, "must be an object")

    for field in ("title", "priority", "preconditions", "steps"):
        if field not in case:
            _fail(f"{path}.{field}", "is required")

    _require_non_empty_string(case["title"], f"{path}.title")
    _require_non_empty_string(case["priority"], f"{path}.priority")
    priority = case["priority"]
    if priority not in ALLOWED_PRIORITIES:
        _fail(f"{path}.priority", "must be one of P0/P1/P2/P3")
    _validate_optional_note(case, path)

    prefix = PRIORITY_PREFIX_RE.match(case["title"].strip())
    if prefix is None:
        _fail(f"{path}.title", f"must start with [{priority}]")
    if prefix.group(1).upper() != priority:
        _fail(f"{path}.title", "priority prefix must match priority")

    _require_non_empty_string(case["preconditions"], f"{path}.preconditions")
    steps = case["steps"]
    if not isinstance(steps, list) or not steps:
        _fail(f"{path}.steps", "must be a non-empty list")
    for index, step in enumerate(steps):
        step_path = f"{path}.steps[{index}]"
        if not isinstance(step, dict):
            _fail(step_path, "must be an object")
        _validate_optional_note(step, step_path)
        for field in ("action", "expected"):
            if field not in step:
                _fail(f"{step_path}.{field}", "is required")
            _require_non_empty_string(step[field], f"{step_path}.{field}")


def _validate_group(group, path):
    if not isinstance(group, dict):
        _fail(path, "must be an object")
    if "title" not in group:
        _fail(f"{path}.title", "is required")
    _require_non_empty_string(group["title"], f"{path}.title")
    _validate_optional_note(group, path)

    for field in ("groups", "cases"):
        value = group.get(field, [])
        if not isinstance(value, list):
            _fail(f"{path}.{field}", "must be a list")

    for index, child in enumerate(group.get("groups", [])):
        _validate_group(child, f"{path}.groups[{index}]")
    for index, case in enumerate(group.get("cases", [])):
        _validate_case(case, f"{path}.cases[{index}]")


def validate_case_tree(data: dict) -> dict:
    if not isinstance(data, dict):
        _fail("$", "must be an object")
    _validate_optional_note(data, "")
    groups = data.get("groups")
    if not isinstance(groups, list) or not groups:
        _fail("groups", "must be a non-empty list")
    for index, group in enumerate(groups):
        _validate_group(group, f"groups[{index}]")
    return data
