"""Reference semantics for the Sana debate core startup transaction.

This module models the manager-side PREPARE/COMMIT barrier. It does not spawn
agents and grants no authority; the host remains responsible for creating real
threads and reporting observable outcomes.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
import re
from typing import Any, Mapping


STARTUP_PROTOCOL = "core-two-phase-v1"
CONTINUATION_SCHEMA = "sana.debate-continuation.v1"
CORE_ROLES = ("proposing_tl", "peer_tl", "chief_architect")
SERIAL_PREPARE_ORDER = ("chief_architect", "peer_tl", "proposing_tl")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


class StartupViolation(ValueError):
    """Raised when a manager attempts an unsafe startup transition."""

    def __init__(self, code: str, detail: str):
        super().__init__(f"{code}: {detail}")
        self.code = code
        self.detail = detail


@dataclass(frozen=True)
class CoreRoleAttempt:
    role: str
    status: str = "NOT_ATTEMPTED"
    thread_id: str | None = None
    error_code: str | None = None


def _canonical_json(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )


def _packet_hash(value: Mapping[str, Any]) -> str:
    return sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def _require_sha256(name: str, value: str) -> None:
    if not SHA256_RE.fullmatch(value):
        raise StartupViolation("INVALID_FROZEN_HASH", f"{name} is not lowercase SHA-256")


class CoreStartupTransaction:
    """Fail-closed two-phase barrier for the three required debate roles."""

    def __init__(
        self,
        *,
        run_id: str,
        frame_sha256: str,
        evidence_ledger_sha256: str,
        routing_manifest_sha256: str,
    ) -> None:
        if not run_id:
            raise StartupViolation("INVALID_RUN_ID", "run_id is required")
        frozen = {
            "frame_sha256": frame_sha256,
            "evidence_ledger_sha256": evidence_ledger_sha256,
            "routing_manifest_sha256": routing_manifest_sha256,
        }
        for name, value in frozen.items():
            _require_sha256(name, value)
        self.run_id = run_id
        self.frozen_inputs = frozen
        self.state = "PREPARING"
        self.attempts = {role: CoreRoleAttempt(role=role) for role in CORE_ROLES}
        self.substantive_exposure_roles: list[str] = []

    def record_ready(self, role: str, thread_id: str) -> str:
        self._require_preparing("record readiness")
        self._require_role(role)
        if not thread_id:
            raise StartupViolation("INVALID_THREAD_ID", f"{role} thread_id is required")
        if self.attempts[role].status != "NOT_ATTEMPTED":
            raise StartupViolation("DUPLICATE_CORE_ATTEMPT", role)
        expected_role = self.next_prepare_role()
        if role != expected_role:
            raise StartupViolation(
                "PREPARE_ORDER_VIOLATION",
                f"expected {expected_role}, received {role}",
            )
        self.attempts[role] = CoreRoleAttempt(
            role=role,
            status="READY",
            thread_id=thread_id,
        )
        if all(attempt.status == "READY" for attempt in self.attempts.values()):
            self.state = "PREPARED"
        return self.state

    def record_capacity_failure(
        self,
        role: str,
        *,
        error_code: str = "THREAD_LIMIT_REACHED",
    ) -> str:
        self._require_preparing("record capacity failure")
        self._require_role(role)
        if self.attempts[role].status != "NOT_ATTEMPTED":
            raise StartupViolation("DUPLICATE_CORE_ATTEMPT", role)
        if not error_code:
            raise StartupViolation("INVALID_CAPACITY_ERROR", "error_code is required")
        expected_role = self.next_prepare_role()
        if role != expected_role:
            raise StartupViolation(
                "PREPARE_ORDER_VIOLATION",
                f"expected {expected_role}, received {role}",
            )
        self.attempts[role] = CoreRoleAttempt(
            role=role,
            status="THREAD_LIMIT_REACHED",
            error_code=error_code,
        )
        self.state = "WAITING_FOR_CORE_CAPACITY"
        return self.state

    def record_substantive_exposure(self, role: str) -> str:
        self._require_role(role)
        if role not in self.substantive_exposure_roles:
            self.substantive_exposure_roles.append(role)
        if self.state != "RUNNING":
            self.state = "ABORTED_PARTIAL_EXPOSURE"
        return self.state

    def commit(self) -> str:
        if self.state != "PREPARED":
            raise StartupViolation(
                "STARTUP_NOT_PREPARED",
                f"cannot commit from {self.state}",
            )
        self.state = "RUNNING"
        return self.state

    def next_prepare_role(self) -> str | None:
        """Return the next role in the Chief-first serial PREPARE schedule."""

        if self.state == "PREPARED":
            return None
        self._require_preparing("select next PREPARE role")
        for role in SERIAL_PREPARE_ORDER:
            if self.attempts[role].status == "NOT_ATTEMPTED":
                return role
        return None

    def continuation_packet(self) -> dict[str, Any]:
        if self.state not in {"WAITING_FOR_CORE_CAPACITY", "ABORTED_PARTIAL_EXPOSURE"}:
            raise StartupViolation(
                "CONTINUATION_NOT_AVAILABLE",
                f"state {self.state} is not a failed startup",
            )
        packet: dict[str, Any] = {
            "schema": CONTINUATION_SCHEMA,
            "startup_protocol": STARTUP_PROTOCOL,
            "run_id": self.run_id,
            "state": self.state,
            "frozen_inputs": dict(self.frozen_inputs),
            "core_roles": {
                role: asdict(self.attempts[role])
                for role in CORE_ROLES
            },
            "substantive_exposure_roles": list(self.substantive_exposure_roles),
            "substantive_artifacts_admissible": False,
            "resume_requirements": {
                "parent_run_id": self.run_id,
                "new_run_required": True,
                "fresh_core_threads_required": True,
                "revalidate_frozen_hashes": True,
                "reuse_partial_threads": False,
                "observed_capacity_change_required": True,
            },
        }
        packet["packet_hash"] = _packet_hash(packet)
        return packet

    def _require_preparing(self, action: str) -> None:
        if self.state != "PREPARING":
            raise StartupViolation(
                "STARTUP_TERMINAL_OR_PREPARED",
                f"cannot {action} from {self.state}",
            )

    @staticmethod
    def _require_role(role: str) -> None:
        if role not in CORE_ROLES:
            raise StartupViolation("UNKNOWN_CORE_ROLE", role)


def validate_continuation_packet(packet: Mapping[str, Any]) -> None:
    """Validate semantic constraints not conveniently expressed by JSON Schema."""

    expected = {
        "schema",
        "startup_protocol",
        "run_id",
        "state",
        "frozen_inputs",
        "core_roles",
        "substantive_exposure_roles",
        "substantive_artifacts_admissible",
        "resume_requirements",
        "packet_hash",
    }
    if set(packet) != expected:
        raise StartupViolation("MALFORMED_CONTINUATION", "top-level fields differ")
    if packet["schema"] != CONTINUATION_SCHEMA or packet["startup_protocol"] != STARTUP_PROTOCOL:
        raise StartupViolation("UNKNOWN_CONTINUATION_PROFILE", "schema or startup protocol differs")
    if packet["state"] not in {"WAITING_FOR_CORE_CAPACITY", "ABORTED_PARTIAL_EXPOSURE"}:
        raise StartupViolation("INVALID_CONTINUATION_STATE", str(packet["state"]))
    unhashed = dict(packet)
    supplied_hash = unhashed.pop("packet_hash")
    if supplied_hash != _packet_hash(unhashed):
        raise StartupViolation("CONTINUATION_HASH_MISMATCH", "packet hash differs")
    if packet["substantive_artifacts_admissible"] is not False:
        raise StartupViolation("CONTINUATION_WIDENS_AUTHORITY", "artifacts must be inadmissible")
    if set(packet["core_roles"]) != set(CORE_ROLES):
        raise StartupViolation("MALFORMED_CONTINUATION", "core role set differs")
    for name, value in packet["frozen_inputs"].items():
        _require_sha256(name, value)
    for role in CORE_ROLES:
        attempt = packet["core_roles"][role]
        if set(attempt) != {"role", "status", "thread_id", "error_code"}:
            raise StartupViolation("MALFORMED_CONTINUATION", f"{role} attempt fields differ")
        if attempt["role"] != role:
            raise StartupViolation("MALFORMED_CONTINUATION", f"{role} identity differs")
        status = attempt["status"]
        if status == "READY":
            if not attempt["thread_id"] or attempt["error_code"] is not None:
                raise StartupViolation("MALFORMED_CONTINUATION", f"{role} READY fields differ")
        elif status == "THREAD_LIMIT_REACHED":
            if attempt["thread_id"] is not None or not attempt["error_code"]:
                raise StartupViolation("MALFORMED_CONTINUATION", f"{role} failure fields differ")
        elif status == "NOT_ATTEMPTED":
            if attempt["thread_id"] is not None or attempt["error_code"] is not None:
                raise StartupViolation("MALFORMED_CONTINUATION", f"{role} idle fields differ")
        else:
            raise StartupViolation("MALFORMED_CONTINUATION", f"{role} status differs")
    resume = packet["resume_requirements"]
    if (
        resume.get("parent_run_id") != packet["run_id"]
        or resume.get("new_run_required") is not True
        or resume.get("fresh_core_threads_required") is not True
        or resume.get("revalidate_frozen_hashes") is not True
        or resume.get("reuse_partial_threads") is not False
        or resume.get("observed_capacity_change_required") is not True
    ):
        raise StartupViolation("CONTINUATION_WIDENS_AUTHORITY", "resume requirements differ")
