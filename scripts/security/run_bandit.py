"""Scan all tracked Python sources; preserve scanner errors and JSON evidence."""

import json
from pathlib import Path
import subprocess
import sys

from check_reports import check_bandit


def main():
    output = Path(sys.argv[1] if len(sys.argv) > 1 else "security-reports")
    output.mkdir(parents=True, exist_ok=True)
    files = subprocess.check_output(["git", "ls-files", "-z"], text=True).split("\0")
    sources = sorted(path for path in files if path.endswith(".py"))
    if not sources:
        raise ValueError("No tracked Python files to analyze")
    (output / "python-files.json").write_text(json.dumps(sources, indent=2), encoding="utf-8")
    version = subprocess.check_output([sys.executable, "-m", "bandit", "--version"], text=True)
    (output / "bandit-version.txt").write_text(version, encoding="utf-8")
    report_path = output / "bandit.json"
    # Ignore inline suppressions: exceptions need a separate reviewed policy change.
    result = subprocess.run(
        [sys.executable, "-m", "bandit", "--ignore-nosec", "-f", "json", "-o", str(report_path), *sources],
        check=False,
    )
    if result.returncode not in (0, 1):
        raise ValueError(f"Bandit execution failed: exit {result.returncode}")
    report = json.loads(report_path.read_text(encoding="utf-8"))
    blocked = check_bandit(report)
    # Exit 1 is normal only when the report actually contains findings.
    if result.returncode == 1 and not report["results"]:
        raise ValueError("Bandit exited unsuccessfully without findings")
    for finding in blocked:
        print(f"BLOCKED: {finding}")
    print(f"Python files: {len(sources)}; blocking findings: {len(blocked)}")
    return 1 if blocked else 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError) as exc:
        print(f"SECURITY SCAN FAILED: {exc}")
        raise SystemExit(2) from exc
