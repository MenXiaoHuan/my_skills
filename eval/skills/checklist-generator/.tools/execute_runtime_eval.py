#!/usr/bin/env python3
import argparse
import json
import os
import subprocess
import time
import uuid
from pathlib import Path
from typing import Optional


ROOT = Path(__file__).resolve().parent.parent
WORKSPACE_ROOT = ROOT / ".runtime" / "runtime-eval-workspace"
SKILL_SNAPSHOTS_DIR = WORKSPACE_ROOT / "skill-snapshots"


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def find_project_root() -> Path:
    current = Path.cwd()
    for parent in [current, *current.parents]:
        if (parent / ".claude").is_dir():
            return parent
    return current


def ensure_runner(runner: str) -> None:
    result = subprocess.run(
        ["bash", "-lc", f"command -v {runner} >/dev/null 2>&1"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise SystemExit(
            f"runner '{runner}' not found in PATH; run check_runtime_runner.py first or install the CLI before executing runtime evals"
        )


def build_temp_command(
    project_root: Path,
    config_name: str,
    skill_dir: Path,
) -> tuple[str, Path]:
    name = f"{skill_dir.name}-{config_name}-{uuid.uuid4().hex[:8]}"
    commands_dir = project_root / ".claude" / "commands"
    commands_dir.mkdir(parents=True, exist_ok=True)
    command_path = commands_dir / f"{name}.md"
    skill_md = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    command_path.write_text(skill_md, encoding="utf-8")
    return name, command_path


def run_prompt(
    prompt: str,
    outputs_dir: Path,
    runner: str,
    model: Optional[str],
    skill_dir: Optional[Path],
    config_name: str,
    timeout_seconds: int,
) -> dict:
    project_root = find_project_root()
    env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}
    temp_command_path = None
    command_name = None

    try:
        final_prompt = prompt
        if skill_dir:
            command_name, temp_command_path = build_temp_command(project_root, config_name, skill_dir)
            final_prompt = f"Use the skill `{command_name}` if relevant.\n\n{prompt}"

        cmd = [runner, "-p", "--output-format", "text"]
        if model:
            cmd.extend(["--model", model])

        started = time.time()
        result = subprocess.run(
            cmd,
            input=final_prompt,
            capture_output=True,
            text=True,
            cwd=project_root,
            env=env,
            timeout=timeout_seconds,
        )
        ended = time.time()

        transcript_path = outputs_dir / "transcript.md"
        response_path = outputs_dir / "response.txt"
        stderr_path = outputs_dir / "stderr.txt"
        transcript_path.write_text(
            f"# Prompt\n\n{final_prompt}\n\n# Stdout\n\n{result.stdout}\n",
            encoding="utf-8",
        )
        response_path.write_text(result.stdout, encoding="utf-8")
        stderr_path.write_text(result.stderr, encoding="utf-8")

        timing = {
            "duration_ms": int((ended - started) * 1000),
            "total_duration_seconds": round(ended - started, 3),
            "executor_start": started,
            "executor_end": ended,
        }
        (outputs_dir.parent / "timing.json").write_text(json.dumps(timing, indent=2), encoding="utf-8")

        return {
            "returncode": result.returncode,
            "stdout_path": str(response_path),
            "stderr_path": str(stderr_path),
            "transcript_path": str(transcript_path),
            "used_temp_command": command_name,
        }
    finally:
        if temp_command_path and temp_command_path.exists():
            temp_command_path.unlink()


def resolve_skill_dir(config_name: str) -> Optional[Path]:
    if config_name == "with_skill":
        return SKILL_SNAPSHOTS_DIR / "current_skill"
    if config_name == "old_skill":
        return SKILL_SNAPSHOTS_DIR / "old_skill"
    return None


def execute_workspace(workspace_root: Path, runner: str, model: Optional[str], timeout_seconds: int) -> Path:
    iteration_dir = workspace_root / "iteration-1"
    ensure_runner(runner)
    manifest = load_json(workspace_root / "workspace_manifest.json")

    run_summary = {
        "workspace_type": manifest["workspace_type"],
        "configurations": manifest["configurations"],
        "runs": [],
    }

    for eval_dir in sorted(iteration_dir.glob("eval-*")):
        prompt = (eval_dir / "prompt.txt").read_text(encoding="utf-8")
        for config_name in manifest["configurations"]:
            outputs_dir = eval_dir / config_name / "outputs"
            outputs_dir.mkdir(parents=True, exist_ok=True)
            result = run_prompt(
                prompt=prompt,
                outputs_dir=outputs_dir,
                runner=runner,
                model=model,
                skill_dir=resolve_skill_dir(config_name),
                config_name=config_name,
                timeout_seconds=timeout_seconds,
            )
            run_summary["runs"].append(
                {
                    "eval_dir": eval_dir.name,
                    "configuration": config_name,
                    **result,
                }
            )

    summary_path = workspace_root / "iteration-1" / "runtime_execution_summary.json"
    summary_path.write_text(json.dumps(run_summary, ensure_ascii=False, indent=2), encoding="utf-8")
    return summary_path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace-root", default=str(WORKSPACE_ROOT))
    parser.add_argument("--runner", default="claude")
    parser.add_argument("--model", default=None)
    parser.add_argument("--timeout-seconds", type=int, default=300)
    args = parser.parse_args()

    summary_path = execute_workspace(
        workspace_root=Path(args.workspace_root),
        runner=args.runner,
        model=args.model,
        timeout_seconds=args.timeout_seconds,
    )
    print(summary_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
