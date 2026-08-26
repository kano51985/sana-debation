from __future__ import annotations

import copy
import json
from pathlib import Path
import sys
import unittest

from jsonschema import Draft202012Validator, ValidationError


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from p5_protocol import (  # noqa: E402
    P5ProtocolViolation,
    attest_candidate,
    capture_baseline,
    close_finding,
    link_candidate_to_finding,
    make_delta_candidate,
    make_peer_discovery_finding,
    reconcile_terminal,
    rollback_authority_epoch,
    route_delta_candidates,
    validate_authority_publication,
    validate_finding_batch,
    validate_projection,
)


def trace(observable: str = "a distinct revised concern is suppressed") -> dict[str, str]:
    return {
        "precondition": "the mechanism ID is retained across revisions",
        "event": "the supplied revision changes handler behavior",
        "observable_failure": observable,
    }


class P5CoreTests(unittest.TestCase):
    def setUp(self) -> None:
        self.baseline = capture_baseline(
            "Concerns sharing an axis and mechanism ID are duplicates."
        )

    def candidate(
        self,
        *,
        classification: str = "DECISION_RELEVANT",
        supplied_behavior_change: bool = True,
        decision_surface: str = "deduplication equivalence",
    ) -> dict:
        return make_delta_candidate(
            baseline=self.baseline,
            proposal_ref="P0",
            decision_surface=decision_surface,
            change_kind="CHANGED",
            before="axis and mechanism ID imply duplicate",
            after="changed failure contracts remain distinct across revisions",
            classification=classification,
            rationale="the duplicate decision changes",
            supplied_behavior_change=supplied_behavior_change,
        )

    def finding(self, candidate: dict) -> dict:
        return link_candidate_to_finding(
            candidate,
            axis="revision effects",
            mechanism="cross-revision duplicate classification",
            issue_statement="a changed handler can be suppressed under an unchanged ID",
            failure_trace=trace(),
            falsifier="prove unchanged observable behavior across the supplied revision",
        )

    def test_baseline_capture_is_literal_and_stable(self) -> None:
        second = capture_baseline(self.baseline["literal_content"])
        self.assertEqual("B0", self.baseline["baseline_ref"])
        self.assertEqual(self.baseline["content_hash"], second["content_hash"])

    def test_preemptive_repair_is_retained_as_resolved_finding_and_routes_cycle(self) -> None:
        candidate = attest_candidate(self.candidate(), "RELEVANT", "Peer verified the B0/P0 delta")
        finding = close_finding(
            self.finding(candidate),
            status="RESOLVED",
            response_status="accepted",
            response_basis="P0 replaces ID-only equivalence with failure-contract comparison",
            peer_disposition="modified",
            peer_verification_basis="B0/P0 replay proves the structural defect is removed",
        )
        route = route_delta_candidates([candidate], supplied_conflict_ids=[candidate["candidate_id"]])
        terminal = reconcile_terminal(
            candidates=[candidate],
            findings=[finding],
            cycles_used=1,
            chief_disposition="APPROVE",
        )
        self.assertFalse(route["zero_cycle_eligible"])
        self.assertEqual(1, route["minimum_substantive_cycles"])
        self.assertEqual([finding["finding_id"]], terminal["detected_finding_ids"])

    def test_supplied_behavior_change_cannot_be_attested_non_relevant(self) -> None:
        candidate = attest_candidate(
            self.candidate(classification="NON_DECISION_RELEVANT"),
            "NON_RELEVANT",
            "exact severity is unknown",
        )
        with self.assertRaises(P5ProtocolViolation) as raised:
            route_delta_candidates([candidate], supplied_conflict_ids=[candidate["candidate_id"]])
        self.assertEqual("SUPPLIED_CHANGE_MISCLASSIFIED", raised.exception.code)

    def test_editorial_delta_can_remain_zero_cycle_after_peer_attestation(self) -> None:
        candidate = make_delta_candidate(
            baseline=self.baseline,
            proposal_ref="P0",
            decision_surface="wording",
            change_kind="CHANGED",
            before="duplicate",
            after="semantically duplicate",
            classification="NON_DECISION_RELEVANT",
            rationale="wording only",
            supplied_behavior_change=False,
        )
        candidate = attest_candidate(candidate, "NON_RELEVANT", "Peer verified no decision effect")
        route = route_delta_candidates([candidate], supplied_conflict_ids=[])
        terminal = reconcile_terminal(
            candidates=[candidate], findings=[], cycles_used=0, chief_disposition="APPROVE"
        )
        self.assertTrue(route["zero_cycle_eligible"])
        self.assertEqual([], terminal["detected_finding_ids"])

    def test_missing_attestation_and_missing_finding_link_fail_closed(self) -> None:
        candidate = self.candidate()
        with self.assertRaises(P5ProtocolViolation) as missing_attestation:
            route_delta_candidates([candidate], supplied_conflict_ids=[])
        self.assertEqual("CLASSIFICATION_ATTESTATION_MISSING", missing_attestation.exception.code)

        candidate = attest_candidate(candidate, "RELEVANT", "verified")
        with self.assertRaises(P5ProtocolViolation) as missing_link:
            reconcile_terminal(
                candidates=[candidate], findings=[], cycles_used=1, chief_disposition="APPROVE"
            )
        self.assertEqual("CANDIDATE_FINDING_LINK_MISSING", missing_link.exception.code)

    def test_generic_closure_and_unjustified_batch_fail_closed(self) -> None:
        candidate = attest_candidate(self.candidate(), "RELEVANT", "verified")
        with self.assertRaises(P5ProtocolViolation) as generic:
            close_finding(
                self.finding(candidate),
                status="RESOLVED",
                response_status="accepted",
                response_basis="already fixed",
                peer_disposition="modified",
                peer_verification_basis="looks addressed",
            )
        self.assertEqual("RESPONSE_EVIDENCE_MISSING", generic.exception.code)

        second_candidate = attest_candidate(
            self.candidate(decision_surface="audit history"), "RELEVANT", "verified"
        )
        first = self.finding(candidate)
        second = link_candidate_to_finding(
            second_candidate,
            axis="audit semantics",
            mechanism="historical projection",
            issue_statement="history can be overwritten",
            failure_trace=trace("auditors reconstruct the wrong historical decision"),
            falsifier="immutable event replay",
        )
        with self.assertRaises(P5ProtocolViolation) as batch:
            validate_finding_batch([first, second])
        self.assertEqual("BATCH_CAUSALITY_UNJUSTIFIED", batch.exception.code)

    def test_finding_identity_is_stable_across_resolution(self) -> None:
        candidate = attest_candidate(self.candidate(), "RELEVANT", "verified")
        finding = self.finding(candidate)
        resolved = close_finding(
            finding,
            status="RESOLVED",
            response_status="accepted",
            response_basis="changed comparison key is present in P0",
            peer_disposition="modified",
            peer_verification_basis="replay distinguishes old and new failure contracts",
        )
        self.assertEqual(finding["finding_id"], resolved["finding_id"])

    def test_peer_discovery_routes_unchanged_flawed_baseline_without_delta(self) -> None:
        finding = make_peer_discovery_finding(
            baseline=self.baseline,
            proposal_ref="P0",
            precondition_provenance="SUPPLIED_FACT",
            axis="materiality",
            mechanism="ID-only semantic equivalence",
            issue_statement="unchanged IDs suppress supplied changed behavior",
            failure_trace=trace(),
            falsifier="prove the supplied handler change preserves observable behavior",
        )
        finding = close_finding(
            finding,
            status="RESOLVED",
            response_status="accepted",
            response_basis="P1 adds observable failure-contract identity",
            peer_disposition="modified",
            peer_verification_basis="Peer replay distinguishes the supplied handler change",
        )
        terminal = reconcile_terminal(
            candidates=[],
            findings=[finding],
            cycles_used=1,
            chief_disposition="APPROVE",
        )
        self.assertIsNone(finding["candidate_id"])
        self.assertEqual("PEER_DISCOVERY", finding["provenance_origin"])
        self.assertEqual([finding["finding_id"]], terminal["detected_finding_ids"])

    def test_hypothetical_cannot_be_promoted_to_peer_discovery(self) -> None:
        with self.assertRaises(P5ProtocolViolation) as raised:
            make_peer_discovery_finding(
                baseline=self.baseline,
                proposal_ref="P0",
                precondition_provenance="HYPOTHETICAL",
                axis="materiality",
                mechanism="invented outage",
                issue_statement="an unsupplied outage might occur",
                failure_trace=trace("a hypothetical failure occurs"),
                falsifier="external evidence not present in the closed world",
            )
        self.assertEqual("PEER_DISCOVERY_PROVENANCE_INVALID", raised.exception.code)


