"""Regression tests for failure and severity boundaries, without scanner services."""

import copy
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from check_reports import check_bandit, check_sarif


def sarif(score="7.0"):
    return {
        "version": "2.1.0",
        "runs": [{
            "tool": {"driver": {"name": "CodeQL", "rules": [{
                "id": "js/example", "properties": {"security-severity": score, "tags": ["security"]},
            }]}},
            "results": [{"ruleId": "js/example"}],
        }],
    }


class SecurityGateTests(unittest.TestCase):
    def test_codeql_security_boundaries(self):
        for score, expected in [(0, 0), (3.9, 0), (4, 0), (6.9, 0), (7, 1), (8.9, 1), (9, 1), (10, 1)]:
            with self.subTest(score=score):
                self.assertEqual(len(check_sarif(sarif(str(score)))), expected)

    def test_suppression_does_not_silently_bypass_gate(self):
        report = sarif()
        report["runs"][0]["results"][0]["suppressions"] = [{"status": "accepted", "kind": "external"}]
        self.assertEqual(len(check_sarif(report)), 1)

    def test_invalid_severity_fails_closed(self):
        for score in ["NaN", "inf", "-1", "11", "unknown"]:
            with self.subTest(score=score), self.assertRaises(ValueError):
                check_sarif(sarif(score))

    def test_missing_security_severity_fails(self):
        report = sarif()
        del report["runs"][0]["tool"]["driver"]["rules"][0]["properties"]["security-severity"]
        with self.assertRaises(ValueError):
            check_sarif(report)

    def test_empty_and_failed_analyses_fail(self):
        empty = {"version": "2.1.0", "runs": []}
        failed = sarif()
        failed["runs"][0]["invocations"] = [{"executionSuccessful": False}]
        notification = sarif()
        notification["runs"][0]["invocations"] = [{"toolExecutionNotifications": [{"level": "error"}]}]
        missing_results = sarif()
        del missing_results["runs"][0]["results"]
        for report in [empty, failed, notification, missing_results]:
            with self.subTest(report=report), self.assertRaises((ValueError, KeyError)):
                check_sarif(report)

    def test_clean_codeql_result_passes(self):
        report = sarif()
        report["runs"][0]["results"] = []
        self.assertEqual(check_sarif(report), [])

    def test_bandit_severity_and_errors(self):
        report = {"errors": [], "metrics": {"_totals": {"loc": 5}}, "results": []}
        self.assertEqual(check_bandit(report), [])
        for severity, expected in [("LOW", 0), ("MEDIUM", 0), ("HIGH", 1)]:
            report["results"] = [{"issue_severity": severity, "test_id": "B000", "filename": "app.py", "line_number": 1}]
            self.assertEqual(len(check_bandit(report)), expected)
        broken = copy.deepcopy(report)
        broken["errors"] = [{"reason": "syntax error"}]
        with self.assertRaises(ValueError):
            check_bandit(broken)
        broken = copy.deepcopy(report)
        broken["metrics"]["_totals"]["loc"] = 0
        with self.assertRaises(ValueError):
            check_bandit(broken)
        report["results"][0]["issue_severity"] = "UNDEFINED"
        with self.assertRaises(ValueError):
            check_bandit(report)


@unittest.skipUnless(importlib.util.find_spec("bandit"), "Install requirements-security.txt")
class BanditIntegrationTests(unittest.TestCase):
    def scan(self, code):
        wrapper = Path(__file__).with_name("run_bandit.py").resolve()
        with tempfile.TemporaryDirectory() as folder:
            subprocess.run(["git", "init", "-q", folder], check=True)
            Path(folder, "app.py").write_text(code, encoding="utf-8")
            subprocess.run(["git", "add", "app.py"], cwd=folder, check=True)
            return subprocess.run(
                [sys.executable, str(wrapper), "reports"], cwd=folder,
                capture_output=True, text=True, check=False,
            )

    def test_clean_source_passes(self):
        result = self.scan("message = 'hello'\n")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_high_finding_blocks_even_with_nosec(self):
        result = self.scan("import subprocess\ncommand = input()\nsubprocess.run(command, shell=True)  # nosec\n")
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)

    def test_parse_error_is_not_clean_scan(self):
        result = self.scan("def broken(\n")
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
