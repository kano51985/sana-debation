"""Deterministic P5 baseline-delta, finding, and authority reference semantics."""

from __future__ import annotations

import copy
import hashlib
import json
from typing import Any, Iterable, Mapping, Sequence


P5_PROTOCOL = "adaptive-axes-v2"
P5_CONTRACT = "baseline-delta-ledger-v1"
P5_SCHEMA_VERSION = 1

CLASSIFICATIONS = {"NON_DECISION_RELEVANT", "DECISION_RELEVANT", "UNCERTAIN"}
ATTESTATIONS = {"NON_RELEVANT", "RELEVANT", "UNRESOLVED"}
CHANGE_KINDS = {"ADDITIVE", "REMOVED", "CHANGED"}
FINDING_STATUSES = {"OPEN", "RESOLVED", "REBUTTED", "ACCEPTED_RISK", "INDETERMINATE"}
PRECONDITION_PROVENANCES = {"SUPPLIED_FACT", "VERIFIED_EVIDENCE", "HYPOTHETICAL"}


class P5ProtocolViolation(ValueError):
    def __init__(self, code: str, detail: str = "") -> None:
        self.code = code
        self.detail = detail
        super().__init__(f"{code}: {detail}" if detail else code)


def _canonical_json(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )


def _sha256(value: Any) -> str:
    return hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def _stable_id(prefix: str, value: Any) -> str:
    return f"{prefix}-{_sha256(value)[:24]}"


def capture_baseline(literal_content: Any) -> dict[str, Any]:
    """Capture the literal supplied baseline before any proposer repair."""

    return {
        "baseline_ref": "B0",
        "content_hash": _sha256(literal_content),
        "literal_content": copy.deepcopy(literal_content),
    }


def make_delta_candidate(
    *,
    baseline: Mapping[str, Any],
    proposal_ref: str,
    decision_surface: str,
    change_kind: str,
    before: Any,
    after: Any,
    classification: str,
    rationale: str,
    supplied_behavior_change: bool,
    precondition_provenance: str | None = None,
) -> dict[str, Any]:
    """Admit a non-identical B0/Pn delta before semantic exclusion is possible."""

    if change_kind not in CHANGE_KINDS:
        raise P5ProtocolViolation("UNKNOWN_CHANGE_KIND", change_kind)
    if classification not in CLASSIFICATIONS:
        raise P5ProtocolViolation("UNKNOWN_DELTA_CLASSIFICATION", classification)
    if precondition_provenance is None:
        precondition_provenance = (
            "SUPPLIED_FACT" if supplied_behavior_change else "VERIFIED_EVIDENCE"
        )
    if precondition_provenance not in PRECONDITION_PROVENANCES:
        raise P5ProtocolViolation(
            "UNKNOWN_PRECONDITION_PROVENANCE", precondition_provenance
        )
    if not proposal_ref or not decision_surface or not rationale:
        raise P5ProtocolViolation("DELTA_RECORD_INCOMPLETE")
    if before == after:
        raise P5ProtocolViolation("IDENTICAL_DELTA_NOT_ADMITTED")
    identity = {
        "baseline_hash": baseline.get("content_hash"),
        "proposal_ref": proposal_ref,
        "decision_surface": decision_surface,
        "change_kind": change_kind,
        "before": before,
        "after": after,
        "provenance_origin": "BASELINE_DELTA",
    }
    return {
        "candidate_id": _stable_id("C", identity),
        "baseline_ref": baseline.get("baseline_ref"),
        "baseline_hash": baseline.get("content_hash"),
        "proposal_ref": proposal_ref,
        "decision_surface": decision_surface,
        "change_kind": change_kind,
        "before": copy.deepcopy(before),
        "after": copy.deepcopy(after),
        "classification": classification,
        "precondition_provenance": precondition_provenance,
        "provenance_origin": "BASELINE_DELTA",
        "rationale": rationale,
        "supplied_behavior_change": bool(supplied_behavior_change),
        "peer_attestation": None,
        "peer_attestation_basis": None,
        "finding_id": None,
    }


def attest_candidate(
    candidate: Mapping[str, Any], attestation: str, basis: str
) -> dict[str, Any]:
    if attestation not in ATTESTATIONS:
        raise P5ProtocolViolation("UNKNOWN_PEER_ATTESTATION", attestation)
    if not basis:
        raise P5ProtocolViolation("CLASSIFICATION_ATTESTATION_MISSING")
    result = copy.deepcopy(dict(candidate))
    result["peer_attestation"] = attestation
    result["peer_attestation_basis"] = basis
    return result


