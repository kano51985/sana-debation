"""Non-authorizing ER-A3-MIN v2 semantic-profile reader and lifecycle router.

V2 defines one closed product-preference profile.  It never resolves design sources, publishes a
source instance, evaluates compatibility, grants authority, or performs acquisition.  The v1
validator remains byte-identical and is reachable here only through an explicit audit route.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Final

from src.e14_c1a_er_a3_min import verify_package as _verify_v1_package


CONTRACT_VERSION: Final = 2
CONTRACT_STATUS: Final = "DESIGN_CONTRACT_AVAILABLE"
LINEAGE_RELATION: Final = "HISTORICAL_SUCCESSOR_ONLY"
PROFILE_ID: Final = "C1A_CANDIDATE_A_PREFERENCE_PROFILE"
PROFILE_VERSION: Final = 1
_ACQUISITION_TOPOLOGY: Final = "LOCAL_NODE_BY_VALUE_PLUS_SINGLE_REMOTE_OPAQUE_BODY"
_HTTP_ATTEMPT_PROFILE: Final = "ONE_DNS_ONE_TCP_ONE_TLS_ONE_GET_IDENTITY_NO_RETRY"
PREFERENCE_CLASS: Final = "PRODUCT_DESIGN_PREFERENCE"
CUSTODY_SEMANTICS: Final = "OBSERVED_CUSTODY_ONLY"
SERIALIZATION_SEMANTICS: Final = "J1_SERIALIZATION_ONLY"
COMPATIBILITY: Final = "UNASSESSED"
AUTHORITY_EFFECT: Final = "NONE"
FIXTURE_CLASSIFICATION: Final = "CONFORMANCE_FIXTURE_NON_NORMATIVE"
V1_STATUS: Final = "RETIRED_UNISSUED"
V1_AUDIT_PURPOSE: Final = "AUDIT_REPRODUCTION"
V2_DESIGN_PURPOSE: Final = "NORMAL_DESIGN_CONTRACT_USE"
MAX_RAW_BYTES: Final = 8_192

FAILURE_CODES: Final = (
    "ER_A3_V2_RAW_TOO_LARGE",
    "ER_A3_V2_JSON_BOM",
    "ER_A3_V2_JSON_INVALID_UTF8",
    "ER_A3_V2_JSON_INVALID",
    "ER_A3_V2_JSON_DUPLICATE_KEY",
    "ER_A3_V2_PROFILE_FIELD_SET",
    "ER_A3_V2_PROFILE_ID_UNSUPPORTED",
    "ER_A3_V2_PROFILE_VERSION_UNSUPPORTED",
    "ER_A3_V2_PROFILE_VALUE_INVALID",
    "ER_A3_CONTRACT_VERSION_UNSUPPORTED",
    "ER_A3_CONTRACT_PURPOSE_UNSUPPORTED",
    "ER_A3_V1_RETIRED_UNISSUED",
    "ER_A3_REGISTERED_SOURCE_INSTANCE_ABSENT",
)

__all__ = (
    "AUTHORITY_EFFECT",
    "COMPATIBILITY",
    "CONTRACT_STATUS",
    "CONTRACT_VERSION",
    "CUSTODY_SEMANTICS",
    "FAILURE_CODES",
    "FIXTURE_CLASSIFICATION",
    "LINEAGE_RELATION",
    "MAX_RAW_BYTES",
    "PREFERENCE_CLASS",
    "PROFILE_ID",
    "PROFILE_VERSION",
    "SERIALIZATION_SEMANTICS",
    "V1_AUDIT_PURPOSE",
    "V1_STATUS",
    "V2_DESIGN_PURPOSE",
    "CandidateAPreferenceProfileV1",
    "ContractResolution",
    "ERA3V2Error",
    "V1AuditResult",
    "parse_candidate_a_preference_profile",
    "resolve_contract",
    "resolve_registered_source_instance",
    "validate_v1_for_audit",
)


_TOKEN = object()
_EXPECTED_FIELDS = (
    "profile_id",
    "profile_version",
    "acquisition_topology",
    "http_attempt_profile",
)


class ERA3V2Error(ValueError):
    """Stable fail-closed v2 reader or lifecycle error."""

    def __init__(self, code: str, *, pointer: str = "", detail: str = "") -> None:
        if code not in FAILURE_CODES:
            raise ValueError(f"unknown ER-A3-MIN v2 failure code {code!r}")
        self.code = code
        self.pointer = pointer
        self.detail = detail
        message = code
        if pointer:
            message += f" at {pointer}"
        if detail:
            message += f": {detail}"
        super().__init__(message)


def _fail(code: str, pointer: str, detail: str) -> None:
    raise ERA3V2Error(code, pointer=pointer, detail=detail)


@dataclass(frozen=True, slots=True, init=False)
class CandidateAPreferenceProfileV1:
    """One nominal, sealed semantic result constructed only after whole-record validation."""

    profile_id: str
    profile_version: int
    acquisition_topology: str
    http_attempt_profile: str
    preference_class: str
    custody_semantics: str
    serialization_semantics: str
    compatibility: str
    authority_effect: str
    next_stage_authorized: bool

    def __init__(self, *, _token: object) -> None:
        if _token is not _TOKEN:
            raise TypeError(
                "CandidateAPreferenceProfileV1 is created only by "
                "parse_candidate_a_preference_profile"
            )
        object.__setattr__(self, "profile_id", PROFILE_ID)
        object.__setattr__(self, "profile_version", PROFILE_VERSION)
        object.__setattr__(self, "acquisition_topology", _ACQUISITION_TOPOLOGY)
        object.__setattr__(self, "http_attempt_profile", _HTTP_ATTEMPT_PROFILE)
        object.__setattr__(self, "preference_class", PREFERENCE_CLASS)
        object.__setattr__(self, "custody_semantics", CUSTODY_SEMANTICS)
        object.__setattr__(self, "serialization_semantics", SERIALIZATION_SEMANTICS)
        object.__setattr__(self, "compatibility", COMPATIBILITY)
        object.__setattr__(self, "authority_effect", AUTHORITY_EFFECT)
        object.__setattr__(self, "next_stage_authorized", False)


@dataclass(frozen=True, slots=True)
class ContractResolution:
    version: int
    purpose: str
    lifecycle_status: str
    lineage_relation: str
    normal_use_available: bool
    audit_reproduction_only: bool
    compatibility: str
    authority_effect: str
    next_stage_authorized: bool


@dataclass(frozen=True, slots=True)
class V1AuditResult:
    lifecycle_status: str
    purpose: str
    raw_sha256: str
    package_shape: str
    admission_effect: str
    authority_effect: str
    next_stage_authorized: bool


def _parse(raw: bytes) -> dict[str, object]:
    if type(raw) is not bytes:
        raise TypeError("raw profile must be bytes")
    if len(raw) > MAX_RAW_BYTES:
        _fail("ER_A3_V2_RAW_TOO_LARGE", "/", f"maximum is {MAX_RAW_BYTES} bytes")
    if raw.startswith(b"\xef\xbb\xbf"):
        _fail("ER_A3_V2_JSON_BOM", "/", "UTF-8 BOM is forbidden")
    try:
        text = raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        _fail("ER_A3_V2_JSON_INVALID_UTF8", "/", f"invalid byte at offset {exc.start}")

    def no_duplicates(pairs: list[tuple[str, object]]) -> dict[str, object]:
        result: dict[str, object] = {}
        for key, value in pairs:
            if key in result:
                _fail("ER_A3_V2_JSON_DUPLICATE_KEY", f"/{key}", "duplicate key")
            result[key] = value
        return result

    def reject_constant(token: str) -> object:
        _fail("ER_A3_V2_JSON_INVALID", "/", f"forbidden number {token}")

    try:
        value = json.loads(
            text,
            object_pairs_hook=no_duplicates,
            parse_constant=reject_constant,
        )
    except ERA3V2Error:
        raise
    except (json.JSONDecodeError, UnicodeError) as exc:
        _fail("ER_A3_V2_JSON_INVALID", "/", str(exc))
    if type(value) is not dict:
        _fail("ER_A3_V2_JSON_INVALID", "/", "expected object")
    return value


def parse_candidate_a_preference_profile(raw: bytes) -> CandidateAPreferenceProfileV1:
    """Validate the entire closed v2 wire record before returning one sealed variant."""

    value = _parse(raw)
    actual = set(value)
    expected = set(_EXPECTED_FIELDS)
    if actual != expected:
        _fail(
            "ER_A3_V2_PROFILE_FIELD_SET",
            "/",
            f"field set mismatch; missing={sorted(expected - actual)}, extra={sorted(actual - expected)}",
        )
    if type(value["profile_id"]) is not str or value["profile_id"] != PROFILE_ID:
        _fail("ER_A3_V2_PROFILE_ID_UNSUPPORTED", "/profile_id", "unsupported profile")
    if type(value["profile_version"]) is not int or value["profile_version"] != PROFILE_VERSION:
        _fail(
            "ER_A3_V2_PROFILE_VERSION_UNSUPPORTED",
            "/profile_version",
            "unsupported complete-profile version",
        )
    expected_values = (
        ("acquisition_topology", _ACQUISITION_TOPOLOGY),
        ("http_attempt_profile", _HTTP_ATTEMPT_PROFILE),
    )
    for field, expected_value in expected_values:
        if type(value[field]) is not str or value[field] != expected_value:
            _fail(
                "ER_A3_V2_PROFILE_VALUE_INVALID",
                f"/{field}",
                "value is not a member of the sealed profile",
            )
    return CandidateAPreferenceProfileV1(_token=_TOKEN)


def resolve_contract(version: int, purpose: str) -> ContractResolution:
    """Resolve contract definitions only; never resolve or publish a source instance."""

    if type(version) is not int or version not in {1, 2}:
        _fail("ER_A3_CONTRACT_VERSION_UNSUPPORTED", "/version", "supported versions are 1 and 2")
    if type(purpose) is not str:
        _fail("ER_A3_CONTRACT_PURPOSE_UNSUPPORTED", "/purpose", "purpose must be a string")
    if version == 1:
        if purpose != V1_AUDIT_PURPOSE:
            _fail("ER_A3_V1_RETIRED_UNISSUED", "/version", "v1 is audit-reproduction-only")
        return ContractResolution(
            version=1,
            purpose=purpose,
            lifecycle_status=V1_STATUS,
            lineage_relation="HISTORICAL_ONLY",
            normal_use_available=False,
            audit_reproduction_only=True,
            compatibility=COMPATIBILITY,
            authority_effect=AUTHORITY_EFFECT,
            next_stage_authorized=False,
        )
    if purpose != V2_DESIGN_PURPOSE:
        _fail(
            "ER_A3_CONTRACT_PURPOSE_UNSUPPORTED",
            "/purpose",
            "v2 is available only for non-authorizing design-contract use",
        )
    return ContractResolution(
        version=2,
        purpose=purpose,
        lifecycle_status=CONTRACT_STATUS,
        lineage_relation=LINEAGE_RELATION,
        normal_use_available=True,
        audit_reproduction_only=False,
        compatibility=COMPATIBILITY,
        authority_effect=AUTHORITY_EFFECT,
        next_stage_authorized=False,
    )


def validate_v1_for_audit(raw: bytes) -> V1AuditResult:
    """Run the immutable v1 validator while making the audit-only effect explicit."""

    resolve_contract(1, V1_AUDIT_PURPOSE)
    verified = _verify_v1_package(raw)
    return V1AuditResult(
        lifecycle_status=V1_STATUS,
        purpose=V1_AUDIT_PURPOSE,
        raw_sha256=verified.raw_sha256,
        package_shape=verified.package_shape,
        admission_effect="NONE",
        authority_effect=AUTHORITY_EFFECT,
        next_stage_authorized=False,
    )


def resolve_registered_source_instance(version: int) -> None:
    """Return the intentionally empty registered-instance state for known contract versions."""

    if type(version) is not int or version not in {1, 2}:
        _fail("ER_A3_CONTRACT_VERSION_UNSUPPORTED", "/version", "supported versions are 1 and 2")
    return None