class P5AuthorityTests(unittest.TestCase):
    def canonical(self) -> dict:
        return {
            "artifact_id": "artifact-1",
            "detected_finding_ids": ["F-1"],
            "chief_disposition": "APPROVE",
            "open_risk_ids": [],
        }

    def projection(self) -> dict:
        return {
            "canonical_parent_id": "artifact-1",
            "detected_finding_ids": ["F-1"],
            "chief_disposition": "APPROVE",
            "open_risk_ids": [],
            "loss_manifest": [],
        }

    def test_projection_cannot_erase_detection_or_disposition(self) -> None:
        broken = self.projection()
        broken["detected_finding_ids"] = []
        with self.assertRaises(P5ProtocolViolation) as raised:
            validate_projection(self.canonical(), broken)
        self.assertEqual("PROJECTION_NON_INJECTIVE", raised.exception.code)

    def test_authority_requires_registered_route_and_matching_receipt(self) -> None:
        canonical = self.canonical()
        projection = self.projection()
        registry = [
            {
                "route_id": "grader-primary",
                "schema_version": 1,
                "authority_capability": True,
                "epoch": 4,
            }
        ]
        receipts = [
            {
                "route_id": "grader-primary",
                "epoch": 4,
                "artifact_digest": "wrong",
                "detected_finding_ids": ["F-1"],
                "chief_disposition": "APPROVE",
            }
        ]
        with self.assertRaises(P5ProtocolViolation) as mismatch:
            validate_authority_publication(
                canonical,
                projection,
                registry=registry,
                receipts=receipts,
                required_route_ids=["grader-primary"],
                epoch=4,
            )
        self.assertEqual("CONSUMER_RECEIPT_MISMATCH", mismatch.exception.code)

        with self.assertRaises(P5ProtocolViolation) as unregistered:
            validate_authority_publication(
                canonical,
                projection,
                registry=registry,
                receipts=[],
                required_route_ids=["grader-primary", "legacy-export"],
                epoch=4,
            )
        self.assertEqual("AUTHORITY_ROUTE_UNREGISTERED", unregistered.exception.code)

    def test_authority_accepts_matching_registered_route_and_receipt(self) -> None:
        canonical = self.canonical()
        projection = self.projection()
        digest = validate_projection(canonical, projection)["artifact_digest"]
        result = validate_authority_publication(
            canonical,
            projection,
            registry=[
                {
                    "route_id": "grader-primary",
                    "authority_capability": True,
                    "epoch": 4,
                }
            ],
            receipts=[
                {
                    "route_id": "grader-primary",
                    "epoch": 4,
                    "artifact_digest": digest,
                    "detected_finding_ids": ["F-1"],
                    "chief_disposition": "APPROVE",
                }
            ],
            required_route_ids=["grader-primary"],
            epoch=4,
        )
        self.assertEqual("AUTHORIZED", result["status"])

    def test_authority_rejects_missing_ack_wrong_epoch_and_bypass(self) -> None:
        canonical = self.canonical()
        projection = self.projection()
        with self.assertRaises(P5ProtocolViolation) as missing:
            validate_authority_publication(
                canonical,
                projection,
                registry=[{"route_id": "grader", "authority_capability": True, "epoch": 4}],
                receipts=[],
                required_route_ids=["grader"],
                epoch=4,
            )
        self.assertEqual("CONSUMER_ACK_MISSING", missing.exception.code)

        with self.assertRaises(P5ProtocolViolation) as stale:
            validate_authority_publication(
                canonical,
                projection,
                registry=[{"route_id": "grader", "authority_capability": True, "epoch": 3}],
                receipts=[],
                required_route_ids=["grader"],
                epoch=4,
            )
        self.assertEqual("AUTHORITY_EPOCH_MISMATCH", stale.exception.code)

        with self.assertRaises(P5ProtocolViolation) as bypass:
            validate_authority_publication(
                canonical,
                projection,
                registry=[{"route_id": "grader", "authority_capability": False, "epoch": 4}],
                receipts=[],
                required_route_ids=["grader"],
                epoch=4,
            )
        self.assertEqual("AUTHORITY_BYPASS_ATTEMPT", bypass.exception.code)

    def test_rollback_creates_future_epoch_without_rewriting_history(self) -> None:
        result = rollback_authority_epoch(
            current_epoch=4,
            issued_artifact_epochs={"artifact-1": 3, "artifact-2": 4},
        )
        self.assertEqual(5, result["new_epoch"])
        self.assertEqual({"artifact-1": 3, "artifact-2": 4}, result["issued_artifact_epochs"])

        with self.assertRaises(P5ProtocolViolation) as future:
            rollback_authority_epoch(
                current_epoch=4,
                issued_artifact_epochs={"artifact-future": 5},
            )
        self.assertEqual("HISTORICAL_INTERPRETATION_MISMATCH", future.exception.code)