def link_candidate_to_finding(
    candidate: dict[str, Any],
    *,
    axis: str,
    mechanism: str,
    issue_statement: str,
    failure_trace: Mapping[str, str],
    falsifier: str,
) -> dict[str, Any]:
    required_trace = {"precondition", "event", "observable_failure"}
    if set(failure_trace) != required_trace or not all(failure_trace.values()):
        raise P5ProtocolViolation("CHALLENGE_MECHANISM_MISSING")
    if not all((axis, mechanism, issue_statement, falsifier)):
        raise P5ProtocolViolation("FINDING_RECORD_INCOMPLETE")
    identity = {
        "baseline_hash": candidate.get("baseline_hash"),
        "decision_surface": candidate.get("decision_surface"),
        "provenance_origin": candidate.get("provenance_origin"),
        "issue_statement": issue_statement,
    }
    finding_id = _stable_id("F", identity)
    candidate["finding_id"] = finding_id
    return {
        "finding_id": finding_id,
        "candidate_id": candidate["candidate_id"],
        "baseline_ref": candidate["baseline_ref"],
        "baseline_hash": candidate["baseline_hash"],
        "proposal_ref": candidate["proposal_ref"],
        "provenance_origin": candidate["provenance_origin"],
        "precondition_provenance": candidate["precondition_provenance"],
        "axis": axis,
        "mechanism": mechanism,
        "issue_statement": issue_statement,
        "failure_trace": dict(failure_trace),
        "falsifier": falsifier,
        "status": "OPEN",
        "response_status": None,
        "response_basis": None,
        "peer_disposition": None,
        "peer_verification_basis": None,
    }


def make_peer_discovery_finding(
    *,
    baseline: Mapping[str, Any],
    proposal_ref: str,
    precondition_provenance: str,
    axis: str,
    mechanism: str,
    issue_statement: str,
    failure_trace: Mapping[str, str],
    falsifier: str,
) -> dict[str, Any]:
    """Admit a supplied/verified conflict independently discovered by Peer.

    This path is deliberately candidate-free: no B0-to-P0 proposal mutation is required for a
    literal B0 defect to exist. Hypotheticals remain limitations and cannot become findings here.
    """

    if precondition_provenance not in {"SUPPLIED_FACT", "VERIFIED_EVIDENCE"}:
        raise P5ProtocolViolation(
            "PEER_DISCOVERY_PROVENANCE_INVALID", precondition_provenance
        )
    required_trace = {"precondition", "event", "observable_failure"}
    if set(failure_trace) != required_trace or not all(failure_trace.values()):
        raise P5ProtocolViolation("CHALLENGE_MECHANISM_MISSING")
    if not all((proposal_ref, axis, mechanism, issue_statement, falsifier)):
        raise P5ProtocolViolation("FINDING_RECORD_INCOMPLETE")
    identity = {
        "baseline_hash": baseline.get("content_hash"),
        "proposal_ref": proposal_ref,
        "provenance_origin": "PEER_DISCOVERY",
        "precondition_provenance": precondition_provenance,
        "axis": axis,
        "mechanism": mechanism,
        "issue_statement": issue_statement,
    }
    return {
        "finding_id": _stable_id("F", identity),
        "candidate_id": None,
        "baseline_ref": baseline.get("baseline_ref"),
        "baseline_hash": baseline.get("content_hash"),
        "proposal_ref": proposal_ref,
        "provenance_origin": "PEER_DISCOVERY",
        "precondition_provenance": precondition_provenance,
        "axis": axis,
        "mechanism": mechanism,
        "issue_statement": issue_statement,
        "failure_trace": dict(failure_trace),
        "falsifier": falsifier,
        "status": "OPEN",
        "response_status": None,
        "response_basis": None,
        "peer_disposition": None,
        "peer_verification_basis": None,
    }


def _is_generic_closure(text: str) -> bool:
    normalized = " ".join(text.casefold().split())
    markers = (
        "already fixed",
        "looks addressed",
        "addressed by p0",
        "issue addressed",
        "fixed in p0",
    )
    return (
        len(normalized.split()) < 4
        or any(marker in normalized for marker in markers)
    )


