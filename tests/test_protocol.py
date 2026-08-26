from __future__ import annotations

import copy
import json
from pathlib import Path
import sys
import unittest

from jsonschema import Draft202012Validator, ValidationError


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from protocol import (  # noqa: E402
    ADAPTIVE_PROTOCOL,
    CorrectionBudget,
    FIXED_PROTOCOL,
    ProtocolStateMachine,
    ProtocolViolation,
    classify_issue_equivalence,
    make_envelope,
    reconcile_axis,
    resolve_protocol,
    sha256_json,
    validate_axis_coverage,
    validate_capability_acks,
    validate_envelope,
)


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def failure_trace():
    return {
        "precondition": "a prior inspection is closed",
        "event": "a later proposal changes shared behavior",
        "observable_failure": "the terminal record remains stale",
    }


def proposer_response(issue="ISSUE-1"):
    return {"challenge_id": issue, "status": "accepted", "basis": "behavior changed in the proposal"}


def fixed_cycle(index: int):
    return {
        "cycle_id": f"R{index}",
        "axis_id": f"A{index}",
        "proposal_ref": f"P{index}",
        "mechanism": "bounded routed review",
        "rebuttal": "a named invariant can fail",
        "failure_trace": failure_trace(),
        "falsifier": "a golden trace showing the invariant remains enforced",
        "proposer_responses": [proposer_response(f"ISSUE-{index}")],
        "proposal_diff": "add a fail-closed guard",
        "risk_updates": [f"R{index}"],
        "peer_closing_assessment": "the diff closes the design gap",
        "verdict": "modified",
        "evidence_ids": ["E1"],
        "risk_ids": [f"R{index}"],
    }


def adaptive_cycle(index: int):
    value = fixed_cycle(index)
    value.pop("proposal_ref")
    value["proposal_ref_before"] = f"P{index - 1}"
    value["proposal_ref_after"] = f"P{index}"
    return value


def chief_decision(adaptive: bool):
    value = {
        "disposition": "defer pending named evidence",
        "basis": "named conformance evidence remains missing",
        "trace_matrix": [{"issue": "compatibility", "effect": "defer"}],
        "next_action": "run the named evidence gates",
    }
    if adaptive:
        value["stage1_reconciliation"] = [
            {"concern_id": "C1", "status": "CONFIRMED_OPEN", "basis": "E7 is absent"}
        ]
    return value


def adaptive_run(cycle_count: int):
    terminal_ref = f"P{cycle_count}"
    return {
        "run_id": f"adaptive-{cycle_count}",
        "protocol_id": ADAPTIVE_PROTOCOL,
        "schema_version": 1,
        "axis_inspections": [
            {
                "axis_id": f"A{i}",
                "proposal_ref": "P0",
                "mechanism": "inspect the frozen axis",
                "outcome": "MATERIAL_CHALLENGE" if i <= cycle_count else "NO_MATERIAL_OBJECTION",
                "concern_tested": "a decision-critical failure class",
                "reopen_condition": "a changed proposal or new evidence",
                "issue_id": f"ISSUE-{i}" if i <= cycle_count else None,
                "evidence_ids": ["E1"],
                "risk_ids": [f"R{i}"],
            }
            for i in range(1, 4)
        ],
        "cycles": [adaptive_cycle(i) for i in range(1, cycle_count + 1)],
        "terminal_axis_records": [
            {
                "axis_id": f"A{i}",
                "terminal_proposal_ref": terminal_ref,
                "reviewed_diff_ids": [f"D{j}" for j in range(1, cycle_count + 1)],
                "semantic_dependency_ids": [],
                "impact": "NONE",
                "outcome": "TERMINAL_EQUIVALENT",
                "impact_basis": "no reviewed diff changes this axis",
                "finding_id": None,
                "evidence_ids": ["E1"],
                "risk_ids": [f"R{i}"],
            }
            for i in range(1, 4)
        ],
        "chief_terminal_scan": {
            "scan_id": "SCAN-1",
            "terminal_proposal_ref": terminal_ref,
            "context_exposure": "TERMINAL_ONLY",
            "axis_scans": [
                {
                    "axis_id": f"A{i}",
                    "current_mechanism": "terminal protocol mechanism",
                    "outcome": "NO_MATERIAL_FAILURE_FOUND",
                    "failure_trace": None,
                    "falsifier": "a changed terminal mechanism reopens the scan",
                    "invariant_ids": [f"I{i}"],
                    "evidence_ids": ["E1"],
                }
                for i in range(1, 4)
            ],
            "cross_axis_concerns": [],
        },
        "chief_decision": chief_decision(adaptive=True),
    }


