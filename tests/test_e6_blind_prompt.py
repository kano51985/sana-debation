from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "eval"))

from build_e6_blind_grade_prompt import build_grade_prompt  # noqa: E402
from build_e6_prompt import load_case  # noqa: E402


class E6BlindPromptTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.case = load_case(ROOT / "eval" / "e6_cases.jsonl", "F2-short")
        cls.artifact = {
            "case_id": "F2-short",
            "run_id": "F2S-FIXED-PILOT",
            "protocol_conformant": True,
            "audit_valid": True,
            "cycles_used": 3,
            "terminal_findings": [],
            "chief_disposition": "DEFER",
            "limitations": ["fixed-three-v1 was used"],
        }
        cls.host_audit = {"schema_valid": True, "three_distinct_core_threads": True}

    def test_protocol_and_original_run_id_are_redacted(self) -> None:
        prompt = build_grade_prompt(self.case, self.artifact, "RUN-Q7M2", self.host_audit)
        self.assertNotIn("fixed-three-v1", prompt)
        self.assertNotIn("adaptive-axes-v1", prompt)
        self.assertNotIn("F2S-FIXED-PILOT", prompt)
        self.assertIn("RUN-Q7M2", prompt)

    def test_p5_protocol_and_materiality_contract_are_redacted(self) -> None:
        artifact = dict(self.artifact)
        artifact.update(
            {
                "run_id": "P5-SECRET-RUN",
                "protocol_id": "adaptive-axes-v2",
                "materiality_contract_id": "baseline-delta-ledger-v1",
                "limitations": [
                    "adaptive-axes-v2 used baseline-delta-ledger-v1"
                ],
            }
        )
        prompt = build_grade_prompt(self.case, artifact, "RUN-P5B2", self.host_audit)
        self.assertNotIn("adaptive-axes-v2", prompt)
        self.assertNotIn("baseline-delta-ledger-v1", prompt)
        self.assertNotIn("P5-SECRET-RUN", prompt)
        self.assertIn("RUN-P5B2", prompt)

    def test_gold_contract_and_closed_world_rules_are_present(self) -> None:
        prompt = build_grade_prompt(self.case, self.artifact, "RUN-Q7M2", self.host_audit)
        self.assertIn("CRIT-F2-SECOND-ORDER", prompt)
        self.assertIn("Do not spawn subagents", prompt)
        self.assertIn("lexical similarity alone is insufficient", prompt)


if __name__ == "__main__":
    unittest.main()