def close_finding(
    finding: Mapping[str, Any],
    *,
    status: str,
    response_status: str,
    response_basis: str,
    peer_disposition: str,
    peer_verification_basis: str,
) -> dict[str, Any]:
    if status not in FINDING_STATUSES:
        raise P5ProtocolViolation("UNKNOWN_FINDING_STATUS", status)
    if response_status not in {"accepted", "rejected with evidence", "unresolved"}:
        raise P5ProtocolViolation("UNKNOWN_RESPONSE_STATUS", response_status)
    if _is_generic_closure(response_basis):
        raise P5ProtocolViolation("RESPONSE_EVIDENCE_MISSING")
    if _is_generic_closure(peer_verification_basis):
        raise P5ProtocolViolation("PEER_CLOSURE_UNSUPPORTED")
    if " ".join(response_basis.casefold().split()) == " ".join(
        peer_verification_basis.casefold().split()
    ):
        raise P5ProtocolViolation("PEER_CLOSURE_COPIED")
    if peer_disposition not in {"accepted", "modified", "rejected", "unresolved"}:
        raise P5ProtocolViolation("UNKNOWN_PEER_DISPOSITION", peer_disposition)
    result = copy.deepcopy(dict(finding))
    result.update(
        {
            "status": status,
            "response_status": response_status,
            "response_basis": response_basis,
            "peer_disposition": peer_disposition,
            "peer_verification_basis": peer_verification_basis,
        }
    )
    return result


def _candidate_is_routed(candidate: Mapping[str, Any]) -> bool:
    return candidate.get("peer_attestation") in {"RELEVANT", "UNRESOLVED"} or candidate.get(
        "classification"
    ) in {"DECISION_RELEVANT", "UNCERTAIN"}


def route_delta_candidates(
    candidates: Sequence[Mapping[str, Any]], *, supplied_conflict_ids: Sequence[str]
) -> dict[str, Any]:
    supplied = set(supplied_conflict_ids)
    routed: list[str] = []
    for candidate in candidates:
        candidate_id = candidate.get("candidate_id")
        attestation = candidate.get("peer_attestation")
        if attestation not in ATTESTATIONS or not candidate.get("peer_attestation_basis"):
            raise P5ProtocolViolation("CLASSIFICATION_ATTESTATION_MISSING", str(candidate_id))
        if (
            candidate.get("supplied_behavior_change")
            and candidate_id in supplied
            and attestation == "NON_RELEVANT"
        ):
            raise P5ProtocolViolation("SUPPLIED_CHANGE_MISCLASSIFIED", str(candidate_id))
        if _candidate_is_routed(candidate) or candidate_id in supplied:
            routed.append(str(candidate_id))
    return {
        "candidate_count": len(candidates),
        "routed_candidate_ids": routed,
        "zero_cycle_eligible": not routed,
        "minimum_substantive_cycles": 1 if routed else 0,
    }


def validate_finding_batch(findings: Sequence[Mapping[str, Any]]) -> None:
    if not findings:
        raise P5ProtocolViolation("SUBSTANTIVE_CLOSURE_INCOMPLETE")
    causal_keys = {
        (
            finding.get("mechanism"),
            finding.get("failure_trace", {}).get("precondition"),
            finding.get("failure_trace", {}).get("event"),
            finding.get("falsifier"),
        )
        for finding in findings
    }
    if len(causal_keys) != 1:
        raise P5ProtocolViolation("BATCH_CAUSALITY_UNJUSTIFIED")


def reconcile_terminal(
    *,
    candidates: Sequence[Mapping[str, Any]],
    findings: Sequence[Mapping[str, Any]],
    cycles_used: int,
    chief_disposition: str,
) -> dict[str, Any]:
    if cycles_used < 0 or cycles_used > 3:
        raise P5ProtocolViolation("CYCLE_COUNT_INVALID")
    finding_by_id = {finding.get("finding_id"): finding for finding in findings}
    if len(finding_by_id) != len(findings):
        raise P5ProtocolViolation("FINDING_ID_COLLISION")
    candidate_by_id = {
        candidate.get("candidate_id"): candidate for candidate in candidates
    }
    routed_count = 0
    for candidate in candidates:
        if candidate.get("peer_attestation") not in ATTESTATIONS:
            raise P5ProtocolViolation("CLASSIFICATION_ATTESTATION_MISSING")
        if _candidate_is_routed(candidate):
            routed_count += 1
            finding_id = candidate.get("finding_id")
            if not finding_id or finding_id not in finding_by_id:
                raise P5ProtocolViolation("CANDIDATE_FINDING_LINK_MISSING")
            finding = finding_by_id[finding_id]
            if finding.get("candidate_id") != candidate.get("candidate_id"):
                raise P5ProtocolViolation("CANDIDATE_FINDING_LINK_MISSING")
    for finding in findings:
        origin = finding.get("provenance_origin")
        candidate_id = finding.get("candidate_id")
        if origin == "PEER_DISCOVERY":
            if candidate_id is not None or finding.get("precondition_provenance") not in {
                "SUPPLIED_FACT",
                "VERIFIED_EVIDENCE",
            }:
                raise P5ProtocolViolation("PEER_DISCOVERY_LINK_INVALID")
            routed_count += 1
        elif origin == "BASELINE_DELTA":
            if candidate_id not in candidate_by_id:
                raise P5ProtocolViolation("CANDIDATE_FINDING_LINK_MISSING")
        else:
            raise P5ProtocolViolation("UNKNOWN_FINDING_PROVENANCE", str(origin))
    if routed_count and cycles_used == 0:
        raise P5ProtocolViolation("ZERO_CYCLE_RECONCILIATION_INVALID")
    for finding in findings:
        if not all(
            finding.get(field)
            for field in (
                "response_status",
                "response_basis",
                "peer_disposition",
                "peer_verification_basis",
            )
        ):
            raise P5ProtocolViolation("SUBSTANTIVE_CLOSURE_INCOMPLETE")
        if chief_disposition == "APPROVE" and finding.get("status") in {
            "OPEN",
            "INDETERMINATE",
        }:
            raise P5ProtocolViolation("OPEN_FINDING_APPROVED")
    return {
        "status": "TERMINAL_VALID",
        "detected_finding_ids": sorted(str(key) for key in finding_by_id),
        "cycles_used": cycles_used,
        "chief_disposition": chief_disposition,
    }