def issue(issue_id="X", proposal_ref="P0"):
    return {
        "issue_id": issue_id,
        "proposal_ref": proposal_ref,
        "axis_id": "A1",
        "mechanism_id": "routing-close",
        "invariant_ids": ["I4"],
        "affected_behavior_ids": ["terminal-coverage"],
        "risk_ids": ["R6"],
        "evidence_request_ids": ["E7"],
        "failure_signature": {
            "precondition_class": "prior-axis-closed",
            "event_class": "cross-axis-diff",
            "observable_failure_class": "stale-terminal-record",
        },
        "falsifier_id": "T1",
    }


class GoldenTraceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.traces = load_json(ROOT / "fixtures" / "golden_traces.json")

    def test_resolver_golden_traces(self):
        for case in self.traces["resolver"]:
            with self.subTest(case=case["id"]):
                result = resolve_protocol(case["invocation"], case["structured_protocol"])
                self.assertEqual(case["expected_status"], result.status)
                self.assertEqual(case["expected_protocol"], result.protocol_id)
                self.assertEqual(64, len(result.to_dict()["resolution_hash"]))

    def test_state_machine_golden_traces(self):
        for case in self.traces["state_machines"]:
            with self.subTest(case=case["id"]):
                machine = ProtocolStateMachine(case["protocol_id"])
                if "expected_error" in case:
                    with self.assertRaises(ProtocolViolation) as raised:
                        for event in case["events"]:
                            machine.apply(event)
                    self.assertEqual(case["expected_error"], raised.exception.code)
                else:
                    for event in case["events"]:
                        machine.apply(event)
                    self.assertEqual(case["expected_state"], machine.state)
                    self.assertEqual(case["expected_cycles"], machine.cycles_used)


class ArtifactTests(unittest.TestCase):
    def test_canonical_hash_is_order_independent_for_object_keys(self):
        self.assertEqual(sha256_json({"b": 2, "a": 1}), sha256_json({"a": 1, "b": 2}))

    def test_envelope_and_hash_chain(self):
        first = make_envelope(
            run_id="run-1",
            protocol_id=FIXED_PROTOCOL,
            artifact_type="frame",
            sequence=0,
            payload={"decision": "D1"},
        )
        validate_envelope(first)
        second = make_envelope(
            run_id="run-1",
            protocol_id=FIXED_PROTOCOL,
            artifact_type="proposal",
            sequence=1,
            payload={"proposal": "P0"},
            proposal_ref="P0",
            previous_artifact_hash=first["artifact_hash"],
        )
        validate_envelope(second, expected_previous_hash=first["artifact_hash"])

    def test_hash_tampering_fails(self):
        artifact = make_envelope(
            run_id="run-1",
            protocol_id=FIXED_PROTOCOL,
            artifact_type="frame",
            sequence=0,
            payload={"decision": "D1"},
        )
        artifact["payload"]["decision"] = "tampered"
        with self.assertRaises(ProtocolViolation) as raised:
            validate_envelope(artifact)
        self.assertEqual("ARTIFACT_HASH_MISMATCH", raised.exception.code)

    def test_unknown_schema_and_unknown_field_fail_closed(self):
        artifact = make_envelope(
            run_id="run-1",
            protocol_id=FIXED_PROTOCOL,
            artifact_type="frame",
            sequence=0,
            payload={"decision": "D1"},
        )
        wrong_version = copy.deepcopy(artifact)
        wrong_version["schema_version"] = 2
        with self.assertRaises(ProtocolViolation) as raised:
            validate_envelope(wrong_version)
        self.assertEqual("UNKNOWN_SCHEMA_VERSION", raised.exception.code)

        unknown_field = copy.deepcopy(artifact)
        unknown_field["extension"] = "not declared by schema-1"
        with self.assertRaises(ProtocolViolation) as raised:
            validate_envelope(unknown_field)
        self.assertEqual("UNKNOWN_FIELD", raised.exception.code)

    def test_capability_ack_fails_closed(self):
        acks = [
            {"actor_id": actor, "protocol_id": ADAPTIVE_PROTOCOL, "schema_version": 1, "supported": True}
            for actor in ("root", "proposing_tl", "peer_tl")
        ]
        with self.assertRaises(ProtocolViolation) as raised:
            validate_capability_acks(acks, protocol_id=ADAPTIVE_PROTOCOL, schema_version=1)
        self.assertEqual("CAPABILITY_MISMATCH", raised.exception.code)

    def test_one_focused_correction_then_protocol_invalid(self):
        budget = CorrectionBudget()
        self.assertEqual("CORRECTION_REQUESTED", budget.request("cycle-1", "MALFORMED_ARTIFACT"))
        with self.assertRaises(ProtocolViolation) as raised:
            budget.request("cycle-1", "MALFORMED_ARTIFACT")
        self.assertEqual("PROTOCOL_INVALID", raised.exception.code)
        self.assertEqual(2, len(budget.audit))

    def test_static_protocol_error_is_not_retryable(self):
        budget = CorrectionBudget()
        with self.assertRaises(ProtocolViolation) as raised:
            budget.request("capability", "CAPABILITY_MISMATCH")
        self.assertEqual("NON_RETRYABLE_PROTOCOL_ERROR", raised.exception.code)


