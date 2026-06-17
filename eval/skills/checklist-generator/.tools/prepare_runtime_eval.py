#!/usr/bin/env python3
import argparse
import json
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
REPO_ROOT = ROOT.parents[2]
SKILL_DIR = REPO_ROOT / "skills" / "checklist-generator"
BASELINE_PATH = ROOT / "baseline.json"
OLD_SKILL_COMMIT = "a8dbd4a"


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def run_git_show(commit: str, path: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "show", f"{commit}:{path}"],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def sanitize_name(text: str) -> str:
    return "".join(ch.lower() if ch.isalnum() else "-" for ch in text).strip("-")


def comparative_expectations(case: dict) -> list[dict]:
    expectations = []
    if "expected_current_trigger" in case:
        expectations.append(
            {
                "text": "Current skill should respect the tightened trigger boundary.",
                "target_configuration": "with_skill",
                "expected": case["expected_current_trigger"],
            }
        )
        expectations.append(
            {
                "text": "Old skill should exhibit the broader historical trigger behavior.",
                "target_configuration": "old_skill",
                "expected": case["expected_old_trigger"],
            }
        )
        expectations.append(
            {
                "text": "No-skill baseline should be recorded for later comparison.",
                "target_configuration": "without_skill",
                "expected": "capture-output",
            }
        )
    else:
        expectations.append(
            {
                "text": "Current skill should deliver the file without exposing an absolute path as the main result.",
                "target_configuration": "with_skill",
                "expected": case["expected_current_behavior"],
            }
        )
        expectations.append(
            {
                "text": "Old skill should preserve the legacy path-first behavior.",
                "target_configuration": "old_skill",
                "expected": case["expected_old_behavior"],
            }
        )
        expectations.append(
            {
                "text": "No-skill baseline should be recorded for later comparison.",
                "target_configuration": "without_skill",
                "expected": "capture-output",
            }
        )
    return expectations


def ensure_old_skill_snapshot(snapshot_dir: Path) -> None:
    if snapshot_dir.exists():
        shutil.rmtree(snapshot_dir)
    shutil.copytree(SKILL_DIR, snapshot_dir)
    old_skill_md = run_git_show(OLD_SKILL_COMMIT, "skills/checklist-generator/SKILL.md")
    (snapshot_dir / "SKILL.md").write_text(old_skill_md, encoding="utf-8")


def prepare_eval_dirs(iteration_dir: Path, suite: list[dict]) -> None:
    for index, case in enumerate(suite, start=1):
        eval_name = sanitize_name(case["id"])
        eval_dir = iteration_dir / f"eval-{index:03d}-{eval_name}"
        for config in ["with_skill", "without_skill", "old_skill"]:
            (eval_dir / config / "outputs").mkdir(parents=True, exist_ok=True)

        metadata = {
            "eval_id": index,
            "eval_name": case["id"],
            "prompt": case["prompt"],
            "assertions": comparative_expectations(case),
            "notes": {
                "dimension": case["dimension"],
                "reason": case["reason"],
            },
        }
        write_json(eval_dir / "eval_metadata.json", metadata)
        (eval_dir / "prompt.txt").write_text(case["prompt"], encoding="utf-8")


def prepare_workspace(force: bool) -> Path:
    workspace_dir = ROOT / ".runtime" / "runtime-eval-workspace"
    iteration_dir = workspace_dir / "iteration-1"
    if workspace_dir.exists() and force:
        shutil.rmtree(workspace_dir)
    workspace_dir.mkdir(parents=True, exist_ok=True)

    benchmark = load_json(BASELINE_PATH)
    prepare_eval_dirs(iteration_dir, benchmark["comparative_suite"])

    snapshots_dir = workspace_dir / "skill-snapshots"
    ensure_old_skill_snapshot(snapshots_dir / "old_skill")
    shutil.copytree(SKILL_DIR, snapshots_dir / "current_skill", dirs_exist_ok=True)

    manifest = {
        "skill_name": "checklist-generator",
        "workspace_type": "runtime-comparison",
        "iteration": 1,
        "old_skill_commit": OLD_SKILL_COMMIT,
        "eval_count": len(benchmark["comparative_suite"]),
        "configurations": ["with_skill", "without_skill", "old_skill"],
        "instructions": [
            "Run the same prompt against with_skill, without_skill, and old_skill.",
            "Save each configuration output under its outputs directory.",
            "Record timing.json and grading.json after execution.",
        ],
    }
    write_json(workspace_dir / "workspace_manifest.json", manifest)
    return workspace_dir


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    workspace_dir = prepare_workspace(force=args.force)
    print(workspace_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
