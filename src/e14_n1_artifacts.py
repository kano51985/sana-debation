"""Pure lifecycle-v2 content verification for the E14 P3-N1 profile.

The module deliberately has no builder, generic JSON normalizer, filesystem-backed schema loader,
ambient clock, network integration, persistence, key handling, or authority-granting operation.
It accepts one nominal route and verifies content only.  Operational use remains outside I0.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import hmac
import re
from types import MappingProxyType
from typing import Any, Final


SCHEMA: Final = "sana.e14.n1.lifecycle-artifact.v2"
PROFILE_KIND: Final = "P3_N1_CONTROL_CLOSURE_V1"
SELECTOR: Final = "N1_LIFECYCLE_ARTIFACT_V2"
MEDIA_TYPE: Final = "application/vnd.sana.e14.n1-lifecycle-artifact-v2+json"
DOMAIN: Final = b"sana.e14.n1.lifecycle-artifact.v2\n"
ROOT_PREFIX: Final = "sha256-jcs-e14-n1-v2:"

MAX_RAW_BYTES: Final = 262_144
MAX_DEPTH: Final = 12
MAX_NODES: Final = 4_096
MAX_MEMBERS: Final = 2_048
MAX_MEMBERS_PER_OBJECT: Final = 128
MAX_KEY_CHARS: Final = 160
MAX_STRING_SCALARS: Final = 1_024
MAX_STRING_UTF8_BYTES: Final = 4_096
MAX_SAFE_INTEGER: Final = 9_007_199_254_740_991

ARTIFACT_KINDS: Final = (
    "N1_ISSUER_POLICY",
    "N1_PROFILE_QUALIFIED",
    "N1_OUTPUT_RESERVED",
    "N1_CONTAINER_PREPARED",
    "G8_N1_RUN_AUTHORIZED",
    "N1_RUN_EVIDENCE_CANDIDATE",
    "G9_N1_TERMINAL",
)

FAILURE_CODES: Final = (
    "N1_ROUTE_SELECTOR_MISSING",
    "N1_ROUTE_SELECTOR_UNSUPPORTED",
    "N1_ROUTE_MEDIA_TYPE_MISMATCH",
    "N1_RAW_TOO_LARGE",
    "N1_JSON_BOM",
    "N1_JSON_INVALID_UTF8",
    "N1_JSON_SYNTAX",
    "N1_JSON_TRAILING_DATA",
    "N1_JSON_ARRAY_FORBIDDEN",
    "N1_JSON_DUPLICATE_KEY",
    "N1_JSON_DEPTH_LIMIT",
    "N1_JSON_NODE_LIMIT",
    "N1_JSON_MEMBER_LIMIT",
    "N1_JSON_OBJECT_MEMBER_LIMIT",
    "N1_JSON_KEY_NON_ASCII",
    "N1_JSON_KEY_TOO_LONG",
    "N1_JSON_STRING_SCALAR_LIMIT",
    "N1_JSON_STRING_UTF8_LIMIT",
    "N1_JSON_SURROGATE_INVALID",
    "N1_JSON_NUMBER_FORBIDDEN",
    "N1_JSON_INTEGER_RANGE",
    "N1_ENVELOPE_FIELD_SET",
    "N1_SCHEMA_UNSUPPORTED",
    "N1_PROFILE_KIND_MISMATCH",
    "N1_ARTIFACT_KIND_UNSUPPORTED",
    "N1_PAYLOAD_INVALID",
    "N1_CONTENT_ROOT_FORMAT",
    "N1_CONTENT_ROOT_MISMATCH",
)

__all__ = (
    "DOMAIN",
    "FAILURE_CODES",
    "MEDIA_TYPE",
    "PROFILE_KIND",
    "ROOT_PREFIX",
    "SCHEMA",
    "SELECTOR",
    "LifecycleV2Route",
    "N1ArtifactError",
    "N1LifecycleV2Root",
    "RevocationSnapshot",
    "UseEvaluation",
    "VerifiedLifecycleArtifactV2",
    "evaluate_use",
    "verify_content",
)


class N1ArtifactError(ValueError):
    """Stable typed verification failure; ``detail`` is diagnostic only."""

    def __init__(
        self,
        code: str,
        *,
        detail: str = "",
        byte_offset: int | None = None,
        pointer: str | None = None,
        limit: int | None = None,
        observed: int | None = None,
    ) -> None:
        if code not in FAILURE_CODES:
            raise ValueError(f"unknown N1 failure code {code!r}")
        self.code = code
        self.detail = detail
        self.byte_offset = byte_offset
        self.pointer = pointer
        self.limit = limit
        self.observed = observed
        super().__init__(code if not detail else f"{code}: {detail}")


@dataclass(frozen=True, slots=True)
class LifecycleV2Route:
    selector: str | None
    media_type: str | None


_VERIFICATION_TOKEN = object()


@dataclass(frozen=True, slots=True, init=False)
class N1LifecycleV2Root:
    value: str

    def __init__(self, value: str, *, _token: object | None = None) -> None:
        if _token is not _VERIFICATION_TOKEN:
            raise TypeError("N1LifecycleV2Root is created only by verify_content")
        object.__setattr__(self, "value", value)


@dataclass(frozen=True, slots=True, init=False)
class VerifiedLifecycleArtifactV2:
    schema: str
    artifact_kind: str
    profile_kind: str
    content_root: N1LifecycleV2Root
    payload: Mapping[str, Any]
    commitment_bytes: bytes

    def __init__(
        self,
        *,
        schema: str,
        artifact_kind: str,
        profile_kind: str,
        content_root: N1LifecycleV2Root,
        payload: Mapping[str, Any],
        commitment_bytes: bytes,
        _token: object | None = None,
    ) -> None:
        if _token is not _VERIFICATION_TOKEN:
            raise TypeError("VerifiedLifecycleArtifactV2 is created only by verify_content")
        object.__setattr__(self, "schema", schema)
        object.__setattr__(self, "artifact_kind", artifact_kind)
        object.__setattr__(self, "profile_kind", profile_kind)
        object.__setattr__(self, "content_root", content_root)
        object.__setattr__(self, "payload", payload)
        object.__setattr__(self, "commitment_bytes", commitment_bytes)


@dataclass(frozen=True, slots=True)
class RevocationSnapshot:
    """Explicit immutable revocation input; an empty snapshot revokes nothing."""

    revoked_content_roots: frozenset[str] = frozenset()
    minimum_epoch_by_policy: tuple[tuple[str, int], ...] = ()

    def __post_init__(self) -> None:
        seen: set[str] = set()
        for policy_root, epoch in self.minimum_epoch_by_policy:
            if policy_root in seen:
                raise ValueError("duplicate policy root in revocation snapshot")
            if not _TYPED_ROOT_RE.fullmatch(policy_root):
                raise ValueError("invalid policy root in revocation snapshot")
            if type(epoch) is not int or not 0 <= epoch <= MAX_SAFE_INTEGER:
                raise ValueError("invalid epoch in revocation snapshot")
            seen.add(policy_root)
        if any(not _TYPED_ROOT_RE.fullmatch(root) for root in self.revoked_content_roots):
            raise ValueError("invalid revoked content root")

    def minimum_epoch(self, policy_root: str) -> int | None:
        for candidate, epoch in self.minimum_epoch_by_policy:
            if candidate == policy_root:
                return epoch
        return None


@dataclass(frozen=True, slots=True)
class UseEvaluation:
    status: str
    reason: str | None = None


_TYPED_ROOT_RE = re.compile(r"^sha256-jcs-e14-n1-v2:[0-9a-f]{64}$")
_SHA256_RE = re.compile(r"^[0-9A-F]{64}$")
_IDENTIFIER_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]*$")
_MAP_KEY_RE = re.compile(r"^[a-z][a-z0-9_]*$")
_TIMESTAMP_RE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$")
_DETAIL_RE = re.compile(r"^N1_[A-Z0-9_]+$")
_INTEGER_TOKEN_RE = re.compile(rb"(?:0|-[1-9][0-9]{0,15}|[1-9][0-9]{0,15})\Z")


class _RawParser:
    _WS = b" \t\r\n"

    def __init__(self, raw: bytes) -> None:
        self.raw = raw
        self.length = len(raw)
        self.index = 0
        self.nodes = 0
        self.members = 0

    def parse(self) -> Any:
        self._skip_ws()
        value = self._parse_value(1)
        self._skip_ws()
        if self.index != self.length:
            self._check_utf8_at(self.index)
            self._raise("N1_JSON_TRAILING_DATA", self.index)
        return value

    def _raise(
        self,
        code: str,
        offset: int,
        *,
        detail: str = "",
        limit: int | None = None,
        observed: int | None = None,
    ) -> None:
        raise N1ArtifactError(
            code,
            detail=detail,
            byte_offset=offset,
            limit=limit,
            observed=observed,
        )

    def _skip_ws(self) -> None:
        while self.index < self.length and self.raw[self.index] in self._WS:
            self.index += 1

    def _syntax(self, offset: int, detail: str) -> None:
        self._check_utf8_at(offset)
        self._raise("N1_JSON_SYNTAX", offset, detail=detail)

    def _check_utf8_at(self, offset: int) -> tuple[str, int] | None:
        if offset >= self.length or self.raw[offset] < 0x80:
            return None
        lead = self.raw[offset]
        if 0xC2 <= lead <= 0xDF:
            width = 2
        elif 0xE0 <= lead <= 0xEF:
            width = 3
        elif 0xF0 <= lead <= 0xF4:
            width = 4
        else:
            self._raise("N1_JSON_INVALID_UTF8", offset)
        token = self.raw[offset : offset + width]
        try:
            character = token.decode("utf-8")
        except UnicodeDecodeError as error:
            self._raise("N1_JSON_INVALID_UTF8", offset + error.start)
        if len(token) != width or len(character) != 1:
            self._raise("N1_JSON_INVALID_UTF8", offset)
        return character, width

    def _parse_value(self, depth: int) -> Any:
        if self.index >= self.length:
            self._syntax(self.index, "expected value")
        if depth > MAX_DEPTH:
            self._raise(
                "N1_JSON_DEPTH_LIMIT",
                self.index,
                limit=MAX_DEPTH,
                observed=depth,
            )
        self.nodes += 1
        if self.nodes > MAX_NODES:
            self._raise(
                "N1_JSON_NODE_LIMIT",
                self.index,
                limit=MAX_NODES,
                observed=self.nodes,
            )

        token = self.raw[self.index]
        if token == 0x7B:  # {
            return self._parse_object(depth)
        if token == 0x5B:  # [
            self._raise("N1_JSON_ARRAY_FORBIDDEN", self.index)
        if token == 0x22:  # "
            return self._parse_string(is_key=False)
        if token == 0x74:
            return self._parse_literal(b"true", True)
        if token == 0x66:
            return self._parse_literal(b"false", False)
        if token == 0x6E:
            return self._parse_literal(b"null", None)
        if token == 0x2D or 0x30 <= token <= 0x39:
            return self._parse_integer()
        self._syntax(self.index, "unexpected token")

    def _parse_object(self, depth: int) -> dict[str, Any]:
        self.index += 1
        result: dict[str, Any] = {}
        object_members = 0
        self._skip_ws()
        if self.index < self.length and self.raw[self.index] == 0x7D:
            self.index += 1
            return result

        while True:
            if self.index >= self.length or self.raw[self.index] != 0x22:
                self._syntax(self.index, "expected object key")
            key_offset = self.index
            key = self._parse_string(is_key=True)
            object_members += 1
            self.members += 1
            if object_members > MAX_MEMBERS_PER_OBJECT:
                self._raise(
                    "N1_JSON_OBJECT_MEMBER_LIMIT",
                    key_offset,
                    limit=MAX_MEMBERS_PER_OBJECT,
                    observed=object_members,
                )
            if self.members > MAX_MEMBERS:
                self._raise(
                    "N1_JSON_MEMBER_LIMIT",
                    key_offset,
                    limit=MAX_MEMBERS,
                    observed=self.members,
                )
            if key in result:
                self._raise("N1_JSON_DUPLICATE_KEY", key_offset, detail=key)

            self._skip_ws()
            if self.index >= self.length or self.raw[self.index] != 0x3A:
                self._syntax(self.index, "expected colon")
            self.index += 1
            self._skip_ws()
            result[key] = self._parse_value(depth + 1)
            self._skip_ws()
            if self.index >= self.length:
                self._syntax(self.index, "unterminated object")
            delimiter = self.raw[self.index]
            if delimiter == 0x7D:
                self.index += 1
                return result
            if delimiter != 0x2C:
                self._syntax(self.index, "expected comma or object end")
            self.index += 1
            self._skip_ws()

    def _parse_string(self, *, is_key: bool) -> str:
        self.index += 1
        characters: list[str] = []
        scalar_count = 0
        utf8_count = 0
        while self.index < self.length:
            char_offset = self.index
            byte = self.raw[self.index]
            if byte == 0x22:
                self.index += 1
                return "".join(characters)
            if byte < 0x20:
                self._syntax(char_offset, "unescaped control character")

            if byte == 0x5C:
                character = self._parse_escape(char_offset)
            elif byte < 0x80:
                character = chr(byte)
                self.index += 1
            else:
                decoded = self._check_utf8_at(self.index)
                if decoded is None:
                    raise AssertionError("non-ASCII byte did not decode")
                character, width = decoded
                self.index += width

            scalar_count += 1
            utf8_count += len(character.encode("utf-8"))
            if is_key:
                if ord(character) > 0x7F:
                    self._raise("N1_JSON_KEY_NON_ASCII", char_offset)
                if scalar_count > MAX_KEY_CHARS:
                    self._raise(
                        "N1_JSON_KEY_TOO_LONG",
                        char_offset,
                        limit=MAX_KEY_CHARS,
                        observed=scalar_count,
                    )
            else:
                if scalar_count > MAX_STRING_SCALARS:
                    self._raise(
                        "N1_JSON_STRING_SCALAR_LIMIT",
                        char_offset,
                        limit=MAX_STRING_SCALARS,
                        observed=scalar_count,
                    )
                if utf8_count > MAX_STRING_UTF8_BYTES:
                    self._raise(
                        "N1_JSON_STRING_UTF8_LIMIT",
                        char_offset,
                        limit=MAX_STRING_UTF8_BYTES,
                        observed=utf8_count,
                    )
            characters.append(character)
        self._syntax(self.index, "unterminated string")

    def _parse_escape(self, escape_offset: int) -> str:
        self.index += 1
        if self.index >= self.length:
            self._syntax(self.index, "unterminated escape")
        marker = self.raw[self.index]
        self.index += 1
        simple = {
            0x22: '"',
            0x5C: "\\",
            0x2F: "/",
            0x62: "\b",
            0x66: "\f",
            0x6E: "\n",
            0x72: "\r",
            0x74: "\t",
        }
        if marker in simple:
            return simple[marker]
        if marker != 0x75:
            self._syntax(escape_offset, "invalid escape")
        first = self._read_hex_quad(escape_offset)
        if 0xD800 <= first <= 0xDBFF:
            if self.index + 6 > self.length or self.raw[self.index : self.index + 2] != b"\\u":
                self._raise("N1_JSON_SURROGATE_INVALID", escape_offset)
            self.index += 2
            second = self._read_hex_quad(escape_offset)
            if not 0xDC00 <= second <= 0xDFFF:
                self._raise("N1_JSON_SURROGATE_INVALID", escape_offset)
            scalar = 0x10000 + ((first - 0xD800) << 10) + (second - 0xDC00)
            return chr(scalar)
        if 0xDC00 <= first <= 0xDFFF:
            self._raise("N1_JSON_SURROGATE_INVALID", escape_offset)
        return chr(first)

    def _read_hex_quad(self, escape_offset: int) -> int:
        if self.index + 4 > self.length:
            self._syntax(escape_offset, "short unicode escape")
        token = self.raw[self.index : self.index + 4]
        if any(byte not in b"0123456789abcdefABCDEF" for byte in token):
            self._syntax(escape_offset, "invalid unicode escape")
        self.index += 4
        return int(token, 16)

    def _parse_literal(self, token: bytes, value: Any) -> Any:
        offset = self.index
        for delta, expected in enumerate(token):
            candidate = offset + delta
            if candidate >= self.length or self.raw[candidate] != expected:
                self._syntax(candidate, "invalid literal")
        self.index += len(token)
        return value

    def _parse_integer(self) -> int:
        offset = self.index
        while self.index < self.length and self.raw[self.index] not in b" \t\r\n,}":
            self.index += 1
        token = self.raw[offset : self.index]
        if not _INTEGER_TOKEN_RE.fullmatch(token):
            self._raise("N1_JSON_NUMBER_FORBIDDEN", self._number_failure_offset(token, offset))
        value = int(token)
        if not -MAX_SAFE_INTEGER <= value <= MAX_SAFE_INTEGER:
            magnitude = token[1:] if token.startswith(b"-") else token
            running = 0
            decisive = offset + (1 if token.startswith(b"-") else 0)
            for delta, byte in enumerate(magnitude):
                running = running * 10 + byte - 0x30
                decisive = offset + delta + (1 if token.startswith(b"-") else 0)
                if running > MAX_SAFE_INTEGER:
                    break
            self._raise(
                "N1_JSON_INTEGER_RANGE",
                decisive,
                limit=MAX_SAFE_INTEGER,
                observed=abs(value),
            )
        return value

    @staticmethod
    def _number_failure_offset(token: bytes, offset: int) -> int:
        index = 0
        if token.startswith(b"-"):
            index = 1
            if index >= len(token):
                return offset + index
            if token[index] == 0x30:
                return offset + index
        if index >= len(token) or not 0x30 <= token[index] <= 0x39:
            return offset + index
        if token[index] == 0x30 and index + 1 < len(token):
            return offset + index + 1
        digits = 0
        while index < len(token) and 0x30 <= token[index] <= 0x39:
            digits += 1
            if digits > 16:
                return offset + index
            index += 1
        return offset + index


def _parse_raw(raw: bytes) -> Any:
    if len(raw) > MAX_RAW_BYTES:
        raise N1ArtifactError(
            "N1_RAW_TOO_LARGE",
            byte_offset=MAX_RAW_BYTES,
            limit=MAX_RAW_BYTES,
            observed=len(raw),
        )
    if raw.startswith(b"\xef\xbb\xbf"):
        raise N1ArtifactError("N1_JSON_BOM", byte_offset=0)
    return _RawParser(raw).parse()


def _json_pointer(parent: str, name: str) -> str:
    escaped = name.replace("~", "~0").replace("/", "~1")
    return f"{parent}/{escaped}"


def _payload_error(pointer: str, detail: str) -> None:
    raise N1ArtifactError("N1_PAYLOAD_INVALID", pointer=pointer, detail=detail)


def _object_rule(fields: tuple[tuple[str, Any], ...]) -> tuple[str, tuple[tuple[str, Any], ...]]:
    return ("object", fields)


ROOT_RULE = ("root",)
SHA_RULE = ("sha256",)
IDENTIFIER_RULE = ("identifier",)
TIMESTAMP_RULE = ("timestamp",)
NONNEGATIVE_INTEGER_RULE = ("integer", 0, MAX_SAFE_INTEGER)
POSITIVE_INTEGER_RULE = ("integer", 1, MAX_SAFE_INTEGER)
ROOT_MAP_RULE = ("root_map",)

ROLE_MAP_RULE = _object_rule(
    (
        ("policy_issuer", IDENTIFIER_RULE),
        ("qualification_issuer", IDENTIFIER_RULE),
        ("g8_authorizer", IDENTIFIER_RULE),
        ("controller", IDENTIFIER_RULE),
        ("g9_finalizer", IDENTIFIER_RULE),
    )
)

PLATFORM_RULE = _object_rule(
    (
        ("host_os_build", IDENTIFIER_RULE),
        ("virtualization_backend", IDENTIFIER_RULE),
        ("docker_desktop_build", IDENTIFIER_RULE),
        ("engine_build", IDENTIFIER_RULE),
        ("containerd_build", IDENTIFIER_RULE),
        ("runc_build", IDENTIFIER_RULE),
        ("linux_kernel_build", IDENTIFIER_RULE),
        ("architecture", ("enum", ("amd64", "arm64"))),
        ("cgroup_mode", IDENTIFIER_RULE),
        ("security_options_root", ROOT_RULE),
        ("seccomp_policy_sha256", SHA_RULE),
    )
)

VALIDITY_RULE = _object_rule(
    (("issued_at", TIMESTAMP_RULE), ("not_before", TIMESTAMP_RULE), ("expires_at", TIMESTAMP_RULE))
)

PAYLOAD_RULES: Final = {
    "N1_ISSUER_POLICY": _object_rule(
        (
            ("scope", ("const", "A2")),
            ("roles", ROLE_MAP_RULE),
            ("environment_predicates_root", ROOT_RULE),
            ("evidence_predicates_root", ROOT_RULE),
            ("maximum_qualification_validity_seconds", POSITIVE_INTEGER_RULE),
            ("maximum_authorization_validity_seconds", POSITIVE_INTEGER_RULE),
            ("revocation_authority", IDENTIFIER_RULE),
            ("revocation_epoch", NONNEGATIVE_INTEGER_RULE),
            ("compatibility_profile", ("const", "N1_STRICT_MUTUAL_REJECTION_V1")),
        )
    ),
    "N1_PROFILE_QUALIFIED": _object_rule(
        (
            ("issuer_policy_root", ROOT_RULE),
            ("qualification_id", IDENTIFIER_RULE),
            ("issued_by", IDENTIFIER_RULE),
            ("validity", VALIDITY_RULE),
            ("revocation_epoch", NONNEGATIVE_INTEGER_RULE),
            ("dedicated_image_sha256", SHA_RULE),
            ("normative_final_view_manifest_root", ROOT_RULE),
            ("interpreter_sha256", SHA_RULE),
            ("closure_roots", ROOT_MAP_RULE),
            ("tool_roots", ROOT_MAP_RULE),
            ("platform", PLATFORM_RULE),
            ("negative_suite_root", ROOT_RULE),
            ("consumer_conformance_root", ROOT_RULE),
            ("authority_effect", ("const", "NONE")),
        )
    ),
    "N1_OUTPUT_RESERVED": _object_rule(
        (
            ("qualification_root", ROOT_RULE),
            ("reservation_id", IDENTIFIER_RULE),
            ("immutable_object_identity", IDENTIFIER_RULE),
            ("empty_initial_inventory_root", ROOT_RULE),
            ("lease_token_sha256", SHA_RULE),
            ("creation_event_root", ROOT_RULE),
            ("attachment_history_root", ROOT_RULE),
            ("exclusive_single_use", ("const", True)),
            ("authority_effect", ("const", "NONE")),
        )
    ),
    "N1_CONTAINER_PREPARED": _object_rule(
        (
            ("qualification_root", ROOT_RULE),
            ("output_reservation_root", ROOT_RULE),
            ("container_id", IDENTIFIER_RULE),
            ("container_config_sha256", SHA_RULE),
            ("dedicated_image_sha256", SHA_RULE),
            ("launch_root", ROOT_RULE),
            ("mount_view_root", ROOT_RULE),
            ("environment_root", ROOT_RULE),
            ("platform_root", ROOT_RULE),
            ("guest_execution_during_prepare", ("const", False)),
            ("unqualified_hook_execution", ("const", False)),
            ("exclusive_start_controller", IDENTIFIER_RULE),
            ("state", ("const", "STOPPED_NOT_AUTHORIZED")),
            ("authority_effect", ("const", "NONE")),
        )
    ),
    "G8_N1_RUN_AUTHORIZED": _object_rule(
        (
            ("issuer_policy_root", ROOT_RULE),
            ("qualification_root", ROOT_RULE),
            ("output_reservation_root", ROOT_RULE),
            ("prepared_container_root", ROOT_RULE),
            ("authorization_id", IDENTIFIER_RULE),
            ("issued_by", IDENTIFIER_RULE),
            ("fresh_run_nonce_sha256", SHA_RULE),
            ("request_id", IDENTIFIER_RULE),
            ("input_roots", ROOT_MAP_RULE),
            ("g1_g6_roots", ROOT_MAP_RULE),
            ("stopped_container_id", IDENTIFIER_RULE),
            ("container_config_sha256", SHA_RULE),
            ("launch_root", ROOT_RULE),
            ("mount_view_root", ROOT_RULE),
            ("environment_root", ROOT_RULE),
            ("output_object_identity", IDENTIFIER_RULE),
            ("lease_token_sha256", SHA_RULE),
            ("controller_root", ROOT_RULE),
            ("finalizer_root", ROOT_RULE),
            ("platform_root", ROOT_RULE),
            ("validity", VALIDITY_RULE),
            ("run_sequence", POSITIVE_INTEGER_RULE),
            ("predecessor_final_record_root", ("root_or_genesis",)),
            ("single_use", ("const", True)),
            ("authority_effect", ("const", "START_ONCE")),
        )
    ),
    "N1_RUN_EVIDENCE_CANDIDATE": _object_rule(
        (
            ("authorization_root", ROOT_RULE),
            ("qualification_root", ROOT_RULE),
            ("run_nonce_sha256", SHA_RULE),
            ("request_id", IDENTIFIER_RULE),
            ("input_roots", ROOT_MAP_RULE),
            ("actual_container_id", IDENTIFIER_RULE),
            ("actual_launch_root", ROOT_RULE),
            ("actual_mount_view_root", ROOT_RULE),
            ("start_stop_exit_root", ROOT_RULE),
            ("network_observation_root", ROOT_RULE),
            ("process_observation_root", ROOT_RULE),
            ("resource_observation_root", ROOT_RULE),
            ("output_object_identity", IDENTIFIER_RULE),
            ("attachment_history_root", ROOT_RULE),
            ("initial_output_root", ROOT_RULE),
            ("final_output_root", ROOT_RULE),
            ("runner_evidence_root", ROOT_RULE),
            ("controller_evidence_root", ROOT_RULE),
            ("guest_authority_claim", ("const", False)),
            ("authority_effect", ("const", "NONE")),
        )
    ),
    "G9_N1_TERMINAL": _object_rule(
        (
            ("issuer_policy_root", ROOT_RULE),
            ("qualification_root", ROOT_RULE),
            ("authorization_root", ROOT_RULE),
            ("candidate_root", ROOT_RULE),
            ("finalizer_root", ROOT_RULE),
            ("ledger_head_before", ("root_or_genesis",)),
            ("ledger_head_after", ROOT_RULE),
            ("nonce_single_use_verified", ("boolean",)),
            ("predecessor_verified", ("boolean",)),
            ("qualification_current", ("boolean",)),
            ("revocation_clear", ("boolean",)),
            ("candidate_unique_fresh", ("boolean",)),
            ("container_identity_verified", ("boolean",)),
            ("output_identity_verified", ("boolean",)),
            ("evidence_complete", ("boolean",)),
            (
                "terminal_outcome",
                ("enum", ("N1_FINAL_PASS", "N1_FINAL_DENY", "N1_INDETERMINATE_BLOCK")),
            ),
            ("detail_code", ("detail_or_null",)),
            ("authority_effect", ("const", "ADMISSION_TERMINAL")),
        )
    ),
}


def _validate_rule(value: Any, rule: tuple[Any, ...], pointer: str) -> None:
    kind = rule[0]
    if kind == "object":
        if type(value) is not dict:
            _payload_error(pointer, "expected object")
        fields = rule[1]
        expected = tuple(name for name, _ in fields)
        missing = [name for name in expected if name not in value]
        if missing:
            _payload_error(_json_pointer(pointer, missing[0]), "missing required field")
        extras = sorted(set(value) - set(expected))
        if extras:
            _payload_error(_json_pointer(pointer, extras[0]), "unknown field")
        for name, child_rule in fields:
            _validate_rule(value[name], child_rule, _json_pointer(pointer, name))
        return
    if kind == "const":
        if type(value) is not type(rule[1]) or value != rule[1]:
            _payload_error(pointer, "constant mismatch")
        return
    if kind == "enum":
        if type(value) is not str or value not in rule[1]:
            _payload_error(pointer, "enum mismatch")
        return
    if kind == "root":
        if type(value) is not str or not _TYPED_ROOT_RE.fullmatch(value):
            _payload_error(pointer, "invalid typed root")
        return
    if kind == "sha256":
        if type(value) is not str or not _SHA256_RE.fullmatch(value):
            _payload_error(pointer, "invalid SHA-256")
        return
    if kind == "identifier":
        if (
            type(value) is not str
            or not 1 <= len(value) <= 160
            or not _IDENTIFIER_RE.fullmatch(value)
        ):
            _payload_error(pointer, "invalid identifier")
        return
    if kind == "timestamp":
        if type(value) is not str or not _valid_timestamp(value):
            _payload_error(pointer, "invalid canonical UTC timestamp")
        return
    if kind == "integer":
        if type(value) is not int or not rule[1] <= value <= rule[2]:
            _payload_error(pointer, "integer outside allowed range")
        return
    if kind == "boolean":
        if type(value) is not bool:
            _payload_error(pointer, "expected boolean")
        return
    if kind == "root_map":
        if type(value) is not dict or not 1 <= len(value) <= 128:
            _payload_error(pointer, "invalid root map size")
        for name in sorted(value):
            child_pointer = _json_pointer(pointer, name)
            if len(name) > 160 or not _MAP_KEY_RE.fullmatch(name):
                _payload_error(child_pointer, "invalid root-map key")
            _validate_rule(value[name], ROOT_RULE, child_pointer)
        return
    if kind == "root_or_genesis":
        if value != "GENESIS" and (type(value) is not str or not _TYPED_ROOT_RE.fullmatch(value)):
            _payload_error(pointer, "expected typed root or GENESIS")
        return
    if kind == "detail_or_null":
        if value is not None and (
            type(value) is not str or len(value) > 96 or not _DETAIL_RE.fullmatch(value)
        ):
            _payload_error(pointer, "invalid terminal detail code")
        return
    raise AssertionError(f"unknown embedded rule {kind!r}")


def _valid_timestamp(value: str) -> bool:
    if not _TIMESTAMP_RE.fullmatch(value):
        return False
    try:
        datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        return False
    return True


def _encode_string(value: str) -> bytes:
    result = bytearray(b'"')
    short = {
        '"': b'\\"',
        "\\": b"\\\\",
        "\b": b"\\b",
        "\t": b"\\t",
        "\n": b"\\n",
        "\f": b"\\f",
        "\r": b"\\r",
    }
    for character in value:
        codepoint = ord(character)
        if 0xD800 <= codepoint <= 0xDFFF:
            raise ValueError("surrogate is outside N1-V2-CANON")
        if character in short:
            result.extend(short[character])
        elif codepoint < 0x20:
            result.extend(f"\\u{codepoint:04x}".encode("ascii"))
        else:
            result.extend(character.encode("utf-8"))
    result.append(0x22)
    return bytes(result)


def _canonical_bytes(value: Any) -> bytes:
    if value is None:
        return b"null"
    if value is True:
        return b"true"
    if value is False:
        return b"false"
    if type(value) is int:
        if not -MAX_SAFE_INTEGER <= value <= MAX_SAFE_INTEGER:
            raise ValueError("integer is outside N1-V2-CANON")
        return str(value).encode("ascii")
    if type(value) is str:
        return _encode_string(value)
    if isinstance(value, Mapping):
        keys = list(value)
        if any(type(key) is not str or not key.isascii() for key in keys):
            raise ValueError("object key is outside N1-V2-CANON")
        encoded = []
        for key in sorted(keys):
            encoded.append(_encode_string(key) + b":" + _canonical_bytes(value[key]))
        return b"{" + b",".join(encoded) + b"}"
    raise ValueError("value is outside N1-V2-CANON")


def _deep_freeze(value: Any) -> Any:
    if type(value) is dict:
        return MappingProxyType({key: _deep_freeze(child) for key, child in value.items()})
    return value


def _check_route(route: LifecycleV2Route | None) -> None:
    if route is None or route.selector is None or route.selector == "":
        raise N1ArtifactError("N1_ROUTE_SELECTOR_MISSING")
    if route.selector != SELECTOR:
        raise N1ArtifactError("N1_ROUTE_SELECTOR_UNSUPPORTED")
    if route.media_type != MEDIA_TYPE:
        raise N1ArtifactError("N1_ROUTE_MEDIA_TYPE_MISMATCH")


def _check_envelope_fields(parsed: Any) -> dict[str, Any]:
    if type(parsed) is not dict:
        raise N1ArtifactError(
            "N1_ENVELOPE_FIELD_SET", pointer="", detail="envelope must be an object"
        )
    expected = ("schema", "artifact_kind", "profile_kind", "content_root", "payload")
    missing = [name for name in expected if name not in parsed]
    if missing:
        raise N1ArtifactError(
            "N1_ENVELOPE_FIELD_SET",
            pointer=_json_pointer("", missing[0]),
            detail="missing required field",
        )
    extras = sorted(set(parsed) - set(expected))
    if extras:
        raise N1ArtifactError(
            "N1_ENVELOPE_FIELD_SET",
            pointer=_json_pointer("", extras[0]),
            detail="unknown field",
        )
    return parsed


def verify_content(
    raw_bytes: bytes,
    explicit_route: LifecycleV2Route | None,
) -> VerifiedLifecycleArtifactV2:
    """Verify one lifecycle-v2 byte string without consulting ambient state."""

    _check_route(explicit_route)
    if type(raw_bytes) is not bytes:
        raise TypeError("raw_bytes must be bytes")
    envelope = _check_envelope_fields(_parse_raw(raw_bytes))

    if envelope["schema"] != SCHEMA:
        raise N1ArtifactError("N1_SCHEMA_UNSUPPORTED", pointer="/schema")
    if envelope["profile_kind"] != PROFILE_KIND:
        raise N1ArtifactError("N1_PROFILE_KIND_MISMATCH", pointer="/profile_kind")
    artifact_kind = envelope["artifact_kind"]
    if type(artifact_kind) is not str or artifact_kind not in PAYLOAD_RULES:
        raise N1ArtifactError("N1_ARTIFACT_KIND_UNSUPPORTED", pointer="/artifact_kind")

    payload = envelope["payload"]
    _validate_rule(payload, PAYLOAD_RULES[artifact_kind], "/payload")

    presented_root = envelope["content_root"]
    if type(presented_root) is not str or not _TYPED_ROOT_RE.fullmatch(presented_root):
        raise N1ArtifactError("N1_CONTENT_ROOT_FORMAT", pointer="/content_root")

    commitment = {
        "schema": envelope["schema"],
        "artifact_kind": artifact_kind,
        "profile_kind": envelope["profile_kind"],
        "payload": payload,
    }
    commitment_bytes = _canonical_bytes(commitment)
    expected_root = ROOT_PREFIX + hashlib.sha256(DOMAIN + commitment_bytes).hexdigest()
    if not hmac.compare_digest(presented_root, expected_root):
        raise N1ArtifactError("N1_CONTENT_ROOT_MISMATCH", pointer="/content_root")

    return VerifiedLifecycleArtifactV2(
        schema=SCHEMA,
        artifact_kind=artifact_kind,
        profile_kind=PROFILE_KIND,
        content_root=N1LifecycleV2Root(presented_root, _token=_VERIFICATION_TOKEN),
        payload=_deep_freeze(payload),
        commitment_bytes=commitment_bytes,
        _token=_VERIFICATION_TOKEN,
    )


def _parse_timestamp(value: str) -> datetime:
    if not _valid_timestamp(value):
        raise ValueError("now_utc must be a canonical UTC timestamp")
    return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def evaluate_use(
    verified: VerifiedLifecycleArtifactV2,
    now_utc: str,
    revocation: RevocationSnapshot,
) -> UseEvaluation:
    """Evaluate explicit validity/revocation inputs; this result grants no authority."""

    if type(verified) is not VerifiedLifecycleArtifactV2:
        raise TypeError("verified must be VerifiedLifecycleArtifactV2")
    if type(revocation) is not RevocationSnapshot:
        raise TypeError("revocation must be RevocationSnapshot")
    now = _parse_timestamp(now_utc)
    payload = verified.payload

    referenced_roots = {verified.content_root.value}
    for name in ("issuer_policy_root", "qualification_root"):
        candidate = payload.get(name)
        if isinstance(candidate, str) and _TYPED_ROOT_RE.fullmatch(candidate):
            referenced_roots.add(candidate)
    if referenced_roots.intersection(revocation.revoked_content_roots):
        return UseEvaluation("N1_USE_REVOKED", "content root revoked")

    policy_root = payload.get("issuer_policy_root")
    epoch = payload.get("revocation_epoch")
    if isinstance(policy_root, str) and type(epoch) is int:
        minimum = revocation.minimum_epoch(policy_root)
        if minimum is not None and epoch < minimum:
            return UseEvaluation("N1_USE_REVOKED", "revocation epoch is stale")

    validity = payload.get("validity")
    if isinstance(validity, Mapping):
        issued_at = _parse_timestamp(validity["issued_at"])
        not_before = _parse_timestamp(validity["not_before"])
        expires_at = _parse_timestamp(validity["expires_at"])
        if not issued_at <= not_before < expires_at:
            return UseEvaluation("N1_USE_INVALID_INTERVAL", "validity interval is inconsistent")
        if now < not_before:
            return UseEvaluation("N1_USE_NOT_YET_VALID", "before not_before")
        if now >= expires_at:
            return UseEvaluation("N1_USE_EXPIRED", "at or after expires_at")
    return UseEvaluation("N1_USE_VALID")