class DuplicateClassifierTests(unittest.TestCase):
    def test_exact_effect_with_reviewed_unchanged_diff_is_duplicate(self):
        predecessor = issue()
        candidate = copy.deepcopy(predecessor)
        candidate.update(
            {
                "issue_id": "Y",
                "proposal_ref": "P1",
                "predecessor_issue_id": "X",
                "proposal_dependency_impact": "NONE",
                "reviewed_diff_ids": ["D1"],
            }
        )
        self.assertEqual("DUPLICATE", classify_issue_equivalence(predecessor, candidate))

    def test_distinct_failure_effect_is_new_issue(self):
        predecessor = issue()
        candidate = copy.deepcopy(predecessor)
        candidate["issue_id"] = "Y"
        candidate["failure_signature"]["observable_failure_class"] = "silent-invariant-loss"
        self.assertEqual("NEW_ISSUE", classify_issue_equivalence(predecessor, candidate))

    def test_transitive_dependency_is_new_issue(self):
        predecessor = issue()
        candidate = copy.deepcopy(predecessor)
        candidate.update(
            {
                "issue_id": "Y",
                "proposal_ref": "P1",
                "predecessor_issue_id": "X",
                "proposal_dependency_impact": "TRANSITIVE",
                "reviewed_diff_ids": ["D1"],
            }
        )
        self.assertEqual("NEW_ISSUE", classify_issue_equivalence(predecessor, candidate))

    def test_changed_proposal_without_reviewed_diffs_is_indeterminate(self):
        predecessor = issue()
        candidate = copy.deepcopy(predecessor)
        candidate.update(
            {
                "issue_id": "Y",
                "proposal_ref": "P1",
                "predecessor_issue_id": "X",
                "proposal_dependency_impact": "NONE",
            }
        )
        with self.assertRaises(ProtocolViolation) as raised:
            classify_issue_equivalence(predecessor, candidate)
        self.assertEqual("EQUIVALENCE_INDETERMINATE", raised.exception.code)


