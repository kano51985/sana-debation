from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "eval"))

from build_e6_clean_blind_grade_prompt import build_clean_grade_prompt  # noqa: E402
from build_e6_prompt import load_case  # noqa: E402


class E6CleanBlindPromptTests(unittest.TestCase):
    def test_protocol_and_original_run_id_are_redacted(self) -> None:
        case = load_case(ROOT / "eval" / "e6_cases.jsonl", "F3-short")
        artifact = {
            "run_id": "ORIGINAL-fixed-three-v1",
            "audit_valid": True,
            "terminal_findings": [],
        }
        prompt = build_clean_grade_prompt(case, artifact, "RUN-Z", {"ok": True})
        self.assertNotIn("ORIGINAL-fixed-three-v1", prompt)
        self.assertNotIn("fixed-three-v1", prompt)
        self.assertIn("RUN-Z", prompt)

    def test_schema_is_structured_output_compatible(self) -> None:
        schema = json.loads(
            (ROOT / "eval" / "e6_clean_blind_grade.schema.json").read_text(encoding="utf-8")
        )
        self.assertEqual(set(schema["required"]), set(schema["properties"]))
        self.assertNotIn(
            "uniqueItems", schema["properties"]["unsupported_material_finding_refs"]
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
