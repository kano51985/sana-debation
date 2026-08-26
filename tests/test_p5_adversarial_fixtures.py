from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest


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


class P5AdversarialFixtureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixture = json.loads(
            (ROOT / "fixtures" / "p5_adversarial_traces.json").read_text(encoding="utf-8")
        )

    def setUp(self) -> None:
        self.baseline = capture_baseline("same axis and mechanism ID means duplicate")

    def candidate(self, *, surface: str = "deduplication", classification: str = "DECISION_RELEVANT") -> dict:
        return make_delta_candidate(
            baseline=self.baseline,
            proposal_ref="P0",
            decision_surface=surface,
            change_kind="CHANGED",
            before="mechanism ID equality",
            after="failure-contract equality",
            classification=classification,
            rationale="observable duplicate semantics change",
            supplied_behavior_change=True,
        )

    def finding(self, candidate: dict, *, mechanism: str = "cross-revision deduplication") -> dict:
        return link_candidate_to_finding(
            candidate,
            axis="revision effects",
            mechanism=mechanism,
            issue_statement="changed handlers can be suppressed",
            failure_trace={
                "precondition": "a revision retains its mechanism ID",
                "event": "the supplied revision changes handler behavior",
                "observable_failure": "the distinct revised concern is suppressed",
            },
            falsifier="replay proves unchanged observable behavior",
        )

    @staticmethod
    def canonical() -> dict:
        return {
            "artifact_id": "artifact-1",
            "detected_finding_ids": ["F-1"],
            "chief_disposition": "APPROVE",
            "open_risk_ids": [],
        }

    @staticmethod
    def projection() -> dict:
        return {
            "canonical_parent_id": "artifact-1",
            "detected_finding_ids": ["F-1"],
            "chief_disposition": "APPROVE",
            "open_risk_ids": [],
            "loss_manifest": [],
        }

    def execute(self, operation: str):
        if operation == "supplied_change_non_relevant":
            candidate = attest_candidate(
                self.candidate(classification="NON_DECISION_RELEVANT"),
                "NON_RELEVANT",
                "impact details are absent",
            )
            return route_delta_candidates([candidate], supplied_conflict_ids=[candidate["candidate_id"]])
        if operation == "missing_attestation":
            return route_delta_candidates([self.candidate()], supplied_conflict_ids=[])
        if operation == "missing_finding_link":
            candidate = attest_candidate(self.candidate(), "RELEVANT", "Peer replayed B0/P0")
            return reconcile_terminal(candidates=[candidate], findings=[], cycles_used=1, chief_disposition="APPROVE")
        if operation == "relevant_zero_cycle":
            candidate = attest_candidate(self.candidate(), "RELEVANT", "Peer replayed B0/P0")
            finding = self.finding(candidate)
            return reconcile_terminal(candidates=[candidate], findings=[finding], cycles_used=0, chief_disposition="DEFER")
        if operation in {"generic_response", "already_fixed", "copied_close", "unsupported_close"}:
            candidate = attest_candidate(self.candidate(), "RELEVANT", "Peer replayed B0/P0")
            finding = self.finding(candidate)
            response = {
                "generic_response": "issue addressed",
                "already_fixed": "already fixed in P0",
                "copied_close": "P0 changes equality to observable failure-contract comparison",
                "unsupported_close": "verified",
            }[operation]
            peer_basis = (
                response
                if operation == "copied_close"
                else "Peer replay independently distinguishes the revised handler"
            )
            if operation == "unsupported_close":
                response = "P0 changes equality to observable failure-contract comparison"
                peer_basis = "verified"
            return close_finding(
                finding,
                status="RESOLVED",
                response_status="accepted",
                response_basis=response,
                peer_disposition="modified",
                peer_verification_basis=peer_basis,
            )
        if operation == "unjustified_batch":
            first_candidate = attest_candidate(self.candidate(), "RELEVANT", "Peer verified first")
            second_candidate = attest_candidate(
                self.candidate(surface="audit projection"), "RELEVANT", "Peer verified second"
            )
            first = self.finding(first_candidate)
            second = link_candidate_to_finding(
                second_candidate,
                axis="audit semantics",
                mechanism="historical projection",
                issue_statement="history can be overwritten",
                failure_trace={
                    "precondition": "a correction exists",
                    "event": "a consumer reads a stale projection",
                    "observable_failure": "the wrong historical decision is reconstructed",
                },
                falsifier="immutable epoch replay matches the canonical artifact",
            )
            return validate_finding_batch([first, second])
        if operation == "hypothetical_peer_discovery":
            return make_peer_discovery_finding(
                baseline=self.baseline,
                proposal_ref="P0",
                precondition_provenance="HYPOTHETICAL",
                axis="materiality",
                mechanism="invented outage",
                issue_statement="an unsupplied outage might happen",
                failure_trace={
                    "precondition": "an imagined provider fails",
                    "event": "an imagined retry occurs",
                    "observable_failure": "an imagined result is lost",
                },
                falsifier="evidence outside the frozen case",
            )
        if operation == "projection_loss":
            projection = self.projection()
            projection["detected_finding_ids"] = []
            return validate_projection(self.canonical(), projection)

        canonical = self.canonical()
        projection = self.projection()
        registry = [{"route_id": "grader", "authority_capability": True, "epoch": 4}]
        digest = validate_projection(canonical, projection)["artifact_digest"]
        receipts = [{
            "route_id": "grader",
            "epoch": 4,
            "artifact_digest": digest,
            "detected_finding_ids": ["F-1"],
            "chief_disposition": "APPROVE",
        }]
        if operation == "unknown_route":
            return validate_authority_publication(canonical, projection, registry=registry, receipts=receipts, required_route_ids=["missing"], epoch=4)
        if operation == "authority_bypass":
            registry[0]["authority_capability"] = False
        elif operation == "stale_epoch":
            registry[0]["epoch"] = 3
        elif operation == "missing_ack":
            receipts = []
        elif operation == "bad_receipt":
            receipts[0]["artifact_digest"] = "wrong"
        elif operation == "future_epoch":
            return rollback_authority_epoch(current_epoch=4, issued_artifact_epochs={"future": 5})
        elif operation != "valid_authority":
            self.fail(f"unknown fixture operation: {operation}")
        return validate_authority_publication(
            canonical,
            projection,
            registry=registry,
            receipts=receipts,
            required_route_ids=["grader"],
            epoch=4,
        )

    def test_all_adversarial_traces_fail_with_named_code_and_positive_control_passes(self) -> None:
        self.assertEqual("adaptive-axes-v2", self.fixture["protocol_id"])
        for case in self.fixture["cases"]:
            with self.subTest(case=case["name"]):
                if "expected_code" in case:
                    with self.assertRaises(P5ProtocolViolation) as raised:
                        self.execute(case["operation"])
                    self.assertEqual(case["expected_code"], raised.exception.code)
                else:
                    result = self.execute(case["operation"])
                    self.assertEqual(case["expected_status"], result["status"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