class TerminalReconciliationTests(unittest.TestCase):
    def test_T1_cycle_three_transitive_defect_stays_open(self):
        result = reconcile_axis(
            axis_id="A1",
            prior_proposal_ref="P2",
            terminal_proposal_ref="P3",
            cycles_used=3,
            diffs=[
                {
                    "diff_id": "D3",
                    "from_ref": "P2",
                    "to_ref": "P3",
                    "axis_impacts": [
                        {
                            "axis_id": "A1",
                            "impact": "TRANSITIVE",
                            "material_issue": {"issue_id": "T1-DEFECT", "invariant_ids": ["I4"]},
                        }
                    ],
                }
            ],
        )
        self.assertEqual("OPEN_BUDGET_EXHAUSTED", result["status"])

    def test_T2_no_semantic_dependency_is_terminal_equivalent(self):
        result = reconcile_axis(
            axis_id="A1",
            prior_proposal_ref="P2",
            terminal_proposal_ref="P3",
            cycles_used=2,
            diffs=[
                {
                    "diff_id": "D3",
                    "from_ref": "P2",
                    "to_ref": "P3",
                    "axis_impacts": [{"axis_id": "A1", "impact": "NONE", "material_issue": None}],
                }
            ],
        )
        self.assertEqual("TERMINAL_EQUIVALENT", result["status"])
        self.assertEqual(["D3"], result["reviewed_diff_ids"])

    def test_T3_material_issue_below_ceiling_reenters_queue(self):
        result = reconcile_axis(
            axis_id="A2",
            prior_proposal_ref="P1",
            terminal_proposal_ref="P2",
            cycles_used=2,
            diffs=[
                {
                    "diff_id": "D2",
                    "from_ref": "P1",
                    "to_ref": "P2",
                    "axis_impacts": [
                        {
                            "axis_id": "A2",
                            "impact": "DIRECT",
                            "material_issue": {"issue_id": "T3-DEFECT", "invariant_ids": ["I4"]},
                        }
                    ],
                }
            ],
        )
        self.assertEqual("QUEUED", result["status"])

    def test_T4_hash_or_malformed_reconciliation_is_invalid(self):
        mismatch = reconcile_axis(
            axis_id="A1",
            prior_proposal_ref="P1",
            terminal_proposal_ref="P3",
            cycles_used=1,
            diffs=[{"diff_id": "D2", "from_ref": "P1", "to_ref": "P2", "axis_impacts": []}],
        )
        malformed = reconcile_axis(
            axis_id="A1",
            prior_proposal_ref="P1",
            terminal_proposal_ref="P2",
            cycles_used=1,
            diffs=[{"diff_id": "D2", "from_ref": "P1", "to_ref": "P2"}],
        )
        self.assertEqual("PROTOCOL_INVALID", mismatch["status"])
        self.assertEqual("PROTOCOL_INVALID", malformed["status"])


class SchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixed_schema = load_json(ROOT / "schemas" / "fixed-three-v1.schema.json")
        cls.adaptive_schema = load_json(ROOT / "schemas" / "adaptive-axes-v1.schema.json")
        Draft202012Validator.check_schema(cls.fixed_schema)
        Draft202012Validator.check_schema(cls.adaptive_schema)

    def test_fixed_success_requires_exactly_three_complete_rounds(self):
        run = {
            "run_id": "fixed-1",
            "protocol_id": FIXED_PROTOCOL,
            "schema_version": 1,
            "rounds": [fixed_cycle(i) for i in range(1, 4)],
            "risk_register": [
                {"risk_id": "R1", "failure_condition": "missed invariant", "affected_invariant": "I4", "status": "needs evidence"}
            ],
            "chief_decision": chief_decision(adaptive=False),
        }
        Draft202012Validator(self.fixed_schema).validate(run)
        broken = copy.deepcopy(run)
        broken["rounds"] = broken["rounds"][:2]
        with self.assertRaises(ValidationError):
            Draft202012Validator(self.fixed_schema).validate(broken)

    def test_adaptive_zero_one_three_cycle_shapes(self):
        validator = Draft202012Validator(self.adaptive_schema)
        for count in (0, 1, 3):
            with self.subTest(cycles=count):
                run = adaptive_run(count)
                validator.validate(run)
                validate_axis_coverage(run["axis_inspections"])
                validate_axis_coverage(run["terminal_axis_records"])

    def test_missing_cycle_falsifier_fails(self):
        run = adaptive_run(1)
        del run["cycles"][0]["falsifier"]
        with self.assertRaises(ValidationError):
            Draft202012Validator(self.adaptive_schema).validate(run)

    def test_legacy_fixed_consumer_fails_closed_on_adaptive(self):
        run = adaptive_run(0)
        with self.assertRaises(ValidationError):
            Draft202012Validator(self.fixed_schema).validate(run)

    def test_duplicate_axis_records_fail_semantic_validation(self):
        run = adaptive_run(0)
        run["axis_inspections"][2]["axis_id"] = "A2"
        with self.assertRaises(ProtocolViolation) as raised:
            validate_axis_coverage(run["axis_inspections"])
        self.assertEqual("AXIS_COVERAGE_INVALID", raised.exception.code)


if __name__ == "__main__":
    unittest.main(verbosity=2)
