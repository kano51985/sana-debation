from __future__ import annotations

import json
from pathlib import Path
import subprocess
import unittest
from unittest import mock

from tools.e14_n1_i1_evidence import (
    BUNDLE_FILENAMES,
    EXPECTED_G1_FREEZE_SHA256,
    EXPECTED_SCANNER_SHA256,
    EXPECTED_V1_REVIEW_SHA256,
    build_all_evidence,
    canonical_bytes,
    evaluate_fixture_case,
    load_json_strict,
    validate_evidence_record,
)


ROOT = Path(__file__).resolve().parents[1]
SCANNER = ROOT / "src" / "e14_admission.py"
G1_V1 = ROOT / "evidence" / "e14-a2-g1-production-freeze-v1.json"
V1_REVIEW = ROOT / "evidence" / "n1" / "scanner-dataflow-review-v1.json"
DIRECT_CASES = ROOT / "fixtures" / "e14_n1_scanner_dataflow_cases_v1.json"
MODEL_CASES = ROOT / "fixtures" / "e14_n1_i1_remediation_cases_v1.json"
EVIDENCE_DIR = ROOT / "evidence" / "n1" / "remediation"
EVIDENCE_SCHEMA = ROOT / "schemas" / "e14-n1-i1-remediation-evidence-v1.schema.json"


class I1RemediationEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.records = build_all_evidence()

    def test_v1_scanner_g1_and_failed_review_remain_byte_exact(self) -> None:
        import hashlib

        self.assertEqual(hashlib.sha256(SCANNER.read_bytes()).hexdigest().upper(), EXPECTED_SCANNER_SHA256)
        self.assertEqual(hashlib.sha256(G1_V1.read_bytes()).hexdigest().upper(), EXPECTED_G1_FREEZE_SHA256)
        self.assertEqual(hashlib.sha256(V1_REVIEW.read_bytes()).hexdigest().upper(), EXPECTED_V1_REVIEW_SHA256)

    def test_direct_unchanged_cases_are_all_diagnosed_without_identity_shortcut(self) -> None:
        coverage = self.records["OBLIGATION_COVERAGE"]["results"]
        rows = coverage["direct_diagnostic_cases"]
        self.assertEqual(len(rows), 14)
        self.assertEqual(coverage["direct_diagnostic_summary"], {"blocking": 14, "unexpected": 0})
        self.assertTrue(all(row["decision"] == "BLOCKING" for row in rows))
        self.assertTrue(all(row["archive_identity_checked"] is False for row in rows))
        self.assertEqual(
            {row["case_id"] for row in rows},
            {row["case_id"] for row in load_json_strict(DIRECT_CASES)["cases"]},
        )

    def test_all_nine_records_have_closed_common_contract_and_reproduce(self) -> None:
        self.assertEqual(set(self.records), set(BUNDLE_FILENAMES))
        for kind, record in self.records.items():
            with self.subTest(kind=kind):
                validate_evidence_record(record)
                persisted = load_json_strict(EVIDENCE_DIR / BUNDLE_FILENAMES[kind])
                self.assertEqual(persisted, record)
                material = dict(record)
                root = material.pop("bundle_root")
                self.assertEqual(
                    root,
                    "sha256-e14-n1-i1-evidence-v1:"
                    + __import__("hashlib").sha256(canonical_bytes(material)).hexdigest().upper(),
                )

    def test_json_schema_freezes_the_same_closed_common_contract(self) -> None:
        schema = load_json_strict(EVIDENCE_SCHEMA)
        self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
        self.assertFalse(schema["unevaluatedProperties"])
        self.assertEqual(set(schema["required"]), set(self.records["ROLLBACK"]))
        self.assertEqual(
            set(schema["properties"]["bundle_kind"]["enum"]), set(BUNDLE_FILENAMES)
        )
        self.assertEqual(
            set(schema["properties"]["status"]["enum"]),
            {"PASS", "FAIL", "INCONCLUSIVE", "NOT_RUN"},
        )

    def test_statuses_preserve_unresolved_and_not_run_boundaries(self) -> None:
        expected = {
            "OBLIGATION_COVERAGE": "INCONCLUSIVE",
            "HERMETIC_DIAGNOSTIC": "NOT_RUN",
            "FREEZE_REPRODUCTION": "PASS",
            "LIFECYCLE_AUTHORITY": "INCONCLUSIVE",
            "ROUTING_COMPATIBILITY": "PASS",
            "CONSUMER_CONFORMANCE": "PASS",
            "I2_AUTHORIZATION_CONTROL": "PASS",
            "ROLLBACK": "PASS",
            "DEPENDENCY_APPROVAL": "NOT_RUN",
        }
        self.assertEqual({kind: row["status"] for kind, row in self.records.items()}, expected)
        self.assertTrue(all(row["authority_effect"] == "NONE" for row in self.records.values()))
        self.assertTrue(all(row["next_stage_authorized"] is False for row in self.records.values()))

    def test_supervisor_abnormal_paths_never_emit_success_envelope(self) -> None:
        cases = [case for case in load_json_strict(MODEL_CASES)["cases"] if case["domain"] == "SUPERVISOR"]
        results = {case["scenario"]: evaluate_fixture_case(case) for case in cases}
        self.assertEqual(results["clean_success"], "SUCCESS_ENVELOPE_EMITTED")
        self.assertTrue(
            all(result == "ABORTED_NO_ENVELOPE" for name, result in results.items() if name != "clean_success")
        )

    def test_every_synthetic_model_case_matches_the_frozen_expectation(self) -> None:
        corpus = load_json_strict(MODEL_CASES)
        self.assertEqual(corpus["authority_effect"], "NONE")
        self.assertEqual(len({case["case_id"] for case in corpus["cases"]}), len(corpus["cases"]))
        for case in corpus["cases"]:
            with self.subTest(case_id=case["case_id"]):
                self.assertEqual(evaluate_fixture_case(case), case["expected"])

    def test_freeze_root_is_reproduced_by_independent_encoders(self) -> None:
        result = self.records["FREEZE_REPRODUCTION"]["results"]
        self.assertTrue(result["roots_equal"])
        self.assertEqual(result["primary_root"], result["independent_root"])
        self.assertTrue(result["synthetic_only"])

    def test_consumer_policy_maps_every_prescan_claim_only_to_record_evidence(self) -> None:
        result = self.records["CONSUMER_CONFORMANCE"]["results"]
        self.assertEqual(set(result["claim_to_action"].values()), {"RECORD_EVIDENCE"})
        self.assertEqual(result["production_consumers"], [])
        self.assertTrue(result["repository_scope_only"])

    def test_build_phase_is_read_only_and_never_starts_processes(self) -> None:
        with (
            mock.patch.object(subprocess, "Popen", side_effect=AssertionError("process started")),
            mock.patch.object(Path, "write_text", side_effect=AssertionError("write attempted")),
            mock.patch.object(Path, "write_bytes", side_effect=AssertionError("write attempted")),
            mock.patch.object(Path, "unlink", side_effect=AssertionError("delete attempted")),
        ):
            rebuilt = build_all_evidence()
        self.assertEqual(rebuilt, self.records)


if __name__ == "__main__":
    unittest.main()
