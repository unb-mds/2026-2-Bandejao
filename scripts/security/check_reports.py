"""Fail-closed gates for Bandit JSON and CodeQL SARIF (RNF05)."""

import argparse
import json
import math
from pathlib import Path


def check_bandit(report):
    if report["errors"]:
        raise ValueError("Bandit could not analyze every input file")
    if report["metrics"]["_totals"]["loc"] <= 0:
        raise ValueError("Bandit analyzed no lines of code")
    findings = report["results"]
    if not isinstance(findings, list):
        raise ValueError("Invalid Bandit results")
    blocked = []
    for finding in findings:
        severity = finding["issue_severity"]
        if severity not in {"LOW", "MEDIUM", "HIGH"}:
            raise ValueError(f"Unknown Bandit severity: {severity}")
        if severity == "HIGH":
            blocked.append(f"{finding['test_id']}: {finding['filename']}:{finding['line_number']}")
    return blocked


def check_sarif(report):
    if report["version"] != "2.1.0" or not report["runs"]:
        raise ValueError("Missing SARIF runs or unsupported version")
    blocked = []
    for run in report["runs"]:
        driver = run["tool"]["driver"]
        if driver["name"] != "CodeQL":
            raise ValueError("Expected CodeQL tool in SARIF")
        for invocation in run.get("invocations", []):
            if invocation.get("executionSuccessful") is False:
                raise ValueError("CodeQL invocation failed")
            for notification in invocation.get("toolExecutionNotifications", []):
                if notification.get("level") == "error":
                    raise ValueError("CodeQL reported an execution error")
        if not isinstance(run["results"], list):
            raise ValueError("Invalid SARIF results")
        declared_rules = driver.get("rules", [])
        if not isinstance(declared_rules, list):
            raise ValueError("Invalid CodeQL rules")
        if run["results"] and not declared_rules:
            raise ValueError("Expected CodeQL rules for reported results")
        rules = {rule["id"]: rule for rule in declared_rules}
        for finding in run["results"]:
            rule = rules[finding["ruleId"]]
            props = rule.get("properties", {})
            raw_score = props.get("security-severity")
            if raw_score is None:
                if "security" in props.get("tags", []):
                    raise ValueError(f"Missing security severity: {rule['id']}")
                continue  # Non-security code-quality rule; retained in the report.
            score = float(raw_score)
            if not math.isfinite(score) or not 0 <= score <= 10:
                raise ValueError(f"Invalid security severity: {raw_score}")
            if score >= 7.0:
                blocked.append(f"{rule['id']}: security-severity={score}")
    return blocked


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("format", choices=["bandit", "sarif"])
    parser.add_argument("paths", nargs="+", type=Path)
    args = parser.parse_args()
    checker = check_bandit if args.format == "bandit" else check_sarif
    try:
        blocked = []
        for path in args.paths:
            blocked.extend(checker(json.loads(path.read_text(encoding="utf-8"))))
        for finding in blocked:
            print(f"BLOCKED: {finding}")
        print(f"Blocking findings: {len(blocked)}")
        return 1 if blocked else 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"INVALID SECURITY REPORT: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
