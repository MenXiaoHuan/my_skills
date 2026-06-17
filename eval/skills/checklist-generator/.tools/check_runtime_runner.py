#!/usr/bin/env python3
import shutil
from pathlib import Path


def main() -> int:
    claude = shutil.which("claude")
    trae = Path("/usr/local/bin/trae")

    print("runtime runner check")
    print(f"claude_in_path={bool(claude)}")
    if claude:
        print(f"claude_path={claude}")
    else:
        print("claude_path=<missing>")

    print(f"trae_symlink_exists={trae.exists() or trae.is_symlink()}")
    if trae.is_symlink():
        target = trae.resolve(strict=False)
        print(f"trae_symlink_target={target}")
        print(f"trae_target_exists={target.exists()}")
    else:
        print("trae_symlink_target=<not-a-symlink>")
        print("trae_target_exists=False")

    if claude:
        print("runner_status=ready")
        return 0

    if trae.is_symlink() and trae.resolve(strict=False).exists():
        print("runner_status=trae-present-but-not-in-path")
        return 0

    print("runner_status=missing")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