class P5SchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = json.loads(
            (ROOT / "schemas" / "adaptive-axes-v2.schema.json").read_text(encoding="utf-8")
        )
        Draft202012Validator.check_schema(cls.schema)

    def valid_run(self) -> dict:
        return {
            "run_id": "p5-run",
            "protocol_id": "adaptive-axes-v2",
            "schema_version": 1,
            "baseline": {
                "baseline_ref": "B0",
                "content_hash": "a" * 64,
                "literal_content": "literal supplied baseline",
            },
            "delta_candidates": [
                {
                    "candidate_id": "C1",
                    "baseline_ref": "B0",
                    "baseline_hash": "a" * 64,
                    "proposal_ref": "P0",
                    "decision_surface": "deduplication",
                    "change_kind": "CHANGED",
                    "before": "ID equality",
                    "after": "behavioral equivalence",
                    "classification": "DECISION_RELEVANT",
                    "precondition_provenance": "SUPPLIED_FACT",
                    "provenance_origin": "BASELINE_DELTA",
                    "rationale": "decision semantics changed",
                    "supplied_behavior_change": True,
                    "peer_attestation": "RELEVANT",
                    "peer_attestation_basis": "verified against B0 and P0",
                    "finding_id": "F1",
                }
            ],
            "terminal_findings": [
                {
                    "finding_id": "F1",
                    "candidate_id": "C1",
                    "baseline_ref": "B0",
                    "baseline_hash": "a" * 64,
                    "proposal_ref": "P0",
                    "provenance_origin": "BASELINE_DELTA",
                    "precondition_provenance": "SUPPLIED_FACT",
                    "axis": "revision effects",
                    "mechanism": "duplicate classification",
                    "issue_statement": "changed behavior is suppressed",
                    "failure_trace": trace(),
                    "falsifier": "behavioral equivalence evidence",
                    "status": "RESOLVED",
                    "response_status": "accepted",
                    "response_basis": "comparison key changed",
                    "peer_disposition": "modified",
                    "peer_verification_basis": "replay verifies the repair",
                }
            ],
            "cycle_accounting": {
                "interactions": 2,
                "substantive_cycles": 1,
                "routed_findings": 1,
                "substantively_closed_findings": 1,
                "zero_cycle_eligible": False,
            },
            "authority": {
                "epoch": 1,
                "status": "PENDING_AUTHORITY",
                "required_route_ids": ["grader-primary"],
                "receipts": [],
            },
            "chief_decision": {
                "disposition": "approve",
                "basis": "all findings resolved",
            },
        }

    def test_canonical_schema_accepts_complete_run_and_rejects_missing_candidate_ledger(self) -> None:
        validator = Draft202012Validator(self.schema)
        run = self.valid_run()
        validator.validate(run)
        broken = copy.deepcopy(run)
        del broken["delta_candidates"]
        with self.assertRaises(ValidationError):
            validator.validate(broken)


if __name__ == "__main__":
    unittest.main(verbosity=2)