def validate_projection(
    canonical_artifact: Mapping[str, Any], projection: Mapping[str, Any]
) -> dict[str, Any]:
    if projection.get("canonical_parent_id") != canonical_artifact.get("artifact_id"):
        raise P5ProtocolViolation("PROJECTION_LOSS_UNDECLARED")
    canonical_findings = set(canonical_artifact.get("detected_finding_ids", []))
    projected_findings = set(projection.get("detected_finding_ids", []))
    if canonical_findings != projected_findings:
        raise P5ProtocolViolation("PROJECTION_NON_INJECTIVE")
    if projection.get("chief_disposition") != canonical_artifact.get("chief_disposition"):
        raise P5ProtocolViolation("PROJECTION_NON_INJECTIVE")
    if set(projection.get("open_risk_ids", [])) != set(
        canonical_artifact.get("open_risk_ids", [])
    ):
        raise P5ProtocolViolation("PROJECTION_NON_INJECTIVE")
    if projection.get("loss_manifest"):
        raise P5ProtocolViolation("PROJECTION_LOSS_UNDECLARED")
    return {"status": "PROJECTION_VALID", "artifact_digest": _sha256(canonical_artifact)}


def validate_authority_publication(
    canonical_artifact: Mapping[str, Any],
    projection: Mapping[str, Any],
    *,
    registry: Sequence[Mapping[str, Any]],
    receipts: Sequence[Mapping[str, Any]],
    required_route_ids: Sequence[str],
    epoch: int,
) -> dict[str, Any]:
    projection_result = validate_projection(canonical_artifact, projection)
    route_by_id = {route.get("route_id"): route for route in registry}
    for route_id in required_route_ids:
        if route_id not in route_by_id:
            raise P5ProtocolViolation("AUTHORITY_ROUTE_UNREGISTERED", route_id)
        route = route_by_id[route_id]
        if not route.get("authority_capability"):
            raise P5ProtocolViolation("AUTHORITY_BYPASS_ATTEMPT", route_id)
        if route.get("epoch") != epoch:
            raise P5ProtocolViolation("AUTHORITY_EPOCH_MISMATCH", route_id)
    receipt_by_id = {receipt.get("route_id"): receipt for receipt in receipts}
    for route_id in required_route_ids:
        if route_id not in receipt_by_id:
            raise P5ProtocolViolation("CONSUMER_ACK_MISSING", route_id)
        receipt = receipt_by_id[route_id]
        if (
            receipt.get("epoch") != epoch
            or receipt.get("artifact_digest") != projection_result["artifact_digest"]
            or set(receipt.get("detected_finding_ids", []))
            != set(canonical_artifact.get("detected_finding_ids", []))
            or receipt.get("chief_disposition") != canonical_artifact.get("chief_disposition")
        ):
            raise P5ProtocolViolation("CONSUMER_RECEIPT_MISMATCH", route_id)
    return {
        "status": "AUTHORIZED",
        "epoch": epoch,
        "artifact_digest": projection_result["artifact_digest"],
        "authorized_route_ids": sorted(required_route_ids),
    }


def rollback_authority_epoch(
    *, current_epoch: int, issued_artifact_epochs: Mapping[str, int]
) -> dict[str, Any]:
    if current_epoch < 0:
        raise P5ProtocolViolation("AUTHORITY_EPOCH_MISMATCH")
    if any(epoch > current_epoch for epoch in issued_artifact_epochs.values()):
        raise P5ProtocolViolation("HISTORICAL_INTERPRETATION_MISMATCH")
    return {
        "prior_epoch": current_epoch,
        "new_epoch": current_epoch + 1,
        "issued_artifact_epochs": copy.deepcopy(dict(issued_artifact_epochs)),
    }
