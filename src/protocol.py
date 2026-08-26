"""Executable reference semantics for the Sana adaptive debate evidence package.

This module is evidence, not an installed skill implementation.  It deliberately
uses conservative, fail-closed rules so protocol ambiguity is visible in tests.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
import re
from typing import Any, Iterable, Mapping, Sequence


FIXED_PROTOCOL = "fixed-three-v1"
ADAPTIVE_PROTOCOL = "adaptive-axes-v1"
SCHEMA_VERSION = 1

FIXED_LITERAL_RE = re.compile(
    r"(?i)(?<![\w-])(?:three[- ]round|3[- ]round)(?![\w-])|三轮(?:辩论)?"
)
INLINE_PROTOCOL_RE = re.compile(r"(?i)(?<!\S)protocol=([^\s]+)")


class ProtocolViolation(ValueError):
    """Raised when a protocol artifact or transition fails closed."""

    def __init__(self, code: str, detail: str):
        super().__init__(f"{code}: {detail}")
        self.code = code
        self.detail = detail


@dataclass(frozen=True)
class ResolvedProtocol:
    status: str
    selector_version: int = 1
    protocol_id: str | None = None
    schema_version: int | None = None
    resolution_source: tuple[str, ...] = ()
    detail: str | None = None

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["resolution_source"] = list(self.resolution_source)
        value["resolution_hash"] = sha256_json(
            {
                "selector_version": self.selector_version,
                "protocol_id": self.protocol_id,
                "schema_version": self.schema_version,
                "resolution_source": value["resolution_source"],
                "status": self.status,
                "detail": self.detail,
            }
        )
        return value


def canonical_json(value: Any) -> str:
    """Return the E7 canonical JSON representation.

    JSON object keys are sorted, array order is preserved, nulls are preserved,
    UTF-8 characters are not escaped, and insignificant whitespace is omitted.
    """

    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )


def sha256_json(value: Any) -> str:
    return sha256(canonical_json(value).encode("utf-8")).hexdigest()


def resolve_protocol(
    invocation: str,
    structured_protocol: str | None = None,
) -> ResolvedProtocol:
    """Resolve one immutable protocol or return a typed fail-closed outcome.

    Exact structured or ``protocol=...`` selectors are authoritative signals.
    Literal requests for a three-round debate are fixed signals.  Combining a
    fixed and adaptive signal is invalid rather than silently coerced.
    """

    tokens = INLINE_PROTOCOL_RE.findall(invocation)
    selector_tokens: list[tuple[str, str]] = []
    if structured_protocol is not None:
        selector_tokens.append(("structured_protocol", structured_protocol))
    selector_tokens.extend(("inline_protocol", token) for token in tokens)

    unknown = [token for _, token in selector_tokens if token not in {FIXED_PROTOCOL, ADAPTIVE_PROTOCOL}]
    if unknown:
        return ResolvedProtocol(
            status="UNKNOWN_PROTOCOL",
            resolution_source=tuple(source for source, _ in selector_tokens),
            detail=",".join(sorted(set(unknown))),
        )

    fixed_sources = [source for source, token in selector_tokens if token == FIXED_PROTOCOL]
    adaptive_sources = [source for source, token in selector_tokens if token == ADAPTIVE_PROTOCOL]
    if FIXED_LITERAL_RE.search(invocation):
        fixed_sources.append("literal_three_round")

    if fixed_sources and adaptive_sources:
        return ResolvedProtocol(
            status="PROTOCOL_SELECTION_CONFLICT",
            resolution_source=tuple(fixed_sources + adaptive_sources),
            detail="fixed and adaptive signals are both present",
        )
    if fixed_sources:
        return ResolvedProtocol(
            status="RESOLVED",
            protocol_id=FIXED_PROTOCOL,
            schema_version=SCHEMA_VERSION,
            resolution_source=tuple(fixed_sources),
        )
    if adaptive_sources:
        return ResolvedProtocol(
            status="RESOLVED",
            protocol_id=ADAPTIVE_PROTOCOL,
            schema_version=SCHEMA_VERSION,
            resolution_source=tuple(adaptive_sources),
        )
    return ResolvedProtocol(
        status="RESOLVED",
        protocol_id=FIXED_PROTOCOL,
        schema_version=SCHEMA_VERSION,
        resolution_source=("unqualified_default",),
    )


def make_envelope(
    *,
    run_id: str,
    protocol_id: str,
    artifact_type: str,
    sequence: int,
    payload: Mapping[str, Any],
    proposal_ref: str | None = None,
    previous_artifact_hash: str | None = None,
) -> dict[str, Any]:
    envelope: dict[str, Any] = {
        "run_id": run_id,
        "protocol_id": protocol_id,
        "schema_version": SCHEMA_VERSION,
        "artifact_type": artifact_type,
        "sequence": sequence,
        "proposal_ref": proposal_ref,
        "previous_artifact_hash": previous_artifact_hash,
        "payload": dict(payload),
    }
    envelope["artifact_hash"] = sha256_json(envelope)
    return envelope


def validate_envelope(
    envelope: Mapping[str, Any],
    *,
    expected_previous_hash: str | None = None,
) -> None:
    required = {
        "run_id",
        "protocol_id",
        "schema_version",
        "artifact_type",
        "sequence",
        "proposal_ref",
        "previous_artifact_hash",
        "payload",
        "artifact_hash",
    }
    unknown = set(envelope) - required
    missing = required - set(envelope)
    if missing:
        raise ProtocolViolation("MALFORMED_ARTIFACT", f"missing fields: {sorted(missing)}")
    if unknown:
        raise ProtocolViolation("UNKNOWN_FIELD", f"unknown fields: {sorted(unknown)}")
    if envelope["protocol_id"] not in {FIXED_PROTOCOL, ADAPTIVE_PROTOCOL}:
        raise ProtocolViolation("UNKNOWN_PROTOCOL", str(envelope["protocol_id"]))
    if envelope["schema_version"] != SCHEMA_VERSION:
        raise ProtocolViolation("UNKNOWN_SCHEMA_VERSION", str(envelope["schema_version"]))
    if expected_previous_hash != envelope["previous_artifact_hash"]:
        raise ProtocolViolation(
            "HASH_CHAIN_MISMATCH",
            f"expected previous {expected_previous_hash!r}, got {envelope['previous_artifact_hash']!r}",
        )
    unhashed = dict(envelope)
    supplied_hash = unhashed.pop("artifact_hash")
    calculated = sha256_json(unhashed)
    if supplied_hash != calculated:
        raise ProtocolViolation("ARTIFACT_HASH_MISMATCH", "artifact hash does not match canonical payload")


def validate_capability_acks(
    acks: Sequence[Mapping[str, Any]],
    *,
    protocol_id: str,
    schema_version: int,
    required_actors: Iterable[str] = ("root", "proposing_tl", "peer_tl", "chief_architect"),
) -> None:
    by_actor = {ack.get("actor_id"): ack for ack in acks}
    for actor in required_actors:
        ack = by_actor.get(actor)
        if ack is None:
            raise ProtocolViolation("CAPABILITY_MISMATCH", f"missing acknowledgement: {actor}")
        if (
            ack.get("protocol_id") != protocol_id
            or ack.get("schema_version") != schema_version
            or ack.get("supported") is not True
        ):
            raise ProtocolViolation("CAPABILITY_MISMATCH", f"incompatible acknowledgement: {actor}")


def validate_axis_coverage(records: Sequence[Mapping[str, Any]]) -> None:
    """Require exactly one record for each frozen axis A1-A3."""

    axis_ids = [record.get("axis_id") for record in records]
    if len(axis_ids) != 3 or set(axis_ids) != {"A1", "A2", "A3"}:
        raise ProtocolViolation(
            "AXIS_COVERAGE_INVALID",
            f"expected exactly A1,A2,A3; got {axis_ids}",
        )


class CorrectionBudget:
    """Allow one focused correction only for a malformed known artifact."""

    CORRECTABLE = {"MALFORMED_ARTIFACT", "MALFORMED_REQUIRED_OUTPUT", "FORMAT_INVALID"}

    def __init__(self) -> None:
        self._corrections: dict[str, int] = {}
        self.audit: list[dict[str, str | int]] = []

    def request(self, artifact_id: str, error_code: str) -> str:
        if error_code not in self.CORRECTABLE:
            raise ProtocolViolation(
                "NON_RETRYABLE_PROTOCOL_ERROR",
                f"{artifact_id}: {error_code}",
            )
        count = self._corrections.get(artifact_id, 0)
        self.audit.append(
            {"artifact_id": artifact_id, "error_code": error_code, "correction_index": count + 1}
        )
        if count >= 1:
            raise ProtocolViolation(
                "PROTOCOL_INVALID",
                f"focused correction exhausted for {artifact_id}",
            )
        self._corrections[artifact_id] = count + 1
        return "CORRECTION_REQUESTED"


FIXED_TRANSITIONS = {
    ("RESOLVED", "CORE_ACK"): "CORE_ACKED",
    ("CORE_ACKED", "P0"): "P0_VALID",
    ("P0_VALID", "CLOSE_ROUND_1"): "ROUND_1_CLOSED",
    ("ROUND_1_CLOSED", "CLOSE_ROUND_2"): "ROUND_2_CLOSED",
    ("ROUND_2_CLOSED", "CLOSE_ROUND_3"): "ROUND_3_CLOSED",
    ("ROUND_3_CLOSED", "CHIEF_DECIDE"): "CHIEF_DECIDED",
    ("CHIEF_DECIDED", "COMPLETE"): "COMPLETE",
}


class ProtocolStateMachine:
    """Small executable state machine used by E7 golden traces."""

    def __init__(self, protocol_id: str):
        if protocol_id not in {FIXED_PROTOCOL, ADAPTIVE_PROTOCOL}:
            raise ProtocolViolation("UNKNOWN_PROTOCOL", protocol_id)
        self.protocol_id = protocol_id
        self.state = "RESOLVED"
        self.cycles_used = 0
        self.history: list[str] = [self.state]

    def apply(self, event: str) -> str:
        if self.state in {"PROTOCOL_INVALID", "CORE_ROLE_FAILED", "COMPLETE"}:
            raise ProtocolViolation("INVALID_TRANSITION", f"terminal state {self.state}")
        if event in {"PROTOCOL_INVALID", "CORE_ROLE_FAILED"}:
            self.state = event
            self.history.append(self.state)
            return self.state

        if self.protocol_id == FIXED_PROTOCOL:
            target = FIXED_TRANSITIONS.get((self.state, event))
            if target is None:
                raise ProtocolViolation("INVALID_TRANSITION", f"{self.state} + {event}")
            self.state = target
            self.history.append(self.state)
            return self.state

        target = self._adaptive_target(event)
        self.state = target
        self.history.append(self.state)
        return self.state

    def _adaptive_target(self, event: str) -> str:
        simple = {
            ("RESOLVED", "CORE_ACK"): "CORE_ACKED",
            ("CORE_ACKED", "P0"): "P0_VALID",
            ("P0_VALID", "ATTACK_MAP"): "ATTACK_MAP_VALID",
            ("ATTACK_MAP_VALID", "START_TERMINAL"): "TERMINAL_RECONCILING",
            ("CYCLE_CLOSED", "START_TERMINAL"): "TERMINAL_RECONCILING",
            ("TERMINAL_RECONCILING", "TERMINAL_VALID"): "TERMINAL_VALID",
            ("TERMINAL_VALID", "CHIEF_SCAN"): "CHIEF_SCAN_FROZEN",
            ("CHIEF_SCAN_FROZEN", "CHIEF_DECIDE"): "CHIEF_RECONCILED_AND_DECIDED",
            ("CHIEF_RECONCILED_AND_DECIDED", "COMPLETE"): "COMPLETE",
        }
        if event == "OPEN_CYCLE" and self.state in {
            "ATTACK_MAP_VALID",
            "CYCLE_CLOSED",
            "TERMINAL_RECONCILING",
        }:
            if self.cycles_used >= 3:
                raise ProtocolViolation("CYCLE_BUDGET_EXHAUSTED", "fourth cycle is forbidden")
            return "CYCLE_OPEN"
        if event == "CLOSE_CYCLE" and self.state == "CYCLE_OPEN":
            self.cycles_used += 1
            return "CYCLE_CLOSED"
        target = simple.get((self.state, event))
        if target is None:
            raise ProtocolViolation("INVALID_TRANSITION", f"{self.state} + {event}")
        return target


ISSUE_EFFECT_FIELDS = (
    "axis_id",
    "mechanism_id",
    "invariant_ids",
    "affected_behavior_ids",
    "risk_ids",
    "evidence_request_ids",
    "failure_signature",
    "falsifier_id",
)


def _normalized_list(value: Any) -> tuple[str, ...]:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ProtocolViolation("MALFORMED_ISSUE", "expected a list of strings")
    return tuple(sorted(value))


def issue_effect_key(issue: Mapping[str, Any]) -> str:
    missing = [field for field in ISSUE_EFFECT_FIELDS if field not in issue]
    if missing:
        raise ProtocolViolation("EQUIVALENCE_INDETERMINATE", f"missing issue fields: {missing}")
    signature = issue["failure_signature"]
    if not isinstance(signature, Mapping) or set(signature) != {
        "precondition_class",
        "event_class",
        "observable_failure_class",
    }:
        raise ProtocolViolation("EQUIVALENCE_INDETERMINATE", "incomplete failure signature")
    key = {
        "axis_id": issue["axis_id"],
        "mechanism_id": issue["mechanism_id"],
        "invariant_ids": _normalized_list(issue["invariant_ids"]),
        "affected_behavior_ids": _normalized_list(issue["affected_behavior_ids"]),
        "risk_ids": _normalized_list(issue["risk_ids"]),
        "evidence_request_ids": _normalized_list(issue["evidence_request_ids"]),
        "failure_signature": dict(signature),
        "falsifier_id": issue["falsifier_id"],
    }
    return sha256_json(key)


def classify_issue_equivalence(
    predecessor: Mapping[str, Any],
    candidate: Mapping[str, Any],
) -> str:
    """Return DUPLICATE, NEW_ISSUE, or fail closed as indeterminate.

    Exact structured effect equality is necessary but not sufficient.  A later
    proposal can be called duplicate only when all intervening diffs were
    reviewed and explicitly have no dependency impact on the issue.
    """

    previous_key = issue_effect_key(predecessor)
    candidate_key = issue_effect_key(candidate)
    if previous_key != candidate_key:
        return "NEW_ISSUE"
    if candidate.get("predecessor_issue_id") != predecessor.get("issue_id"):
        raise ProtocolViolation("EQUIVALENCE_INDETERMINATE", "canonical predecessor is missing")
    impact = candidate.get("proposal_dependency_impact")
    if impact not in {"NONE", "DIRECT", "TRANSITIVE", "UNKNOWN"}:
        raise ProtocolViolation("EQUIVALENCE_INDETERMINATE", "dependency impact is missing")
    if impact in {"DIRECT", "TRANSITIVE"}:
        return "NEW_ISSUE"
    if impact == "UNKNOWN":
        raise ProtocolViolation("EQUIVALENCE_INDETERMINATE", "proposal dependency is unknown")
    if predecessor.get("proposal_ref") != candidate.get("proposal_ref"):
        reviewed = candidate.get("reviewed_diff_ids")
        if not isinstance(reviewed, list) or not reviewed:
            raise ProtocolViolation("EQUIVALENCE_INDETERMINATE", "changed proposal lacks reviewed diffs")
    return "DUPLICATE"


def reconcile_axis(
    *,
    axis_id: str,
    prior_proposal_ref: str,
    terminal_proposal_ref: str,
    diffs: Sequence[Mapping[str, Any]],
    cycles_used: int,
) -> dict[str, Any]:
    """Reference terminal reconciliation used by T1-T4."""

    if cycles_used < 0 or cycles_used > 3:
        return {"status": "PROTOCOL_INVALID", "reason": "invalid cycle count"}
    cursor = prior_proposal_ref
    reviewed: list[str] = []
    impacts: list[Mapping[str, Any]] = []
    for diff in diffs:
        required = {"diff_id", "from_ref", "to_ref", "axis_impacts"}
        if not required.issubset(diff):
            return {"status": "PROTOCOL_INVALID", "reason": "malformed diff"}
        if diff["from_ref"] != cursor:
            return {"status": "PROTOCOL_INVALID", "reason": "non-contiguous diff chain"}
        if not isinstance(diff["axis_impacts"], list):
            return {"status": "PROTOCOL_INVALID", "reason": "malformed axis impacts"}
        cursor = str(diff["to_ref"])
        reviewed.append(str(diff["diff_id"]))
        impacts.extend(item for item in diff["axis_impacts"] if item.get("axis_id") == axis_id)
    if cursor != terminal_proposal_ref:
        return {"status": "PROTOCOL_INVALID", "reason": "terminal proposal mismatch"}

    material = [item for item in impacts if item.get("material_issue") is not None]
    unknown = [
        item
        for item in impacts
        if item.get("impact") not in {"NONE", "DIRECT", "TRANSITIVE"}
    ]
    if unknown:
        return {"status": "PROTOCOL_INVALID", "reason": "unknown dependency impact"}
    if material:
        finding = material[-1]["material_issue"]
        return {
            "status": "QUEUED" if cycles_used < 3 else "OPEN_BUDGET_EXHAUSTED",
            "axis_id": axis_id,
            "terminal_proposal_ref": terminal_proposal_ref,
            "reviewed_diff_ids": reviewed,
            "finding": finding,
        }
    if any(item.get("impact") in {"DIRECT", "TRANSITIVE"} for item in impacts):
        return {
            "status": "TERMINAL_REINSPECTED_NO_MATERIAL",
            "axis_id": axis_id,
            "terminal_proposal_ref": terminal_proposal_ref,
            "reviewed_diff_ids": reviewed,
        }
    return {
        "status": "TERMINAL_EQUIVALENT",
        "axis_id": axis_id,
        "terminal_proposal_ref": terminal_proposal_ref,
        "reviewed_diff_ids": reviewed,
    }
