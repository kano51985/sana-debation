from __future__ import annotations

import json
import marshal
import os
from pathlib import Path
import pickle
import subprocess
import unittest
from unittest import mock

from tools.e14_n1_dataflow_audit import EXPECTED_SCANNER_SHA256, build_evidence


ROOT = Path(__file__).resolve().parents[1]
SCANNER = ROOT / "src" / "e14_admission.py"
CASES = ROOT / "fixtures" / "e14_n1_scanner_dataflow_cases_v1.json"
EVIDENCE = ROOT / "evidence" / "n1"


class N1ScannerDataflowEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.bundle = build_evidence(SCANNER, CASES)

    def test_exact_production_scanner_hash_is_frozen(self) -> None:
        self.assertEqual(
            self.bundle["review"]["scanner"]["sha256"], EXPECTED_SCANNER_SHA256
        )
        self.assertTrue(self.bundle["review"]["scanner"]["matches_g1_freeze"])

    def test_fixture_corpus_covers_all_seven_attack_families_in_both_languages(self) -> None:
        corpus = json.loads(CASES.read_text(encoding="utf-8"))
        self.assertEqual(corpus["authority_effect"], "NONE")
        self.assertEqual(len(corpus["cases"]), 14)
        self.assertEqual(len({case["case_id"] for case in corpus["cases"]}), 14)
        expected = {
            (language, category)
            for language in ("NODE", "PYTHON")
            for category in (
                "ALIAS",
                "REFLECTION",
                "DYNAMIC_CODE",
                "DESERIALIZER_CALLBACK",
                "NATIVE_LOAD",
                "SUBPROCESS",
                "OUTPUT_REENTRY",
            )
        }
        self.assertEqual(
            {(case["language"], case["category"]) for case in corpus["cases"]}, expected
        )
        self.assertTrue(all(case["required_decision"] == "REJECT" for case in corpus["cases"]))

    def test_scanner_source_has_no_execution_network_or_write_sink(self) -> None:
        source = self.bundle["review"]["source_audit"]
        self.assertEqual(source["status"], "PASS")
        self.assertEqual(source["dangerous_imports"], [])
        self.assertEqual(source["dangerous_calls"], [])
        self.assertEqual(source["filesystem_mutation_calls"], [])
        self.assertEqual(source["vendor_selected_callback_sites"], [])

    def test_callback_manifest_names_every_fixed_and_ambient_callback_boundary(self) -> None:
        callbacks = self.bundle["callbacks"]
        self.assertEqual(callbacks["status"], "PASS_WITH_TCB_BOUNDARY")
        self.assertEqual(
            {entry["callback_id"] for entry in callbacks["callbacks"]},
            {
                "JSON_OBJECT_PAIRS_HOOK",
                "EMAIL_POLICY_HEADER_FACTORY",
                "FIXED_TEXT_CODEC_REGISTRY",
                "AMBIENT_INTERPRETER_HOOKS",
            },
        )
        self.assertTrue(all(not entry["vendor_selectable"] for entry in callbacks["callbacks"]))

    def test_current_analyzer_gate_fails_closed_and_names_every_accepted_case(self) -> None:
        review = self.bundle["review"]
        self.assertEqual(review["status"], "FAIL")
        self.assertEqual(review["decision"], "I1_FAIL_STOP")
        accepted = [row for row in review["negative_cases"] if row["actual_decision"] == "ACCEPT"]
        self.assertGreater(len(accepted), 0)
        self.assertEqual(review["summary"]["unexpected_accepts"], len(accepted))
        self.assertTrue(
            {row["category"] for row in accepted}.intersection(
                {"ALIAS", "REFLECTION", "OUTPUT_REENTRY"}
            )
        )

    def test_policy_and_three_evidence_files_are_exactly_reproducible(self) -> None:
        paths = {
            "policy": EVIDENCE / "scanner-data-nonexecution-policy-v1.json",
            "callbacks": EVIDENCE / "trusted-callback-manifest-v1.json",
            "review": EVIDENCE / "scanner-dataflow-review-v1.json",
        }
        for name, path in paths.items():
            with self.subTest(name=name):
                persisted = json.loads(path.read_text(encoding="utf-8"))
                self.assertEqual(persisted, self.bundle[name])

    def test_audit_execution_cannot_use_dangerous_apis_or_mutate_files(self) -> None:
        with (
            mock.patch("builtins.eval", side_effect=AssertionError("eval called")),
            mock.patch("builtins.exec", side_effect=AssertionError("exec called")),
            mock.patch("os.system", side_effect=AssertionError("process called")),
            mock.patch.object(subprocess, "Popen", side_effect=AssertionError("process called")),
            mock.patch.object(pickle, "loads", side_effect=AssertionError("pickle called")),
            mock.patch.object(marshal, "loads", side_effect=AssertionError("marshal called")),
            mock.patch.object(Path, "write_bytes", side_effect=AssertionError("write called")),
            mock.patch.object(Path, "write_text", side_effect=AssertionError("write called")),
            mock.patch.object(Path, "unlink", side_effect=AssertionError("delete called")),
            mock.patch.object(Path, "mkdir", side_effect=AssertionError("mkdir called")),
        ):
            again = build_evidence(SCANNER, CASES)
        self.assertEqual(again, self.bundle)


if __name__ == "__main__":
    unittest.main()
