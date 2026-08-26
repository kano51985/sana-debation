from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "eval"))

from build_e6_prompt import build_prompt, load_case  # noqa: E402


class E6PromptTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.case = load_case(ROOT / "eval" / "e6_cases.jsonl", "F2-short")

    def test_prompt_does_not_leak_gold_labels_or_grading_notes(self) -> None:
        prompt = build_prompt(self.case, "adaptive-axes-v1", "pilot-A")
        self.assertNotIn("CRIT-F2-SECOND-ORDER", prompt)
        self.assertNotIn(self.case["grading_notes"], prompt)
        self.assertNotIn("seeded_post_revision_issue_ids", prompt)
        self.assertNotIn("critical_issue_ids", prompt)

    def test_fixed_and_adaptive_contracts_are_distinct(self) -> None:
        fixed = build_prompt(self.case, "fixed-three-v1", "pilot-F")
        adaptive = build_prompt(self.case, "adaptive-axes-v1", "pilot-A")
        self.assertIn("exactly three complete", fixed)
        self.assertIn("zero through three", adaptive)

    def test_worker_budget_is_frozen_and_closed_world(self) -> None:
        fixed = build_prompt(self.case, "fixed-three-v1", "pilot-F")
        adaptive = build_prompt(self.case, "adaptive-axes-v1", "pilot-A")
        marker = "Keep P0 under\n700 words"
        self.assertIn(marker, fixed)
        self.assertIn(marker, adaptive)
        self.assertIn("closed world", fixed)

    def test_worker_has_hash_pinned_skill_snapshot_fallback(self) -> None:
        prompt = build_prompt(self.case, "adaptive-axes-v1", "pilot-A")
        self.assertIn("byte-identical workspace snapshot `SKILL.md`", prompt)
        self.assertIn(
            "D7C599444A4E85FBB089DB7972D060537FB68DC21D6D3068929A95F31B9AD57F",
            prompt,
        )

    def test_chief_handoff_is_protocol_specific_not_conflicting(self) -> None:
        fixed = build_prompt(self.case, "fixed-three-v1", "pilot-F")
        adaptive = build_prompt(self.case, "adaptive-axes-v1", "pilot-A")
        common = "For fixed-three-v1 that is\none complete-record handoff after round 3"
        self.assertIn(common, fixed)
        self.assertIn(common, adaptive)
        self.assertIn("blind terminal scan", adaptive)
        self.assertIn("Fixed-three-v1 has no Peer\nterminal-reconciliation stage", fixed)
        self.assertIn("`CHIEF_DECISION`", fixed)

    def test_output_schemas_parse(self) -> None:
        for name in ("e6_run_output.schema.json", "e6_blind_grade.schema.json"):
            data = json.loads((ROOT / "eval" / name).read_text(encoding="utf-8"))
            self.assertEqual(data["type"], "object")
            self.assertFalse(data["additionalProperties"])

    def test_blind_grade_schema_uses_supported_structured_output_keywords(self) -> None:
        data = json.loads(
            (ROOT / "eval" / "e6_blind_grade.schema.json").read_text(encoding="utf-8")
        )
        for field in (
            "detected_issue_ids",
            "false_no_material_issue_ids",
            "false_duplicate_issue_ids",
        ):
            self.assertNotIn("uniqueItems", data["properties"][field])

    def test_p4_materiality_contract_is_versioned_and_legacy_default_is_stable(self) -> None:
        legacy = build_prompt(self.case, "adaptive-axes-v1", "pilot-A")
        p4 = build_prompt(
            self.case,
            "adaptive-axes-v1",
            "pilot-P4",
            "closed-world-provenance-v1",
        )
        self.assertIn("materiality contract `legacy-v1`", legacy)
        self.assertNotIn("`SUPPLIED_FACT`", legacy)
        self.assertIn("materiality contract `closed-world-provenance-v1`", p4)
        self.assertIn("`SUPPLIED_FACT`", p4)
        self.assertIn("`VERIFIED_EVIDENCE`", p4)
        self.assertIn("`HYPOTHETICAL`", p4)

    def test_p4_hypotheticals_cannot_block_or_become_terminal_findings(self) -> None:
        p4 = build_prompt(
            self.case,
            "fixed-three-v1",
            "pilot-P4",
            "closed-world-provenance-v1",
        )
        self.assertIn("creates no terminal finding", p4)
        self.assertIn("missing evidence for a self-created hypothetical", p4)
        self.assertIn("Fixed still\nreports `cycles_used=3`", p4)

    def test_p4_adaptive_clean_case_can_route_zero_cycles(self) -> None:
        clean = load_case(ROOT / "eval" / "e6_cases.jsonl", "F3-short")
        p4 = build_prompt(
            clean,
            "adaptive-axes-v1",
            "pilot-P4",
            "closed-world-provenance-v1",
        )
        self.assertIn("routes zero cycles", p4)
        self.assertNotIn(clean["grading_notes"], p4)

    def test_p5_protocol_and_contract_are_explicit_without_changing_legacy_default(self) -> None:
        legacy = build_prompt(self.case, "adaptive-axes-v1", "pilot-legacy")
        p5 = build_prompt(
            self.case,
            "adaptive-axes-v2",
            "pilot-P5",
            "baseline-delta-ledger-v1",
        )
        self.assertIn("governed by `adaptive-axes-v2`", p5)
        self.assertIn("materiality contract `baseline-delta-ledger-v1`", p5)
        self.assertIn("materiality contract `legacy-v1`", legacy)
        self.assertNotIn("baseline-delta-ledger-v1", legacy)

    def test_p5_retains_preemptive_repairs_before_classification_and_terminally(self) -> None:
        p5 = build_prompt(
            self.case,
            "adaptive-axes-v2",
            "pilot-P5",
            "baseline-delta-ledger-v1",
        )
        self.assertIn("literal immutable `B0`", p5)
        self.assertIn("before semantic classification", p5)
        self.assertIn("Peer-attested", p5)
        self.assertIn("Resolution changes status only", p5)
        self.assertIn("remain in `terminal_findings`", p5)
        self.assertIn("improved", p5)
        self.assertIn("final proposal is not detection evidence", p5)

    def test_p5_supplied_behavior_change_routes_even_when_impact_details_are_missing(self) -> None:
        noisy = load_case(ROOT / "eval" / "e6_cases.jsonl", "F2-noisy")
        p5 = build_prompt(
            noisy,
            "adaptive-axes-v2",
            "pilot-P5",
            "baseline-delta-ledger-v1",
        )
        self.assertIn("cannot prove equivalence or `NON_DECISION_RELEVANT`", p5)
        self.assertIn("P1 changes the failure handler but retains the mechanism ID", p5)
        self.assertNotIn("CRIT-F2-SECOND-ORDER", p5)
        self.assertNotIn(noisy["grading_notes"], p5)

    def test_p5_clean_case_can_emit_empty_delta_ledger_and_zero_cycles(self) -> None:
        clean = load_case(ROOT / "eval" / "e6_cases.jsonl", "F3-noisy")
        p5 = build_prompt(
            clean,
            "adaptive-axes-v2",
            "pilot-P5",
            "baseline-delta-ledger-v1",
        )
        self.assertIn("may emit empty", p5)
        self.assertIn("`delta_candidates`", p5)
        self.assertIn("zero substantive cycles", p5)
        self.assertNotIn(clean["grading_notes"], p5)

    def test_p5_worker_schema_is_separate_and_structured_output_compatible(self) -> None:
        data = json.loads(
            (ROOT / "eval" / "e6_run_output_p5.schema.json").read_text(encoding="utf-8")
        )
        self.assertEqual("adaptive-axes-v2", data["properties"]["protocol_id"]["const"])
        self.assertIn("baseline", data["required"])
        self.assertIn("delta_candidates", data["required"])
        self.assertIn("cycle_accounting", data["required"])
        self.assertFalse(data["additionalProperties"])

        def assert_consts_have_types(node: object) -> None:
            if isinstance(node, dict):
                if "const" in node:
                    self.assertIn("type", node)
                for value in node.values():
                    assert_consts_have_types(value)
            elif isinstance(node, list):
                for value in node:
                    assert_consts_have_types(value)

        assert_consts_have_types(data)


if __name__ == "__main__":
    unittest.main()
