from __future__ import annotations

import copy
import json
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "eval"))

from grade_e6 import grade, read_jsonl  # noqa: E402


class E6GraderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = read_jsonl(ROOT / "eval" / "e6_cases.jsonl")
        cls.synthetic = read_jsonl(ROOT / "fixtures" / "e6_synthetic_results.jsonl")

    def test_synthetic_records_never_satisfy_e6(self):
        report = grade(self.cases, self.synthetic)
        self.assertEqual("HARNESS_ONLY", report["status"])
        self.assertFalse(report["behavioral_gate"]["complete_matched_live_records"])

    def test_grader_detects_seeded_false_duplicate(self):
        report = grade(self.cases, self.synthetic)
        adaptive = report["protocol_metrics"]["adaptive-axes-v1"]
        missed = {(item["case_id"], item["issue_id"]) for item in adaptive["critical_misses"]}
        self.assertIn(("F2-short", "CRIT-F2-SECOND-ORDER"), missed)
        self.assertIn(("F2-noisy", "CRIT-F2-SECOND-ORDER"), missed)
        self.assertEqual(2, len(adaptive["false_duplicate"]))

    def test_missing_pair_is_reported(self):
        incomplete = copy.deepcopy(self.synthetic[:-1])
        report = grade(self.cases, incomplete)
        self.assertTrue(any("missing result" in error for error in report["errors"]))

    def test_duplicate_issue_ids_are_rejected_outside_response_schema(self):
        duplicated = copy.deepcopy(self.synthetic)
        duplicated[0]["detected_issue_ids"] = ["I-F1-AXIS", "I-F1-AXIS"]
        report = grade(self.cases, duplicated)
        self.assertTrue(any("duplicate issue ID" in error for error in report["errors"]))

    def test_all_live_perfect_records_can_pass_harness_gate(self):
        live = copy.deepcopy(self.synthetic)
        for record in live:
            record["evidence_kind"] = "live-real-subagents"
            case = next(case for case in self.cases if case["case_id"] == record["case_id"])
            record["detected_issue_ids"] = list(case["critical_issue_ids"])
            record["false_no_material_issue_ids"] = []
            record["false_duplicate_issue_ids"] = []
            record["failure_trace_specificity"] = 1.0
            if not case["critical_issue_ids"] and not case["seeded_initial_issue_ids"]:
                record["unsupported_material_finding_refs"] = []
        report = grade(self.cases, live)
        self.assertEqual("PASS", report["status"])
        self.assertTrue(all(report["behavioral_gate"].values()))

    def test_live_clean_case_requires_and_counts_unsupported_findings(self):
        live = copy.deepcopy(self.synthetic)
        for record in live:
            record["evidence_kind"] = "live-real-subagents"
            case = next(case for case in self.cases if case["case_id"] == record["case_id"])
            if not case["critical_issue_ids"] and not case["seeded_initial_issue_ids"]:
                record["unsupported_material_finding_refs"] = ["FINDING-SPURIOUS"]
        report = grade(self.cases, live)
        adaptive = report["protocol_metrics"]["adaptive-axes-v1"]
        self.assertTrue(adaptive["unsupported_material_findings"])
        self.assertFalse(
            report["behavioral_gate"]["adaptive_zero_unsupported_material_findings"]
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
